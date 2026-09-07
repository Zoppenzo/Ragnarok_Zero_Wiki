from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

anchor = "    if (id === 'blacksmith-forging') {"
start = s.index(anchor)
groups_start = s.index("      const groups = [", start)
groups_end = s.index("\n      ];\n      const matHtml", groups_start) + len("\n      ];")

new_groups = r'''      const groups = [
        ['Dagger','Smith Dagger',[
          [1,'Knife',['1 Iron','10 Jellopy']], [1,'Cutter',['25 Iron']], [1,'Main Gauche',['50 Iron']],
          [2,'Dirk',['17 Steel']], [2,'Dagger',['30 Steel']], [2,'Stiletto',['40 Steel']],
          [3,'Gladius',['4 Oridecon','40 Steel','1 Sapphire']], [3,'Damascus',['4 Oridecon','60 Steel','1 Zircon']]
        ]],
        ['Sword','Smith Sword',[
          [1,'Sword',['2 Iron']], [1,'Falchion',['30 Iron']], [1,'Blade',['45 Iron','25 Bat Fang']],
          [2,'Rapier',['20 Steel']], [2,'Scimitar',['35 Steel']], [2,'Ring Pommel Saber',['40 Steel','50 Wolf Claw']],
          [3,'Tsurugi',['8 Oridecon','15 Steel','1 Garnet']], [3,'Saber',['8 Oridecon','5 Steel','1 Opal']],
          [3,'Haedonggum',['8 Oridecon','10 Steel','1 Topaz']]
        ]],
        ['Two-Handed Sword','Smith Two-handed Sword',[
          [1,'Katana',['35 Iron',"15 Dead Man's Tooth"]], [2,'Slayer',['25 Steel',"20 Dead Man's Nail"]], [2,'Bastard Sword',['45 Steel']],
          [3,'Two-Handed Sword',['12 Oridecon','10 Steel']], [3,'Broad Sword',['12 Oridecon','20 Steel']],
          [3,'Claymore',['16 Oridecon','20 Steel','1 Damaged Diamond']]
        ]],
        ['Axe','Smith Axe',[
          [1,'Axe',['10 Iron']], [1,'Battle Axe',['110 Iron']], [2,'Hammer',['30 Steel']],
          [3,'Buster',['4 Oridecon','20 Steel','30 Orc Fang']], [3,'Two-Handed Axe',['8 Oridecon','10 Steel','1 Amethyst']]
        ]],
        ['Mace','Smith Mace',[
          [1,'Club',['3 Iron']], [1,'Mace',['30 Iron']], [2,'Smasher',['20 Steel']], [2,'Flail',['33 Steel']], [2,'Chain',['45 Steel']],
          [3,'Morning Star',['85 Steel','1 Diamond 1-Carat']], [3,'Sword Mace',['100 Steel','20 Sharp Scale']],
          [3,'Stunner',['120 Steel',"1 Orc Warrior's Token"]]
        ]],
        ['Spear','Smith Spear',[
          [1,'Javelin',['3 Iron']], [1,'Spear',['35 Iron']], [1,'Pike',['70 Iron']],
          [2,'Guisarme',['25 Steel']], [2,'Glaive',['40 Steel']], [2,'Partizan',['55 Steel']],
          [3,'Trident',['8 Oridecon','10 Steel','5 Aquamarine']], [3,'Halberd',['12 Oridecon','10 Steel']],
          [3,'Lance',['12 Oridecon','3 Ruby','2 Devil Horn']]
        ]],
        ['Knuckle','Smith Knucklebrace',[
          [1,'Baghnakh',['160 Iron','1 Pearl']], [2,'Knuckle Duster',['50 Steel']], [2,'Hora',['65 Steel']],
          [3,'Fist',['4 Oridecon','10 Ruby']], [3,'Claw',['8 Oridecon','10 Topaz']], [3,'Finger',['4 Oridecon','10 Opal']]
        ]]
      ];'''

s = s[:groups_start] + new_groups + s[groups_end:]

# Client-verified validation from the supplied screenshots.
checks = [
    "[2,'Slayer',['25 Steel',\"20 Dead Man's Nail\"]]",
    "[3,'Two-Handed Axe',['8 Oridecon','10 Steel','1 Amethyst']]",
    "[3,'Stunner',['120 Steel',\"1 Orc Warrior's Token\"]]",
    "[3,'Lance',['12 Oridecon','3 Ruby','2 Devil Horn']]",
    "[1,'Baghnakh',['160 Iron','1 Pearl']]",
    "[2,'Hora',['65 Steel']]",
    "[3,'Claymore',['16 Oridecon','20 Steel','1 Damaged Diamond']]",
]
for x in checks:
    assert x in s, x
for banned in [
    "[2,'Slayer',['24 Steel'",
    "[3,'Two-Handed Axe',['8 Oridecon','20 Steel'",
    "Heroic Emblem",
    "Horrendous Mouth",
    "Decayed Nail",
    "Cracked Diamond",
    "Evil Horn",
    "Waghnak",
    "Knuckle Dusters",
    "Studded Knuckles",
    "Scimiter",
    "[3,'Flamberge'",
]:
    assert banned not in s[start:s.index("\n    if (id === 'npc-recipes')", start)], banned

p.write_text(s, encoding='utf-8')
