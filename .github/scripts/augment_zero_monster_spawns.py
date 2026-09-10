from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from pathlib import Path

ROSTER = Path('assets/client-monster-roster.js')
NAV = Path('assets/client-monster-navigation-current.js')
CONSENSUS = Path('assets/monster-zero-consensus.js')
TWROZ_URL = 'https://ragnarokzero.net/database/monsters/{id}'
UA = 'Ragnarok-Zero-Wiki/2.3 (+https://github.com/Zoppenzo/Ragnarok_Zero_Wiki)'


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
            self.parts.append(' ' + data + ' ')

    def text(self) -> str:
        lines=[]
        for line in ''.join(self.parts).splitlines():
            line=re.sub(r'\s+',' ',line).strip()
            if line:
                lines.append(line)
        return '\n'.join(lines)


def fetch(url: str, timeout: int = 25) -> str | None:
    req=urllib.request.Request(url,headers={'User-Agent':UA,'Accept':'text/html,*/*;q=0.8'})
    try:
        with urllib.request.urlopen(req,timeout=timeout) as r:
            return r.read().decode('utf-8','replace')
    except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError):
        return None


def parse_assignment(path: Path, variable: str):
    text=path.read_text(encoding='utf-8')
    m=re.search(rf'window\.{re.escape(variable)}=(.*?);(?:\n|$)',text,re.S)
    if not m:
        raise SystemExit(f'Could not parse {variable} from {path}')
    return json.loads(m.group(1)), text


def parse_roster():
    rows,_=parse_assignment(ROSTER,'RZ_CLIENT_MONSTER_ROSTER')
    if len(rows)!=598:
        raise SystemExit(f'Expected 598 sprite-backed roster identities, got {len(rows)}')
    return rows


def visible_text(raw: str) -> str:
    parser=VisibleTextParser(); parser.feed(raw); return parser.text()


PURE_MAP_IDS={
    'prontera','geffen','payon','morocc','alberta','izlude','aldebaran','comodo','umbala','niflheim',
    'xmas','yuno','einbroch','einbech','lighthalzen','rachel','veins','hugel','moscovia','brasilis',
    'dewata','malangdo','mora','eclage','lasagna'
}
MAP_TOKEN=re.compile(r'(?<![A-Za-z0-9_])([a-z][a-z0-9]{0,15}_[a-z0-9_]{1,24})(?![A-Za-z0-9_])')


def parse_spawns(mob_id: int, raw: str) -> list[dict]:
    text=visible_text(raw)
    if f'#{mob_id}' not in text:
        return []
    lines=text.splitlines()
    start=next((i for i,line in enumerate(lines) if line.startswith('Spawns')),None)
    if start is None:
        return []
    end=next((i for i in range(start+1,len(lines)) if lines[i]=='Source' or lines[i].startswith('Source ')),len(lines))
    section='\n'.join(lines[start+1:end])

    found=[]
    for token in MAP_TOKEN.findall(section):
        if token not in found:
            found.append(token)
    for line in lines[start+1:end]:
        token=line.strip().split(' ',1)[0]
        if token in PURE_MAP_IDS and token not in found:
            found.append(token)

    # TWRoZ explicitly distinguishes location data from estimated rAthena counts.
    # Only the map identity is imported. Population/respawn estimates are ignored.
    return [{'mapId':map_id,'source':'TWRoZ','status':'zero-regional'} for map_id in found]


roster=parse_roster()
nav,_=parse_assignment(NAV,'RZ_CLIENT_MONSTER_NAV_CURRENT')
consensus,text=parse_assignment(CONSENSUS,'RZ_MONSTER_ZERO_CONSENSUS')
meta,_=parse_assignment(CONSENSUS,'RZ_MONSTER_ZERO_CONSENSUS_META')

# Exact internal identity remains the Navi join key. TWRoZ is queried only for
# roster identities that have no current Navi record at all.
targets=[]
for row in roster:
    if not isinstance(row,list) or len(row)<2:
        continue
    mid=int(row[0]); internal=str(row[1] or '').strip()
    if internal and internal not in nav:
        targets.append((mid,internal))

results={}
with ThreadPoolExecutor(max_workers=6) as ex:
    futs={ex.submit(fetch,TWROZ_URL.format(id=mid)):mid for mid,_ in targets}
    for i,fut in enumerate(as_completed(futs),1):
        mid=futs[fut]
        raw=fut.result()
        spawns=parse_spawns(mid,raw) if raw else []
        if spawns:
            results[mid]=spawns
        if i%40==0:
            print(f'Fetched {i}/{len(futs)} no-Navi TWRoZ spawn pages')

# Remove stale generated fallback spawns first, then write the current extraction.
for rec in consensus.values():
    if isinstance(rec,dict):
        rec.pop('spawns',None)

for mid,spawns in results.items():
    rec=consensus.setdefault(str(mid),{'fields':{},'drops':[],'modes':[],'skills':[],'sourceAvailability':{}})
    rec['spawns']=spawns
    availability=rec.setdefault('sourceAvailability',{})
    availability['TWRoZ']=True

spawn_maps=sum(len(v) for v in results.values())
meta['spawnPolicy']='TWRoZ map identities only, only for current-client roster identities without an exact-name Navi record; estimated counts/respawns are excluded'
meta['spawnTargetsWithoutNavi']=len(targets)
meta['spawnMonsters']=len(results)
meta['spawnMaps']=spawn_maps

# Regression anchors: these two MVPs are absent from current exact-name Navi but
# TWRoZ exposes Zero-specific boss-map identities for them.
baph={x['mapId'] for x in results.get(1039,[])}
doppel={x['mapId'] for x in results.get(1046,[])}
assert 'b_maz_d03' in baph, baph
assert 'b_gef_d01' in doppel, doppel

CONSENSUS.write_text(
    '// Cross-database Ragnarok Zero monster consensus. No Renewal/iRO/RateMyServer fallback is imported.\n'
    + '// The builder scans every sprite-backed identity in the supplied current client roster.\n'
    + 'window.RZ_MONSTER_ZERO_CONSENSUS=' + json.dumps(consensus,ensure_ascii=False,separators=(',',':'),sort_keys=True) + ';\n'
    + 'window.RZ_MONSTER_ZERO_CONSENSUS_META=' + json.dumps(meta,ensure_ascii=False,separators=(',',':'),sort_keys=True) + ';\n',
    encoding='utf-8'
)
print(json.dumps({
    'targetsWithoutNavi':len(targets),
    'spawnMonsters':len(results),
    'spawnMaps':spawn_maps,
    'baphomet':sorted(baph),
    'doppelganger':sorted(doppel),
},ensure_ascii=False,indent=2))
