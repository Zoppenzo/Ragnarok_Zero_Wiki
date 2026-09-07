from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
start = s.index('  function enchantmentPage(topic) {')
end = s.index('\n  function ', start + 10)
f = s[start:end]

# 1) Keep official enchant-system names in English and merge Job Essence into Memorial Dungeon Enchant.
f = f.replace('        <input class="enchant-tab-input" type="radio" name="enchant-tabs" id="enchant-tab-essences">\n', '')
f = f.replace('          <label for="enchant-tab-costume">${navLabel(\'Costumes\',\'Costumes\')}</label>', '          <label for="enchant-tab-costume">Costume Enchant</label>')
f = f.replace('          <label for="enchant-tab-poring">Poring Village</label>', '          <label for="enchant-tab-poring">Poring Village Enchant</label>')
f = f.replace('          <label for="enchant-tab-memorial">${navLabel(\'Memorial Equipment\',\'Équipement mémorial\')}</label>', '          <label for="enchant-tab-memorial">Memorial Dungeon Enchant</label>')
f = f.replace('          <label for="enchant-tab-essences">${navLabel(\'Job Essences\',\'Essences de classe\')}</label>\n', '')

mem_start = f.index('          <section class="enchant-tab-panel" id="enchant-panel-memorial">')
ess_start = f.index('          <section class="enchant-tab-panel" id="enchant-panel-essences">')
tam_start = f.index('          <section class="enchant-tab-panel" id="enchant-panel-taming">')
mem_block = f[mem_start:ess_start]
ess_block = f[ess_start:tam_start]
mem_close = mem_block.rfind('</section>')
assert mem_close != -1
ess_open_end = ess_block.index('>') + 1
ess_close = ess_block.rfind('</section>')
ess_inner = ess_block[ess_open_end:ess_close]
ess_inner = ess_inner.replace('<h2 id="job-essences">${navLabel(\'Job Essence enchantments\',\'Enchantements Essences de classe\')}</h2>', '<h2 id="job-essence">Job Essence</h2>')
ess_inner = ess_inner.replace("['essence-rules',navLabel('Requirements / rules','Prérequis / règles')],['essence-first',navLabel('1st Job Essences','Essences classe 1')],['essence-second',navLabel('2nd Job Essences','Essences classe 2')]", "['essence-rules','Job Essence rules'],['essence-first','1st Job Essence'],['essence-second','2nd Job Essence']")
ess_inner = ess_inner.replace("${navLabel('First Job Essences','Essences de classe 1')}", '1st Job Essence')
ess_inner = ess_inner.replace("${navLabel('Second Job Essences — Essence I and Essence II','Essences de classe 2 — Essence I et Essence II')}", '2nd Job Essence — Essence I / Essence II')
merged_mem = mem_block[:mem_close] + '\n' + ess_inner + '\n          ' + mem_block[mem_close:]
f = f[:mem_start] + merged_mem + f[tam_start:]

# 2) Verified Job Essence names + effects. Names stay in English and are clickable.
new_data = r'''    const firstEssences = [
      {job:'Mage', names:["Mage's Essence Lv.1","Mage's Essence Lv.2"], lv1:fx('Cold Bolt, Fire Bolt and Lightning Bolt damage +20%. Every 2 Fire Wall levels: Variable Cast Time -1%.','Dégâts de Cold Bolt, Fire Bolt et Lightning Bolt +20 %. Tous les 2 niveaux de Fire Wall : Variable Cast Time -1 %.'), lv2:fx('Cold Bolt, Fire Bolt and Lightning Bolt damage +20%. Every Fire Wall level: Variable Cast Time -1%. Every 2 armor refines: Max SP +50.','Dégâts de Cold Bolt, Fire Bolt et Lightning Bolt +20 %. Par niveau de Fire Wall : Variable Cast Time -1 %. Tous les 2 raffinages de l’armure : Max SP +50.')},
      {job:'Acolyte', names:["Acolyte's Essence Lv.1","Acolyte's Essence Lv.2"], lv1:fx('Heal, Increase Agility and Blessing SP cost -15%. Every 2 Heal levels: healing +1%.','Coût en SP de Heal, Increase Agility et Blessing -15 %. Tous les 2 niveaux de Heal : soins +1 %.'), lv2:fx('Heal, Increase Agility and Blessing SP cost -15%. Every Heal level: healing +1%. Every 2 armor refines: Max HP +70 and Max SP +30.','Coût en SP de Heal, Increase Agility et Blessing -15 %. Par niveau de Heal : soins +1 %. Tous les 2 raffinages : Max HP +70 et Max SP +30.')},
      {job:'Archer', names:["Archer's Essence Lv.1","Archer's Essence Lv.2"], lv1:fx('Double Strafe SP cost -5. Every Vulture\'s Eye level: Bow damage +1%.','Coût en SP de Double Strafe -5. Par niveau de Vulture\'s Eye : dégâts à l’arc +1 %.'), lv2:fx('Double Strafe SP cost -5. Every Vulture\'s Eye level: Bow damage +2%. Every 2 armor refines: Arrow Shower damage +5%.','Coût en SP de Double Strafe -5. Par niveau de Vulture\'s Eye : dégâts à l’arc +2 %. Tous les 2 raffinages : dégâts d’Arrow Shower +5 %.')},
      {job:'Swordsman', names:["Swordsman's Essence Lv.1","Swordsman's Essence Lv.2"], lv1:fx('Magnum Break SP cost -10. Every 2 Bash levels: After Attack Delay -1%.','Coût en SP de Magnum Break -10. Tous les 2 niveaux de Bash : After Attack Delay -1 %.'), lv2:fx('Magnum Break SP cost -10. Every Bash level: After Attack Delay -1%. Every 2 armor refines: Magnum Break damage +15%.','Coût en SP de Magnum Break -10. Par niveau de Bash : After Attack Delay -1 %. Tous les 2 raffinages : dégâts de Magnum Break +15 %.')},
      {job:'Thief', names:["Thief's Essence Lv.1","Thief's Essence Lv.2"], lv1:fx('When worn by a Thief: ATK +30. Every 2 Steal levels: After Attack Delay -1%.','Porté par un Thief : ATK +30. Tous les 2 niveaux de Steal : After Attack Delay -1 %.'), lv2:fx('When worn by a Thief: ATK +30. Every Steal level: After Attack Delay -1%. Every 2 armor refines: FLEE +10.','Porté par un Thief : ATK +30. Par niveau de Steal : After Attack Delay -1 %. Tous les 2 raffinages : FLEE +10.')},
      {job:'Merchant', names:["Merchant's Essence Lv.1","Merchant's Essence Lv.2"], lv1:fx('ATK +2 per Discount level. Every 2 Overcharge levels: After Attack Delay -1%.','ATK +2 par niveau de Discount. Tous les 2 niveaux d’Overcharge : After Attack Delay -1 %.'), lv2:fx('ATK +2 per Discount level. Every Overcharge level: After Attack Delay -1%. Every 2 armor refines: Max HP +100.','ATK +2 par niveau de Discount. Par niveau d’Overcharge : After Attack Delay -1 %. Tous les 2 raffinages : Max HP +100.')}
    ];

    const secondEssences = [
      {job:'Knight', names:["Knight's Essence Lv.1","Knight's Essence Lv.2","Knight's Essence II Lv.1","Knight's Essence II Lv.2"], i1:fx('CRIT +3 per Cavalry Mastery level. Bowling Bash damage +20%. After Attack Delay -1% per armor refine.','CRIT +3 par niveau de Cavalry Mastery. Dégâts de Bowling Bash +20 %. After Attack Delay -1 % par raffinage.'), i2:fx('CRIT +5 per Cavalry Mastery level. Bowling Bash damage +20%. When worn by a Swordsman: Critical Damage +7%. After Attack Delay -1% per armor refine.','CRIT +5 par niveau de Cavalry Mastery. Dégâts de Bowling Bash +20 %. Porté par un Swordsman : Critical Damage +7 %. After Attack Delay -1 % par raffinage.'), ii1:fx('HIT +1 per Spear Mastery level. Pierce damage +20%. ATK +2 per armor refine.','HIT +1 par niveau de Spear Mastery. Dégâts de Pierce +20 %. ATK +2 par raffinage.'), ii2:fx('HIT +2 per Spear Mastery level. Pierce damage +20% and Brandish Spear damage +40%. ATK +2 per armor refine.','HIT +2 par niveau de Spear Mastery. Dégâts de Pierce +20 % et Brandish Spear +40 %. ATK +2 par raffinage.')},
      {job:'Blacksmith', names:["Blacksmith's Essence Lv.1","Blacksmith's Essence Lv.2","Blacksmith's Essence II Lv.1","Blacksmith's Essence II Lv.2"], i1:fx('When worn by a Merchant: CRIT +10. CRIT increases every 3 Maximize Power levels. After Attack Delay -1% per armor refine.','Porté par un Merchant : CRIT +10. CRIT augmente tous les 3 niveaux de Maximize Power. After Attack Delay -1 % par raffinage.'), i2:fx('When worn by a Merchant: CRIT +10. CRIT +5 per Maximize Power level. Critical Damage +1% per Weaponry Research level. After Attack Delay -1% per armor refine.','Porté par un Merchant : CRIT +10. CRIT +5 par niveau de Maximize Power. Critical Damage +1 % par niveau de Weaponry Research. After Attack Delay -1 % par raffinage.'), ii1:fx('LUK +1 per Skin Tempering level. DEX +10. Every 2 armor refines: LUK +1.','LUK +1 par niveau de Skin Tempering. DEX +10. Tous les 2 raffinages : LUK +1.'), ii2:fx('LUK +2 per Skin Tempering level. DEX +10. When worn by a Merchant: DEX +10 and LUK +10. Every 2 armor refines: LUK +1.','LUK +2 par niveau de Skin Tempering. DEX +10. Porté par un Merchant : DEX +10 et LUK +10. Tous les 2 raffinages : LUK +1.')},
      {job:'Assassin', names:['Assassin Essence Lv.1','Assassin Essence Lv.2','Assassin Essence II Lv.1','Assassin Essence II Lv.2'], i1:fx('CRIT +3 per Grimtooth level. Sonic Blow damage +20%. Critical Damage +1% per armor refine.','CRIT +3 par niveau de Grimtooth. Dégâts de Sonic Blow +20 %. Critical Damage +1 % par raffinage.'), i2:fx('CRIT +5 per Grimtooth level. Sonic Blow damage +20%. When worn by a Thief: After Attack Delay -7%. Critical Damage +1% per armor refine.','CRIT +5 par niveau de Grimtooth. Dégâts de Sonic Blow +20 %. Porté par un Thief : After Attack Delay -7 %. Critical Damage +1 % par raffinage.'), ii1:fx('FLEE +3 per Lefthand Mastery level. Venom Splasher damage +20%. Every 2 armor refines: Variable Cast Time -3%.','FLEE +3 par niveau de Lefthand Mastery. Dégâts de Venom Splasher +20 %. Tous les 2 raffinages : Variable Cast Time -3 %.'), ii2:fx('FLEE +5 per Lefthand Mastery level. Venom Splasher damage +40%. Every 2 armor refines: Variable Cast Time -3%.','FLEE +5 par niveau de Lefthand Mastery. Dégâts de Venom Splasher +40 %. Tous les 2 raffinages : Variable Cast Time -3 %.')},
      {job:'Wizard', names:['Wizard Essence Lv.1','Wizard Essence Lv.2','Wizard Essence II Lv.1','Wizard Essence II Lv.2'], i1:fx('Variable Cast Time reduction increases by 3 times the Heaven\'s Drive level. Meteor Storm, Lord of Vermilion and Storm Gust damage +20%. Every 2 armor refines: MATK +1%.','Réduction de Variable Cast Time augmentée de 3 fois le niveau de Heaven\'s Drive. Dégâts de Meteor Storm, Lord of Vermilion et Storm Gust +20 %. Tous les 2 raffinages : MATK +1 %.'), i2:fx('Variable Cast Time reduction increases by 5 times the Heaven\'s Drive level. Meteor Storm, Lord of Vermilion and Storm Gust damage +20%. When worn by a Mage: FLEE +30. Every 2 armor refines: MATK +1%.','Réduction de Variable Cast Time augmentée de 5 fois le niveau de Heaven\'s Drive. Dégâts de Meteor Storm, Lord of Vermilion et Storm Gust +20 %. Porté par un Mage : FLEE +30. Tous les 2 raffinages : MATK +1 %.'), ii1:fx('Variable Cast Time reduction increases by 2 times the Lord of Vermilion level. Jupitel Thunder damage +20%. MATK +2 per armor refine.','Réduction de Variable Cast Time augmentée de 2 fois le niveau de Lord of Vermilion. Dégâts de Jupitel Thunder +20 %. MATK +2 par raffinage.'), ii2:fx('Variable Cast Time reduction increases by 3 times the Lord of Vermilion level. Jupitel Thunder damage +40%. MATK +2 per armor refine.','Réduction de Variable Cast Time augmentée de 3 fois le niveau de Lord of Vermilion. Dégâts de Jupitel Thunder +40 %. MATK +2 par raffinage.')},
      {job:'Priest', names:['Priest Essence Lv.1','Priest Essence Lv.2','Priest Essence II Lv.1','Priest Essence II Lv.2'], i1:fx('Variable Cast Time reduction increases by 3 times the Magnificat level. Magnus Exorcismus damage +20%. Every 2 armor refines: Magnus Exorcismus damage +5%.','Réduction de Variable Cast Time augmentée de 3 fois le niveau de Magnificat. Dégâts de Magnus Exorcismus +20 %. Tous les 2 raffinages : dégâts de Magnus Exorcismus +5 %.'), i2:fx('Variable Cast Time reduction increases by 5 times the Magnificat level. Magnus Exorcismus damage +20%. When worn by an Acolyte: MATK +7% and healing +15%. Every 2 armor refines: Magnus Exorcismus damage +5%.','Réduction de Variable Cast Time augmentée de 5 fois le niveau de Magnificat. Dégâts de Magnus Exorcismus +20 %. Porté par un Acolyte : MATK +7 % et soins +15 %. Tous les 2 raffinages : dégâts de Magnus Exorcismus +5 %.'), ii1:fx('ATK +3 per Mace Mastery level. Critical Damage +15%. ATK +2 per armor refine.','ATK +3 par niveau de Mace Mastery. Critical Damage +15 %. ATK +2 par raffinage.'), ii2:fx('ATK +5 per Mace Mastery level. Critical Damage +15%. When worn by an Acolyte, normal melee attacks have a high chance to trigger Bash Lv.10. ATK +2 per armor refine.','ATK +5 par niveau de Mace Mastery. Critical Damage +15 %. Porté par un Acolyte, les attaques normales au corps-à-corps ont une forte chance de déclencher Bash Lv.10. ATK +2 par raffinage.')},
      {job:'Hunter', names:['Hunter Essence Lv.1','Hunter Essence Lv.2','Hunter Essence II Lv.1','Hunter Essence II Lv.2'], i1:fx('After Attack Delay -1% multiplied by 2 times the Blitz Beat level. Blitz Beat damage +40%. LUK +1 per armor refine.','After Attack Delay -1 % multiplié par 2 fois le niveau de Blitz Beat. Dégâts de Blitz Beat +40 %. LUK +1 par raffinage.'), i2:fx('After Attack Delay -1% multiplied by 3 times the Blitz Beat level. Blitz Beat damage +80%. LUK +1 per armor refine.','After Attack Delay -1 % multiplié par 3 fois le niveau de Blitz Beat. Dégâts de Blitz Beat +80 %. LUK +1 par raffinage.'), ii1:fx('ATK +3 per Beastbane level. Double Strafe damage +20%. Every 2 armor refines: ranged physical damage +3%.','ATK +3 par niveau de Beastbane. Dégâts de Double Strafe +20 %. Tous les 2 raffinages : dégâts physiques à distance +3 %.'), ii2:fx('ATK +5 per Beastbane level. Double Strafe damage +40%. Every 2 armor refines: ranged physical damage +3%.','ATK +5 par niveau de Beastbane. Dégâts de Double Strafe +40 %. Tous les 2 raffinages : dégâts physiques à distance +3 %.')},
      {job:'Crusader', names:['Crusader Essence Lv.1','Crusader Essence Lv.2','Crusader Essence II Lv.1','Crusader Essence II Lv.2'], i1:fx('ATK +3 per Faith level. Holy Cross damage +15%. Every 2 armor refines: Max HP +100.','ATK +3 par niveau de Faith. Dégâts de Holy Cross +15 %. Tous les 2 raffinages : Max HP +100.'), i2:fx('ATK +5 per Faith level. Holy Cross damage +15%. When worn by a Swordsman: DEF +80. Every 2 armor refines: Max HP +100.','ATK +5 par niveau de Faith. Dégâts de Holy Cross +15 %. Porté par un Swordsman : DEF +80. Tous les 2 raffinages : Max HP +100.'), ii1:fx('MATK +3 per Faith level. Grand Cross damage +20%. MATK +2 per armor refine.','MATK +3 par niveau de Faith. Dégâts de Grand Cross +20 %. MATK +2 par raffinage.'), ii2:fx('MATK +5 per Faith level. Grand Cross damage +20%. When worn by a Swordsman: healing received +15%. MATK +2 per armor refine.','MATK +5 par niveau de Faith. Dégâts de Grand Cross +20 %. Porté par un Swordsman : soins reçus +15 %. MATK +2 par raffinage.')},
      {job:'Alchemist', names:['Alchemist Essence Lv.1','Alchemist Essence Lv.2','Alchemist Essence II Lv.1','Alchemist Essence II Lv.2'], i1:fx('ATK +3 per Potion Research level. After Attack Delay -10%. Every 2 armor refines: CRIT +5.','ATK +3 par niveau de Potion Research. After Attack Delay -10 %. Tous les 2 raffinages : CRIT +5.'), i2:fx('ATK +5 per Potion Research level. After Attack Delay -10%. When worn by a Merchant: all stats +7. Every 2 armor refines: CRIT +5.','ATK +5 par niveau de Potion Research. After Attack Delay -10 %. Porté par un Merchant : toutes les stats +7. Tous les 2 raffinages : CRIT +5.'), ii1:fx('ATK +3 per Prepare Potion level. Mammonite damage +100%. ATK +2 per armor refine.','ATK +3 par niveau de Prepare Potion. Dégâts de Mammonite +100 %. ATK +2 par raffinage.'), ii2:fx('ATK +5 per Prepare Potion level. Mammonite damage +100%. When worn by a Merchant, normal melee attacks have a high chance to trigger Bash Lv.10. ATK +2 per armor refine.','ATK +5 par niveau de Prepare Potion. Dégâts de Mammonite +100 %. Porté par un Merchant, les attaques normales au corps-à-corps ont une forte chance de déclencher Bash Lv.10. ATK +2 par raffinage.')},
      {job:'Rogue', names:["Rogue's Essence Lv.1","Rogue's Essence Lv.2","Rogue's Essence II Lv.1","Rogue's Essence II Lv.2"], i1:fx('ATK +3 per Intimidate level. Sightless Mind damage +20%. After Attack Delay -1% per armor refine.','ATK +3 par niveau d’Intimidate. Dégâts de Sightless Mind +20 %. After Attack Delay -1 % par raffinage.'), i2:fx('ATK +5 per Intimidate level. Sightless Mind damage +20%. Sightless Mind SP cost -15%. After Attack Delay -1% per armor refine.','ATK +5 par niveau d’Intimidate. Dégâts de Sightless Mind +20 %. Coût SP de Sightless Mind -15 %. After Attack Delay -1 % par raffinage.'), ii1:fx('HIT +1 per Gank level. Back Stab damage +20%. ATK +2 per armor refine.','HIT +1 par niveau de Gank. Dégâts de Back Stab +20 %. ATK +2 par raffinage.'), ii2:fx('HIT +2 per Gank level. Back Stab damage +40%. ATK +2 per armor refine.','HIT +2 par niveau de Gank. Dégâts de Back Stab +40 %. ATK +2 par raffinage.')},
      {job:'Sage', names:["Sage's Essence Lv.1","Sage's Essence Lv.2","Sage's Essence II Lv.1","Sage's Essence II Lv.2"], i1:fx('MATK +3 per Hindsight level. Heaven\'s Drive and Earth Spike damage +20%. After Attack Delay -1% per armor refine.','MATK +3 par niveau de Hindsight. Dégâts de Heaven\'s Drive et Earth Spike +20 %. After Attack Delay -1 % par raffinage.'), i2:fx('MATK +5 per Hindsight level. Heaven\'s Drive and Earth Spike damage +20%. ASPD +1. Earth magic damage +15%. After Attack Delay -1% per armor refine.','MATK +5 par niveau de Hindsight. Dégâts de Heaven\'s Drive et Earth Spike +20 %. ASPD +1. Dégâts magiques Terre +15 %. After Attack Delay -1 % par raffinage.'), ii1:fx('MATK +3 per Study level. Fire Bolt, Cold Bolt and Lightning Bolt damage +20%. MATK +2 per armor refine.','MATK +3 par niveau de Study. Dégâts de Fire Bolt, Cold Bolt et Lightning Bolt +20 %. MATK +2 par raffinage.'), ii2:fx('MATK +5 per Study level. Fire Bolt, Cold Bolt and Lightning Bolt damage +40%. MATK +2 per armor refine.','MATK +5 par niveau de Study. Dégâts de Fire Bolt, Cold Bolt et Lightning Bolt +40 %. MATK +2 par raffinage.')},
      {job:'Monk', names:["Monk's Essence Lv.1","Monk's Essence Lv.2","Monk's Essence II Lv.1","Monk's Essence II Lv.2"], i1:fx('ATK +3 per Demon Bane level. Raging Quadruple Blow damage +20%. Every 2 armor refines: Raging Thrust damage +5%.','ATK +3 par niveau de Demon Bane. Dégâts de Raging Quadruple Blow +20 %. Tous les 2 raffinages : dégâts de Raging Thrust +5 %.'), i2:fx('ATK +5 per Demon Bane level. Raging Quadruple Blow damage +20%. When worn by an Acolyte, normal melee attacks have a high chance to trigger Hindsight and Summon Spirit Sphere. Every 2 armor refines: Raging Thrust damage +5%.','ATK +5 par niveau de Demon Bane. Dégâts de Raging Quadruple Blow +20 %. Porté par un Acolyte, les attaques normales au corps-à-corps ont une forte chance de déclencher Hindsight et Summon Spirit Sphere. Tous les 2 raffinages : dégâts de Raging Thrust +5 %.'), ii1:fx('Occult Impaction Variable Cast Time reduction increases by 3 times the Demon Bane level. Occult Impaction damage +20%. Every 2 armor refines: Occult Impaction damage +5%.','Réduction du Variable Cast Time d’Occult Impaction augmentée de 3 fois le niveau de Demon Bane. Dégâts d’Occult Impaction +20 %. Tous les 2 raffinages : dégâts d’Occult Impaction +5 %.'), ii2:fx('Occult Impaction Variable Cast Time reduction increases by 5 times the Demon Bane level. Occult Impaction damage +20%. Using Occult Impaction has a high chance to trigger Summon Spirit Sphere. Every 2 armor refines: Occult Impaction damage +5%.','Réduction du Variable Cast Time d’Occult Impaction augmentée de 5 fois le niveau de Demon Bane. Dégâts d’Occult Impaction +20 %. Utiliser Occult Impaction a une forte chance de déclencher Summon Spirit Sphere. Tous les 2 raffinages : dégâts d’Occult Impaction +5 %.')},
      {job:'Bard & Dancer', names:["Bard & Dancer's Essence Lv.1","Bard & Dancer's Essence Lv.2","Bard & Dancer's Essence II Lv.1","Bard & Dancer's Essence II Lv.2"], i1:fx('Amp cooldown is reduced by the sum of Music Lessons and Dance Lessons levels, up to 60 seconds. Every 2 armor refines: Max SP +30.','Le cooldown d’Amp est réduit de la somme des niveaux de Music Lessons et Dance Lessons, jusqu’à 60 secondes. Tous les 2 raffinages : Max SP +30.'), i2:fx('Amp cooldown is reduced by 3 times the sum of Music Lessons and Dance Lessons levels, up to 60 seconds. When worn by an Archer: natural SP recovery +50%. Every 2 armor refines: Max SP +30.','Le cooldown d’Amp est réduit de 3 fois la somme des niveaux de Music Lessons et Dance Lessons, jusqu’à 60 secondes. Porté par un Archer : récupération naturelle de SP +50 %. Tous les 2 raffinages : Max SP +30.'), ii1:fx('ATK +3 per Music Lessons or Dance Lessons level. Melody Strike or Slinging Arrow damage +20%. Every 2 armor refines: ranged physical damage +1%.','ATK +3 par niveau de Music Lessons ou Dance Lessons. Dégâts de Melody Strike ou Slinging Arrow +20 %. Tous les 2 raffinages : dégâts physiques à distance +1 %.'), ii2:fx('ATK +5 per Music Lessons or Dance Lessons level. Melody Strike or Slinging Arrow damage +40%. Every 2 armor refines: ranged physical damage +1%.','ATK +5 par niveau de Music Lessons ou Dance Lessons. Dégâts de Melody Strike ou Slinging Arrow +40 %. Tous les 2 raffinages : dégâts physiques à distance +1 %.')}
    ];'''

f, n = re.subn(r"    const firstEssences = \[.*?\n    const secondEssences = \[.*?\n    \];", new_data, f, count=1, flags=re.S)
assert n == 1, 'essence data block not replaced'

# Render exact clickable names, not translated/generated labels.
f = f.replace("${firstEssences.map(e=>`<tr><th>${esc(e.job)}</th><td class=\"essence-effect\"><strong>${itemLink(`${e.job}'s Essence Lv.1`)}</strong><br>${esc(e.lv1)}</td><td class=\"essence-effect\"><strong>${itemLink(`${e.job}'s Essence Lv.2`)}</strong><br>${esc(e.lv2)}</td></tr>`).join('')}", "${firstEssences.map(e=>`<tr><th>${esc(e.job)}</th><td class=\"essence-effect\"><strong>${itemLink(e.names[0])}</strong><br>${esc(e.lv1)}</td><td class=\"essence-effect\"><strong>${itemLink(e.names[1])}</strong><br>${esc(e.lv2)}</td></tr>`).join('')}")
f = f.replace("${secondEssences.map(e=>`<tr><th>${esc(e.job)}</th><td class=\"essence-effect\">${esc(e.i1)}</td><td class=\"essence-effect\">${esc(e.i2)}</td><td class=\"essence-effect\">${esc(e.ii1)}</td><td class=\"essence-effect\">${esc(e.ii2)}</td></tr>`).join('')}", "${secondEssences.map(e=>`<tr><th>${esc(e.job)}</th><td class=\"essence-effect\"><strong>${itemLink(e.names[0])}</strong><br>${esc(e.i1)}</td><td class=\"essence-effect\"><strong>${itemLink(e.names[1])}</strong><br>${esc(e.i2)}</td><td class=\"essence-effect\"><strong>${itemLink(e.names[2])}</strong><br>${esc(e.ii1)}</td><td class=\"essence-effect\"><strong>${itemLink(e.names[3])}</strong><br>${esc(e.ii2)}</td></tr>`).join('')}")

# 3) Costume Enchant: replace the mixed/old pools with the confirmed Craft Box B / Box A pools.
upper = ['Recovery Stone (Upper)','Heal effect Stone (Upper)','Large Stone (Upper)','Medium Stone (Upper)','Small Stone (Upper)','Critical Stone (Upper)','Variable Casting Stone (Upper)']
middle = ['Recovery Stone (Middle)','HP Stone (Middle)','SP Stone (Middle)','ATK Stone (Middle)','MATK Stone (Middle)','MHP Stone (Middle)','DEF Stone (Middle)','Critical Stone (Middle)','Variable Casting Stone (Middle)']
lower = ['Recovery Stone (Lower)','HIT Stone (Lower)','FLEE Stone (Lower)','HP Stone (Lower)','MSP Stone (Lower)','MDEF Stone (Lower)','ATK Stone (Lower)','MATK Stone (Lower)','Variable Casting Stone (Lower)','Critical Stone (Lower)']
garment = ['Double Attack Stone (Garment)','Critical Stone (Garment)']

def js_items(xs):
    return '${stoneList(' + repr(xs).replace('"', "'") + ')}'

pool_html = f'''            <h3 id="costume-pool">${{navLabel('Current Craft Box B pools','Pools actuels de Craft Box B')}}</h3>
            <div class="table-wrap"><table>
              <thead><tr><th>${{navLabel('Result box','Boîte obtenue')}}</th><th>${{navLabel('Possible enchant stones','Enchant stones possibles')}}</th></tr></thead>
              <tbody>
                <tr><th>${{itemLink('Costume Enchant Stone (Upper) Box A')}}</th><td>{js_items(upper)}</td></tr>
                <tr><th>${{itemLink('Costume Enchant Stone (Middle) Box A')}}</th><td>{js_items(middle)}</td></tr>
                <tr><th>${{itemLink('Costume Enchant Stone (Lower) Box A')}}</th><td>{js_items(lower)}</td></tr>
                <tr><th>${{itemLink('Costume Enchant Stone (Garment) Box A')}}</th><td>{js_items(garment)}</td></tr>
              </tbody>
            </table></div>'''
f, n = re.subn(r'            <h3 id="costume-pool">.*?</table></div>', pool_html, f, count=1, flags=re.S)
assert n == 1, 'costume pool not replaced'

# Remove unverified claims about a separate application success/break roll and consumption wording.
f = f.replace("              [navLabel('Application failure','Échec de l’application'),risk('safe','No failure roll indicated','Aucun jet d’échec indiqué')],\n              [navLabel('Item destruction','Destruction de l’objet'),risk('safe','No breaking step indicated','Aucune casse indiquée')]", "              [navLabel('Stone application rate','Taux d’application'),'—'],\n              [navLabel('Stone application break rule','Casse à l’application'),'—']")
f = re.sub(r"\n              <li>\$\{navLabel\('The five costumes used in the craft box are consumed by the conversion\.'.*?</li>", '', f, count=1)
f = f.replace("<tr><td>${navLabel('Apply the stone','Appliquer la pierre')}</td><td>${navLabel('No result reroll: the chosen stone defines the effect','Pas de nouveau tirage : la pierre choisie définit l’effet')}</td><td>${risk('safe','No item-destruction mechanic indicated','Aucune mécanique de destruction indiquée')}</td></tr>", "<tr><td>${navLabel('Apply the stone','Appliquer la pierre')}</td><td>${navLabel('The selected stone defines the effect','La pierre sélectionnée définit l’effet')}</td><td>—</td></tr>")
f = f.replace("The current Zero flow does not expose a separate success percentage for applying a compatible costume stone. The RNG is documented at the box/result stages, so no extra percentage is invented here.", "No separate application percentage is displayed here because it is not confirmed in the current data used for this guide.")
f = f.replace("Le système Zero actuel n’affiche pas de pourcentage de réussite séparé pour l’application d’une pierre compatible. Le hasard intervient lors de la boîte et du résultat obtenu ; aucun pourcentage supplémentaire n’est donc inventé ici.", "Aucun pourcentage d’application séparé n’est affiché ici car il n’est pas confirmé dans les données actuelles utilisées pour ce guide.")

# 4) Poring Village: keep user-verified current behavior and remove the unsupported 'must be equipped' prerequisite.
f = re.sub(r"\n              <li>\$\{navLabel\('The headgear must be equipped when using the Veggie Enchanter\.'.*?</li>", '', f, count=1)

# 5) Memorial Dungeon Enchant: official equipment names stay in English.
f = f.replace('Subjugation / Répression', 'Subjugation')
f = f.replace('Expedition / Expédition', 'Expedition')
f = f.replace('Dispatching / Contingent', 'Dispatching')
f = f.replace('Conqueror / Conquérant', 'Conqueror')
f = f.replace("${navLabel('Job Essence enchantments','Enchantements Essences de classe')}", 'Job Essence')
f = f.replace("${navLabel('First Job Essences','Essences de classe 1')}", '1st Job Essence')
f = f.replace("${navLabel('Second Job Essences — Essence I and Essence II','Essences de classe 2 — Essence I et Essence II')}", '2nd Job Essence — Essence I / Essence II')

# 6) Taming Ring audit: keep only facts actually confirmed; remove invented Lv1/reset percentages, zeny cost and break claims.
tam_pos = f.index('          <section class="enchant-tab-panel" id="enchant-panel-taming">')
tam = f[tam_pos:]
new_tam_facts = r'''            ${facts([
              [navLabel('Item','Objet'),itemLink('Taming Ring')],
              [navLabel('Required level','Niveau requis'),'1'],
              [navLabel('Equippable by','Utilisable par'),navLabel('All jobs — Accessory Right','Toutes les classes — Accessory Right')],
              [navLabel('Ring price','Prix de la bague'),'50 000 zeny'],
              ['Lv.1',navLabel('Requires 1 Pet Egg','Demande 1 Pet Egg')],
              ['Lv.2',`${navLabel('Requires a 2nd identical Pet Egg','Demande un 2e Pet Egg identique')} · ${risk('warn','50% success','50 % de réussite')}`],
              ['Reset',navLabel('Available in the Reset tab','Disponible dans l’onglet Reset')]
            ])}'''
tam, n = re.subn(r'            \$\{facts\(\[.*?\]\)\}', new_tam_facts, tam, count=1, flags=re.S)
assert n == 1, 'taming facts not replaced'

tam = tam.replace("              navLabel('Select the egg and create the Lv.1 enchant. The Lv.1 step has a 100% success rate.','Sélectionne l’œuf et crée l’enchantement Lv.1. Cette étape possède 100 % de réussite.'),", "              navLabel('Select the egg in the General tab to create the Lv.1 enchant.','Sélectionne l’œuf dans l’onglet General pour créer l’enchantement Lv.1.'),")
new_tam_risk = r'''            <h3 id="taming-risk">${navLabel('Success, failure and reset','Réussite, échec et reset')}</h3>
            <div class="table-wrap"><table><thead><tr><th>${navLabel('Action','Action')}</th><th>${navLabel('Requirement','Prérequis')}</th><th>${navLabel('Confirmed rate','Taux confirmé')}</th><th>${navLabel('Other confirmed information','Autre information confirmée')}</th></tr></thead><tbody>
              <tr><td>Lv.1</td><td>1 Pet Egg</td><td>—</td><td>—</td></tr>
              <tr><td>Lv.2</td><td>${navLabel('2nd identical Pet Egg','2e Pet Egg identique')}</td><td>${risk('warn','50%','50 %')}</td><td>—</td></tr>
              <tr><td>Reset</td><td>${navLabel('Reset tab','Onglet Reset')}</td><td>—</td><td>—</td></tr>
            </tbody></table></div>'''
tam, n = re.subn(r'            <h3 id="taming-risk">.*?</table></div>\n            <div class="enchant-detail-note">.*?</div>', new_tam_risk, tam, count=1, flags=re.S)
assert n == 1, 'taming risk table not replaced'
tam = tam.replace('/navi prontera 218/211', '/navi prontera 218/21')
f = f[:tam_pos] + tam

# 7) Status map: Job Essence is no longer a separate tab/section status.
s = s[:start] + f + s[end:]
s = s.replace("'#/wiki/enchantment': { costume:'partial', 'poring-village':'complete', 'memorial-gear':'complete', 'job-essences':'partial', 'taming-ring':'complete' },", "'#/wiki/enchantment': { costume:'partial', 'poring-village':'complete', 'memorial-gear':'partial', 'taming-ring':'partial' },")

# CSS can keep harmless old selectors, but the visible essence tab must be gone.
a = s.index('  function enchantmentPage(topic) {')
b = s.index('\n  function ', a + 10)
chk = s[a:b]
assert 'id="enchant-tab-essences"' not in chk
assert 'for="enchant-tab-essences"' not in chk
assert 'Essences de classe' not in chk
assert 'Enchantements Essences de classe' not in chk
assert "Rogue's Essence Lv.1" in chk and 'Intimidate level' in chk
assert 'Assassin Essence II Lv.2' in chk
assert "Swordsman's Essence Lv.1" in chk
assert "itemLink(e.names[0])" in chk and "itemLink(e.names[3])" in chk
assert 'Variable Casting Stone (Garment)' not in chk[chk.index('id="costume-pool"'):chk.index('id="enchant-panel-poring"')]
assert '/navi prontera 218/21' in chk
assert '1 Pet Egg + 10 000 zeny' not in chk
assert "Lv.1 step has a 100% success rate" not in chk
assert 'Ring destruction' not in chk

# Names of websites remain only in the Sources block, never in guide prose.
guide_body = chk.split('${officialSources([',1)[0]
for site in ['Criatura','MidgardHub','iRO Wiki','roz-global','TWRo','KRO']:
    assert site not in guide_body, site

p.write_text(s, encoding='utf-8')
