from pathlib import Path
import base64
import hashlib
import json
import lzma

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / 'assets' / 'client-data'
CANONICAL_PATH = DATA_DIR / 'item-descriptions.json'
PART_DIR = DATA_DIR / 'itemdesc85v2'
EXPECTED_SHA = 'a83d6b0ff58c68ea00794ae64ac60d91275b8dd4316016e1f510fd16a00303a5'
EXPECTED_LENGTHS = [18000, 18000, 18000, 18000, 18000, 18000, 15080]

part_paths = [PART_DIR / f'part{i:02d}' for i in range(1, 8)]

if all(p.exists() for p in part_paths):
    parts = [p.read_text(encoding='utf-8').strip() for p in part_paths]
    actual_lengths = [len(x) for x in parts]
    if actual_lengths != EXPECTED_LENGTHS:
        raise SystemExit(f'Unexpected item description chunk lengths: {actual_lengths}')
    try:
        compressed = base64.b85decode(''.join(parts).encode('ascii'))
        raw = lzma.decompress(compressed)
    except Exception as exc:
        raise SystemExit(f'Could not decode official item descriptions: {exc}')
elif CANONICAL_PATH.exists():
    raw = CANONICAL_PATH.read_bytes()
else:
    missing = [str(p.relative_to(ROOT)) for p in part_paths if not p.exists()]
    raise SystemExit('Missing official item description data: ' + ', '.join(missing))

actual_sha = hashlib.sha256(raw).hexdigest()
if actual_sha != EXPECTED_SHA:
    raise SystemExit(f'Unexpected item description SHA256: {actual_sha}')

overlay = json.loads(raw.decode('utf-8'))
if len(overlay) != 4032:
    raise SystemExit(f'Expected 4032 item description records, got {len(overlay)}')

checks = {
    '501': 'Recovery tonic finely ground from Red Herb. Recovers about 45 HP.',
    '517': 'Well-cooked meat, looks appetizing. Recovers a small amount of HP.',
    '519': 'Processed and sterilized milk from cows. Commonly used as nutritious food for Kids. Recovers a small amount of HP.',
    '1201': 'Short dagger designed so anyone can use it with ease.',
}
for item_id, expected in checks.items():
    got = overlay.get(item_id, {}).get('d')
    if got != expected:
        raise SystemExit(f'Unexpected description for {item_id}: {got!r}')

if 'Novice Class' not in overlay.get('1201', {}).get('j', ''):
    raise SystemExit('Knife applicable jobs are missing from official client descriptions')
if overlay.get('4001', {}).get('p') != 'Armor':
    raise SystemExit('Poring Card equipment position is missing from official client descriptions')

compact = json.dumps(overlay, ensure_ascii=False, separators=(',', ':'))
compact_bytes = compact.encode('utf-8')
normalized_sha = hashlib.sha256(compact_bytes).hexdigest()
if normalized_sha != EXPECTED_SHA:
    raise SystemExit(f'Normalized item description SHA256 changed: {normalized_sha}')

CANONICAL_PATH.write_text(compact, encoding='utf-8')
(ROOT / 'assets' / 'client-item-descriptions.js').write_text(
    'window.RZ_ITEM_DESCRIPTION_OVERLAY=' + compact + ';\n', encoding='utf-8'
)

print(f'Built {len(overlay)} official Zero item description records (SHA256 {actual_sha}).')
