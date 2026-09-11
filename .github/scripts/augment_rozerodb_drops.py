from __future__ import annotations

import json
import re
import time
import unicodedata
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from pathlib import Path

CONSENSUS = Path('assets/monster-zero-consensus.js')
ROZERODB_URL = 'https://rozerodb.com/monsters/{id}'
TWROZ_URL = 'https://ragnarokzero.net/database/monsters/{id}'
UA = 'Ragnarok-Zero-Wiki/2.4 (+https://github.com/Zoppenzo/Ragnarok_Zero_Wiki)'


class SectionAnchorParser(HTMLParser):
    """Collect links together with the closest h1/h2/h3 section heading."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.current_heading = ''
        self.heading_tag = None
        self.heading_parts: list[str] = []
        self.in_link = False
        self.link_section = ''
        self.link_href = ''
        self.link_parts: list[str] = []
        self.links: list[tuple[str, str, str]] = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in {'script', 'style', 'noscript'}:
            self.skip += 1
            return
        if self.skip:
            return
        if tag in {'h1', 'h2', 'h3'}:
            self.heading_tag = tag
            self.heading_parts = []
        elif tag == 'a':
            self.in_link = True
            self.link_section = self.current_heading
            self.link_href = dict(attrs).get('href', '')
            self.link_parts = []

    def handle_endtag(self, tag):
        if tag in {'script', 'style', 'noscript'} and self.skip:
            self.skip -= 1
            return
        if self.skip:
            return
        if self.heading_tag == tag:
            heading = re.sub(r'\s+', ' ', ' '.join(self.heading_parts)).strip()
            if heading:
                self.current_heading = heading
            self.heading_tag = None
            self.heading_parts = []
        elif tag == 'a' and self.in_link:
            text = re.sub(r'\s+', ' ', ' '.join(self.link_parts)).strip()
            self.links.append((self.link_section, self.link_href, text))
            self.in_link = False
            self.link_section = ''
            self.link_href = ''
            self.link_parts = []

    def handle_data(self, data):
        if self.skip:
            return
        if self.heading_tag:
            self.heading_parts.append(data)
        if self.in_link:
            self.link_parts.append(data)


class VisibleTextParser(HTMLParser):
    BLOCK = {'h1', 'h2', 'h3', 'h4', 'p', 'div', 'section', 'article', 'li', 'tr', 'td', 'th', 'br', 'table'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in {'script', 'style', 'noscript'}:
            self.skip += 1
        if not self.skip and tag in self.BLOCK:
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if tag in {'script', 'style', 'noscript'} and self.skip:
            self.skip -= 1
        if not self.skip and tag in self.BLOCK:
            self.parts.append('\n')

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(' ' + data + ' ')

    def text(self) -> str:
        lines = []
        for line in ''.join(self.parts).splitlines():
            line = re.sub(r'\s+', ' ', line).strip()
            if line:
                lines.append(line)
        return '\n'.join(lines)


def fetch(url: str, timeout: int = 22) -> str | None:
    for attempt in range(2):
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': UA,
                'Accept': 'text/html,application/xhtml+xml;q=0.9,*/*;q=0.8',
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return response.read().decode('utf-8', 'replace')
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
            if attempt == 0:
                time.sleep(0.2)
    return None


def normalize_name(value: str) -> str:
    value = unicodedata.normalize('NFKD', value or '').encode('ascii', 'ignore').decode('ascii').lower()
    value = re.sub(r'\(bound\)|\[costume\]', '', value)
    return re.sub(r'[^a-z0-9]+', '', value)


def parse_rate(value: str):
    value = (value or '').strip().rstrip('%')
    if not value or '?' in value or value.lower() == 'unknown' or value in {'—', '-'}:
        return None
    try:
        number = float(value)
        return int(number) if number.is_integer() else number
    except ValueError:
        return None


def parse_rozerodb_drops(raw: str) -> list[dict]:
    parser = SectionAnchorParser()
    parser.feed(raw)
    out: list[dict] = []
    seen: set[int] = set()

    for section, _href, text in parser.links:
        if not section.lower().startswith('drops'):
            continue
        # Drop cards render as e.g. "Cobweb#1025 45%" or
        # "[Costume] Spider Wings (Bound)#480573???".
        match = re.search(r'#\s*(\d+)\s*(?:(\d+(?:\.\d+)?)%|(\?{1,3}|unknown|—|-))?\s*$', text, re.I)
        if not match:
            continue
        item_id = int(match.group(1))
        if item_id in seen:
            continue
        name = text[:match.start()].strip()
        if not name:
            continue
        rate_token = match.group(2) if match.group(2) is not None else match.group(3)
        out.append({'itemId': item_id, 'name': name, 'rate': parse_rate(rate_token or '')})
        seen.add(item_id)

    return out


def parse_twroz_drops(raw: str) -> list[dict]:
    parser = VisibleTextParser()
    parser.feed(raw)
    text = parser.text()
    section = text.split('\nDrops', 1)[1] if '\nDrops' in text else ''
    if not section:
        return []
    section = re.split(r'\n(?:Skill AI|Spawns|Source)\b', section, 1)[0]

    drops = []
    candidate = None
    item_id = None
    for line in section.splitlines():
        if re.fullmatch(r'ID:\s*[\d,]+', line):
            item_id = int(line.split(':', 1)[1].replace(',', '').strip())
            continue
        if re.fullmatch(r'Drop rate:\s*(?:(?:\?+|[\d.]+)%|—|-)', line):
            rate_txt = line.split(':', 1)[1].strip()
            rate = parse_rate(rate_txt)
            if candidate and item_id is not None:
                drops.append({'itemId': item_id, 'name': candidate, 'rate': rate})
            candidate = None
            item_id = None
            continue
        if line.startswith('≈') or line.startswith('Drops ('):
            continue
        if not line.startswith('ID:') and not line.startswith('Drop rate:') and line not in {'Image'}:
            candidate = line
    return drops


def load_consensus():
    text = CONSENSUS.read_text(encoding='utf-8')
    marker = 'window.RZ_MONSTER_ZERO_CONSENSUS='
    meta_marker = ';\nwindow.RZ_MONSTER_ZERO_CONSENSUS_META='
    if marker not in text or meta_marker not in text:
        raise SystemExit('Unexpected monster-zero-consensus.js format')
    payload = text.split(marker, 1)[1].split(meta_marker, 1)[0]
    meta_payload = text.split(meta_marker, 1)[1].rstrip().rstrip(';')
    return json.loads(payload), json.loads(meta_payload)


def save_consensus(data: dict, meta: dict):
    CONSENSUS.write_text(
        '// Cross-database Ragnarok Zero monster consensus. No Renewal/iRO/RateMyServer fallback is imported.\n'
        + '// TWRoZ and RO ZERO DATABASE are independently rechecked for drop relations; one-source relations remain unknown.\n'
        + 'window.RZ_MONSTER_ZERO_CONSENSUS=' + json.dumps(data, ensure_ascii=False, separators=(',', ':'), sort_keys=True) + ';\n'
        + 'window.RZ_MONSTER_ZERO_CONSENSUS_META=' + json.dumps(meta, ensure_ascii=False, separators=(',', ':'), sort_keys=True) + ';\n',
        encoding='utf-8',
    )


def drop_indexes(drops: list[dict]):
    by_id = {int(d['itemId']): d for d in drops if d.get('itemId') is not None}
    by_name = {normalize_name(d.get('name') or ''): d for d in drops if normalize_name(d.get('name') or '')}
    return by_id, by_name


def find_drop(drops: list[dict], candidate: dict):
    by_id, by_name = drop_indexes(drops)
    if candidate.get('itemId') is not None and int(candidate['itemId']) in by_id:
        return by_id[int(candidate['itemId'])]
    return by_name.get(normalize_name(candidate.get('name') or ''))


def add_source(target: dict, source: str, candidate: dict):
    sources = target.setdefault('sources', {})
    sources[source] = candidate.get('rate')
    if target.get('itemId') is None and candidate.get('itemId') is not None:
        target['itemId'] = int(candidate['itemId'])
    if not target.get('name') and candidate.get('name'):
        target['name'] = candidate['name']


def merge_verified_drop_sources(record: dict, tw_drops: list[dict], rz_drops: list[dict]) -> tuple[int, int]:
    drops = record.setdefault('drops', [])
    evidence_added = 0
    created = 0

    # First enrich relations that the original comparison builder already found.
    for source, source_drops in [('TWRoZ', tw_drops), ('ROZeroDB', rz_drops)]:
        for candidate in source_drops:
            target = find_drop(drops, candidate)
            if not target:
                continue
            before = set((target.get('sources') or {}).keys())
            add_source(target, source, candidate)
            evidence_added += source not in before

    # If an item was completely missed upstream, create it only when the two
    # independent Zero databases both contain the same monster->item relation.
    rz_by_id, rz_by_name = drop_indexes(rz_drops)
    for tw in tw_drops:
        rz = None
        if tw.get('itemId') is not None:
            rz = rz_by_id.get(int(tw['itemId']))
        if not rz:
            rz = rz_by_name.get(normalize_name(tw.get('name') or ''))
        if not rz:
            continue
        target = find_drop(drops, tw) or find_drop(drops, rz)
        if not target:
            target = {
                'itemId': int(tw.get('itemId') or rz.get('itemId')),
                'name': tw.get('name') or rz.get('name') or '',
                'rate': None,
                'status': 'relation-consensus',
                'conflict': False,
                'sources': {},
            }
            drops.append(target)
            created += 1
        for source, candidate in [('TWRoZ', tw), ('ROZeroDB', rz)]:
            before = set((target.get('sources') or {}).keys())
            add_source(target, source, candidate)
            evidence_added += source not in before

    return evidence_added, created


def main():
    data, meta = load_consensus()
    candidate_ids = [int(mid) for mid, row in data.items() if row.get('drops') or row.get('skills') or row.get('fields')]
    fetched: dict[int, tuple[list[dict], list[dict]]] = {}
    tw_hits = 0
    rz_hits = 0

    def fetch_one(mid: int):
        tw_raw = fetch(TWROZ_URL.format(id=mid))
        rz_raw = fetch(ROZERODB_URL.format(id=mid))
        return (
            mid,
            parse_twroz_drops(tw_raw) if tw_raw else [],
            parse_rozerodb_drops(rz_raw) if rz_raw else [],
        )

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_one, mid): mid for mid in sorted(candidate_ids)}
        for index, future in enumerate(as_completed(futures), 1):
            mid, tw_drops, rz_drops = future.result()
            if tw_drops:
                tw_hits += 1
            if rz_drops:
                rz_hits += 1
            if tw_drops or rz_drops:
                fetched[mid] = (tw_drops, rz_drops)
            if index % 50 == 0:
                print(f'Independent Zero drop cross-check {index}/{len(futures)}')

    evidence_added = 0
    created = 0
    for mid, (tw_drops, rz_drops) in fetched.items():
        added, new_rows = merge_verified_drop_sources(data.setdefault(str(mid), {'fields': {}, 'drops': [], 'modes': [], 'skills': []}), tw_drops, rz_drops)
        evidence_added += added
        created += new_rows

    # Regression guards for the two lists that exposed the loss.
    argos = data.get('1100') or {}
    spider = next((d for d in argos.get('drops', []) if d.get('itemId') == 480573), None)
    assert spider, argos.get('drops')
    assert {'TWRoZ', 'ROZeroDB'}.issubset(set((spider.get('sources') or {}).keys())), spider

    ak = data.get('1219') or {}
    abyss_helm = next((d for d in ak.get('drops', []) if d.get('itemId') == 401072), None)
    lance = next((d for d in ak.get('drops', []) if d.get('itemId') == 630036), None)
    assert abyss_helm and {'TWRoZ', 'ROZeroDB'}.issubset(set((abyss_helm.get('sources') or {}).keys())), abyss_helm
    assert lance and {'TWRoZ', 'ROZeroDB'}.issubset(set((lance.get('sources') or {}).keys())), lance

    meta['twrozRecheckedDropPages'] = tw_hits
    meta['roZeroDbDropPages'] = rz_hits
    meta['crossCheckDropEvidenceAdded'] = evidence_added
    meta['crossCheckDropRelationsCreated'] = created
    meta['dropVerificationPolicy'] = 'A monster->item relation is eligible only after at least two independent Ragnarok Zero databases agree.'
    save_consensus(data, meta)
    print(json.dumps({
        'candidateMonsters': len(candidate_ids),
        'twrozPagesWithDrops': tw_hits,
        'roZeroDbPagesWithDrops': rz_hits,
        'evidenceAdded': evidence_added,
        'relationsRecoveredFromTwoSources': created,
        'argosSpiderWingsSources': sorted((spider.get('sources') or {}).keys()),
        'abysmalKnightAbyssHelmSources': sorted((abyss_helm.get('sources') or {}).keys()),
        'abysmalKnightLanceSources': sorted((lance.get('sources') or {}).keys()),
    }, indent=2))


if __name__ == '__main__':
    main()
