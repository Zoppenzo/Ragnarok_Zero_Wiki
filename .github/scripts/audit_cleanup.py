from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
index_path = ROOT / "index.html"
text = index_path.read_text(encoding="utf-8")

# Audit metadata.
text = text.replace(
    "Audit du contenu : 6 sept. 2026.",
    "Audit du contenu : 8 sept. 2026.",
)

# Pet table: the body already has four cells, so expose the missing Bonus header.
text = text.replace(
    """        <thead><tr>
          <th>Pet</th>
          <th>Taming Item</th>
          <th>${navLabel('Drop source','Source de drop')}</th>
        </tr></thead>""",
    """        <thead><tr>
          <th>Pet</th>
          <th>${navLabel('Bonus','Bonus')}</th>
          <th>Taming Item</th>
          <th>${navLabel('Drop source','Source de drop')}</th>
        </tr></thead>""",
)

# Skill level table: no Effect column. Official client values shown are Level,
# SP, Range, Cast, Cast Delay and Cooldown.
text = text.replace(
    "navLabel('Effects by level','Effets par niveau')",
    "navLabel('Level data','Données par niveau')",
)
text = text.replace("          <th>${navLabel('Effect','Effet')}</th>\n", "")
text = text.replace("          <td>${esc(row.effect)}</td>\n", "")

# Stop using the legacy manual level table in the generic skill page. The
# official client synchronizer is the runtime authority.
text = text.replace(
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
)

# Non-damaging/passive skills do not need a Damage Formula section.
text = text.replace(
    """    if (data.type === 'none') {
      return `<h2 id=\"formula\">${navLabel('Damage formula','Formule des dégâts')}</h2>
        <div class=\"notes-box\">${navLabel(data.en,data.fr)}</div>`;
    }""",
    "    if (data.type === 'none') return '';",
)
text = text.replace(
    "            {id:'formula',label:navLabel('Damage formula','Formule des dégâts')},\n",
    "            ...(hasFormulaSection ? [{id:'formula',label:navLabel('Damage formula','Formule des dégâts')}] : []),\n",
    1,
)

# Source visibility follows official client coverage instead of the old manual
# level table.
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

# Basic Skill has its own page; remove the same useless formula section there.
text = text.replace(
    "${toc([{id:'levels',label:navLabel('Levels','Niveaux')},{id:'formula',label:navLabel('Damage formula','Formule des dégâts')},{id:'notes',label:t('notes')},{id:'sources',label:navLabel('Sources','Sources')}])}",
    "${toc([{id:'levels',label:navLabel('Levels','Niveaux')},{id:'notes',label:t('notes')},{id:'sources',label:navLabel('Sources','Sources')}])}",
)
text = text.replace(
    """          <h2 id=\"formula\">${navLabel('Damage formula','Formule des dégâts')}</h2>
          <div class=\"notes-box\">${navLabel('Basic Skill does not inflict damage, so it has no direct damage formula.','Basic Skill n’inflige pas de dégâts ; elle n’a donc pas de formule de dégâts directe.')}</div>
""",
    "",
)

# Remove the broad observer over the whole rendered app. Explicit refreshes are
# already run on initial load, route changes and language changes.
text = text.replace(
    """  const pageObserver = new MutationObserver(() => preparePage());
  pageObserver.observe(app, { childList: true, subtree: true });

""",
    """  // Full-app subtree observer removed; explicit lifecycle refreshes are used.

""",
)

# Remove obsolete/misleading repository files.
(ROOT / "assets/client-data/skills.zlib.b64").unlink(missing_ok=True)
(ROOT / "assets/database/memorial-dungeon.gif").unlink(missing_ok=True)

index_path.write_text(text, encoding="utf-8")
print("Audit cleanup applied.")
