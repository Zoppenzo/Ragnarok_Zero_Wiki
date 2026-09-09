from __future__ import annotations

import html
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

IDENTITY = Path('assets/client-monster-identity.js')
OUT = Path('assets/rms-monster-behavior.js')
RATHENA_URL = 'https://raw.githubusercontent.com/rathena/rathena/master/db/re/mob_db.yml'
RMS_URL = 'https://ratemyserver.net/index.php?mob_id={id}&page=re_mob_db'
UA = 'Ragnarok-Zero-Wiki/1.0 (+https://zoppenzo.github.io/Ragnarok_Zero_Wiki/)'
FIELDS = ('walkSpeed', 'attackRange', 'spellRange', 'sightRange', 'delayAfterHit')


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        if data and data.strip():
            self.parts.append(data.strip())


def load_ids() -> list[int]:
    text = IDENTITY.read_text(encoding='utf-8')
    ids = sorted({int(x) for x in re.findall(r'\[\s*(\d{3,6})\s*,', text)})
    if len(ids) < 200:
        raise RuntimeError(f'Only found {len(ids)} client Mob-IDs')
    return ids


def fetch_text(url: str, accept: str = 'text/plain, */*') -> str:
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': accept})
    with urllib.request.urlopen(req, timeout=60) as response:
        return response.read().decode('utf-8', errors='replace')


def walk_speed_label(value: int) -> str:
    # RMS uses "Immovable" for Athena's stationary speed (1000ms and above).
    # Verified moving samples: Mimic 100 -> Very Fast, Hornet 150 -> Fast,
    # Scorpion/Alarm 200/300 -> Slow, Poring 400 -> Very Slow.
    if value >= 1000:
        return 'Immovable'
    if value <= 100:
        return 'Very Fast'
    if value <= 150:
        return 'Fast'
    if value <= 300:
        return 'Slow'
    return 'Very Slow'


def damage_motion_label(value: int, non_attacker: bool) -> str:
    # Non-attacking eggs/plants with the Athena sentinel damage motion are
    # displayed by RMS as n/a rather than as a duration.
    if non_attacker and value <= 1:
        return 'n/a'
    # Verified RMS samples: Mimic 288 -> Very Short, Poring/Arclouze 480 ->
    # Short, Scorpion/Skeleton Prisoner 576 -> Average, Alarm 768 -> Long.
    if value < 400:
        return 'Very Short'
    if value < 550:
        return 'Short'
    if value < 700:
        return 'Average'
    if value < 1000:
        return 'Long'
    return 'Very Long'


def cells(value: int) -> str:
    # RMS keeps the wording "1 cells" even for a single cell.
    return f'{value} cells'


def parse_database(raw: str, requested: set[int]) -> dict[str, dict[str, object]]:
    rows: dict[str, dict[str, object]] = {}
    current_id: int | None = None
    current: dict[str, int | str] = {}

    def flush() -> None:
        nonlocal current_id, current
        if current_id is None or current_id not in requested:
            current = {}
            return

        row: dict[str, object] = {}
        walk = current.get('WalkSpeed')
        damage = current.get('DamageMotion')
        attack_range = current.get('AttackRange')
        skill_range = current.get('SkillRange')
        chase_range = current.get('ChaseRange')
        non_attacker = not isinstance(attack_range, int)

        if isinstance(walk, int):
            row['walkSpeed'] = walk_speed_label(walk)
            row['walkSpeedMs'] = walk
        if isinstance(damage, int):
            row['delayAfterHit'] = damage_motion_label(damage, non_attacker)
            row['damageMotionMs'] = damage
        if isinstance(attack_range, int):
            row['attackRange'] = cells(attack_range)
        elif isinstance(walk, int) and walk >= 1000:
            row['attackRange'] = 'non-attacker'
        if isinstance(skill_range, int):
            row['spellRange'] = cells(skill_range)
        if isinstance(chase_range, int):
            row['sightRange'] = cells(chase_range)

        if row:
            rows[str(current_id)] = row
        current = {}

    for line in raw.splitlines():
        m = re.match(r'^\s{2}- Id:\s*(\d+)\s*$', line)
        if m:
            flush()
            current_id = int(m.group(1))
            current = {}
            continue
        if current_id is None or current_id not in requested:
            continue
        m = re.match(r'^\s{4}(AegisName|WalkSpeed|DamageMotion|AttackRange|SkillRange|ChaseRange):\s*(.+?)\s*$', line)
        if not m:
            continue
        key, value = m.groups()
        if key == 'AegisName':
            current[key] = value
        else:
            try:
                current[key] = int(value)
            except ValueError:
                pass

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

    def grab(pattern: str) -> str | None:
        match = re.search(pattern, text, re.I)
        if not match:
            return None
        value = re.sub(r'\s+', ' ', match.group(1)).strip(' :-')
        return value or None

    row = {
        'walkSpeed': grab(r'Walk Speed\s+(.+?)\s+Job Exp\b'),
        'delayAfterHit': grab(r'Delay After Hit\s+(.+?)\s+Atk Range\b'),
        'attackRange': grab(r'Atk Range\s+(.+?)\s+Str\b'),
        'spellRange': grab(r'Spell Range\s+(.+?)\s+Agi\b'),
        'sightRange': grab(r'Sight Range\s+(.+?)\s+Vit\b'),
    }
    return {key: value for key, value in row.items() if value is not None} or None


def fill_missing_from_rms(rows: dict[str, dict[str, object]], ids: list[int]) -> list[int]:
    # The bulk source normally covers virtually every client ID. For the tiny
    # remainder only, query RMS directly so we do not return to hundreds of
    # requests and trigger its rate limiting.
    missing = [mob_id for mob_id in ids if str(mob_id) not in rows]
    unresolved: list[int] = []
    for mob_id in missing:
        try:
            parsed = parse_rms_page(mob_id, fetch_text(RMS_URL.format(id=mob_id), 'text/html'))
        except Exception as exc:
            print(f'RMS fallback failed for {mob_id}: {type(exc).__name__}: {exc}')
            parsed = None
        if parsed:
            rows[str(mob_id)] = parsed
        else:
            unresolved.append(mob_id)
    return unresolved


def main() -> None:
    ids = load_ids()
    requested = set(ids)
    rows = parse_database(fetch_text(RATHENA_URL), requested)
    unresolved = fill_missing_from_rms(rows, ids)

    complete = [mob_id for mob_id, row in rows.items() if all(row.get(k) is not None for k in FIELDS)]
    minimum = max(240, int(len(ids) * 0.95))
    if len(complete) < minimum:
        raise RuntimeError(
            f'RMS-compatible behavior overlay incomplete: {len(complete)}/{len(ids)} complete rows; '
            f'need at least {minimum}'
        )

    # Hard checks against RateMyServer Renewal pages. These cover ordinary,
    # immovable attacker and immovable non-attacker display cases.
    expected = {
        '1002': ('Very Slow', 'Short', '1 cells', '10 cells', '12 cells'),
        '1193': ('Slow', 'Long', '1 cells', '10 cells', '12 cells'),
        '1191': ('Very Fast', 'Very Short', '1 cells', '10 cells', '12 cells'),
        '1192': ('Slow', 'Very Short', '1 cells', '10 cells', '12 cells'),
        '1001': ('Slow', 'Average', '1 cells', '10 cells', '12 cells'),
        '1020': ('Immovable', 'Average', '4 cells', '10 cells', '12 cells'),
        '1047': ('Immovable', 'n/a', 'non-attacker', '10 cells', '12 cells'),
        '1068': ('Immovable', 'Average', '7 cells', '10 cells', '12 cells'),
    }
    for mob_id, values in expected.items():
        if mob_id not in rows:
            raise RuntimeError(f'Missing required RMS validation mob {mob_id}')
        row = rows[mob_id]
        actual = tuple(row.get(key) for key in FIELDS)
        wanted = (values[0], values[2], values[3], values[4], values[1])
        if actual != wanted:
            raise RuntimeError(f'RMS validation mismatch for {mob_id}: {actual!r} != {wanted!r}')

    meta = {
        'source': 'RateMyServer-compatible Renewal behavior/range fields',
        'bulkSource': 'rAthena Renewal mob_db.yml',
        'bulkSourceUrl': RATHENA_URL,
        'validatedAgainst': 'RateMyServer Renewal Monster Database',
        'fields': list(FIELDS),
        'matched': len(rows),
        'complete': len(complete),
        'requested': len(ids),
        'unresolvedIds': unresolved,
    }
    payload = json.dumps(rows, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    metadata = json.dumps(meta, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    OUT.write_text(
        '// RMS-compatible Renewal behavior/range overlay. Only the five approved display fields are applied.\n'
        '// Bulk values come from rAthena Renewal mob_db and are validated against RateMyServer Renewal samples.\n'
        f'window.RZ_MONSTER_RMS_BEHAVIOR={payload};\n'
        f'window.RZ_MONSTER_RMS_BEHAVIOR_META={metadata};\n',
        encoding='utf-8',
    )
    print(
        f'Wrote {len(rows)} rows ({len(complete)} complete) for {len(ids)} client Mob-IDs; '
        f'unresolved={unresolved}'
    )


if __name__ == '__main__':
    main()
