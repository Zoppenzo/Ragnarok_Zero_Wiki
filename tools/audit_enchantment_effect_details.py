from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Styling: make every Essence readable as a list of independent effects.
css_anchor = '/* Detailed enchantment guide blocks */'
assert css_anchor in s
if '.essence-effect-list {' not in s:
    css = '''/* Essence effect readability */
.essence-effect-list {
  margin: 7px 0 0 17px;
  padding: 0;
}
.essence-effect-list li {
  margin: 4px 0;
  line-height: 1.42;
}
.essence-reading-key {
  margin: 12px 0 18px;
  padding: 10px 12px;
  border: 1px solid #8daac9;
  background: #f1f7fd;
  line-height: 1.5;
}
.essence-reading-key strong { color: var(--text); }

'''
    s = s.replace(css_anchor, css + css_anchor, 1)

fn_start = s.index('  function enchantmentPage(topic) {')
fn_end = s.index('\n  function ', fn_start + 10)
f = s[fn_start:fn_end]

# Add a renderer that turns the audited ||-separated effect strings into wiki-style bullets.
fx_line = "    const fx = (en,fr) => navLabel(en,fr);"
assert fx_line in f
if 'const effectHtml =' not in f:
    f = f.replace(
        fx_line,
        fx_line + "\n    const effectHtml = text => `<ul class=\"essence-effect-list\">${String(text).split('||').map(x=>`<li>${esc(x.trim())}</li>`).join('')}</ul>`;",
        1
    )

first_start = f.index('    const firstEssences = [')
second_start = f.index('    const secondEssences = [', first_start)
return_start = f.index('\n\n    return `${breadcrumbs', second_start)

first_block = r'''    const firstEssences = [
      {job:'Mage', names:["Mage's Essence Lv.1","Mage's Essence Lv.2"],
        lv1:fx('Cold Bolt, Fire Bolt and Lightning Bolt damage +20%.||Every 2 Fire Wall levels: Variable Cast Time -1%.','Cold Bolt, Fire Bolt et Lightning Bolt : dégâts +20 %.||Tous les 2 niveaux de Fire Wall : Variable Cast Time -1 %.'),
        lv2:fx('Cold Bolt, Fire Bolt and Lightning Bolt damage +20%.||Every Fire Wall level: Variable Cast Time -1%.||Every 2 armor refines: Max SP +50.','Cold Bolt, Fire Bolt et Lightning Bolt : dégâts +20 %.||Par niveau de Fire Wall : Variable Cast Time -1 %.||Tous les 2 raffinages de l’armure : Max SP +50.')},
      {job:'Acolyte', names:["Acolyte's Essence Lv.1","Acolyte's Essence Lv.2"],
        lv1:fx('Heal, Increase Agility and Blessing SP cost -15%.||Every 2 Heal levels: Heal Amount +1%.','Heal, Increase Agility et Blessing : coût en SP -15 %.||Tous les 2 niveaux de Heal : Heal Amount +1 %.'),
        lv2:fx('Heal, Increase Agility and Blessing SP cost -15%.||Every Heal level: Heal Amount +1%.||Every 2 armor refines: Max HP +70 and Max SP +30.','Heal, Increase Agility et Blessing : coût en SP -15 %.||Par niveau de Heal : Heal Amount +1 %.||Tous les 2 raffinages de l’armure : Max HP +70 et Max SP +30.')},
      {job:'Archer', names:["Archer's Essence Lv.1","Archer's Essence Lv.2"],
        lv1:fx('Double Strafe SP cost -5.||Every Vulture\'s Eye level: Bow damage +1%.','Double Strafe : coût en SP -5.||Par niveau de Vulture\'s Eye : dégâts à l’arc +1 %.'),
        lv2:fx('Double Strafe SP cost -5.||Every Vulture\'s Eye level: Bow damage +2%.||Every 2 armor refines: Arrow Shower damage +5%.','Double Strafe : coût en SP -5.||Par niveau de Vulture\'s Eye : dégâts à l’arc +2 %.||Tous les 2 raffinages de l’armure : dégâts d’Arrow Shower +5 %.')},
      {job:'Swordsman', names:["Swordsman's Essence Lv.1","Swordsman's Essence Lv.2"],
        lv1:fx('Magnum Break SP cost -10.||Every 2 Bash levels: After Attack Delay -1%.','Magnum Break : coût en SP -10.||Tous les 2 niveaux de Bash : After Attack Delay -1 %.'),
        lv2:fx('Magnum Break SP cost -10.||Every Bash level: After Attack Delay -1%.||Every 2 armor refines: Magnum Break damage +15%.','Magnum Break : coût en SP -10.||Par niveau de Bash : After Attack Delay -1 %.||Tous les 2 raffinages de l’armure : dégâts de Magnum Break +15 %.')},
      {job:'Thief', names:["Thief's Essence Lv.1","Thief's Essence Lv.2"],
        lv1:fx('When equipped by Thief Class, using Steal grants ATK +30 for 60 seconds.||Every 2 Steal levels: After Attack Delay -1%.','Équipé par Thief Class, utiliser Steal donne ATK +30 pendant 60 secondes.||Tous les 2 niveaux de Steal : After Attack Delay -1 %.'),
        lv2:fx('When equipped by Thief Class, using Steal grants ATK +30 for 60 seconds.||Every Steal level: After Attack Delay -1%.||Every 2 armor refines: FLEE +10.','Équipé par Thief Class, utiliser Steal donne ATK +30 pendant 60 secondes.||Par niveau de Steal : After Attack Delay -1 %.||Tous les 2 raffinages de l’armure : FLEE +10.')},
      {job:'Merchant', names:["Merchant's Essence Lv.1","Merchant's Essence Lv.2"],
        lv1:fx('ATK +2 per Discount level.||Every 2 Overcharge levels: After Attack Delay -1%.','ATK +2 par niveau de Discount.||Tous les 2 niveaux d’Overcharge : After Attack Delay -1 %.'),
        lv2:fx('ATK +2 per Discount level.||Every Overcharge level: After Attack Delay -1%.||Every 2 armor refines: Max HP +100.','ATK +2 par niveau de Discount.||Par niveau d’Overcharge : After Attack Delay -1 %.||Tous les 2 raffinages de l’armure : Max HP +100.')}
    ];

'''

second_block = r'''    const secondEssences = [
      {job:'Knight', names:["Knight's Essence Lv.1","Knight's Essence Lv.2","Knight's Essence II Lv.1","Knight's Essence II Lv.2"],
        i1:fx('CRIT +3 per Cavalry Mastery level.||Bowling Bash damage +20%.||For each armor refine: After Attack Delay -1%.','CRIT +3 par niveau de Cavalry Mastery.||Dégâts de Bowling Bash +20 %.||Par raffinage de l’armure : After Attack Delay -1 %.'),
        i2:fx('CRIT +5 per Cavalry Mastery level.||Bowling Bash damage +20%.||When equipped by Swordsman Class, using Two-Hand Quicken grants Critical Damage +7% for 60 seconds.||For each armor refine: After Attack Delay -1%.','CRIT +5 par niveau de Cavalry Mastery.||Dégâts de Bowling Bash +20 %.||Équipé par Swordsman Class, utiliser Two-Hand Quicken donne Critical Damage +7 % pendant 60 secondes.||Par raffinage de l’armure : After Attack Delay -1 %.'),
        ii1:fx('HIT +1 per Spear Mastery level.||Pierce damage +20%.||For each armor refine: ATK +2.','HIT +1 par niveau de Spear Mastery.||Dégâts de Pierce +20 %.||Par raffinage de l’armure : ATK +2.'),
        ii2:fx('HIT +2 per Spear Mastery level.||Pierce damage +20%.||Using Pierce increases Brandish Spear damage by 40% for 60 seconds.||For each armor refine: ATK +2.','HIT +2 par niveau de Spear Mastery.||Dégâts de Pierce +20 %.||Utiliser Pierce augmente les dégâts de Brandish Spear de 40 % pendant 60 secondes.||Par raffinage de l’armure : ATK +2.')},

      {job:'Blacksmith', names:["Blacksmith's Essence Lv.1","Blacksmith's Essence Lv.2","Blacksmith's Essence II Lv.1","Blacksmith's Essence II Lv.2"],
        i1:fx('When equipped by Merchant Class, using Weapon Perfection grants CRIT +10 for 60 seconds.||CRIT +3 per Maximize Power level.||For each armor refine: After Attack Delay -1%.','Équipé par Merchant Class, utiliser Weapon Perfection donne CRIT +10 pendant 60 secondes.||CRIT +3 par niveau de Maximize Power.||Par raffinage de l’armure : After Attack Delay -1 %.'),
        i2:fx('When equipped by Merchant Class, using Weapon Perfection grants CRIT +10 for 60 seconds.||CRIT +5 per Maximize Power level.||Critical Damage +1% per Weaponry Research level.||For each armor refine: After Attack Delay -1%.','Équipé par Merchant Class, utiliser Weapon Perfection donne CRIT +10 pendant 60 secondes.||CRIT +5 par niveau de Maximize Power.||Critical Damage +1 % par niveau de Weaponry Research.||Par raffinage de l’armure : After Attack Delay -1 %.'),
        ii1:fx('LUK +1 per Skin Tempering level.||DEX +10.||Every 2 armor refines: LUK +1.','LUK +1 par niveau de Skin Tempering.||DEX +10.||Tous les 2 raffinages de l’armure : LUK +1.'),
        ii2:fx('LUK +2 per Skin Tempering level.||DEX +10.||Using Adrenaline Rush grants an additional DEX +10 and LUK +10 for 60 seconds.||Every 2 armor refines: LUK +1.','LUK +2 par niveau de Skin Tempering.||DEX +10.||Utiliser Adrenaline Rush donne en plus DEX +10 et LUK +10 pendant 60 secondes.||Tous les 2 raffinages de l’armure : LUK +1.')},

      {job:'Assassin', names:['Assassin Essence Lv.1','Assassin Essence Lv.2','Assassin Essence II Lv.1','Assassin Essence II Lv.2'],
        i1:fx('CRIT +3 per Grimtooth level.||Sonic Blow damage +20%.||For each armor refine: Critical Damage +1%.','CRIT +3 par niveau de Grimtooth.||Dégâts de Sonic Blow +20 %.||Par raffinage de l’armure : Critical Damage +1 %.'),
        i2:fx('CRIT +5 per Grimtooth level.||Sonic Blow damage +20%.||When equipped by Thief Class, using Sonic Blow grants After Attack Delay -7% for 60 seconds.||For each armor refine: Critical Damage +1%.','CRIT +5 par niveau de Grimtooth.||Dégâts de Sonic Blow +20 %.||Équipé par Thief Class, utiliser Sonic Blow donne After Attack Delay -7 % pendant 60 secondes.||Par raffinage de l’armure : Critical Damage +1 %.'),
        ii1:fx('FLEE +3 per Lefthand Mastery level.||Venom Splasher damage +20%.||Every 2 armor refines: Variable Cast Time -3%.','FLEE +3 par niveau de Lefthand Mastery.||Dégâts de Venom Splasher +20 %.||Tous les 2 raffinages de l’armure : Variable Cast Time -3 %.'),
        ii2:fx('FLEE +5 per Lefthand Mastery level.||Venom Splasher damage +20%.||Using Cloaking grants an additional Venom Splasher damage +20% for 60 seconds (40% total during the effect).||Every 2 armor refines: Variable Cast Time -3%.','FLEE +5 par niveau de Lefthand Mastery.||Dégâts de Venom Splasher +20 %.||Utiliser Cloaking donne +20 % de dégâts supplémentaires à Venom Splasher pendant 60 secondes (40 % au total pendant l’effet).||Tous les 2 raffinages de l’armure : Variable Cast Time -3 %.')},

      {job:'Wizard', names:['Wizard Essence Lv.1','Wizard Essence Lv.2','Wizard Essence II Lv.1','Wizard Essence II Lv.2'],
        i1:fx('Every Heaven\'s Drive level: Variable Cast Time -3%.||Meteor Storm, Lord of Vermilion and Storm Gust damage +20%.||Every 2 armor refines: MATK +1%.','Par niveau de Heaven\'s Drive : Variable Cast Time -3 %.||Dégâts de Meteor Storm, Lord of Vermilion et Storm Gust +20 %.||Tous les 2 raffinages de l’armure : MATK +1 %.'),
        i2:fx('Every Heaven\'s Drive level: Variable Cast Time -5%.||Meteor Storm, Lord of Vermilion and Storm Gust damage +20%.||When equipped by Mage Class, using Quagmire grants FLEE +30 for 60 seconds.||Every 2 armor refines: MATK +1%.','Par niveau de Heaven\'s Drive : Variable Cast Time -5 %.||Dégâts de Meteor Storm, Lord of Vermilion et Storm Gust +20 %.||Équipé par Mage Class, utiliser Quagmire donne FLEE +30 pendant 60 secondes.||Tous les 2 raffinages de l’armure : MATK +1 %.'),
        ii1:fx('Every Lord of Vermilion level: Variable Cast Time -2%.||Jupitel Thunder damage +20%.||For each armor refine: MATK +2.','Par niveau de Lord of Vermilion : Variable Cast Time -2 %.||Dégâts de Jupitel Thunder +20 %.||Par raffinage de l’armure : MATK +2.'),
        ii2:fx('Every Lord of Vermilion level: Variable Cast Time -3%.||Jupitel Thunder damage +20%.||Using Frost Nova grants an additional Jupitel Thunder damage +20% for 60 seconds (40% total during the effect).||For each armor refine: MATK +2.','Par niveau de Lord of Vermilion : Variable Cast Time -3 %.||Dégâts de Jupitel Thunder +20 %.||Utiliser Frost Nova donne +20 % de dégâts supplémentaires à Jupitel Thunder pendant 60 secondes (40 % au total pendant l’effet).||Par raffinage de l’armure : MATK +2.')},

      {job:'Priest', names:['Priest Essence Lv.1','Priest Essence Lv.2','Priest Essence II Lv.1','Priest Essence II Lv.2'],
        i1:fx('Every Magnificat level: Variable Cast Time -3%.||Magnus Exorcismus damage +20%.||Every 2 armor refines: Magnus Exorcismus damage +5%.','Par niveau de Magnificat : Variable Cast Time -3 %.||Dégâts de Magnus Exorcismus +20 %.||Tous les 2 raffinages de l’armure : dégâts de Magnus Exorcismus +5 %.'),
        i2:fx('Every Magnificat level: Variable Cast Time -5%.||Magnus Exorcismus damage +20%.||When equipped by Acolyte Class, using Gloria grants MATK +7% and Heal Amount +15% for 60 seconds.||Every 2 armor refines: Magnus Exorcismus damage +5%.','Par niveau de Magnificat : Variable Cast Time -5 %.||Dégâts de Magnus Exorcismus +20 %.||Équipé par Acolyte Class, utiliser Gloria donne MATK +7 % et Heal Amount +15 % pendant 60 secondes.||Tous les 2 raffinages de l’armure : dégâts de Magnus Exorcismus +5 %.'),
        ii1:fx('ATK +3 per Mace Mastery level.||Critical Damage +15%.||For each armor refine: ATK +2.','ATK +3 par niveau de Mace Mastery.||Critical Damage +15 %.||Par raffinage de l’armure : ATK +2.'),
        ii2:fx('ATK +5 per Mace Mastery level.||Critical Damage +15%.||When equipped by Acolyte Class, after using Status Recovery, normal melee attacks have a high chance to trigger Bash Lv.10 for 60 seconds.||For each armor refine: ATK +2.','ATK +5 par niveau de Mace Mastery.||Critical Damage +15 %.||Équipé par Acolyte Class, après avoir utilisé Status Recovery, les attaques normales au corps-à-corps ont une forte chance de déclencher Bash Lv.10 pendant 60 secondes.||Par raffinage de l’armure : ATK +2.')},

      {job:'Hunter', names:['Hunter Essence Lv.1','Hunter Essence Lv.2','Hunter Essence II Lv.1','Hunter Essence II Lv.2'],
        i1:fx('Every 2 Blitz Beat levels: After Attack Delay -1%.||Blitz Beat damage +40%.||For each armor refine: LUK +1.','Tous les 2 niveaux de Blitz Beat : After Attack Delay -1 %.||Dégâts de Blitz Beat +40 %.||Par raffinage de l’armure : LUK +1.'),
        i2:fx('Every 2 Blitz Beat levels: After Attack Delay -1%.||Blitz Beat damage +40%.||Using Improve Concentration grants an additional Blitz Beat damage +40% for 60 seconds (80% total during the effect).||For each armor refine: LUK +1.','Tous les 2 niveaux de Blitz Beat : After Attack Delay -1 %.||Dégâts de Blitz Beat +40 %.||Utiliser Improve Concentration donne +40 % de dégâts supplémentaires à Blitz Beat pendant 60 secondes (80 % au total pendant l’effet).||Par raffinage de l’armure : LUK +1.'),
        ii1:fx('ATK +3 per Beastbane level.||Double Strafe damage +20%.||Every 2 armor refines: Ranged Weapon Physical Damage +3%.','ATK +3 par niveau de Beastbane.||Dégâts de Double Strafe +20 %.||Tous les 2 raffinages de l’armure : Ranged Weapon Physical Damage +3 %.'),
        ii2:fx('ATK +5 per Beastbane level.||Double Strafe damage +20%.||Using Detect grants an additional Double Strafe damage +20% for 60 seconds (40% total during the effect).||Every 2 armor refines: Ranged Weapon Physical Damage +3%.','ATK +5 par niveau de Beastbane.||Dégâts de Double Strafe +20 %.||Utiliser Detect donne +20 % de dégâts supplémentaires à Double Strafe pendant 60 secondes (40 % au total pendant l’effet).||Tous les 2 raffinages de l’armure : Ranged Weapon Physical Damage +3 %.')},

      {job:'Crusader', names:['Crusader Essence Lv.1','Crusader Essence Lv.2','Crusader Essence II Lv.1','Crusader Essence II Lv.2'],
        i1:fx('ATK +3 per Faith level.||Holy Cross damage +15%.||Every 2 armor refines: Max HP +100.','ATK +3 par niveau de Faith.||Dégâts de Holy Cross +15 %.||Tous les 2 raffinages de l’armure : Max HP +100.'),
        i2:fx('ATK +5 per Faith level.||Holy Cross damage +15%.||When equipped by Swordsman Class, using Auto Guard grants DEF +80 for 60 seconds.||Every 2 armor refines: Max HP +100.','ATK +5 par niveau de Faith.||Dégâts de Holy Cross +15 %.||Équipé par Swordsman Class, utiliser Auto Guard donne DEF +80 pendant 60 secondes.||Tous les 2 raffinages de l’armure : Max HP +100.'),
        ii1:fx('MATK +3 per Faith level.||Grand Cross damage +20%.||For each armor refine: MATK +2.','MATK +3 par niveau de Faith.||Dégâts de Grand Cross +20 %.||Par raffinage de l’armure : MATK +2.'),
        ii2:fx('MATK +5 per Faith level.||Grand Cross damage +20%.||Using Endure increases Heal Received by 15% for 60 seconds.||For each armor refine: MATK +2.','MATK +5 par niveau de Faith.||Dégâts de Grand Cross +20 %.||Utiliser Endure augmente Heal Received de 15 % pendant 60 secondes.||Par raffinage de l’armure : MATK +2.')},

      {job:'Alchemist', names:['Alchemist Essence Lv.1','Alchemist Essence Lv.2','Alchemist Essence II Lv.1','Alchemist Essence II Lv.2'],
        i1:fx('ATK +3 per Potion Research level.||After Attack Delay -10%.||Every 2 armor refines: CRIT +5.','ATK +3 par niveau de Potion Research.||After Attack Delay -10 %.||Tous les 2 raffinages de l’armure : CRIT +5.'),
        i2:fx('ATK +5 per Potion Research level.||After Attack Delay -10%.||Every 2 armor refines: CRIT +5.','ATK +5 par niveau de Potion Research.||After Attack Delay -10 %.||Tous les 2 raffinages de l’armure : CRIT +5.'),
        ii1:fx('ATK +3 per Prepare Potion level.||Mammonite damage +100%.||For each armor refine: ATK +2.','ATK +3 par niveau de Prepare Potion.||Dégâts de Mammonite +100 %.||Par raffinage de l’armure : ATK +2.'),
        ii2:fx('ATK +5 per Prepare Potion level.||Mammonite damage +100%.||When equipped by Merchant Class, after using Potion Pitcher, normal melee attacks have a high chance to trigger Bash Lv.10 for 60 seconds.||For each armor refine: ATK +2.','ATK +5 par niveau de Prepare Potion.||Dégâts de Mammonite +100 %.||Équipé par Merchant Class, après avoir utilisé Potion Pitcher, les attaques normales au corps-à-corps ont une forte chance de déclencher Bash Lv.10 pendant 60 secondes.||Par raffinage de l’armure : ATK +2.')},

      {job:'Rogue', names:["Rogue's Essence Lv.1","Rogue's Essence Lv.2","Rogue's Essence II Lv.1","Rogue's Essence II Lv.2"],
        i1:fx('ATK +3 per Intimidate level.||Sightless Mind damage +20%.||For each armor refine: After Attack Delay -1%.','ATK +3 par niveau d’Intimidate.||Dégâts de Sightless Mind +20 %.||Par raffinage de l’armure : After Attack Delay -1 %.'),
        i2:fx('ATK +5 per Intimidate level.||Sightless Mind damage +20%.||Using Hide reduces Sightless Mind SP cost by 15% for 60 seconds.||For each armor refine: After Attack Delay -1%.','ATK +5 par niveau d’Intimidate.||Dégâts de Sightless Mind +20 %.||Utiliser Hide réduit le coût en SP de Sightless Mind de 15 % pendant 60 secondes.||Par raffinage de l’armure : After Attack Delay -1 %.'),
        ii1:fx('HIT +1 per Gank level.||Back Stab damage +20%.||For each armor refine: ATK +2.','HIT +1 par niveau de Gank.||Dégâts de Back Stab +20 %.||Par raffinage de l’armure : ATK +2.'),
        ii2:fx('HIT +2 per Gank level.||Back Stab damage +20%.||Using Envenom grants an additional Back Stab damage +20% for 60 seconds (40% total during the effect).||For each armor refine: ATK +2.','HIT +2 par niveau de Gank.||Dégâts de Back Stab +20 %.||Utiliser Envenom donne +20 % de dégâts supplémentaires à Back Stab pendant 60 secondes (40 % au total pendant l’effet).||Par raffinage de l’armure : ATK +2.')},

      {job:'Sage', names:["Sage's Essence Lv.1","Sage's Essence Lv.2","Sage's Essence II Lv.1","Sage's Essence II Lv.2"],
        i1:fx('MATK +3 per Hindsight level.||Heaven\'s Drive and Earth Spike damage +20%.||For each armor refine: After Attack Delay -1%.','MATK +3 par niveau de Hindsight.||Dégâts de Heaven\'s Drive et Earth Spike +20 %.||Par raffinage de l’armure : After Attack Delay -1 %.'),
        i2:fx('MATK +5 per Hindsight level.||Heaven\'s Drive and Earth Spike damage +20%.||ASPD +1.||Neutral resistance +7%.','MATK +5 par niveau de Hindsight.||Dégâts de Heaven\'s Drive et Earth Spike +20 %.||ASPD +1.||Résistance Neutral +7 %.'),
        ii1:fx('MATK +3 per Study level.||Fire Bolt, Cold Bolt and Lightning Bolt damage +20%.||For each armor refine: MATK +2.','MATK +3 par niveau de Study.||Dégâts de Fire Bolt, Cold Bolt et Lightning Bolt +20 %.||Par raffinage de l’armure : MATK +2.'),
        ii2:fx('MATK +5 per Study level.||Fire Bolt, Cold Bolt and Lightning Bolt damage +20%.||After using Earth Spike, Fire Bolt, Cold Bolt and Lightning Bolt gain an additional damage +20% for 60 seconds (40% total during the effect).||For each armor refine: MATK +2.','MATK +5 par niveau de Study.||Dégâts de Fire Bolt, Cold Bolt et Lightning Bolt +20 %.||Après avoir utilisé Earth Spike, Fire Bolt, Cold Bolt et Lightning Bolt gagnent +20 % de dégâts supplémentaires pendant 60 secondes (40 % au total pendant l’effet).||Par raffinage de l’armure : MATK +2.')},

      {job:'Monk', names:["Monk's Essence Lv.1","Monk's Essence Lv.2","Monk's Essence II Lv.1","Monk's Essence II Lv.2"],
        i1:fx('ATK +3 per Demon Bane level.||Raging Quadruple Blow damage +20%.||Every 2 armor refines: Raging Thrust damage +5%.','ATK +3 par niveau de Demon Bane.||Dégâts de Raging Quadruple Blow +20 %.||Tous les 2 raffinages de l’armure : dégâts de Raging Thrust +5 %.'),
        i2:fx('ATK +5 per Demon Bane level.||Raging Quadruple Blow damage +20%.||When equipped by Acolyte Class, using Explosion Spirits activates a 60-second effect during which normal melee attacks have a high chance to trigger Hindsight and Summon Spirit Sphere.||Every 2 armor refines: Raging Thrust damage +5%.','ATK +5 par niveau de Demon Bane.||Dégâts de Raging Quadruple Blow +20 %.||Équipé par Acolyte Class, utiliser Explosion Spirits active pendant 60 secondes un effet durant lequel les attaques normales au corps-à-corps ont une forte chance de déclencher Hindsight et Summon Spirit Sphere.||Tous les 2 raffinages de l’armure : dégâts de Raging Thrust +5 %.'),
        ii1:fx('Every Demon Bane level: Occult Impaction Variable Cast Time -3%.||Occult Impaction damage +20%.||Every 2 armor refines: Occult Impaction damage +5%.','Par niveau de Demon Bane : Variable Cast Time d’Occult Impaction -3 %.||Dégâts d’Occult Impaction +20 %.||Tous les 2 raffinages de l’armure : dégâts d’Occult Impaction +5 %.'),
        ii2:fx('Every Demon Bane level: Occult Impaction Variable Cast Time -5%.||Occult Impaction damage +20%.||After using Blessing, for 60 seconds using Occult Impaction has a high chance to trigger Summon Spirit Sphere.||Every 2 armor refines: Occult Impaction damage +5%.','Par niveau de Demon Bane : Variable Cast Time d’Occult Impaction -5 %.||Dégâts d’Occult Impaction +20 %.||Après avoir utilisé Blessing, pendant 60 secondes Occult Impaction a une forte chance de déclencher Summon Spirit Sphere.||Tous les 2 raffinages de l’armure : dégâts d’Occult Impaction +5 %.')},

      {job:'Bard & Dancer', names:["Bard & Dancer's Essence Lv.1","Bard & Dancer's Essence Lv.2","Bard & Dancer's Essence II Lv.1","Bard & Dancer's Essence II Lv.2"],
        i1:fx('Amp cooldown is reduced by the Music Lessons / Dance Lessons level, up to 60 seconds.||Every 2 armor refines: Max SP +30.','Le cooldown d’Amp est réduit selon le niveau de Music Lessons / Dance Lessons, jusqu’à 60 secondes.||Tous les 2 raffinages de l’armure : Max SP +30.'),
        i2:fx('Amp cooldown reduction is 3× the Music Lessons / Dance Lessons level, up to 60 seconds.||When equipped by Archer Class, using Service For You or A Poem of Bragi grants Natural SP Recovery +50% for 60 seconds.||Every 2 armor refines: Max SP +30.','La réduction du cooldown d’Amp vaut 3× le niveau de Music Lessons / Dance Lessons, jusqu’à 60 secondes.||Équipé par Archer Class, utiliser Service For You ou A Poem of Bragi donne Natural SP Recovery +50 % pendant 60 secondes.||Tous les 2 raffinages de l’armure : Max SP +30.'),
        ii1:fx('ATK +3 per Music Lessons / Dance Lessons level.||Melody Strike and Slinging Arrow damage +20%.||Every 2 armor refines: Ranged Weapon Physical Damage +1%.','ATK +3 par niveau de Music Lessons / Dance Lessons.||Dégâts de Melody Strike et Slinging Arrow +20 %.||Tous les 2 raffinages de l’armure : Ranged Weapon Physical Damage +1 %.'),
        ii2:fx('ATK +5 per Music Lessons / Dance Lessons level.||Melody Strike and Slinging Arrow damage +20%.||After using Encore, Melody Strike and Slinging Arrow gain an additional damage +20% for 60 seconds (40% total during the effect).||Every 2 armor refines: Ranged Weapon Physical Damage +1%.','ATK +5 par niveau de Music Lessons / Dance Lessons.||Dégâts de Melody Strike et Slinging Arrow +20 %.||Après avoir utilisé Encore, Melody Strike et Slinging Arrow gagnent +20 % de dégâts supplémentaires pendant 60 secondes (40 % au total pendant l’effet).||Tous les 2 raffinages de l’armure : Ranged Weapon Physical Damage +1 %.')}
    ];'''

f = f[:first_start] + first_block + second_block + f[return_start:]

# Render each Essence as a clean bullet list instead of one dense sentence.
old_first = '${firstEssences.map(e=>`<tr><th>${esc(e.job)}</th><td class="essence-effect"><strong>${itemLink(e.names[0])}</strong><br>${esc(e.lv1)}</td><td class="essence-effect"><strong>${itemLink(e.names[1])}</strong><br>${esc(e.lv2)}</td></tr>`).join(\'\')}'
new_first = '${firstEssences.map(e=>`<tr><th>${esc(e.job)}</th><td class="essence-effect"><strong>${itemLink(e.names[0])}</strong>${effectHtml(e.lv1)}</td><td class="essence-effect"><strong>${itemLink(e.names[1])}</strong>${effectHtml(e.lv2)}</td></tr>`).join(\'\')}'
assert old_first in f
f = f.replace(old_first, new_first, 1)

old_second = '${secondEssences.map(e=>`<tr><th>${esc(e.job)}</th><td class="essence-effect"><strong>${itemLink(e.names[0])}</strong><br>${esc(e.i1)}</td><td class="essence-effect"><strong>${itemLink(e.names[1])}</strong><br>${esc(e.i2)}</td><td class="essence-effect"><strong>${itemLink(e.names[2])}</strong><br>${esc(e.ii1)}</td><td class="essence-effect"><strong>${itemLink(e.names[3])}</strong><br>${esc(e.ii2)}</td></tr>`).join(\'\')}'
new_second = '${secondEssences.map(e=>`<tr><th>${esc(e.job)}</th><td class="essence-effect"><strong>${itemLink(e.names[0])}</strong>${effectHtml(e.i1)}</td><td class="essence-effect"><strong>${itemLink(e.names[1])}</strong>${effectHtml(e.i2)}</td><td class="essence-effect"><strong>${itemLink(e.names[2])}</strong>${effectHtml(e.ii1)}</td><td class="essence-effect"><strong>${itemLink(e.names[3])}</strong>${effectHtml(e.ii2)}</td></tr>`).join(\'\')}'
assert old_second in f
f = f.replace(old_second, new_second, 1)

# Explain how to read the table. This avoids ambiguity between passive and triggered bonuses.
key_anchor = '            <h3 id="essence-first">1st Job Essence</h3>'
assert key_anchor in f
key = '''            <div class="essence-reading-key"><strong>${navLabel('How to read the effects','Comment lire les effets')}:</strong> ${navLabel(
              'Each bullet is one separate effect. When a bonus requires a skill to be used, the trigger and its duration are written explicitly. If no duration is shown, the effect is passive or scales while the Essence is equipped. “High chance” is kept as-is when no reliable numeric proc rate is available.',
              'Chaque puce correspond à un effet séparé. Lorsqu’un bonus demande d’utiliser un skill, le déclencheur et sa durée sont indiqués explicitement. Si aucune durée n’est affichée, l’effet est passif ou évolue tant que l’Essence est équipée. « Forte chance » est conservé tel quel lorsqu’aucun taux numérique fiable n’est disponible.'
            )}</div>\n\n'''
f = f.replace(key_anchor, key + key_anchor, 1)

# The exact random-option roll percentages currently conflict between published datasets and are not confirmed in the live Global client.
# Keep the option pools useful, but stop presenting disputed precision as fact.
rate_start = f.index('            <h3 id="md-rates">')
rate_end = f.index('            <div class="hero-actions">', rate_start)
rate_replacement = '''            <h3 id="md-rates">${navLabel('Random option pool','Pool des options aléatoires')}</h3>
            <div class="notice info"><svg class="notice-icon"><use href="#i-info"></use></svg><div>${navLabel(
              'The exact individual roll percentages are intentionally not displayed for now because they are not confirmed in the current Global client data. The possible option families remain listed below without inventing a probability.',
              'Les pourcentages exacts de tirage ne sont volontairement pas affichés pour le moment car ils ne sont pas confirmés dans les données du client Global actuel. Les familles d’options possibles restent indiquées ci-dessous sans inventer de probabilité.'
            )}</div></div>
            <div class="table-wrap"><table><thead><tr><th>${navLabel('Family','Famille')}</th><th>${navLabel('Possible options','Options possibles')}</th></tr></thead><tbody>
              <tr><th>${navLabel('Stats','Stats')}</th><td>STR +1/+2 · AGI +1/+2 · VIT +1/+2 · INT +1/+2 · DEX +1/+2 · LUK +1/+2</td></tr>
              <tr><th>${navLabel('Utility','Utilitaire')}</th><td>FLEE +3 · CRI +1 · DEF +15 · MDEF +2</td></tr>
              <tr><th>HP</th><td>Max HP +50 · +100 · +200</td></tr>
            </tbody></table></div>
'''
f = f[:rate_start] + rate_replacement + f[rate_end:]

# Rebuild page function in full file.
s = s[:fn_start] + f + s[fn_end:]

# Regression / audit assertions.
a = s.index('  function enchantmentPage(topic) {')
b = s.index('\n  function ', a + 10)
guide = s[a:b]
for needle in [
    'Using Pierce increases Brandish Spear damage by 40% for 60 seconds.',
    'using Two-Hand Quicken grants Critical Damage +7% for 60 seconds.',
    'using Weapon Perfection grants CRIT +10 for 60 seconds.',
    'using Sonic Blow grants After Attack Delay -7% for 60 seconds.',
    'using Quagmire grants FLEE +30 for 60 seconds.',
    'using Gloria grants MATK +7% and Heal Amount +15% for 60 seconds.',
    'Using Improve Concentration grants an additional Blitz Beat damage +40% for 60 seconds',
    'using Auto Guard grants DEF +80 for 60 seconds.',
    'Using Hide reduces Sightless Mind SP cost by 15% for 60 seconds.',
    'Using Cloaking grants an additional Venom Splasher damage +20% for 60 seconds',
    'Using Frost Nova grants an additional Jupitel Thunder damage +20% for 60 seconds',
    'after using Status Recovery',
    'Using Detect grants an additional Double Strafe damage +20% for 60 seconds',
    'Using Endure increases Heal Received by 15% for 60 seconds.',
    'after using Potion Pitcher',
    'Using Envenom grants an additional Back Stab damage +20% for 60 seconds',
    'After using Earth Spike',
    'After using Blessing, for 60 seconds',
    'After using Encore',
    'Neutral resistance +7%.',
    'effectHtml(e.ii2)',
    'exact individual roll percentages are intentionally not displayed'
]:
    assert needle in guide, needle

# Removed/incorrect or disputed old claims must not survive in the guide.
for forbidden in [
    'all stats +7',
    'Earth magic damage +15%',
    'Random option rates — refine +0 to +8',
    '10.52%',
    '7.58%'
]:
    assert forbidden not in guide, forbidden

# Site/version provenance remains restricted to Sources only.
guide_body = guide.split('${officialSources([', 1)[0]
for site in ['Criatura','MidgardHub','iRO Wiki','roz-global','TWRo','KRO']:
    assert site not in guide_body, site

p.write_text(s, encoding='utf-8')
