from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
index_path = ROOT / "index.html"
text = index_path.read_text(encoding="utf-8")

# Use the existing Item/UI sprite already present in the wiki assets.
# Do not generate or substitute a new backpack drawing.
old_paths = [
    "assets/database/item-ui.png?v=12",
    "assets/database/item-backpack.svg?v=1",
    "assets/database/item-backpack.svg?v=2",
]
new = "assets/database/item-ui.png?v=13"

changed = False
for old in old_paths:
    if old in text:
        text = text.replace(old, new)
        changed = True

if not changed and new not in text:
    raise SystemExit("Could not locate Item database icon path")

index_path.write_text(text, encoding="utf-8")
print("Existing Item database sprite applied.")
