from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# --- GTB Memorial Dungeon: destroy eggs so the boss does not strengthen, while keeping rewards at step 4.
old_gtb = """        steps: [
          navLabel('Enter the culvert and progress through the instance.','Entre dans les égouts et progresse dans l’instance.'),
          navLabel('Destroy the Ancient Thief Bug Eggs until Ancient Golden Thief Bug appears.','Détruis les Ancient Thief Bug Eggs jusqu’à l’apparition de Ancient Golden Thief Bug.'),
          navLabel('Defeat Ancient Golden Thief Bug.','Bats Ancient Golden Thief Bug.'),
          navLabel('Collect the rewards from the chest before leaving the instance.','Récupère les récompenses dans le coffre avant de sortir de l’instance.')
        ],"""
new_gtb = """        steps: [
          navLabel('Enter the culvert and progress through the instance.','Entre dans les égouts et progresse dans l’instance.'),
          navLabel('Destroy the Ancient Thief Bug Eggs until Ancient Golden Thief Bug appears.','Détruis les Ancient Thief Bug Eggs jusqu’à l’apparition de Ancient Golden Thief Bug.'),
          navLabel('During the boss encounter, destroy the remaining Ancient Thief Bug Eggs so Ancient Golden Thief Bug does not strengthen, then defeat it.','Pendant le combat contre le boss, détruis les Ancient Thief Bug Eggs restants pour empêcher Ancient Golden Thief Bug de se renforcer, puis bats-le.'),
          navLabel('Collect the rewards from the chest before leaving the instance.','Récupère les récompenses dans le coffre avant de sortir de l’instance.')
        ],"""
assert old_gtb in s
s = s.replace(old_gtb, new_gtb, 1)

# Replace the Craft detail renderer with a richer version while keeping legacy fallback pages.
marker = "  function craftingDetailPage(id) {"
assert marker in s
s = s.replace(marker, "  function craftingDetailPageLegacy(id) {", 1)

new_function = r'''
  function craftingDetailPage(id) {
    const back = `<p><a href="#/wiki/crafting">← ${navLabel('Back to Crafting','Retour au Craft')}</a></p>`;
    const itemLink = name => memorialDbLink('items', name);
    const sourceBlock = rows => officialSources(rows);

    if (id === 'arrow-crafting') {
      const recipes = [
        ['Amulet', [['Cursed Arrow',40]]],
        ['Ancient Tooth', [['Steel Arrow',20],['Crystal Arrow',300]]],
        ['Armor Piece of Dullahan', [['Arrow of Shadow',150]]],
        ['Barren Trunk', [['Arrow',20]]],
        ['Battered Kettle', [['Steel Arrow',50]]],
        ['Bee Stinger', [['Rusty Arrow',1]]],
        ['Blade Lost in Darkness', [['Sharp Arrow',600],['Arrow of Shadow',200]]],
        ['Bloody Edge', [['Sharp Arrow',600],['Cursed Arrow',200]]],
        ['Blue Bijou', [['Arrow of Wind',50],['Crystal Arrow',50],['Frozen Arrow',80]]],
        ['Blue Gemstone', [['Crystal Arrow',30],['Frozen Arrow',1]]],
        ['Broken Farming Utensil', [['Rusty Arrow',50],['Iron Arrow',10],['Cursed Arrow',20]]],
        ['Burning Heart', [['Fire Arrow',150]]],
        ['Burning Horseshoe', [['Steel Arrow',100]]],
        ['Burnt Tree', [['Fire Arrow',250]]],
        ['Cactus Needle', [['Arrow',50]]],
        ["Cat's Eye", [['Arrow of Wind',200]]],
        ['Clattering Skull', [['Arrow of Shadow',50],['Cursed Arrow',50]]],
        ['Coal', [['Arrow of Shadow',8]]],
        ['Crystal Blue', [['Crystal Arrow',150]]],
        ['Crystal Fragment', [['Flash Arrow',10],['Sleep Arrow',30]]],
        ['Cursed Ruby', [['Cursed Arrow',50],['Sleep Arrow',10]]],
        ['Cursed Seal', [['Cursed Arrow',50],['Mute Arrow',50]]],
        ['Dark Crystal Fragment', [['Cursed Arrow',30],['Arrow of Shadow',50]]],
        ['Dead Branch', [['Mute Arrow',40]]],
        ['Decayed Nail', [['Rusty Arrow',1],['Arrow of Shadow',1]]],
        ['Destroyed Armor', [['Steel Arrow',150]]],
        ['Dokebi Horn', [['Iron Arrow',40],['Arrow of Shadow',2]]],
        ['Dragon Canine', [['Iron Arrow',50],['Oridecon Arrow',1]]],
        ['Dragon Skin', [['Steel Arrow',10],['Cursed Arrow',50],['Mute Arrow',50]]],
        ['Elunium', [['Steel Arrow',1000],['Stun Arrow',50]]],
        ['Emperium', [['Immaterial Arrow',600],['Mute Arrow',600],['Oridecon Arrow',600]]],
        ['Empty Bottle', [['Iron Arrow',2]]],
        ['Emveretarcon', [['Silver Arrow',40],['Iron Arrow',200]]],
        ['Evil Horn', [['Arrow of Shadow',20],['Flash Arrow',10],['Stun Arrow',5]]],
        ['Fang', [['Silver Arrow',40],['Sharp Arrow',2]]],
        ['Fang of Hatii', [['Crystal Arrow',100]]],
        ['Fin Helm', [['Crystal Arrow',200],['Steel Arrow',200]]],
        ['Fine-grained Trunk', [['Arrow',20]]],
        ['Fire Dragon Scale', [['Fire Arrow',300],['Stun Arrow',300]]],
        ['Flame Heart', [['Fire Arrow',1800],['Mute Arrow',5]]],
        ['Foolishness of Blind', [['Flash Arrow',200]]],
        ['Garlet', [['Iron Arrow',12]]],
        ['Gill', [['Iron Arrow',80],['Crystal Arrow',150]]],
        ['Glacial Heart', [['Crystal Arrow',50],['Frozen Arrow',50]]],
        ['Glittering Jacket', [['Flash Arrow',1000]]],
        ['Gold', [['Oridecon Arrow',50],['Flash Arrow',50]]],
        ['Golden Ornament', [['Silver Arrow',200],['Holy Arrow',300]]],
        ['Green Bijou', [['Stone Arrow',100],['Poison Arrow',80]]],
        ['Great Nature', [['Stone Arrow',450],['Flash Arrow',5]]],
        ['Green Live', [['Stone Arrow',150]]],
        ['Hard Feeler', [['Sharp Arrow',20]]],
        ['Heroic Emblem', [['Stun Arrow',5],['Oridecon Arrow',1]]],
        ['Horn', [['Iron Arrow',35]]],
        ['Horrendous Mouth', [['Arrow of Shadow',5]]],
        ['Ice Cubic', [['Crystal Arrow',100]]],
        ['Ice Scale', [['Crystal Arrow',150],['Frozen Arrow',400],['Mute Arrow',200]]],
        ['Insect Leg', [['Sharp Arrow',10],['Poison Arrow',80]]],
        ['Iron', [['Iron Arrow',100]]],
        ['Iron Ore', [['Iron Arrow',50]]],
        ['Jellopy', [['Arrow',4]]],
        ['Key of the Clock Tower', [['Oridecon Arrow',50]]],
        ['Lantern', [['Iron Arrow',80]]],
        ['Leopard Claw', [['Sharp Arrow',10]]],
        ['Little Evil Horn', [['Iron Arrow',50],['Cursed Arrow',2]]],
        ['Live Coal', [['Fire Arrow',100]]],
        ["Loki's Whispers", [['Arrow of Shadow',1000]]],
        ["Lucifer's Lament", [['Stun Arrow',800],['Mute Arrow',400],['Sleep Arrow',800]]],
        ['Manacles', [['Steel Arrow',50]]],
        ['Mantis Scythe', [['Sharp Arrow',1]]],
        ['Matchstick', [['Fire Arrow',3000]]],
        ["Matyr's Leash", [['Arrow of Wind',50],['Steel Arrow',100],['Sharp Arrow',10]]],
        ['Mole Claw', [['Iron Arrow',50],['Stone Arrow',60]]],
        ["Mother's Nightmare", [['Cursed Arrow',1000]]],
        ['Mr. Scream', [['Sharp Arrow',200],['Steel Arrow',300]]],
        ['Mystic Frozen', [['Crystal Arrow',450],['Frozen Arrow',5]]],
        ['Needle of Alarm', [['Arrow',100],['Sleep Arrow',5]]],
        ['Ogre Tooth', [['Steel Arrow',30],['Rusty Arrow',5]]],
        ['Old Blue Box', [['Sharp Arrow',50],['Sleep Arrow',50]]],
        ['Old Hilt', [['Oridecon Arrow',1000]]],
        ['Old Pick', [['Rusty Arrow',100],['Steel Arrow',50]]],
        ['Orc Claw', [['Steel Arrow',10]]],
        ["Orc's Fang", [['Iron Arrow',30],['Steel Arrow',5],['Stone Arrow',10]]],
        ['Oridecon', [['Oridecon Arrow',250]]],
        ['Opera Masque', [['Steel Arrow',200],['Mute Arrow',40]]],
        ['Phracon', [['Iron Arrow',50]]],
        ['Piece of Bamboo', [['Arrow',100]]],
        ['Piece of Shield', [['Steel Arrow',100],['Oridecon Arrow',100],['Immaterial Arrow',300]]],
        ['Poisonous Toad Skin', [['Poison Arrow',20]]],
        ['Porcupine Quill', [['Arrow',70],['Stone Arrow',30]]],
        ['Red Bijou', [['Fire Arrow',100],['Flash Arrow',80]]],
        ['Red Blood', [['Fire Arrow',600]]],
        ['Red Gemstone', [['Rusty Arrow',10],['Poison Arrow',1],['Cursed Arrow',1]]],
        ['Reins', [['Iron Arrow',100],['Steel Arrow',50]]],
        ['Rough Elunium', [['Steel Arrow',200],['Stun Arrow',5]]],
        ['Rough Oridecon', [['Oridecon Arrow',50]]],
        ['Rough Wind', [['Arrow of Wind',450],['Sleep Arrow',5]]],
        ['Rune of the Darkness', [['Arrow of Shadow',300],['Flash Arrow',150]]],
        ['Scell', [['Steel Arrow',8]]],
        ['Scorpion Tail', [['Rusty Arrow',3]]],
        ['Shackles', [['Iron Arrow',700],['Steel Arrow',50]]],
        ['Sharp Leaf', [['Sharp Arrow',30]]],
        ['Shining Spear Blade', [['Oridecon Arrow',100]]],
        ['Silver Robe', [['Silver Arrow',700]]],
        ['Silver Robe [1]', [['Silver Arrow',1000],['Immaterial Arrow',10]]],
        ['Skeletal Armor Piece', [['Immaterial Arrow',500],['Arrow of Shadow',200],['Oridecon Arrow',100]]],
        ['Solid Peach', [['Stun Arrow',30]]],
        ['Solid Trunk', [['Arrow',20]]],
        ['Star Crumb', [['Flash Arrow',30]]],
        ['Star Dust', [['Flash Arrow',10]]],
        ['Steel', [['Steel Arrow',100]]],
        ['Stinky Scale', [['Poison Arrow',1]]],
        ['Stone Fragment', [['Stone Arrow',50],['Stun Arrow',30]]],
        ['Tooth of Bat', [['Arrow of Shadow',1]]],
        ['Tangled Chains', [['Steel Arrow',50],['Arrow of Shadow',50]]],
        ['Tree Root', [['Arrow',7]]],
        ['Trunk', [['Arrow',40]]],
        ['Key of Underground', [['Arrow of Shadow',100]]],
        ['Unicorn Horn', [['Silver Arrow',1000]]],
        ['Used Iron Plate', [['Steel Arrow',100],['Rusty Arrow',100]]],
        ["Valhala's Flower", [['Immaterial Arrow',600],['Holy Arrow',600],['Sharp Arrow',600]]],
        ['Venom Canine', [['Poison Arrow',1]]],
        ['Welding Mask', [['Steel Arrow',200],['Stun Arrow',40]]],
        ['Will of the Darkness', [['Cursed Arrow',30],['Poison Arrow',30],['Arrow of Shadow',50]]],
        ['Will of the Red Darkness', [['Cursed Arrow',200],['Poison Arrow',200],['Arrow of Shadow',100]]],
        ['Wind of Verdure', [['Arrow of Wind',150]]],
        ['Wolf Claw', [['Iron Arrow',15]]],
        ['Wooden Mail', [['Arrow',700],['Iron Arrow',500]]],
        ['Wooden Mail [1]', [['Arrow',1000],['Iron Arrow',700]]],
        ['Yellow Bijou', [['Silver Arrow',50],['Immaterial Arrow',50],['Sleep Arrow',80]]],
        ['Yellow Gemstone', [['Stone Arrow',10],['Sleep Arrow',1]]],
        ['Young Twig', [['Mute Arrow',1000]]],
        ['Zargon', [['Silver Arrow',40]]],
        ["Zenorc's Fang", [['Rusty Arrow',5]]]
      ];
      const rows = recipes.map(([material,outputs])=>`<tr><th>${itemLink(material)}</th><td>${outputs.map(([name,qty])=>`${qty.toLocaleString(lang==='fr'?'fr-FR':'en-US')} × ${itemLink(name)}`).join('<br>')}</td></tr>`).join('');
      return `${breadcrumbs([{label:navLabel('Crafting','Craft'),href:'#/wiki/crafting'},{label:'Arrow Crafting'}])}
        <div class="article-heading"><h1>${icon('item')}Arrow Crafting</h1><div class="page-subtitle">${t('fromWiki')}</div></div>
        <p class="article-lead">${navLabel('Arrow Crafting is an Archer quest skill that converts compatible materials into arrows.','Arrow Crafting est un skill de quête Archer qui transforme des matériaux compatibles en flèches.')}</p>
        <div class="wiki-feature-list">
          <div><strong>${navLabel('Class','Classe')}</strong><p><a href="#/classes/archer">Archer</a></p></div>
          <div><strong>${navLabel('Skill level','Niveau du skill')}</strong><p>Lv. 1</p></div>
          <div><strong>SP</strong><p>10</p></div>
          <div><strong>${navLabel('Weight restriction','Restriction de poids')}</strong><p>${navLabel('Cannot be used at 50% weight or more.','Ne peut pas être utilisé à 50 % de poids ou plus.')}</p></div>
        </div>
        <h2 id="materials">${navLabel('Usable materials','Matériaux utilisables')}</h2>
        <div class="table-wrap"><table><thead><tr><th>${navLabel('Source material','Matériau source')}</th><th>${navLabel('Arrows created','Flèches créées')}</th></tr></thead><tbody>${rows}</tbody></table></div>
        ${sourceBlock([['iRO Wiki — Arrow Crafting','https://irowiki.org/wiki/Arrow_Crafting']])}
        ${back}`;
    }

    if (id === 'potion-creation') {
      const recipes = [
        ['Red Potion','Potion Creation Guide',['1 Empty Potion Bottle','1 Red Herb']],
        ['Yellow Potion','Potion Creation Guide',['1 Empty Potion Bottle','1 Yellow Herb']],
        ['White Potion','Potion Creation Guide',['1 Empty Potion Bottle','1 White Herb']],
        ['Blue Potion','Potion Creation Guide',['1 Empty Potion Bottle','1 Blue Herb','1 Scell']],
        ['Anodyne','Potion Creation Guide',['1 Empty Bottle','1 Alcohol','1 Ment']],
        ['Aloevera','Potion Creation Guide',['1 Honey','1 Aloe']],
        ['Embryo','Potion Creation Guide',['1 Morning Dew of Yggdrasil','1 Seed of Life','1 Glass Tube']],
        ['Homunculus Tablet','Potion Creation Guide',['1 Yellow Herb','1 Seed of Life','1 Empty Bottle']],
        ['Condensed Red Potion','Condensed Potion Creation Guide',['1 Empty Test Tube','1 Red Potion','1 Cactus Needle']],
        ['Condensed Yellow Potion','Condensed Potion Creation Guide',['1 Empty Test Tube','1 Yellow Potion','1 Mole Whiskers']],
        ['Condensed White Potion','Condensed Potion Creation Guide',['1 Empty Test Tube','1 White Potion','1 Witch Starsand']],
        ['Alcohol','Alcohol Creation Guide',['1 Empty Test Tube','1 Empty Bottle','5 Stem','5 Poison Spore']],
        ['Bottle Grenade','Bottle Grenade Creation Guide',['1 Empty Bottle','1 Fabric','1 Alcohol']],
        ['Acid Bottle','Acid Bottle Creation Guide',['1 Empty Bottle','1 Immortal Heart']],
        ['Glistening Coat','Glistening Coat Creation Guide',['1 Empty Bottle',"1 Mermaid's Heart","1 Zenorc's Fang",'1 Alcohol']],
        ['Marine Sphere Bottle','Marine Sphere Creation Guide',['1 Empty Bottle','1 Tendon','1 Detonator']],
        ['Plant Bottle','Plant Bottle Creation Guide',['1 Empty Bottle','2 Maneater Blossom']],
        ['Coldproof Potion','Elemental Potion Creation Guide',['1 Empty Potion Bottle','1 Blue Gemstone',"3 Mermaid's Heart"]],
        ['Thunderproof Potion','Elemental Potion Creation Guide',['1 Empty Potion Bottle','1 Blue Gemstone','3 Moth Dust']],
        ['Earthproof Potion','Elemental Potion Creation Guide',['1 Empty Potion Bottle','1 Yellow Gemstone','2 Large Jellopy']],
        ['Fireproof Potion','Elemental Potion Creation Guide',['1 Empty Potion Bottle','1 Red Gemstone','2 Frill']]
      ];
      const matHtml = list => list.map(entry=>{
        const m = entry.match(/^(\d+)\s+(.+)$/);
        return m ? `${m[1]} × ${itemLink(m[2])}` : itemLink(entry);
      }).join('<br>');
      const rows = recipes.map(([product,guide,mats])=>`<tr><th>${itemLink(product)}</th><td>${itemLink(guide)}</td><td>${matHtml(mats)}</td></tr>`).join('');
      return `${breadcrumbs([{label:navLabel('Crafting','Craft'),href:'#/wiki/crafting'},{label:'Potion Creation'}])}
        <div class="article-heading"><h1>${icon('item')}Potion Creation</h1><div class="page-subtitle">${t('fromWiki')}</div></div>
        <p class="article-lead">${navLabel('Potion Creation uses Prepare Potion together with the appropriate creation manual and ingredients.','Potion Creation utilise Prepare Potion avec le manuel de création correspondant et les ingrédients nécessaires.')}</p>
        <div class="wiki-feature-list">
          <div><strong>${navLabel('Class','Classe')}</strong><p><a href="#/classes/alchemist">Alchemist</a></p></div>
          <div><strong>${navLabel('Main skill','Skill principal')}</strong><p>Prepare Potion</p></div>
          <div><strong>${navLabel('Catalyst','Catalyseur')}</strong><p>${itemLink('Medicine Bowl')}</p></div>
          <div><strong>${navLabel('Manual','Manuel')}</strong><p>${navLabel('Depends on the recipe.','Dépend de la recette.')}</p></div>
        </div>
        <h2 id="recipes">${navLabel('Potion recipes','Recettes de potions')}</h2>
        <div class="table-wrap"><table><thead><tr><th>${navLabel('Result','Résultat')}</th><th>${navLabel('Creation guide','Manuel')}</th><th>${navLabel('Materials','Matériaux')}</th></tr></thead><tbody>${rows}</tbody></table></div>
        <div class="notice info"><svg class="notice-icon"><use href="#i-info"></use></svg><div>${navLabel('Each Prepare Potion attempt also uses one Medicine Bowl as its catalyst.','Chaque tentative de Prepare Potion utilise également un Medicine Bowl comme catalyseur.')}</div></div>
        ${sourceBlock([['iRO Wiki — Potion Creation','https://irowiki.org/wiki/Potion_Creation']])}
        ${back}`;
    }

    if (id === 'blacksmith-forging') {
      const groups = [
        ['Dagger','Smith Dagger',[
          [1,'Knife',['1 Iron','10 Jellopy']], [1,'Cutter',['25 Iron']], [1,'Main Gauche',['50 Iron']],
          [2,'Dirk',['17 Steel']], [2,'Dagger',['30 Steel']], [2,'Stiletto',['40 Steel']],
          [3,'Gladius',['4 Oridecon','40 Steel','1 Sapphire']], [3,'Damascus',['4 Oridecon','60 Steel','1 Zircon']]
        ]],
        ['Sword','Smith Sword',[
          [1,'Sword',['2 Iron']], [1,'Falchion',['30 Iron']], [1,'Blade',['45 Iron','25 Tooth of Bat']],
          [2,'Rapier',['20 Steel']], [2,'Scimiter',['35 Steel']], [2,'Ring Pommel Saber',['40 Steel','50 Wolf Claw']],
          [3,'Saber',['8 Oridecon','5 Steel','1 Opal']], [3,'Haedonggum',['8 Oridecon','10 Steel','1 Topaz']],
          [3,'Tsurugi',['8 Oridecon','15 Steel','1 Garnet']], [3,'Flamberge',['16 Oridecon','1 Cursed Ruby']]
        ]],
        ['Two-Handed Sword','Smith Two-handed Sword',[
          [1,'Katana',['35 Iron','15 Horrendous Mouth']], [2,'Slayer',['24 Steel','20 Decayed Nail']], [2,'Bastard Sword',['45 Steel']],
          [3,'Two Handed Sword',['12 Oridecon','10 Steel']], [3,'Broad Sword',['12 Oridecon','20 Steel']], [3,'Claymore',['16 Oridecon','20 Steel','1 Cracked Diamond']]
        ]],
        ['Axe','Smith Axe',[
          [1,'Axe',['10 Iron']], [1,'Battle Axe',['110 Iron']], [2,'Hammer',['30 Steel']],
          [3,'Buster',['4 Oridecon','20 Steel','30 Orc Fang']], [3,'Two-Handed Axe',['8 Oridecon','20 Steel','1 Amethyst']]
        ]],
        ['Mace','Smith Mace',[
          [1,'Club',['3 Iron']], [1,'Mace',['30 Iron']], [2,'Smasher',['20 Steel']], [2,'Flail',['33 Steel']], [2,'Chain',['45 Steel']],
          [3,'Morning Star',['85 Steel','1 1 Carat Diamond']], [3,'Sword Mace',['100 Steel','20 Sharp Scale']], [3,'Stunner',['120 Steel','1 Heroic Emblem']]
        ]],
        ['Spear','Smith Spear',[
          [1,'Javelin',['3 Iron']], [1,'Spear',['35 Iron']], [1,'Pike',['70 Iron']],
          [2,'Guisarme',['25 Steel']], [2,'Glaive',['40 Steel']], [2,'Partizan',['55 Steel']],
          [3,'Trident',['8 Oridecon','10 Steel','5 Aquamarine']], [3,'Hallberd',['12 Oridecon','10 Steel']],
          [3,'Lance',['12 Oridecon','3 Ruby','2 Evil Horn']]
        ]],
        ['Knuckle','Smith Knucklebrace',[
          [1,'Waghnak',['160 Iron','1 Pearl']], [2,'Knuckle Dusters',['50 Steel']], [2,'Studded Knuckles',['65 Steel']],
          [3,'Fist',['4 Oridecon','10 Ruby']], [3,'Finger',['4 Oridecon','10 Opal']], [3,'Claw',['8 Oridecon','10 Topaz']]
        ]]
      ];
      const matHtml = list => list.map(entry=>{
        const m = entry.match(/^(\d+)\s+(.+)$/);
        return m ? `${m[1]} × ${itemLink(m[2])}` : itemLink(entry);
      }).join('<br>');
      const sections = groups.map(([type,skill,rows])=>`<h2 id="forge-${type.toLowerCase().replace(/[^a-z]+/g,'-')}">${esc(type)}</h2>
        <p><strong>${navLabel('Forging skill','Skill de forge')}:</strong> ${esc(skill)}</p>
        <div class="table-wrap"><table><thead><tr><th>${navLabel('Skill Lv.','Niveau skill')}</th><th>${navLabel('Weapon','Arme')}</th><th>${navLabel('Materials','Matériaux')}</th></tr></thead><tbody>${rows.map(([lv,weapon,mats])=>`<tr><td>${lv}</td><th>${itemLink(weapon)}</th><td>${matHtml(mats)}</td></tr>`).join('')}</tbody></table></div>`).join('');
      return `${breadcrumbs([{label:navLabel('Crafting','Craft'),href:'#/wiki/crafting'},{label:'Blacksmith Forging'}])}
        <div class="article-heading"><h1>${icon('item')}Blacksmith Forging</h1><div class="page-subtitle">${t('fromWiki')}</div></div>
        <p class="article-lead">${navLabel('Blacksmith forging creates weapons by combining the appropriate forging skill, an anvil, a forging hammer and the listed weapon materials.','La forge du Blacksmith permet de créer des armes avec le skill de forge correspondant, une enclume, un marteau de forge et les matériaux indiqués.')}</p>
        <div class="wiki-feature-list">
          <div><strong>${navLabel('Class','Classe')}</strong><p><a href="#/classes/blacksmith">Blacksmith</a></p></div>
          <div><strong>${navLabel('Required item','Objet requis')}</strong><p>${itemLink('Anvil')}</p></div>
          <div><strong>${navLabel('Catalyst','Catalyseur')}</strong><p>${navLabel('Forging hammer + weapon materials','Marteau de forge + matériaux de l’arme')}</p></div>
          <div><strong>${navLabel('Skill levels','Niveaux')}</strong><p>1–3</p></div>
        </div>
        ${sections}
        ${sourceBlock([
          ['iRO Wiki — Smith Axe','https://irowiki.org/wiki/Smith_Axe'],
          ['iRO Wiki — Smith Dagger','https://irowiki.org/wiki/Smith_Dagger'],
          ['iRO Wiki — Smith Knucklebrace','https://irowiki.org/wiki/Smith_Knucklebrace'],
          ['iRO Wiki — Smith Mace','https://irowiki.org/wiki/Smith_Mace'],
          ['iRO Wiki — Smith Spear','https://irowiki.org/wiki/Smith_Spear'],
          ['iRO Wiki — Smith Sword','https://irowiki.org/wiki/Smith_Sword'],
          ['iRO Wiki — Smith Two-handed Sword','https://irowiki.org/wiki/Smith_Two-handed_Sword']
        ])}
        ${back}`;
    }

    return craftingDetailPageLegacy(id);
  }

'''

insert_at = s.index("  function craftingDetailPageLegacy(id) {")
s = s[:insert_at] + new_function + s[insert_at:]

# Validation
assert "destroy the remaining Ancient Thief Bug Eggs so Ancient Golden Thief Bug does not strengthen" in s
assert "function craftingDetailPageLegacy(id)" in s
assert "function craftingDetailPage(id)" in s
assert "Arrow Crafting" in s and "List of usable materials" not in new_function
assert "['Amulet', [['Cursed Arrow',40]]]" in s
assert "['Young Twig', [['Mute Arrow',1000]]]" in s
assert "Potion Creation Guide" in s
assert "Condensed White Potion" in s
assert "Coldproof Potion" in s
assert "Blacksmith Forging" in s
for weapon in ['Damascus','Flamberge','Claymore','Two-Handed Axe','Stunner','Lance','Claw']:
    assert weapon in s, weapon
assert "return craftingDetailPageLegacy(id);" in s

p.write_text(s, encoding='utf-8')
