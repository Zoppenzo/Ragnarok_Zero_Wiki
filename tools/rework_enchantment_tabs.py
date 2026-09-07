from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Update verification map for the new enchantment categories.
old_status = "'#/wiki/enchantment': { overview:'complete', costume:'partial', 'taming-ring':'complete', 'content-enchants':'partial' },"
new_status = "'#/wiki/enchantment': { costume:'partial', 'poring-village':'complete', 'memorial-gear':'partial', 'job-essences':'partial', 'taming-ring':'complete' },"
assert old_status in s, 'old enchantment status map not found'
s = s.replace(old_status, new_status, 1)

css_anchor = "/* Click-to-copy /navi commands */"
assert css_anchor in s
if '.enchant-tabs {' not in s:
    css = r'''
/* Enchantment system tabs */
.enchant-tabs { margin-top: 18px; }
.enchant-tab-input { position: absolute; opacity: 0; pointer-events: none; }
.enchant-tab-labels {
  display: flex;
  flex-wrap: wrap;
  gap: 3px;
  margin-bottom: 0;
  border-bottom: 1px solid var(--line);
}
.enchant-tab-labels label {
  display: inline-flex;
  align-items: center;
  min-height: 38px;
  padding: 8px 13px;
  margin-bottom: -1px;
  border: 1px solid transparent;
  border-bottom-color: var(--line);
  color: var(--blue);
  background: #f8f9fa;
  cursor: pointer;
  font-weight: 700;
}
.enchant-tab-labels label:hover { background: #fff; }
.enchant-tab-panels {
  padding: 2px 1px 6px;
  border-top: 0;
}
.enchant-tab-panel { display: none; }
#enchant-tab-costume:checked ~ .enchant-tab-labels label[for="enchant-tab-costume"],
#enchant-tab-poring:checked ~ .enchant-tab-labels label[for="enchant-tab-poring"],
#enchant-tab-memorial:checked ~ .enchant-tab-labels label[for="enchant-tab-memorial"],
#enchant-tab-essences:checked ~ .enchant-tab-labels label[for="enchant-tab-essences"],
#enchant-tab-taming:checked ~ .enchant-tab-labels label[for="enchant-tab-taming"] {
  color: var(--text);
  background: #fff;
  border-color: var(--line);
  border-bottom-color: #fff;
}
#enchant-tab-costume:checked ~ .enchant-tab-panels #enchant-panel-costume,
#enchant-tab-poring:checked ~ .enchant-tab-panels #enchant-panel-poring,
#enchant-tab-memorial:checked ~ .enchant-tab-panels #enchant-panel-memorial,
#enchant-tab-essences:checked ~ .enchant-tab-panels #enchant-panel-essences,
#enchant-tab-taming:checked ~ .enchant-tab-panels #enchant-panel-taming { display: block; }
.enchant-summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit,minmax(190px,1fr));
  gap: 8px;
  margin: 12px 0 16px;
}
.enchant-summary-grid > div {
  padding: 10px 12px;
  border: 1px solid var(--line-soft);
  background: #f8f9fa;
}
.enchant-summary-grid strong { display: block; margin-bottom: 4px; }
@media (max-width: 760px) {
  .enchant-tab-labels { display: grid; grid-template-columns: 1fr 1fr; }
  .enchant-tab-labels label { margin-bottom: 0; border: 1px solid var(--line-soft); }
}

'''
    s = s.replace(css_anchor, css + css_anchor, 1)

new_func = r'''  function enchantmentPage(topic) {
    const title = navLabel('Enchantment','Enchantement');
    const itemLink = name => memorialDbLink('items', name);
    const stoneList = names => names.map(itemLink).join(' · ');
    const statStones = slot => ['STR','INT','AGI','DEX','VIT','LUK'].map(x=>`${x} Stone (${slot})`);
    const conversionStones = slot => ['STR','INT','AGI','DEX','VIT','LUK'].map(x=>`${x} Conversion Stone (${slot})`);
    const poringOptions = ['STR +1','VIT +1','INT +1','DEX +1','AGI +1','LUK +1','SP +10','SP +25','SP +50','HP +100','HP +200'];
    const commonMemorial = [
      ['Stats','AGI +1 / +2 · DEX +1 / +2 · STR +1 / +2 · INT +1 / +2 · VIT +1 / +2 · LUK +1 / +2'],
      [navLabel('Combat','Combat'),'FLEE +3 · CRI +1'],
      [navLabel('Defense','Défense'),'DEF +15 · MDEF +2'],
      ['HP','Max HP +50 · Max HP +100 · Max HP +200']
    ];
    const baseEssences = ['Swordsman Essence Lv1','Merchant Essence Lv1','Thief Essence Lv1','Mage Essence Lv1','Acolyte Essence Lv1','Archer Essence Lv1'];

    return `${breadcrumbs([{label:title}])}
      <div class="article-heading"><h1>${icon('item')}${title}</h1><div class="page-subtitle">${t('fromWiki')}</div></div>
      <p class="article-lead">${navLabel(
        'Enchantment systems add bonuses through a dedicated NPC or interface. Each system has its own compatible equipment, materials and option pool; random drop Affixes remain a separate mechanic.',
        'Les systèmes d’enchantement ajoutent des bonus via un NPC ou une interface dédiée. Chaque système possède ses propres équipements compatibles, matériaux et pools d’options ; les Affixes aléatoires des drops restent une mécanique séparée.'
      )}</p>

      <div class="enchant-tabs">
        <input class="enchant-tab-input" type="radio" name="enchant-tabs" id="enchant-tab-costume" checked>
        <input class="enchant-tab-input" type="radio" name="enchant-tabs" id="enchant-tab-poring">
        <input class="enchant-tab-input" type="radio" name="enchant-tabs" id="enchant-tab-memorial">
        <input class="enchant-tab-input" type="radio" name="enchant-tabs" id="enchant-tab-essences">
        <input class="enchant-tab-input" type="radio" name="enchant-tabs" id="enchant-tab-taming">

        <div class="enchant-tab-labels" role="tablist" aria-label="${esc(navLabel('Enchantment categories','Catégories d’enchantement'))}">
          <label for="enchant-tab-costume">${navLabel('Costumes','Costumes')}</label>
          <label for="enchant-tab-poring">Poring Village</label>
          <label for="enchant-tab-memorial">${navLabel('Memorial Equipment','Équipement mémorial')}</label>
          <label for="enchant-tab-essences">${navLabel('Job Essences','Essences de classe')}</label>
          <label for="enchant-tab-taming">Taming Ring</label>
        </div>

        <div class="enchant-tab-panels">
          <section class="enchant-tab-panel" id="enchant-panel-costume">
            <h2 id="costume">${navLabel('Costume enchantments','Enchantements de costumes')}</h2>
            <p>${navLabel(
              'Costumes use dedicated enchantment stones. An enchantment box can be purchased for 10,000 zeny; place 5 compatible costumes in the box to obtain a random enchantment stone or stone box, then apply a compatible stone to the matching costume slot.',
              'Les costumes utilisent des pierres d’enchantement dédiées. Une boîte d’enchantement peut être achetée pour 10 000 zeny ; place 5 costumes compatibles dans la boîte pour obtenir aléatoirement une pierre ou une boîte de pierres, puis applique une pierre compatible à l’emplacement de costume correspondant.'
            )}</p>
            <div class="enchant-summary-grid">
              <div><strong>${navLabel('Enchanter','Enchanteur')}</strong><code>/navi prontera 263/270</code></div>
              <div><strong>${navLabel('Box cost','Coût de la boîte')}</strong>10 000 zeny</div>
              <div><strong>${navLabel('Exchange','Échange')}</strong>${navLabel('5 compatible costumes','5 costumes compatibles')}</div>
            </div>
            <h3>${navLabel('Currently documented stone families','Familles de pierres actuellement documentées')}</h3>
            <div class="table-wrap"><table>
              <thead><tr><th>${navLabel('Costume slot','Emplacement')}</th><th>${navLabel('Possible stones','Pierres possibles')}</th></tr></thead>
              <tbody>
                <tr><th>Upper</th><td>${stoneList(statStones('Upper'))}</td></tr>
                <tr><th>Middle</th><td>${stoneList([...statStones('Middle'),...conversionStones('Middle')])}</td></tr>
                <tr><th>Lower</th><td>${stoneList(['Recovery Stone (Lower)','HIT Stone (Lower)','FLEE Stone (Lower)','HP Stone (Lower)','MSP Stone (Lower)','MDEF Stone (Lower)','ATK Stone (Lower)','MATK Stone (Lower)','Variable Casting Stone (Lower)','Critical Stone (Lower)',...conversionStones('Lower')])}</td></tr>
                <tr><th>Garment</th><td>${stoneList(['Double Attack Stone (Garment)','Critical Stone (Garment)','Variable Casting Stone (Garment)'])}</td></tr>
              </tbody>
            </table></div>
          </section>

          <section class="enchant-tab-panel" id="enchant-panel-poring">
            <h2 id="poring-village">Poring Village</h2>
            <p>${navLabel(
              'The Poring Village headgears use their own enchantment system. Poring Village Leek and Poring Village Carrot can receive one enchantment each.',
              'Les headgears de Poring Village utilisent leur propre système. Poring Village Leek et Poring Village Carrot peuvent recevoir un seul enchantement chacun.'
            )}</p>
            <div class="enchant-summary-grid">
              <div><strong>${navLabel('Enchanter','Enchanteur')}</strong><code>/navi prt_fild05 174/238</code></div>
              <div><strong>${navLabel('Enchant cost','Coût enchantement')}</strong>${itemLink('Jellopy')} ×50 + 20 000 zeny</div>
              <div><strong>${navLabel('Reset cost','Coût du reset')}</strong>${itemLink('Jellopy')} ×50 + 20 000 zeny</div>
              <div><strong>${navLabel('Failure','Échec')}</strong>30 % · ${navLabel('item is not destroyed','l’objet n’est pas détruit')}</div>
            </div>
            <div class="table-wrap"><table>
              <thead><tr><th>${navLabel('Compatible equipment','Équipement compatible')}</th><th>${navLabel('Possible enchants','Enchantements possibles')}</th></tr></thead>
              <tbody><tr><td>${itemLink('Poring Village Leek')}<br>${itemLink('Poring Village Carrot')}</td><td>${poringOptions.map(esc).join(' · ')}</td></tr></tbody>
            </table></div>
            <div class="hero-actions"><a class="button" href="#/memorial-dungeons/poring-village">${miniIcon('map')}${navLabel('Open Poring Village guide','Ouvrir le guide Poring Village')}</a></div>
          </section>

          <section class="enchant-tab-panel" id="enchant-panel-memorial">
            <h2 id="memorial-gear">${navLabel('Memorial Dungeon equipment','Équipement des Mémorial Donjons')}</h2>
            <p>${navLabel(
              'Memorial Dungeon equipment has a dedicated random enchantment pool. A standard enchant attempt costs 100,000 zeny. The exact reset rules are intentionally not displayed until they are verified directly in the current client.',
              'L’équipement des Mémorial Donjons possède un pool d’enchantements aléatoires dédié. Une tentative d’enchantement standard coûte 100 000 zeny. Les règles exactes du reset ne sont volontairement pas affichées tant qu’elles ne sont pas vérifiées directement dans le client actuel.'
            )}</p>
            <div class="enchant-summary-grid">
              <div><strong>${navLabel('Enchant cost','Coût enchantement')}</strong>100 000 zeny</div>
              <div><strong>${navLabel('Common pool','Pool commun')}</strong>${navLabel('Stats, combat, defense and HP','Stats, combat, défense et HP')}</div>
              <div><strong>+9 Armor</strong>${navLabel('Can access the Job Essence pool','Peut accéder au pool des Essences de classe')}</div>
            </div>
            <div class="table-wrap"><table>
              <thead><tr><th>${navLabel('Category','Catégorie')}</th><th>${navLabel('Possible enchants','Enchantements possibles')}</th></tr></thead>
              <tbody>${commonMemorial.map(r=>`<tr><th>${esc(r[0])}</th><td>${esc(r[1])}</td></tr>`).join('')}</tbody>
            </table></div>
            <div class="hero-actions"><a class="button" href="#/memorial-dungeons">${miniIcon('map')}${navLabel('Open Memorial Dungeons','Ouvrir Mémorial Donjon')}</a></div>
          </section>

          <section class="enchant-tab-panel" id="enchant-panel-essences">
            <h2 id="job-essences">${navLabel('Job Essence enchantments','Enchantements Essences de classe')}</h2>
            <p>${navLabel(
              'At +9, compatible Memorial Dungeon armor can roll a class-oriented Essence instead of only the common stat pool. The first documented Subjugation set contains one Lv.1 Essence for each first-job archetype.',
              'À +9, une armure compatible des Mémorial Donjons peut obtenir une Essence orientée classe au lieu de se limiter au pool commun de stats. Le premier ensemble documenté de Répression contient une Essence Lv.1 pour chaque archétype de première classe.'
            )}</p>
            <div class="table-wrap"><table>
              <thead><tr><th>${navLabel('Archetype','Archétype')}</th><th>Essence</th></tr></thead>
              <tbody>
                ${baseEssences.map(name=>`<tr><td>${esc(name.replace(' Essence Lv1',''))}</td><td>${itemLink(name)}</td></tr>`).join('')}
              </tbody>
            </table></div>
            <div class="notice info"><svg class="notice-icon"><use href="#i-info"></use></svg><div>${navLabel(
              'Additional Essence tiers and second-job Essence effects will be added here only after they are verified for the current server content.',
              'Les paliers d’Essence supplémentaires et les effets des Essences de secondes classes seront ajoutés ici uniquement après vérification sur le contenu actuel du serveur.'
            )}</div></div>
          </section>

          <section class="enchant-tab-panel" id="enchant-panel-taming">
            <h2 id="taming-ring">Taming Ring</h2>
            <p>${navLabel(
              'A Pet Egg can be sealed into a Taming Ring to give the ring that pet’s Lv.1 enchant effect. Upgrading the same enchant to Lv.2 requires a second egg of the same pet and has a 50% success rate.',
              'Un Pet Egg peut être scellé dans une Taming Ring afin de donner à la bague l’effet d’enchantement Lv.1 de ce pet. Le passage du même enchantement au Lv.2 demande un second œuf du même pet et possède 50 % de chance de réussite.'
            )}</p>
            <div class="enchant-summary-grid">
              <div><strong>${navLabel('Ring price','Prix de la bague')}</strong>50 000 zeny</div>
              <div><strong>Lv.1</strong>${navLabel('1 Pet Egg','1 Pet Egg')}</div>
              <div><strong>Lv.2</strong>${navLabel('2nd identical Pet Egg · 50% success','2e Pet Egg identique · 50 % de réussite')}</div>
            </div>
            <h3>${navLabel('Taming Merchants','Taming Merchants')}</h3>
            <div class="table-wrap"><table><thead><tr><th>${navLabel('City','Ville')}</th><th>${navLabel('Navigation','Navigation')}</th></tr></thead><tbody>
              <tr><td>Payon</td><td><code>/navi payon 175/131</code></td></tr>
              <tr><td>Geffen</td><td><code>/navi geffen 193/152</code></td></tr>
              <tr><td>Izlude</td><td><code>/navi izlude 72/98</code></td></tr>
              <tr><td>Morocc</td><td><code>/navi morocc 203/83</code></td></tr>
              <tr><td>Prontera</td><td><code>/navi prontera 218/21</code></td></tr>
            </tbody></table></div>
            <div class="hero-actions"><a class="button" href="#/wiki/pet-system">${miniIcon('monster')}${navLabel('Open Pet System','Ouvrir Système de Pet')}</a></div>
          </section>
        </div>
      </div>

      ${officialSources([
        ['MidgardHub — New Player Guide','https://midgardhub.com/guides/new-player'],
        ['MidgardHub — Memorial Dungeons','https://midgardhub.com/guides/memorial-dungeons'],
        ['MidgardHub — Item Database','https://midgardhub.com/database/items'],
        ['Criatura Academy — Memorial Dungeon Equipment Enchanting','https://old.criatura-academy.com/memorial-dungeons/equipment-enchanting/'],
        ['Ragnarok Zero Global Guide — Memorial Equipment Enchanting','https://roz-global.info/donjon-equipement-enchantement.html'],
        ['Ragnarok Zero Global Guide — Qpets','https://roz-global.info/qpets.html']
      ])}`;
  }'''

pattern = re.compile(r"  function enchantmentPage\(topic\) \{.*?\n  \}\n\n  function ", re.S)
m = pattern.search(s)
assert m, 'enchantmentPage function not found'
s = s[:m.start()] + new_func + "\n\n  function " + s[m.end():]

# Validation: the old long-page structure must be gone and all new tabs present.
for token in [
    'enchant-tab-costume','enchant-tab-poring','enchant-tab-memorial','enchant-tab-essences','enchant-tab-taming',
    'Poring Village Leek','100 000 zeny','Swordsman Essence Lv1','/navi payon 175/131'
]:
    assert token in s, token
assert 'Content-specific enchantments' not in s
assert "'content-enchants':'partial'" not in s

p.write_text(s, encoding='utf-8')
