from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

IDENTITY = Path('assets/client-monster-identity.js')
OUT = Path('assets/rms-monster-behavior.js')
RATHENA_URL = 'https://raw.githubusercontent.com/rathena/rathena/master/db/re/mob_db.yml'
UA = 'Ragnarok-Zero-Wiki/1.0 (+https://zoppenzo.github.io/Ragnarok_Zero_Wiki/)'


def load_ids() -> list[int]:
    text = IDENTITY.read_text(encoding='utf-8')
    ids = sorted({int(x) for x in re.findall(r'\[\s*(\d{3,6})\s*,', text)})
    if len(ids) < 200:
        raise RuntimeError(f'Only found {len(ids)} client Mob-IDs')
    return ids


def fetch_database() -> str:
    req = urllib.request.Request(
        RATHENA_URL,
        headers={'User-Agent': UA, 'Accept': 'text/plain, */*'},
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        return response.read().decode('utf-8', errors='replace')


def walk_speed_label(value: int) -> str:
    # RateMyServer presents Athena walk-speed milliseconds as four readable
    # buckets. These thresholds reproduce RMS for the verified samples:
    # Mimic 100 -> Very Fast, Hornet 150 -> Fast, Scorpion/Alarm 200/300 ->
    # Slow, Poring 400 -> Very Slow.
    if value <= 100:
        return 'Very Fast'
    if value <= 150:
        return 'Fast'
    if value <= 300:
        return 'Slow'
    return 'Very Slow'


def damage_motion_label(value: int) -> str:
    # RMS labels the post-hit damage motion rather than showing milliseconds.
    # Verified samples: Mimic 288 -> Very Short, Poring/Arclouze 480 -> Short,
    # Scorpion/Skeleton Prisoner 576 -> Average, Alarm 768 -> Long.
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
    # RMS itself uses the wording "1 cells", so keep its display convention.
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

        if isinstance(walk, int):
            row['walkSpeed'] = walk_speed_label(walk)
            row['walkSpeedMs'] = walk
        if isinstance(damage, int):
            row['delayAfterHit'] = damage_motion_label(damage)
            row['damageMotionMs'] = damage
        if isinstance(attack_range, int):
            row['attackRange'] = cells(attack_range)
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


def main() -> None:
    ids = load_ids()
    requested = set(ids)
    raw = fetch_database()
    rows = parse_database(raw, requested)

    complete = [
        mob_id for mob_id, row in rows.items()
        if all(row.get(k) for k in ('walkSpeed', 'delayAfterHit', 'attackRange', 'spellRange', 'sightRange'))
    ]
    minimum = max(200, int(len(ids) * 0.90))
    if len(complete) < minimum:
        raise RuntimeError(
            f'RMS-compatible behavior overlay incomplete: {len(complete)}/{len(ids)} complete rows; '
            f'need at least {minimum}'
        )

    # Hard checks against RateMyServer Renewal pages. These catch accidental
    # parser or display-bucket changes before anything is deployed.
    expected = {
        '1002': ('Very Slow', 'Short', '1 cells', '10 cells', '12 cells'),
        '1193': ('Slow', 'Long', '1 cells', '10 cells', '12 cells'),
        '1191': ('Very Fast', 'Very Short', '1 cells', '10 cells', '12 cells'),
        '1192': ('Slow', 'Very Short', '1 cells', '10 cells', '12 cells'),
        '1001': ('Slow', 'Average', '1 cells', '10 cells', '12 cells'),
    }
    for mob_id, values in expected.items():
        if mob_id not in rows:
            raise RuntimeError(f'Missing required RMS validation mob {mob_id}')
        row = rows[mob_id]
        actual = (
            row.get('walkSpeed'), row.get('delayAfterHit'), row.get('attackRange'),
            row.get('spellRange'), row.get('sightRange'),
        )
        if actual != values:
            raise RuntimeError(f'RMS validation mismatch for {mob_id}: {actual!r} != {values!r}')

    meta = {
        'source': 'RateMyServer-compatible Renewal behavior/range fields',
        'bulkSource': 'rAthena Renewal mob_db.yml',
        'bulkSourceUrl': RATHENA_URL,
        'validatedAgainst': 'RateMyServer Renewal Monster Database',
        'fields': ['walkSpeed', 'attackRange', 'spellRange', 'sightRange', 'delayAfterHit'],
        'matched': len(rows),
        'complete': len(complete),
        'requested': len(ids),
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
    print(f'Wrote {len(rows)} rows ({len(complete)} complete) for {len(ids)} client Mob-IDs to {OUT}')


if __name__ == '__main__':
    main()
