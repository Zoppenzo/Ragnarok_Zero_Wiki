from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# --- Memorial Dungeon data: add guide images and source cross-checks ---
md_start = s.index('  function memorialDungeonData() {')
md_end = s.index('\n  function memorialDungeonDatabasePage() {', md_start)

memorial_data = r'''  function memorialDungeonData() {
    return {
      'poring-village': {
        name: 'Poring Village',
        subtitle: navLabel('Early Memorial Dungeon','Mémorial Donjon de début de progression'),
        access: navLabel('Current Global guide: /navi prt_fild05 146/235. The entrance is one map west of Prontera, at Emily.','Guide Global actuel : /navi prt_fild05 146/235. L’entrée se trouve une map à l’ouest de Prontera, auprès d’Emily.'),
        level: navLabel('Base Lv. 30+ · KRO reference: 30–60','Base Lv. 30+ · Référence KRO : 30–60'),
        objective: navLabel('Fight through three Poring waves, each ending with a boss, then claim the daily reward.','Affronte trois vagues de Porings, chacune se terminant par un boss, puis récupère la récompense quotidienne.'),
        mechanics: [
          navLabel('The current Global new-player guide confirms three boss waves and a daily completion reward.','Le guide Global actuel confirme trois vagues avec boss et une récompense quotidienne à la fin.'),
          navLabel('KRO/Criatura documents blue pillars that transform the character and temporarily increase ATK.','KRO/Criatura documente des piliers bleus qui transforment le personnage et augmentent temporairement l’ATK.'),
          navLabel('KRO/Criatura documents one entry per day with the restriction resetting at 04:00.','KRO/Criatura documente une entrée par jour avec réinitialisation de la restriction à 04:00.')
        ],
        crosscheck: [
          navLabel('Global guide (MidgardHub/Lymd): entrance shown at prt_fild05 146/235, three boss waves, daily reward.','Guide Global (MidgardHub/Lymd) : entrée indiquée à prt_fild05 146/235, trois vagues de boss et récompense quotidienne.'),
          navLabel('MidgardHub Memorial Dungeons is explicitly TWRo-derived and lists Emily at 145/235. The one-cell coordinate difference is kept in the sources rather than treated as a gameplay contradiction.','La page Mémorial Donjons de MidgardHub est explicitement basée sur TWRo et indique Emily à 145/235. La différence d’une case est conservée dans les sources plutôt que traitée comme une contradiction de gameplay.'),
          navLabel('King Poring element differs between references: Criatura/KRO says Neutral Lv.1; MidgardHub/TWRo says Neutral Lv.2. Global has not been independently confirmed, so the table shows both references.','L’élément de King Poring diffère selon les références : Criatura/KRO indique Neutral Lv.1 ; MidgardHub/TWRo indique Neutral Lv.2. Global n’étant pas encore vérifié indépendamment, le tableau affiche les deux références.'),
          navLabel('Criatura/KRO requires a party; MidgardHub’s TWRo memorial overview calls its four instances solo. Until current Global entry rules are independently verified, this wiki does not promote either regional rule as definitive for Global.','Criatura/KRO demande une party ; la page Mémorial Donjons TWRo de MidgardHub décrit ses quatre instances comme solo. Tant que la règle Global actuelle n’est pas vérifiée indépendamment, le wiki ne présente aucune de ces règles régionales comme définitive pour Global.')
        ],
        images: [
          ['https://d33wubrfki0l68.cloudfront.net/66417fa7576de4232df6a19e65681ca14ca7eec6/ae066/images/maps/poring-village-location.bmp', navLabel('Poring Village entrance location — Criatura Academy','Emplacement de l’entrée de Poring Village — Criatura Academy')],
          ['https://d33wubrfki0l68.cloudfront.net/11384f1547675a629da8c425bd831b82f85d701a/9a775/images/monsters/3810-md-king-poring.gif', 'King Poring — Criatura Academy']
        ],
        monsters: [
          ['Fortified Poring','34','1,023','10 / 12','Formless','Earth Lv.1','Small','369 / 291'],
          ['Fortified Marin','33','960','10 / 10','Formless','Water Lv.1','Small','358 / 279'],
          ['Fortified Poporing','36','1,167','10 / 12','Formless','Wind Lv.1','Small','384 / 309'],
          ['Fortified Drops','35','1,095','10 / 10','Formless','Fire Lv.1','Small','377 / 300'],
          ['Amering','35','72,810','10 / 10','Formless','Poison Lv.1','Large','6,375 / 5,524'],
          ['Goldring','35','72,118','10 / 10','Formless','Holy Lv.1','Large','6,327 / 5,565'],
          ['King Poring','35','140,000','20 / 20','Formless','Neutral Lv.1 (KRO) / Lv.2 (TWRo)','Large','9,580 / 8,288']
        ],
        rewards: [
          navLabel('Treasure chest: non-sale Red, Blue, Orange, Yellow, White and Green Potions (KRO reference).','Coffre : Red, Blue, Orange, Yellow, White et Green Potions non revendables (référence KRO).'),
          navLabel('Poring Village Green Onion / Leek — translation differs by source.','Poring Village Green Onion / Leek — traduction différente selon la source.'),
          'Poring Village Carrot',
          navLabel('Daily Jello Fragment reward: Poring (Mon), Poporing (Tue), Drops (Wed), Deviling (Thu), Angeling (Fri), Jello Fragment Box (Sat/Sun) — KRO reference.','Récompense Jello Fragment selon le jour : Poring (lun.), Poporing (mar.), Drops (mer.), Deviling (jeu.), Angeling (ven.), Jello Fragment Box (sam./dim.) — référence KRO.')
        ],
        sources: [
          ['MidgardHub / Lymd — Current Global New Player Guide','https://midgardhub.com/guides/new-player'],
          ['MidgardHub — Memorial Dungeons (TWRo reference)','https://midgardhub.com/guides/memorial-dungeons'],
          ['Criatura Academy — Poring Village (KRO Zero)','https://old.criatura-academy.com/memorial-dungeons/poring-village']
        ]
      },
      'orcs-memory': {
        name: "Orc's Memory",
        subtitle: navLabel('Memorial Dungeon — Orc Village','Mémorial Donjon — Orc Village'),
        access: navLabel('KRO reference: Orc Village, outside Orc Dungeon, through the Scientist NPC. The dungeon is live on Global since the September 3 update.','Référence KRO : Orc Village, à l’extérieur d’Orc Dungeon, via le NPC Scientist. Le donjon est live sur Global depuis la mise à jour du 3 septembre.'),
        level: navLabel('KRO reference: Base Lv. 59+','Référence KRO : Base Lv. 59+'),
        objective: navLabel("Progress through the Orc encounters and defeat Fallen Orc Hero. The KRO guide warns that Shaman's Flowers strengthen the final boss.","Progresse à travers les groupes d’Orcs et bats Fallen Orc Hero. Le guide KRO avertit que les Shaman's Flowers renforcent le boss final."),
        mechanics: [
          navLabel("KRO/Criatura: Shaman's Flowers buff Fallen Orc Hero and should not be ignored.","KRO/Criatura : les Shaman's Flowers renforcent Fallen Orc Hero et ne doivent pas être ignorées."),
          navLabel('KRO/Criatura: Grade IV Memorial Dungeon equipment is part of the normal-mode reward pool.','KRO/Criatura : l’équipement Mémorial Donjon Grade IV fait partie des récompenses du mode normal.'),
          navLabel('Official Global September 3 update confirms the new Memorial Dungeon wave, but does not publish the complete monster/reward table.','La mise à jour officielle Global du 3 septembre confirme la nouvelle vague de Mémorial Donjons mais ne publie pas le tableau complet des monstres/récompenses.')
        ],
        crosscheck: [
          navLabel('Criatura is a Korean Ragnarok Zero reference. Exact monster stats and reward quantities below are therefore marked as regional reference data unless independently confirmed on Global.','Criatura est une référence Ragnarok Zero coréenne. Les stats exactes et quantités de récompenses ci-dessous restent donc des données régionales tant qu’elles ne sont pas confirmées indépendamment sur Global.'),
          navLabel('MidgardHub’s Memorial Dungeon page is derived from TWRo and explicitly warns that NPCs, rewards and mechanics may differ on Global.','La page Mémorial Donjon de MidgardHub est dérivée de TWRo et avertit explicitement que NPC, récompenses et mécaniques peuvent différer sur Global.'),
          navLabel('Party/solo rules conflict between regional references (KRO party vs TWRo solo overview); the wiki leaves the Global entry mode unasserted until live confirmation.','Les règles party/solo se contredisent entre références régionales (KRO party vs aperçu TWRo solo) ; le wiki ne fixe donc pas le mode d’entrée Global tant qu’il n’est pas confirmé live.')
        ],
        images: [
          ['https://d33wubrfki0l68.cloudfront.net/acb128fac29195d6b809889b3887ff327599c32d/f8dc8/images/maps/orcs-memory-location.bmp', navLabel("Orc's Memory entrance location — Criatura Academy","Emplacement de l’entrée de Orc's Memory — Criatura Academy")],
          ['https://d33wubrfki0l68.cloudfront.net/67f65a7c902bc00f0429108eac358dcc1a85e77a/ad4a4/images/monsters/3901-md-fallen-orc-hero.png', 'Fallen Orc Hero — Criatura Academy']
        ],
        monsters: [
          ['Orc Skeleton','60','4,458','82 / 10','Undead','Undead Lv.1','Medium','627 / 562'],
          ['Orc Zombie','60','4,475','71 / 5','Brute','Undead Lv.1','Medium','649 / 600'],
          ['Anapholes','95','6,617','7 / 10','Insect','Wind Lv.3','Small','? / ?'],
          ["Shaman's Flower",'98','5','160 / 99','Plant','Earth Lv.1','Medium','0 / 0'],
          ['Fallen Orc Hero','70','2,110,562','197 / 70','Demi-human','Earth Lv.2','Large','166,639 / 118,717']
        ],
        rewards: [
          navLabel('KRO Normal: Shimmering Crystal ×1–3.','KRO Normal : Shimmering Crystal ×1–3.'),
          navLabel('KRO Normal: Subjugation Sash [1] and Subjugation Armor [1].','KRO Normal : Subjugation Sash [1] et Subjugation Armor [1].'),
          navLabel('KRO Hard reference pool: Shimmering Crystal ×6–10, Cursed Emerald ×0–3, Mithril Ore ×1–4, Elunium/Oridecon and rough ores, plus elemental materials.','Pool KRO Hard : Shimmering Crystal ×6–10, Cursed Emerald ×0–3, Mithril Ore ×1–4, Elunium/Oridecon et minerais bruts, plus matériaux élémentaires.')
        ],
        sources: [
          ["Criatura Academy — Orc's Memory (KRO Zero)",'https://old.criatura-academy.com/memorial-dungeons/orcs-memory/'],
          ['MidgardHub — Memorial Dungeons (TWRo reference)','https://midgardhub.com/guides/memorial-dungeons'],
          ['Official GNJOY — September 3 update','https://roz.mygnjoy.com/en/news/update/92'],
          ['Prontera.info — Global release tracker','https://roz.prontera.info/release']
        ]
      },
      'prontera-culvert': {
        name: 'Prontera Culvert',
        subtitle: navLabel('Memorial Dungeon — Prontera field','Mémorial Donjon — champ de Prontera'),
        access: navLabel('KRO reference: prt_fild05 264, 208, one map west of Prontera, through the Culvert Manager. The dungeon is live on Global since the September 3 update.','Référence KRO : prt_fild05 264, 208, une map à l’ouest de Prontera, via le Culvert Manager. Le donjon est live sur Global depuis la mise à jour du 3 septembre.'),
        level: navLabel('KRO reference: Base Lv. 59+','Référence KRO : Base Lv. 59+'),
        objective: navLabel('KRO reference: destroy the Ancient Thief Bug Eggs to spawn Ancient Golden Thief Bug; clearing the eggs around the boss before killing it enables the bonus chest.','Référence KRO : détruis les Ancient Thief Bug Eggs pour faire apparaître Ancient Golden Thief Bug ; éliminer les œufs autour du boss avant de le tuer permet d’obtenir le coffre bonus.'),
        mechanics: [
          navLabel('KRO/Criatura: the first egg-clearing phase triggers the boss spawn.','KRO/Criatura : la première phase de destruction des œufs déclenche l’apparition du boss.'),
          navLabel('KRO/Criatura: clear the eggs around the boss before finishing Ancient Golden Thief Bug for the bonus-chest condition.','KRO/Criatura : élimine les œufs autour du boss avant de terminer Ancient Golden Thief Bug pour remplir la condition du coffre bonus.'),
          navLabel('Official Global September 3 update confirms the new Memorial Dungeon wave, but does not publish the complete monster/reward table.','La mise à jour officielle Global du 3 septembre confirme la nouvelle vague de Mémorial Donjons mais ne publie pas le tableau complet des monstres/récompenses.')
        ],
        crosscheck: [
          navLabel('Criatura/KRO gives the 59+ entry level, egg mechanic and exact monster/reward figures shown below.','Criatura/KRO fournit le niveau d’entrée 59+, la mécanique des œufs et les chiffres exacts de monstres/récompenses affichés ci-dessous.'),
          navLabel('MidgardHub’s Memorial Dungeon guide is TWRo-derived and explicitly warns that exact NPC locations, rewards and mechanics may differ on Global.','Le guide Mémorial Donjon de MidgardHub est dérivé de TWRo et avertit explicitement que les emplacements NPC, récompenses et mécaniques exactes peuvent différer sur Global.'),
          navLabel('Party/solo rules conflict between regional references; the wiki does not present either regional rule as confirmed Global behavior.','Les règles party/solo se contredisent entre références régionales ; le wiki ne présente donc aucune de ces règles comme comportement Global confirmé.')
        ],
        images: [
          ['https://d33wubrfki0l68.cloudfront.net/9ff892c03fa929822f41914bdbf47af262606300/215d8/images/maps/prontera-culvert-location.bmp', navLabel('Prontera Culvert entrance location — Criatura Academy','Emplacement de l’entrée de Prontera Culvert — Criatura Academy')],
          ['https://d33wubrfki0l68.cloudfront.net/44db4f8728a5ffbb886ecd69ac4022383f3ac3c2/c6717/images/monsters/3975-md-ancient-golden-thief-bug.png', 'Ancient Golden Thief Bug — Criatura Academy']
        ],
        monsters: [
          ['Sewer Giant Thief Bug','60','3,330','40 / 20','Formless','Shadow Lv.1','Medium','0 / 0'],
          ['Sewer Thief Bug','60','200','24 / 3','Insect','Neutral Lv.3','Small','0 / 0'],
          ['Ancient Thief Bug Egg','60','10','64 / 10','Insect','Shadow Lv.1','Small','0 / 0'],
          ['Ancient Golden Thief Bug','60','1,200,000','159 / 81','Insect','Fire Lv.1','Large','75,000 / 63,000']
        ],
        rewards: [
          navLabel('KRO Normal: Shimmering Crystal ×1–3.','KRO Normal : Shimmering Crystal ×1–3.'),
          navLabel('KRO Normal: Subjugation Ring [1] and Subjugation Boots [1].','KRO Normal : Subjugation Ring [1] et Subjugation Boots [1].'),
          navLabel('KRO Hard reference pool: Shimmering Crystal ×6–10, Shiny Opal ×0–3, Mithril Ore ×1–4, Elunium/Oridecon and rough ores, plus elemental materials.','Pool KRO Hard : Shimmering Crystal ×6–10, Shiny Opal ×0–3, Mithril Ore ×1–4, Elunium/Oridecon et minerais bruts, plus matériaux élémentaires.')
        ],
        sources: [
          ['Criatura Academy — Prontera Culvert (KRO Zero)','https://old.criatura-academy.com/memorial-dungeons/prontera-culvert/'],
          ['MidgardHub — Memorial Dungeons (TWRo reference)','https://midgardhub.com/guides/memorial-dungeons'],
          ['Official GNJOY — September 3 update','https://roz.mygnjoy.com/en/news/update/92'],
          ['Prontera.info — Global release tracker','https://roz.prontera.info/release']
        ]
      }
    };
  }
'''
s = s[:md_start] + memorial_data + s[md_end:]

# Replace Memorial Dungeon detail renderer so each guide has images + explicit source cross-check.
detail_start = s.index('  function memorialDungeonDetail(id) {')
detail_end = s.index('\n  function ', detail_start + len('  function memorialDungeonDetail(id) {'))
memorial_detail = r'''  function memorialDungeonDetail(id) {
    const d = memorialDungeonData()[id];
    if (!d) return notFound();
    const monsterRows = d.monsters.map(m=>`<tr><th>${esc(m[0])}</th><td>${esc(m[1])}</td><td>${esc(m[2])}</td><td>${esc(m[3])}</td><td>${esc(m[4])}</td><td>${esc(m[5])}</td><td>${esc(m[6])}</td><td>${esc(m[7])}</td></tr>`).join('');
    const gallery = (d.images || []).length ? `<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;align-items:start;margin:16px 0 24px">${d.images.map(([src,caption])=>`<figure style="margin:0;text-align:center"><div style="min-height:190px;display:flex;align-items:center;justify-content:center;border:1px solid var(--line-soft);background:#f8f9fa;padding:10px"><img src="${esc(src)}" alt="${esc(caption)}" loading="lazy" style="display:block;max-width:100%;max-height:300px;width:auto;height:auto;image-rendering:auto"></div><figcaption style="margin-top:7px;color:var(--muted);font-size:12px">${esc(caption)}</figcaption></figure>`).join('')}</div>` : '';
    return `${breadcrumbs([{label:navLabel('Memorial Dungeons','Mémorial Donjons'),href:'#/memorial-dungeons'},{label:d.name}])}
      <div class="article-heading"><h1>${icon('memorial')}${esc(d.name)}</h1><div class="page-subtitle">${esc(d.subtitle)}</div></div>
      ${gallery}
      <div class="table-wrap"><table><tbody>
        <tr><th>${navLabel('Entry / Location','Entrée / Emplacement')}</th><td>${esc(d.access)}</td></tr>
        <tr><th>${navLabel('Level','Niveau')}</th><td>${esc(d.level)}</td></tr>
        <tr><th>${navLabel('Main objective','Objectif principal')}</th><td>${esc(d.objective)}</td></tr>
      </tbody></table></div>

      <h2 id="mechanics">${navLabel('Dungeon guide','Guide du donjon')}</h2>
      <ul>${d.mechanics.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>

      <h2 id="source-check">${navLabel('Source cross-check','Croisement des sources')}</h2>
      <div class="notice info"><svg class="notice-icon"><use href="#i-info"></use></svg><div>${navLabel('MidgardHub and Criatura document different regional versions of Ragnarok Zero. Current Global / official evidence takes priority; conflicting regional values remain labeled instead of being silently merged.','MidgardHub et Criatura documentent des versions régionales différentes de Ragnarok Zero. Les données Global actuelles / officielles sont prioritaires ; les valeurs régionales contradictoires restent indiquées au lieu d’être fusionnées silencieusement.')}</div></div>
      <ul>${(d.crosscheck || []).map(x=>`<li>${esc(x)}</li>`).join('')}</ul>

      <h2 id="monsters">${navLabel('Monsters & Bosses','Monstres et Boss')}</h2>
      <div class="table-wrap"><table>
        <thead><tr><th>${navLabel('Monster','Monstre')}</th><th>Lv.</th><th>HP</th><th>DEF / MDEF</th><th>${navLabel('Race','Race')}</th><th>${navLabel('Property','Propriété')}</th><th>${navLabel('Size','Taille')}</th><th>Base / Job EXP</th></tr></thead>
        <tbody>${monsterRows}</tbody>
      </table></div>

      <h2 id="rewards">${navLabel('Rewards','Récompenses')}</h2>
      <ul>${d.rewards.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>

      ${officialSources(d.sources)}`;
  }
'''
s = s[:detail_start] + memorial_detail + s[detail_end:]

# --- Craft: index only, every system opens its own page ---
craft_start = s.index('  function craftingPage(topic) {')
craft_end = s.index('\n  function enchantmentPage(topic) {', craft_start)
craft_code = r'''  function craftingPage(topic) {
    const title = navLabel('Crafting','Craft');
    const cards = [
      ['arrow-crafting','Arrow Crafting',navLabel('Archer quest skill for converting compatible materials into arrows.','Skill de quête Archer permettant de transformer certains matériaux en flèches.')],
      ['blacksmith-forging','Blacksmith Forging',navLabel('Blacksmith weapon forging and its recipe system.','Forge d’armes Blacksmith et son système de recettes.')],
      ['potion-creation','Potion Creation',navLabel('Alchemist brewing with Potion Research and Prepare Potion.','Brewing Alchemist avec Potion Research et Prepare Potion.')],
      ['system-recipes',navLabel('NPC / System Recipes','Recettes NPC / Systèmes'),navLabel('Crafts handled by NPCs or content-specific systems.','Crafts réalisés via des NPC ou des systèmes de contenu spécifiques.')]
    ];
    return `${breadcrumbs([{label:title}])}
      <div class="article-heading"><h1>${icon('item')}${title}</h1><div class="page-subtitle">${t('fromWiki')}</div></div>
      <p class="article-lead">${navLabel('Crafting is an index of separate crafting systems. Open a system below to access its dedicated guide; detailed recipe tables are only promoted after current Global verification.','Craft est maintenant un index de systèmes séparés. Ouvre un système ci-dessous pour accéder à son guide dédié ; les tableaux de recettes détaillés ne passent en vérifié qu’après contrôle sur la version Global actuelle.')}</p>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px;margin:18px 0 24px">
        ${cards.map(([id,name,desc])=>`<a class="panel" href="#/crafting/${id}" style="display:block;color:inherit;text-decoration:none;overflow:hidden"><div class="panel-heading">${miniIcon('item')}${name}</div><div class="panel-body"><p>${desc}</p><span class="table-link">${navLabel('Open guide →','Ouvrir le guide →')}</span></div></a>`).join('')}
      </div>
      <div class="notice"><svg class="notice-icon"><use href="#i-warning"></use></svg><div>${navLabel('Do not use TWROZ/iRO recipe quantities as Global values unless they have been checked against the current Global client or current Global sources.','Ne pas utiliser les quantités de recettes TWROZ/iRO comme valeurs Global tant qu’elles n’ont pas été contrôlées avec le client Global actuel ou des sources Global actuelles.')}</div></div>
      ${officialSources([
        ['MidgardHub — current Global guides/database','https://midgardhub.com/'],
        ['Criatura Academy — KRO Zero reference database','https://old.criatura-academy.com/']
      ])}`;
  }

  function craftingDetailPage(id) {
    const back = `<p><a href="#/wiki/crafting">← ${navLabel('Back to Crafting','Retour au Craft')}</a></p>`;
    if (id === 'arrow-crafting') {
      return `${breadcrumbs([{label:navLabel('Crafting','Craft'),href:'#/wiki/crafting'},{label:'Arrow Crafting'}])}
        <div class="article-heading"><h1>${icon('item')}Arrow Crafting</h1><div class="page-subtitle">${t('fromWiki')}</div></div>
        <p class="article-lead">${navLabel('Arrow Crafting is the Archer quest skill used to convert compatible materials into arrows.','Arrow Crafting est le skill de quête Archer utilisé pour transformer des matériaux compatibles en flèches.')}</p>
        <div class="table-wrap"><table><tbody>
          <tr><th>${navLabel('Class','Classe')}</th><td><a href="#/classes/archer">Archer</a></td></tr>
          <tr><th>${navLabel('Skill level','Niveau du skill')}</th><td>Lv. 1</td></tr>
          <tr><th>SP</th><td>10</td></tr>
          <tr><th>${navLabel('Skill page','Page du skill')}</th><td><a href="#/skills/arrow-crafting">Arrow Crafting</a></td></tr>
        </tbody></table></div>
        <h2>${navLabel('Recipes','Recettes')}</h2>
        <p>${navLabel('Material → Arrow outputs will be listed here once the current Global recipe table is verified.','Les conversions matériau → flèches seront listées ici une fois le tableau de recettes Global actuel vérifié.')}</p>
        ${back}`;
    }
    if (id === 'blacksmith-forging') {
      return `${breadcrumbs([{label:navLabel('Crafting','Craft'),href:'#/wiki/crafting'},{label:'Blacksmith Forging'}])}
        <div class="article-heading"><h1>${icon('item')}Blacksmith Forging</h1><div class="page-subtitle">${t('fromWiki')}</div></div>
        <p class="article-lead">${navLabel('Blacksmith Forging covers weapon-production skills, forging materials and recipe-specific results for the Blacksmith branch.','Blacksmith Forging regroupe les skills de production d’armes, les matériaux de forge et les résultats propres aux recettes de la branche Blacksmith.')}</p>
        <p><a href="#/classes/blacksmith">${navLabel('Open the Blacksmith class page','Ouvrir la page de la classe Blacksmith')}</a></p>
        <h2>${navLabel('Recipe database','Base de recettes')}</h2>
        <p>${navLabel('The exact Global forging recipe table is being separated from older regional RO tables. Recipes will be added here after verification rather than copied from iRO/TWROZ.','Le tableau exact des recettes de forge Global est séparé des anciennes tables régionales RO. Les recettes seront ajoutées ici après vérification au lieu d’être copiées depuis iRO/TWROZ.')}</p>
        ${officialSources([['MidgardHub — Global guides/database','https://midgardhub.com/'],['Criatura Academy — KRO Zero reference','https://old.criatura-academy.com/']])}
        ${back}`;
    }
    if (id === 'potion-creation') {
      return `${breadcrumbs([{label:navLabel('Crafting','Craft'),href:'#/wiki/crafting'},{label:'Potion Creation'}])}
        <div class="article-heading"><h1>${icon('item')}Potion Creation</h1><div class="page-subtitle">${t('fromWiki')}</div></div>
        <p class="article-lead">${navLabel('Alchemist uses Prepare Potion to brew potions and chemical items.','L’Alchemist utilise Prepare Potion pour fabriquer des potions et des objets chimiques.')}</p>
        <div class="table-wrap"><table>
          <thead><tr><th>${navLabel('Skill / Requirement','Skill / Prérequis')}</th><th>${navLabel('Current Global information','Information Global actuelle')}</th></tr></thead>
          <tbody>
            <tr><th>Potion Research</th><td>${navLabel('Passive, Max Lv.10. Improves potion effectiveness and contributes to potion crafting.','Passif, Max Lv.10. Améliore l’efficacité des potions et participe au craft de potions.')}</td></tr>
            <tr><th>Prepare Potion</th><td>${navLabel('Max Lv.10 · Requires Potion Research Lv.5 · 5 SP per use.','Max Lv.10 · Requiert Potion Research Lv.5 · 5 SP par utilisation.')}</td></tr>
            <tr><th>Mortar Bowl</th><td>${navLabel('1 Mortar Bowl is consumed when Prepare Potion is used.','1 Mortar Bowl est consommé à l’utilisation de Prepare Potion.')}</td></tr>
            <tr><th>${navLabel('Potion manual','Manuel de potion')}</th><td>${navLabel('The corresponding manual is required for the potion or chemical item being crafted.','Le manuel correspondant est requis selon la potion ou l’objet chimique fabriqué.')}</td></tr>
          </tbody>
        </table></div>
        <div class="notice info"><svg class="notice-icon"><use href="#i-info"></use></svg><div>${navLabel('The exact brewing success formula is not presented as definitive until the current Global formula is independently verified.','La formule exacte de réussite du brewing n’est pas présentée comme définitive tant que la formule Global actuelle n’est pas vérifiée indépendamment.')}</div></div>
        ${officialSources([
          ['Prontera.info — Alchemist / Prepare Potion','https://roz.prontera.info/skills/planner?class=creator'],
          ['Prontera.info — Data & Formulas','https://roz.prontera.info/mechanics'],
          ['MidgardHub — Brewing Calculator','https://midgardhub.com/tools/brewing'],
          ['Criatura Academy — KRO Zero reference','https://old.criatura-academy.com/']
        ])}
        ${back}`;
    }
    if (id === 'system-recipes') {
      return `${breadcrumbs([{label:navLabel('Crafting','Craft'),href:'#/wiki/crafting'},{label:navLabel('NPC / System Recipes','Recettes NPC / Systèmes')}])}
        <div class="article-heading"><h1>${icon('item')}${navLabel('NPC / System Recipes','Recettes NPC / Systèmes')}</h1><div class="page-subtitle">${t('fromWiki')}</div></div>
        <p class="article-lead">${navLabel('This page groups crafts produced through an NPC or a content-specific system rather than a class crafting skill.','Cette page regroupe les crafts produits via un NPC ou un système de contenu spécifique plutôt que par un skill de craft de classe.')}</p>
        <p>${navLabel('Each recipe will be documented with its NPC, location, inputs, output and current Global verification status.','Chaque recette sera documentée avec son NPC, son emplacement, ses composants, son résultat et son statut de vérification Global actuel.')}</p>
        ${back}`;
    }
    return notFound();
  }
'''
s = s[:craft_start] + craft_code + s[craft_end:]

# Route dedicated Craft pages.
router_marker = "    else if(hash[0]==='wiki'&&hash[1]) html=topicDetail(hash[1]);"
if router_marker not in s:
    raise SystemExit('Router marker not found')
s = s.replace(router_marker, "    else if(hash[0]==='crafting'&&hash[1]) html=craftingDetailPage(hash[1]);\n" + router_marker, 1)

# Validation.
assert "function craftingDetailPage(id)" in s
assert "#/crafting/potion-creation" in s
assert "Potion Creation</h1>" in s
assert "function memorialDungeonDetail(id)" in s
assert "Croisement des sources" in s
assert "Neutral Lv.1 (KRO) / Lv.2 (TWRo)" in s
for url in [
    'poring-village-location.bmp',
    'orcs-memory-location.bmp',
    'prontera-culvert-location.bmp',
    '3901-md-fallen-orc-hero.png',
    '3975-md-ancient-golden-thief-bug.png'
]:
    assert url in s

p.write_text(s, encoding='utf-8')
print('Memorial guides cross-checked and Craft split into dedicated pages.')
