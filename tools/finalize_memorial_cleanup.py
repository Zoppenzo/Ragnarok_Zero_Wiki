from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
start = s.index('  function memorialDungeonData() {')
end = s.index('\n  function statusEffectsPage', start)
block = s[start:end]

block = block.replace(
    "          navLabel('Clear the Orc Skeleton, Orc Zombie and Anapholes encounters while progressing through the dungeon.','Élimine les Orc Skeleton, Orc Zombie et Anapholes en progressant dans le donjon.'),",
    "          navLabel('Progress through the instance toward the final encounter.','Progresse dans l’instance jusqu’au combat final.'),"
)

block = block.replace(
    "rewardIntro: navLabel('The completion chest contains dungeon crafting materials and Subjugation equipment. Equipment quantities improve with a party of 7 or more members.','Le coffre de fin contient des matériaux de craft de donjon et de l’équipement Subjugation. Les quantités d’équipement augmentent avec un groupe de 7 membres ou plus.'),",
    "rewardIntro: navLabel('Rewards include dungeon crafting materials and Subjugation equipment. Equipment quantities improve with a party of 7 or more members.','Les récompenses comprennent des matériaux de craft de donjon et de l’équipement Subjugation. Les quantités d’équipement augmentent avec un groupe de 7 membres ou plus.'),"
)

block = block.replace(
    "<h2 id=\"rewards\">${navLabel('Treasure Chest Rewards','Récompenses du coffre')}</h2>",
    "<h2 id=\"rewards\">${navLabel('Rewards','Récompenses')}</h2>",
    1,
)

for banned in [
    'completion chest', 'coffre de fin', 'Treasure Chest Rewards', 'Récompenses du coffre',
    'Clear the Orc Skeleton, Orc Zombie and Anapholes encounters'
]:
    assert banned not in block, banned

s = s[:start] + block + s[end:]
p.write_text(s, encoding='utf-8')
