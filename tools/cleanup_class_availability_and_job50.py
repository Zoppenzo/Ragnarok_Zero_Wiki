from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Catch the remaining first-job notes using the compact spelling.
s = s.replace('Job Lv.40', 'Job Lv.50')

# Second-class descriptions: availability is implicit; keep only class relation.
s = s.replace(' is a currently playable second class branching from ', ' is a second class branching from ')
s = s.replace(' est une seconde classe actuellement jouable issue de ', ' est une seconde classe issue de ')

# Second-class notes: keep the verification note, remove redundant release-status sentence.
s = s.replace('Available since the September 3, 2026 update. ', '')
s = s.replace('Disponible depuis la mise à jour du 3 septembre 2026. ', '')

# Classes directory: no need to restate that classes are playable/available.
old_lead = "${navLabel('Click anywhere on a class card — the sprite, background or name — to open its dedicated page. First and second classes shown below are currently playable on Ragnarok Zero: Global.','Clique n’importe où sur la case d’une classe — sprite, fond ou nom — pour ouvrir sa page dédiée. Les premières et secondes classes affichées ci-dessous sont actuellement jouables sur Ragnarok Zero: Global.')}"
new_lead = "${navLabel('Click anywhere on a class card — the sprite, background or name — to open its dedicated page.','Clique n’importe où sur la case d’une classe — sprite, fond ou nom — pour ouvrir sa page dédiée.')}"
if old_lead not in s:
    raise SystemExit('Class index lead not found')
s = s.replace(old_lead, new_lead, 1)

old_notice = "      <div class=\"notice info-notice\"><svg class=\"notice-icon\"><use href=\"#i-info\"></use></svg><div><strong>${navLabel('Current Global content.','Contenu Global actuel.')}</strong> ${navLabel('The thirteen second classes have been available since the September 3, 2026 update. Detailed skill data remains marked unverified until checked against the current Global version.','Les treize secondes classes sont disponibles depuis la mise à jour du 3 septembre 2026. Les données détaillées des skills restent non vérifiées tant qu’elles ne sont pas contrôlées sur la version Global actuelle.')}</div></div>\n"
new_notice = "      <div class=\"notice info-notice\"><svg class=\"notice-icon\"><use href=\"#i-info\"></use></svg><div>${navLabel('Detailed second-class skill data remains marked unverified until checked against the current Global version.','Les données détaillées des skills de secondes classes restent non vérifiées tant qu’elles ne sont pas contrôlées sur la version Global actuelle.')}</div></div>\n"
if old_notice not in s:
    raise SystemExit('Class index notice not found')
s = s.replace(old_notice, new_notice, 1)

# Generic second-class page message: remove redundant playable statement.
s = s.replace(
    "This class is playable. Its detailed skill tree is intentionally left unverified until the current Global values are documented; data from other RO versions is not substituted.",
    "Its detailed skill tree is intentionally left unverified until the current Global values are documented; data from other RO versions is not substituted."
)
s = s.replace(
    "Cette classe est jouable. Son arbre de skills détaillé reste volontairement non vérifié tant que les valeurs Global actuelles ne sont pas documentées ; les données des autres versions de RO ne sont pas utilisées à la place.",
    "Son arbre de skills détaillé reste volontairement non vérifié tant que les valeurs Global actuelles ne sont pas documentées ; les données des autres versions de RO ne sont pas utilisées à la place."
)

# Levels page: keep only useful progression facts, not availability reminders.
s = s.replace(
    'Since the September 3 update, the live cap is Base Level 60 / Job Level 60 and the thirteen second classes are available. Novice still changes to a first class from Job Level 10, and first classes can change to their second-job path from Job Level 50. Future cap increases are not mixed into this live table.',
    'Since the September 3 update, the live cap is Base Level 60 / Job Level 60. Novice still changes to a first class from Job Level 10, and first classes change to their second-job path at Job Level 50. Future cap increases are not mixed into this live table.'
)
s = s.replace(
    'Depuis la mise à jour du 3 septembre, le plafond live est Base Level 60 / Job Level 60 et les treize secondes classes sont disponibles. Le Novice change toujours vers une première classe à partir du Job Level 10, puis les premières classes peuvent passer vers leur seconde classe à partir du Job Level 50. Les futures hausses de niveau ne sont pas mélangées à ce tableau du contenu live.',
    'Depuis la mise à jour du 3 septembre, le plafond live est Base Level 60 / Job Level 60. Le Novice change toujours vers une première classe à partir du Job Level 10, puis les premières classes passent vers leur seconde classe au Job Level 50. Les futures hausses de niveau ne sont pas mélangées à ce tableau du contenu live.'
)

# Experience page wording.
s = s.replace(
    'This table applies to the currently available first classes: Swordman, Mage, Archer, Merchant, Thief and Acolyte.',
    'This table applies to the first classes: Swordman, Mage, Archer, Merchant, Thief and Acolyte.'
)
s = s.replace(
    'Ce tableau s’applique aux premières classes actuellement disponibles : Swordman, Mage, Archer, Merchant, Thief et Acolyte.',
    'Ce tableau s’applique aux premières classes : Swordman, Mage, Archer, Merchant, Thief et Acolyte.'
)

# Validation of the user's requested progression value.
assert 'Job Lv.40' not in s
assert 'Job Level 40' not in s
assert 'Job Lv 40+' not in s
assert '2e classe — bientôt disponible' not in s

p.write_text(s, encoding='utf-8')
print('Cleaned redundant class availability text and all remaining Job 40 references.')
