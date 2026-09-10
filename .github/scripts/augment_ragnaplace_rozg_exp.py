from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from pathlib import Path

ROSTER = Path('assets/client-monster-roster.js')
OUT = Path('assets/monster-zero-consensus.js')
BASE_URL = 'https://ragnaplace.com/en/rozg-en/mob'
SOURCE_NAME = 'RagnaPlace ROZg EN'
UA = 'Ragnarok-Zero-Wiki/2.3 (+https://github.com/Zoppenzo/Ragnarok_Zero_Wiki)'
MIN_PAGES = 30


class VisibleTextParser(HTMLParser):
    BLOCK = {'h1','h2','h3','h4','p','div','section','article','li','tr','td','th','br','table','a'}
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
    def lines(self) -> list[str]:
        raw=''.join(self.parts)
        return [re.sub(r'\s+',' ',line).strip() for line in raw.splitlines() if re.sub(r'\s+',' ',line).strip()]


def fetch(url: str, *, attempts: int = 3, timeout: int = 30) -> str:
    last = None
    for attempt in range(attempts):
        req=urllib.request.Request(url,headers={
            'User-Agent':UA,
            'Accept':'text/html,application/xhtml+xml',
            'Accept-Language':'en-US,en;q=0.9'
        })
        try:
            with urllib.request.urlopen(req,timeout=timeout) as r:
                return r.read().decode('utf-8','replace')
        except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError) as exc:
            last=exc
            if attempt+1<attempts:
                time.sleep(1.5*(attempt+1))
    raise RuntimeError(f'Could not fetch {url}: {last}')


def parse_exp(value: str | None):
    if value is None:
        return None
    value=value.strip().replace(',','')
    if not value or value == '-':
        return None
    if not re.fullmatch(r'\d+',value):
        return None
    return int(value)


def parse_page(raw: str, page: int) -> list[dict]:
    parser=VisibleTextParser(); parser.feed(raw)
    lines=parser.lines()
    joined='\n'.join(lines)
    if 'ROZg EN' not in joined or 'Zero Global EN' not in joined:
        raise RuntimeError(f'Page {page} is not the ROZg EN / Zero Global EN monster list')

    out=[]
    for i,line in enumerate(lines):
        m=re.fullmatch(r'(\d+)\s*/\s*([A-Za-z0-9_]+)',line)
        if not m:
            continue
        mob_id=int(m.group(1)); internal=m.group(2)
        base_raw=job_raw=None
        for candidate in lines[i+1:min(i+9,len(lines))]:
            if candidate.startswith('Base exp:') and base_raw is None:
                base_raw=candidate.split(':',1)[1].strip()
            elif candidate.startswith('Job exp:') and job_raw is None:
                job_raw=candidate.split(':',1)[1].strip()
            if base_raw is not None and job_raw is not None:
                break
        if base_raw is None or job_raw is None:
            continue
        out.append({
            'id':mob_id,
            'internalName':internal,
            'baseExp':parse_exp(base_raw),
            'jobExp':parse_exp(job_raw),
            'baseRaw':base_raw,
            'jobRaw':job_raw,
            'page':page
        })
    return out


def parse_roster() -> dict[int,str]:
    text=ROSTER.read_text(encoding='utf-8')
    m=re.search(r'window\.RZ_CLIENT_MONSTER_ROSTER=(\[.*?\]);',text,re.S)
    if not m:
        raise SystemExit('Could not parse client monster roster')
    rows=json.loads(m.group(1))
    roster={int(row[0]):str(row[1]) for row in rows if isinstance(row,list) and len(row)>=2 and str(row[0]).isdigit()}
    if len(roster)!=598:
        raise SystemExit(f'Expected 598 sprite-backed roster Mob-IDs, got {len(roster)}')
    return roster


def load_consensus():
    text=OUT.read_text(encoding='utf-8')
    try:
        payload=text.split('window.RZ_MONSTER_ZERO_CONSENSUS=',1)[1].split(';\nwindow.RZ_MONSTER_ZERO_CONSENSUS_META=',1)[0]
        meta_payload=text.split('window.RZ_MONSTER_ZERO_CONSENSUS_META=',1)[1].rstrip().rstrip(';')
    except IndexError as exc:
        raise SystemExit('Could not parse monster-zero-consensus.js') from exc
    return json.loads(payload),json.loads(meta_payload)


def write_consensus(consensus: dict, meta: dict):
    OUT.write_text(
        'window.RZ_MONSTER_ZERO_CONSENSUS='+json.dumps(consensus,separators=(',',':'),ensure_ascii=False)+';\n'
        'window.RZ_MONSTER_ZERO_CONSENSUS_META='+json.dumps(meta,separators=(',',':'),ensure_ascii=False)+';\n',
        encoding='utf-8'
    )


def field_value(record: dict, field: str):
    item=(record.get('fields') or {}).get(field)
    return item.get('value') if isinstance(item,dict) else None


def main():
    roster=parse_roster()
    consensus,meta=load_consensus()

    first_raw=fetch(BASE_URL)
    page_numbers=[int(x) for x in re.findall(r'[?&](?:amp;)?page=(\d+)',first_raw)]
    page_count=max([MIN_PAGES,*page_numbers])
    if page_count>60:
        raise SystemExit(f'Unexpected RagnaPlace pagination: {page_count} pages')

    pages={1:first_raw}
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures={pool.submit(fetch,f'{BASE_URL}?page={page}'):page for page in range(2,page_count+1)}
        for future in as_completed(futures):
            page=futures[future]
            pages[page]=future.result()
    if len(pages)!=page_count:
        raise SystemExit(f'Expected {page_count} RagnaPlace pages, fetched {len(pages)}')

    rows_by_id={}
    duplicates=[]
    for page in range(1,page_count+1):
        for row in parse_page(pages[page],page):
            old=rows_by_id.get(row['id'])
            if old and (old['internalName'],old['baseRaw'],old['jobRaw']) != (row['internalName'],row['baseRaw'],row['jobRaw']):
                duplicates.append({'id':row['id'],'first':old,'second':row})
                continue
            rows_by_id[row['id']]=row

    if duplicates:
        raise SystemExit('Conflicting duplicate RagnaPlace rows: '+json.dumps(duplicates[:5],ensure_ascii=False))
    if len(rows_by_id)<580:
        raise SystemExit(f'Expected at least 580 ROZg EN monster rows, parsed {len(rows_by_id)}')

    # Regression samples deliberately include numeric and blank values. A dash is
    # unknown, never numeric zero.
    samples={mid:rows_by_id.get(mid) for mid in (2398,1155,1053,1046)}
    assert samples[2398] and samples[2398]['baseExp']==24 and samples[2398]['jobExp']==4, samples[2398]
    assert samples[1155] and samples[1155]['baseExp']==14167 and samples[1155]['jobExp'] is None, samples[1155]
    assert samples[1053] and samples[1053]['baseExp'] is None and samples[1053]['jobExp'] is None, samples[1053]
    assert samples[1046] and samples[1046]['baseExp']==7607000 and samples[1046]['jobExp']==899009, samples[1046]

    roster_matches=0
    internal_mismatches=[]
    applied_base=applied_job=0
    existing_base=existing_job=0
    source_numeric_base=source_numeric_job=0

    for mid,row in rows_by_id.items():
        if mid not in roster:
            continue
        roster_matches += 1
        if roster[mid] != row['internalName']:
            internal_mismatches.append({'id':mid,'client':roster[mid],'source':row['internalName']})

        if row['baseExp'] is not None:
            source_numeric_base += 1
        if row['jobExp'] is not None:
            source_numeric_job += 1
        if row['baseExp'] is None and row['jobExp'] is None:
            continue

        record=consensus.setdefault(str(mid),{'fields':{},'drops':[],'skills':[],'modes':[]})
        fields=record.setdefault('fields',{})
        for field,value in (('baseExp',row['baseExp']),('jobExp',row['jobExp'])):
            if value is None:
                continue
            current=fields.get(field)
            current_value=current.get('value') if isinstance(current,dict) else None
            if current_value is not None:
                if field=='baseExp': existing_base += 1
                else: existing_job += 1
                continue
            fields[field]={
                'value':value,
                'status':'zero-global-db',
                'conflict':False,
                'sources':{SOURCE_NAME:value}
            }
            if field=='baseExp': applied_base += 1
            else: applied_job += 1

    coverage=meta.setdefault('coverage',{})
    for field in ('baseExp','jobExp'):
        coverage[field]=sum(1 for record in consensus.values() if field_value(record,field) is not None)
    sources=meta.setdefault('sources',[])
    if SOURCE_NAME not in sources:
        sources.append(SOURCE_NAME)
    meta['monsters']=len(consensus)
    meta['ragnaplaceRozgPages']=page_count
    meta['ragnaplaceRozgRows']=len(rows_by_id)
    meta['ragnaplaceRozgRosterMatches']=roster_matches
    meta['ragnaplaceRozgInternalNameMismatches']=len(internal_mismatches)
    meta['ragnaplaceRozgNumericBaseExp']=source_numeric_base
    meta['ragnaplaceRozgNumericJobExp']=source_numeric_job
    meta['ragnaplaceRozgAppliedBaseExp']=applied_base
    meta['ragnaplaceRozgAppliedJobExp']=applied_job
    meta['ragnaplaceRozgExistingBaseExp']=existing_base
    meta['ragnaplaceRozgExistingJobExp']=existing_job
    meta['ragnaplaceRozgSamples']={
        str(mid):None if row is None else {'internalName':row['internalName'],'baseExp':row['baseExp'],'jobExp':row['jobExp']}
        for mid,row in samples.items()
    }

    write_consensus(consensus,meta)
    print(json.dumps({
        'source':SOURCE_NAME,
        'pages':page_count,
        'rows':len(rows_by_id),
        'rosterMatches':roster_matches,
        'internalNameMismatches':len(internal_mismatches),
        'numericBaseExp':source_numeric_base,
        'numericJobExp':source_numeric_job,
        'appliedBaseExp':applied_base,
        'appliedJobExp':applied_job,
        'coverageBaseExp':coverage['baseExp'],
        'coverageJobExp':coverage['jobExp'],
        'sampleMismatches':internal_mismatches[:10]
    },indent=2,ensure_ascii=False))


if __name__=='__main__':
    main()
