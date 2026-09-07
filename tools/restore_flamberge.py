from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
old = "          [3,'Tsurugi',['8 Oridecon','15 Steel','1 Garnet']], [3,'Saber',['8 Oridecon','5 Steel','1 Opal']],\n          [3,'Haedonggum',['8 Oridecon','10 Steel','1 Topaz']]"
new = "          [3,'Tsurugi',['8 Oridecon','15 Steel','1 Garnet']], [3,'Saber',['8 Oridecon','5 Steel','1 Opal']],\n          [3,'Haedonggum',['8 Oridecon','10 Steel','1 Topaz']], [3,'Flamberge',['16 Oridecon','1 Cursed Ruby']]"
assert old in s, 'Sword forging block not found'
s = s.replace(old, new, 1)
assert "[3,'Flamberge',['16 Oridecon','1 Cursed Ruby']]" in s
p.write_text(s, encoding='utf-8')
