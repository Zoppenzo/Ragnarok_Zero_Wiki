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

# Keep the old technical per-level table removed, but restore a compact
# Damage-by-level table for offensive skills. Values come from the current
# official Zero client data loaded by client-sync.js.
damage_table_functions = r'''
  function skillDamageLevelRows(sk) {
    const r = window.RZ_CLIENT_SKILL_FOR ? window.RZ_CLIENT_SKILL_FOR(sk) : null;
    if (!r || sk.role !== 'damage') return [];

    const max = Math.max(1, Number(r.m || sk.maxLevel || 1));
    const effects = Array.isArray(r.le) ? r.le : [];
    const hitWord = n => n === 1 ? 'hit' : 'hits';

    const specialDamage = i => {
      const lv = i + 1;
      switch (r.a) {
        case 'MG_FIREBOLT':
        case 'MG_COLDBOLT':
        case 'MG_LIGHTNINGBOLT':
        case 'MG_THUNDERSTORM':
          return `MATK 100% × ${lv} ${hitWord(lv)}`;
        case 'WZ_EARTHSPIKE':
          return `MATK 200% × ${lv} ${hitWord(lv)}`;
        case 'MG_SOULSTRIKE': {
          const hits = Math.ceil(lv / 2);
          return `MATK 100% × ${hits} ${hitWord(hits)} · +${lv * 5}% vs Undead`;
        }
        case 'MG_FIREWALL': {
          const hits = lv + 2;
          return `MATK 50% × up to ${hits} ${hitWord(hits)} per wall`;
        }
        case 'AL_RUWACH':
          return 'MATK 145%';
        case 'AC_CHARGEARROW':
          return 'ATK 150%';
        case 'TF_SPRINKLESAND':
          return 'ATK 130%';
        case 'TF_THROWSTONE':
          return navLabel('50 fixed damage (ignores DEF)','50 dégâts fixes (ignore la DEF)');
        case 'MC_CARTREVOLUTION':
          return navLabel('ATK 150%–250% depending on cart weight','ATK 150 %–250 % selon le poids du chariot');
        case 'AL_HOLYLIGHT':
          return 'MATK 125%';
        default:
          return '';
      }
    };

    const rows = [];
    for (let i = 0; i < max; i++) {
      let damage = specialDamage(i);
      if (!damage) {
        const effect = String(effects[i] || '').trim();
        if (/^Center:\s*MATK/i.test(effect)) {
          damage = effect;
        } else if (/^(ATK|MATK)\s/i.test(effect)) {
          damage = effect.split(/,\s*(?=[A-Za-z])/)[0];
        } else if (/^Damage:\s*/i.test(effect)) {
          damage = `${navLabel('Normal physical damage','Dégâts physiques normaux')} ${effect.replace(/^Damage:\s*/i,'')}`;
        }
      }
      if (damage) rows.push([i + 1, damage]);
    }
    return rows;
  }

  function detailedSkillLevelTable(sk) {
    const rows = skillDamageLevelRows(sk);
    if (!rows.length) return '';
    return `
      <h2 id="damage-levels">${navLabel('Damage by level','Dégâts par niveau')}</h2>
      <div class="table-wrap"><table class="skill-damage-level-table">
        <thead><tr>
          <th style="width:90px">${navLabel('Level','Niveau')}</th>
          <th>${navLabel('Damage','Dégâts')}</th>
        </tr></thead>
        <tbody>${rows.map(([lv,damage])=>`<tr><td><strong>Lv. ${lv}</strong></td><td>${esc(damage)}</td></tr>`).join('')}</tbody>
      </table></div>`;
  }
'''

text = re.sub(
    r"\n  function (?:skillDamageLevelRows|detailedSkillLevelTable)\(sk\) \{.*?\n  \}\n(?:\n  function detailedSkillLevelTable\(sk\) \{.*?\n  \}\n)?\n  function skillDetail",
    "\n" + damage_table_functions.strip("\n") + "\n\n  function skillDetail",
    text,
    count=1,
    flags=re.S,
)

# Older deployments may only contain the one-line disabled function.
text = text.replace(
    "  function detailedSkillLevelTable(sk) { return ''; }\n\n  function skillDetail",
    damage_table_functions.strip("\n") + "\n\n  function skillDetail",
    1,
)

# Ensure skillDetail knows whether a current-client damage table exists.
if "const damageLevelRows = skillDamageLevelRows(sk);" not in text:
    text = text.replace(
        "    const hasDetailedLevels = !!rows;\n",
        "    const hasDetailedLevels = !!rows;\n    const damageLevelRows = skillDamageLevelRows(sk);\n    const hasDamageLevels = damageLevelRows.length > 0;\n",
        1,
    )

# Add Damage by level to the article TOC immediately before the formula.
if "{id:'damage-levels',label:navLabel('Damage by level','Dégâts par niveau')}" not in text:
    text = text.replace(
        "            {id:'formula',label:navLabel('Damage formula','Formule des dégâts')},\n",
        "            ...(hasDamageLevels ? [{id:'damage-levels',label:navLabel('Damage by level','Dégâts par niveau')}] : []),\n            {id:'formula',label:navLabel('Damage formula','Formule des dégâts')},\n",
        1,
    )

# Render the compact damage table before the damage formula.
if "${hasDamageLevels ? detailedSkillLevelTable(sk) : ''}" not in text:
    text = text.replace(
        "          ${skillDamageFormulaBlock(sk)}\n",
        "          ${hasDamageLevels ? detailedSkillLevelTable(sk) : ''}\n\n          ${skillDamageFormulaBlock(sk)}\n",
        1,
    )

# Remove any legacy Level data entry/table if still present.
text = text.replace(
    "            ...(hasDetailedLevels ? [{id:'levels',label:navLabel('Level data','Données par niveau')}] : []),\n",
    "",
)
text = text.replace(
    "          ${hasDetailedLevels ? detailedSkillLevelTable(sk) : ''}\n\n",
    "",
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
print("Official client data prepared; damage-by-level tables restored for offensive skills.")