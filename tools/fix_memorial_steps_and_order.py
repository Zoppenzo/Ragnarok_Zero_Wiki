from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Poring Village enchant reset: correct cost and failure behavior.
old = "reset: navLabel('Reset costs 200,000 zeny. Enchanting and resetting each have a 30% failure chance; on failure the item is destroyed.','Le reset coûte 200 000 zeny. L’enchantement et le reset ont chacun 30 % de risque d’échec ; en cas d’échec l’objet est détruit.'),"
new = "reset: navLabel('Reset costs 50 Jellopy + 20,000 zeny. Enchanting and resetting each have a 30% failure chance; failure does not destroy the item.','Le reset coûte 50 Jellopy + 20 000 zeny. L’enchantement et le reset ont chacun 30 % de risque d’échec ; un échec ne détruit pas l’objet.'),"
assert old in s
s = s.replace(old, new, 1)

# Orc's Memory: Shaman's Flowers must be destroyed, not controlled.
old = "navLabel(\"At the final encounter, destroy or control the Shaman's Flowers so they do not keep strengthening Fallen Orc Hero.\",\"Lors du combat final, détruis ou contrôle les Shaman's Flowers afin qu’elles ne continuent pas à renforcer Fallen Orc Hero.\"),"
new = "navLabel(\"At the final encounter, destroy the Shaman's Flowers so they do not keep strengthening Fallen Orc Hero.\",\"Lors du combat final, détruis les Shaman's Flowers afin qu’elles ne continuent pas à renforcer Fallen Orc Hero.\"),"
assert old in s
s = s.replace(old, new, 1)

# Orc's Memory: reward chest is collected before leaving the instance.
old = "navLabel('Leave the instance, then destroy the dungeon to receive the rewards.','Sors de l’instance, puis détruis le donjon pour recevoir les récompenses.')"
new = "navLabel('Collect the rewards from the chest before leaving the instance.','Récupère les récompenses dans le coffre avant de sortir de l’instance.')"
# First occurrence is Poring, second is Orc, third is GTB. Replace Orc only.
first = s.find(old)
assert first != -1
second = s.find(old, first + 1)
assert second != -1
s = s[:second] + s[second:].replace(old, new, 1)

# Prontera Culvert / GTB: step 4 is reward chest before leaving.
third = s.find(old, second + len(new))
assert third != -1
s = s[:third] + s[third:].replace(old, new, 1)

# Swap MVP Raid and Memorial Dungeon positions in Systems & Mechanics.
old_nav = "    { id:'memorial-dungeons', group:'Systems & Mechanics', en:'Memorial Dungeon', fr:'Mémorial Donjon', href:'#/memorial-dungeons', icon:'memorial' },\n    { id:'mvp-raid', group:'Systems & Mechanics', en:'MVP Raid', fr:'Raid MVP' },"
new_nav = "    { id:'mvp-raid', group:'Systems & Mechanics', en:'MVP Raid', fr:'Raid MVP' },\n    { id:'memorial-dungeons', group:'Systems & Mechanics', en:'Memorial Dungeon', fr:'Mémorial Donjon', href:'#/memorial-dungeons', icon:'memorial' },"
assert old_nav in s
s = s.replace(old_nav, new_nav, 1)

# Validate only the Memorial Dungeon block for the requested corrections.
a = s.index('  function memorialDungeonData() {')
b = s.index('\n  function statusEffectsPage', a)
m = s[a:b]
assert 'Reset costs 50 Jellopy + 20,000 zeny' in m
assert 'Le reset coûte 50 Jellopy + 20 000 zeny' in m
assert 'failure does not destroy the item' in m
assert 'un échec ne détruit pas l’objet' in m
assert 'destroy or control' not in m
assert 'détruis ou contrôle' not in m
assert m.count('Collect the rewards from the chest before leaving the instance.') == 2
assert m.count('Récupère les récompenses dans le coffre avant de sortir de l’instance.') == 2
assert s.index("{ id:'mvp-raid', group:'Systems & Mechanics'") < s.index("{ id:'memorial-dungeons', group:'Systems & Mechanics'")

p.write_text(s, encoding='utf-8')
