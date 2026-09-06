from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

start = s.index('  const TOPICS = [')
end = s.index('  ];', start) + len('  ];')

new_topics = '''  const TOPICS = [
    { id:'introduction', group:'General Topics', en:'Introduction to Ragnarok', fr:'Introduction à Ragnarok', icon:'introduction' },
    { id:'getting-started', group:'General Topics', en:'Getting Started', fr:'Bien débuter', icon:'start' },
    { id:'basic-controls', group:'General Topics', en:'Basic Controls', fr:'Contrôles de base', icon:'controls' },
    { id:'useful-info', group:'General Topics', en:'Useful Information', fr:'Informations utiles', icon:'info' },
    { id:'glossary', group:'General Topics', en:'Glossary', fr:'Glossaire', icon:'glossary' },
    { id:'classes', group:'General Topics', en:'Classes', fr:'Classes', href:'#/classes' },
    { id:'levels', group:'General Topics', en:'Levels', fr:'Niveaux' },
    { id:'experience', group:'General Topics', en:'Experience', fr:'Expérience' },
    { id:'party', group:'General Topics', en:'Party', fr:'Groupe / Party' },
    { id:'guild-system', group:'General Topics', en:'Guild', fr:'Guilde' },
    { id:'auto-hunt', group:'General Topics', en:'Auto-Hunt', fr:'Chasse automatique' },
    { id:'stats', group:'General Topics', en:'Stats', fr:'Statistiques' },
    { id:'skill-usage', group:'General Topics', en:'Skills', fr:'Compétences', href:'#/skills' },
    { id:'quests', group:'General Topics', en:'Quests', fr:'Quêtes', href:'#/quests' },
    { id:'items', group:'General Topics', en:'Items', fr:'Objets', href:'#/items' },
    { id:'cards', group:'General Topics', en:'Cards', fr:'Cartes', href:'#/cards' },
    { id:'affixes', group:'General Topics', en:'Affixes / Random Options', fr:'Affixes / Options aléatoires', icon:'item' },
    { id:'monsters', group:'General Topics', en:'Monsters', fr:'Monstres', href:'#/monsters' },
    { id:'world-map', group:'General Topics', en:'World Map', fr:'Carte du monde', href:'#/maps' },
    { id:'sources-links', group:'General Topics', en:'Sources & Useful Links', fr:'Sources et liens utiles', icon:'info' },
    { id:'get-poring', group:'General Topics', en:'Get Poring', fr:'Get Poring' },
    { id:'ro-factory', group:'General Topics', en:'RO Factory', fr:'RO Factory' },

    { id:'elements', group:'Systems & Mechanics', en:'Elements', fr:'Éléments' },
    { id:'monster-sizes', group:'Systems & Mechanics', en:'Monster Sizes', fr:'Tailles des monstres', icon:'monster' },
    { id:'monster-races', group:'Systems & Mechanics', en:'Monster Races', fr:'Races des monstres', icon:'monster' },
    { id:'monster-exclusive-skills', group:'Systems & Mechanics', en:'Monster Skills', fr:'Compétences des monstres' },
    { id:'status-effects', group:'Systems & Mechanics', en:'Status Effects', fr:'Effets de statut' },
    { id:'refinement-system', group:'Systems & Mechanics', en:'Refinement', fr:'Raffinement' },
    { id:'crafting', group:'Systems & Mechanics', en:'Crafting', fr:'Craft' },
    { id:'enchantment', group:'Systems & Mechanics', en:'Enchantment', fr:'Enchantement' },
    { id:'pet-system', group:'Systems & Mechanics', en:'Pet System', fr:'Système de Pet' },
    { id:'mvp-raid', group:'Systems & Mechanics', en:'MVP Raid', fr:'Raid MVP' },
  ];'''

s = s[:start] + new_topics + s[end:]

old_home = '''        <section class=\"classic-topic-box\">
          <h2>${navLabel('Systems & Data','Systèmes & données')}</h2>
          ${homeTopicList('Systems & Data')}
        </section>'''
new_home = '''        <section class=\"classic-topic-box\">
          <h2>${navLabel('Systems & Mechanics','Système et Mechanics')}</h2>
          ${homeTopicList('Systems & Mechanics')}
        </section>'''
if old_home not in s:
    raise SystemExit('Systems & Data home block not found')
s = s.replace(old_home, new_home, 1)

# Validation of exact requested placement/order.
general_start = s.index('  const TOPICS = [')
systems_start = s.index("{ id:'elements', group:'Systems & Mechanics'", general_start)
general = s[general_start:systems_start]
assert general.index("id:'experience'") < general.index("id:'party'") < general.index("id:'guild-system'") < general.index("id:'auto-hunt'")
assert general.index("id:'cards'") < general.index("id:'affixes'") < general.index("id:'monsters'")
assert general.rfind("id:'get-poring'") < general.rfind("id:'ro-factory'")
assert general.rfind("id:'ro-factory'") > general.rfind("id:'sources-links'")
for moved in ['party','guild-system','auto-hunt','affixes','get-poring','ro-factory']:
    assert f"id:'{moved}', group:'Systems & Mechanics'" not in s
assert "en:'Guild', fr:'Guilde'" in s
assert "Systems & Data" not in s[s.index('  const TOPICS = ['):s.index('  const navLabel', s.index('  const TOPICS = ['))]
assert "homeTopicList('Systems & Mechanics')" in s

p.write_text(s, encoding='utf-8')
print('Navigation topics reordered and Systems & Data renamed to Systems & Mechanics.')
