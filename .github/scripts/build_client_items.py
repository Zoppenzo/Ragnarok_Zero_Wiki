from pathlib import Path
import base64
import hashlib
import json
import zlib

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "assets" / "client-data"

part_paths = [DATA_DIR / f"items.part{i}" for i in range(1, 5)]
parts = [p.read_text(encoding="utf-8").strip() for p in part_paths]

# A single character was lost from part 3 during its first API transfer.
if len(parts[2]) == 15999 and "CKDNXY4daq" in parts[2]:
    parts[2] = parts[2].replace("CKDNXY4daq", "CKDNXY4Edaq", 1)
    part_paths[2].write_text(parts[2], encoding="utf-8")

expected_lengths = [16000, 16000, 16000, 13116]
actual_lengths = [len(x) for x in parts]
if actual_lengths != expected_lengths:
    raise SystemExit(f"Unexpected item chunk lengths: {actual_lengths}")

expected_part_sha = [
    "e9ed7f08c17a76111c642a234db69ee878c68d91cd973300c8b416671552a7a9",
    "1766cba589849fbfad543f84dfe31f86a5796b119a6f5df8bed63e2ad7ac44d9",
    "b2b36f6237ded6ef7f6c3a3b94328a074514b5b9d4413deb70418e9583ee342a",
    "dcdfd78acf42ae8dd731450c3f7af622fb9c4e0c07f40c0800eee8e8066256c0",
]
actual_part_sha = [hashlib.sha256(x.encode("ascii")).hexdigest() for x in parts]
if actual_part_sha != expected_part_sha:
    problems = [
        f"part{i+1}: {actual_part_sha[i]} expected {expected_part_sha[i]}"
        for i in range(4) if actual_part_sha[i] != expected_part_sha[i]
    ]
    raise SystemExit("Item chunk hash mismatch: " + "; ".join(problems))

payload = "".join(parts)
try:
    raw = zlib.decompress(base64.b64decode(payload, validate=True))
except Exception as exc:
    raise SystemExit(f"Could not decode official item dataset ({len(payload)} base64 chars): {exc}")

actual_sha = hashlib.sha256(raw).hexdigest()
expected_sha = "5422d9866339af927f04885fe27d27f38eb6a1f4b5031a1adccda5e555e30732"
if actual_sha != expected_sha:
    raise SystemExit(f"Unexpected official item dataset SHA256: {actual_sha}")

items = json.loads(raw.decode("utf-8"))
if len(items) != 4033:
    raise SystemExit(f"Expected 4033 items, got {len(items)}")

checks = [(501, "Red Potion"), (1201, "Knife"), (4001, "Poring Card"), (5001, "Headset")]
for item_id, name in checks:
    if not any(x.get("i") == item_id and x.get("n") == name for x in items):
        raise SystemExit(f"Missing expected client item {item_id} / {name}")

knife = next(x for x in items if x.get("i") == 1201)
if knife.get("a") != 17 or knife.get("t") != "Equipment":
    raise SystemExit(f"Knife client values are invalid: {knife}")
poring_card = next(x for x in items if x.get("i") == 4001)
if poring_card.get("t") != "Card":
    raise SystemExit(f"Poring Card client type is invalid: {poring_card}")

compact = json.dumps(items, ensure_ascii=False, separators=(",", ":"))
(DATA_DIR / "items.json").write_text(compact, encoding="utf-8")
(ROOT / "assets" / "client-items-data.js").write_text("window.RZ_CLIENT_ITEMS=" + compact + ";\n", encoding="utf-8")

print(f"Built {len(items)} official client item records (SHA256 {actual_sha}).")
