from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

start = s.index('  function memorialDungeonData() {')
end = s.index('\n  function memorialDungeonDatabasePage()', start)
block = s[start:end]

repls = {
"access: navLabel('Current Global guide: /navi prt_fild05 146/235. The entrance is one map west of Prontera, at Emily.','Guide Global actuel : /navi prt_fild05 146/235. L’entrée se trouve une map à l’ouest de Prontera, auprès d’Emily.'),":"access: navLabel('/navi prt_fild05 146/235. The entrance is one map west of Prontera, at Emily.','/navi prt_fild05 146/235. L’entrée se trouve une map à l’ouest de Prontera, auprès d’Emily.'),",
"level: navLabel('Base Lv. 30+ · KRO reference: 30–60','Base Lv. 30+ · Référence KRO : 30–60'),":"level: 'Base Lv. 30–60',",
"navLabel('The current Global new-player guide confirms three boss waves and a daily completion reward.','Le guide Global actuel confirme trois vagues avec boss et une récompense quotidienne à la fin.'),":"navLabel('The dungeon is cleared through three boss waves and gives a daily completion reward.','Le donjon se termine après trois vagues avec boss et donne une récompense quotidienne.'),",
"navLabel('KRO/Criatura documents blue pillars that transform the character and temporarily increase ATK.','KRO/Criatura documente des piliers bleus qui transforment le personnage et augmentent temporairement l’ATK.'),":"navLabel('Blue pillars transform the character and temporarily increase ATK.','Les piliers bleus transforment le personnage et augmentent temporairement l’ATK.'),",
"navLabel('KRO/Criatura documents one entry per day with the restriction resetting at 04:00.','KRO/Criatura documente une entrée par jour avec réinitialisation de la restriction à 04:00.')":"navLabel('The entry restriction resets daily at 04:00.','La restriction d’entrée se réinitialise chaque jour à 04:00.')",
"navLabel('Poring Village Green Onion / Leek — translation differs by source.','Poring Village Green Onion / Leek — traduction différente selon la source.'),":"'Poring Village Green Onion / Leek',",
"navLabel('Daily Jello Fragment reward: Poring (Mon), Poporing (Tue), Drops (Wed), Deviling (Thu), Angeling (Fri), Jello Fragment Box (Sat/Sun) — KRO reference.','Récompense Jello Fragment selon le jour : Poring (lun.), Poporing (mar.), Drops (mer.), Deviling (jeu.), Angeling (ven.), Jello Fragment Box (sam./dim.) — référence KRO.')":"navLabel('Daily Jello Fragment reward: Poring (Mon), Poporing (Tue), Drops (Wed), Deviling (Thu), Angeling (Fri), Jello Fragment Box (Sat/Sun).','Récompense Jello Fragment selon le jour : Poring (lun.), Poporing (mar.), Drops (mer.), Deviling (jeu.), Angeling (ven.), Jello Fragment Box (sam./dim.).')",
"access: navLabel('KRO reference: Orc Village, outside Orc Dungeon, through the Scientist NPC. The dungeon is live on Global since the September 3 update.','Référence KRO : Orc Village, à l’extérieur d’Orc Dungeon, via le NPC Scientist. Le donjon est live sur Global depuis la mise à jour du 3 septembre.'),":"access: navLabel('Orc Village, outside Orc Dungeon, through the Scientist NPC.','Orc Village, à l’extérieur d’Orc Dungeon, via le NPC Scientist.'),",
"level: navLabel('KRO reference: Base Lv. 59+','Référence KRO : Base Lv. 59+'),":"level: 'Base Lv. 59+',",
"objective: navLabel(\"Progress through the Orc encounters and defeat Fallen Orc Hero. The KRO guide warns that Shaman's Flowers strengthen the final boss.\",\"Progresse à travers les groupes d’Orcs et bats Fallen Orc Hero. Le guide KRO avertit que les Shaman's Flowers renforcent le boss final.\"),":"objective: navLabel(\"Progress through the Orc encounters and defeat Fallen Orc Hero. Shaman's Flowers strengthen the final boss.\",\"Progresse à travers les groupes d’Orcs et bats Fallen Orc Hero. Les Shaman's Flowers renforcent le boss final.\"),",
"navLabel(\"KRO/Criatura: Shaman's Flowers buff Fallen Orc Hero and should not be ignored.\",\"KRO/Criatura : les Shaman's Flowers renforcent Fallen Orc Hero et ne doivent pas être ignorées.\"),":"navLabel(\"Shaman's Flowers buff Fallen Orc Hero and should not be ignored.\",\"Les Shaman's Flowers renforcent Fallen Orc Hero et ne doivent pas être ignorées.\"),",
"navLabel('KRO/Criatura: Grade IV Memorial Dungeon equipment is part of the normal-mode reward pool.','KRO/Criatura : l’équipement Mémorial Donjon Grade IV fait partie des récompenses du mode normal.'),":"navLabel('Grade IV Memorial Dungeon equipment is part of the normal-mode reward pool.','L’équipement Mémorial Donjon Grade IV fait partie des récompenses du mode normal.')",
"access: navLabel('KRO reference: prt_fild05 264, 208, one map west of Prontera, through the Culvert Manager. The dungeon is live on Global since the September 3 update.','Référence KRO : prt_fild05 264, 208, une map à l’ouest de Prontera, via le Culvert Manager. Le donjon est live sur Global depuis la mise à jour du 3 septembre.'),":"access: navLabel('/navi prt_fild05 264/208. One map west of Prontera, through the Culvert Manager.','/navi prt_fild05 264/208. Une map à l’ouest de Prontera, via le Culvert Manager.'),",
"objective: navLabel('KRO reference: destroy the Ancient Thief Bug Eggs to spawn Ancient Golden Thief Bug; clearing the eggs around the boss before killing it enables the bonus chest.','Référence KRO : détruis les Ancient Thief Bug Eggs pour faire apparaître Ancient Golden Thief Bug ; éliminer les œufs autour du boss avant de le tuer permet d’obtenir le coffre bonus.'),":"objective: navLabel('Destroy the Ancient Thief Bug Eggs to spawn Ancient Golden Thief Bug; clearing the eggs around the boss before killing it enables the bonus chest.','Détruis les Ancient Thief Bug Eggs pour faire apparaître Ancient Golden Thief Bug ; éliminer les œufs autour du boss avant de le tuer permet d’obtenir le coffre bonus.'),",
"navLabel('KRO/Criatura: the first egg-clearing phase triggers the boss spawn.','KRO/Criatura : la première phase de destruction des œufs déclenche l’apparition du boss.'),":"navLabel('The first egg-clearing phase triggers the boss spawn.','La première phase de destruction des œufs déclenche l’apparition du boss.'),",
"navLabel('KRO/Criatura: clear the eggs around the boss before finishing Ancient Golden Thief Bug for the bonus-chest condition.','KRO/Criatura : élimine les œufs autour du boss avant de terminer Ancient Golden Thief Bug pour remplir la condition du coffre bonus.'),":"navLabel('Clear the eggs around the boss before finishing Ancient Golden Thief Bug to unlock the bonus chest.','Élimine les œufs autour du boss avant de terminer Ancient Golden Thief Bug pour débloquer le coffre bonus.'),",
"'Neutral Lv.1 (KRO) / Lv.2 (TWRo)'":"'Neutral'",
"navLabel('KRO Normal: Shimmering Crystal ×1–3.','KRO Normal : Shimmering Crystal ×1–3.')":"navLabel('Normal: Shimmering Crystal ×1–3.','Normal : Shimmering Crystal ×1–3.')",
"navLabel('KRO Normal: Subjugation Sash [1] and Subjugation Armor [1].','KRO Normal : Subjugation Sash [1] et Subjugation Armor [1].')":"navLabel('Normal: Subjugation Sash [1] and Subjugation Armor [1].','Normal : Subjugation Sash [1] et Subjugation Armor [1].')",
"navLabel('KRO Hard reference pool: Shimmering Crystal ×6–10, Cursed Emerald ×0–3, Mithril Ore ×1–4, Elunium/Oridecon and rough ores, plus elemental materials.','Pool KRO Hard : Shimmering Crystal ×6–10, Cursed Emerald ×0–3, Mithril Ore ×1–4, Elunium/Oridecon et minerais bruts, plus matériaux élémentaires.')":"navLabel('Hard: Shimmering Crystal ×6–10, Cursed Emerald ×0–3, Mithril Ore ×1–4, Elunium/Oridecon and rough ores, plus elemental materials.','Hard : Shimmering Crystal ×6–10, Cursed Emerald ×0–3, Mithril Ore ×1–4, Elunium/Oridecon et minerais bruts, plus matériaux élémentaires.')",
"navLabel('KRO Normal: Subjugation Ring [1] and Subjugation Boots [1].','KRO Normal : Subjugation Ring [1] et Subjugation Boots [1].')":"navLabel('Normal: Subjugation Ring [1] and Subjugation Boots [1].','Normal : Subjugation Ring [1] et Subjugation Boots [1].')",
"navLabel('KRO Hard reference pool: Shimmering Crystal ×6–10, Shiny Opal ×0–3, Mithril Ore ×1–4, Elunium/Oridecon and rough ores, plus elemental materials.','Pool KRO Hard : Shimmering Crystal ×6–10, Shiny Opal ×0–3, Mithril Ore ×1–4, Elunium/Oridecon et minerais bruts, plus matériaux élémentaires.')":"navLabel('Hard: Shimmering Crystal ×6–10, Shiny Opal ×0–3, Mithril Ore ×1–4, Elunium/Oridecon and rough ores, plus elemental materials.','Hard : Shimmering Crystal ×6–10, Shiny Opal ×0–3, Mithril Ore ×1–4, Elunium/Oridecon et minerais bruts, plus matériaux élémentaires.')",
"navLabel('Poring Village entrance location — Criatura Academy','Emplacement de l’entrée de Poring Village — Criatura Academy')":"navLabel('Poring Village entrance location','Emplacement de l’entrée de Poring Village')",
"'King Poring — Criatura Academy'":"'King Poring'",
"navLabel(\"Orc's Memory entrance location — Criatura Academy\",\"Emplacement de l’entrée de Orc's Memory — Criatura Academy\")":"navLabel(\"Orc's Memory entrance location\",\"Emplacement de l’entrée de Orc's Memory\")",
"'Fallen Orc Hero — Criatura Academy'":"'Fallen Orc Hero'",
"navLabel('Prontera Culvert entrance location — Criatura Academy','Emplacement de l’entrée de Prontera Culvert — Criatura Academy')":"navLabel('Prontera Culvert entrance location','Emplacement de l’entrée de Prontera Culvert')",
"'Ancient Golden Thief Bug — Criatura Academy'":"'Ancient Golden Thief Bug'",
}
for a,b in repls.items():
    block = block.replace(a,b)

# Remove source-comparison arrays entirely.
block = re.sub(r"\n        crosscheck: \[.*?\n        \],", "", block, flags=re.S)
# Remove update/source meta lines from mechanics lists.
block = re.sub(r"\n\s*navLabel\('Official Global September 3 update confirms the new Memorial Dungeon wave, but does not publish the complete monster/reward table\.',\s*'La mise à jour officielle Global du 3 septembre confirme la nouvelle vague de Mémorial Donjons mais ne publie pas le tableau complet des monstres/récompenses\.'\),?", "", block)

s = s[:start] + block + s[end:]

# Memorial index: guide info only, no source-provenance notice.
s = s.replace(
"<p class=\"article-lead\">${navLabel('Each current Memorial Dungeon now has its own page with access information, mechanics, monsters and reward references.','Chaque Mémorial Donjon actuel possède désormais sa propre page avec les informations d’accès, les mécaniques, les monstres et les références de récompenses.')}</p>\n      <div class=\"notice info-notice\"><svg class=\"notice-icon\"><use href=\"#i-info\"></use></svg><div><strong>${navLabel('Source scope','Périmètre des sources')}</strong><br>${navLabel('Global release status is cross-checked with current Global sources. Detailed historical Zero values use Criatura Academy, a Korean Ragnarok Zero reference database, and remain source-qualified where Global has not published the exact value.','Le statut de sortie Global est recoupé avec les sources Global actuelles. Les valeurs détaillées historiques de Zero utilisent Criatura Academy, une base de référence du Ragnarok Zero coréen, et restent attribuées à cette source lorsque Global n’a pas publié la valeur exacte.')}</div></div>",
"<p class=\"article-lead\">${navLabel('Each Memorial Dungeon has its own page with access information, mechanics, monsters, bosses, images and rewards.','Chaque Mémorial Donjon possède sa propre page avec les informations d’accès, les mécaniques, les monstres, les boss, les images et les récompenses.')}</p>",
1)

# Remove the source cross-check section from each dungeon page.
s = re.sub(r"\n\s*<h2 id=\\?\"source-check\\?\">.*?<h2 id=\\?\"monsters\\?\">", "\n\n      <h2 id=\"monsters\">", s, count=1, flags=re.S)

# Craft pages: no external-version/source provenance in prose; source names remain in Sources only.
s = s.replace(
"${navLabel('Do not use TWROZ/iRO recipe quantities as Global values unless they have been checked against the current Global client or current Global sources.','Ne pas utiliser les quantités de recettes TWROZ/iRO comme valeurs Global tant qu’elles n’ont pas été contrôlées avec le client Global actuel ou des sources Global actuelles.')}",
"${navLabel('Recipe quantities are only published after they have been checked for the current game version.','Les quantités de recettes sont publiées uniquement après vérification sur la version actuelle du jeu.')}")
s = s.replace(
"${navLabel('The exact Global forging recipe table is being separated from older regional RO tables. Recipes will be added here after verification rather than copied from iRO/TWROZ.','Le tableau exact des recettes de forge Global est séparé des anciennes tables régionales RO. Les recettes seront ajoutées ici après vérification au lieu d’être copiées depuis iRO/TWROZ.')}",
"${navLabel('Forging recipes are added here after their materials, quantities and results have been checked for the current game version.','Les recettes de forge sont ajoutées ici après vérification des matériaux, des quantités et des résultats sur la version actuelle du jeu.')}")

# Validation: external site/version names may remain in Sources, but not in Memorial guide data/rendering.
ms = s[s.index('  function memorialDungeonData() {'):s.index('\n  function sourcesLinksPage', s.index('  function memorialDungeonData() {'))]
for banned in ['crosscheck:', 'Source cross-check', 'Croisement des sources', 'KRO/Criatura', 'référence KRO', 'KRO reference', '— Criatura Academy']:
    assert banned not in ms, banned
assert "Neutral Lv.1 (KRO) / Lv.2 (TWRo)" not in ms
assert "function craftingDetailPage(id)" in s

p.write_text(s, encoding='utf-8')
