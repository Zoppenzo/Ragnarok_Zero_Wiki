from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

ROSTER = Path('assets/client-monster-roster.js')
OUT = Path('assets/monster-ragnaplace-exp.js')
UA = 'Ragnarok-Zero-Wiki/2.3 (+https://github.com/Zoppenzo/Ragnarok_Zero_Wiki)'
URL = 'https://ragnaplace.com/en/rozg-en/mob/{id}'

# Exact normal/world candidates reported by the refined audit as missing at least
# one EXP field on 2026-09-11. Re-querying this bounded set avoids crawling the
# whole site on every deployment. Values already present in runtime are never
# overwritten by the generated overlay.
TARGET_IDS = [
    1250,3032,25336,25321,25322,25323,25324,25325,25326,
    1078,1080,1081,1082,1083,1084,1085,1583,2404,2405,2406,
    1029,1032,1038,1039,1041,1049,1053,1054,1066,1071,1086,1092,1098,
    1101,1108,1112,1121,1147,1151,1157,1161,1175,1196,1197,1199,1200,
    1201,1202,1208,1209,1214,1253,1257,1260,1263,1267,1268,1272,1275,
    1281,1293,1295,1297,1300,1303,1305,1306,1310,1311,1320,1511,
    1045,1065,1069,1132,1142,1154,1155,1158,1163,1164,1178,1195,1219,
    1270,1276,1283,1291,1298,
]


class VisibleText(HTMLParser):
    BLOCK = {'h1','h2','h3','h4','p','div','section','article','li','tr','td','th','br','table','label'}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in {'script','style','noscript'}:
            self.skip += 1
            return
        if not self.skip and tag in self.BLOCK:
            self.parts.append('\n')
    def handle_endtag(self, tag):
        if tag in {'script','style','noscript'} and self.skip:
            self.skip -= 1
            return
        if not self.skip and tag in self.BLOCK:
            self.parts.append('\n')
    def handle_data(self, data):
        if not self.skip:
            self.parts.append(' ' + data + ' ')
    def text(self) -> str:
        raw=''.join(self.parts)
        lines=[]
        for line in raw.splitlines():
            line=re.sub(r'\s+',' ',line).strip()
            if line:
                lines.append(line)
        return '\n'.join(lines)


def parse_roster() -> dict[int, str]:
    raw=ROSTER.read_text(encoding='utf-8')
    m=re.search(r'window\.RZ_CLIENT_MONSTER_ROSTER=(\[.*?\]);',raw,re.S)
    if not m:
        raise SystemExit('Could not parse client monster roster')
    rows=json.loads(m.group(1))
    out={int(row[0]):str(row[1]) for row in rows if isinstance(row,list) and len(row)>=2 and str(row[0]).isdigit()}
    if len(out)!=598:
        raise SystemExit(f'Expected 598 roster identities, got {len(out)}')
    missing=[x for x in TARGET_IDS if x not in out]
    if missing:
        raise SystemExit(f'EXP target Mob-IDs missing from current client roster: {missing}')
    return out


def fetch(url: str, timeout: int = 20) -> str | None:
    req=urllib.request.Request(url,headers={
        'User-Agent':UA,
        'Accept':'text/html,application/xhtml+xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'en-US,en;q=0.9',
    })
    try:
        with urllib.request.urlopen(req,timeout=timeout) as r:
            return r.read().decode('utf-8','replace')
    except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError):
        return None


def as_int(s: str) -> int | None:
    s=str(s or '').strip().replace(',','').replace('\u202f','').replace(' ','')
    if not s or not s.isdigit():
        return None
    return int(s)


def looks_like_scaled_triplet(values: list[int], offset: int) -> bool:
    if len(values) < offset+6:
        return False
    b1,j1,b15,j15,b2,j2=values[offset:offset+6]
    checks=0
    ok=0
    for a,b,c in ((b1,b15,b2),(j1,j15,j2)):
        if a>0:
            checks += 1
            if b in {int(a*1.5), round(a*1.5)} and c==a*2:
                ok += 1
    return checks>0 and ok==checks


def parse_exp(mob_id: int, internal_name: str, raw: str) -> tuple[dict, str | None]:
    p=VisibleText(); p.feed(raw); text=p.text()
    ident=re.compile(rf'\b{mob_id}\s*/\s*{re.escape(internal_name)}\b',re.I)
    if not ident.search(text):
        return {}, 'identity-mismatch'

    m=re.search(r'(?is)(?:^|\n)Experience\s*\n\s*Base\s*\n\s*Job\s*\n(.*?)(?:\nSkills\b|\n[A-Z][^\n]{0,80}\n)',text)
    if not m:
        # Fallback bounded by Skills; some layouts insert extra wrappers between
        # the Experience heading and the Base/Job labels.
        m=re.search(r'(?is)(?:^|\n)Experience\b(.*?)(?:\nSkills\b|$)',text)
    if not m:
        return {}, 'experience-section-missing'

    body=m.group(1)
    nums=[]
    for line in body.splitlines():
        line=line.strip()
        if re.fullmatch(r'[\d,\u202f ]+',line):
            n=as_int(line)
            if n is not None:
                nums.append(n)

    # Normally the visible section is six values: x1 Base/Job, x1.5 Base/Job,
    # x2 Base/Job. If an input multiplier value leaks into visible text there can
    # be one small leading number; remove it only when the remaining six values
    # validate against the displayed 1.5x and 2x rows.
    offset=0
    if len(nums)>=7 and nums[0] <= 10 and looks_like_scaled_triplet(nums,1):
        offset=1
    elif len(nums)>=6 and looks_like_scaled_triplet(nums,0):
        offset=0
    elif len(nums)>=6:
        offset=max(0,len(nums)-6)
    else:
        return {}, f'experience-numbers-short:{nums}'

    base,job=nums[offset],nums[offset+1]
    out={}
    # Zero or a dash on RagnaPlace can mean unavailable rather than genuine zero.
    # Import only strictly positive values; unknown remains unknown in the wiki.
    if base>0:
        out['baseExp']=base
    if job>0:
        out['jobExp']=job
    return out, None


def build_one(mob_id: int, internal_name: str):
    raw=fetch(URL.format(id=mob_id))
    if raw is None:
        return mob_id, {}, 'fetch-failed'
    data,err=parse_exp(mob_id,internal_name,raw)
    return mob_id,data,err


def js_payload(data: dict[str, dict], meta: dict) -> str:
    d=json.dumps(data,ensure_ascii=False,separators=(',',':'))
    m=json.dumps(meta,ensure_ascii=False,separators=(',',':'))
    return f"""(() => {{
  'use strict';
  const data={d};
  const meta={m};
  window.RZ_MONSTER_RAGNAPLACE_EXP=data;
  window.RZ_MONSTER_RAGNAPLACE_EXP_META=meta;

  const unknown=value=>value===null||value===undefined||value===''||/^n\\/?a$/i.test(String(value).trim())||String(value).trim()==='—';
  const monsters=Array.isArray(window.RO_DATA?.monsters)?window.RO_DATA.monsters:[];
  for(const monster of monsters){{
    const id=String(monster?.clientId??monster?.id??'');
    const row=data[id];
    if(!row)continue;
    monster.fieldMeta=monster.fieldMeta&&typeof monster.fieldMeta==='object'?monster.fieldMeta:{{}};
    for(const [field,value] of Object.entries(row)){{
      if(!['baseExp','jobExp'].includes(field)||!Number.isFinite(Number(value))||Number(value)<=0)continue;
      if(!unknown(monster[field]))continue;
      monster[field]=Number(value);
      monster.fieldMeta[field]={{
        status:'zero-global-external',
        conflict:false,
        source:'RagnaPlace ROZg EN',
        sources:{{RagnaPlace:Number(value)}}
      }};
    }}
  }}
}})();
"""


def main():
    roster=parse_roster()
    results={}
    errors={}
    pages=0
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs={ex.submit(build_one,mob_id,roster[mob_id]):mob_id for mob_id in TARGET_IDS}
        for fut in as_completed(futs):
            mob_id=futs[fut]
            try:
                rid,data,err=fut.result()
            except Exception as exc:
                errors[str(mob_id)]=f'exception:{type(exc).__name__}'
                continue
            if err!='fetch-failed':
                pages += 1
            if data:
                results[str(rid)]=data
            if err:
                errors[str(rid)]=err

    meta={
        'source':'RagnaPlace ROZg EN',
        'generatedAt':datetime.now(timezone.utc).isoformat(),
        'targets':len(TARGET_IDS),
        'pages':pages,
        'monstersWithExp':len(results),
        'baseExp':sum(1 for row in results.values() if row.get('baseExp',0)>0),
        'jobExp':sum(1 for row in results.values() if row.get('jobExp',0)>0),
        'errors':errors,
        'policy':'Only strictly positive values from the Zero Global EN Experience table are imported. Zero/dash remains unknown.',
    }
    OUT.write_text(js_payload(results,meta),encoding='utf-8')
    print(json.dumps(meta,ensure_ascii=False,indent=2))
    if pages < 50:
        raise SystemExit(f'RagnaPlace Zero Global coverage unexpectedly low: {pages}/{len(TARGET_IDS)} pages')


if __name__=='__main__':
    main()
