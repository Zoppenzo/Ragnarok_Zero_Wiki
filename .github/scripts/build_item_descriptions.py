from pathlib import Path
import base64
import hashlib
import json
import zlib

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / 'assets' / 'client-data'

part_paths = [DATA_DIR / f'item-desc.part{i}' for i in range(1, 5)]
parts = [p.read_text(encoding='utf-8').strip() for p in part_paths]
expected_lengths = [47000, 47000, 47000, 46904]
actual_lengths = [len(x) for x in parts]
if actual_lengths != expected_lengths:
    raise SystemExit(f'Unexpected item description chunk lengths: {actual_lengths}')

payload = ''.join(parts)
try:
    raw = zlib.decompress(base64.b64decode(payload, validate=True))
except Exception as exc:
    raise SystemExit(f'Could not decode official item descriptions: {exc}')

actual_sha = hashlib.sha256(raw).hexdigest()
expected_sha = 'f57b339b79cc546ba8d0e76105bc7c715eaa7d34b48f7b0cdd498fcb8ab5e77d'
if actual_sha != expected_sha:
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

compact = json.dumps(overlay, ensure_ascii=False, separators=(',', ':'))
(DATA_DIR / 'item-descriptions.json').write_text(compact, encoding='utf-8')
(ROOT / 'assets' / 'client-item-descriptions.js').write_text(
    'window.RZ_ITEM_DESCRIPTION_OVERLAY=' + compact + ';\n', encoding='utf-8'
)

print(f'Built {len(overlay)} official Zero item description records (SHA256 {actual_sha}).')
