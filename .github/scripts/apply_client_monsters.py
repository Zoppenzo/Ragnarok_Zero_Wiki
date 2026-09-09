from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

scripts = [
    '<script src="assets/client-monsters-data.js"></script>',
    '<script src="assets/client-monsters.js"></script>',
]

# Remove stale duplicates first, then place the monster loader after the item
# client loader and before the main application closes over RO_DATA.
for tag in scripts:
    s = s.replace(tag + '\n', '').replace(tag, '')

marker = '<script src="assets/client-items.js"></script>'
if marker not in s:
    raise SystemExit('client-items.js marker not found in index.html')
insert = marker + '\n' + '\n'.join(scripts)
s = s.replace(marker, insert, 1)

p.write_text(s, encoding='utf-8')
