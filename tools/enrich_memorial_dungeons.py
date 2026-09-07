from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

start = s.index('  function memorialDungeonData() {')
end = s.index('\n  function memorialDungeonDatabasePage()', start)

new_block = r'''  function memorialDbSlug(name) {
    return String(name || '')
      .toLowerCase()
      .normalize('NFD').replace(/[\u0300-\u036f]/g,'')
      .replace(/\[[^\]]*\]/g,'')
      .replace(/[^a-z0-9]+/g,'-')
      .replace(/^-+|-+$/g,'');
  }

  function memorialDbLink(kind, name) {
    const label = esc(name);
    const slug = memorialDbSlug(name);
    return `<a class="table-link" href="#/${kind}/${slug}" data-db-kind="${kind}" data-db-name="${esc(name)}">${label}</a>`;
  }

  function memorialDungeonData() {
    return {
      'poring-village': {
        name: 'Poring Village',
        subtitle: navLabel('Early Memorial Dungeon','Mémorial Donjon de début de progression'),
        level: 'Base Lv. 30–60',
        access: navLabel('/navi prt_fild05 146/235. One map west of Prontera. Speak with Emily on the west side of the field.','/navi prt_fild05 146/235. Une map à l’ouest de Prontera. Parle à Emily sur la partie ouest du field.'),
        requirements: [
          navLabel('Base Level 30 to 60.','Base Level 30 à 60.'),
          navLabel('Enter through the Memorial Dungeon NPC.','Entrée via le NPC du Mémorial Donjon.'),
          navLabel('One completion per day; the restriction resets at 04:00.','Une complétion par jour ; la restriction se réinitialise à 04:00.')
        ],
        objective: navLabel('Clear three waves of Porings. Each wave ends with a boss, and the final clear opens the treasure reward.','Élimine trois vagues de Porings. Chaque vague se termine par un boss et la fin de l’instance ouvre la récompense du coffre.'),
        steps: [
          navLabel('Enter the village and clear the first group of fortified Porings.','Entre dans le village et élimine le premier groupe de Porings renforcés.'),
          navLabel('Use the blue pillars when useful: they transform the character and temporarily increase ATK.','Utilise les piliers bleus quand c’est utile : ils transforment le personnage et augmentent temporairement l’ATK.'),
          navLabel('Defeat the boss of each wave and continue until the third boss is defeated.','Bats le boss de chaque vague et continue jusqu’à la défaite du troisième boss.'),
          navLabel('Claim the treasure chest and the daily Jello Fragment reward.','Récupère le coffre et la récompense quotidienne en Jello Fragment.')
        ],
        mechanics: [
          navLabel('Blue pillars provide a temporary transformation with increased ATK.','Les piliers bleus donnent une transformation temporaire avec une augmentation d’ATK.'),
          navLabel('Treasure rewards improve with more party members.','Les récompenses du coffre augmentent avec davantage de membres dans le groupe.'),
          navLabel('The daily fragment depends on the day of the week.','Le fragment quotidien dépend du jour de la semaine.')
        ],
        images: [
          ['https://d33wubrfki0l68.cloudfront.net/66417fa7576de4232df6a19e65681ca14ca7eec6/ae066/images/maps/poring-village-location.bmp', navLabel('Poring Village entrance location','Emplacement de l’entrée de Poring Village')],
          ['https://d33wubrfki0l68.cloudfront.net/11384f1547675a629da8c425bd831b82f85d701a/9a775/images/monsters/3810-md-king-poring.gif', 'King Poring']
        ],
        monsters: [
          {name:'Fortified Poring',level:'34',hp:'1,023',def:'10',mdef:'12',class:'Normal',race:'Formless',element:'Earth Lv.1',size:'Small',baseExp:'369',jobExp:'291'},
          {name:'Fortified Marin',level:'33',hp:'960',def:'10',mdef:'10',class:'Normal',race:'Formless',element:'Water Lv.1',size:'Small',baseExp:'358',jobExp:'279'},
          {name:'Fortified Poporing',level:'36',hp:'1,167',def:'10',mdef:'12',class:'Normal',race:'Formless',element:'Wind Lv.1',size:'Small',baseExp:'384',jobExp:'309'},
          {name:'Fortified Drops',level:'35',hp:'1,095',def:'10',mdef:'10',class:'Normal',race:'Formless',element:'Fire Lv.1',size:'Small',baseExp:'377',jobExp:'300'},
          {name:'Amering',level:'35',hp:'72,810',def:'10',mdef:'10',class:'Boss',race:'Formless',element:'Poison Lv.1',size:'Large',baseExp:'6,375',jobExp:'5,524'},
          {name:'Goldring',level:'35',hp:'72,118',def:'10',mdef:'10',class:'Boss',race:'Formless',element:'Holy Lv.1',size:'Large',baseExp:'6,327',jobExp:'5,565'},
          {name:'King Poring',level:'35',hp:'140,000',def:'20',mdef:'20',class:'Boss',race:'Formless',element:'Neutral',size:'Large',baseExp:'9,580',jobExp:'8,288'}
        ],
        rewardIntro: navLabel('The completion chest can contain consumables, lower headgear and materials used by the Memorial Dungeon crafting chain.','Le coffre de fin peut contenir des consommables, des lower headgear et des matériaux utilisés dans la chaîne de craft des Mémorial Donjons.'),
        rewardGroups: [
          {title:navLabel('Consumables','Consommables'), rows:[
            {item:'[Not For Sale] Red Potion',qty:'—'}, {item:'[Not For Sale] Blue Potion',qty:'—'},
            {item:'[Not For Sale] Orange Potion',qty:'—'}, {item:'[Not For Sale] Yellow Potion',qty:'—'},
            {item:'[Not For Sale] White Potion',qty:'—'}, {item:'[Not For Sale] Green Potion',qty:'—'}
          ]},
          {title:navLabel('Daily Jello Fragment','Jello Fragment quotidien'), rows:[
            {item:'Poring Jello Fragment',qty:navLabel('Monday','Lundi')},
            {item:'Poporing Jello Fragment',qty:navLabel('Tuesday','Mardi')},
            {item:'Drops Jello Fragment',qty:navLabel('Wednesday','Mercredi')},
            {item:'Deviling Jello Fragment',qty:navLabel('Thursday','Jeudi')},
            {item:'Angeling Jello Fragment',qty:navLabel('Friday','Vendredi')},
            {item:'Jello Fragment Box',qty:navLabel('Saturday / Sunday','Samedi / Dimanche')}
          ]}
        ],
        headgear: [
          {name:'Poring Village Leek',slot:'0',level:'30',weight:'10',effect:navLabel('When receiving a physical attack, has a chance to transform the wearer into a Smokie for 5 seconds. Movement speed is increased while transformed and does not stack with Increase Agility.','Lorsqu’une attaque physique est reçue, a une chance de transformer le porteur en Smokie pendant 5 secondes. La vitesse de déplacement augmente pendant la transformation et ne se cumule pas avec Increase Agility.')},
          {name:'Poring Village Carrot',slot:'0',level:'30',weight:'10',effect:navLabel('When performing a physical attack, has a chance to transform the wearer into a Lunatic for 5 seconds. Movement speed is increased while transformed and does not stack with Increase Agility.','Lors d’une attaque physique, a une chance de transformer le porteur en Lunatic pendant 5 secondes. La vitesse de déplacement augmente pendant la transformation et ne se cumule pas avec Increase Agility.')}
        ],
        enchant: {
          cost: navLabel('50 Jellopy + 20,000 zeny per enchant attempt.','50 Jellopy + 20 000 zeny par tentative d’enchantement.'),
          reset: navLabel('Reset costs 200,000 zeny. Enchanting and resetting each have a 30% failure chance; on failure the item is destroyed.','Le reset coûte 200 000 zeny. L’enchantement et le reset ont chacun 30 % de risque d’échec ; en cas d’échec l’objet est détruit.'),
          rules:[navLabel('Only one enchant can be added to the headgear.','Un seul enchantement peut être ajouté au headgear.')],
          options:['STR +1','VIT +1','INT +1','DEX +1','AGI +1','LUK +1','SP +10','SP +25','SP +50','HP +100','HP +200']
        },
        sources: [
          ['Poring Village guide','https://old.criatura-academy.com/memorial-dungeons/poring-village'],
          ['Memorial Dungeons guide','https://midgardhub.com/guides/memorial-dungeons'],
          ['Current New Player Guide','https://midgardhub.com/guides/new-player']
        ]
      },

      'orcs-memory': {
        name: "Orc's Memory",
        subtitle: navLabel('Memorial Dungeon — Orc Village','Mémorial Donjon — Orc Village'),
        level: 'Base Lv. 59+',
        access: navLabel('Go to Orc Village, outside Orc Dungeon, and speak with the Scientist NPC to create the instance.','Va à Orc Village, à l’extérieur d’Orc Dungeon, puis parle au NPC Scientist pour créer l’instance.'),
        requirements: [
          navLabel('Base Level 59 or higher.','Base Level 59 ou plus.'),
          navLabel('Create the instance from the Scientist NPC.','Crée l’instance auprès du NPC Scientist.')
        ],
        objective: navLabel("Progress through the Orc encounters and defeat Fallen Orc Hero. Shaman's Flowers strengthen the final boss and should be handled during the fight.","Progresse à travers les combats contre les Orcs et bats Fallen Orc Hero. Les Shaman's Flowers renforcent le boss final et doivent être gérées pendant le combat."),
        steps: [
          navLabel('Create the instance and enter Orc’s Memory.','Crée l’instance et entre dans Orc’s Memory.'),
          navLabel('Clear the Orc Skeleton, Orc Zombie and Anapholes encounters while progressing through the dungeon.','Élimine les Orc Skeleton, Orc Zombie et Anapholes en progressant dans le donjon.'),
          navLabel("At the final encounter, destroy or control the Shaman's Flowers so they do not keep strengthening Fallen Orc Hero.","Lors du combat final, détruis ou contrôle les Shaman's Flowers afin qu’elles ne continuent pas à renforcer Fallen Orc Hero."),
          navLabel('Defeat Fallen Orc Hero and claim the completion chest.','Bats Fallen Orc Hero puis récupère le coffre de fin.')
        ],
        mechanics: [
          navLabel("Shaman's Flowers are boss-class objects with very low HP but high DEF/MDEF and act as part of the final-boss mechanic.","Les Shaman's Flowers sont des entités de classe Boss avec très peu de HP mais une DEF/MDEF élevée et font partie de la mécanique du boss final."),
          navLabel('Equipment rewards increase when the party has 7 or more members.','Les récompenses d’équipement augmentent lorsque le groupe compte 7 membres ou plus.'),
          navLabel('Normal and Hard modes use different reward pools and quantities.','Les modes Normal et Hard utilisent des pools et quantités de récompenses différents.')
        ],
        images: [
          ['https://d33wubrfki0l68.cloudfront.net/acb128fac29195d6b809889b3887ff327599c32d/f8dc8/images/maps/orcs-memory-location.bmp', navLabel("Orc's Memory entrance location","Emplacement de l’entrée de Orc's Memory")],
          ['https://d33wubrfki0l68.cloudfront.net/67f65a7c902bc00f0429108eac358dcc1a85e77a/ad4a4/images/monsters/3901-md-fallen-orc-hero.png', 'Fallen Orc Hero']
        ],
        monsters: [
          {name:'Orc Skeleton',level:'60',hp:'4,458',def:'82',mdef:'10',class:'Normal',race:'Undead',element:'Undead Lv.1',size:'Medium',baseExp:'627',jobExp:'562'},
          {name:'Orc Zombie',level:'60',hp:'4,475',def:'71',mdef:'5',class:'Normal',race:'Brute',element:'Undead Lv.1',size:'Medium',baseExp:'649',jobExp:'600'},
          {name:'Anapholes',level:'95',hp:'6,617',def:'7',mdef:'10',class:'Normal',race:'Insect',element:'Wind Lv.3',size:'Small',baseExp:'?',jobExp:'?'},
          {name:"Shaman's Flower",level:'98',hp:'5',def:'160',mdef:'99',class:'Boss',race:'Plant',element:'Earth Lv.1',size:'Medium',baseExp:'0',jobExp:'0'},
          {name:'Fallen Orc Hero',level:'70',hp:'2,110,562',def:'197',mdef:'70',class:'Boss',race:'Demi-human',element:'Earth Lv.2',size:'Large',baseExp:'166,639',jobExp:'118,717'}
        ],
        rewardIntro: navLabel('The completion chest contains dungeon crafting materials and Subjugation equipment. Equipment quantities improve with a party of 7 or more members.','Le coffre de fin contient des matériaux de craft de donjon et de l’équipement Subjugation. Les quantités d’équipement augmentent avec un groupe de 7 membres ou plus.'),
        rewardGroups: [
          {title:navLabel('Normal Mode','Mode Normal'),rows:[
            {item:'Shimmering Crystal',qty:'1–3'},
            {item:'Subjugation Sash [1]',qty:'0–2 / 1–3'},
            {item:'Subjugation Armor [1]',qty:'0–2 / 1–3'}
          ]},
          {title:navLabel('Hard Mode','Mode Hard'),rows:[
            {item:'Shimmering Crystal',qty:'6–10'}, {item:'Cursed Emerald',qty:'0–3'}, {item:'Mithril Ore',qty:'1–4'},
            {item:'Elunium',qty:'1–3'}, {item:'Oridecon',qty:'1–3'}, {item:'Rough Elunium',qty:'2–8'},
            {item:'Rough Oridecon',qty:'2–8'}, {item:'Wind of Verdure',qty:'1–3'}, {item:'Red Blood',qty:'1–3'}, {item:'Green Live',qty:'1–3'}
          ]}
        ],
        sources: [
          ["Orc's Memory guide",'https://old.criatura-academy.com/memorial-dungeons/orcs-memory/'],
          ['Memorial Dungeons guide','https://midgardhub.com/guides/memorial-dungeons'],
          ['September 3 update','https://roz.mygnjoy.com/en/news/update/92']
        ]
      },

      'prontera-culvert': {
        name: 'Prontera Culvert',
        subtitle: navLabel('Memorial Dungeon — Prontera field','Mémorial Donjon — champ de Prontera'),
        level: 'Base Lv. 59+',
        access: navLabel('/navi prt_fild05 264/208. One map west of Prontera. Speak with the Culvert Manager to create the instance.','/navi prt_fild05 264/208. Une map à l’ouest de Prontera. Parle au Culvert Manager pour créer l’instance.'),
        requirements: [
          navLabel('Base Level 59 or higher.','Base Level 59 ou plus.'),
          navLabel('Create the instance from the Culvert Manager.','Crée l’instance auprès du Culvert Manager.')
        ],
        objective: navLabel('Destroy the Ancient Thief Bug Eggs to make Ancient Golden Thief Bug appear. Before killing the boss, clear the eggs around it to enable the bonus chest.','Détruis les Ancient Thief Bug Eggs pour faire apparaître Ancient Golden Thief Bug. Avant de tuer le boss, élimine les œufs autour de lui afin d’activer le coffre bonus.'),
        steps: [
          navLabel('Enter the culvert and clear the Sewer Thief Bugs and Sewer Giant Thief Bugs.','Entre dans les égouts et élimine les Sewer Thief Bugs et Sewer Giant Thief Bugs.'),
          navLabel('Destroy all Ancient Thief Bug Eggs in the first phase.','Détruis tous les Ancient Thief Bug Eggs pendant la première phase.'),
          navLabel('Ancient Golden Thief Bug appears after the egg-clearing condition is completed.','Ancient Golden Thief Bug apparaît une fois la condition de destruction des œufs remplie.'),
          navLabel('Before finishing the boss, destroy the eggs around it to satisfy the bonus-chest condition.','Avant d’achever le boss, détruis les œufs autour de lui pour remplir la condition du coffre bonus.'),
          navLabel('Defeat Ancient Golden Thief Bug and collect the normal chest plus the bonus chest when its condition was completed.','Bats Ancient Golden Thief Bug puis récupère le coffre normal ainsi que le coffre bonus si sa condition a été remplie.')
        ],
        mechanics: [
          navLabel('The egg-clearing sequence controls the boss spawn.','La séquence de destruction des œufs contrôle l’apparition du boss.'),
          navLabel('A second egg-clearing condition around the boss determines access to the bonus chest.','Une seconde condition de destruction des œufs autour du boss détermine l’accès au coffre bonus.'),
          navLabel('Equipment rewards increase when the party has 7 or more members.','Les récompenses d’équipement augmentent lorsque le groupe compte 7 membres ou plus.'),
          navLabel('Normal and Hard modes use different reward pools and quantities.','Les modes Normal et Hard utilisent des pools et quantités de récompenses différents.')
        ],
        images: [
          ['https://d33wubrfki0l68.cloudfront.net/9ff892c03fa929822f41914bdbf47af262606300/215d8/images/maps/prontera-culvert-location.bmp', navLabel('Prontera Culvert entrance location','Emplacement de l’entrée de Prontera Culvert')],
          ['https://d33wubrfki0l68.cloudfront.net/44db4f8728a5ffbb886ecd69ac4022383f3ac3c2/c6717/images/monsters/3975-md-ancient-golden-thief-bug.png', 'Ancient Golden Thief Bug']
        ],
        monsters: [
          {name:'Sewer Giant Thief Bug',level:'60',hp:'3,330',def:'40',mdef:'20',class:'Normal',race:'Formless',element:'Shadow Lv.1',size:'Medium',baseExp:'0',jobExp:'0'},
          {name:'Sewer Thief Bug',level:'60',hp:'200',def:'24',mdef:'3',class:'Normal',race:'Insect',element:'Neutral Lv.3',size:'Small',baseExp:'0',jobExp:'0'},
          {name:'Ancient Thief Bug Egg',level:'60',hp:'10',def:'64',mdef:'10',class:'Normal',race:'Insect',element:'Shadow Lv.1',size:'Small',baseExp:'0',jobExp:'0'},
          {name:'Ancient Golden Thief Bug',level:'60',hp:'1,200,000',def:'159',mdef:'81',class:'Boss',race:'Insect',element:'Fire Lv.1',size:'Large',baseExp:'75,000',jobExp:'63,000'}
        ],
        rewardIntro: navLabel('The completion chest contains dungeon crafting materials and Subjugation equipment. Equipment quantities improve with a party of 7 or more members.','Le coffre de fin contient des matériaux de craft de donjon et de l’équipement Subjugation. Les quantités d’équipement augmentent avec un groupe de 7 membres ou plus.'),
        rewardGroups: [
          {title:navLabel('Normal Mode','Mode Normal'),rows:[
            {item:'Shimmering Crystal',qty:'1–3'},
            {item:'Subjugation Ring [1]',qty:'0–2 / 1–3'},
            {item:'Subjugation Boots [1]',qty:'0–2 / 1–3'}
          ]},
          {title:navLabel('Hard Mode','Mode Hard'),rows:[
            {item:'Shimmering Crystal',qty:'6–10'}, {item:'Shiny Opal',qty:'0–3'}, {item:'Mithril Ore',qty:'1–4'},
            {item:'Elunium',qty:'1–3'}, {item:'Oridecon',qty:'1–3'}, {item:'Rough Elunium',qty:'2–8'},
            {item:'Rough Oridecon',qty:'2–8'}, {item:'Wind of Verdure',qty:'1–3'}, {item:'Red Blood',qty:'1–3'}, {item:'Green Live',qty:'1–3'}
          ]}
        ],
        sources: [
          ['Prontera Culvert guide','https://old.criatura-academy.com/memorial-dungeons/prontera-culvert/'],
          ['Memorial Dungeons guide','https://midgardhub.com/guides/memorial-dungeons'],
          ['September 3 update','https://roz.mygnjoy.com/en/news/update/92']
        ]
      }
    };
  }
'''

s = s[:start] + new_block + s[end:]

# Replace the detail renderer with a more complete guide layout.
detail_start = s.index('  function memorialDungeonDetail(id) {')
detail_end = s.index('\n  function statusEffectsPage(topic)', detail_start)

new_detail = r'''  function memorialDungeonCollectDbEntities() {
    const out = {items:{}, monsters:{}};
    Object.values(memorialDungeonData()).forEach(d=>{
      (d.monsters || []).forEach(m=> out.monsters[memorialDbSlug(m.name)] = m.name);
      (d.rewardGroups || []).forEach(g=>(g.rows || []).forEach(r=> out.items[memorialDbSlug(r.item)] = r.item));
      (d.headgear || []).forEach(h=> out.items[memorialDbSlug(h.name)] = h.name);
    });
    return out;
  }

  function memorialDatabaseEntityPage(kind, slug) {
    const entities = memorialDungeonCollectDbEntities();
    const group = kind === 'items' ? entities.items : entities.monsters;
    const name = group[slug];
    if (!name) return kind === 'items' ? itemsOverviewPage() : monstersOverviewPage();
    const title = kind === 'items' ? navLabel('Item Database','Database Objet') : navLabel('Monster Database','Database Monstre');
    const back = kind === 'items' ? '#/items' : '#/monsters';
    return `${breadcrumbs([{label:title,href:back},{label:name}])}
      <div class="article-heading"><h1>${miniIcon(kind === 'items' ? 'item' : 'monster')}${esc(name)}</h1><div class="page-subtitle">${t('fromWiki')}</div></div>
      <div class="notice info"><svg class="notice-icon"><use href="#i-info"></use></svg><div>${navLabel('This entity is already linked from the wiki guides. Its complete database sheet will appear on this same route when the database is populated.','Cette entité est déjà reliée depuis les guides du wiki. Sa fiche complète de database apparaîtra sur cette même route lorsque la database sera remplie.')}</div></div>
      <p><a class="button" href="${back}">${navLabel('Open database','Ouvrir la database')}</a></p>`;
  }

  function memorialDungeonDetail(id) {
    const d = memorialDungeonData()[id];
    if (!d) return notFound();

    const gallery = (d.images || []).length ? `<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;align-items:start;margin:16px 0 24px">${d.images.map(([src,caption])=>`<figure style="margin:0;text-align:center"><div style="min-height:190px;display:flex;align-items:center;justify-content:center;border:1px solid var(--line-soft);background:#f8f9fa;padding:10px"><img src="${esc(src)}" alt="${esc(caption)}" loading="lazy" style="display:block;max-width:100%;max-height:320px;width:auto;height:auto;image-rendering:auto"></div><figcaption style="margin-top:7px;color:var(--muted);font-size:12px">${esc(caption)}</figcaption></figure>`).join('')}</div>` : '';

    const monsterRows = (d.monsters || []).map(m=>`<tr>
      <th>${memorialDbLink('monsters',m.name)}</th><td>${esc(m.level)}</td><td>${esc(m.hp)}</td><td>${esc(m.def)}</td><td>${esc(m.mdef)}</td>
      <td>${esc(m.class)}</td><td>${esc(m.race)}</td><td>${esc(m.element)}</td><td>${esc(m.size)}</td><td>${esc(m.baseExp)}</td><td>${esc(m.jobExp)}</td>
    </tr>`).join('');

    const rewards = (d.rewardGroups || []).map(g=>`<h3>${esc(g.title)}</h3><div class="table-wrap"><table><thead><tr><th>${navLabel('Item','Objet')}</th><th>${navLabel('Quantity / Condition','Quantité / Condition')}</th></tr></thead><tbody>${(g.rows||[]).map(r=>`<tr><th>${memorialDbLink('items',r.item)}</th><td>${esc(r.qty || '—')}</td></tr>`).join('')}</tbody></table></div>`).join('');

    const headgear = (d.headgear || []).length ? `<h2 id="headgear">${navLabel('Headgear rewards','Récompenses Headgear')}</h2>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px">${d.headgear.map(h=>`<div class="panel"><div class="panel-heading">${memorialDbLink('items',h.name)}</div><div class="panel-body"><div class="table-wrap"><table><tbody><tr><th>${navLabel('Slot','Slot')}</th><td>${esc(h.slot)}</td></tr><tr><th>${navLabel('Required level','Niveau requis')}</th><td>${esc(h.level)}</td></tr><tr><th>${navLabel('Weight','Poids')}</th><td>${esc(h.weight)}</td></tr></tbody></table></div><p>${esc(h.effect)}</p></div></div>`).join('')}</div>` : '';

    const enchant = d.enchant ? `<h2 id="enchant">${navLabel('Headgear enchant','Enchantement du Headgear')}</h2>
      <ul><li>${esc(d.enchant.cost)}</li><li>${esc(d.enchant.reset)}</li>${(d.enchant.rules||[]).map(x=>`<li>${esc(x)}</li>`).join('')}</ul>
      <div class="table-wrap"><table><thead><tr><th>${navLabel('Possible enchants','Enchantements possibles')}</th></tr></thead><tbody>${d.enchant.options.map(x=>`<tr><td>${esc(x)}</td></tr>`).join('')}</tbody></table></div>` : '';

    return `${breadcrumbs([{label:navLabel('Memorial Dungeons','Mémorial Donjons'),href:'#/memorial-dungeons'},{label:d.name}])}
      <div class="article-heading"><h1>${icon('memorial')}${esc(d.name)}</h1><div class="page-subtitle">${esc(d.subtitle)}</div></div>

      <div class="wiki-feature-list">
        <div><strong>${navLabel('Level','Niveau')}</strong><p>${esc(d.level)}</p></div>
        <div><strong>${navLabel('Access','Accès')}</strong><p>${esc(d.access)}</p></div>
        <div><strong>${navLabel('Objective','Objectif')}</strong><p>${esc(d.objective)}</p></div>
      </div>

      ${gallery}

      <h2 id="requirements">${navLabel('Requirements & entry','Prérequis et entrée')}</h2>
      <ul>${(d.requirements || []).map(x=>`<li>${esc(x)}</li>`).join('')}</ul>

      <h2 id="walkthrough">${navLabel('Walkthrough','Déroulement')}</h2>
      <ol>${(d.steps || []).map(x=>`<li>${esc(x)}</li>`).join('')}</ol>

      <h2 id="mechanics">${navLabel('Dungeon mechanics','Mécaniques du donjon')}</h2>
      <ul>${(d.mechanics || []).map(x=>`<li>${esc(x)}</li>`).join('')}</ul>

      <h2 id="monsters">${navLabel('Monsters & Bosses','Monstres et Boss')}</h2>
      <p class="page-subtitle">${navLabel('Monster names are internal database links and will open their full sheets when the Monster Database is populated.','Les noms des monstres sont déjà des liens internes vers la database et ouvriront leur fiche complète lorsque la Database Monstre sera remplie.')}</p>
      <div class="table-wrap"><table><thead><tr><th>${navLabel('Monster','Monstre')}</th><th>Lv.</th><th>HP</th><th>DEF</th><th>MDEF</th><th>${navLabel('Class','Classe')}</th><th>${navLabel('Race','Race')}</th><th>${navLabel('Element','Élément')}</th><th>${navLabel('Size','Taille')}</th><th>Base EXP</th><th>Job EXP</th></tr></thead><tbody>${monsterRows}</tbody></table></div>

      <h2 id="rewards">${navLabel('Treasure Chest Rewards','Récompenses du coffre')}</h2>
      <p>${esc(d.rewardIntro || '')}</p>
      ${rewards}
      ${headgear}
      ${enchant}

      ${officialSources(d.sources)}`;
  }
'''

s = s[:detail_start] + new_detail + s[detail_end:]

# Add stable entity routes so guide links are future-proof when the databases are populated.
old_items = "    else if(hash[0]==='items'&&!hash[1]) html=itemsOverviewPage();"
new_items = "    else if(hash[0]==='items'&&hash[1]) html=memorialDatabaseEntityPage('items',hash[1]);\n" + old_items
if "memorialDatabaseEntityPage('items'" not in s:
    assert old_items in s
    s = s.replace(old_items, new_items, 1)

old_monsters = "    else if(hash[0]==='monsters'&&!hash[1]) html=monstersOverviewPage();"
new_monsters = "    else if(hash[0]==='monsters'&&hash[1]) html=memorialDatabaseEntityPage('monsters',hash[1]);\n" + old_monsters
if "memorialDatabaseEntityPage('monsters'" not in s:
    assert old_monsters in s
    s = s.replace(old_monsters, new_monsters, 1)

# Ensure provenance/site names appear only inside Sources arrays for the new memorial guide block.
mem = s[s.index('  function memorialDbSlug'):s.index('\n  function statusEffectsPage', s.index('  function memorialDbSlug'))]
assert 'Croisement des sources' not in mem
assert 'Source cross-check' not in mem
assert 'KRO/Criatura' not in mem
assert 'Référence KRO' not in mem
assert 'memorialDbLink(\'monsters\'' in mem
assert 'memorialDbLink(\'items\'' in mem
assert 'Headgear enchant' in mem
assert 'Walkthrough' in mem
assert "hash[0]==='items'&&hash[1]" in s
assert "hash[0]==='monsters'&&hash[1]" in s

p.write_text(s, encoding='utf-8')
