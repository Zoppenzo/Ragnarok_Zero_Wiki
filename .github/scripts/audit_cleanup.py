from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
index_path = ROOT / "index.html"
text = index_path.read_text(encoding="utf-8")

# Audit date.
text = text.replace("Audit du contenu : 6 sept. 2026.", "Audit du contenu : 8 sept. 2026.")

# Pet List: body has Pet + Bonus + Taming Item + Drop Source, so the header must
# have the same four columns.
text = re.sub(
    r"(<thead><tr>\s*<th>Pet</th>\s*)(<th>Taming Item</th>\s*<th>\$\{navLabel\('Drop source','Source de drop'\)\}</th>)",
    r"\1<th>${navLabel('Bonus','Bonus')}</th>\n          \2",
    text,
    count=1,
)

# Skill level tables: the user explicitly asked to remove the per-level Effect
# column. Keep only the useful official-client values.
text = text.replace("navLabel('Effects by level','Effets par niveau')", "navLabel('Level data','Données par niveau')")
text = re.sub(r"\s*<th>\$\{navLabel\('Effect','Effet'\)\}</th>\n", "\n", text, count=1)
text = re.sub(r"\s*<td>\$\{esc\(row\.effect\)\}</td>\n", "\n", text, count=1)

# The old hand-maintained per-level tables are no longer authoritative for the
# generic first-job skill page. Official client data is loaded by client-sync.
state_pattern = re.compile(
    r"    const rows = wikiSkillLevelData\(sk\.id\);\s*"
    r"const hasDetailedLevels = !!rows;\s*"
    r"const effectLevelRows = skillLevelEffectRows\(sk\);\s*"
    r"const hasEffectLevels = effectLevelRows\.length > 0;"
)
state_replacement = """    const rows = null; // legacy manual table intentionally bypassed
    const hasDetailedLevels = false;
    const effectLevelRows = skillLevelEffectRows(sk);
    const hasEffectLevels = effectLevelRows.length > 0;
    const hasClientData = !!(window.RZ_CLIENT_SKILL_FOR && window.RZ_CLIENT_SKILL_FOR(sk));
    const hasFormulaSection = skillDamageFormulaData(sk).type !== 'none';"""
text = state_pattern.sub(state_replacement, text, count=1)

# Non-damaging/passive skills should not show a meaningless Damage Formula box.
text = re.sub(
    r"    if \(data\.type === 'none'\) \{\s*"
    r"return `<h2 id=\"formula\">\$\{navLabel\('Damage formula','Formule des dégâts'\)\}</h2>\s*"
    r"<div class=\"notes-box\">\$\{navLabel\(data\.en,data\.fr\)\}</div>`;\s*"
    r"\}",
    "    if (data.type === 'none') return '';",
    text,
    count=1,
)

# Hide Formula in the generic skill TOC when there is no formula section.
text = text.replace(
    "            {id:'formula',label:navLabel('Damage formula','Formule des dégâts')},\n",
    "            ...(hasFormulaSection ? [{id:'formula',label:navLabel('Damage formula','Formule des dégâts')}] : []),\n",
    1,
)

# Sources now depend on the official client record rather than the legacy table.
text = text.replace(
    "            ...(hasDetailedLevels ? [{id:'sources',label:navLabel('Sources','Sources')}] : [])",
    "            ...(hasClientData ? [{id:'sources',label:navLabel('Sources','Sources')}] : [])",
    1,
)
text = text.replace(
    "          ${hasDetailedLevels ? `<h2 id=\"sources\">",
    "          ${hasClientData ? `<h2 id=\"sources\">",
    1,
)

# Add the structural/mechanics reference when Notes are present.
iro_marker = "RagnaPlace — fixed / variable / global delay tables</a></li>' : ''}"
if iro_marker in text and "iRO Wiki — additional gameplay mechanics reference" not in text:
    text = text.replace(
        iro_marker,
        iro_marker + "\n            ${Array.isArray(sk.noteList) && sk.noteList.length ? '<li><a href=\"https://irowiki.org/wiki/Skills\" target=\"_blank\" rel=\"noopener\">iRO Wiki — additional gameplay mechanics reference</a></li>' : ''}",
        1,
    )

# Basic Skill is a special page and had its own useless formula entry/section.
text = text.replace(
    "${toc([{id:'levels',label:navLabel('Levels','Niveaux')},{id:'formula',label:navLabel('Damage formula','Formule des dégâts')},{id:'notes',label:t('notes')},{id:'sources',label:navLabel('Sources','Sources')}])}",
    "${toc([{id:'levels',label:navLabel('Levels','Niveaux')},{id:'notes',label:t('notes')},{id:'sources',label:navLabel('Sources','Sources')}])}",
)
text = re.sub(
    r"\s*<h2 id=\"formula\">\$\{navLabel\('Damage formula','Formule des dégâts'\)\}</h2>\s*"
    r"<div class=\"notes-box\">\$\{navLabel\('Basic Skill does not inflict damage, so it has no direct damage formula\.','Basic Skill n’inflige pas de dégâts ; elle n’a donc pas de formule de dégâts directe\.'\)\}</div>\n",
    "\n",
    text,
    count=1,
)

# Remove the broad full-app MutationObserver. The editor already refreshes on
# initial load, route changes and language changes.
text = re.sub(
    r"  const pageObserver = new MutationObserver\(\(\) => preparePage\(\)\);\s*"
    r"pageObserver\.observe\(app, \{ childList: true, subtree: true \}\);\s*",
    "  // Full-app subtree observer removed; explicit lifecycle refreshes are used.\n\n",
    text,
    count=1,
)

# Remove obsolete/misleading files from the repository checkout. `git add -A`
# in the workflow records these deletions.
for obsolete in (
    ROOT / "assets/client-data/skills.zlib.b64",
    ROOT / "assets/database/memorial-dungeon.gif",
):
    obsolete.unlink(missing_ok=True)

# Guardrails: fail only after all resilient transformations have been attempted.
checks = {
    "Pet List Bonus header": "<th>${navLabel('Bonus','Bonus')}</th>" in text,
    "Level data label": "navLabel('Level data','Données par niveau')" in text,
    "Effect header removed": "<th>${navLabel('Effect','Effet')}</th>" not in text,
    "Effect cell removed": "<td>${esc(row.effect)}</td>" not in text,
    "French audit date": "Audit du contenu : 8 sept. 2026." in text,
    "Formula hidden for non-damage": "if (data.type === 'none') return '';" in text,
    "Formula TOC condition": "const hasFormulaSection = skillDamageFormulaData(sk).type !== 'none';" in text,
    "Legacy rows bypassed": "const rows = null; // legacy manual table intentionally bypassed" in text,
    "Full-app observer removed": "const pageObserver = new MutationObserver" not in text,
}
failed = [name for name, ok in checks.items() if not ok]
if failed:
    raise RuntimeError("Audit cleanup validation failed: " + ", ".join(failed))

index_path.write_text(text, encoding="utf-8")
print("Audit cleanup applied successfully.")
