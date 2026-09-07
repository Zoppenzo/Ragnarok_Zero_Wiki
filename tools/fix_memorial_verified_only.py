from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

start = s.index('  function memorialDungeonData() {')
end = s.index('\n  function statusEffectsPage', start)
block = s[start:end]

# Poring Village: minimum level only, daily CD wording, no blue pillars, no potion rewards.
block = block.replace("level: 'Base Lv. 30–60',", "level: 'Base Lv. 30+',")
block = block.replace(
    "navLabel('Base Level 30 to 60.','Base Level 30 à 60.'),",
    "navLabel('Base Level 30 or higher.','Base Level 30 ou plus.'),"
)
block = block.replace(
    "navLabel('One completion per day; the restriction resets at 04:00.','Une complétion par jour ; la restriction se réinitialise à 04:00.')",
    "navLabel('CD: once per day.','CD : 1 fois par jour.')"
)
block = block.replace(
    "objective: navLabel('Clear three waves of Porings. Each wave ends with a boss, and the final clear opens the treasure reward.','Élimine trois vagues de Porings. Chaque vague se termine par un boss et la fin de l’instance ouvre la récompense du coffre.'),",
    "objective: navLabel('Clear the three waves of Porings and defeat the bosses.','Élimine les trois vagues de Porings et bats les boss.'),"
)
block = block.replace(
    "          navLabel('Enter the village and clear the first group of fortified Porings.','Entre dans le village et élimine le premier groupe de Porings renforcés.'),\n          navLabel('Use the blue pillars when useful: they transform the character and temporarily increase ATK.','Utilise les piliers bleus quand c’est utile : ils transforment le personnage et augmentent temporairement l’ATK.'),\n          navLabel('Defeat the boss of each wave and continue until the third boss is defeated.','Bats le boss de chaque vague et continue jusqu’à la défaite du troisième boss.'),\n          navLabel('Claim the treasure chest and the daily Jello Fragment reward.','Récupère le coffre et la récompense quotidienne en Jello Fragment.')",
    "          navLabel('Enter the instance and clear the first wave.','Entre dans l’instance et élimine la première vague.'),\n          navLabel('Continue through the following waves.','Continue avec les vagues suivantes.'),\n          navLabel('Defeat the boss at the end of the final wave.','Bats le boss à la fin de la dernière vague.'),\n          navLabel('Leave the instance, then destroy the dungeon to receive the rewards.','Sors de l’instance, puis détruis le donjon pour recevoir les récompenses.')"
)
block = block.replace(
    "rewardIntro: navLabel('The completion chest can contain consumables, lower headgear and materials used by the Memorial Dungeon crafting chain.','Le coffre de fin peut contenir des consommables, des lower headgear et des matériaux utilisés dans la chaîne de craft des Mémorial Donjons.'),",
    "rewardIntro: navLabel('Rewards include lower headgear, Jello Fragments and Memorial Dungeon crafting materials.','Les récompenses comprennent des lower headgear, des Jello Fragments et des matériaux de craft des Mémorial Donjons.'),"
)
block = re.sub(
    r"\n\s*\{title:navLabel\('Consumables','Consommables'\), rows:\[.*?\n\s*\]\},",
    "",
    block,
    count=1,
    flags=re.S,
)

# Remove the entire Mechanics section/data for Memorial Dungeons.
block = re.sub(r"\n\s*mechanics:\s*\[.*?\n\s*\],", "", block, flags=re.S)
block = block.replace(
    "\n      <h2 id=\"mechanics\">${navLabel('Dungeon mechanics','Mécaniques du donjon')}</h2>\n      <ul>${(d.mechanics || []).map(x=>`<li>${esc(x)}</li>`).join('')}</ul>\n",
    "\n"
)

# Remove Base/Job EXP from Memorial monster data and table for now.
block = re.sub(r",baseExp:'[^']*',jobExp:'[^']*'", "", block)
old_rows = """    const monsterRows = (d.monsters || []).map(m=>`<tr>\n      <th>${memorialDbLink('monsters',m.name)}</th><td>${esc(m.level)}</td><td>${esc(m.hp)}</td><td>${esc(m.def)}</td><td>${esc(m.mdef)}</td>\n      <td>${esc(m.class)}</td><td>${esc(m.race)}</td><td>${esc(m.element)}</td><td>${esc(m.size)}</td><td>${esc(m.baseExp)}</td><td>${esc(m.jobExp)}</td>\n    </tr>`).join('');"""
new_rows = """    const monsterRows = (d.monsters || []).map(m=>`<tr>\n      <th>${memorialDbLink('monsters',m.name)}</th><td>${esc(m.level)}</td><td>${esc(m.hp)}</td><td>${esc(m.def)}</td><td>${esc(m.mdef)}</td>\n      <td>${esc(m.class)}</td><td>${esc(m.race)}</td><td>${esc(m.element)}</td><td>${esc(m.size)}</td>\n    </tr>`).join('');"""
assert old_rows in block
block = block.replace(old_rows, new_rows, 1)
block = block.replace(
    "      <p class=\"page-subtitle\">${navLabel('Monster names are internal database links and will open their full sheets when the Monster Database is populated.','Les noms des monstres sont déjà des liens internes vers la database et ouvriront leur fiche complète lorsque la Database Monstre sera remplie.')}</p>\n",
    ""
)
block = block.replace(
    "<th>${navLabel('Monster','Monstre')}</th><th>Lv.</th><th>HP</th><th>DEF</th><th>MDEF</th><th>${navLabel('Class','Classe')}</th><th>${navLabel('Race','Race')}</th><th>${navLabel('Element','Élément')}</th><th>${navLabel('Size','Taille')}</th><th>Base EXP</th><th>Job EXP</th>",
    "<th>${navLabel('Monster','Monstre')}</th><th>Lv.</th><th>HP</th><th>DEF</th><th>MDEF</th><th>${navLabel('Class','Classe')}</th><th>${navLabel('Race','Race')}</th><th>${navLabel('Element','Élément')}</th><th>${navLabel('Size','Taille')}</th>",
    1,
)

# Remove unconfirmed bonus-chest wording from Prontera Culvert.
block = block.replace(
    "objective: navLabel('Destroy the Ancient Thief Bug Eggs to make Ancient Golden Thief Bug appear. Before killing the boss, clear the eggs around it to enable the bonus chest.','Détruis les Ancient Thief Bug Eggs pour faire apparaître Ancient Golden Thief Bug. Avant de tuer le boss, élimine les œufs autour de lui afin d’activer le coffre bonus.'),",
    "objective: navLabel('Destroy the Ancient Thief Bug Eggs to make Ancient Golden Thief Bug appear, then defeat the boss.','Détruis les Ancient Thief Bug Eggs pour faire apparaître Ancient Golden Thief Bug, puis bats le boss.'),"
)
block = block.replace(
    "          navLabel('Enter the culvert and clear the Sewer Thief Bugs and Sewer Giant Thief Bugs.','Entre dans les égouts et élimine les Sewer Thief Bugs et Sewer Giant Thief Bugs.'),\n          navLabel('Destroy all Ancient Thief Bug Eggs in the first phase.','Détruis tous les Ancient Thief Bug Eggs pendant la première phase.'),\n          navLabel('Ancient Golden Thief Bug appears after the egg-clearing condition is completed.','Ancient Golden Thief Bug apparaît une fois la condition de destruction des œufs remplie.'),\n          navLabel('Before finishing the boss, destroy the eggs around it to satisfy the bonus-chest condition.','Avant d’achever le boss, détruis les œufs autour de lui pour remplir la condition du coffre bonus.'),\n          navLabel('Defeat Ancient Golden Thief Bug and collect the normal chest plus the bonus chest when its condition was completed.','Bats Ancient Golden Thief Bug puis récupère le coffre normal ainsi que le coffre bonus si sa condition a été remplie.')",
    "          navLabel('Enter the culvert and progress through the instance.','Entre dans les égouts et progresse dans l’instance.'),\n          navLabel('Destroy the Ancient Thief Bug Eggs until Ancient Golden Thief Bug appears.','Détruis les Ancient Thief Bug Eggs jusqu’à l’apparition de Ancient Golden Thief Bug.'),\n          navLabel('Defeat Ancient Golden Thief Bug.','Bats Ancient Golden Thief Bug.'),\n          navLabel('Leave the instance, then destroy the dungeon to receive the rewards.','Sors de l’instance, puis détruis le donjon pour recevoir les récompenses.')"
)

# Use the user-confirmed instance-destruction reward flow for Orc's Memory too.
block = block.replace(
    "          navLabel('Defeat Fallen Orc Hero and claim the completion chest.','Bats Fallen Orc Hero puis récupère le coffre de fin.')",
    "          navLabel('Defeat Fallen Orc Hero.','Bats Fallen Orc Hero.'),\n          navLabel('Leave the instance, then destroy the dungeon to receive the rewards.','Sors de l’instance, puis détruis le donjon pour recevoir les récompenses.')"
)

# Make /navi commands actual click-to-copy controls using the wiki's existing navi-copy system.
helper = """\n  function memorialAccessHtml(access) {\n    const text = String(access || '');\n    const match = text.match(/\\/navi\\s+[A-Za-z0-9_]+\\s+\\d+\\/\\d+/i);\n    if (!match) return esc(text);\n    const command = match[0];\n    const at = text.indexOf(command);\n    return esc(text.slice(0, at)) + `<code>${esc(command)}</code>` + esc(text.slice(at + command.length));\n  }\n"""
marker = "\n  function memorialDungeonDetail(id) {"
assert marker in block
if 'function memorialAccessHtml(access)' not in block:
    block = block.replace(marker, helper + marker, 1)
block = block.replace(
    "<div><strong>${navLabel('Access','Accès')}</strong><p>${esc(d.access)}</p></div>",
    "<div><strong>${navLabel('Access','Accès')}</strong><p>${memorialAccessHtml(d.access)}</p></div>",
    1,
)

# Validation of the requested cleanup within Memorial Dungeon code only.
for banned in [
    'Base Lv. 30–60', 'Base Level 30 to 60', 'One completion per day', 'Une complétion par jour',
    'blue pillars', 'piliers bleus', "title:navLabel('Consumables','Consommables')",
    '[Not For Sale] Red Potion', '[Not For Sale] Blue Potion', 'Dungeon mechanics', 'Mécaniques du donjon',
    'Monster names are internal database links', 'Les noms des monstres sont déjà des liens internes',
    'bonus chest', 'coffre bonus', '<th>Base EXP</th>', '<th>Job EXP</th>', 'm.baseExp', 'm.jobExp'
]:
    assert banned not in block, banned
assert "level: 'Base Lv. 30+'," in block
assert "navLabel('CD: once per day.','CD : 1 fois par jour.')" in block
assert "destroy the dungeon to receive the rewards" in block
assert 'function memorialAccessHtml(access)' in block
assert '${memorialAccessHtml(d.access)}' in block

s = s[:start] + block + s[end:]
p.write_text(s, encoding='utf-8')
