from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# 1) Class tree: remove availability labels and obsolete coming-soon wording.
s = s.replace("${navLabel('2nd Class — coming soon','2e classe — bientôt disponible')}", "${navLabel('2nd Class','2e classe')}")

old_badge = '''  function classStatusBadge(c) {
    return c?.releaseStatus === 'coming-soon'
      ? `<span class=\"class-status-badge coming\">${navLabel('Coming soon','Bientôt')}</span>`
      : `<span class=\"class-status-badge live\">${navLabel('Available','Disponible')}</span>`;
  }
'''
if old_badge not in s:
    raise SystemExit('classStatusBadge block not found')
s = s.replace(old_badge, "  function classStatusBadge(c) {\n    return '';\n  }\n", 1)

# Remove Available/Disponible from class directory cards.
s = s.replace("${esc(c.tier)} · ${navLabel('Available','Disponible')}", "${esc(c.tier)}")

# Remove status rows from class infoboxes; class availability is no longer useful UI.
s = s.replace("            ${infoRow(t('status'),navLabel('Available','Disponible'))}\n", "")
s = s.replace("${infoRow(t('status'),status)}", "")

# 2) Correct second-job requirement: first class must reach Job Level 50.
s = s.replace('Job Level 40', 'Job Level 50')
s = s.replace('Job Lv 40+', 'Job Lv 50+')

# 3) Experience tables order: Novice first, then Base 1-50, then first-class Job 1-50.
def table_block(marker: str):
    start = s.find(marker)
    if start == -1:
        raise SystemExit(f'Marker not found: {marker}')
    end_marker = '</table></div>'
    end = s.find(end_marker, start)
    if end == -1:
        raise SystemExit(f'Table end not found after: {marker}')
    end += len(end_marker)
    return start, end, s[start:end]

base_marker = "      <h3>${navLabel('Base Level EXP — Lv. 1 to 50','Base Level EXP — Nv. 1 à 50')}</h3>"
novice_marker = "      <h3>${navLabel('Novice Job EXP — Job Lv. 1 to 10','Job EXP Novice — Job Nv. 1 à 10')}</h3>"
first_marker = "      <h3>${navLabel('First Class Job EXP — Job Lv. 1 to 50','Job EXP des premières classes — Job Nv. 1 à 50')}</h3>"

b0,b1,base_block = table_block(base_marker)
n0,n1,novice_block = table_block(novice_marker)
f0,f1,first_block = table_block(first_marker)
if not (b0 < n0 < f0):
    raise SystemExit(f'Unexpected EXP table order before patch: base={b0}, novice={n0}, first={f0}')

replacement = novice_block + '\n\n' + base_block + '\n\n' + first_block
s = s[:b0] + replacement + s[f1:]

# Validation.
assert "2nd Class — coming soon" not in s
assert "2e classe — bientôt disponible" not in s
assert "class-status-badge live" not in s[s.find('function classStatusBadge'):s.find('function classTreeNode')]
assert 'Job Level 40' not in s
assert 'Job Lv 40+' not in s

# Verify final EXP order in the Experience page.
nb = s.find(novice_marker)
bb = s.find(base_marker)
fb = s.find(first_marker)
assert nb != -1 and bb != -1 and fb != -1 and nb < bb < fb

p.write_text(s, encoding='utf-8')
print('Patched class labels, Job 50 requirement and EXP table order.')
