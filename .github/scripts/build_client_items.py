from pathlib import Path
import base64
import hashlib
import json
import zlib

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / 'assets' / 'client-data'

part_paths = [DATA_DIR / f'items-core.part{i}' for i in range(1, 5)]
parts = [p.read_text(encoding='utf-8').strip() for p in part_paths]

expected_lengths = [20000, 20000, 20000, 13984]
expected_part_sha = [
    '7e279bbe09369673024898931e905b3d05e2503849d08d8ac51974dc1254e6fe',
    '1aedeaa3d19710d5cecd62b4ba16ee8d2730024e824935960f46c836655f5286',
    '318b4fabb3dfe7a32735ba2994502f06998082598f34c8f6bafe443d1faa2831',
    '72444045d800e6aea903ffb754d7421c9e1fade75d35d1562ebe5f5901737ccb',
]

def digest(text):
    return hashlib.sha256(text.encode('ascii')).hexdigest()

# Part 2 gained one extra character during its first API transfer. Recover the
# exact original chunk by testing each possible one-character deletion against
# the known SHA256 from the locally extracted Zero client data.
if len(parts[1]) == 20001 and digest(parts[1]) != expected_part_sha[1]:
    repaired = None
    for pos in range(len(parts[1])):
        candidate = parts[1][:pos] + parts[1][pos + 1:]
        if digest(candidate) == expected_part_sha[1]:
            repaired = candidate
            break
    if repaired is None:
        raise SystemExit('Could not repair items-core.part2')
    parts[1] = repaired
    part_paths[1].write_text(repaired, encoding='utf-8')

actual_lengths = [len(x) for x in parts]
if actual_lengths != expected_lengths:
    raise SystemExit(f'Unexpected item core chunk lengths: {actual_lengths}')

actual_part_sha = [digest(x) for x in parts]
if actual_part_sha != expected_part_sha:
    problems = [
        f'part{i+1}: {actual_part_sha[i]} expected {expected_part_sha[i]}'
        for i in range(4) if actual_part_sha[i] != expected_part_sha[i]
    ]
    raise SystemExit('Item core chunk hash mismatch: ' + '; '.join(problems))

payload = ''.join(parts)
try:
    raw = zlib.decompress(base64.b64decode(payload, validate=True))
except Exception as exc:
    raise SystemExit(f'Could not decode official item core dataset: {exc}')

actual_sha = hashlib.sha256(raw).hexdigest()
expected_sha = '3397b7bad5a34bd9de0661a627bfc9e7099a56dcd129d9003109ae5903da9524'
if actual_sha != expected_sha:
    raise SystemExit(f'Unexpected official item core SHA256: {actual_sha}')

items = json.loads(raw.decode('utf-8'))
if len(items) != 4033:
    raise SystemExit(f'Expected 4033 items, got {len(items)}')

checks = [(501, 'Red Potion'), (517, 'Meat'), (519, 'Milk'), (1201, 'Knife'), (4001, 'Poring Card'), (5001, 'Headset')]
by_id = {int(x['i']): x for x in items}
for item_id, name in checks:
    row = by_id.get(item_id)
    if not row or row.get('n') != name:
        raise SystemExit(f'Missing expected client item {item_id} / {name}: {row}')

knife = by_id[1201]
if knife.get('a') != 17 or knife.get('t') != 'Equipment':
    raise SystemExit(f'Knife client values are invalid: {knife}')
if by_id[4001].get('t') != 'Card':
    raise SystemExit(f'Poring Card client type is invalid: {by_id[4001]}')

compact = json.dumps(items, ensure_ascii=False, separators=(',', ':'))
(DATA_DIR / 'items.json').write_text(compact, encoding='utf-8')
(ROOT / 'assets' / 'client-items-data.js').write_text('window.RZ_CLIENT_ITEMS=' + compact + ';\n', encoding='utf-8')

print(f'Built {len(items)} official Zero client item records (SHA256 {actual_sha}).')
