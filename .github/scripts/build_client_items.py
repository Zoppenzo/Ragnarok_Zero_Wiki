from pathlib import Path
import base64
import hashlib
import json
import zlib

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "assets" / "client-data"

parts = [DATA_DIR / f"items.part{i}" for i in range(1, 5)]
payload = "".join(p.read_text(encoding="utf-8").strip() for p in parts)
try:
    raw = zlib.decompress(base64.b64decode(payload, validate=True))
except Exception as exc:
    raise SystemExit(f"Could not decode official item dataset ({len(payload)} base64 chars): {exc}")

actual_sha = hashlib.sha256(raw).hexdigest()
items = json.loads(raw.decode("utf-8"))
if len(items) != 4033:
    raise SystemExit(f"Expected 4033 items, got {len(items)} (SHA256 {actual_sha})")

checks = [
    (501, "Red Potion"),
    (1201, "Knife"),
    (4001, "Poring Card"),
    (5001, "Headset"),
]
for item_id, name in checks:
    if not any(x.get("i") == item_id and x.get("n") == name for x in items):
        raise SystemExit(f"Missing expected client item {item_id} / {name} (SHA256 {actual_sha})")

knife = next(x for x in items if x.get("i") == 1201)
if knife.get("a") != 17 or knife.get("t") != "Equipment":
    raise SystemExit(f"Knife client values are invalid: {knife}")
poring_card = next(x for x in items if x.get("i") == 4001)
if poring_card.get("t") != "Card":
    raise SystemExit(f"Poring Card client type is invalid: {poring_card}")

compact = json.dumps(items, ensure_ascii=False, separators=(",", ":"))
(DATA_DIR / "items.json").write_text(compact, encoding="utf-8")
(ROOT / "assets" / "client-items-data.js").write_text(
    "window.RZ_CLIENT_ITEMS=" + compact + ";\n",
    encoding="utf-8",
)

print(f"Built {len(items)} official client item records (SHA256 {actual_sha}).")
