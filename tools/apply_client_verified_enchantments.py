from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

first_start = s.index('    const firstEssences = [')
second_start = s.index('    const secondEssences = [', first_start)

first_block = r'''    const firstEssences = [
      {job:'Swordsman', names:["Swordsman's Essence Lv.1","Swordsman's Essence Lv.2"],
        lv1:fx('Reduces SP cost of Magnum Break by 10.||For every 2 levels of Bash, ASPD increases (After Attack Delay -1%).','Magnum Break : coût en SP -10.||Tous les 2 niveaux de Bash : ASPD augmente (After Attack Delay -1 %).'),
        lv2:fx('For every 1 level of Bash, ASPD increases (After Attack Delay -1%).||For every 2 armor refine levels, Magnum Break damage +15%.','Par niveau de Bash : ASPD augmente (After Attack Delay -1 %).||Tous les 2 niveaux de refine de l’armure : dégâts de Magnum Break +15 %.')},
      {job:'Merchant', names:["Merchant's Essence Lv.1","Merchant's Essence Lv.2"],
        lv1:fx('For every 1 level of Discount, ATK +2.||For every 2 levels of Overcharge, ASPD increases (After Attack Delay -1% per step).','Par niveau de Discount : ATK +2.||Tous les 2 niveaux d’Overcharge : ASPD augmente (After Attack Delay -1 % par palier).'),
        lv2:fx('For every 1 level of Overcharge, ASPD increases (After Attack Delay -1% per step).||For every 2 refine levels on armor, MHP +100.','Par niveau d’Overcharge : ASPD augmente (After Attack Delay -1 % par palier).||Tous les 2 niveaux de refine de l’armure : MHP +100.')},
      {job:'Thief', names:["Thief's Essence Lv.1","Thief's Essence Lv.2"],
        lv1:fx('When equipped by Thief Class, ATK +30.||For every 2 levels of Steal, ASPD increases (After Attack Delay -1% per step).','Thief Class : ATK +30.||Tous les 2 niveaux de Steal : ASPD augmente (After Attack Delay -1 % par palier).'),
        lv2:fx('For every 1 level of Steal, ASPD increases (After Attack Delay -1% per step).||For every 2 refine levels on armor, FLEE +10.','Par niveau de Steal : ASPD augmente (After Attack Delay -1 % par palier).||Tous les 2 niveaux de refine de l’armure : FLEE +10.')},
      {job:'Mage', names:["Mage's Essence Lv.1","Mage's Essence Lv.2"],
        lv1:fx('Increases damage of Cold Bolt, Fire Bolt, and Lightning Bolt by 20%.||For every 2 levels of Fire Wall, Variable Casting Time -1%.','Cold Bolt, Fire Bolt et Lightning Bolt : dégâts +20 %.||Tous les 2 niveaux de Fire Wall : Variable Casting Time -1 %.'),
        lv2:fx('For every 1 level of Fire Wall, Variable Casting Time -1%.||For every 2 refine levels on armor, MSP +50.','Par niveau de Fire Wall : Variable Casting Time -1 %.||Tous les 2 niveaux de refine de l’armure : MSP +50.')},
      {job:'Acolyte', names:["Acolyte's Essence Lv.1","Acolyte's Essence Lv.2"],
        lv1:fx('Reduces SP cost of Heal, Increase Agility, and Blessing by 15%.||For every 2 levels of Heal, Heal Amount +1%.','Heal, Increase Agility et Blessing : coût en SP -15 %.||Tous les 2 niveaux de Heal : Heal Amount +1 %.'),
        lv2:fx('For every 1 level of Heal, Heal Amount +1%.||For every 2 refine levels on armor, MHP +70 and MSP +30.','Par niveau de Heal : Heal Amount +1 %.||Tous les 2 niveaux de refine de l’armure : MHP +70 et MSP +30.')},
      {job:'Archer', names:["Archer's Essence Lv.1","Archer's Essence Lv.2"],
        lv1:fx('Reduces SP cost of Double Strafe by 5.||For every 1 level of Vulture\'s Eye, Bow Damage +1%.','Double Strafe : coût en SP -5.||Par niveau de Vulture\'s Eye : Bow Damage +1 %.'),
        lv2:fx('For every 1 level of Vulture\'s Eye, Bow Damage +2%.||For every 2 refine levels on armor, Arrow Shower damage +5%.','Par niveau de Vulture\'s Eye : Bow Damage +2 %.||Tous les 2 niveaux de refine de l’armure : dégâts d’Arrow Shower +5 %.')}
    ];

'''

second_end = s.index('\n    const mdCommonOptions = [', second_start)
second_block = r'''    const secondEssences = [
      {job:'Knight', names:["Knight's Essence Lv.1","Knight's Essence Lv.2","Knight's Essence II Lv.1","Knight's Essence II Lv.2"],
        i1:fx('CRIT increases by 3× the level of Cavalier Mastery.||Increases Bowling Bash damage by 20%.||For each armor refine level, ASPD increases (After Attack Delay -1%).','CRIT +3 × niveau de Cavalier Mastery.||Bowling Bash : dégâts +20 %.||Par niveau de refine de l’armure : ASPD augmente (After Attack Delay -1 %).'),
        i2:fx('CRIT increases by 5× the level of Cavalier Mastery.||When equipped by Swordsman Class, Critical Damage +7%.','CRIT +5 × niveau de Cavalier Mastery.||Swordsman Class : Critical Damage +7 %.'),
        ii1:fx('Increases HIT by the level of Spear Mastery.||Increases Pierce damage by 20%.||For each armor refine level, ATK +2.','HIT + niveau de Spear Mastery.||Pierce : dégâts +20 %.||Par niveau de refine de l’armure : ATK +2.'),
        ii2:fx('Increases HIT by 2× the level of Spear Mastery.||Increases Brandish Spear damage by 40%.','HIT +2 × niveau de Spear Mastery.||Brandish Spear : dégâts +40 %.')},
      {job:'Blacksmith', names:["Blacksmith's Essence Lv.1","Blacksmith's Essence Lv.2","Blacksmith's Essence II Lv.1","Blacksmith's Essence II Lv.2"],
        i1:fx('When equipped by Merchant Class, CRIT +10.||For every 3 levels of Maximize Power, CRIT increases.||For each refine level on armor, ASPD increases (After Attack Delay -1%).','Merchant Class : CRIT +10.||Tous les 3 niveaux de Maximize Power : CRIT augmente.||Par niveau de refine de l’armure : ASPD augmente (After Attack Delay -1 %).'),
        i2:fx('CRIT increases by 5× the skill level of Maximize Power.||For every level of Weaponry Research, Critical Damage +1%.','CRIT +5 × niveau de Maximize Power.||Par niveau de Weaponry Research : Critical Damage +1 %.'),
        ii1:fx('Increases LUK by the level of Skin Tempering.||For every 2 armor refine levels, LUK +1.','LUK + niveau de Skin Tempering.||Tous les 2 niveaux de refine de l’armure : LUK +1.'),
        ii2:fx('Increases LUK by 2× the level of Skin Tempering.||When equipped by Merchant Class, DEX +10 and LUK +10.','LUK +2 × niveau de Skin Tempering.||Merchant Class : DEX +10 et LUK +10.')},
      {job:'Assassin', names:['Assassin Essence Lv.1','Assassin Essence Lv.2','Assassin Essence II Lv.1','Assassin Essence II Lv.2'],
        i1:fx('CRIT increases by 3× the level of Grimtooth.||For each armor refine level, Critical Damage +1%.','CRIT +3 × niveau de Grimtooth.||Par niveau de refine de l’armure : Critical Damage +1 %.'),
        i2:fx('CRIT increases by 5× the level of Grimtooth.||When equipped by Thief Class, ASPD increases (After Attack Delay -7%).','CRIT +5 × niveau de Grimtooth.||Thief Class : ASPD augmente (After Attack Delay -7 %).'),
        ii1:fx('FLEE increases by 3× the skill level of Lefthand Mastery.||Increases Venom Splasher damage by 20%.||For every 2 armor refine levels, Variable Casting Time -3%.','FLEE +3 × niveau de Lefthand Mastery.||Venom Splasher : dégâts +20 %.||Tous les 2 niveaux de refine de l’armure : Variable Casting Time -3 %.'),
        ii2:fx('FLEE increases by 5× the skill level of Lefthand Mastery.||Increases Venom Splasher damage by 40%.||For every 2 refines, Variable Casting Time -3%.','FLEE +5 × niveau de Lefthand Mastery.||Venom Splasher : dégâts +40 %.||Tous les 2 niveaux de refine : Variable Casting Time -3 %.')},
      {job:'Wizard', names:['Wizard Essence Lv.1','Wizard Essence Lv.2','Wizard Essence II Lv.1','Wizard Essence II Lv.2'],
        i1:fx('Variable Casting Time is reduced by 3× the level of Heaven\'s Drive.||Increases Meteor Storm, Lord of Vermilion, and Storm Gust damage by 20%.||For every 2 armor refine levels, MATK +1%.','Variable Casting Time réduit de 3 % × niveau de Heaven\'s Drive.||Meteor Storm, Lord of Vermilion et Storm Gust : dégâts +20 %.||Tous les 2 niveaux de refine de l’armure : MATK +1 %.'),
        i2:fx('Variable Casting Time is reduced by 5× the level of Heaven\'s Drive.||When equipped by Mage Class, FLEE +30.','Variable Casting Time réduit de 5 % × niveau de Heaven\'s Drive.||Mage Class : FLEE +30.'),
        ii1:fx('Variable Cast Time Reduction increases by 2× the level of Lord of Vermilion.||Increases Jupitel Thunder damage by 20%.||For each armor refine level, MATK +2.','Réduction du Variable Cast Time +2 % × niveau de Lord of Vermilion.||Jupitel Thunder : dégâts +20 %.||Par niveau de refine de l’armure : MATK +2.'),
        ii2:fx('Variable Cast Time Reduction increases by 3× the level of Lord of Vermilion.||Increases Jupitel Thunder damage by 40%.','Réduction du Variable Cast Time +3 % × niveau de Lord of Vermilion.||Jupitel Thunder : dégâts +40 %.')},
      {job:'Priest', names:['Priest Essence Lv.1','Priest Essence Lv.2','Priest Essence II Lv.1','Priest Essence II Lv.2'],
        i1:fx('Variable Cast Time Reduction increases by 3× the level of Magnificat.||Increases Magnus Exorcismus damage by 20%.||For every 2 armor refine levels, Magnus Exorcismus damage +5%.','Réduction du Variable Cast Time +3 % × niveau de Magnificat.||Magnus Exorcismus : dégâts +20 %.||Tous les 2 niveaux de refine de l’armure : dégâts de Magnus Exorcismus +5 %.'),
        i2:fx('Variable Cast Time Reduction increases by 5× the level of Magnificat.||When equipped by Acolyte Class, MATK +7% and Heal Amount +15%.','Réduction du Variable Cast Time +5 % × niveau de Magnificat.||Acolyte Class : MATK +7 % et Heal Amount +15 %.'),
        ii1:fx('Increases ATK by 3× the level of Mace Mastery.||For each refine, ATK +2.','ATK +3 × niveau de Mace Mastery.||Par niveau de refine : ATK +2.'),
        ii2:fx('Increases ATK by 5× the level of Mace Mastery.||When equipped by Acolyte Class, normal melee attacks have a high chance to trigger Bash Lv 10.','ATK +5 × niveau de Mace Mastery.||Acolyte Class : les attaques normales au corps-à-corps ont une forte chance de déclencher Bash Lv.10.')},
      {job:'Hunter', names:['Hunter Essence Lv.1','Hunter Essence Lv.2','Hunter Essence II Lv.1','Hunter Essence II Lv.2'],
        i1:fx('ASPD increases by 2× the level of Blitz Beat (After Attack Delay -1%).||Increases Blitz Beat damage by 40%.||For each armor refine level, LUK +1.','ASPD augmente de 2 × niveau de Blitz Beat (After Attack Delay -1 %).||Blitz Beat : dégâts +40 %.||Par niveau de refine de l’armure : LUK +1.'),
        i2:fx('ASPD increases by 3× the level of Blitz Beat (After Attack Delay -1%).||Increases Blitz Beat damage by 80%.','ASPD augmente de 3 × niveau de Blitz Beat (After Attack Delay -1 %).||Blitz Beat : dégâts +80 %.'),
        ii1:fx('Increases ATK by 3× the level of Beastbane.||Increases Double Strafe damage by 20%.||For every 2 refines, Ranged Weapon Physical Damage +3%.','ATK +3 × niveau de Beastbane.||Double Strafe : dégâts +20 %.||Tous les 2 niveaux de refine : Ranged Weapon Physical Damage +3 %.'),
        ii2:fx('Increases ATK by 5× the level of Beastbane.||Increases Double Strafe damage by 40%.','ATK +5 × niveau de Beastbane.||Double Strafe : dégâts +40 %.')},
      {job:'Crusader', names:['Crusader Essence Lv.1','Crusader Essence Lv.2','Crusader Essence II Lv.1','Crusader Essence II Lv.2'],
        i1:fx('ATK increases by 3× the level of Faith.||Increases Holy Cross damage by 15%.||For every 2 armor refine levels, MHP +100.','ATK +3 × niveau de Faith.||Holy Cross : dégâts +15 %.||Tous les 2 niveaux de refine de l’armure : MHP +100.'),
        i2:fx('ATK increases by 5× the level of Faith.||When equipped by Swordsman Class, DEF +80.','ATK +5 × niveau de Faith.||Swordsman Class : DEF +80.'),
        ii1:fx('MATK increases by 3× the level of Faith.||Increases Grand Cross damage by 20%.','MATK +3 × niveau de Faith.||Grand Cross : dégâts +20 %.'),
        ii2:fx('MATK increases by 5× the level of Faith.||When equipped by Swordsman Class, received Heal Amount +15%.','MATK +5 × niveau de Faith.||Swordsman Class : Heal Amount reçu +15 %.')},
      {job:'Alchemist', names:['Alchemist Essence Lv.1','Alchemist Essence Lv.2','Alchemist Essence II Lv.1','Alchemist Essence II Lv.2'],
        i1:fx('Increases ATK by 3× the level of Potion Research.||ASPD increases (After Attack Delay -10%).||For every 2 armor refine levels, CRIT +5.','ATK +3 × niveau de Potion Research.||ASPD augmente (After Attack Delay -10 %).||Tous les 2 niveaux de refine de l’armure : CRIT +5.'),
        i2:fx('Increases ATK by 5× the level of Potion Research.||When equipped by Merchant Class, All Stats +7.','ATK +5 × niveau de Potion Research.||Merchant Class : All Stats +7.'),
        ii1:fx('Increases ATK by 3× the level of Prepare Potion.||Increases Mammonite damage by 100%.','ATK +3 × niveau de Prepare Potion.||Mammonite : dégâts +100 %.'),
        ii2:fx('Increases ATK by 5× the level of Prepare Potion.||When equipped by Merchant Class, normal melee attacks have a high chance to trigger Bash Lv 10.','ATK +5 × niveau de Prepare Potion.||Merchant Class : les attaques normales au corps-à-corps ont une forte chance de déclencher Bash Lv.10.')},
      {job:'Rogue', names:["Rogue's Essence Lv.1","Rogue's Essence Lv.2","Rogue's Essence II Lv.1","Rogue's Essence II Lv.2"],
        i1:fx('ATK increases by 3× the level of Intimidate.||Increases Sightless Mind damage by 20%.','ATK +3 × niveau d’Intimidate.||Sightless Mind : dégâts +20 %.'),
        i2:fx('ATK increases by 5× the level of Intimidate.||Reduces Sightless Mind SP cost by 15%.','ATK +5 × niveau d’Intimidate.||Sightless Mind : coût en SP -15 %.'),
        ii1:fx('Increases HIT by the level of Gank.||Increases Back Stab damage by 20%.','HIT + niveau de Gank.||Back Stab : dégâts +20 %.'),
        ii2:fx('Increases HIT by 2× the level of Gank.||Increases Back Stab damage by 40%.','HIT +2 × niveau de Gank.||Back Stab : dégâts +40 %.')},
      {job:'Sage', names:["Sage's Essence Lv.1","Sage's Essence Lv.2","Sage's Essence II Lv.1","Sage's Essence II Lv.2"],
        i1:fx('MATK increases by 3× the skill level of Hindsight.||Increases Heaven\'s Drive and Earth Spike damage by 20%.','MATK +3 × niveau de Hindsight.||Heaven\'s Drive et Earth Spike : dégâts +20 %.'),
        i2:fx('MATK increases by 5× the skill level of Hindsight.||Earth Magical Damage +15%.','MATK +5 × niveau de Hindsight.||Earth Magical Damage +15 %.'),
        ii1:fx('Increases MATK by 3× the level of Study.||Increases Fire Bolt, Cold Bolt, and Lightning Bolt damage by 20%.','MATK +3 × niveau de Study.||Fire Bolt, Cold Bolt et Lightning Bolt : dégâts +20 %.'),
        ii2:fx('Increases MATK by 5× the level of Study.||Increases Fire Bolt, Cold Bolt, and Lightning Bolt damage by 40%.','MATK +5 × niveau de Study.||Fire Bolt, Cold Bolt et Lightning Bolt : dégâts +40 %.')},
      {job:'Monk', names:["Monk's Essence Lv.1","Monk's Essence Lv.2","Monk's Essence II Lv.1","Monk's Essence II Lv.2"],
        i1:fx('ATK increases by 3× the level of Demon Bane.||Increases Raging Quadruple Blow damage by 20%.||For every 2 armor refine levels, Raging Thrust damage +5%.','ATK +3 × niveau de Demon Bane.||Raging Quadruple Blow : dégâts +20 %.||Tous les 2 niveaux de refine de l’armure : dégâts de Raging Thrust +5 %.'),
        i2:fx('ATK increases by 5× the level of Demon Bane.||When equipped by Acolyte Class, normal melee attacks have a high chance to trigger Hindsight and Summon Spirit Sphere.','ATK +5 × niveau de Demon Bane.||Acolyte Class : les attaques normales au corps-à-corps ont une forte chance de déclencher Hindsight et Summon Spirit Sphere.'),
        ii1:fx('Reduces Variable Cast Time of Occult Impaction by 3× the level of Demon Bane.||Increases Occult Impaction damage by 20%.||For every 2 refines, Occult Impaction damage +5%.','Variable Cast Time d’Occult Impaction réduit de 3 % × niveau de Demon Bane.||Occult Impaction : dégâts +20 %.||Tous les 2 niveaux de refine : dégâts d’Occult Impaction +5 %.'),
        ii2:fx('Variable Casting Time Reduction of Occult Impaction increases by 5× the level of Demon Bane.||Using Occult Impaction has a high chance to trigger Summon Spirit Sphere.||For every 2 armor refine levels, Occult Impaction damage +5%.','Réduction du Variable Casting Time d’Occult Impaction +5 % × niveau de Demon Bane.||Occult Impaction : forte chance de déclencher Summon Spirit Sphere.||Tous les 2 niveaux de refine de l’armure : dégâts d’Occult Impaction +5 %.')},
      {job:'Bard & Dancer', names:["Bard & Dancer's Essence Lv.1","Bard & Dancer's Essence Lv.2","Bard & Dancer's Essence II Lv.1","Bard & Dancer's Essence II Lv.2"],
        i1:fx('Reduces Amp cooldown by the combined levels of Music Lessons and Dance Lessons.||Reduces Amp cooldown by 60 seconds.||For every 2 armor refine levels, MSP +30.','Cooldown d’Amp réduit selon le total des niveaux de Music Lessons et Dance Lessons.||Cooldown d’Amp -60 secondes.||Tous les 2 niveaux de refine de l’armure : MSP +30.'),
        i2:fx('Reduces Amp cooldown by 3× the combined levels of Music Lessons and Dance Lessons.||When equipped by Archer Class, natural SP Heal effect +50%.','Cooldown d’Amp réduit de 3 × le total des niveaux de Music Lessons et Dance Lessons.||Archer Class : Natural SP Heal effect +50 %.'),
        ii1:fx('Increases ATK by 3× the level of Music Lessons or Dance Lessons.||Increases Melody Strike or Slinging Arrow damage by 20%.||For every 2 refines, Ranged Weapon Physical Damage +1%.','ATK +3 × niveau de Music Lessons ou Dance Lessons.||Melody Strike ou Slinging Arrow : dégâts +20 %.||Tous les 2 niveaux de refine : Ranged Weapon Physical Damage +1 %.'),
        ii2:fx('Increases ATK by 5× the level of Music Lessons or Dance Lessons.||Increases Melody Strike or Slinging Arrow damage by 40%.','ATK +5 × niveau de Music Lessons ou Dance Lessons.||Melody Strike ou Slinging Arrow : dégâts +40 %.')}
    ];
'''

s = s[:first_start] + first_block + s[second_start:]
second_start2 = s.index('    const secondEssences = [', first_start)
second_end2 = s.index('\n    const mdCommonOptions = [', second_start2)
s = s[:second_start2] + second_block + s[second_end2:]

# Exact names present in the supplied current Global client.
s = s.replace("{name:\"Subjugation Team's Boots\", normalSlots:['4th slot']}", "{name:'Subjugation Team Boots', normalSlots:['4th slot']}")
s = s.replace("{name:'Expedition Armor', normalSlots:['4th slot'], essenceSlot:'4th slot', essencePools:['first','second'], open:true}", "{name:\"Expedition's Armor\", normalSlots:['4th slot'], essenceSlot:'4th slot', essencePools:['first','second'], open:true}")
s = s.replace("{name:'Expedition Robe', normalSlots:['4th slot'], essenceSlot:'4th slot', essencePools:['first','second'], open:true}", "{name:\"Expedition's Robe\", normalSlots:['4th slot'], essenceSlot:'4th slot', essencePools:['first','second'], open:true}")

# Grade II / I item names are not present in the supplied current client. Keep the requested pages,
# but do not present old-region item lists as current-client data.
s = re.sub(r"    const mdDispatchingItems = \[.*?\n    \];\n    const mdConquerorItems = \[.*?\n    \];", "    const mdDispatchingItems = [];\n    const mdConquerorItems = [];", s, count=1, flags=re.S)

s = s.replace("intro:navLabel('Dispatching is the Grade II Memorial Dungeon equipment family. The compatible armor-type pieces use the 3rd slot for Job Essence at +9.','Dispatching correspond au Grade II. Les pièces de type armure compatibles utilisent le 3rd slot pour les Job Essence à +9.')", "intro:navLabel('No Grade II equipment entry is present in the current Global client supplied for this wiki.','Aucune entrée d’équipement Grade II n’est présente dans le client Global actuel fourni pour ce wiki.')")
s = s.replace("intro:navLabel('Conqueror is the Grade I Memorial Dungeon equipment family. The compatible armor-type pieces use the 2nd slot for Job Essence at +9.','Conqueror correspond au Grade I. Les pièces de type armure compatibles utilisent le 2nd slot pour les Job Essence à +9.')", "intro:navLabel('No Grade I equipment entry is present in the current Global client supplied for this wiki.','Aucune entrée d’équipement Grade I n’est présente dans le client Global actuel fourni pour ce wiki.')")

# Avoid a misleading rate on a shop purchase.
s = s.replace("<tr><td>${navLabel('Buy Taming Ring','Acheter Taming Ring')}</td><td>—</td><td>50 000 zeny</td><td>100%</td><td>${risk('safe','No','Non')}</td><td>${itemLink('Taming Ring')}</td></tr>", "<tr><td>${navLabel('Buy Taming Ring','Acheter Taming Ring')}</td><td>—</td><td>50 000 zeny</td><td>—</td><td>—</td><td>${itemLink('Taming Ring')}</td></tr>")

# Direct-client regression checks.
checks = [
    "Brandish Spear : dégâts +40 %.",
    "Thief Class : ATK +30.",
    "Swordsman Class : Critical Damage +7 %.",
    "Blitz Beat : dégâts +80 %.",
    "Earth Magical Damage +15 %.",
    "Expedition's Armor",
    "Expedition's Robe",
    "Subjugation Team Boots",
    "const mdDispatchingItems = [];",
    "const mdConquerorItems = [];"
]
for x in checks:
    assert x in s, x

# Old temporary-trigger interpretations must be gone from the enchantment function.
a = s.index('  function enchantmentPage(topic) {')
b = s.index('\n  function monsterSkillsPage(topic) {', a)
section = s[a:b]
for bad in [
    'Pierce: Brandish Spear damage +40% for 60 seconds',
    'Two-Hand Quicken: Critical Damage +7% for 60 seconds',
    'Improve Concentration: Blitz Beat damage +40% for 60 seconds',
    'Sonic Blow: After Attack Delay -7% for 60 seconds',
    'Quagmire: FLEE +30 for 60 seconds'
]:
    assert bad not in section, bad

p.write_text(s, encoding='utf-8')
