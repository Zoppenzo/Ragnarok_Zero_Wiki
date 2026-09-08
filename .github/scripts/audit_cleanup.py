from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
index_path = ROOT / "index.html"
text = index_path.read_text(encoding="utf-8")


def replace_once(old: str, new: str, label: str) -> None:
    global text
    if old in text:
        text = text.replace(old, new, 1)
        return
    if new in text:
        return
    raise RuntimeError(f"Could not apply cleanup: {label}")


# ---------------------------------------------------------------------------
# Audit metadata / small correctness fixes
# ---------------------------------------------------------------------------
text = text.replace(
    "Audit du contenu : 6 sept. 2026.",
    "Audit du contenu : 8 sept. 2026.",
)

# Pet List had four body cells but only three headers.
pet_header_old = """        <thead><tr>
          <th>Pet</th>
          <th>Taming Item</th>
          <th>${navLabel('Drop source','Source de drop')}</th>
        </tr></thead>"""
pet_header_new = """        <thead><tr>
          <th>Pet</th>
          <th>${navLabel('Bonus','Bonus')}</th>
          <th>Taming Item</th>
          <th>${navLabel('Drop source','Source de drop')}</th>
        </tr></thead>"""
replace_once(pet_header_old, pet_header_new, "Pet List table header")


# ---------------------------------------------------------------------------
# Skill pages: official client is authoritative for level data.
# The user explicitly does not want an Effect column because it was usually
# empty/redundant. Keep only Level, SP, Range, Cast, Cast Delay and Cooldown.
# ---------------------------------------------------------------------------
text = text.replace(
    "navLabel('Effects by level','Effets par niveau')",
    "navLabel('Level data','Données par niveau')",
)
text = text.replace("          <th>${navLabel('Effect','Effet')}</th>\n", "")
text = text.replace("          <td>${esc(row.effect)}</td>\n", "")

# Stop using the old hand-maintained per-level table as an authority in the
# generic first-job skill page. The client synchronizer supplies the values.
replace_once(
    """    const rows = wikiSkillLevelData(sk.id);
    const hasDetailedLevels = !!rows;
    const effectLevelRows = skillLevelEffectRows(sk);
    const hasEffectLevels = effectLevelRows.length > 0;""",
    """    const rows = null; // legacy manual table intentionally bypassed
    const hasDetailedLevels = false;
    const effectLevelRows = skillLevelEffectRows(sk);
    const hasEffectLevels = effectLevelRows.length > 0;
    const hasClientData = !!(window.RZ_CLIENT_SKILL_FOR && window.RZ_CLIENT_SKILL_FOR(sk));
    const hasFormulaSection = skillDamageFormulaData(sk).type !== 'none';""",
    "client-first skill detail state",
)

# Passive/non-damaging skills should not display a pointless Damage Formula box.
formula_none_old = """    if (data.type === 'none') {
      return `<h2 id=\"formula\">${navLabel('Damage formula','Formule des dégâts')}</h2>
        <div class=\"notes-box\">${navLabel(data.en,data.fr)}</div>`;
    }"""
formula_none_new = """    if (data.type === 'none') return '';"""
replace_once(formula_none_old, formula_none_new, "hide formula for non-damaging skills")

# The TOC must also hide the Formula entry when there is no formula section.
replace_once(
    "            {id:'formula',label:navLabel('Damage formula','Formule des dégâts')},\n",
    "            ...(hasFormulaSection ? [{id:'formula',label:navLabel('Damage formula','Formule des dégâts')}] : []),\n",
    "conditional formula TOC entry",
)

# Sources should follow the official client record, not the legacy manual table.
text = text.replace(
    "            ...(hasDetailedLevels ? [{id:'sources',label:navLabel('Sources','Sources')}] : [])",
    "            ...(hasClientData ? [{id:'sources',label:navLabel('Sources','Sources')}] : [])",
)
text = text.replace(
    "          ${hasDetailedLevels ? `<h2 id=\"sources\">",
    "          ${hasClientData ? `<h2 id=\"sources\">",
)

# Notes are compatibility-checked gameplay remarks; expose iRO as the structural
# / mechanics reference whenever a skill actually has such Notes.
iro_anchor = """            ${sk.classId==='mage' ? '<li><a href=\"https://ragnaplace.com/en/rozg-en/skill/16/stone-curse\" target=\"_blank\" rel=\"noopener\">RagnaPlace — fixed / variable / global delay tables</a></li>' : ''}
"""
iro_with_source = iro_anchor + """            ${Array.isArray(sk.noteList) && sk.noteList.length ? '<li><a href=\"https://irowiki.org/wiki/Skills\" target=\"_blank\" rel=\"noopener\">iRO Wiki — additional gameplay mechanics reference</a></li>' : ''}
"""
if iro_anchor in text and "iRO Wiki — additional gameplay mechanics reference" not in text:
    text = text.replace(iro_anchor, iro_with_source, 1)

# Basic Skill is a special page and had its own useless Damage Formula section.
basic_toc_old = "${toc([{id:'levels',label:navLabel('Levels','Niveaux')},{id:'formula',label:navLabel('Damage formula','Formule des dégâts')},{id:'notes',label:t('notes')},{id:'sources',label:navLabel('Sources','Sources')}])}"
basic_toc_new = "${toc([{id:'levels',label:navLabel('Levels','Niveaux')},{id:'notes',label:t('notes')},{id:'sources',label:navLabel('Sources','Sources')}])}"
text = text.replace(basic_toc_old, basic_toc_new)
text = text.replace(
    """          <h2 id=\"formula\">${navLabel('Damage formula','Formule des dégâts')}</h2>
          <div class=\"notes-box\">${navLabel('Basic Skill does not inflict damage, so it has no direct damage formula.','Basic Skill n’inflige pas de dégâts ; elle n’a donc pas de formule de dégâts directe.')}</div>
""",
    "",
)


# ---------------------------------------------------------------------------
# Performance: the editor already refreshes on initial load, hash changes and
# language changes. Observing the whole rendered app subtree is unnecessary.
# ---------------------------------------------------------------------------
observer_old = """  const pageObserver = new MutationObserver(() => preparePage());
  pageObserver.observe(app, { childList: true, subtree: true });

"""
observer_new = """  // Full-app subtree observation removed: preparePage() is already called on
  // initial load, route changes and language changes.

"""
text = text.replace(observer_old, observer_new)


# ---------------------------------------------------------------------------
# Remove obsolete / misleading repository assets.
# ---------------------------------------------------------------------------
for obsolete in (
    ROOT / "assets/client-data/skills.zlib.b64",
    ROOT / "assets/database/memorial-dungeon.gif",
):
    obsolete.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# Guardrails: fail the workflow instead of silently redeploying regressions.
# ---------------------------------------------------------------------------
if "<th>${navLabel('Effect','Effet')}</th>" in text:
    raise RuntimeError("Effect column still present in skill level table")
if "<td>${esc(row.effect)}</td>" in text:
    raise RuntimeError("Effect cell still present in skill level table")
if "navLabel('Level data','Données par niveau')" not in text:
    raise RuntimeError("Level data heading/TOC was not applied")
if "<th>${navLabel('Bonus','Bonus')}</th>" not in text:
    raise RuntimeError("Pet List Bonus header missing")
if "Audit du contenu : 8 sept. 2026." not in text:
    raise RuntimeError("French audit date was not updated")
if "if (data.type === 'none') return '';" not in text:
    raise RuntimeError("Non-damaging formula section cleanup missing")
if "const hasFormulaSection = skillDamageFormulaData(sk).type !== 'none';" not in text:
    raise RuntimeError("Conditional formula state missing")
if "const pageObserver = new MutationObserver" in text:
    raise RuntimeError("Full-app MutationObserver is still active")

index_path.write_text(text, encoding="utf-8")
print("Audit cleanup applied: Pet header, skill level table, passive formulas, sources, metadata, performance and obsolete assets.")
