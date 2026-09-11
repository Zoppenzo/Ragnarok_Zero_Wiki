from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

CONSENSUS = Path('assets/monster-zero-consensus.js')
RAGNADEX = Path('assets/monster-zero-stats.js')

FIELD_TO_RAGNADEX_TARGET = {
    'hp': 'hp',
    'def': 'def',
    'mdef': 'mdef',
    'baseExp': 'baseExp',
    'jobExp': 'jobExp',
}


def parse_js_object(path: Path, var_name: str):
    text = path.read_text(encoding='utf-8')
    marker = f'window.{var_name}='
    if marker not in text:
        raise SystemExit(f'Missing {var_name} in {path}')
    payload = text.split(marker, 1)[1].split(';', 1)[0]
    return json.loads(payload)


def numeric(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return None


def same_number(a, b):
    na, nb = numeric(a), numeric(b)
    return na is not None and nb is not None and abs(na - nb) < 1e-9


def source_value_candidates(value):
    values = value if isinstance(value, list) else [value]
    out = set()
    for v in values:
        n = numeric(v)
        if n is not None:
            out.add(n)
    return out


def strict_field(mid: str, field: str, meta: dict, ragna_verified: dict) -> dict | None:
    sources = meta.get('sources') or {}
    usable = {}

    for source, value in sources.items():
        if numeric(value) is None:
            continue
        if source == 'RagnaDex':
            target = FIELD_TO_RAGNADEX_TARGET.get(field)
            if not target:
                continue
            rvalue = (ragna_verified.get(mid) or {}).get(target)
            if rvalue is None or not same_number(rvalue, value):
                continue
        elif source not in {'TWRoZ', 'Prontera', 'ROZeroDB'}:
            continue
        usable[source] = value

    by_value = defaultdict(list)
    for source, value in usable.items():
        n = numeric(value)
        key = int(n) if n is not None and n.is_integer() else n
        by_value[key].append(source)

    winners = [(value, srcs) for value, srcs in by_value.items() if len(set(srcs)) >= 2]
    if not winners:
        return None
    winners.sort(key=lambda x: (-len(set(x[1])), str(x[0])))
    value, verified_sources = winners[0]
    all_values = {numeric(v) for v in usable.values() if numeric(v) is not None}
    return {
        'value': value,
        'status': 'strict-consensus',
        'conflict': len(all_values) > 1,
        'sources': usable,
        'verifiedSources': sorted(set(verified_sources)),
    }


def strict_drop(drop: dict) -> dict | None:
    sources = drop.get('sources') or {}
    allowed = {'TWRoZ', 'Prontera', 'ROZeroDB'}
    usable = {k: v for k, v in sources.items() if k in allowed}
    if len(usable) < 2:
        return None

    per_source = {source: source_value_candidates(value) for source, value in usable.items()}
    numeric_sources = {source: values for source, values in per_source.items() if values}

    votes = defaultdict(list)
    for source, values in numeric_sources.items():
        for value in values:
            votes[value].append(source)
    winners = [(value, srcs) for value, srcs in votes.items() if len(set(srcs)) >= 2]
    chosen = None
    rate_sources = []
    if winners:
        winners.sort(key=lambda x: (-len(set(x[1])), x[0]))
        chosen, rate_sources = winners[0]
        if isinstance(chosen, float) and chosen.is_integer():
            chosen = int(chosen)

    all_rates = set().union(*numeric_sources.values()) if numeric_sources else set()
    return {
        'itemId': drop.get('itemId'),
        'name': drop.get('name') or '',
        'rate': chosen,
        'status': 'strict-consensus' if chosen is not None else 'relation-consensus',
        'conflict': len(all_rates) > 1,
        'sources': usable,
        'verifiedSources': sorted(usable),
        'rateVerifiedSources': sorted(set(rate_sources)),
        'relationVerified': True,
    }


def main():
    consensus = parse_js_object(CONSENSUS, 'RZ_MONSTER_ZERO_CONSENSUS')
    ragna_verified = parse_js_object(RAGNADEX, 'RZ_MONSTER_ZERO_STATS')

    strict = {}
    field_count = 0
    drop_count = 0
    for mid, record in consensus.items():
        fields = {}
        for field, meta in (record.get('fields') or {}).items():
            accepted = strict_field(mid, field, meta, ragna_verified)
            if accepted:
                fields[field] = accepted
                field_count += 1

        drops = []
        for drop in record.get('drops') or []:
            accepted = strict_drop(drop)
            if accepted:
                drops.append(accepted)
                drop_count += 1

        out = {
            'fields': fields,
            'drops': drops,
            'modes': [],
            'skills': [],
            'spawns': [],
            'sourceAvailability': record.get('sourceAvailability') or {},
        }
        if fields or drops:
            strict[mid] = out

    meta = {
        'sources': ['RagnaDex zero_felder', 'RagnarokZero.net / TWRoZ', 'Prontera.Info ROZ', 'RO ZERO DATABASE / RoZeroDB'],
        'policy': 'STRICT: client data is accepted separately; server data is displayed only when at least two independent Ragnarok Zero databases agree. Unknown stays ???.',
        'monsters': len(strict),
        'verifiedFields': field_count,
        'verifiedDrops': drop_count,
        'dropsPolicy': 'Monster->item requires at least two independent Zero databases. Drop rate requires two matching numeric Zero sources; otherwise rate is ???.',
        'skillsPolicy': 'No monster->skill association is displayed until at least two Zero databases confirm it.',
        'mapsPolicy': 'Only current-client Navi maps are displayed until external maps have two-source Zero confirmation.',
    }

    CONSENSUS.write_text(
        '// Strict cross-database Ragnarok Zero monster consensus.\n'
        + '// Single-source server values are intentionally removed; unknown stays ???.\n'
        + 'window.RZ_MONSTER_ZERO_CONSENSUS=' + json.dumps(strict, ensure_ascii=False, separators=(',', ':'), sort_keys=True) + ';\n'
        + 'window.RZ_MONSTER_ZERO_CONSENSUS_META=' + json.dumps(meta, ensure_ascii=False, separators=(',', ':'), sort_keys=True) + ';\n',
        encoding='utf-8',
    )
    print(json.dumps(meta, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
