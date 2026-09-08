from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old = """    const mdFirstEssenceRows = firstEssences.flatMap(e=>[\n      {name:e.names[0], effect:e.lv1}, {name:e.names[1], effect:e.lv2}\n    ]);"""
new = """    const mdFirstEssenceLv1Rows = firstEssences.map(e=>({name:e.names[0], effect:e.lv1}));\n    const mdFirstEssenceRows = firstEssences.flatMap(e=>[\n      {name:e.names[0], effect:e.lv1}, {name:e.names[1], effect:e.lv2}\n    ]);"""
assert old in s, 'mdFirstEssenceRows block not found'
s = s.replace(old, new, 1)

old = """      if (pools.includes('first')) rows.push(...mdFirstEssenceRows);\n      if (pools.includes('second')) rows.push(...mdSecondEssenceRows);"""
new = """      if (pools.includes('first-lv1')) rows.push(...mdFirstEssenceLv1Rows);\n      if (pools.includes('first')) rows.push(...mdFirstEssenceRows);\n      if (pools.includes('second')) rows.push(...mdSecondEssenceRows);"""
assert old in s, 'mdEssenceRows pool block not found'
s = s.replace(old, new, 1)

old = "{name:\"Subjugation Team's Armor\", normalSlots:['4th slot'], essenceSlot:'4th slot', essencePools:['first'], open:true}"
new = "{name:\"Subjugation Team's Armor\", normalSlots:['4th slot'], essenceSlot:'4th slot', essencePools:['first-lv1'], open:true}"
assert old in s, 'Subjugation armor row not found'
s = s.replace(old, new, 1)

old = """intro:navLabel('Subjugation equipment is the Grade IV Memorial Dungeon set. Each piece has its own enchant table below. Job Essence is only shown on the compatible armor at +9.','L’équipement Subjugation correspond au Grade IV des Memorial Dungeons. Chaque pièce possède son propre tableau d’enchantement ci-dessous. Les Job Essence ne sont affichées que sur l’armure compatible à +9.')"""
new = """intro:navLabel('Subjugation equipment is the Grade IV Memorial Dungeon set. At +9, Subjugation Team\\'s Armor can roll 1st Job Essence Lv.1 only. Lv.2 Job Essence begins with higher-grade equipment.','L’équipement Subjugation correspond au Grade IV des Memorial Dungeons. À +9, Subjugation Team\\'s Armor peut recevoir uniquement les 1st Job Essence Lv.1. Les Job Essence Lv.2 commencent avec les équipements de grade supérieur.')"""
assert old in s, 'Subjugation intro not found'
s = s.replace(old, new, 1)

p.write_text(s, encoding='utf-8')
print('patched')
