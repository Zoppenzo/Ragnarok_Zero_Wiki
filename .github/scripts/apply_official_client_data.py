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

# Per-level technical tables are intentionally removed. The infobox already
# carries SP/range/cast/delay/cooldown summaries; the article section is now
# reserved for useful Notes instead of repeating a mostly empty table.
text = re.sub(
    r"\n  function detailedSkillLevelTable\(sk\) \{.*?\n  \}\n\n  function skillDetail",
    "\n  function detailedSkillLevelTable(sk) { return ''; }\n\n  function skillDetail",
    text,
    count=1,
    flags=re.S,
)
text = text.replace(
    "            ...(hasDetailedLevels ? [{id:'levels',label:navLabel('Level data','Données par niveau')}] : []),\n",
    "",
)
text = text.replace(
    "          ${hasDetailedLevels ? detailedSkillLevelTable(sk) : ''}\n\n",
    "",
)

# Notes can now be structured as bullet points (sk.noteList) while retaining
# the old plain-text sk.notes fallback for skills that do not yet have a list.
old_notes = """          <h2 id=\"notes\">${t('notes')}</h2>
          <div class=\"notes-box\">${esc(txt(sk.notes))}</div>"""
new_notes = """          <h2 id=\"notes\">${t('notes')}</h2>
          <div class=\"notes-box\">${Array.isArray(sk.noteList) && sk.noteList.length
            ? `<ul>${sk.noteList.map(note=>`<li>${esc(txt(note))}</li>`).join('')}</ul>`
            : esc(txt(sk.notes))}</div>"""
if old_notes in text:
    text = text.replace(old_notes, new_notes, 1)

# Orc Hero is currently active.
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
        'The Orc Hero MVP Raid is currently available. Official client navigation data links ORK_HERO to b_gef_f03 and its b_gef_f03_z variant.',
        'Le MVP Raid Orc Hero est actuellement disponible. Les données de navigation du client officiel relient ORK_HERO à b_gef_f03 et à sa variante b_gef_f03_z.'
      )}</p>
      <div class="verified-topic-note"><svg class="notice-icon"><use href="#i-info"></use></svg><div><strong>${navLabel('Official client cross-check','Vérification client officiel')}</strong><br><code>ORK_HERO → b_gef_f03</code> · <code>b_gef_f03_z</code></div></div>

"""
    text = text.replace(rewards_heading, section + rewards_heading)

text = text.replace("Content audit: 6 Sep 2026.", "Content audit: 8 Sep 2026.")
index_path.write_text(text, encoding="utf-8")
print("Official client data prepared; level tables removed; notes layout enabled.")
