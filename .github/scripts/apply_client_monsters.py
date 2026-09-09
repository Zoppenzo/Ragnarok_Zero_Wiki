from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

scripts=[
    '<script src="assets/client-monsters-data.js"></script>',
    '<script src="assets/client-monster-identity.js"></script>',
    '<script src="assets/monster-zero-stats.js"></script>',
    '<script src="assets/rms-monster-behavior.js"></script>',
    '<script src="assets/client-monsters.js"></script>',
    '<script src="assets/client-monster-sprites.js"></script>',
    '<script src="assets/monster-detail-rms.js"></script>',
    '<script src="assets/monster-element-colors.js"></script>',
    '<script src="assets/monster-db-optimized.js"></script>',
]
for tag in scripts:
    s=s.replace(tag+'\n','').replace(tag,'')

marker='<script src="assets/client-items.js"></script>'
if marker not in s:
    raise SystemExit('client-items.js marker not found in index.html')
s=s.replace(marker,marker+'\n'+'\n'.join(scripts),1)

monster_wire="    setTimeout(() => { if (window.RZ_MONSTER_DB_OPT?.wire(type)) return; if (!window.RZ_ITEM_DB_OPT?.wire(type)) wireList(type); }, 0);"
item_wire="    setTimeout(() => { if (!window.RZ_ITEM_DB_OPT?.wire(type)) wireList(type); }, 0);"
legacy_wire='    setTimeout(() => wireList(type), 0);'
if item_wire in s:
    s=s.replace(item_wire,monster_wire,1)
elif legacy_wire in s:
    s=s.replace(legacy_wire,monster_wire,1)
elif monster_wire not in s:
    raise SystemExit('Could not wire paginated monster database renderer')

canonical='''  function monsterDetail(id) {
    const m = getMonster(id);
    if (!m) return notFound();
    queueMicrotask(() => window.RZ_RENDER_RMS_MONSTER_DETAIL?.());
    return `<div class="rz-monster-rms-pending" data-monster-id="${esc(m.id)}"></div>`;
  }
'''
pattern=re.compile(r"  function monsterDetail\(id\) \{.*?\n  \}\n\n  function itemDetail\(id, cardRoute=false\) \{",re.S)
s,count=pattern.subn(canonical+'\n  function itemDetail(id, cardRoute=false) {',s,count=1)
if count!=1:
    raise SystemExit(f'Expected exactly one monsterDetail renderer, replaced {count}')

p.write_text(s,encoding='utf-8')
print('Official monster identity, verified Zero stats, RMS behavior fields, element badges and animated sprite renderer wired.')
