from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old_func = re.search(r"  function classIndexView\(\) \{.*?\n  \}\n\n  function officialSources", s, flags=re.S)
if not old_func:
    raise SystemExit('classIndexView not found')

new_func = '''  function classIndexView() {
    const first=['novice','swordman','mage','archer','merchant','thief','acolyte'];
    const second=['knight','crusader','wizard','sage','hunter','bard','dancer','blacksmith','alchemist','assassin','rogue','priest','monk'];
    return `${breadcrumbs([{label:t('classes')}])}
      <div class="article-heading"><div><span class="eyebrow">${navLabel('Character','Personnage')}</span><h1>${icon('class')}${t('classes')}</h1><div class="page-subtitle">${t('fromWiki')}</div></div></div>
      <p class="article-lead">${navLabel('Click anywhere on a class card — the sprite, background or name — to open its dedicated page. First and second classes shown below are currently playable on Ragnarok Zero: Global.','Clique n’importe où sur la case d’une classe — sprite, fond ou nom — pour ouvrir sa page dédiée. Les premières et secondes classes affichées ci-dessous sont actuellement jouables sur Ragnarok Zero: Global.')}</p>
      <div class="notice info-notice"><svg class="notice-icon"><use href="#i-info"></use></svg><div><strong>${navLabel('Current Global content.','Contenu Global actuel.')}</strong> ${navLabel('The thirteen second classes have been available since the September 3, 2026 update. Detailed skill data remains marked unverified until checked against the current Global version.','Les treize secondes classes sont disponibles depuis la mise à jour du 3 septembre 2026. Les données détaillées des skills restent non vérifiées tant qu’elles ne sont pas contrôlées sur la version Global actuelle.')}</div></div>
      ${classProgressionTree(false)}
      <h2>${navLabel('First classes','Premières classes')}</h2>
      <div class="class-directory">${first.map(id=>{const c=getClass(id);return `<a class="class-directory-card" href="#/classes/${id}">${icon('class')}<span><strong>${esc(c.name)}</strong><small>${esc(c.tier)} · ${navLabel('Available','Disponible')}</small></span><span class="class-directory-arrow">→</span></a>`}).join('')}</div>
      <h2>${navLabel('Second classes','Secondes classes')}</h2>
      <div class="class-directory upcoming">${second.map(id=>{const c=getClass(id);return `<a class="class-directory-card" href="#/classes/${id}"><img class="class-directory-sprite" src="${esc(asset(c.image))}" alt=""><span><strong>${esc(c.name)}</strong><small>${esc(c.tier)} · ${navLabel('Available','Disponible')}</small></span><span class="class-directory-arrow">→</span></a>`}).join('')}</div>
    `;
  }

  function officialSources'''

s = s[:old_func.start()] + new_func + s[old_func.end():]

repls = {
"Swordman develops into Knight or Crusader. These second classes are kept in the wiki as upcoming Global content.": "Swordman develops into Knight or Crusader. Both second classes are currently available on Ragnarok Zero: Global.",
"Swordman évolue vers Knight ou Crusader. Ces secondes classes sont conservées dans le wiki comme contenu Global à venir.": "Swordman évolue vers Knight ou Crusader. Ces deux secondes classes sont actuellement disponibles sur Ragnarok Zero: Global.",
"Mage advances to Wizard or Sage from Job Level 40. Both are kept in the wiki as upcoming Global second classes.": "Mage advances to Wizard or Sage from Job Level 40. Both second classes are currently available on Ragnarok Zero: Global.",
"Mage évolue vers Wizard ou Sage à partir du Job Level 40. Les deux sont conservées dans le wiki comme secondes classes Global à venir.": "Mage évolue vers Wizard ou Sage à partir du Job Level 40. Ces deux secondes classes sont actuellement disponibles sur Ragnarok Zero: Global."
}
for old,new in repls.items():
    s = s.replace(old,new)

# Sanity checks: no hard-coded upcoming directory remains for second classes.
assert "const upcoming=['knight'" not in s
assert "<h2>${navLabel('Coming soon','Bientôt disponibles')}</h2>" not in s
assert "Second classes are already shown as upcoming" not in s
assert "secondes classes sont déjà affichées comme contenu à venir" not in s

p.write_text(s, encoding='utf-8')
print('class 2 availability UI fixed')
