from pathlib import Path
import base64
import re
import zlib

ROOT = Path(__file__).resolve().parents[2]

# Reassemble the official-client skill dataset from repository-safe chunks.
parts = [ROOT / f"assets/client-data/skills.part{i}" for i in range(1, 5)]
packed = "".join(p.read_text(encoding="utf-8").strip() for p in parts)
raw = zlib.decompress(base64.b64decode(packed)).decode("utf-8")
skills_json = ROOT / "assets/client-data/skills.json"
skills_json.write_text(raw, encoding="utf-8")

# Patch the main single-file wiki.
index_path = ROOT / "index.html"
text = index_path.read_text(encoding="utf-8")

script_tag = '  <script src="assets/client-sync.js"></script>\n'
if "assets/client-sync.js" not in text:
    text = text.replace("</body>", script_tag + "</body>")

# Skill list descriptions stay concise. Per-level client details belong in the
# skill page's level table, not inside the description column.
level_table_functions = r'''
  function skillShortDescription(sk) {
    let value = String(txt(sk && sk.description ? sk.description : '') || '').trim();
    value = value
      .replace(/\s*\[(?:Lv\.?|Level|Niv\.?)\s*1\][\s\S]*$/i, '')
      .replace(/\s*\[SP\s+\d+[\s\S]*$/i, '')
      .trim();

    // Keep the class overview iRO-like: usually one or two short sentences.
    const parts = value.match(/[^.!?]+[.!?]+|[^.!?]+$/g) || [];
    if (parts.length > 2) value = parts.slice(0, 2).join(' ').trim();
    if (value.length > 330) {
      const cut = value.slice(0, 330);
      value = cut.slice(0, Math.max(cut.lastIndexOf(' '), 250)).trim() + '…';
    }
    return value;
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
      const f = Number(at(r.d.cf, i) || 0);
      const v = Number(at(r.d.cv, i) || 0);
      const total = f + v;
      if (!total) return '—';
      if (f && v) return `${time(total)} (${time(f).replace(' s','')} fixed + ${time(v).replace(' s','')} variable)`;
      if (f) return `${time(f)} fixed`;
      return `${time(v)} variable`;
    };

    const enEffects = Array.isArray(r.le) ? r.le : [];
    const frEffects = [];
    const frText = String(r.df || '');
    const frRe = /\[Niv\.\s*(\d+)\]\s*([\s\S]*?)(?=\[Niv\.\s*\d+\]|$)/gi;
    let match;
    while ((match = frRe.exec(frText))) {
      frEffects[Number(match[1]) - 1] = String(match[2] || '').trim();
    }

    const rows = [];
    for (let i = 0; i < max; i++) {
      let en = String(enEffects[i] || '').trim();
      let fr = String(frEffects[i] || '').trim();

      // Heal is the only current first-job multi-level skill whose client text
      // exposes level scaling without listing a separate per-level Effect line.
      if (r.a === 'AL_HEAL' && !en) {
        en = `Heal strength: skill-level factor ×${i + 1}; final amount also scales with Base Level, total INT and weapon MATK.`;
        fr = `Puissance de Heal : facteur de niveau ×${i + 1} ; le montant final dépend aussi du Base Level, de l’INT totale et de la MATK de l’arme.`;
      }

      if (!en && fr) en = fr;
      if (!fr && en) fr = en;
      const effect = en || fr ? navLabel(en || fr, fr || en) : '—';

      rows.push({
        level: i + 1,
        effect,
        sp: at(r.sp, i) == null ? '—' : String(at(r.sp, i)),
        range: at(r.r, i) == null ? '—' : String(at(r.r, i)),
        cast: castAtLevel(i),
        delay: r.d && Array.isArray(r.d.gd) ? time(at(r.d.gd, i)) : '—',
        cooldown: r.d && Array.isArray(r.d.cd) ? time(at(r.d.cd, i)) : '—'
      });
    }
    return rows;
  }

  function detailedSkillLevelTable(sk) {
    const rows = skillLevelEffectRows(sk);
    if (!rows.length) return '';
    return `
      <h2 id="level-effects">${navLabel('Effects by level','Effets par niveau')}</h2>
      <div class="table-wrap"><table class="skill-level-effect-table">
        <thead><tr>
          <th style="width:76px">${navLabel('Level','Niveau')}</th>
          <th>${navLabel('Effect','Effet')}</th>
          <th style="width:62px">SP</th>
          <th style="width:72px">${navLabel('Range','Portée')}</th>
          <th style="width:150px">Cast</th>
          <th style="width:105px">Cast Delay</th>
          <th style="width:105px">Cooldown</th>
        </tr></thead>
        <tbody>${rows.map(row=>`<tr>
          <td><strong>Lv. ${row.level}</strong></td>
          <td>${esc(row.effect)}</td>
          <td>${esc(row.sp)}</td>
          <td>${esc(row.range)}</td>
          <td>${esc(row.cast)}</td>
          <td>${esc(row.delay)}</td>
          <td>${esc(row.cooldown)}</td>
        </tr>`).join('')}</tbody>
      </table></div>`;
  }
'''

# Replace either the previous damage-only implementation or a previous version
# of this generic implementation. Keep the operation idempotent.
new_block_pattern = re.compile(
    r"\n  function skillShortDescription\(sk\) \{.*?\n  \}\n\n"
    r"  function skillLevelEffectRows\(sk\) \{.*?\n  \}\n\n"
    r"  function detailedSkillLevelTable\(sk\) \{.*?\n  \}\n",
    re.S,
)
old_block_pattern = re.compile(
    r"\n  function skillDamageLevelRows\(sk\) \{.*?\n  \}\n\n"
    r"  function detailedSkillLevelTable\(sk\) \{.*?\n  \}\n",
    re.S,
)

replacement = "\n" + level_table_functions.strip("\n") + "\n"
text, changed = new_block_pattern.subn(lambda _m: replacement, text, count=1)
if not changed:
    text, changed = old_block_pattern.subn(lambda _m: replacement, text, count=1)
if not changed:
    text = text.replace(
        "  function detailedSkillLevelTable(sk) { return ''; }\n\n  function skillDetail",
        level_table_functions.strip("\n") + "\n\n  function skillDetail",
        1,
    )

# Use the generic level table for every multi-level skill, active or passive.
text = text.replace(
    "    const damageLevelRows = skillDamageLevelRows(sk);\n    const hasDamageLevels = damageLevelRows.length > 0;\n",
    "    const effectLevelRows = skillLevelEffectRows(sk);\n    const hasEffectLevels = effectLevelRows.length > 0;\n",
)
if "const effectLevelRows = skillLevelEffectRows(sk);" not in text:
    text = text.replace(
        "    const hasDetailedLevels = !!rows;\n",
        "    const hasDetailedLevels = !!rows;\n    const effectLevelRows = skillLevelEffectRows(sk);\n    const hasEffectLevels = effectLevelRows.length > 0;\n",
        1,
    )

text = text.replace(
    "            ...(hasDamageLevels ? [{id:'damage-levels',label:navLabel('Damage by level','Dégâts par niveau')}] : []),\n",
    "            ...(hasEffectLevels ? [{id:'level-effects',label:navLabel('Effects by level','Effets par niveau')}] : []),\n",
)
if "{id:'level-effects',label:navLabel('Effects by level','Effets par niveau')}" not in text:
    text = text.replace(
        "            {id:'formula',label:navLabel('Damage formula','Formule des dégâts')},\n",
        "            ...(hasEffectLevels ? [{id:'level-effects',label:navLabel('Effects by level','Effets par niveau')}] : []),\n            {id:'formula',label:navLabel('Damage formula','Formule des dégâts')},\n",
        1,
    )

text = text.replace(
    "          ${hasDamageLevels ? detailedSkillLevelTable(sk) : ''}\n\n",
    "          ${hasEffectLevels ? detailedSkillLevelTable(sk) : ''}\n\n",
)
if "${hasEffectLevels ? detailedSkillLevelTable(sk) : ''}" not in text:
    text = text.replace(
        "          ${skillDamageFormulaBlock(sk)}\n",
        "          ${hasEffectLevels ? detailedSkillLevelTable(sk) : ''}\n\n          ${skillDamageFormulaBlock(sk)}\n",
        1,
    )

# Remove obsolete generic/damage level entries left by older deployments.
text = text.replace(
    "            ...(hasDetailedLevels ? [{id:'levels',label:navLabel('Level data','Données par niveau')}] : []),\n",
    "",
)
text = text.replace(
    "          ${hasDetailedLevels ? detailedSkillLevelTable(sk) : ''}\n\n",
    "",
)

# Keep class overview descriptions and the skill lead concise. Per-level values
# are presented only in the table above.
text = text.replace("${esc(txt(sk.description))}", "${esc(skillShortDescription(sk))}")
text = text.replace(
    "${esc(sk.classId==='swordman' && hasDetailedLevels ? swordmanSkillExtraText(sk) : txt(sk.description))}",
    "${esc(skillShortDescription(sk))}",
)

# Notes are iRO-style gameplay remarks: no generic verification text, no
# prerequisite repetition, and no empty Notes heading.
text = text.replace(
    "            {id:'notes',label:t('notes')},\n",
    "            ...(Array.isArray(sk.noteList) && sk.noteList.length ? [{id:'notes',label:t('notes')}] : []),\n",
)

current_notes = """          <h2 id=\"notes\">${t('notes')}</h2>
          <div class=\"notes-box\">${Array.isArray(sk.noteList) && sk.noteList.length
            ? `<ul>${sk.noteList.map(note=>`<li>${esc(txt(note))}</li>`).join('')}</ul>`
            : esc(txt(sk.notes))}</div>"""
conditional_notes = """          ${Array.isArray(sk.noteList) && sk.noteList.length ? `
          <h2 id=\"notes\">${t('notes')}</h2>
          <div class=\"notes-box\"><ul>${sk.noteList.map(note=>`<li>${esc(txt(note))}</li>`).join('')}</ul></div>` : ''}"""
if current_notes in text:
    text = text.replace(current_notes, conditional_notes, 1)
else:
    text = text.replace(
        """          <h2 id=\"notes\">${t('notes')}</h2>
          <div class=\"notes-box\">${esc(txt(sk.notes))}</div>""",
        conditional_notes,
        1,
    )

# Orc Hero is currently active, but source/verification annotations are not
# shown inside the article body.
text = text.replace(
    "The two MVP Raids currently available are Golden Thief Bug in Prontera Culvert and Moonlight Flower in Payon Cave 5.",
    "The three MVP Raids currently available are Golden Thief Bug in Prontera Culvert, Moonlight Flower in Payon Cave 5 and Orc Hero on the Orc/Geffen raid map (b_gef_f03).",
)
text = text.replace(
    "Les deux MVP Raids actuellement disponibles sont Golden Thief Bug à Prontera Culvert et Moonlight Flower à Payon Cave 5.",
    "Les trois MVP Raids actuellement disponibles sont Golden Thief Bug à Prontera Culvert, Moonlight Flower à Payon Cave 5 et Orc Hero sur la map de raid Orc/Geffen (b_gef_f03).",
)

moon = """      {
        boss:'Moonlight Flower',
        access:'Payon Cave 5',
        pve:navLabel('General Habitat / PvE','General Habitat / PvE'),
        pvp:navLabel('PK Habitat / PvP','PK Habitat / PvP'),
        release:navLabel('August 18, 2026 — server launch','18 août 2026 — ouverture du serveur')
      }
"""
if "boss:'Orc Hero'" not in text and moon in text:
    text = text.replace(moon, moon.rstrip() + ",\n" + """      {
        boss:'Orc Hero',
        access:navLabel('Orc / Geffen raid map — b_gef_f03','Map de raid Orc / Geffen — b_gef_f03'),
        pve:navLabel('General Habitat / PvE','General Habitat / PvE'),
        pvp:navLabel('PK Habitat / PvP','PK Habitat / PvP'),
        release:navLabel('Currently available','Actuellement disponible')
      }
""")

toc_line = "        {id:'moonlight-raid',label:'Moonlight Flower'},\n"
if "{id:'orc-hero-raid',label:'Orc Hero'}" not in text:
    text = text.replace(toc_line, toc_line + "        {id:'orc-hero-raid',label:'Orc Hero'},\n")

rewards_heading = "      <h2 id=\"rewards\">${navLabel('Reward boxes','Boîtes de récompense')}</h2>"
if 'id="orc-hero-raid"' not in text and rewards_heading in text:
    section = """      <h2 id="orc-hero-raid">Orc Hero</h2>
      <p>${navLabel(
        'Orc Hero is currently available as an MVP Raid on the Orc / Geffen raid map.',
        'Orc Hero est actuellement disponible en MVP Raid sur la map de raid Orc / Geffen.'
      )}</p>

"""
    text = text.replace(rewards_heading, section + rewards_heading)

text = text.replace(
    "The Orc Hero MVP Raid is currently available. Official client navigation data links ORK_HERO to b_gef_f03 and its b_gef_f03_z variant.",
    "Orc Hero is currently available as an MVP Raid on the Orc / Geffen raid map.",
)
text = text.replace(
    "Le MVP Raid Orc Hero est actuellement disponible. Les données de navigation du client officiel relient ORK_HERO à b_gef_f03 et à sa variante b_gef_f03_z.",
    "Orc Hero est actuellement disponible en MVP Raid sur la map de raid Orc / Geffen.",
)
text = re.sub(
    r'\n\s*<div class="verified-topic-note"><svg class="notice-icon"><use href="#i-info"></use></svg><div><strong>\$\{navLabel\(\'Official client cross-check\',\'Vérification client officiel\'\)\}</strong><br><code>ORK_HERO → b_gef_f03</code> · <code>b_gef_f03_z</code></div></div>',
    '',
    text,
    count=1,
)

text = text.replace("Content audit: 6 Sep 2026.", "Content audit: 8 Sep 2026.")
index_path.write_text(text, encoding="utf-8")
print("Official client data prepared; concise skill descriptions and effect-by-level tables enabled for every multi-level skill.")