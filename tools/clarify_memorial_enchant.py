from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Poring Village: item must be unequipped before enchanting.
s = s.replace(
    "navLabel('Equip the Leek or Carrot you want to enchant.','Équipe le Leek ou la Carrot que tu veux enchanter.'),",
    "navLabel('Unequip the Leek or Carrot you want to enchant.','Déséquipe le Leek ou la Carrot que tu veux enchanter.'),",
    1
)
needle = "<li>${navLabel('You need a Poring Village Leek or Poring Village Carrot.','Il faut posséder un Poring Village Leek ou un Poring Village Carrot.')}</li>"
assert needle in s
s = s.replace(
    needle,
    needle + "\n              <li>${navLabel('The Leek or Carrot must be unequipped before talking to the enchanter.','Le Leek ou la Carrot doit être déséquipé avant de parler à l’enchanter.')}</li>",
    1
)

# Replace the Memorial Dungeon Enchant panel with a clearer decision-based guide.
start = s.index('          <section class="enchant-tab-panel" id="enchant-panel-memorial">')
end = s.index('          <section class="enchant-tab-panel" id="enchant-panel-taming">', start)

mem = r'''          <section class="enchant-tab-panel" id="enchant-panel-memorial">
            <h2 id="memorial-gear">Memorial Dungeon Enchant</h2>
            ${subnav([
              ['md-quick',navLabel('Which enchant can I get?','Quel enchant puis-je obtenir ?')],
              ['md-npcs',navLabel('NPCs / equipment','NPC / équipement')],
              ['md-process',navLabel('How enchanting works','Fonctionnement')],
              ['md-reset',navLabel('Reset / destruction','Reset / destruction')],
              ['md-slots',navLabel('Slots by rank','Slots selon le rang')],
              ['md-base-essence','1st Job Essence'],
              ['md-second-essence','2nd Job Essence'],
              ['md-knight',"Knight's Essence"],
              ['md-options',navLabel('Common options','Options communes')]
            ])}

            ${facts([
              [navLabel('Enchant cost','Coût enchantement'),'100 000 zeny'],
              [navLabel('Normal enchant can destroy the item?','L’enchantement normal peut casser l’objet ?'),risk('safe','No','Non')],
              [navLabel('Job Essence minimum refine','Raffinage minimum pour Job Essence'),'+9'],
              [navLabel('Can you choose the exact Job Essence?','Peut-on choisir la Job Essence exacte ?'),navLabel('No — the result is random inside the selected Job Essence pool.','Non — le résultat est aléatoire dans le pool de Job Essence sélectionné.')],
              [navLabel('Exact rate for one specific Job Essence','Taux exact d’une Job Essence précise'),navLabel('Not stated. Do not assume equal odds between all entries.','Non indiqué. Il ne faut pas supposer que toutes les entrées ont la même probabilité.')]
            ])}

            <h3 id="md-quick">${navLabel('Which enchant can I get?','Quel enchant puis-je obtenir ?')}</h3>
            <p>${navLabel(
              'The important point is that Memorial Dungeon enchanting has different pools. Your equipment, its refine level and the NPC/pool you use determine what can appear.',
              'Le point important est que Memorial Dungeon Enchant possède plusieurs pools. Ton équipement, son niveau de raffinage et le NPC/pool utilisé déterminent ce qui peut apparaître.'
            )}</p>
            <div class="table-wrap"><table>
              <thead><tr><th>${navLabel('What you want','Ce que tu veux')}</th><th>${navLabel('Equipment condition','Condition sur l’équipement')}</th><th>${navLabel('Pool / NPC','Pool / NPC')}</th><th>${navLabel('Possible result','Résultat possible')}</th></tr></thead>
              <tbody>
                <tr>
                  <th>${navLabel('Normal stat enchant','Enchantement de stats normal')}</th>
                  <td>${navLabel('Compatible Memorial Dungeon equipment. Job Essence is not required.','Équipement Memorial Dungeon compatible. Aucun prérequis Job Essence.')}</td>
                  <td>${navLabel('Normal enchant pool','Pool normal')}</td>
                  <td>FLEE / CRIT / DEF / MDEF / Max HP / STR / AGI / VIT / INT / DEX / LUK</td>
                </tr>
                <tr>
                  <th>1st Job Essence</th>
                  <td>${navLabel('Compatible armor-type Memorial Dungeon equipment at +9.','Équipement Memorial Dungeon compatible de type armure à +9.')}</td>
                  <td>1st Job Enchant Employee</td>
                  <td>${navLabel('A random Mage / Thief / Archer / Swordsman / Merchant / Acolyte Essence from the available pool.','Une Essence Mage / Thief / Archer / Swordsman / Merchant / Acolyte aléatoire parmi le pool disponible.')}</td>
                </tr>
                <tr>
                  <th>2nd Job Essence</th>
                  <td>${navLabel('Compatible +9 Expedition / Dispatching / Conqueror armor-type equipment.','Équipement compatible Expedition / Dispatching / Conqueror de type armure à +9.')}</td>
                  <td>2nd Job Enchant Employee</td>
                  <td>${navLabel('A random second-job Essence I or Essence II, Lv.1 or Lv.2, from the available pool.','Une Job Essence de seconde classe aléatoire : Essence I ou Essence II, Lv.1 ou Lv.2, parmi le pool disponible.')}</td>
                </tr>
              </tbody>
            </table></div>
            <div class="enchant-detail-note">${navLabel(
              'Subjugation uses the base-archetype Job Essence pool. Knight, Blacksmith, Assassin, Wizard, Priest, Hunter, Crusader, Alchemist, Rogue, Sage, Monk and Bard & Dancer belong to the 2nd Job pool.',
              'Subjugation utilise le pool de Job Essence des classes de base. Knight, Blacksmith, Assassin, Wizard, Priest, Hunter, Crusader, Alchemist, Rogue, Sage, Monk et Bard & Dancer appartiennent au pool 2nd Job.'
            )}</div>

            <h3 id="md-npcs">${navLabel('NPCs and equipment access','NPC et accès selon l’équipement')}</h3>
            <div class="table-wrap"><table>
              <thead><tr><th>${navLabel('System','Système')}</th><th>${navLabel('NPC / navigation','NPC / navigation')}</th><th>${navLabel('What it is used for','À quoi il sert')}</th></tr></thead>
              <tbody>
                <tr><th>Subjugation Team Enchant</th><td><code>/navi prt_in 135/35</code></td><td>${navLabel('Subjugation Team equipment and the base Job Essence pool.','Équipement Subjugation Team et pool de Job Essence des classes de base.')}</td></tr>
                <tr><th>Expedition Corps Enchant</th><td><code>/navi prt_in 135/28</code></td><td>${navLabel('Expedition Corps equipment and access to the 2nd Job Essence pool.','Équipement Expedition Corps et accès au pool 2nd Job Essence.')}</td></tr>
              </tbody>
            </table></div>

            <h3 id="md-process">${navLabel('How Memorial Dungeon enchanting works','Fonctionnement de Memorial Dungeon Enchant')}</h3>
            ${steps([
              navLabel('Choose the equipment piece you want to enchant.','Choisis la pièce d’équipement que tu veux enchanter.'),
              navLabel('Check its rank and refine level. This determines how many enchant slots it can use and which slot can become a Job Essence slot.','Vérifie son rang et son raffinage. Cela détermine le nombre de slots d’enchantement disponibles et quel slot peut devenir un slot Job Essence.'),
              navLabel('Choose the correct enchant NPC/pool. Use the normal pool for stat enchants, the 1st Job pool for base-class Essences, or the 2nd Job pool for second-class Essences.','Choisis le bon NPC/pool. Utilise le pool normal pour les stats, le pool 1st Job pour les Essences de classes de base, ou le pool 2nd Job pour les Essences de secondes classes.'),
              navLabel('Pay 100,000 zeny for the enchant attempt. The normal enchant action itself does not destroy the equipment.','Paie 100 000 zeny pour la tentative. L’enchantement normal lui-même ne détruit pas l’équipement.'),
              navLabel('The result is rolled from the pool you selected. For Job Essence, you choose the Job group pool, not the exact Essence name.','Le résultat est tiré dans le pool sélectionné. Pour Job Essence, tu choisis le groupe de Job, pas le nom exact de l’Essence.'),
              navLabel('If you want another result, reset/remove the enchant before rolling again.','Si tu veux un autre résultat, reset/retire l’enchantement avant de refaire un tirage.')
            ])}

            <h3 id="md-reset">${navLabel('Reset and item destruction','Reset et destruction de l’objet')}</h3>
            <div class="table-wrap"><table>
              <thead><tr><th>${navLabel('Action','Action')}</th><th>${navLabel('Cost','Coût')}</th><th>${navLabel('Result','Résultat')}</th><th>${navLabel('Item destruction','Destruction de l’objet')}</th></tr></thead>
              <tbody>
                <tr><td>${navLabel('Normal enchant','Enchantement normal')}</td><td>100 000 zeny</td><td>${navLabel('Random result from the selected pool','Résultat aléatoire dans le pool sélectionné')}</td><td>${risk('safe','0%','0 %')}</td></tr>
                <tr><td>${navLabel('Zeny reset','Reset en zeny')}</td><td>—</td><td>${risk('warn','70% without destruction','70 % sans destruction')}</td><td>${risk('danger','30% destruction','30 % de destruction')}</td></tr>
                <tr><td>${navLabel('Safe reset','Reset sécurisé')}</td><td>${itemLink('Zelstar')} ×1</td><td>${risk('safe','100% reset','100 % de reset')}</td><td>${risk('safe','0%','0 %')}</td></tr>
              </tbody>
            </table></div>
            <div class="enchant-detail-note">${navLabel(
              'The zeny amount for the risky reset is intentionally left blank here until it is checked directly in the current client. The destruction rule is kept separate so the guide does not mix the cost with the risk.',
              'Le montant en zeny du reset risqué est volontairement laissé vide ici jusqu’à lecture directe dans le client actuel. La règle de destruction reste affichée séparément pour ne pas mélanger le coût et le risque.'
            )}</div>

            <h3 id="md-slots">${navLabel('Job Essence slot by equipment rank','Slot Job Essence selon le rang de l’équipement')}</h3>
            <div class="table-wrap"><table>
              <thead><tr><th>${navLabel('Equipment family','Famille d’équipement')}</th><th>${navLabel('Compatible +9 armor-type pieces','Pièces de type armure compatibles à +9')}</th><th>${navLabel('Job Essence slot','Slot Job Essence')}</th><th>${navLabel('Job Essence access','Accès Job Essence')}</th></tr></thead>
              <tbody>
                <tr><th>Subjugation — Grade IV</th><td>${itemLink('Subjugation Armor')} / ${itemLink('Subjugation Robe')}</td><td>4th slot</td><td>1st Job Essence</td></tr>
                <tr><th>Expedition — Grade III</th><td>${itemLink('Expedition Armor')} / ${itemLink('Expedition Robe')}</td><td>4th slot</td><td>1st Job Essence / 2nd Job Essence</td></tr>
                <tr><th>Dispatching — Grade II</th><td>${itemLink('Dispatching Chain Mail')} / ${itemLink('Dispatching Robe')} / ${itemLink('Dispatching Garment')} / ${itemLink('Dispatching Cloth')}</td><td>3rd slot</td><td>1st Job Essence / 2nd Job Essence</td></tr>
                <tr><th>Conqueror — Grade I</th><td>${itemLink('Conqueror Chain Mail')} / ${itemLink('Conqueror Robe')} / ${itemLink('Conqueror Garment')} / ${itemLink('Conqueror Cloth')}</td><td>2nd slot</td><td>1st Job Essence / 2nd Job Essence</td></tr>
              </tbody>
            </table></div>
            <p>${navLabel(
              'The +9 requirement applies to the armor-type piece receiving Job Essence. Shoes, rings and the other Memorial Dungeon pieces can still use their normal enchant slots, but they do not become Job Essence armor simply because they are +9.',
              'Le prérequis +9 concerne la pièce de type armure qui reçoit Job Essence. Les shoes, rings et autres pièces Memorial Dungeon peuvent utiliser leurs slots d’enchantement normaux, mais elles ne deviennent pas des armures Job Essence simplement parce qu’elles sont +9.'
            )}</p>

            <h3 id="md-base-essence">1st Job Essence</h3>
            <p>${navLabel(
              'Use the 1st Job Enchant Employee when you want the base-class Essence pool. The exact Essence and its level are random inside that pool.',
              'Utilise le 1st Job Enchant Employee lorsque tu veux le pool des Essences de classes de base. L’Essence exacte et son niveau sont aléatoires dans ce pool.'
            )}</p>
            <div class="table-wrap"><table><thead><tr><th>${navLabel('Job','Job')}</th><th>Lv.1</th><th>Lv.2</th></tr></thead><tbody>
              ${firstEssences.map(e=>`<tr><th>${esc(e.job)}</th><td class="essence-effect"><strong>${itemLink(e.names[0])}</strong><br>${esc(e.lv1)}</td><td class="essence-effect"><strong>${itemLink(e.names[1])}</strong><br>${esc(e.lv2)}</td></tr>`).join('')}
            </tbody></table></div>

            <h3 id="md-second-essence">2nd Job Essence</h3>
            <p>${navLabel(
              'Use the 2nd Job Enchant Employee when you want second-class Essences. Each second job has two different lines, Essence I and Essence II, and each line can appear as Lv.1 or Lv.2. The exact result is random.',
              'Utilise le 2nd Job Enchant Employee lorsque tu veux les Essences de secondes classes. Chaque seconde classe possède deux lignes différentes, Essence I et Essence II, et chaque ligne peut apparaître en Lv.1 ou Lv.2. Le résultat exact est aléatoire.'
            )}</p>
            <div class="table-wrap"><table><thead><tr><th>${navLabel('Job','Job')}</th><th>Essence I Lv.1</th><th>Essence I Lv.2</th><th>Essence II Lv.1</th><th>Essence II Lv.2</th></tr></thead><tbody>
              ${secondEssences.map(e=>`<tr><th>${esc(e.job)}</th><td class="essence-effect"><strong>${itemLink(e.names[0])}</strong><br>${esc(e.i1)}</td><td class="essence-effect"><strong>${itemLink(e.names[1])}</strong><br>${esc(e.i2)}</td><td class="essence-effect"><strong>${itemLink(e.names[2])}</strong><br>${esc(e.ii1)}</td><td class="essence-effect"><strong>${itemLink(e.names[3])}</strong><br>${esc(e.ii2)}</td></tr>`).join('')}
            </tbody></table></div>

            <h3 id="md-knight">${navLabel("Example: how to roll Knight's Essence","Exemple : comment obtenir Knight's Essence")}</h3>
            <div class="panel"><div class="panel-body">
              <ol class="enchant-steps">
                <li>${navLabel('Use compatible Expedition, Dispatching or Conqueror armor-type Memorial Dungeon equipment refined to +9.','Utilise un équipement Memorial Dungeon compatible de type armure Expedition, Dispatching ou Conqueror raffiné à +9.')}</li>
                <li>${navLabel('Use the 2nd Job Enchant Employee / 2nd Job pool. Do not use the Subjugation base Job Essence pool if your goal is Knight.','Utilise le 2nd Job Enchant Employee / pool 2nd Job. N’utilise pas le pool Job Essence de base Subjugation si ton objectif est Knight.')}</li>
                <li>${navLabel('Enchant the Job Essence slot corresponding to the equipment rank: 4th slot on Expedition, 3rd on Dispatching, 2nd on Conqueror.','Enchante le slot Job Essence correspondant au rang : 4th slot sur Expedition, 3rd sur Dispatching, 2nd sur Conqueror.')}</li>
                <li>${navLabel('The result is random inside the 2nd Job pool. Knight is not selected directly.','Le résultat est aléatoire dans le pool 2nd Job. Knight n’est pas sélectionné directement.')}</li>
              </ol>
              <p><strong>${navLabel('Knight results in this pool:','Résultats Knight présents dans ce pool :')}</strong><br>
                ${itemLink("Knight's Essence Lv.1")} · ${itemLink("Knight's Essence Lv.2")} · ${itemLink("Knight's Essence II Lv.1")} · ${itemLink("Knight's Essence II Lv.2")}
              </p>
              <p>${navLabel(
                'No exact per-Essence probability is shown because the documented system only states that the Job Essence result is random. The guide does not divide 100% by the number of entries.',
                'Aucun taux exact par Essence n’est affiché car le système documenté indique seulement que le résultat Job Essence est aléatoire. Le guide ne divise donc pas 100 % par le nombre d’entrées.'
              )}</p>
            </div></div>

            <h3 id="md-options">${navLabel('Common non-Job enchant options','Options communes hors Job Essence')}</h3>
            <p>${navLabel('These are the common stat-style results used by Memorial Dungeon equipment. Job Essence is a separate +9 armor result and follows the pool rules explained above.','Voici les résultats de stats communs de l’équipement Memorial Dungeon. Job Essence est un résultat séparé réservé aux armures +9 et suit les règles de pool expliquées ci-dessus.')}</p>
            <div class="table-wrap"><table class="enchant-rate-table"><thead><tr><th>${navLabel('Enchant','Enchant')}</th><th>${navLabel('Rate','Taux')}</th></tr></thead><tbody>${baseRates.map(r=>`<tr><td>${esc(r[0])}</td><td>${esc(r[1])}</td></tr>`).join('')}</tbody></table></div>

            <h3>${navLabel('+9 Garment / Shoes option table','Table des options Garment / Shoes +9')}</h3>
            <div class="table-wrap"><table><thead><tr><th>${navLabel('Enchant','Enchant')}</th><th>Garment +9</th><th>Shoes +9</th></tr></thead><tbody>${plus9Rates.map(r=>`<tr><td>${esc(r[0])}</td><td>${esc(r[1])}</td><td>${esc(r[2])}</td></tr>`).join('')}</tbody></table></div>

            <div class="hero-actions"><a class="button" href="#/memorial-dungeons">${miniIcon('map')}${navLabel('Open Memorial Dungeons','Ouvrir Memorial Dungeons')}</a></div>
          </section>

'''

s = s[:start] + mem + s[end:]

# Visible guide must not mention source-site names.
a = s.index('  function enchantmentPage(topic) {')
b = s.index('${officialSources([', a)
body = s[a:b]
for site in ['Criatura','MidgardHub','iRO Wiki','roz-global','TWRo','KRO']:
    assert site not in body, site

# Required clarity checks.
for x in [
    'Déséquipe le Leek ou la Carrot',
    'Le Leek ou la Carrot doit être déséquipé',
    'Which enchant can I get?',
    '2nd Job Enchant Employee',
    "Knight's Essence Lv.1",
    "Knight's Essence II Lv.2",
    'Aucun taux exact par Essence',
    'Subjugation utilise le pool de Job Essence des classes de base',
    'Expedition — Grade III',
    'Dispatching — Grade II',
    'Conqueror — Grade I'
]:
    assert x in s, x

# Ensure old wrong Poring instruction is gone.
assert 'Équipe le Leek ou la Carrot que tu veux enchanter.' not in s

p.write_text(s, encoding='utf-8')
