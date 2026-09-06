from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# 1) User-facing French labels: plural forms.
s = s.replace('Système et mécanique', 'Systèmes et mécaniques')
s = s.replace('Compétence et Cast Time', 'Compétences et Cast Time')

# 2) Criatura Academy is also a database/reference source, not only a guide.
s = s.replace(
    "[navLabel('Guide','Guide'), 'Criatura Academy', 'https://old.criatura-academy.com/']",
    "[navLabel('Guide / Database','Guide / Base de données'), 'Criatura Academy', 'https://old.criatura-academy.com/']"
)

# 3) Expand Craft with Alchemist Potion Creation / Prepare Potion.
old_toc = "${toc([{id:'overview',label:navLabel('Overview','Aperçu')},{id:'current-systems',label:navLabel('Current systems','Systèmes actuels')},{id:'verification',label:navLabel('Recipe verification','Vérification des recettes')}])}"
new_toc = "${toc([{id:'overview',label:navLabel('Overview','Aperçu')},{id:'current-systems',label:navLabel('Current systems','Systèmes actuels')},{id:'potion-creation',label:'Potion Creation'},{id:'verification',label:navLabel('Recipe verification','Vérification des recettes')}])}"
if old_toc not in s:
    raise SystemExit('Craft TOC marker not found')
s = s.replace(old_toc, new_toc, 1)

old_feature = """        <div><strong>Blacksmith Forging</strong><p>${navLabel('Blacksmith is now a playable second class. Forging recipes and Global-specific weapon results are documented separately from generic Renewal/iRO data.','Blacksmith est désormais une seconde classe jouable. Les recettes de forge et résultats propres à Global sont documentés séparément des données génériques Renewal/iRO.')}</p></div>
        <div><strong>${navLabel('Quest / system recipes','Recettes de quêtes / systèmes')}</strong>"""
new_feature = """        <div><strong>Blacksmith Forging</strong><p>${navLabel('Blacksmith is now a playable second class. Forging recipes and Global-specific weapon results are documented separately from generic Renewal/iRO data.','Blacksmith est désormais une seconde classe jouable. Les recettes de forge et résultats propres à Global sont documentés séparément des données génériques Renewal/iRO.')}</p></div>
        <div><strong>Potion Creation</strong><p>${navLabel('Alchemist crafting through Prepare Potion. The skill consumes a Mortar Bowl and uses the manual and ingredients required by the selected potion or chemical item.','Craft Alchemist via Prepare Potion. Le skill consomme un Mortar Bowl et utilise le manuel ainsi que les ingrédients requis par la potion ou l’objet chimique choisi.')}</p></div>
        <div><strong>${navLabel('Quest / system recipes','Recettes de quêtes / systèmes')}</strong>"""
if old_feature not in s:
    raise SystemExit('Craft feature marker not found')
s = s.replace(old_feature, new_feature, 1)

verification_marker = """      <h2 id=\"verification\">${navLabel('Recipe verification','Vérification des recettes')}</h2>"""
potion_section = """      <h2 id=\"potion-creation\">Potion Creation</h2>
      <p>${navLabel(
        'Alchemist uses the Prepare Potion skill to brew potions and chemical items. On the current Ragnarok Zero: Global skill tree, Prepare Potion has 10 levels and requires Potion Research Lv.5.',
        'L’Alchemist utilise le skill Prepare Potion pour fabriquer des potions et des objets chimiques. Sur l’arbre actuel de Ragnarok Zero: Global, Prepare Potion possède 10 niveaux et demande Potion Research Lv.5.'
      )}</p>
      <div class=\"table-wrap\"><table>
        <thead><tr><th>${navLabel('Skill / Requirement','Skill / Prérequis')}</th><th>${navLabel('Current Global information','Information Global actuelle')}</th></tr></thead>
        <tbody>
          <tr><th>Potion Research</th><td>${navLabel('Passive, Max Lv.10. Improves potion effectiveness and contributes to potion crafting.','Passif, Max Lv.10. Améliore l’efficacité des potions et participe au craft de potions.')}</td></tr>
          <tr><th>Prepare Potion</th><td>${navLabel('Max Lv.10 · Requires Potion Research Lv.5 · 5 SP per use.','Max Lv.10 · Requiert Potion Research Lv.5 · 5 SP par utilisation.')}</td></tr>
          <tr><th>Mortar Bowl</th><td>${navLabel('1 Mortar Bowl is consumed when Prepare Potion is used.','1 Mortar Bowl est consommé à l’utilisation de Prepare Potion.')}</td></tr>
          <tr><th>${navLabel('Potion manual','Manuel de potion')}</th><td>${navLabel('The corresponding manual is required for the potion or chemical item being crafted.','Le manuel correspondant est requis selon la potion ou l’objet chimique fabriqué.')}</td></tr>
        </tbody>
      </table></div>
      <div class=\"notice info-notice\"><svg class=\"notice-icon\"><use href=\"#i-info\"></use></svg><div>${navLabel(
        'The exact brewing success formula is still flagged as unresolved by the current Global data reference, so the wiki does not present one formula as definitive yet.',
        'La formule exacte de réussite du brewing reste indiquée comme non résolue par la référence Global actuelle ; le wiki ne présente donc pas encore une formule unique comme définitive.'
      )}</div></div>
      <div class=\"related-list\">
        <a href=\"https://roz.prontera.info/skills/planner?class=creator\" target=\"_blank\" rel=\"noopener\">Prontera.info — Alchemist / Prepare Potion</a>
        <a href=\"https://roz.prontera.info/mechanics\" target=\"_blank\" rel=\"noopener\">Prontera.info — Brewing formula data</a>
        <a href=\"https://midgardhub.com/tools/brewing\" target=\"_blank\" rel=\"noopener\">MidgardHub — Brewing Calculator</a>
      </div>

"""
if verification_marker not in s:
    raise SystemExit('Craft verification marker not found')
s = s.replace(verification_marker, potion_section + verification_marker, 1)

# Add Criatura to Craft sources too.
s = s.replace(
    "['MidgardHub — current Global guides/database','https://midgardhub.com/']\n      ])}`;",
    "['MidgardHub — current Global guides/database','https://midgardhub.com/'],\n        ['Criatura Academy — Ragnarok Zero reference database','https://old.criatura-academy.com/']\n      ])}`;",
    1
)

# 4) Replace the old Memorial Dungeon stub with a list + one detail page per current Memorial Dungeon.
start = s.index('  function memorialDungeonDatabasePage() {')
end = s.index('\n  function ', start + len('  function memorialDungeonDatabasePage() {'))

memorial_code = r'''  function memorialDungeonData() {
    return {
      'poring-village': {
        name: 'Poring Village',
        subtitle: navLabel('Early Memorial Dungeon','Mémorial Donjon de début de progression'),
        access: navLabel('One map west of Prontera. Criatura Academy identifies Emily as the entry NPC.','Une map à l’ouest de Prontera. Criatura Academy indique Emily comme NPC d’entrée.'),
        level: 'Base Lv. 30–60',
        objective: navLabel('Use the blue pillars during the run for a temporary transformation and ATK increase, then clear the Poring encounters and bosses.','Utilise les piliers bleus pendant le run pour obtenir une transformation temporaire et une hausse d’ATK, puis élimine les Porings et les boss.'),
        mechanics: [
          navLabel('Criatura documents party entry and a once-per-day lockout resetting at 04:00.','Criatura documente une entrée en party et une limite d’une entrée par jour, réinitialisée à 04:00.'),
          navLabel('Blue pillars transform the character and temporarily increase ATK.','Les piliers bleus transforment le personnage et augmentent temporairement l’ATK.'),
          navLabel('More party members can increase the amount of treasure-chest rewards in the Korean Zero reference data.','Dans les données de référence Korean Zero, davantage de membres dans la party peuvent augmenter la quantité de récompenses du coffre.')
        ],
        monsters: [
          ['Fortified Poring','34','1,023','10 / 12','Formless','Earth Lv.1','Small','369 / 291'],
          ['Fortified Marin','33','960','10 / 10','Formless','Water Lv.1','Small','358 / 279'],
          ['Fortified Poporing','36','1,167','10 / 12','Formless','Wind Lv.1','Small','384 / 309'],
          ['Fortified Drops','35','1,095','10 / 10','Formless','Fire Lv.1','Small','377 / 300'],
          ['Amering','35','72,810','10 / 10','Formless','Poison Lv.1','Large','6,375 / 5,524'],
          ['Goldring','35','72,118','10 / 10','Formless','Holy Lv.1','Large','6,327 / 5,565'],
          ['King Poring','35','140,000','20 / 20','Formless','Neutral Lv.1','Large','9,580 / 8,288']
        ],
        rewards: [
          navLabel('Treasure chest: non-sale Red, Blue, Orange, Yellow, White and Green Potions.','Coffre : Red, Blue, Orange, Yellow, White et Green Potions non revendables.'),
          'Poring Village Leek',
          'Poring Village Carrot',
          navLabel('Daily Jello Fragment reward: Poring (Mon), Poporing (Tue), Drops (Wed), Deviling (Thu), Angeling (Fri), Jello Fragment Box (Sat/Sun).','Récompense Jello Fragment selon le jour : Poring (lun.), Poporing (mar.), Drops (mer.), Deviling (jeu.), Angeling (ven.), Jello Fragment Box (sam./dim.).')
        ],
        sources: [
          ['Criatura Academy — Poring Village','https://old.criatura-academy.com/memorial-dungeons/poring-village'],
          ['MidgardHub — Memorial Dungeons','https://midgardhub.com/guides/memorial-dungeons']
        ]
      },
      'orcs-memory': {
        name: "Orc's Memory",
        subtitle: navLabel('Memorial Dungeon — Orc Village','Mémorial Donjon — Orc Village'),
        access: navLabel('Located in Orc Village, outside Orc Dungeon. Criatura Academy identifies the Scientist NPC as the instance starter.','Situé à Orc Village, à l’extérieur d’Orc Dungeon. Criatura Academy indique le NPC Scientist comme point de départ de l’instance.'),
        level: 'Base Lv. 59+',
        objective: navLabel("Progress through the Orc encounters and defeat Fallen Orc Hero. Destroy or control the Shaman's Flowers because they strengthen the final boss.","Progresse à travers les groupes d’Orcs et bats Fallen Orc Hero. Détruis ou contrôle les Shaman's Flowers car elles renforcent le boss final."),
        mechanics: [
          navLabel("Shaman's Flowers buff the final boss and should not be ignored.","Les Shaman's Flowers renforcent le boss final et ne doivent pas être ignorées."),
          navLabel('Grade IV Memorial Dungeon equipment is part of the normal-mode reward pool in the Korean Zero reference data.','L’équipement Mémorial Donjon Grade IV fait partie des récompenses du mode normal dans les données Korean Zero de référence.'),
          navLabel('Prontera.info places Orc Memory in the Global September 3 progression wave.','Prontera.info place Orc Memory dans la vague de progression Global du 3 septembre.')
        ],
        monsters: [
          ['Orc Skeleton','60','4,458','82 / 10','Undead','Undead Lv.1','Medium','627 / 562'],
          ['Orc Zombie','60','4,475','71 / 5','Brute','Undead Lv.1','Medium','649 / 600'],
          ['Anapholes','95','6,617','7 / 10','Insect','Wind Lv.3','Small','? / ?'],
          ["Shaman's Flower",'98','5','160 / 99','Plant','Earth Lv.1','Medium','0 / 0'],
          ['Fallen Orc Hero','70','2,110,562','197 / 70','Demi-human','Earth Lv.2','Large','166,639 / 118,717']
        ],
        rewards: [
          navLabel('Normal: Shimmering Crystal ×1–3.','Normal : Shimmering Crystal ×1–3.'),
          navLabel('Normal: Subjugation Sash [1] and Subjugation Armor [1].','Normal : Subjugation Sash [1] et Subjugation Armor [1].'),
          navLabel('Hard reference pool: Shimmering Crystal ×6–10, Cursed Emerald ×0–3, Mithril Ore ×1–4, Elunium/Oridecon and rough ores, plus elemental materials.','Pool de référence Hard : Shimmering Crystal ×6–10, Cursed Emerald ×0–3, Mithril Ore ×1–4, Elunium/Oridecon et minerais bruts, plus matériaux élémentaires.')
        ],
        sources: [
          ["Criatura Academy — Orc's Memory",'https://old.criatura-academy.com/memorial-dungeons/orcs-memory/'],
          ['Prontera.info — Global release tracker','https://roz.prontera.info/release'],
          ['Official GNJOY — September 3 update','https://roz.mygnjoy.com/en/news/update/92']
        ]
      },
      'prontera-culvert': {
        name: 'Prontera Culvert',
        subtitle: navLabel('Memorial Dungeon — Prontera field','Mémorial Donjon — champ de Prontera'),
        access: navLabel('Criatura Academy places the entrance at prt_fild05 264, 208, one map west of Prontera, through the Culvert Manager while in a party.','Criatura Academy place l’entrée à prt_fild05 264, 208, une map à l’ouest de Prontera, via le Culvert Manager en étant dans une party.'),
        level: 'Base Lv. 59+',
        objective: navLabel('Destroy the Ancient Thief Bug Eggs to spawn the boss, then defeat Ancient Golden Thief Bug. Clearing the eggs around the boss before killing it enables the bonus chest in the Korean Zero reference flow.','Détruis les Ancient Thief Bug Eggs pour faire apparaître le boss, puis bats Ancient Golden Thief Bug. Dans le déroulement Korean Zero de référence, éliminer les œufs autour du boss avant de le tuer permet d’obtenir le coffre bonus.'),
        mechanics: [
          navLabel('The first egg-clearing phase triggers the boss spawn.','La première phase de destruction des œufs déclenche l’apparition du boss.'),
          navLabel('Clear the eggs around the boss before finishing Ancient Golden Thief Bug for the bonus-chest condition documented by Criatura.','Élimine les œufs autour du boss avant de terminer Ancient Golden Thief Bug pour remplir la condition du coffre bonus documentée par Criatura.'),
          navLabel('Prontera.info places Prontera Culvert in the Global September 3 progression wave.','Prontera.info place Prontera Culvert dans la vague de progression Global du 3 septembre.')
        ],
        monsters: [
          ['Sewer Giant Thief Bug','60','3,330','40 / 20','Formless','Shadow Lv.1','Medium','0 / 0'],
          ['Sewer Thief Bug','60','200','24 / 3','Insect','Neutral Lv.3','Small','0 / 0'],
          ['Ancient Thief Bug Egg','60','10','64 / 10','Insect','Shadow Lv.1','Small','0 / 0'],
          ['Ancient Golden Thief Bug','60','1,200,000','159 / 81','Insect','Fire Lv.1','Large','75,000 / 63,000']
        ],
        rewards: [
          navLabel('Normal: Shimmering Crystal ×1–3.','Normal : Shimmering Crystal ×1–3.'),
          navLabel('Normal: Subjugation Ring [1] and Subjugation Boots [1].','Normal : Subjugation Ring [1] et Subjugation Boots [1].'),
          navLabel('Hard reference pool: Shimmering Crystal ×6–10, Shiny Opal ×0–3, Mithril Ore ×1–4, Elunium/Oridecon and rough ores, plus elemental materials.','Pool de référence Hard : Shimmering Crystal ×6–10, Shiny Opal ×0–3, Mithril Ore ×1–4, Elunium/Oridecon et minerais bruts, plus matériaux élémentaires.')
        ],
        sources: [
          ['Criatura Academy — Prontera Culvert','https://old.criatura-academy.com/memorial-dungeons/prontera-culvert/'],
          ['Prontera.info — Global release tracker','https://roz.prontera.info/release'],
          ['Official GNJOY — September 3 update','https://roz.mygnjoy.com/en/news/update/92']
        ]
      }
    };
  }

  function memorialDungeonDatabasePage() {
    const data = memorialDungeonData();
    const cards = Object.entries(data).map(([id,d])=>`<a class="panel" href="#/memorial-dungeons/${id}" style="display:block;color:inherit;text-decoration:none;overflow:hidden">
      <div class="panel-heading">${miniIcon('memorial')}${esc(d.name)}</div>
      <div class="panel-body"><strong>${esc(d.level)}</strong><p>${esc(d.subtitle)}</p><span class="table-link">${navLabel('Open dungeon page →','Ouvrir la page du donjon →')}</span></div>
    </a>`).join('');
    return `${breadcrumbs([{label:navLabel('Memorial Dungeons','Mémorial Donjons')}])}
      <div class="article-heading"><h1>${icon('memorial')}${navLabel('Memorial Dungeons','Mémorial Donjons')}</h1><div class="page-subtitle">${t('fromWiki')}</div></div>
      <p class="article-lead">${navLabel('Each current Memorial Dungeon now has its own page with access information, mechanics, monsters and reward references.','Chaque Mémorial Donjon actuel possède désormais sa propre page avec les informations d’accès, les mécaniques, les monstres et les références de récompenses.')}</p>
      <div class="notice info-notice"><svg class="notice-icon"><use href="#i-info"></use></svg><div><strong>${navLabel('Source scope','Périmètre des sources')}</strong><br>${navLabel('Global release status is cross-checked with current Global sources. Detailed historical Zero values use Criatura Academy, a Korean Ragnarok Zero reference database, and remain source-qualified where Global has not published the exact value.','Le statut de sortie Global est recoupé avec les sources Global actuelles. Les valeurs détaillées historiques de Zero utilisent Criatura Academy, une base de référence du Ragnarok Zero coréen, et restent attribuées à cette source lorsque Global n’a pas publié la valeur exacte.')}</div></div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px">${cards}</div>
      ${officialSources([
        ['Official GNJOY — September 3 update','https://roz.mygnjoy.com/en/news/update/92'],
        ['Prontera.info — Global release tracker','https://roz.prontera.info/release'],
        ['Criatura Academy — Memorial Dungeons database','https://old.criatura-academy.com/'],
        ['MidgardHub — Memorial Dungeons guide','https://midgardhub.com/guides/memorial-dungeons']
      ])}`;
  }

  function memorialDungeonDetail(id) {
    const d = memorialDungeonData()[id];
    if (!d) return notFound();
    const monsterRows = d.monsters.map(m=>`<tr><th>${esc(m[0])}</th><td>${esc(m[1])}</td><td>${esc(m[2])}</td><td>${esc(m[3])}</td><td>${esc(m[4])}</td><td>${esc(m[5])}</td><td>${esc(m[6])}</td><td>${esc(m[7])}</td></tr>`).join('');
    return `${breadcrumbs([{label:navLabel('Memorial Dungeons','Mémorial Donjons'),href:'#/memorial-dungeons'},{label:d.name}])}
      <div class="article-heading"><h1>${icon('memorial')}${esc(d.name)}</h1><div class="page-subtitle">${esc(d.subtitle)}</div></div>
      <div class="notice info-notice"><svg class="notice-icon"><use href="#i-info"></use></svg><div><strong>${navLabel('Global / Zero source note','Note sur les sources Global / Zero')}</strong><br>${navLabel('The dungeon is documented for the current Global progression; detailed monster/reward numbers below are sourced from Criatura Academy’s Korean Ragnarok Zero database when no exact Global table is publicly available yet.','Le donjon est documenté dans la progression Global actuelle ; les valeurs détaillées des monstres/récompenses ci-dessous proviennent de la base Korean Ragnarok Zero de Criatura Academy lorsqu’aucun tableau Global exact n’est encore publié.')}</div></div>
      ${toc([
        {id:'access',label:navLabel('Access & requirements','Accès et prérequis')},
        {id:'mechanics',label:navLabel('Dungeon mechanics','Mécaniques du donjon')},
        {id:'monsters',label:navLabel('Monsters & boss','Monstres et boss')},
        {id:'rewards',label:navLabel('Rewards','Récompenses')},
        {id:'sources',label:navLabel('Sources','Sources')}
      ])}
      <h2 id="access">${navLabel('Access & requirements','Accès et prérequis')}</h2>
      <div class="table-wrap"><table><tbody>
        <tr><th>${navLabel('Level','Niveau')}</th><td>${esc(d.level)}</td></tr>
        <tr><th>${navLabel('Entrance','Entrée')}</th><td>${esc(d.access)}</td></tr>
        <tr><th>${navLabel('Main objective','Objectif principal')}</th><td>${esc(d.objective)}</td></tr>
      </tbody></table></div>
      <h2 id="mechanics">${navLabel('Dungeon mechanics','Mécaniques du donjon')}</h2>
      <ul>${d.mechanics.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>
      <h2 id="monsters">${navLabel('Monsters & boss','Monstres et boss')}</h2>
      <div class="table-wrap"><table>
        <thead><tr><th>${navLabel('Monster','Monstre')}</th><th>Lv.</th><th>HP</th><th>DEF / MDEF</th><th>${navLabel('Race','Race')}</th><th>${navLabel('Property','Élément')}</th><th>${navLabel('Size','Taille')}</th><th>EXP / JEXP</th></tr></thead>
        <tbody>${monsterRows}</tbody>
      </table></div>
      <h2 id="rewards">${navLabel('Treasure & rewards','Trésor et récompenses')}</h2>
      <ul>${d.rewards.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>
      <h2 id="sources">${navLabel('Sources','Sources')}</h2>
      ${officialSources(d.sources)}
      <div class="related-list"><a href="#/memorial-dungeons">${miniIcon('memorial')}${navLabel('All Memorial Dungeons','Tous les Mémorial Donjons')}</a></div>`;
  }
'''

s = s[:start] + memorial_code + s[end:]

# Route detail pages before the list-only fallback.
route_old = "else if(hash[0]==='memorial-dungeons'&&!hash[1]) html=memorialDungeonDatabasePage();"
route_new = "else if(hash[0]==='memorial-dungeons'&&hash[1]) html=memorialDungeonDetail(hash[1]);\n    else if(hash[0]==='memorial-dungeons'&&!hash[1]) html=memorialDungeonDatabasePage();"
if route_old not in s:
    raise SystemExit('Memorial route marker not found')
s = s.replace(route_old, route_new, 1)

# Add section verification metadata for Potion Creation and Memorial pages.
s = s.replace(
    "'#/wiki/crafting': { overview:'complete', 'current-systems':'partial', verification:'partial' },",
    "'#/wiki/crafting': { overview:'complete', 'current-systems':'partial', 'potion-creation':'complete', verification:'partial' },"
)

# Validation.
assert "Systèmes et mécaniques" in s
assert "Compétences et Cast Time" in s
assert "fr:'Compétence et Cast Time'" not in s
assert "'Criatura Academy', 'https://old.criatura-academy.com/'" in s
assert 'Potion Creation</h2>' in s
assert 'Prepare Potion' in s
assert "function memorialDungeonDetail(id)" in s
assert "#/memorial-dungeons/${id}" in s
assert "hash[0]==='memorial-dungeons'&&hash[1]" in s
for md in ['poring-village','orcs-memory','prontera-culvert']:
    assert f"'{md}':" in s

p.write_text(s, encoding='utf-8')
print('Updated labels, Craft/Potion Creation, Criatura source, and individual Memorial Dungeon pages.')
