from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
index_path = ROOT / "index.html"
text = index_path.read_text(encoding="utf-8")

old = "assets/database/item-ui.png?v=12"
new = "assets/database/item-backpack.svg?v=1"
if old in text:
    text = text.replace(old, new)
elif new not in text:
    raise SystemExit("Could not locate Item database icon path")

index_path.write_text(text, encoding="utf-8")
print("Item database backpack icon applied.")
