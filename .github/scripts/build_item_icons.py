from pathlib import Path
import base64
import json
import zlib

# Rebuild and validate the official-client item icon map before deployment.
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'assets' / 'client-data'

parts = [DATA / f'item-icons-map.part{i}' for i in range(1, 4)]
payload = ''.join(p.read_text(encoding='utf-8').strip() for p in parts)
raw = zlib.decompress(base64.b64decode(payload, validate=True))
rows = json.loads(raw.decode('utf-8'))

if len(rows) != 3954:
    raise SystemExit(f'Expected 3954 item icon mappings, got {len(rows)}')

by_id = {int(r['i']): r for r in rows}
checks = {
    517: 'Meat',
    519: 'Milk',
    1201: 'Knife',
    4001: 'Poring Card',
}
for item_id, name in checks.items():
    row = by_id.get(item_id)
    if not row or row.get('n') != name or row.get('ic') is None:
        raise SystemExit(f'Invalid item icon mapping for {item_id} / {name}: {row}')

(DATA / 'item-icons.json').write_text(
    json.dumps(rows, ensure_ascii=False, separators=(',', ':')),
    encoding='utf-8',
)
print(f'Built {len(rows)} official-client item icon mappings.')
