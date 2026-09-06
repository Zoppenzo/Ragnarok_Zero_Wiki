from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Make the second-class cap explicit in generic second-class infoboxes.
old = "${infoRow(t('tier'),String(c.tier))}${infoRow(t('parentClass')"
new = "${infoRow(t('tier'),String(c.tier))}${c.group==='second'?infoRow(navLabel('Max Base Level','Base Level max'),'60'):''}${c.group==='second'?infoRow(navLabel('Max Job Level','Job Level max'),'60'):''}${infoRow(t('parentClass')"
if s.count(old) != 1:
    raise SystemExit(f'Expected one generic class infobox marker, found {s.count(old)}')
s = s.replace(old, new, 1)

# Clarify the distinction between the first-class change requirement and the second-class cap.
s = s.replace(
    'Since the September 3 update, the live cap is Base Level 60 / Job Level 60. Novice still changes to a first class from Job Level 10, and first classes change to their second-job path at Job Level 50. Future cap increases are not mixed into this live table.',
    'Since the September 3 update, second-class characters can reach Base Level 60 / Job Level 60. Job Level 50 is only the first-class requirement to change into a second class; after the job change, Job Level restarts at 1 and can reach 60. Future cap increases are not mixed into this live table.'
)
s = s.replace(
    'Depuis la mise à jour du 3 septembre, le plafond live est Base Level 60 / Job Level 60. Le Novice change toujours vers une première classe à partir du Job Level 10, puis les premières classes passent vers leur seconde classe au Job Level 50. Les futures hausses de niveau ne sont pas mélangées à ce tableau du contenu live.',
    'Depuis la mise à jour du 3 septembre, les personnages de seconde classe peuvent atteindre Base Level 60 / Job Level 60. Le Job Level 50 est uniquement le prérequis de la première classe pour passer en seconde classe ; après le changement, le Job Level repart à 1 et peut monter jusqu’à 60. Les futures hausses de niveau ne sont pas mélangées à ce tableau du contenu live.'
)

old_block = '''      <h2 id="job-change">${navLabel('Current job-change progression','Progression actuelle des changements de classe')}</h2>
      <div class="wiki-feature-list">
        <div><strong>1. Novice</strong><p>${navLabel('Base Level progresses normally; raise Job Level from 1 to 10.','Le Base Level progresse normalement ; monte le Job Level de 1 à 10.')}</p></div>
        <div><strong>2. Job Level 10</strong><p>${navLabel('Complete the chosen first-job change and become Swordman, Mage, Archer, Merchant, Thief or Acolyte.','Effectue le changement vers la première classe choisie : Swordman, Mage, Archer, Merchant, Thief ou Acolyte.')}</p></div>
        <div><strong>3. 1st Class</strong><p>${navLabel('Job Level restarts at 1. Earn Job EXP and spend the resulting skill points in the class tree.','Le Job Level repart à 1. Gagne de la Job EXP et dépense les points obtenus dans l’arbre de la classe.')}</p></div>
        <div><strong>4. ${navLabel('Current cap','Plafond actuel')}</strong><p>${navLabel('Base Level 60 / Job Level 60 are the current live limits documented by this page; second classes are now playable.','Base Level 60 / Job Level 60 sont les limites live actuellement documentées par cette page ; les secondes classes sont désormais jouables.')}</p></div>
      </div>
'''
new_block = '''      <h2 id="job-change">${navLabel('Current job-change progression','Progression actuelle des changements de classe')}</h2>
      <div class="wiki-feature-list">
        <div><strong>1. Novice</strong><p>${navLabel('Base Level progresses normally; raise Job Level from 1 to 10.','Le Base Level progresse normalement ; monte le Job Level de 1 à 10.')}</p></div>
        <div><strong>2. Job Level 10</strong><p>${navLabel('Complete the chosen first-job change and become Swordman, Mage, Archer, Merchant, Thief or Acolyte.','Effectue le changement vers la première classe choisie : Swordman, Mage, Archer, Merchant, Thief ou Acolyte.')}</p></div>
        <div><strong>3. 1st Class</strong><p>${navLabel('Job Level restarts at 1 and can reach Job Level 50.','Le Job Level repart à 1 et peut monter jusqu’au Job Level 50.')}</p></div>
        <div><strong>4. Job Level 50</strong><p>${navLabel('Change into the chosen second class. Base Level does not reset; Job Level restarts at 1.','Passe dans la seconde classe choisie. Le Base Level ne repart pas à zéro ; le Job Level repart à 1.')}</p></div>
        <div><strong>5. 2nd Class</strong><p>${navLabel('The current cap for a second-class character is Base Level 60 / Job Level 60.','Le plafond actuel d’un personnage de seconde classe est Base Level 60 / Job Level 60.')}</p></div>
      </div>
'''
if old_block not in s:
    raise SystemExit('Job-change progression block not found')
s = s.replace(old_block, new_block, 1)

# Experience page: make 60/60 explicitly second-class, not just a global shorthand.
s = s.replace(
    'The current live cap documented by this wiki is Base Level 60 / Job Level 60 following the September 3 update, with second classes now available. See the Levels page for the progression flow and current cap.',
    'For a second-class character, the current live cap documented by this wiki is Base Level 60 / Job Level 60 following the September 3 update. See the Levels page for the full progression flow.'
)
s = s.replace(
    'Le plafond live documenté par ce wiki est désormais Base Level 60 / Job Level 60 depuis la mise à jour du 3 septembre, avec les secondes classes disponibles. Consulte la page Niveaux pour le chemin de progression et le plafond actuel.',
    'Pour un personnage de seconde classe, le plafond live documenté par ce wiki est Base Level 60 / Job Level 60 depuis la mise à jour du 3 septembre. Consulte la page Niveaux pour le chemin de progression complet.'
)

# Validation: Job 50 remains the first-class requirement, while second class is clearly 60/60.
assert "navLabel('2nd Class Job Level','Job Level — 2e classe'),\n        '1',\n        '60'" in s
assert "c.group==='second'?infoRow(navLabel('Max Job Level','Job Level max'),'60')" in s
assert 'Le plafond actuel d’un personnage de seconde classe est Base Level 60 / Job Level 60.' in s
assert 'Base Level 60 / Job Level 50' not in s

p.write_text(s, encoding='utf-8')
print('Second-class cap clarified as Base 60 / Job 60.')
