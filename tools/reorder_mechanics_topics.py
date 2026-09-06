from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Rename the Skills entry in General Topics.
s = s.replace(
    "{ id:'skill-usage', group:'General Topics', en:'Skills', fr:'Compétences', href:'#/skills' },",
    "{ id:'skill-usage', group:'General Topics', en:'Skills & Cast Time', fr:'Compétence et Cast Time', href:'#/skills' },",
    1
)

# Reorder Systems & Mechanics and add Memorial Dungeon.
old = """    { id:'elements', group:'Systems & Mechanics', en:'Elements', fr:'Éléments' },
    { id:'monster-sizes', group:'Systems & Mechanics', en:'Monster Sizes', fr:'Tailles des monstres', icon:'monster' },
    { id:'monster-races', group:'Systems & Mechanics', en:'Monster Races', fr:'Races des monstres', icon:'monster' },
    { id:'monster-exclusive-skills', group:'Systems & Mechanics', en:'Monster Skills', fr:'Compétences des monstres' },
    { id:'status-effects', group:'Systems & Mechanics', en:'Status Effects', fr:'Effets de statut' },
    { id:'refinement-system', group:'Systems & Mechanics', en:'Refinement', fr:'Raffinement' },
    { id:'crafting', group:'Systems & Mechanics', en:'Crafting', fr:'Craft' },
    { id:'enchantment', group:'Systems & Mechanics', en:'Enchantment', fr:'Enchantement' },
    { id:'pet-system', group:'Systems & Mechanics', en:'Pet System', fr:'Système de Pet' },
    { id:'mvp-raid', group:'Systems & Mechanics', en:'MVP Raid', fr:'Raid MVP' },
"""
new = """    { id:'elements', group:'Systems & Mechanics', en:'Elements', fr:'Éléments' },
    { id:'monster-sizes', group:'Systems & Mechanics', en:'Monster Sizes', fr:'Tailles des monstres', icon:'monster' },
    { id:'monster-races', group:'Systems & Mechanics', en:'Monster Races', fr:'Races des monstres', icon:'monster' },
    { id:'monster-exclusive-skills', group:'Systems & Mechanics', en:'Monster Skills', fr:'Compétences des monstres' },
    { id:'status-effects', group:'Systems & Mechanics', en:'Status Effects', fr:'Effets de statut' },
    { id:'memorial-dungeons', group:'Systems & Mechanics', en:'Memorial Dungeon', fr:'Mémorial Donjon', href:'#/memorial-dungeons', icon:'memorial' },
    { id:'mvp-raid', group:'Systems & Mechanics', en:'MVP Raid', fr:'Raid MVP' },
    { id:'crafting', group:'Systems & Mechanics', en:'Crafting', fr:'Craft' },
    { id:'refinement-system', group:'Systems & Mechanics', en:'Refinement', fr:'Raffinement' },
    { id:'enchantment', group:'Systems & Mechanics', en:'Enchantment', fr:'Enchantement' },
    { id:'pet-system', group:'Systems & Mechanics', en:'Pet System', fr:'Système de Pet' },
"""
if old not in s:
    raise SystemExit('Systems & Mechanics topic block not found')
s = s.replace(old, new, 1)

# French title fully in French; keep the English title natural.
s = s.replace(
    "<h2>${navLabel('Systems & Mechanics','Système et Mechanics')}</h2>",
    "<h2>${navLabel('Systems & Mechanics','Système et mécanique')}</h2>",
    1
)

# Validation.
assert "fr:'Compétence et Cast Time'" in s
assert "fr:'Mémorial Donjon', href:'#/memorial-dungeons'" in s
assert "navLabel('Systems & Mechanics','Système et mécanique')" in s
block = s[s.index("{ id:'elements', group:'Systems & Mechanics'"):s.index('  ];', s.index("{ id:'elements', group:'Systems & Mechanics'"))]
assert block.index("id:'memorial-dungeons'") < block.index("id:'mvp-raid'") < block.index("id:'crafting'") < block.index("id:'refinement-system'") < block.index("id:'enchantment'")

p.write_text(s, encoding='utf-8')
print('Mechanics navigation updated.')
