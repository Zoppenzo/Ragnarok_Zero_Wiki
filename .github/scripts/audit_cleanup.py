from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
index_path = ROOT / "index.html"
text = index_path.read_text(encoding="utf-8")

# Audit metadata.
text = text.replace(
    "Audit du contenu : 6 sept. 2026.",
    "Audit du contenu : 8 sept. 2026.",
)

# Pet table: the body has four cells, so expose the missing Bonus header.
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

# ---------------------------------------------------------------------------
# Skills: iRO-style per-level Effect tables using Ragnarok Zero client data.
# The table is skill-specific: damage, accuracy, duration, status chance,
# durability, stat bonuses, etc. are split into meaningful columns. SP Cost is
# kept in the table for active skills. Cast/range/delay/cooldown only appear
# when they actually vary by skill level.
# ---------------------------------------------------------------------------
level_table_functions = r'''
  function skillEffectLabel(raw) {
    const key = String(raw || '').trim().toLowerCase();
    const map = {
      'accuracy bonus':'Accuracy Bonus',
      'hit bonus':'HIT Bonus',
      'hit rate':'Accuracy Bonus',
      'activation chance':'Activation Chance',
      'frozen chance':'Frozen Chance',
      'petrification chance':'Petrification Chance',
      'poison chance':'Poison Chance',
      'success rate':'Success Rate',
      'base success rate':'Base Success Rate',
      'catalyst consumption':'Catalyst Consumption',
      'discount rate':'Discount Rate',
      'markup rate':'Markup Rate',
      'movement speed penalty':'Movement Speed Penalty',
      'items for sale':'Items for Sale',
      'additional sp consumption':'Additional SP Consumption',
      'zeny cost':'Zeny Cost',
      'duration':'Duration',
      'durability':'Durability',
      'blocks':'Blocks',
      'damage':'Damage Bonus',
      'per wall':'Hits per Wall'
    };
    return map[key] || String(raw || '').trim().replace(/\b\w/g, c => c.toUpperCase());
  }

  function parseClientEffect(raw) {
    const out = [];
    const add = (label, value) => {
      label = String(label || '').trim();
      value = String(value || '').trim().replace(/\.$/, '');
      if (!label || !value) return;
      if (!out.some(x => x.label === label)) out.push({label, value});
    };

    let work = String(raw || '').trim().replace(/\.$/, '');
    if (!work) return out;

    // Protect comma-separated stat groups before splitting the client string.
    work = work.replace(/STR,\s*INT,\s*DEX\s*([+\-]\s*\d+%?)/i, (_m,v) => {
      add('STR / INT / DEX', v.replace(/\s+/g,''));
      return '';
    });
    work = work.replace(/DEX,\s*AGI\s*([+\-]\s*\d+%?)/i, (_m,v) => {
      add('DEX / AGI', v.replace(/\s+/g,''));
      return '';
    });

    for (let part of work.split(/\s*,\s*/)) {
      part = part.trim();
      if (!part) continue;
      let m;

      if ((m = part.match(/^ATK\s+(.+)$/i))) add('Damage (ATK)', m[1]);
      else if ((m = part.match(/^MATK\s+(.+)$/i))) add('Damage (MATK)', m[1]);
      else if ((m = part.match(/^Center:\s*MATK\s+(.+)$/i))) add('Center Damage (MATK)', m[1]);
      else if ((m = part.match(/^Outer:\s*MATK\s+(.+)$/i))) add('Outer Damage (MATK)', m[1]);
      else if ((m = part.match(/^HP every 10 sec\s*(.+)$/i))) add('HP Recovery / 10 sec', m[1]);
      else if ((m = part.match(/^SP every 10 sec\s*(.+)$/i))) add('SP Recovery / 10 sec', m[1]);
      else if ((m = part.match(/^Damage\s*:?\s*([+\-].+)$/i))) add('Damage Bonus', m[1]);
      else if ((m = part.match(/^Mounted\s*([+\-].+)$/i))) add('Mounted Bonus', m[1]);
      else if ((m = part.match(/^Duration\s*:?\s*(.+)$/i))) add('Duration', m[1]);
      else if ((m = part.match(/^MDEF\s*([+\-].+)$/i))) add('MDEF', m[1]);
      else if ((m = part.match(/^FLEE\s*([+\-].+)$/i))) add('FLEE', m[1]);
      else if ((m = part.match(/^AGI\s*([+\-].+)$/i))) add('AGI', m[1]);
      else if ((m = part.match(/^DEX\s*([+\-].+)$/i))) add('DEX', m[1]);
      else if ((m = part.match(/^HIT\s*([+\-].+)$/i))) add('HIT', m[1]);
      else if ((m = part.match(/^HP\s*([+\-].+)$/i))) add('HP', m[1]);
      else if ((m = part.match(/^CRIT\s*([+\-].+)$/i))) add('CRIT', m[1]);
      else if ((m = part.match(/^Bow Range\s*([+\-].+)$/i))) add('Bow Range', m[1]);
      else if ((m = part.match(/^Weight Limit\s*([+\-].+)$/i))) add('Weight Limit', m[1]);
      else if ((m = part.match(/^Physical Defense\s*([+\-].+)$/i))) add('Target DEF', m[1]);
      else if ((m = part.match(/^VIT-based Defense\s*([+\-].+)$/i))) add('VIT-based DEF', m[1]);
      else if ((m = part.match(/^Enemy damage\s*([+\-].+)$/i))) add('Target Damage', m[1]);
      else if ((m = part.match(/^Enemy defense\s*([+\-].+)$/i))) add('Target DEF', m[1]);
      else if ((m = part.match(/^After second job:\s*FLEE\s*([+\-].+)$/i))) add('FLEE (2nd Job)', m[1]);
      else if ((m = part.match(/^(\d+)\s+hits?$/i))) add('Hits', m[1]);
      else if ((m = part.match(/^Hits:\s*(\d+)$/i))) add('Hits', m[1]);
      else if ((m = part.match(/^Per wall:\s*(\d+)\s+hits?$/i))) add('Hits per Wall', m[1]);
      else if ((m = part.match(/^([^:]+):\s*(.+)$/))) {
        let label = m[1].trim();
        let value = m[2].trim();
        if (/^Center$/i.test(label) && /^MATK\s+/i.test(value)) {
          add('Center Damage (MATK)', value.replace(/^MATK\s+/i,''));
        } else if (/^Outer$/i.test(label) && /^MATK\s+/i.test(value)) {
          add('Outer Damage (MATK)', value.replace(/^MATK\s+/i,''));
        } else if (/^After second job$/i.test(label) && /^FLEE\s+/i.test(value)) {
          add('FLEE (2nd Job)', value.replace(/^FLEE\s*/i,''));
        } else if (/^Per wall$/i.test(label)) {
          add('Hits per Wall', value.replace(/\s*hits?$/i,''));
        } else {
          add(skillEffectLabel(label), value);
        }
      } else {
        add('Effect', part);
      }
    }
    return out;
  }

  function skillLevelEffectRows(sk) {
    const r = window.RZ_CLIENT_SKILL_FOR ? window.RZ_CLIENT_SKILL_FOR(sk) : null;
    if (!r) return [];

    const max = Math.max(1, Number(r.m || sk.maxLevel || 1));
    if (max <= 1) return [];

    const at = (arr, i) => Array.isArray(arr) && arr.length ? arr[Math.min(i, arr.length - 1)] : null;
    const time = ms => {
      if (ms == null) return '—';
      const n = Number(ms);
      if (!Number.isFinite(n) || n === 0) return '—';
      if (n % 1000 === 0) return (n / 1000) + ' s';
      return (n / 1000).toFixed(3).replace(/0+$/, '').replace(/\.$/, '') + ' s';
    };
    const castAtLevel = i => {
      if (!r.d) return '—';
      const fixed = Number(at(r.d.cf, i) || 0);
      const variable = Number(at(r.d.cv, i) || 0);
      const total = fixed + variable;
      if (!total) return '—';
      if (fixed && variable) return `${time(total)} (${time(fixed).replace(' s','')} fixed + ${time(variable).replace(' s','')} variable)`;
      if (fixed) return `${time(fixed)} fixed`;
      return `${time(variable)} variable`;
    };

    const rows = [];
    const columnOrder = [];
    const addColumn = label => { if (label && !columnOrder.includes(label)) columnOrder.push(label); };

    for (let i = 0; i < max; i++) {
      const raw = Array.isArray(r.le) ? String(r.le[i] || '').trim() : '';
      let parts = parseClientEffect(raw);

      // Zero-specific transformations so the table shows actual damage scaling,
      // not only a hit count.
      if (['MG_COLDBOLT','MG_FIREBOLT','MG_LIGHTNINGBOLT','MG_THUNDERSTORM'].includes(r.a)) {
        const hits = Number((raw.match(/(\d+)\s+hits?/i) || [0, i + 1])[1] || i + 1);
        parts = [{label:'Damage (MATK)', value:`100% × ${hits} hit${hits === 1 ? '' : 's'}`}];
      } else if (r.a === 'WZ_EARTHSPIKE') {
        const hits = Number((raw.match(/(?:Hits:\s*)?(\d+)/i) || [0, i + 1])[1] || i + 1);
        parts = [{label:'Damage (MATK)', value:`200% × ${hits} hit${hits === 1 ? '' : 's'}`}];
      } else if (r.a === 'MG_SOULSTRIKE') {
        const hits = Number((raw.match(/(\d+)\s+hits?/i) || [0, 1])[1] || 1);
        const undead = (raw.match(/Bonus vs Undead:\s*([+\-]?\d+%)/i) || [0,'—'])[1];
        parts = [
          {label:'Damage (MATK)', value:`100% × ${hits} hit${hits === 1 ? '' : 's'}`},
          {label:'Bonus vs Undead', value:undead}
        ];
      } else if (r.a === 'MG_FIREWALL') {
        const hits = (raw.match(/Per wall:\s*(\d+)\s+hits?/i) || [0,'—'])[1];
        const duration = (raw.match(/Duration:\s*([^,]+)/i) || [0,'—'])[1];
        parts = [
          {label:'Damage / Hit (MATK)', value:'50%'},
          {label:'Hits per Wall', value:hits},
          {label:'Duration', value:duration}
        ];
      } else if (r.a === 'AL_HEAL') {
        parts = [{label:'Heal Level Factor', value:`×${i + 1}`}];
      } else if (r.a === 'SM_BASH') {
        const damage = (raw.match(/ATK\s+([^,]+)/i) || [0,'—'])[1];
        const accuracy = (raw.match(/Accuracy bonus:\s*([^,]+)/i) || [0,'—'])[1];
        const stun = i < 5 ? '—' : `${(i - 4) * 5}%`;
        parts = [
          {label:'Damage (ATK)', value:damage},
          {label:'Accuracy Bonus', value:accuracy},
          {label:'Base Stun Chance*', value:stun}
        ];
      }

      const values = {};
      for (const part of parts) {
        addColumn(part.label);
        values[part.label] = part.value;
      }
      rows.push({level:i + 1, values});
    }

    // SP Cost belongs in the iRO-style level table for active skills.
    const spValues = rows.map((_,i) => at(r.sp,i));
    if (spValues.some(v => Number(v) > 0)) {
      addColumn('SP Cost');
      rows.forEach((row,i) => { row.values['SP Cost'] = spValues[i] == null ? '—' : String(spValues[i]); });
    }

    const addIfVaries = (label, values) => {
      const clean = values.map(v => v == null ? '—' : String(v));
      const meaningful = clean.filter(v => v !== '—');
      if (!meaningful.length || new Set(clean).size <= 1) return;
      addColumn(label);
      rows.forEach((row,i) => { row.values[label] = clean[i]; });
    };

    addIfVaries('Range', rows.map((_,i) => at(r.r,i)));
    addIfVaries('Cast Time', rows.map((_,i) => castAtLevel(i)));
    addIfVaries('Cast Delay', rows.map((_,i) => r.d && Array.isArray(r.d.gd) ? time(at(r.d.gd,i)) : '—'));
    addIfVaries('Cooldown', rows.map((_,i) => r.d && Array.isArray(r.d.cd) ? time(at(r.d.cd,i)) : '—'));

    // If the client has no per-level effect text, still keep a useful table for
    // any actual level-varying resource/cast values rather than inventing data.
    rows.columns = columnOrder;
    if (r.a === 'SM_BASH') {
      rows.footnote = 'Fatal Blow enables Stun from Bash Lv.6. The table shows the base Stun Chance; Base Level further increases the final chance.';
    }
    return rows;
  }

  function detailedSkillLevelTable(sk) {
    const rows = skillLevelEffectRows(sk);
    const columns = Array.isArray(rows.columns) ? rows.columns : [];
    if (!rows.length || !columns.length) return '';

    const rowspanAt = (column, index) => {
      const value = rows[index].values[column] ?? '—';
      if (index > 0 && (rows[index - 1].values[column] ?? '—') === value) return 0;
      let span = 1;
      while (index + span < rows.length && (rows[index + span].values[column] ?? '—') === value) span++;
      return span;
    };

    return `
      <h2 id="level-effects" style="clear:both;margin-bottom:10px">${navLabel('Effect','Effet')}</h2>
      <div class="table-wrap"><table class="skill-level-effect-table iro-skill-table">
        <thead><tr>
          <th style="width:72px">${navLabel('Level','Niveau')}</th>
          ${columns.map(column => `<th>${esc(column)}</th>`).join('')}
        </tr></thead>
        <tbody>${rows.map((row,index)=>`<tr>
          <td><strong>${row.level}</strong></td>
          ${columns.map(column => {
            const span = rowspanAt(column,index);
            if (!span) return '';
            const attr = span > 1 ? ` rowspan="${span}"` : '';
            return `<td${attr}>${esc(row.values[column] ?? '—')}</td>`;
          }).join('')}
        </tr>`).join('')}</tbody>
      </table></div>
      ${rows.footnote ? `<p class="muted-note"><small>* ${esc(rows.footnote)}</small></p>` : ''}`;
  }
'''

block_pattern = re.compile(
    r"\n  function skillLevelEffectRows\(sk\) \{.*?\n  \}\n\n"
    r"  function detailedSkillLevelTable\(sk\) \{.*?\n  \}\n",
    re.S,
)
replacement = "\n" + level_table_functions.strip("\n") + "\n"
text, changed = block_pattern.subn(lambda _m: replacement, text, count=1)
if not changed:
    raise RuntimeError("Could not replace skill level table renderer")

# Rename the section/TOC away from the technical 'Level data' wording.
text = text.replace("navLabel('Level data','Données par niveau')", "navLabel('Effect','Effet')")
text = text.replace("navLabel('Effects by level','Effets par niveau')", "navLabel('Effect','Effet')")

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

# Keep idempotency when this state was already generated by a previous run.
if "const hasClientData = !!(window.RZ_CLIENT_SKILL_FOR" not in text:
    text = text.replace(
        "    const hasDetailedLevels = !!rows;\n    const effectLevelRows = skillLevelEffectRows(sk);\n    const hasEffectLevels = effectLevelRows.length > 0;\n",
        "    const hasDetailedLevels = false;\n    const effectLevelRows = skillLevelEffectRows(sk);\n    const hasEffectLevels = effectLevelRows.length > 0;\n    const hasClientData = !!(window.RZ_CLIENT_SKILL_FOR && window.RZ_CLIENT_SKILL_FOR(sk));\n    const hasFormulaSection = skillDamageFormulaData(sk).type !== 'none';\n",
        1,
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

# Source visibility follows official client coverage instead of the old manual table.
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

# Basic Skill has its own page; remove the useless Damage Formula section there.
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
print("Audit cleanup applied with iRO-style Ragnarok Zero skill tables.")
