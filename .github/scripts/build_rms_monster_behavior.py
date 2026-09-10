from __future__ import annotations

import html
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROSTER = Path('assets/client-monster-roster.js')
OUT = Path('assets/rms-monster-behavior.js')
RATHENA_URL = 'https://raw.githubusercontent.com/rathena/rathena/master/db/re/mob_db.yml'
RMS_URL = 'https://ratemyserver.net/index.php?mob_id={id}&page=re_mob_db'
UA = 'Ragnarok-Zero-Wiki/1.0 (+https://zoppenzo.github.io/Ragnarok_Zero_Wiki/)'
FIELDS = ('walkSpeed',)


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        if data and data.strip():
            self.parts.append(data.strip())


def load_ids() -> list[int]:
    text = ROSTER.read_text(encoding='utf-8')
    ids = sorted({int(x) for x in re.findall(r'\[\s*(\d{2,6})\s*,\s*"', text)})
    if len(ids) != 598:
        raise RuntimeError(f'Expected 598 sprite-backed client Mob-IDs, found {len(ids)}')
    return ids


def fetch_text(url: str, accept: str = 'text/plain, */*') -> str:
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': accept})
    with urllib.request.urlopen(req, timeout=60) as response:
        return response.read().decode('utf-8', errors='replace')


def walk_speed_label(value: int) -> str:
    # RateMyServer-compatible labels. Walk Speed is the only external behavior
    # field intentionally kept in the Ragnarok Zero monster database.
    if value >= 1000:
        return 'Immovable'
    if value <= 100:
        return 'Very Fast'
    if value <= 150:
        return 'Fast'
    if value <= 300:
        return 'Slow'
    return 'Very Slow'


def parse_database(raw: str, requested: set[int]) -> dict[str, dict[str, object]]:
    rows: dict[str, dict[str, object]] = {}
    current_id: int | None = None
    current_walk: int | None = None

    def flush() -> None:
        nonlocal current_id, current_walk
        if current_id is not None and current_id in requested and isinstance(current_walk, int):
            rows[str(current_id)] = {
                'walkSpeed': walk_speed_label(current_walk),
                'walkSpeedMs': current_walk,
            }
        current_walk = None

    for line in raw.splitlines():
        m = re.match(r'^\s{2}- Id:\s*(\d+)\s*$', line)
        if m:
            flush()
            current_id = int(m.group(1))
            continue
        if current_id is None or current_id not in requested:
            continue
        m = re.match(r'^\s{4}WalkSpeed:\s*(\d+)\s*$', line)
        if m:
            current_walk = int(m.group(1))

    flush()
    return rows


def visible_text(raw: str) -> str:
    parser = TextExtractor()
    parser.feed(raw)
    return re.sub(r'\s+', ' ', html.unescape(' '.join(parser.parts))).strip()


def parse_rms_page(mob_id: int, raw: str) -> dict[str, object] | None:
    text = visible_text(raw)
    if not re.search(rf'Mob-ID#\s*{mob_id}\b', text):
        return None
    match = re.search(r'Walk Speed\s+(.+?)\s+Job Exp\b', text, re.I)
    if not match:
        return None
    value = re.sub(r'\s+', ' ', match.group(1)).strip(' :-')
    return {'walkSpeed': value} if value else None


def fill_missing_from_rms(rows: dict[str, dict[str, object]], ids: list[int]) -> list[int]:
    # Query RMS directly only for legacy-range Mob-IDs missing from the bulk
    # database. High custom/Zero IDs and technical variants are left unknown
    # instead of hammering RMS with entries it does not contain.
    missing = [mob_id for mob_id in ids if str(mob_id) not in rows]
    fallback_ids = [mob_id for mob_id in missing if mob_id < 10000]
    unresolved: list[int] = [mob_id for mob_id in missing if mob_id >= 10000]
    for mob_id in fallback_ids:
        try:
            parsed = parse_rms_page(mob_id, fetch_text(RMS_URL.format(id=mob_id), 'text/html'))
        except Exception as exc:
            print(f'RMS fallback failed for {mob_id}: {type(exc).__name__}: {exc}')
            parsed = None
        if parsed:
            rows[str(mob_id)] = parsed
        else:
            unresolved.append(mob_id)
    return sorted(unresolved)


def main() -> None:
    ids = load_ids()
    requested = set(ids)
    rows = parse_database(fetch_text(RATHENA_URL), requested)
    unresolved = fill_missing_from_rms(rows, ids)

    complete = [mob_id for mob_id, row in rows.items() if row.get('walkSpeed') is not None]
    # The full sprite roster deliberately includes Zero-only/event/quest/test
    # identities that RateMyServer/rAthena may not know. Guard against a real
    # regression without requiring impossible 95% coverage of those entries.
    minimum = 300
    if len(complete) < minimum:
        raise RuntimeError(
            f'RMS Walk Speed overlay incomplete: {len(complete)}/{len(ids)} complete rows; '
            f'need at least {minimum}'
        )

    # Hard checks against known RateMyServer-compatible Renewal values.
    expected = {
        '1002': 'Very Slow',
        '1193': 'Slow',
        '1191': 'Very Fast',
        '1192': 'Slow',
        '1001': 'Slow',
        '1020': 'Immovable',
        '1047': 'Immovable',
        '1068': 'Immovable',
    }
    for mob_id, wanted in expected.items():
        if mob_id not in rows:
            raise RuntimeError(f'Missing required RMS validation mob {mob_id}')
        actual = rows[mob_id].get('walkSpeed')
        if actual != wanted:
            raise RuntimeError(f'RMS Walk Speed validation mismatch for {mob_id}: {actual!r} != {wanted!r}')

    meta = {
        'source': 'RateMyServer-compatible Renewal Walk Speed',
        'bulkSource': 'rAthena Renewal mob_db.yml',
        'bulkSourceUrl': RATHENA_URL,
        'validatedAgainst': 'RateMyServer Renewal Monster Database',
        'fields': list(FIELDS),
        'matched': len(rows),
        'complete': len(complete),
        'requested': len(ids),
        'rosterPolicy': 'all 598 sprite-backed client identities',
        'unresolvedIds': unresolved,
    }
    payload = json.dumps(rows, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    metadata = json.dumps(meta, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    OUT.write_text(
        '// RateMyServer-compatible Walk Speed overlay. Walk Speed is the only external behavior field kept.\n'
        '// Bulk values come from rAthena Renewal mob_db and are validated against RateMyServer Renewal samples.\n'
        f'window.RZ_MONSTER_RMS_BEHAVIOR={payload};\n'
        f'window.RZ_MONSTER_RMS_BEHAVIOR_META={metadata};\n',
        encoding='utf-8',
    )
    print(
        f'Wrote Walk Speed for {len(rows)} rows ({len(complete)} complete) for {len(ids)} roster Mob-IDs; '
        f'unresolved={len(unresolved)}'
    )


if __name__ == '__main__':
    main()
