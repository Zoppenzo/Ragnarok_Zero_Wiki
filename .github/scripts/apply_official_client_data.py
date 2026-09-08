from pathlib import Path
import base64
import re
import zlib

ROOT = Path(__file__).resolve().parents[2]

# Reassemble the official-client skill dataset from small repository-safe chunks.
parts = [ROOT / f"assets/client-data/skills.part{i}" for i in range(1, 5)]
packed = "".join(p.read_text(encoding="utf-8").strip() for p in parts)
raw = zlib.decompress(base64.b64decode(packed)).decode("utf-8")
skills_json = ROOT / "assets/client-data/skills.json"
skills_json.write_text(raw, encoding="utf-8")

# Remove the empty Effect column from the runtime-synchronized skill tables.
sync_path = ROOT / "assets/client-sync.js"
sync = sync_path.read_text(encoding="utf-8")
sync = re.sub(
    r"function makeRow\(r,i,effect\) \{.*?\n    \}",
    """function makeRow(r,i) {
      const t=techAt(r,i);
      return `<tr><td><strong>Lv. ${i+1}</strong></td><td>${t.sp==null?'—':esc(t.sp)}</td><td>${t.range==null?'—':esc(t.range)}</td><td>${esc(t.cast||'—')}</td><td>${esc(t.delay||'—')}</td><td>${esc(t.cd||'—')}</td></tr>`;
    }""",
    sync,
    count=1,
    flags=re.S,
)
sync = sync.replace("      const effects=(isFr() && r.lf && r.lf.length ? r.lf : r.le) || [];\n", "")
sync = re.sub(r"\s*const old=\[\.\.\.table\.querySelectorAll\('tbody tr'\)\].*?;\n", "", sync, count=1)
sync = sync.replace(
    "        table.querySelector('tbody').innerHTML=Array.from({length:max},(_,i)=>makeRow(r,i,effects[i]||old[i]||'')).join('');",
    "        const effectHeader=table.querySelector('thead tr th:nth-child(2)');\n        if (effectHeader) effectHeader.remove();\n        table.querySelector('tbody').innerHTML=Array.from({length:max},(_,i)=>makeRow(r,i)).join('');",
)
sync = sync.replace("<th>${isFr()?'Effet client':'Client effect'}</th>", "")
sync = sync.replace("Array.from({length:max},(_,i)=>makeRow(r,i,effects[i]||'')).join('')", "Array.from({length:max},(_,i)=>makeRow(r,i)).join('')")
sync_path.write_text(sync, encoding="utf-8")

# Patch the main single-file wiki.
index_path = ROOT / "index.html"
text = index_path.read_text(encoding="utf-8")

script_tag = '  <script src="assets/client-sync.js"></script>\n'
if "assets/client-sync.js" not in text:
    text = text.replace("</body>", script_tag + "</body>")

# Remove Effect-by-level from skill pages and rename the section more accurately.
text = text.replace("Level-by-level effects','Effets par niveau", "Level data','Données par niveau")
text = text.replace("          <th>${navLabel('Effect','Effet')}</th>\n", "")
text = text.replace(
    "${rows.map(([lv,effect,sp,range,cast,delay,cd])=>`<tr><td><strong>Lv. ${lv}</strong></td><td>${esc(effect)}</td><td>${sp}</td><td>${range}</td><td>${esc(cast)}</td><td>${esc(delay)}</td><td>${esc(cd)}</td></tr>`).join('')}",
    "${rows.map(([lv,effect,sp,range,cast,delay,cd])=>`<tr><td><strong>Lv. ${lv}</strong></td><td>${sp}</td><td>${range}</td><td>${esc(cast)}</td><td>${esc(delay)}</td><td>${esc(cd)}</td></tr>`).join('')}",
)

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
print("Official client data prepared and wiki patched.")
