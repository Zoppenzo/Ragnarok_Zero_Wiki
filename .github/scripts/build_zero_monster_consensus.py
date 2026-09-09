from __future__ import annotations

import json
import re
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
UA = 'Ragnarok-Zero-Wiki/2.1 (+https://github.com/Zoppenzo/Ragnarok_Zero_Wiki)'


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
            # Keep sibling inline spans separated: <span>HP</span><span>55</span> -> "HP 55".
            self.parts.append(' ' + data + ' ')
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
    if not s or s in {'—','-','n/a','N/A','?','??','???','unknown'}:
        return None
    try:
        f=float(s)
        return int(f) if f.is_integer() else f
    except ValueError:
        return None


def first(pattern: str, text: str, flags=0):
    m=re.search(pattern,text,flags)
    return m.group(1) if m else None


def label_number(text: str, label: str):
    # Values can be on the same line or the next line depending on the site's markup.
    return num(first(rf'(?im)^\s*{label}\s+([\d,]+|—)\b',text))


def slugify(value: str) -> str:
    value=unicodedata.normalize('NFKD',value or '').encode('ascii','ignore').decode('ascii')
    value=value.lower().replace("'",'').replace('’','')
    value=re.sub(r'[^a-z0-9]+','-',value).strip('-')
    return value


SLUG_ALIASES={
    'farmiliar':'familiar','ork-warrior':'orc-warrior','ork-hero':'orc-hero',
    'knight-of-abyss':'abysmal-knight','c-tower-manager':'clock-tower-manager',
    'moonlight':'moonlight-flower','sword-fish':'swordfish','neraid':'nereid',
    'giant-honet':'giant-hornet','golden-bug':'golden-thief-bug',
}


def parse_identity_ids() -> set[int]:
    s=IDENTITY.read_text(encoding='utf-8')
    m=re.search(r'window\.RZ_CLIENT_MONSTER_IDENTITY=(\{.*?\});',s,re.S)
    if not m:
        raise SystemExit('Could not parse client monster identity')
    obj=json.loads(m.group(1))
    return {int(v[0]) for v in obj.values() if isinstance(v,list) and v and str(v[0]).isdigit()}


def parse_range(value: str | None):
    if not value:
        return (None,None)
    m=re.match(r'\s*([\d,]+)(?:\s*[–-]\s*([\d,]+))?\s*$',value)
    if not m:
        return (None,None)
    lo=num(m.group(1)); hi=num(m.group(2) or m.group(1))
    return lo,hi


def parse_twroz(mob_id: int, raw: str) -> dict:
    text=visible_text(raw)
    if f'#{mob_id}' not in text:
        return {}
    out={'_source':'TWRoZ'}
    labels={
        'level':'Level','hp':'HP','baseExp':'Base EXP','jobExp':'Job EXP',
        'def':'DEF','mdef':'MDEF','hit':r'Hit \(100%\)','flee':r'Flee \(95%\)',
        'str':'STR','agi':'AGI','vit':'VIT','int':'INT','dex':'DEX','luk':'LUK',
    }
    for key,label in labels.items():
        out[key]=label_number(text,label)
    atk=first(r'(?im)^\s*ATK\s+([\d,]+(?:\s*[–-]\s*[\d,]+)?)\s*$',text)
    out['attackMin'],out['attackMax']=parse_range(atk)
    matk=first(r'(?im)^\s*MATK\s+([\d,]+(?:\s*[–-]\s*[\d,]+)?)\s*$',text)
    out['magicAttackMin'],out['magicAttackMax']=parse_range(matk)

    modes=[]
    known=['Aggressive','Physically attackable','Can move','Loots items','Detector','Detects Hidden','Angry',
           'Changes Target When Attacked','Changes Target on Melee','Cast Sensor','Cast Sensor (Idle)','Cast Sensor (Chase)',
           'Immune to knockback','Immune to Status Change']
    low=text.lower()
    for label in known:
        if label.lower() in low:
            modes.append(label.replace('Physically attackable','Physically Attackable').replace('Can move','Can Move').replace('Loots items','Loots Items'))
    out['modes']=modes

    section=text.split('\nDrops',1)[1] if '\nDrops' in text else ''
    if section:
        section=re.split(r'\n(?:Skill AI|Spawns|Source)\b',section,1)[0]
        lines=section.splitlines()
        drops=[]; candidate=None; item_id=None
        for line in lines:
            if re.fullmatch(r'ID:\s*[\d,]+',line):
                item_id=int(line.split(':',1)[1].replace(',','').strip()); continue
            if re.fullmatch(r'Drop rate:\s*(?:\?+|[\d.]+)%',line):
                rate_txt=line.split(':',1)[1].strip().rstrip('%')
                rate=None if '?' in rate_txt else num(rate_txt)
                if candidate and item_id is not None:
                    drops.append({'itemId':item_id,'name':candidate,'rate':rate})
                candidate=None; item_id=None; continue
            if line.startswith('≈') or line.startswith('Drops ('):
                continue
            if not line.startswith('ID:') and not line.startswith('Drop rate:') and line not in {'Image'}:
                candidate=line
        out['drops']=drops

    tp=SectionTableParser(); tp.feed(raw)
    skills=[]
    for section,row in tp.tables:
        if not section.startswith('Skill AI') or len(row)<2:
            continue
        if row[0].lower()=='skill':
            continue
        raw_name=re.sub(r'\s+',' ',row[0]).strip()
        parts=raw_name.split(' ')
        name=parts[0] if parts and parts[0].startswith(('NPC_','MG_','SM_','TF_','AL_','MC_','AC_','PR_','WZ_')) else raw_name
        skills.append({
            'name':name,'level':num(row[1]),
            'rate':num((row[2] if len(row)>2 else '').replace('%','')),
            'state':row[3] if len(row)>3 else None,
            'target':row[4] if len(row)>4 else None,
            'condition':row[5] if len(row)>5 else None,
            'source':'TWRoZ'
        })
    out['skills']=skills
    return out


def parse_prontera(mob_id: int, raw: str) -> dict:
    text=visible_text(raw)
    if not re.search(rf'\bID\s+{mob_id}\b',text):
        return {}
    out={'_source':'Prontera'}
    labels={
        'hp':'HP','def':'DEF','mdef':'MDEF','baseExp':'Base EXP','jobExp':'Job EXP',
        'hit':r'Hit \(100%\)','flee':r'Flee \(95%\)','str':'STR','agi':'AGI','vit':'VIT',
        'int':'INT','dex':'DEX','luk':'LUK','attackRange':r'ATK Range \(cells\)',
        'moveSpeedMs':r'Move Speed \(ms\)'
    }
    for key,label in labels.items():
        out[key]=label_number(text,label)
    out['attackMin']=label_number(text,'ATK Min')
    out['attackMax']=label_number(text,'ATK Max')
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


def choose_field(field: str, ragna: dict, tw: dict, pro: dict) -> dict | None:
    values=[]
    rmap={'hp':'hp','def':'def','mdef':'mdef','baseExp':'basis_exp','jobExp':'job_exp','hit':'hit_100','flee':'flee_95',
          'str':'str','agi':'agi','vit':'vit','int':'int','dex':'dex','luk':'luk','attackRange':'angriffsweite','moveSpeedMs':'bewegung'}
    rk=rmap.get(field)
    if rk and ragna.get(rk) is not None:
        verified=rk in set(ragna.get('zero_felder') or [])
        values.append(('RagnaDex',ragna.get(rk),verified,'zero-verified' if verified else 'unverified-fallback'))
    tv=source_value(tw,field)
    if tv is not None:
        values.append(('TWRoZ',tv,False,'zero-regional'))
    pv=source_value(pro,field)
    if pv is not None:
        if field in {'hp','def','mdef','attackMin','attackMax','attackRange'}:
            group='combat'
        elif field in {'baseExp','jobExp','hit','flee','moveSpeedMs'}:
            group='experience'
        else:
            group='primary'
        verified=bool((pro.get('_verified') or {}).get(group))
        values.append(('Prontera',pv,verified,'global-verified' if verified else 'zero-db-unconfirmed'))
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


def add_source_rate(bucket: dict, source: str, rate):
    if source not in bucket['sources']:
        bucket['sources'][source]=rate
        return
    old=bucket['sources'][source]
    if old==rate:
        return
    vals=[]
    for v in (old if isinstance(old,list) else [old]) + (rate if isinstance(rate,list) else [rate]):
        if v not in vals:
            vals.append(v)
    bucket['sources'][source]=sorted(vals,key=lambda x:(x is None,float(x or 0)))


def numeric_candidates(value):
    vals=value if isinstance(value,list) else [value]
    return {float(v) for v in vals if isinstance(v,(int,float))}


def merge_drops(ragna: dict, tw: dict, pro: dict) -> list[dict]:
    by_key={}
    def add(source, rec, verified=False):
        name=str(rec.get('name') or '').strip(); iid=rec.get('itemId') or rec.get('item_id')
        key=f'id:{int(iid)}' if iid is not None else f'name:{normalize_name(name)}'
        if not key or key=='name:': return
        bucket=by_key.setdefault(key,{'itemId':int(iid) if iid is not None else None,'name':name,'sources':{},'verifiedSources':set()})
        if not bucket['name'] and name: bucket['name']=name
        add_source_rate(bucket,source,rec.get('rate'))
        if verified: bucket['verifiedSources'].add(source)
    for d in tw.get('drops') or []:
        add('TWRoZ',d)
    existing_by_name={normalize_name(v['name']):k for k,v in by_key.items() if v.get('name')}
    for d in pro.get('drops') or []:
        k=existing_by_name.get(normalize_name(d.get('name') or ''))
        if k:
            add_source_rate(by_key[k],'Prontera',d.get('rate'))
            if d.get('status')=='verified': by_key[k]['verifiedSources'].add('Prontera')
        else:
            add('Prontera',d,d.get('status')=='verified')
    for d in ragna.get('drops') or []:
        iid=d.get('item_id'); name=d.get('name') or ''
        k=f'id:{int(iid)}' if iid is not None else existing_by_name.get(normalize_name(name))
        if k in by_key:
            add_source_rate(by_key[k],'RagnaDex',d.get('rate'))
        # Never create a RagnaDex-only drop: its non-Zero fallback can be Renewal.

    out=[]
    for b in by_key.values():
        family_rates={s:numeric_candidates(v) for s,v in b['sources'].items()}
        all_rates=set().union(*family_rates.values()) if family_rates else set()
        chosen=None; status='unknown'
        verified_candidates=[]
        for source in b['verifiedSources']:
            verified_candidates.extend(sorted(family_rates.get(source,set())))
        if verified_candidates:
            chosen=verified_candidates[0]; status='verified'
        elif all_rates:
            votes=Counter()
            for rates in family_rates.values():
                for rate in rates:
                    votes[rate]+=1
            top,count=votes.most_common(1)[0]
            if count>=2:
                chosen=top; status='consensus'
            elif family_rates.get('TWRoZ'):
                chosen=sorted(family_rates['TWRoZ'])[0]; status='zero-regional'
            elif family_rates.get('Prontera'):
                chosen=sorted(family_rates['Prontera'])[0]; status='zero-db-unconfirmed'
        if isinstance(chosen,float) and chosen.is_integer(): chosen=int(chosen)
        conflict=len(all_rates)>1
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

fields=['hp','baseExp','jobExp','attackMin','attackMax','magicAttackMin','magicAttackMax','def','mdef','hit','flee','str','agi','vit','int','dex','luk','attackRange','moveSpeedMs']
consensus={}; coverage=Counter(); conflicts=Counter(); pro_hits=0; tw_hits=0
for mid in sorted(ids):
    r=ragna.get(mid,{})
    tw,pro=fetched.get(mid,({},{}))
    tw_hits+=bool(tw); pro_hits+=bool(pro)
    rec={'fields':{},'drops':merge_drops(r,tw,pro),'modes':[],'skills':tw.get('skills') or []}
    for field in fields:
        meta=choose_field(field,r,tw,pro)
        if meta:
            rec['fields'][field]=meta; coverage[field]+=1; conflicts[field]+=bool(meta.get('conflict'))
    modes=[]
    for source_modes in [tw.get('modes') or [], r.get('merkmale') or []]:
        if not isinstance(source_modes,list):
            continue
        for mode in source_modes:
            mode=str(mode).strip()
            if mode and mode not in modes: modes.append(mode)
    rec['modes']=modes
    rec['sourceAvailability']={'RagnaDex':bool(r),'TWRoZ':bool(tw),'Prontera':bool(pro)}
    if rec['fields'] or rec['drops'] or rec['modes'] or rec['skills']:
        consensus[str(mid)]=rec

p=consensus.get('1002') or {}
assert p.get('fields',{}).get('hp',{}).get('value')==55, p
assert p.get('fields',{}).get('attackMin',{}).get('value')==13, p
assert p.get('fields',{}).get('attackMax',{}).get('value')==17, p
assert p.get('fields',{}).get('magicAttackMin',{}).get('value')==2, p
assert p.get('fields',{}).get('magicAttackMax',{}).get('value')==4, p
jellopy=next((d for d in p.get('drops',[]) if d.get('itemId')==909),None)
assert jellopy and jellopy.get('rate')==70 and not jellopy.get('conflict'), jellopy
apple=next((d for d in p.get('drops',[]) if d.get('itemId')==512),None)
assert apple and apple.get('rate')==10 and apple.get('conflict') is True, apple
card=next((d for d in p.get('drops',[]) if d.get('itemId')==4001),None)
assert card and card.get('rate')==0.2 and card.get('conflict') is True, card
assert len(p.get('skills') or []) >= 2, p.get('skills')

meta={'sources':['RagnaDex','RagnarokZero.net / TWRoZ','Prontera.Info ROZ'],'policy':'Zero databases only; client and verified Global/Zero fields first, then Zero-source consensus, with conflicts preserved','monsters':len(consensus),'twrozPages':tw_hits,'pronteraPages':pro_hits,'coverage':dict(coverage),'conflicts':dict(conflicts)}
OUT.write_text(
    '// Cross-database Ragnarok Zero monster consensus. No Renewal/iRO/RateMyServer fallback is imported.\n'
    + 'window.RZ_MONSTER_ZERO_CONSENSUS=' + json.dumps(consensus,ensure_ascii=False,separators=(',',':'),sort_keys=True) + ';\n'
    + 'window.RZ_MONSTER_ZERO_CONSENSUS_META=' + json.dumps(meta,ensure_ascii=False,separators=(',',':'),sort_keys=True) + ';\n',
    encoding='utf-8'
)
print(json.dumps(meta,ensure_ascii=False,indent=2))
