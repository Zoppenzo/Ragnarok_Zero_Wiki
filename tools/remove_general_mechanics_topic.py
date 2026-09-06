from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
old = "    { id:'mechanics', group:'General Topics', en:'Game Mechanics', fr:'Mécaniques de jeu', icon:'mechanics' },\n"
count = s.count(old)
if count != 1:
    raise SystemExit(f'Expected exactly one General Topics mechanics entry, found {count}')
s = s.replace(old, '')
if "id:'mechanics', group:'General Topics'" in s:
    raise SystemExit('Mechanics topic still present in General Topics')
p.write_text(s, encoding='utf-8')
print('Removed unwanted Game Mechanics topic from General Topics.')
