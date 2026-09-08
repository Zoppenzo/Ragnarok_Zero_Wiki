from pathlib import Path
import base64
import hashlib
import json
import zlib

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "assets" / "client-data"

parts = [DATA_DIR / f"items.part{i}" for i in range(1, 5)]
payload = "".join(p.read_text(encoding="utf-8").strip() for p in parts)
raw = zlib.decompress(base64.b64decode(payload))

expected_sha = "5422d9866339af927f04885fe27d27f38eb6a1f4b5031a1adccda5e555e30732"
actual_sha = hashlib.sha256(raw).hexdigest()
if actual_sha != expected_sha:
    raise SystemExit(f"Unexpected item dataset SHA256: {actual_sha}")

items = json.loads(raw.decode("utf-8"))
if len(items) != 4033:
    raise SystemExit(f"Expected 4033 items, got {len(items)}")

if not any(x.get("i") == 1201 and x.get("n") == "Knife" and x.get("a") == 17 for x in items):
    raise SystemExit("Knife client record validation failed")
if not any(x.get("i") == 4001 and x.get("n") == "Poring Card" and x.get("t") == "Card" for x in items):
    raise SystemExit("Poring Card client record validation failed")

compact = json.dumps(items, ensure_ascii=False, separators=(",", ":"))
(DATA_DIR / "items.json").write_text(compact, encoding="utf-8")
(ROOT / "assets" / "client-items-data.js").write_text(
    "window.RZ_CLIENT_ITEMS=" + compact + ";\n",
    encoding="utf-8",
)

print(f"Built {len(items)} official client item records ({actual_sha}).")
