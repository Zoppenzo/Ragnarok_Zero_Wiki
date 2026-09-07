from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="""      (d.headgear || []).forEach(h=> out.items[memorialDbSlug(h.name)] = h.name);\n    });"""
new="""      (d.headgear || []).forEach(h=> out.items[memorialDbSlug(h.name)] = h.name);\n      if (d.enchant) out.items[memorialDbSlug('Jellopy')] = 'Jellopy';\n    });"""
assert old in s
s=s.replace(old,new,1)
old2="""    const enchant = d.enchant ? `<h2 id=\"enchant\">${navLabel('Headgear enchant','Enchantement du Headgear')}</h2>\n      <ul><li>${esc(d.enchant.cost)}</li><li>${esc(d.enchant.reset)}</li>${(d.enchant.rules||[]).map(x=>`<li>${esc(x)}</li>`).join('')}</ul>"""
new2="""    const enchantCost = d.enchant ? esc(d.enchant.cost).replace('Jellopy', memorialDbLink('items','Jellopy')) : '';\n    const enchant = d.enchant ? `<h2 id=\"enchant\">${navLabel('Headgear enchant','Enchantement du Headgear')}</h2>\n      <ul><li>${enchantCost}</li><li>${esc(d.enchant.reset)}</li>${(d.enchant.rules||[]).map(x=>`<li>${esc(x)}</li>`).join('')}</ul>"""
assert old2 in s
s=s.replace(old2,new2,1)
p.write_text(s,encoding='utf-8')
