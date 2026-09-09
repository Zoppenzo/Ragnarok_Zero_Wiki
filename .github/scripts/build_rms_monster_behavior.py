from __future__ import annotations

import html
import json
import re
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from pathlib import Path

IDENTITY = Path('assets/client-monster-identity.js')
OUT = Path('assets/rms-monster-behavior.js')
URL = 'https://ratemyserver.net/index.php?mob_id={id}&page=re_mob_db'
UA = 'Ragnarok-Zero-Wiki/1.0 (+https://zoppenzo.github.io/Ragnarok_Zero_Wiki/)'


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        if data and data.strip():
            self.parts.append(data.strip())


def visible_text(raw: str) -> str:
    p = TextExtractor()
    p.feed(raw)
    return re.sub(r'\s+', ' ', html.unescape(' '.join(p.parts))).strip()


def clean(value: str | None) -> str | None:
    if not value:
        return None
    value = re.sub(r'\s+', ' ', value).strip(' :-')
    return value if value and value.lower() not in {'n/a', 'na'} else None


def parse_page(mob_id: int, raw: str) -> dict[str, object] | None:
    text = visible_text(raw)
    if not re.search(rf'Mob-ID#\s*{mob_id}\b', text):
        return None

    def grab(pattern: str) -> str | None:
        m = re.search(pattern, text, re.I)
        return clean(m.group(1)) if m else None

    walk = grab(r'Walk Speed\s+(.+?)\s+Job Exp\b')
    delay = grab(r'Delay After Hit\s+(.+?)\s+Atk Range\b')
    atk_range = grab(r'Atk Range\s+(.+?)\s+Str\b')
    spell_range = grab(r'Spell Range\s+(.+?)\s+Agi\b')
    sight_range = grab(r'Sight Range\s+(.+?)\s+Vit\b')

    row = {}
    if walk: row['walkSpeed'] = walk
    if delay: row['delayAfterHit'] = delay
    if atk_range: row['attackRange'] = atk_range
    if spell_range: row['spellRange'] = spell_range
    if sight_range: row['sightRange'] = sight_range
    return row or None


def fetch_one(mob_id: int) -> tuple[int, dict[str, object] | None, str | None]:
    last_error = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(URL.format(id=mob_id), headers={'User-Agent': UA, 'Accept': 'text/html'})
            with urllib.request.urlopen(req, timeout=20) as response:
                raw = response.read().decode('utf-8', errors='replace')
            return mob_id, parse_page(mob_id, raw), None
        except Exception as exc:
            last_error = f'{type(exc).__name__}: {exc}'
            time.sleep(0.4 * (attempt + 1))
    return mob_id, None, last_error


def load_ids() -> list[int]:
    text = IDENTITY.read_text(encoding='utf-8')
    # Identity rows are compact arrays beginning with the canonical Mob-ID.
    ids = sorted({int(x) for x in re.findall(r'\[\s*(\d{3,6})\s*,', text)})
    if len(ids) < 300:
        raise RuntimeError(f'Only found {len(ids)} client Mob-IDs')
    return ids


def load_existing() -> dict[str, object]:
    if not OUT.exists():
        return {}
    text = OUT.read_text(encoding='utf-8')
    m = re.search(r'window\.RZ_MONSTER_RMS_BEHAVIOR=(\{.*?\});\s*window\.RZ_MONSTER_RMS_BEHAVIOR_META=', text, re.S)
    if not m:
        return {}
    try:
        return json.loads(m.group(1))
    except Exception:
        return {}


def main() -> None:
    ids = load_ids()
    existing = load_existing()
    rows: dict[str, object] = {}
    errors: dict[str, str] = {}

    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(fetch_one, mob_id): mob_id for mob_id in ids}
        for i, fut in enumerate(as_completed(futures), 1):
            mob_id, row, error = fut.result()
            if row:
                rows[str(mob_id)] = row
            elif error:
                errors[str(mob_id)] = error
            if i % 50 == 0:
                print(f'RateMyServer: {i}/{len(ids)} checked, {len(rows)} matched')

    # If RMS is temporarily unavailable, keep the last good cached data.
    if len(rows) < 250 and len(existing) >= 250:
        print(f'Only {len(rows)} fresh RMS rows; retaining cached {len(existing)} rows.')
        rows = existing
    elif len(rows) < 250:
        raise RuntimeError(f'RateMyServer overlay too small: {len(rows)} matched rows')

    meta = {
        'source': 'RateMyServer Renewal Monster Database',
        'sourceUrl': 'https://ratemyserver.net/index.php?page=re_mob_db',
        'fields': ['walkSpeed', 'attackRange', 'spellRange', 'sightRange', 'delayAfterHit'],
        'matched': len(rows),
        'requested': len(ids),
        'errors': len(errors),
    }
    payload = json.dumps(rows, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    metadata = json.dumps(meta, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    OUT.write_text(
        '// RateMyServer Renewal behavior/range overlay. Only the five explicitly approved fields are imported.\n'
        f'window.RZ_MONSTER_RMS_BEHAVIOR={payload};\n'
        f'window.RZ_MONSTER_RMS_BEHAVIOR_META={metadata};\n',
        encoding='utf-8',
    )
    print(f'Wrote {len(rows)} RateMyServer behavior rows to {OUT}')


if __name__ == '__main__':
    main()
