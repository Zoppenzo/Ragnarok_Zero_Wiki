from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

CONSENSUS = Path('assets/monster-zero-consensus.js')
ROZERODB_URL = 'https://rozerodb.com/monsters/{id}'
UA = 'Ragnarok-Zero-Wiki/2.5 (+https://github.com/Zoppenzo/Ragnarok_Zero_Wiki)'

EXPECTED = {
    '25327': {
        'internalName': 'BOULDERDWARF_HAMMER_MJ',
        'fields': {'hp': 32952, 'def': 198, 'mdef': 15},
    },
    '25328': {
        'internalName': 'BOULDERDWARF_MACE_MJ',
        'fields': {'hp': 55602, 'def': 179, 'mdef': 30},
    },
    '25329': {
        'internalName': 'BOULDERDWARF_LEADER_MJ',
        'fields': {'hp': 54704, 'def': 224, 'mdef': 23},
    },
    # Swordmaster is intentionally not given HP/DEF/MDEF here: the current
    # Zero databases still publish those fields as unknown.
    '25336': {
        'internalName': 'BOULDERDWARF_SM',
        'fields': {},
    },
}


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
        raw = ''.join(self.parts)
        return '\n'.join(re.sub(r'\s+', ' ', line).strip() for line in raw.splitlines() if line.strip())


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'text/html,*/*;q=0.8'})
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            return response.read().decode('utf-8', 'replace')
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
        raise SystemExit(f'Unable to fetch {url}: {exc}')


def numeric_label(text: str, label: str):
    # ROZeroDB renders values both in summary cards and in Core Statistics.
    m = re.search(rf'(?im)(?:^|\b){re.escape(label)}\s*([\d,]+)\b', text)
    if not m:
        return None
    return int(m.group(1).replace(',', ''))


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
        + '// Boulder Dwarf server stats below are retained only when TWRoZ and RO ZERO DATABASE agree exactly.\n'
        + 'window.RZ_MONSTER_ZERO_CONSENSUS=' + json.dumps(data, ensure_ascii=False, separators=(',', ':'), sort_keys=True) + ';\n'
        + 'window.RZ_MONSTER_ZERO_CONSENSUS_META=' + json.dumps(meta, ensure_ascii=False, separators=(',', ':'), sort_keys=True) + ';\n',
        encoding='utf-8',
    )


def main():
    data, meta = load_consensus()
    verified = {}

    for mid, spec in EXPECTED.items():
        raw = fetch(ROZERODB_URL.format(id=mid))
        parser = VisibleTextParser()
        parser.feed(raw)
        text = parser.text()

        if f'#{mid}' not in text or spec['internalName'] not in text:
            raise SystemExit(f'ROZeroDB identity mismatch for #{mid} {spec["internalName"]}')

        record = data.get(mid)
        if not record:
            raise SystemExit(f'Raw Zero consensus is missing Boulder Dwarf #{mid}')

        rz_values = {
            'hp': numeric_label(text, 'HP'),
            'def': numeric_label(text, 'DEF'),
            'mdef': numeric_label(text, 'MDEF'),
        }

        if not spec['fields']:
            # No fabricated fallback for Swordmaster. Its current ROZeroDB page
            # explicitly has these server fields unknown, so it stays ???.
            if any(rz_values.values()):
                raise SystemExit(f'Unexpected new Swordmaster core stats found: {rz_values}')
            verified[mid] = {'keptUnknown': True}
            continue

        field_result = {}
        for field, expected in spec['fields'].items():
            rz_value = rz_values[field]
            if rz_value != expected:
                raise SystemExit(f'ROZeroDB #{mid} {field}: expected {expected}, got {rz_value}')

            fmeta = (record.get('fields') or {}).get(field)
            if not fmeta:
                raise SystemExit(f'Raw consensus #{mid} is missing {field}; cannot establish two-source proof')
            sources = fmeta.setdefault('sources', {})
            tw_value = sources.get('TWRoZ')
            if tw_value != expected:
                raise SystemExit(f'TWRoZ #{mid} {field}: expected {expected}, got {tw_value}')

            sources['ROZeroDB'] = rz_value
            field_result[field] = {'value': expected, 'sources': ['TWRoZ', 'ROZeroDB']}

        verified[mid] = field_result

    meta['boulderDwarfStatCrossCheck'] = verified
    meta['boulderDwarfPolicy'] = 'HP/DEF/MDEF are kept only when TWRoZ and RO ZERO DATABASE match exactly; otherwise ???.'
    save_consensus(data, meta)
    print(json.dumps(verified, indent=2))


if __name__ == '__main__':
    main()
