from __future__ import annotations

import json
import re
import unicodedata
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from pathlib import Path

CONSENSUS = Path('assets/monster-zero-consensus.js')
ROZERODB_URL = 'https://rozerodb.com/monsters/{id}'
UA = 'Ragnarok-Zero-Wiki/2.3 (+https://github.com/Zoppenzo/Ragnarok_Zero_Wiki)'


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


def fetch(url: str, timeout: int = 22) -> str | None:
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


def parse_rozerodb_drops(raw: str, mob_id: int) -> list[dict]:
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
        + '// RO ZERO DATABASE is used only as an independent Zero cross-check; one-source relations remain unknown.\n'
        + 'window.RZ_MONSTER_ZERO_CONSENSUS=' + json.dumps(data, ensure_ascii=False, separators=(',', ':'), sort_keys=True) + ';\n'
        + 'window.RZ_MONSTER_ZERO_CONSENSUS_META=' + json.dumps(meta, ensure_ascii=False, separators=(',', ':'), sort_keys=True) + ';\n',
        encoding='utf-8',
    )


def merge_rozerodb(record: dict, rz_drops: list[dict]) -> int:
    drops = record.get('drops') or []
    by_id = {int(d['itemId']): d for d in drops if d.get('itemId') is not None}
    by_name = {normalize_name(d.get('name') or ''): d for d in drops if normalize_name(d.get('name') or '')}
    matched = 0

    for rz in rz_drops:
        target = by_id.get(rz['itemId']) or by_name.get(normalize_name(rz['name']))
        if not target:
            # ROZeroDB alone is never enough to create a relation.
            continue
        sources = target.setdefault('sources', {})
        if 'ROZeroDB' in sources:
            continue
        sources['ROZeroDB'] = rz['rate']
        if target.get('itemId') is None:
            target['itemId'] = rz['itemId']
            by_id[rz['itemId']] = target
        matched += 1

    return matched


def main():
    data, meta = load_consensus()
    candidate_ids = [int(mid) for mid, row in data.items() if row.get('drops')]
    fetched: dict[int, list[dict]] = {}
    page_hits = 0

    def fetch_one(mid: int):
        raw = fetch(ROZERODB_URL.format(id=mid))
        return mid, parse_rozerodb_drops(raw, mid) if raw else []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_one, mid): mid for mid in sorted(candidate_ids)}
        for index, future in enumerate(as_completed(futures), 1):
            mid, drops = future.result()
            if drops:
                fetched[mid] = drops
                page_hits += 1
            if index % 50 == 0:
                print(f'ROZeroDB drop cross-check {index}/{len(futures)}')

    matched = 0
    for mid, rz_drops in fetched.items():
        matched += merge_rozerodb(data.get(str(mid), {}), rz_drops)

    # Regression guards for the two lists that exposed the bug.
    argos = data.get('1100') or {}
    spider = next((d for d in argos.get('drops', []) if d.get('itemId') == 480573), None)
    assert spider and 'ROZeroDB' in (spider.get('sources') or {}), spider
    assert any(src in (spider.get('sources') or {}) for src in {'Prontera', 'TWRoZ'}), spider

    ak = data.get('1219') or {}
    abyss_helm = next((d for d in ak.get('drops', []) if d.get('itemId') == 401072), None)
    assert abyss_helm and 'ROZeroDB' in (abyss_helm.get('sources') or {}), abyss_helm
    assert any(src in (abyss_helm.get('sources') or {}) for src in {'Prontera', 'TWRoZ'}), abyss_helm

    meta['roZeroDbDropPages'] = page_hits
    meta['roZeroDbMatchedDropRelations'] = matched
    meta['dropVerificationPolicy'] = 'A monster->item relation is eligible only after at least two independent Ragnarok Zero databases agree.'
    save_consensus(data, meta)
    print(json.dumps({
        'candidateMonsters': len(candidate_ids),
        'roZeroDbPagesWithDrops': page_hits,
        'matchedExistingRelations': matched,
        'argosSpiderWingsSources': sorted((spider.get('sources') or {}).keys()),
        'abysmalKnightAbyssHelmSources': sorted((abyss_helm.get('sources') or {}).keys()),
    }, indent=2))


if __name__ == '__main__':
    main()
