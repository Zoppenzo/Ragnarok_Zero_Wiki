from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
orig = s

# Rebuild the live level-cap table so it matches the September 3 state.
pattern = r"  function levelsPage\(topic\) \{\n    const capRows = \[.*?\n    \];\n\n    return `\$\{generalPageHeader\(topic\)\}"
replacement = r'''  function levelsPage(topic) {
    const capRows = [
      [
        navLabel('Base Level','Base Level'),
        '1',
        '60',
        navLabel('Base EXP','Base EXP'),
        navLabel('Overall character progression, stat points and level-gated content.','Progression générale du personnage, points de caractéristiques et contenu soumis à un niveau minimum.')
      ],
      [
        'Novice Job Level',
        '1',
        '10',
        navLabel('Job EXP','Job EXP'),
        navLabel('Unlocks the first job change once the Novice requirements are met.','Permet le premier changement de classe une fois les conditions du Novice remplies.')
      ],
      [
        navLabel('1st Class Job Level','Job Level — 1re classe'),
        '1',
        '50',
        navLabel('Job EXP','Job EXP'),
        navLabel('Grants first-class skill points; second-job change becomes available from Job Level 40.','Accorde les points de skills de première classe ; le changement vers la seconde classe devient disponible à partir du Job Level 40.')
      ],
      [
        navLabel('2nd Class Job Level','Job Level — 2e classe'),
        '1',
        '60',
        navLabel('Job EXP','Job EXP'),
        navLabel('Current second-class progression cap after the September 3 update.','Plafond actuel de progression des secondes classes depuis la mise à jour du 3 septembre.')
      ]
    ];

    return `${generalPageHeader(topic)}'''
s2, n = re.subn(pattern, replacement, s, count=1, flags=re.S)
if n != 1:
    raise SystemExit(f'Could not rebuild level cap table: matches={n}')
s = s2

# Add the second-class Job Level progression note directly in the Job Level section.
needle = "        <li>${navLabel('Each Job Level gained after Job Level 1 provides one skill point. Reaching Job Level 50 therefore provides 49 points for the current first-class tree.','Chaque Job Level gagné après le Job Level 1 fournit un point de compétence. Atteindre le Job Level 50 donne donc 49 points pour l’arbre actuel de la première classe.')}</li>"
addition = needle + "\n        <li>${navLabel('After changing to a second class, that class has its own Job Level progression; the current Global second-class Job Level cap is 60.','Après le passage en seconde classe, cette classe possède sa propre progression de Job Level ; le plafond Global actuel des secondes classes est Job Level 60.')}</li>"
if needle not in s:
    raise SystemExit('Job Level progression bullet not found')
s = s.replace(needle, addition, 1)

# Put the official September update at the top of the Levels sources.
needle_sources = "      ${officialSources([\n        ['ROZ Database — Global release roadmap','https://rozerodb.com/guides/roadmap-update'],"
repl_sources = "      ${officialSources([\n        ['Official GNJOY — September 3 update: 2nd Jobs / increased level cap','https://roz.mygnjoy.com/en/news/update/92'],\n        ['ROZ Database — Global release roadmap','https://rozerodb.com/guides/roadmap-update'],"
if needle_sources not in s:
    raise SystemExit('Levels source block not found')
s = s.replace(needle_sources, repl_sources, 1)

# Make the English footer wording consistent with the French/static wording.
s = s.replace(
    "footer: 'Only verified or explicitly qualified data should be treated as gameplay reference.'",
    "footer: 'Some database sections are still being documented. Verification status is shown on each section.'",
    1
)

# Clarify branding in the welcome copy.
s = s.replace(
    "welcomeText: 'A bilingual community reference for Ragnarok Online. Game entities keep their English names; the interface and explanatory text can switch between English and French.'",
    "welcomeText: 'A bilingual community reference for Ragnarok Zero: Global. Game entities keep their English names; the interface and explanatory text can switch between English and French.'",
    1
)
s = s.replace(
    'welcomeText: "Une référence communautaire bilingue pour Ragnarok Online. Les noms des éléments du jeu restent en anglais ; l\'interface et les explications peuvent passer entre anglais et français."',
    'welcomeText: "Une référence communautaire bilingue pour Ragnarok Zero: Global. Les noms des éléments du jeu restent en anglais ; l\'interface et les explications peuvent passer entre anglais et français."',
    1
)

# Integrity checks.
assert "navLabel('Base Level','Base Level'),\n        '1',\n        '60'" in s
assert "navLabel('2nd Class Job Level','Job Level — 2e classe')" in s
assert "Current Global scope — 6 September 2026" in s
for cid in ['knight','crusader','wizard','sage','hunter','bard','dancer','blacksmith','alchemist','assassin','rogue','priest','monk']:
    pos = s.find(f'id: "{cid}"')
    assert pos >= 0
    line = s[pos:s.find('\n', pos)]
    assert 'releaseStatus: "available"' in line

if s == orig:
    raise SystemExit('No changes made')
p.write_text(s, encoding='utf-8')
print('Final level-cap consistency fixes applied')
