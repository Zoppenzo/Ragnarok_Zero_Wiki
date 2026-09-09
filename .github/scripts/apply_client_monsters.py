from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

scripts = [
    '<script src="assets/client-monsters-data.js"></script>',
    '<script src="assets/client-monsters.js"></script>',
    '<script src="assets/monster-detail-rms.js"></script>',
]

# Remove stale duplicates first, then place the monster loaders after the item
# client loader and before the main application closes over RO_DATA.
for tag in scripts:
    s = s.replace(tag + '\n', '').replace(tag, '')

marker = '<script src="assets/client-items.js"></script>'
if marker not in s:
    raise SystemExit('client-items.js marker not found in index.html')
insert = marker + '\n' + '\n'.join(scripts)
s = s.replace(marker, insert, 1)

# The search database stays a compact list. A clicked monster gets one canonical
# RMS-style detail renderer, instead of the old article/infobox page.
canonical = '''  function monsterDetail(id) {
    const m = getMonster(id);
    if (!m) return notFound();
    queueMicrotask(() => window.RZ_RENDER_RMS_MONSTER_DETAIL?.());
    return `<div class="rz-monster-rms-pending" data-monster-id="${esc(m.id)}"></div>`;
  }
'''
pattern = re.compile(
    r"  function monsterDetail\(id\) \{.*?\n  \}\n\n  function itemDetail\(id, cardRoute=false\) \{",
    re.S,
)
s, count = pattern.subn(canonical + '\n  function itemDetail(id, cardRoute=false) {', s, count=1)
if count != 1:
    raise SystemExit(f'Expected exactly one monsterDetail renderer, replaced {count}')

p.write_text(s, encoding='utf-8')
