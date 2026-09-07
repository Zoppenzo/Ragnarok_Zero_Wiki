from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Simple wiki-table styling for enchantment guide.
css_anchor = '/* Detailed enchantment guide blocks */'
assert css_anchor in s
if '.enchant-simple-table' not in s:
    css = '''/* Simple enchantment guide tables */
.enchant-simple-table th,
.enchant-simple-table td { vertical-align: top; }
.enchant-simple-table th { white-space: nowrap; }
.enchant-simple-table td { line-height: 1.45; }
.enchant-simple-table .essence-effect-list { margin-top: 0; }
.enchant-simple-note { margin: 8px 0 14px; color: var(--muted); font-size: 12px; }

'''
    s = s.replace(css_anchor, css + css_anchor, 1)

fn_start = s.index('  function enchantmentPage(topic) {')
fn_end = s.index('\n  function ', fn_start + 10)
f = s[fn_start:fn_end]

# Shorter lead: no explanation of how the page was designed.
lead_start = f.index('      <p class="article-lead">')
lead_end = f.index('</p>', lead_start) + 4
new_lead = '''      <p class="article-lead">${navLabel(
        'Enchant requirements, costs, rates, break rules and effects.',
        'Prérequis, coûts, taux, risque de casse et effets des enchantements.'
      )}</p>'''
f = f[:lead_start] + new_lead + f[lead_end:]

# COSTUME PANEL
c_start = f.index('          <section class="enchant-tab-panel" id="enchant-panel-costume">')
p_start = f.index('          <section class="enchant-tab-panel" id="enchant-panel-poring">', c_start)
new_costume = r'''          <section class="enchant-tab-panel" id="enchant-panel-costume">
            <h2 id="costume">Costume Enchant</h2>
            <div class="table-wrap"><table class="enchant-simple-table">
              <thead><tr><th>${navLabel('Action','Action')}</th><th>${navLabel('Requirement','Prérequis')}</th><th>${navLabel('Cost','Coût')}</th><th>%</th><th>${navLabel('Break?','Casse ?')}</th><th>${navLabel('Result','Résultat')}</th></tr></thead>
              <tbody>
                <tr><td>Craft Box B</td><td>${navLabel('5 unbound Costume (C) items','5 Costume (C) non liés')}</td><td>10 000 zeny</td><td>${navLabel('Random result','Aléatoire')}</td><td>—</td><td>${navLabel('Gives one random slot box.','Donne une boîte de slot aléatoire.')}</td></tr>
                <tr><td>${navLabel('Open slot box','Ouvrir la boîte')}</td><td>${navLabel('1 Costume Enchant Stone box','1 boîte Costume Enchant Stone')}</td><td>—</td><td>${navLabel('Random result','Aléatoire')}</td><td>—</td><td>${navLabel('Gives one random stone from that box.','Donne une pierre aléatoire du pool de la boîte.')}</td></tr>
                <tr><td>${navLabel('Apply stone','Appliquer la pierre')}</td><td>${navLabel('Stone and costume must use the same slot: Upper, Middle, Lower or Garment.','La pierre et le costume doivent correspondre au même slot : Upper, Middle, Lower ou Garment.')}</td><td>${navLabel('1 enchant stone','1 enchant stone')}</td><td>—</td><td>—</td><td>${navLabel('Applies the stone effect to the costume.','Applique l’effet de la pierre au costume.')}</td></tr>
              </tbody>
            </table></div>

            <h3>${navLabel('Current stone pools','Pools actuels')}</h3>
            <div class="table-wrap"><table class="enchant-simple-table">
              <thead><tr><th>${navLabel('Box','Boîte')}</th><th>${navLabel('Possible enchant stones','Enchant stones possibles')}</th></tr></thead>
              <tbody>
                <tr><th>${itemLink('Costume Enchant Stone (Upper) Box A')}</th><td>${stoneList(['Recovery Stone (Upper)', 'Heal effect Stone (Upper)', 'Large Stone (Upper)', 'Medium Stone (Upper)', 'Small Stone (Upper)', 'Critical Stone (Upper)', 'Variable Casting Stone (Upper)'])}</td></tr>
                <tr><th>${itemLink('Costume Enchant Stone (Middle) Box A')}</th><td>${stoneList(['Recovery Stone (Middle)', 'HP Stone (Middle)', 'SP Stone (Middle)', 'ATK Stone (Middle)', 'MATK Stone (Middle)', 'MHP Stone (Middle)', 'DEF Stone (Middle)', 'Critical Stone (Middle)', 'Variable Casting Stone (Middle)'])}</td></tr>
                <tr><th>${itemLink('Costume Enchant Stone (Lower) Box A')}</th><td>${stoneList(['Recovery Stone (Lower)', 'HIT Stone (Lower)', 'FLEE Stone (Lower)', 'HP Stone (Lower)', 'MSP Stone (Lower)', 'MDEF Stone (Lower)', 'ATK Stone (Lower)', 'MATK Stone (Lower)', 'Variable Casting Stone (Lower)', 'Critical Stone (Lower)'])}</td></tr>
                <tr><th>${itemLink('Costume Enchant Stone (Garment) Box A')}</th><td>${stoneList(['Double Attack Stone (Garment)', 'Critical Stone (Garment)'])}</td></tr>
              </tbody>
            </table></div>
          </section>

'''
f = f[:c_start] + new_costume + f[p_start:]

# PORING PANEL
p_start = f.index('          <section class="enchant-tab-panel" id="enchant-panel-poring">')
m_start = f.index('          <section class="enchant-tab-panel" id="enchant-panel-memorial">', p_start)
new_poring = r'''          <section class="enchant-tab-panel" id="enchant-panel-poring">
            <h2 id="poring-village">Poring Village Enchant</h2>
            <div class="table-wrap"><table class="enchant-simple-table">
              <thead><tr><th>${navLabel('Action','Action')}</th><th>${navLabel('Requirement','Prérequis')}</th><th>${navLabel('Cost','Coût')}</th><th>%</th><th>${navLabel('Break?','Casse ?')}</th><th>${navLabel('Result','Résultat')}</th></tr></thead>
              <tbody>
                <tr><td>${navLabel('Enchant','Enchant')}</td><td>${itemLink('Poring Village Leek')} / ${itemLink('Poring Village Carrot')}<br><strong>${navLabel('Item must be unequipped.','L’objet doit être déséquipé.')}</strong></td><td>${itemLink('Jellopy')} ×50 + 20 000 zeny</td><td>70%</td><td>${risk('safe','No','Non')}</td><td>${navLabel('Adds 1 random enchant.','Ajoute 1 enchant aléatoire.')}</td></tr>
                <tr><td>Reset</td><td>${navLabel('Enchanted Leek or Carrot, unequipped.','Leek ou Carrot enchanté, déséquipé.')}</td><td>${itemLink('Jellopy')} ×50 + 20 000 zeny</td><td>70%</td><td>${risk('safe','No','Non')}</td><td>${navLabel('Removes the current enchant on success.','Retire l’enchant actuel en cas de réussite.')}</td></tr>
              </tbody>
            </table></div>
            <p class="enchant-simple-note"><code>/navi prt_fild05 174/238</code></p>

            <h3>${navLabel('Possible enchants','Enchants possibles')}</h3>
            <div class="table-wrap"><table class="enchant-simple-table"><thead><tr><th>${navLabel('Type','Type')}</th><th>${navLabel('Possible results','Résultats possibles')}</th></tr></thead><tbody>
              <tr><th>${navLabel('Stats','Stats')}</th><td>STR +1 · AGI +1 · VIT +1 · INT +1 · DEX +1 · LUK +1</td></tr>
              <tr><th>SP</th><td>SP +10 · SP +25 · SP +50</td></tr>
              <tr><th>HP</th><td>HP +100 · HP +200</td></tr>
            </tbody></table></div>
          </section>

'''
f = f[:p_start] + new_poring + f[m_start:]

# MEMORIAL PANEL
m_start = f.index('          <section class="enchant-tab-panel" id="enchant-panel-memorial">')
t_start = f.index('          <section class="enchant-tab-panel" id="enchant-panel-taming">', m_start)
new_memorial = r'''          <section class="enchant-tab-panel" id="enchant-panel-memorial">
            <h2 id="memorial-gear">Memorial Dungeon Enchant</h2>

            <h3>${navLabel('Main rules','Règles principales')}</h3>
            <div class="table-wrap"><table class="enchant-simple-table">
              <thead><tr><th>${navLabel('Action','Action')}</th><th>${navLabel('Requirement','Prérequis')}</th><th>${navLabel('Cost','Coût')}</th><th>%</th><th>${navLabel('Break?','Casse ?')}</th><th>${navLabel('Description','Description')}</th></tr></thead>
              <tbody>
                <tr><td>${navLabel('Normal enchant','Enchant normal')}</td><td>${navLabel('Compatible Memorial Dungeon equipment.','Équipement Memorial Dungeon compatible.')}</td><td>100 000 zeny</td><td>—</td><td>${risk('safe','No','Non')}</td><td>${navLabel('Adds a random enchant from the available pool.','Ajoute un enchant aléatoire du pool disponible.')}</td></tr>
                <tr><td>${navLabel('Zeny reset','Reset zeny')}</td><td>${navLabel('Enchanted Memorial Dungeon equipment.','Équipement Memorial Dungeon enchanté.')}</td><td><strong>100 000 zeny</strong></td><td>—</td><td>${risk('danger','Yes','Oui')}</td><td>${navLabel('Resets the enchant. The equipment can be destroyed.','Reset l’enchantement. L’équipement peut être détruit.')}</td></tr>
                <tr><td>${navLabel('Safe reset','Reset sécurisé')}</td><td>${navLabel('Enchanted Memorial Dungeon equipment.','Équipement Memorial Dungeon enchanté.')}</td><td>${itemLink('Zelstar')} ×1</td><td>—</td><td>${risk('safe','No','Non')}</td><td>${navLabel('Removes the enchant without destroying the equipment.','Retire l’enchantement sans détruire l’équipement.')}</td></tr>
                <tr><td>1st Job Essence</td><td>${navLabel('Compatible Memorial armor +9. Use the 1st Job pool.','Armure Memorial compatible +9. Utiliser le pool 1st Job.')}</td><td>100 000 zeny</td><td>${navLabel('Exact rate not stated','Taux exact non indiqué')}</td><td>${risk('safe','No','Non')}</td><td>${navLabel('Random 1st Job Essence.','1st Job Essence aléatoire.')}</td></tr>
                <tr><td>2nd Job Essence</td><td>${navLabel('Compatible Expedition, Dispatching or Conqueror armor +9. Use the 2nd Job pool.','Armure Expedition, Dispatching ou Conqueror compatible +9. Utiliser le pool 2nd Job.')}</td><td>100 000 zeny</td><td>${navLabel('Exact rate not stated','Taux exact non indiqué')}</td><td>${risk('safe','No','Non')}</td><td>${navLabel('Random 2nd Job Essence. Not available from Subjugation armor.','2nd Job Essence aléatoire. Non disponible sur l’armure Subjugation.')}</td></tr>
              </tbody>
            </table></div>

            <h3>${navLabel('Equipment, slot and Job Essence access','Équipement, slot et accès Job Essence')}</h3>
            <div class="table-wrap"><table class="enchant-simple-table">
              <thead><tr><th>${navLabel('Equipment','Équipement')}</th><th>${navLabel('Requirement','Prérequis')}</th><th>${navLabel('Job Essence slot','Slot Job Essence')}</th><th>${navLabel('Available pool','Pool disponible')}</th></tr></thead>
              <tbody>
                <tr><th>Subjugation — Grade IV</th><td>${itemLink("Subjugation Team's Armor")} +9</td><td>4th slot</td><td>1st Job Essence</td></tr>
                <tr><th>Expedition — Grade III</th><td>${itemLink("Expedition's Armor")} / ${itemLink("Expedition's Robe")} +9</td><td>4th slot</td><td>1st Job Essence · 2nd Job Essence</td></tr>
                <tr><th>Dispatching — Grade II</th><td>${itemLink('Dispatching Chain Mail')} / ${itemLink('Dispatching Robe')} / ${itemLink('Dispatching Garment')} / ${itemLink('Dispatching Cloth')} +9</td><td>3rd slot</td><td>1st Job Essence · 2nd Job Essence</td></tr>
                <tr><th>Conqueror — Grade I</th><td>${itemLink('Conqueror Chain Mail')} / ${itemLink('Conqueror Robe')} / ${itemLink('Conqueror Garment')} / ${itemLink('Conqueror Cloth')} +9</td><td>2nd slot</td><td>1st Job Essence · 2nd Job Essence</td></tr>
              </tbody>
            </table></div>

            <h3>${navLabel('NPCs','NPC')}</h3>
            <div class="table-wrap"><table class="enchant-simple-table"><thead><tr><th>${navLabel('Use','Utilisation')}</th><th>${navLabel('Location','Emplacement')}</th></tr></thead><tbody>
              <tr><td>Subjugation / 1st Job</td><td><code>/navi prt_fild05 251/193</code></td></tr>
              <tr><td>${navLabel('Higher-rank enchant employees','Employés d’enchantement des rangs supérieurs')}</td><td><code>/navi prt_in 135/35</code> · <code>/navi prt_in 135/28</code></td></tr>
            </tbody></table></div>

            <h3>1st Job Essence</h3>
            <div class="table-wrap"><table class="enchant-simple-table"><thead><tr><th>Enchant</th><th>${navLabel('Requirement','Prérequis')}</th><th>${navLabel('Cost','Coût')}</th><th>%</th><th>${navLabel('Break?','Casse ?')}</th><th>${navLabel('Description','Description')}</th></tr></thead><tbody>
              ${firstEssences.flatMap(e=>[
                `<tr><th>${itemLink(e.names[0])}</th><td>${navLabel('Compatible Memorial armor +9 · 1st Job pool','Armure Memorial compatible +9 · pool 1st Job')}</td><td>100 000 zeny</td><td>—</td><td>${risk('safe','No','Non')}</td><td class="essence-effect">${effectHtml(e.lv1)}</td></tr>`,
                `<tr><th>${itemLink(e.names[1])}</th><td>${navLabel('Compatible Memorial armor +9 · 1st Job pool','Armure Memorial compatible +9 · pool 1st Job')}</td><td>100 000 zeny</td><td>—</td><td>${risk('safe','No','Non')}</td><td class="essence-effect">${effectHtml(e.lv2)}</td></tr>`
              ]).join('')}
            </tbody></table></div>

            <h3>2nd Job Essence</h3>
            <div class="table-wrap"><table class="enchant-simple-table"><thead><tr><th>Enchant</th><th>${navLabel('Requirement','Prérequis')}</th><th>${navLabel('Cost','Coût')}</th><th>%</th><th>${navLabel('Break?','Casse ?')}</th><th>${navLabel('Description','Description')}</th></tr></thead><tbody>
              ${secondEssences.flatMap(e=>[
                `<tr><th>${itemLink(e.names[0])}</th><td>${navLabel('Expedition+ compatible armor +9 · 2nd Job pool','Armure Expedition+ compatible +9 · pool 2nd Job')}</td><td>100 000 zeny</td><td>—</td><td>${risk('safe','No','Non')}</td><td class="essence-effect">${effectHtml(e.i1)}</td></tr>`,
                `<tr><th>${itemLink(e.names[1])}</th><td>${navLabel('Expedition+ compatible armor +9 · 2nd Job pool','Armure Expedition+ compatible +9 · pool 2nd Job')}</td><td>100 000 zeny</td><td>—</td><td>${risk('safe','No','Non')}</td><td class="essence-effect">${effectHtml(e.i2)}</td></tr>`,
                `<tr><th>${itemLink(e.names[2])}</th><td>${navLabel('Expedition+ compatible armor +9 · 2nd Job pool','Armure Expedition+ compatible +9 · pool 2nd Job')}</td><td>100 000 zeny</td><td>—</td><td>${risk('safe','No','Non')}</td><td class="essence-effect">${effectHtml(e.ii1)}</td></tr>`,
                `<tr><th>${itemLink(e.names[3])}</th><td>${navLabel('Expedition+ compatible armor +9 · 2nd Job pool','Armure Expedition+ compatible +9 · pool 2nd Job')}</td><td>100 000 zeny</td><td>—</td><td>${risk('safe','No','Non')}</td><td class="essence-effect">${effectHtml(e.ii2)}</td></tr>`
              ]).join('')}
            </tbody></table></div>

            <h3>${navLabel('Normal random options','Options aléatoires normales')}</h3>
            <div class="table-wrap"><table class="enchant-simple-table"><thead><tr><th>${navLabel('Type','Type')}</th><th>${navLabel('Possible options','Options possibles')}</th></tr></thead><tbody>
              <tr><th>${navLabel('Stats','Stats')}</th><td>STR +1/+2 · AGI +1/+2 · VIT +1/+2 · INT +1/+2 · DEX +1/+2 · LUK +1/+2</td></tr>
              <tr><th>${navLabel('Utility','Utilitaire')}</th><td>FLEE +3 · CRI +1 · DEF +15 · MDEF +2</td></tr>
              <tr><th>HP</th><td>Max HP +50 · +100 · +200</td></tr>
              <tr><th>+9 HP</th><td>Max HP +300 · +400</td></tr>
            </tbody></table></div>
          </section>

'''
f = f[:m_start] + new_memorial + f[t_start:]

# TAMING PANEL
# Replace the complete Taming panel until the close of enchant-tab-panels.
t_start = f.index('          <section class="enchant-tab-panel" id="enchant-panel-taming">')
panels_end = f.index('        </div>\n      </div>\n\n      ${officialSources([', t_start)
new_taming = r'''          <section class="enchant-tab-panel" id="enchant-panel-taming">
            <h2 id="taming-ring">Taming Ring</h2>
            <div class="table-wrap"><table class="enchant-simple-table">
              <thead><tr><th>${navLabel('Action','Action')}</th><th>${navLabel('Requirement','Prérequis')}</th><th>${navLabel('Cost','Coût')}</th><th>%</th><th>${navLabel('Break?','Casse ?')}</th><th>${navLabel('Description','Description')}</th></tr></thead>
              <tbody>
                <tr><td>${navLabel('Buy Taming Ring','Acheter Taming Ring')}</td><td>—</td><td>50 000 zeny</td><td>100%</td><td>${risk('safe','No','Non')}</td><td>${itemLink('Taming Ring')}</td></tr>
                <tr><td>Lv.1</td><td>${navLabel('Taming Ring equipped in Accessory Right + 1 Pet Egg.','Taming Ring équipée en Accessory Right + 1 Pet Egg.')}</td><td>1 Pet Egg</td><td>—</td><td>—</td><td>${navLabel('Adds the selected pet enchant at Lv.1.','Ajoute l’enchant du pet sélectionné en Lv.1.')}</td></tr>
                <tr><td>Lv.2</td><td>${navLabel('Lv.1 enchant + a second identical Pet Egg.','Enchant Lv.1 + un deuxième Pet Egg identique.')}</td><td>1 Pet Egg</td><td>50%</td><td>—</td><td>${navLabel('Attempts to upgrade the same pet enchant to Lv.2.','Tente de passer le même enchant de pet en Lv.2.')}</td></tr>
                <tr><td>Reset</td><td>${navLabel('Enchanted Taming Ring.','Taming Ring enchantée.')}</td><td>—</td><td>—</td><td>—</td><td>${navLabel('Removes the current pet enchant.','Retire l’enchant de pet actuel.')}</td></tr>
              </tbody>
            </table></div>

            <h3>${navLabel('Taming Merchants','Taming Merchants')}</h3>
            <div class="table-wrap"><table class="enchant-simple-table"><thead><tr><th>${navLabel('City','Ville')}</th><th>/navi</th></tr></thead><tbody>
              <tr><td>Payon</td><td><code>/navi payon 175/131</code></td></tr>
              <tr><td>Geffen</td><td><code>/navi geffen 193/152</code></td></tr>
              <tr><td>Izlude</td><td><code>/navi izlude 72/98</code></td></tr>
              <tr><td>Morocc</td><td><code>/navi morocc 203/83</code></td></tr>
              <tr><td>Prontera</td><td><code>/navi prontera 218/21</code></td></tr>
            </tbody></table></div>
          </section>
'''
f = f[:t_start] + new_taming + f[panels_end:]

# Remove obsolete CSS reading-key block if still present in page rendering context is irrelevant;
# keep only simple effect bullets. No meta-writing in visible guide.
for forbidden in [
    'How to read the effects',
    'Comment lire les effets',
    'Trigger → Effect → Duration',
    'Déclencheur → Effet → Durée',
    'The exact zeny-reset cost and success/destruction rate are not displayed',
    'Le coût exact et le taux de réussite/destruction du reset en zeny ne sont pas affichés',
    'The important point is that Memorial Dungeon enchanting has different pools',
    'Le point important est que Memorial Dungeon Enchant possède plusieurs pools'
]:
    assert forbidden not in f, forbidden

# Required corrections / layout checks.
for required in [
    '<strong>100 000 zeny</strong>',
    "risk('danger','Yes','Oui')",
    'Item must be unequipped.',
    '70%',
    '1st Job Essence',
    '2nd Job Essence',
    'enchant-simple-table',
    'Brandish Spear damage by 40% for 60 seconds'
]:
    assert required in f, required

s = s[:fn_start] + f + s[fn_end:]
p.write_text(s, encoding='utf-8')
