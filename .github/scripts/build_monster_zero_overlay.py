from __future__ import annotations

import json
import urllib.request
from pathlib import Path

URL = "https://ragnadex.com/api/monsters.json"
OUT = Path("assets/monster-zero-stats.js")

req = urllib.request.Request(
    URL,
    headers={
        "User-Agent": "Ragnarok-Zero-Wiki/1.0 (+https://github.com/Zoppenzo/Ragnarok_Zero_Wiki)",
        "Accept": "application/json",
    },
)
with urllib.request.urlopen(req, timeout=45) as response:
    rows = json.load(response)

if not isinstance(rows, list) or len(rows) < 400:
    raise SystemExit(f"Unexpected RagnaDex monster payload: {type(rows).__name__}, {len(rows) if isinstance(rows, list) else 'n/a'} rows")

field_map = {
    "hp": "hp",
    "def": "def",
    "mdef": "mdef",
    "basis_exp": "baseExp",
    "job_exp": "jobExp",
}
element_names = {
    "Neutral": "Neutral",
    "Water": "Water",
    "Earth": "Earth",
    "Fire": "Fire",
    "Wind": "Wind",
    "Poison": "Poison",
    "Holy": "Holy",
    "Dark": "Shadow",
    "Shadow": "Shadow",
    "Ghost": "Ghost",
    "Undead": "Undead",
}

overlay: dict[str, dict] = {}
for row in rows:
    if not isinstance(row, dict) or row.get("id") is None:
        continue
    verified = set(row.get("zero_felder") or [])
    record: dict = {}
    for source_key, target_key in field_map.items():
        value = row.get(source_key)
        if source_key in verified and value is not None:
            record[target_key] = value
    if "elementtabelle" in verified and isinstance(row.get("elementtabelle"), dict):
        mods = {}
        for source_name, value in row["elementtabelle"].items():
            target_name = element_names.get(source_name)
            if target_name and value is not None:
                mods[target_name] = value
        if mods:
            record["elementModifiers"] = mods
    if record:
        overlay[str(int(row["id"]))] = record

if len(overlay) < 400:
    raise SystemExit(f"Too few verified monster overlays: {len(overlay)}")

poring = overlay.get("1002") or {}
expected = {"hp": 55, "def": 2, "mdef": 5, "baseExp": 150, "jobExp": 30}
for key, value in expected.items():
    if poring.get(key) != value:
        raise SystemExit(f"Poring validation failed for {key}: {poring.get(key)!r} != {value!r}")
if poring.get("elementModifiers", {}).get("Water") != 25:
    raise SystemExit("Poring Zero element table validation failed")

payload = json.dumps(overlay, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
OUT.write_text(
    "// Verified Ragnarok Zero monster fields imported from the open RagnaDex API.\n"
    "// Only fields explicitly listed by the source in zero_felder are included.\n"
    f"window.RZ_MONSTER_ZERO_STATS={payload};\n"
    "window.RZ_MONSTER_ZERO_STATS_META={source:'RagnaDex',url:'https://ragnadex.com/en/api/',policy:'zero_felder only'};\n",
    encoding="utf-8",
)
print(f"Built {len(overlay)} verified Zero monster overlays -> {OUT}")
