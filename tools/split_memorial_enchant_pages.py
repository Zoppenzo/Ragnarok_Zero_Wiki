from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# 1) Fix the obvious Taming Ring display issue: buying an item has no success rate.
s = s.replace("<tr><td>${navLabel('Buy Taming Ring','Acheter Taming Ring')}</td><td>—</td><td>50 000 zeny</td><td>100%</td><td>${risk('safe','No','Non')}</td><td>${itemLink('Taming Ring')}</td></tr>",
              "<tr><td>${navLabel('Buy Taming Ring','Acheter Taming Ring')}</td><td>—</td><td>50 000 zeny</td><td>—</td><td>—</td><td>${itemLink('Taming Ring')}</td></tr>")

# 2) Insert separate Memorial grade page rendering inside enchantmentPage, where all local helpers/data are available.
anchor = "    return `${breadcrumbs([{label:title}])}\n"
idx = s.index(anchor, s.index('  function enchantmentPage(topic) {'))
insert = r'''    const mdGradePages = {
      'subjugation-grade-iv': {
        title:'Subjugation Armor — Grade IV',
        status:navLabel('Current rank','Rang actuel'),
        items:mdSubjugationItems,
        intro:navLabel('Subjugation equipment is the Grade IV Memorial Dungeon set. Each piece has its own enchant table below. Job Essence is only shown on the compatible armor at +9.','L’équipement Subjugation correspond au Grade IV des Memorial Dungeons. Chaque pièce possède son propre tableau d’enchantement ci-dessous. Les Job Essence ne sont affichées que sur l’armure compatible à +9.')
      },
      'expedition-grade-iii': {
        title:'Expedition Armor — Grade III',
        status:navLabel('Higher rank','Rang supérieur'),
        items:mdExpeditionItems,
        intro:navLabel('Expedition is the Grade III Memorial Dungeon equipment family. Armor and Robe have their own +9 Job Essence slot; the other pieces keep normal enchant slots.','Expedition correspond au Grade III. Armor et Robe possèdent leur slot Job Essence à +9 ; les autres pièces conservent leurs slots d’enchantement normaux.')
      },
      'dispatching-grade-ii': {
        title:'Dispatching — Grade II',
        status:navLabel('Higher rank','Rang supérieur'),
        items:mdDispatchingItems,
        intro:navLabel('Dispatching is the Grade II Memorial Dungeon equipment family. The compatible armor-type pieces use the 3rd slot for Job Essence at +9.','Dispatching correspond au Grade II. Les pièces de type armure compatibles utilisent le 3rd slot pour les Job Essence à +9.')
      },
      'conqueror-grade-i': {
        title:'Conqueror — Grade I',
        status:navLabel('Higher rank','Rang supérieur'),
        items:mdConquerorItems,
        intro:navLabel('Conqueror is the Grade I Memorial Dungeon equipment family. The compatible armor-type pieces use the 2nd slot for Job Essence at +9.','Conqueror correspond au Grade I. Les pièces de type armure compatibles utilisent le 2nd slot pour les Job Essence à +9.')
      }
    };

    if (topic && topic._memorialGrade) {
      const g = mdGradePages[topic._memorialGrade];
      if (!g) return notFound();
      return `${breadcrumbs([
          {label:title,href:'#/wiki/enchantment'},
          {label:'Memorial Dungeon Enchant',href:'#/wiki/enchantment'},
          {label:g.title}
        ])}
        <div class="article-heading"><h1>${icon('item')}${g.title}</h1><div class="page-subtitle">${g.status}</div></div>
        <p class="article-lead">${g.intro}</p>

        <div class="table-wrap"><table class="enchant-simple-table">
          <thead><tr><th>${navLabel('Action','Action')}</th><th>${navLabel('Cost','Coût')}</th><th>%</th><th>${navLabel('Break?','Casse ?')}</th></tr></thead>
          <tbody>
            <tr><th>Enchant</th><td>100 000 zeny</td><td>—</td><td>${mdNoBreak()}</td></tr>
            <tr><th>Reset — zeny</th><td><strong>100 000 zeny</strong></td><td>70%</td><td>${mdBreak()}</td></tr>
            <tr><th>Reset — ${itemLink('Zelstar')}</th><td>${itemLink('Zelstar')} ×1</td><td>100%</td><td>${mdNoBreak()}</td></tr>
          </tbody>
        </table></div>
        <p class="enchant-simple-note">${navLabel('Zeny reset: 30% chance to destroy the equipment. Zelstar reset does not destroy it.','Reset zeny : 30 % de risque de détruire l’équipement. Le reset avec Zelstar ne détruit pas l’objet.')}</p>

        ${g.items.map(x=>mdItemTable({...x,open:true})).join('')}

        <div class="hero-actions">
          <a class="button" href="#/wiki/enchantment">← ${navLabel('Back to Enchantment','Retour à Enchantment')}</a>
        </div>
        ${officialSources([
          ['Memorial Dungeon Equipment Enchanting','https://old.criatura-academy.com/memorial-dungeons/equipment-enchanting/'],
          ['Memorial Dungeons — current guide','https://midgardhub.com/guides/memorial-dungeons'],
          ['Memorial equipment enchanting — Global reference','https://roz-global.info/donjon-equipement-enchantement.html']
        ])}`;
    }

'''
s = s[:idx] + insert + s[idx:]

# 3) Replace the giant Memorial tab with a clean index linking to four actual pages.
sec_start = s.index('          <section class="enchant-tab-panel" id="enchant-panel-memorial">')
sec_end = s.index('          <section class="enchant-tab-panel" id="enchant-panel-taming">', sec_start)
new_memorial = r'''          <section class="enchant-tab-panel" id="enchant-panel-memorial">
            <h2 id="memorial-gear">Memorial Dungeon Enchant</h2>
            <p>${navLabel('Choose the equipment grade. Each grade has its own page and its own per-item enchant tables.','Choisis le grade d’équipement. Chaque grade possède sa propre page avec les tableaux d’enchantement de chaque objet.')}</p>

            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px;margin:14px 0 20px">
              <a class="panel" href="#/wiki/enchantment-memorial-subjugation-grade-iv" style="display:block;color:inherit;text-decoration:none">
                <div class="panel-heading">Subjugation Armor — Grade IV</div>
                <div class="panel-body"><strong>${navLabel('Current rank','Rang actuel')}</strong><p>${navLabel('Open all Subjugation equipment enchant tables.','Ouvrir tous les tableaux d’enchantement Subjugation.')}</p></div>
              </a>
              <a class="panel" href="#/wiki/enchantment-memorial-expedition-grade-iii" style="display:block;color:inherit;text-decoration:none">
                <div class="panel-heading">Expedition Armor — Grade III</div>
                <div class="panel-body"><strong>Grade III</strong><p>${navLabel('Open all Expedition equipment enchant tables.','Ouvrir tous les tableaux d’enchantement Expedition.')}</p></div>
              </a>
              <a class="panel" href="#/wiki/enchantment-memorial-dispatching-grade-ii" style="display:block;color:inherit;text-decoration:none">
                <div class="panel-heading">Dispatching — Grade II</div>
                <div class="panel-body"><strong>Grade II</strong><p>${navLabel('Open all Dispatching equipment enchant tables.','Ouvrir tous les tableaux d’enchantement Dispatching.')}</p></div>
              </a>
              <a class="panel" href="#/wiki/enchantment-memorial-conqueror-grade-i" style="display:block;color:inherit;text-decoration:none">
                <div class="panel-heading">Conqueror — Grade I</div>
                <div class="panel-body"><strong>Grade I</strong><p>${navLabel('Open all Conqueror equipment enchant tables.','Ouvrir tous les tableaux d’enchantement Conqueror.')}</p></div>
              </a>
            </div>

            <div class="table-wrap"><table class="enchant-simple-table">
              <thead><tr><th>${navLabel('Action','Action')}</th><th>${navLabel('Cost','Coût')}</th><th>${navLabel('Break?','Casse ?')}</th></tr></thead>
              <tbody>
                <tr><th>Enchant</th><td>100 000 zeny</td><td>${mdNoBreak()}</td></tr>
                <tr><th>Reset — zeny</th><td>100 000 zeny</td><td>${mdBreak()}</td></tr>
                <tr><th>Reset — ${itemLink('Zelstar')}</th><td>${itemLink('Zelstar')} ×1</td><td>${mdNoBreak()}</td></tr>
              </tbody>
            </table></div>
          </section>

'''
s = s[:sec_start] + new_memorial + s[sec_end:]

# 4) Route the four hidden wiki pages through the existing topicDetail route.
route_anchor = "    if (id === 'enchantment') return enchantmentPage(topic);\n"
assert route_anchor in s
route_add = route_anchor + "    if (id === 'enchantment-memorial-subjugation-grade-iv') return enchantmentPage({ ...topic, _memorialGrade:'subjugation-grade-iv' });\n" + \
    "    if (id === 'enchantment-memorial-expedition-grade-iii') return enchantmentPage({ ...topic, _memorialGrade:'expedition-grade-iii' });\n" + \
    "    if (id === 'enchantment-memorial-dispatching-grade-ii') return enchantmentPage({ ...topic, _memorialGrade:'dispatching-grade-ii' });\n" + \
    "    if (id === 'enchantment-memorial-conqueror-grade-i') return enchantmentPage({ ...topic, _memorialGrade:'conqueror-grade-i' });\n"
s = s.replace(route_anchor, route_add, 1)

# Validation assertions.
for x in [
    '#/wiki/enchantment-memorial-subjugation-grade-iv',
    '#/wiki/enchantment-memorial-expedition-grade-iii',
    '#/wiki/enchantment-memorial-dispatching-grade-ii',
    '#/wiki/enchantment-memorial-conqueror-grade-i',
    "_memorialGrade:'subjugation-grade-iv'",
    'Reset zeny : 30 % de risque de détruire l’équipement',
    '<td>50 000 zeny</td><td>—</td><td>—</td>'
]:
    assert x in s, x

p.write_text(s, encoding='utf-8')
