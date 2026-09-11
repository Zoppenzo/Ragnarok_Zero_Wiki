from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

version='20260911-strict-verified4'
script_paths=[
    'assets/client-monsters-data.js',
    'assets/client-monster-disable-legacy-maps.js',
    'assets/client-monster-identity.js',
    'assets/client-monster-navigation-metadata.js',
    'assets/client-monster-navigation-current.js',
    'assets/client-monster-roster.js',
    'assets/monster-zero-stats.js',
    'assets/monster-zero-consensus.js',
    'assets/rms-monster-behavior.js',
    'assets/client-monsters.js',
    'assets/monster-client-corrections.js',
    'assets/monster-audit-20260909.js',
    'assets/client-monster-current-overlay.js',
    'assets/monster-verified-skill-associations.js',
    'assets/monster-final-fixes.js',
    'assets/monster-instance-maps.js',
    'assets/monster-strict-verification.js',
    'assets/client-monster-sprites.js',
    'assets/monster-detail-rms.js',
    'assets/monster-element-colors.js',
    'assets/monster-mvp-style.js',
    'assets/monster-db-optimized.js',
    'assets/item-monster-drops.js',
]
legacy_sprite_paths=[f'assets/client-monster-sprite-data-{i:02d}.js' for i in range(1,12)]
legacy_nav_paths=[f'assets/client-monster-navigation-current-{i:02d}.js' for i in range(1,5)]
for path in script_paths+legacy_sprite_paths+legacy_nav_paths+['assets/monster-ragnaplace-exp.js']:
    s=re.sub(rf'\s*<script src="{re.escape(path)}(?:\?v=[^"]+)?"></script>\s*','\n',s)
scripts=[f'<script src="{path}?v={version}"></script>' for path in script_paths]

marker='<script src="assets/client-items.js"></script>'
if marker not in s:
    raise SystemExit('client-items.js marker not found in index.html')
s=s.replace(marker,marker+'\n'+'\n'.join(scripts),1)

# client-item-icons.js is part of the older common item bundle and therefore is
# not moved with the monster bundle above. Still bump it whenever the monster
# database is deployed so drop-layout fixes cannot be hidden by browser cache.
s=re.sub(
    r'<script src="assets/client-item-icons\.js(?:\?v=[^"]+)?"></script>',
    f'<script src="assets/client-item-icons.js?v={version}"></script>',
    s,
)

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
print('Strict verified-only monster data wired: exact current-client identity/Navi metadata plus two-source Ragnarok Zero server consensus. Item pages receive the inverse verified monster-drop index.')
