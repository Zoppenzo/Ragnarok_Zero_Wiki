from __future__ import annotations

import html
import json
import re
import time
import unicodedata
import urllib.error
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from pathlib import Path

IDENTITY = Path('assets/client-monster-identity.js')
OUT = Path('assets/monster-zero-consensus.js')
RAGNADEX_URL = 'https://ragnadex.com/api/monsters.json'
TWROZ_URL = 'https://ragnarokzero.net/database/monsters/{id}'
PRONTERA_URL = 'https://roz.prontera.info/mobs/{slug}'
UA = 'Ragnarok-Zero-Wiki/2.0 (+https://github.com/Zoppenzo/Ragnarok_Zero_Wiki)'


class VisibleTextParser(HTMLParser):
    BLOCK = {'h1','h2','h3','h4','p','div','section','article','li','tr','td','th','br','table'}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in {'script','style','noscript'}:
            self.skip += 1
        if not self.skip and tag in self.BLOCK:
            self.parts.append('\n')
    def handle_endtag(self, tag):
        if tag in {'script','style','noscript'} and self.skip:
            self.skip -= 1
        if not self.skip and tag in self.BLOCK:
            self.parts.append('\n')
    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)
    def text(self) -> str:
        raw=''.join(self.parts)
        lines=[]
        for line in raw.splitlines():
            line=re.sub(r'\s+',' ',line).strip()
            if line:
                lines.append(line)
        return '\n'.join(lines)


class SectionTableParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.current_heading=''
        self.heading_tag=None
        self.heading_parts=[]
        self.in_table=False
        self.table_section=''
        self.in_cell=False
        self.cell_parts=[]
        self.row=[]
        self.tables=[]
        self.skip=0
    def handle_starttag(self, tag, attrs):
        if tag in {'script','style','noscript'}:
            self.skip += 1
            return
        if self.skip:
            return
        if tag in {'h1','h2','h3'}:
            self.heading_tag=tag
            self.heading_parts=[]
        elif tag=='table':
            self.in_table=True
            self.table_section=self.current_heading
            self.row=[]
        elif self.in_table and tag=='tr':
            self.row=[]
        elif self.in_table and tag in {'td','th'}:
            self.in_cell=True
            self.cell_parts=[]
    def handle_endtag(self, tag):
        if tag in {'script','style','noscript'} and self.skip:
            self.skip -= 1
            return
        if self.skip:
            return
        if self.heading_tag==tag:
            heading=re.sub(r'\s+',' ',' '.join(self.heading_parts)).strip()
            if heading:
                self.current_heading=heading
            self.heading_tag=None
            self.heading_parts=[]
        elif self.in_table and tag in {'td','th'} and self.in_cell:
            cell=re.sub(r'\s+',' ',' '.join(self.cell_parts)).strip()
            self.row.append(cell)
            self.in_cell=False
            self.cell_parts=[]
        elif self.in_table and tag=='tr':
            if self.row:
                self.tables.append((self.table_section,list(self.row)))
            self.row=[]
        elif tag=='table':
            self.in_table=False
    def handle_data(self, data):
        if self.skip:
            return
        if self.heading_tag:
            self.heading_parts.append(data)
        if self.in_cell:
            self.cell_parts.append(data)


def fetch(url: str, *, timeout: int = 25) -> str | None:
    req=urllib.request.Request(url,headers={'User-Agent':UA,'Accept':'text/html,application/json;q=0.9,*/*;q=0.8'})
    try:
        with urllib.request.urlopen(req,timeout=timeout) as r:
            return r.read().decode('utf-8','replace')
    except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError):
        return None


def visible_text(raw: str) -> str:
    p=VisibleTextParser(); p.feed(raw); return p.text()


def num(s):
    if s is None:
        return None
    s=str(s).strip().replace(',','')
    if not s or s in {'—','-','n/a','N/A','?','??','???'}:
        return None
    try:
        f=float(s)
        return int(f) if f.is_integer() else f
    except ValueError:
        return None


def first(pattern: str, text: str, flags=0):
    m=re.search(pattern,text,flags)
    return m.group(1) if m else None


def slugify(value: str) -> str:
    value=unicodedata.normalize('NFKD',value or '').encode('ascii','ignore').decode('ascii')
    value=value.lower().replace("'",'').replace('’','')
    value=re.sub(r'[^a-z0-9]+','-',value).strip('-')
    return value


SLUG_ALIASES={
    'farmiliar':'familiar','ork-warrior':'orc-warrior','ork-hero':'orc-hero',
    'knight-of-abyss':'abysmal-knight','c-tower-manager':'clock-tower-manager',
    'moonlight':'moonlight-flower','sword-fish':'swordfish','neraid':'nereid',
    'giant-honet':'giant-hornet','baphomet':'baphomet','golden-bug':'golden-thief-bug',
}


def parse_identity_ids() -> set[int]:
    s=IDENTITY.read_text(encoding='utf-8')
    m=re.search(r'window\.RZ_CLIENT_MONSTER_IDENTITY=(\{.*?\});',s,re.S)
    if not m:
        raise SystemExit('Could not parse client monster identity')
    obj=json.loads(m.group(1))
    return {int(v[0]) for v in obj.values() if isinstance(v,list) and v and str(v[0]).isdigit()}


def parse_twroz(mob_id: int, raw: str) -> dict:
    text=visible_text(raw)
    if not re.search(rf'(?m)^#?{mob_id}\b',text) and f'#{mob_id}' not in text:
        return {}
    out={'_source':'TWRoZ'}
    patterns={
        'level':r'(?m)^Level\s*$\n([\d,]+)', 'hp':r'(?m)^HP\s*$\n([\d,]+)',
        'baseExp':r'(?m)^Base EXP\s*$\n([\d,]+|—)', 'jobExp':r'(?m)^Job EXP\s*$\n([\d,]+|—)',
        'def':r'(?m)^DEF\s*$\n([\d,]+)', 'mdef':r'(?m)^MDEF\s*$\n([\d,]+)',
        'hit':r'(?m)^Hit \(100%\)\s*$\n([\d,]+)', 'flee':r'(?m)^Flee \(95%\)\s*$\n([\d,]+)',
        'str':r'(?m)^STR\s*$\n([\d,]+)', 'agi':r'(?m)^AGI\s*$\n([\d,]+)', 'vit':r'(?m)^VIT\s*$\n([\d,]+)',
        'int':r'(?m)^INT\s*$\n([\d,]+)', 'dex':r'(?m)^DEX\s*$\n([\d,]+)', 'luk':r'(?m)^LUK\s*$\n([\d,]+)',
    }
    for k,p in patterns.items(): out[k]=num(first(p,text))
    atk=first(r'(?m)^ATK\s*$\n([^\n]+)',text)
    if atk:
        m=re.match(r'([\d,]+)(?:\s*[–-]\s*([\d,]+))?$',atk.strip())
        if m:
            out['attackMin']=num(m.group(1)); out['attackMax']=num(m.group(2) or m.group(1))
    matk=first(r'(?m)^MATK\s*$\n([^\n]+)',text)
    if matk:
        m=re.match(r'([\d,]+)(?:\s*[–-]\s*([\d,]+))?$',matk.strip())
        if m:
            out['magicAttackMin']=num(m.group(1)); out['magicAttackMax']=num(m.group(2) or m.group(1))
    modes=[]
    known=['Aggressive','Physically attackable','Can move','Loots items','Detector','Detects Hidden','Angry',
           'Changes Target When Attacked','Changes Target on Melee','Cast Sensor','Cast Sensor (Idle)','Cast Sensor (Chase)',
           'Immune to knockback','Immune to Status Change']
    low=text.lower()
    for label in known:
        if label.lower() in low:
            modes.append(label.replace('Physically attackable','Physically Attackable').replace('Can move','Can Move').replace('Loots items','Loots Items'))
    out['modes']=modes
    # Drops: the rendered page is regular: item name, ID, drop rate.
    section=text.split('\nDrops',1)[1] if '\nDrops' in text else ''
    if section:
        section=re.split(r'\n(?:Skill AI|Spawns|Source)\b',section,1)[0]
        lines=section.splitlines()
        drops=[]; candidate=None; item_id=None
        ignore={'Image','ID:','Drop rate:'}
        for line in lines:
            if re.fullmatch(r'ID:\s*[\d,]+',line):
                item_id=int(line.split(':',1)[1].replace(',','').strip()); continue
            if re.fullmatch(r'Drop rate:\s*(?:\?+|[\d.]+)%',line):
                rate_txt=line.split(':',1)[1].strip().rstrip('%')
                rate=None if '?' in rate_txt else num(rate_txt)
                if candidate and item_id is not None:
                    drops.append({'itemId':item_id,'name':candidate,'rate':rate})
                candidate=None; item_id=None; continue
            if line.startswith('≈') or line.startswith('Drops (') or line in ignore:
                continue
            if not line.startswith('ID:') and not line.startswith('Drop rate:'):
                candidate=line
        out['drops']=drops
    return out


def parse_prontera(mob_id: int, raw: str) -> dict:
    text=visible_text(raw)
    if not re.search(rf'\bID\s+{mob_id}\b',text):
        return {}
    out={'_source':'Prontera'}
    patterns={
        'hp':r'(?m)^HP\s*$\n([\d,]+)', 'def':r'(?m)^DEF\s*$\n([\d,]+)', 'mdef':r'(?m)^MDEF\s*$\n([\d,]+)',
        'baseExp':r'(?m)^Base EXP\s*$\n([\d,]+|—)', 'jobExp':r'(?m)^Job EXP\s*$\n([\d,]+|—)',
        'hit':r'(?m)^Hit \(100%\)\s*$\n([\d,]+|—)', 'flee':r'(?m)^Flee \(95%\)\s*$\n([\d,]+|—)',
        'str':r'(?m)^STR\s*$\n([\d,]+)', 'agi':r'(?m)^AGI\s*$\n([\d,]+)', 'vit':r'(?m)^VIT\s*$\n([\d,]+)',
        'int':r'(?m)^INT\s*$\n([\d,]+)', 'dex':r'(?m)^DEX\s*$\n([\d,]+)', 'luk':r'(?m)^LUK\s*$\n([\d,]+)',
        'attackRange':r'(?m)^ATK Range \(cells\)\s*$\n([\d,]+|—)',
    }
    for k,p in patterns.items(): out[k]=num(first(p,text))
    out['attackMin']=num(first(r'(?m)^ATK Min\s*$\n([\d,]+|—)',text))
    out['attackMax']=num(first(r'(?m)^ATK Max\s*$\n([\d,]+|—)',text))
    out['_verified']={
        'combat': bool(re.search(r'Combat\s+Verified\b',text)),
        'experience': bool(re.search(r'Experience\s+Verified\b',text)),
        'primary': bool(re.search(r'Primary Stats\s+Verified\b',text)),
        'identity': bool(re.search(r'Identity\s+Verified\b',text)),
    }
    tp=SectionTableParser(); tp.feed(raw)
    drops=[]
    for section,row in tp.tables:
        if 'Drops' not in section or len(row)<2:
            continue
        name=re.sub(r'\s+',' ',row[0]).strip()
        if not name or name.lower()=='item':
            continue
        rate_m=re.search(r'([\d.]+)%',row[1])
        rate=num(rate_m.group(1)) if rate_m else None
        status='verified' if re.search(r'\bVerified\b',row[1]) and not re.search(r'\bUnconfirmed\b',row[1]) else ('unconfirmed' if 'Unconfirmed' in row[1] else 'unknown')
        drops.append({'name':name,'rate':rate,'status':status})
    out['drops']=drops
    return out


def normalize_name(s: str) -> str:
    s=unicodedata.normalize('NFKD',s or '').encode('ascii','ignore').decode('ascii').lower()
    s=re.sub(r'\(bound\)|\[costume\]','',s)
    return re.sub(r'[^a-z0-9]+','',s)


def source_value(source: dict, field: str):
    v=source.get(field)
    return v if isinstance(v,(int,float)) else None


def same(a,b):
    if isinstance(a,float) or isinstance(b,float):
        return abs(float(a)-float(b)) < 1e-9
    return a==b


def choose_field(field: str, ragna: dict, tw: dict, pro: dict) -> dict | None:
    values=[]
    rmap={'hp':'hp','def':'def','mdef':'mdef','baseExp':'basis_exp','jobExp':'job_exp','hit':'hit_100','flee':'flee_95',
          'str':'str','agi':'agi','vit':'vit','int':'int','dex':'dex','luk':'luk','attackRange':'angriffsweite'}
    rk=rmap.get(field)
    if rk and ragna.get(rk) is not None:
        verified=rk in set(ragna.get('zero_felder') or [])
        values.append(('RagnaDex',ragna.get(rk),verified,'zero-verified' if verified else 'unverified-fallback'))
    tv=source_value(tw,field)
    if tv is not None: values.append(('TWRoZ',tv,False,'zero-regional'))
    pv=source_value(pro,field)
    if pv is not None:
        group='combat' if field in {'hp','def','mdef','attackMin','attackMax','attackRange'} else ('experience' if field in {'baseExp','jobExp','hit','flee'} else 'primary')
        verified=bool((pro.get('_verified') or {}).get(group))
        values.append(('Prontera',pv,verified,'global-verified' if verified else 'zero-db-unconfirmed'))
    if field in {'attackMin','attackMax','magicAttackMin','magicAttackMax'}:
        # RagnaDex atk/matk are not the same min/max semantics; never import them here.
        pass
    if not values:
        return None
    verified_vals=[x for x in values if x[2]]
    pool=verified_vals or [x for x in values if x[0] != 'RagnaDex' or x[3] != 'unverified-fallback']
    if not pool:
        return None
    counts=Counter(str(x[1]) for x in pool)
    top,count=counts.most_common(1)[0]
    chosen=next(x for x in pool if str(x[1])==top)
    conflict=len({str(x[1]) for x in values})>1
    status='verified' if verified_vals else ('consensus' if count>=2 else chosen[3])
    return {'value':chosen[1],'status':status,'conflict':conflict,'sources':{x[0]:x[1] for x in values}}


def merge_drops(ragna: dict, tw: dict, pro: dict) -> list[dict]:
    by_key={}
    def add(source, rec, verified=False):
        name=str(rec.get('name') or '').strip(); iid=rec.get('itemId') or rec.get('item_id')
        key=f'id:{int(iid)}' if iid is not None else f'name:{normalize_name(name)}'
        if not key or key=='name:': return
        bucket=by_key.setdefault(key,{'itemId':int(iid) if iid is not None else None,'name':name,'sources':{},'verifiedSources':set()})
        if not bucket['name'] and name: bucket['name']=name
        bucket['sources'][source]=rec.get('rate')
        if verified: bucket['verifiedSources'].add(source)
    for d in tw.get('drops') or []: add('TWRoZ',d)
    # Match Prontera names onto an existing item ID where possible.
    existing_by_name={normalize_name(v['name']):k for k,v in by_key.items() if v.get('name')}
    for d in pro.get('drops') or []:
        k=existing_by_name.get(normalize_name(d.get('name') or ''))
        if k:
            by_key[k]['sources']['Prontera']=d.get('rate')
            if d.get('status')=='verified': by_key[k]['verifiedSources'].add('Prontera')
        else:
            add('Prontera',d,d.get('status')=='verified')
    for d in ragna.get('drops') or []:
        iid=d.get('item_id'); name=d.get('name') or ''
        k=f'id:{int(iid)}' if iid is not None else existing_by_name.get(normalize_name(name))
        if k in by_key:
            by_key[k]['sources']['RagnaDex']=d.get('rate')
        # Do not create RagnaDex-only drops: its unverified drop fallback may be Renewal.
    out=[]
    for b in by_key.values():
        vals=[(s,v) for s,v in b['sources'].items() if isinstance(v,(int,float))]
        chosen=None; status='unknown'
        verified=[(s,v) for s,v in vals if s in b['verifiedSources']]
        if verified:
            chosen=verified[0][1]; status='verified'
        elif vals:
            counts=Counter(str(v) for _,v in vals); top,count=counts.most_common(1)[0]
            if count>=2:
                chosen=next(v for _,v in vals if str(v)==top); status='consensus'
            elif 'TWRoZ' in b['sources'] and isinstance(b['sources']['TWRoZ'],(int,float)):
                chosen=b['sources']['TWRoZ']; status='zero-regional'
            elif 'Prontera' in b['sources'] and isinstance(b['sources']['Prontera'],(int,float)):
                chosen=b['sources']['Prontera']; status='zero-db-unconfirmed'
        conflict=len({str(v) for _,v in vals})>1
        out.append({'itemId':b['itemId'],'name':b['name'],'rate':chosen,'status':status,'conflict':conflict,'sources':b['sources']})
    out.sort(key=lambda d:(d['rate'] is None,-float(d['rate'] or 0),d['name']))
    return out


def prontera_candidates(name: str, aegis: str) -> list[str]:
    candidates=[]
    for raw in [name,aegis.replace('_',' ')]:
        s=slugify(raw); s=SLUG_ALIASES.get(s,s)
        if s and s not in candidates: candidates.append(s)
    return candidates


ids=parse_identity_ids()
raw=fetch(RAGNADEX_URL,timeout=45)
if not raw: raise SystemExit('RagnaDex API unavailable')
ragna_rows=json.loads(raw)
ragna={int(r['id']):r for r in ragna_rows if isinstance(r,dict) and r.get('id') is not None}

# Fetch the two additional Zero databases in parallel, but keep a small worker count.
def fetch_one(mid: int):
    r=ragna.get(mid,{})
    tw_raw=fetch(TWROZ_URL.format(id=mid))
    tw=parse_twroz(mid,tw_raw) if tw_raw else {}
    pro={}
    for slug in prontera_candidates(str(r.get('name') or r.get('aegis') or mid),str(r.get('aegis') or '')):
        p_raw=fetch(PRONTERA_URL.format(slug=slug))
        if p_raw:
            parsed=parse_prontera(mid,p_raw)
            if parsed:
                pro=parsed; pro['_slug']=slug; break
    return mid,tw,pro

fetched={}
with ThreadPoolExecutor(max_workers=5) as ex:
    futs={ex.submit(fetch_one,mid):mid for mid in sorted(ids)}
    for i,fut in enumerate(as_completed(futs),1):
        mid,tw,pro=fut.result(); fetched[mid]=(tw,pro)
        if i%40==0: print(f'Fetched {i}/{len(futs)} Zero monster pages')

fields=['hp','baseExp','jobExp','attackMin','attackMax','magicAttackMin','magicAttackMax','def','mdef','hit','flee','str','agi','vit','int','dex','luk','attackRange']
consensus={}; coverage=Counter(); conflicts=Counter(); pro_hits=0; tw_hits=0
for mid in sorted(ids):
    r=ragna.get(mid,{})
    tw,pro=fetched.get(mid,({},{}))
    tw_hits+=bool(tw); pro_hits+=bool(pro)
    rec={'fields':{},'drops':merge_drops(r,tw,pro),'modes':[]}
    for field in fields:
        meta=choose_field(field,r,tw,pro)
        if meta:
            rec['fields'][field]=meta; coverage[field]+=1; conflicts[field]+=bool(meta.get('conflict'))
    modes=[]
    for source_modes in [tw.get('modes') or [], r.get('merkmale') or []]:
        for mode in source_modes:
            mode=str(mode).strip()
            if mode and mode not in modes: modes.append(mode)
    rec['modes']=modes
    rec['sourceAvailability']={'RagnaDex':bool(r),'TWRoZ':bool(tw),'Prontera':bool(pro)}
    if rec['fields'] or rec['drops'] or rec['modes']:
        consensus[str(mid)]=rec

# Hard validation on Poring demonstrates the intended conflict handling.
p=consensus.get('1002') or {}
assert p.get('fields',{}).get('hp',{}).get('value')==55, p
assert p.get('fields',{}).get('attackMin',{}).get('value')==13, p
assert p.get('fields',{}).get('attackMax',{}).get('value')==17, p
jellopy=next((d for d in p.get('drops',[]) if d.get('itemId')==909),None)
assert jellopy and jellopy.get('rate')==70, jellopy
card=next((d for d in p.get('drops',[]) if d.get('itemId')==4001),None)
assert card and card.get('conflict') is True, card

meta={'sources':['RagnaDex','RagnarokZero.net / TWRoZ','Prontera.Info ROZ'],'policy':'Zero databases only; verified Global/Zero fields first, then Zero-source consensus, with conflicts preserved','monsters':len(consensus),'twrozPages':tw_hits,'pronteraPages':pro_hits,'coverage':dict(coverage),'conflicts':dict(conflicts)}
OUT.write_text(
    '// Cross-database Ragnarok Zero monster consensus. No Renewal/iRO/RateMyServer fallback is imported.\n'
    + 'window.RZ_MONSTER_ZERO_CONSENSUS=' + json.dumps(consensus,ensure_ascii=False,separators=(',',':'),sort_keys=True) + ';\n'
    + 'window.RZ_MONSTER_ZERO_CONSENSUS_META=' + json.dumps(meta,ensure_ascii=False,separators=(',',':'),sort_keys=True) + ';\n',
    encoding='utf-8'
)
print(json.dumps(meta,ensure_ascii=False,indent=2))
