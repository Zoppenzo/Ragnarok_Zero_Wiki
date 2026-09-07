from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Correct current/live NPC layout and reset cost.
s=s.replace(
"<tr><th>Subjugation Team Enchant</th><td><code>/navi prt_in 135/35</code></td><td>${navLabel('Subjugation Team equipment and the base Job Essence pool.','Équipement Subjugation Team et pool de Job Essence des classes de base.')}</td></tr>\n                <tr><th>Expedition Corps Enchant</th><td><code>/navi prt_in 135/28</code></td><td>${navLabel('Expedition Corps equipment and access to the 2nd Job Essence pool.','Équipement Expedition Corps et accès au pool 2nd Job Essence.')}</td></tr>",
"<tr><th>Subjugation Team Enchant</th><td><code>/navi prt_fild05 251/193</code></td><td>${navLabel('Grade IV Subjugation equipment. This is the Memorial Dungeon gear tier used by the current Base/Job 60 progression.','Équipement Subjugation Grade IV. C’est le rang Memorial Dungeon utilisé dans la progression Base/Job 60 actuelle.')}</td></tr>\n                <tr><th>1st Job Enchant Employee</th><td><code>/navi prt_in 135/35</code></td><td>${navLabel('Higher-rank workshop employee for the 1st Job Essence pool.','Employé de l’atelier des rangs supérieurs pour le pool 1st Job Essence.')}</td></tr>\n                <tr><th>2nd Job Enchant Employee</th><td><code>/navi prt_in 135/28</code></td><td>${navLabel('Higher-rank workshop employee for the 2nd Job Essence pool.','Employé de l’atelier des rangs supérieurs pour le pool 2nd Job Essence.')}</td></tr>",
1)

s=s.replace(
"<tr><td>${navLabel('Zeny reset','Reset en zeny')}</td><td>—</td><td>${risk('warn','70% without destruction','70 % sans destruction')}</td><td>${risk('danger','30% destruction','30 % de destruction')}</td></tr>",
"<tr><td>${navLabel('Zeny reset','Reset en zeny')}</td><td>100 000 zeny</td><td>${risk('warn','70% without destruction','70 % sans destruction')}</td><td>${risk('danger','30% destruction','30 % de destruction')}</td></tr>",
1)

old_note="""            <div class=\"enchant-detail-note\">${navLabel(
              'The zeny amount for the risky reset is intentionally left blank here until it is checked directly in the current client. The destruction rule is kept separate so the guide does not mix the cost with the risk.',
              'Le montant en zeny du reset risqué est volontairement laissé vide ici jusqu’à lecture directe dans le client actuel. La règle de destruction reste affichée séparément pour ne pas mélanger le coût et le risque.'
            )}</div>
"""
assert old_note in s
s=s.replace(old_note,'',1)

# Add clear live-scope notice after the quick decision table.
marker="""            <div class=\"enchant-detail-note\">${navLabel(
              'Subjugation uses the base-archetype Job Essence pool. Knight, Blacksmith, Assassin, Wizard, Priest, Hunter, Crusader, Alchemist, Rogue, Sage, Monk and Bard & Dancer belong to the 2nd Job pool.',
              'Subjugation utilise le pool de Job Essence des classes de base. Knight, Blacksmith, Assassin, Wizard, Priest, Hunter, Crusader, Alchemist, Rogue, Sage, Monk et Bard & Dancer appartiennent au pool 2nd Job.'
            )}</div>
"""
assert marker in s
replacement=marker+"""            <div class=\"notice info\"><svg class=\"notice-icon\"><use href=\"#i-info\"></use></svg><div><strong>${navLabel('Current 60/60 progression','Progression actuelle 60/60')}:</strong> ${navLabel('Subjugation is the current Memorial Dungeon equipment tier. The documented 2nd Job Essence route starts with +9 Expedition armor or a higher rank, so Knight / Blacksmith / Assassin / Wizard / Priest / Hunter / Crusader / Alchemist / Rogue / Sage / Monk / Bard & Dancer Essences are not part of the current Subjugation-only enchant route.','Subjugation est le rang Memorial Dungeon de la progression actuelle. La route documentée des 2nd Job Essence commence avec une armure Expedition +9 ou un rang supérieur : les Essences Knight / Blacksmith / Assassin / Wizard / Priest / Hunter / Crusader / Alchemist / Rogue / Sage / Monk / Bard & Dancer ne font donc pas partie de la route d’enchantement Subjugation actuelle.')}</div></div>
"""
s=s.replace(marker,replacement,1)

# Make the 2nd Job quick-row explicit about Base 70+ progression.
s=s.replace(
"<td>${navLabel('Compatible +9 Expedition / Dispatching / Conqueror armor-type equipment.','Équipement compatible Expedition / Dispatching / Conqueror de type armure à +9.')}</td>",
"<td>${navLabel('Compatible +9 Expedition / Dispatching / Conqueror armor-type equipment. Expedition begins with the Base 70 progression.','Équipement compatible Expedition / Dispatching / Conqueror de type armure à +9. Expedition commence avec la progression Base 70.')}</td>",
1)

# Rewrite Knight example so availability is impossible to misunderstand.
old="""            <h3 id=\"md-knight\">${navLabel(\"Example: how to roll Knight's Essence\",\"Exemple : comment obtenir Knight's Essence\")}</h3>
            <div class=\"panel\"><div class=\"panel-body\">
              <ol class=\"enchant-steps\">
"""
assert old in s
new="""            <h3 id=\"md-knight\">${navLabel(\"Example: how to roll Knight's Essence\",\"Exemple : comment obtenir Knight's Essence\")}</h3>
            <div class=\"panel\"><div class=\"panel-body\">
              <p><strong>${navLabel('Current status:','Statut actuel :')}</strong> ${navLabel(\"Knight's Essence belongs to the 2nd Job Essence route. That route requires Expedition-or-higher +9 armor; it is not available through the current Subjugation-only 60/60 progression.\",\"Knight's Essence appartient à la route 2nd Job Essence. Cette route demande une armure Expedition ou supérieure à +9 ; elle n’est pas disponible via la progression actuelle 60/60 limitée à Subjugation.\")}</p>
              <p>${navLabel('When the Expedition tier is available, the documented conditions are:','Lorsque le rang Expedition est disponible, les conditions documentées sont :')}</p>
              <ol class=\"enchant-steps\">
"""
s=s.replace(old,new,1)

# Use exact current English item names where known in the rank table.
s=s.replace("${itemLink('Subjugation Armor')} / ${itemLink('Subjugation Robe')}","${itemLink(\"Subjugation Team's Armor\")}",1)
s=s.replace("${itemLink('Expedition Armor')} / ${itemLink('Expedition Robe')}","${itemLink(\"Expedition's Armor\")} / ${itemLink(\"Expedition's Robe\")}",1)

# Validation.
for x in [
    '/navi prt_fild05 251/193',
    '/navi prt_in 135/35',
    '/navi prt_in 135/28',
    '100 000 zeny</td><td>${risk(\'warn\',\'70% without destruction\'',
    'Progression actuelle 60/60',
    'Expedition commence avec la progression Base 70',
    'elle n’est pas disponible via la progression actuelle 60/60 limitée à Subjugation',
    "Subjugation Team's Armor",
    "Expedition's Armor"
]:
    assert x in s, x

assert 'Le montant en zeny du reset risqué est volontairement laissé vide' not in s

p.write_text(s,encoding='utf-8')
