from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Add a strong red treatment for any destructive action.
css_anchor = '.enchant-simple-note { margin: 8px 0 14px; color: var(--muted); font-size: 12px; }'
assert css_anchor in s
if '.enchant-break-yes {' not in s:
    s = s.replace(css_anchor, css_anchor + '''
.enchant-break-yes {
  color: #b42318;
  font-weight: 800;
}
.enchant-item-block {
  margin: 14px 0;
  border: 1px solid var(--line-soft);
  background: #fff;
}
.enchant-item-block > summary {
  cursor: pointer;
  padding: 10px 12px;
  font-weight: 700;
  background: #f7f8fa;
  border-bottom: 1px solid transparent;
}
.enchant-item-block[open] > summary { border-bottom-color: var(--line-soft); }
.enchant-item-block .table-wrap { margin: 0; }
.enchant-item-block table { margin: 0; }
.enchant-grade-heading { margin-top: 24px; }
.enchant-grade-intro { margin: -4px 0 12px; color: var(--muted); }
''', 1)

fn_start = s.index('  function enchantmentPage(topic) {')
fn_end = s.index('\n  function ', fn_start + 10)
f = s[fn_start:fn_end]

# Helper definitions used only by the Memorial Dungeon Enchant tab.
return_marker = '    return `${breadcrumbs([{label:title}])}'
assert return_marker in f
if 'const mdCommonOptions =' not in f:
    helpers = r'''    const mdCommonOptions = [
      'FLEE +3','CRI +1','DEF +15','MDEF +2','Max HP +50','Max HP +100','Max HP +200',
      'STR +1','STR +2','AGI +1','AGI +2','VIT +1','VIT +2','INT +1','INT +2','DEX +1','DEX +2','LUK +1','LUK +2'
    ];
    const mdPlus9HpOptions = ['Max HP +300','Max HP +400'];
    const mdFirstEssenceRows = firstEssences.flatMap(e=>[
      {name:e.names[0], effect:e.lv1}, {name:e.names[1], effect:e.lv2}
    ]);
    const mdSecondEssenceRows = secondEssences.flatMap(e=>[
      {name:e.names[0], effect:e.i1}, {name:e.names[1], effect:e.i2},
      {name:e.names[2], effect:e.ii1}, {name:e.names[3], effect:e.ii2}
    ]);
    const mdNoBreak = () => risk('safe','No','Non');
    const mdBreak = () => `<span class="enchant-break-yes">${navLabel('Yes — 30% destruction','Oui — 30 % de destruction')}</span>`;
    const mdSlotLabel = slots => slots.join(' + ');
    const mdNormalRows = (name, slots) => mdCommonOptions.map(opt=>`<tr>
      <th>${esc(opt)}</th>
      <td>${itemLink(name)} · ${mdSlotLabel(slots)}</td>
      <td>100 000 zeny</td>
      <td>—</td>
      <td>${mdNoBreak()}</td>
      <td>${navLabel('Random normal enchant.','Enchant normal aléatoire.')}</td>
    </tr>`).join('');
    const mdEssenceRows = (name, slot, pools) => {
      const rows = [];
      if (pools.includes('first')) rows.push(...mdFirstEssenceRows);
      if (pools.includes('second')) rows.push(...mdSecondEssenceRows);
      return rows.map(x=>`<tr>
        <th>${itemLink(x.name)}</th>
        <td>${itemLink(name)} +9 · ${slot}</td>
        <td>100 000 zeny</td>
        <td>${navLabel('Exact rate not stated','Taux exact non indiqué')}</td>
        <td>${mdNoBreak()}</td>
        <td class="essence-effect">${effectHtml(x.effect)}</td>
      </tr>`).join('');
    };
    const mdExtraPlus9Rows = (name, slot) => mdPlus9HpOptions.map(opt=>`<tr>
      <th>${esc(opt)}</th>
      <td>${itemLink(name)} +9 · ${slot}</td>
      <td>100 000 zeny</td>
      <td>—</td>
      <td>${mdNoBreak()}</td>
      <td>${navLabel('Additional +9 armor option.','Option supplémentaire de l’armure +9.')}</td>
    </tr>`).join('');
    const mdResetRows = name => `<tr>
      <th>Reset — zeny</th>
      <td>${itemLink(name)} ${navLabel('with at least one enchant','avec au moins un enchant')}</td>
      <td>100 000 zeny</td>
      <td>70%</td>
      <td>${mdBreak()}</td>
      <td>${navLabel('30% chance to destroy the equipment.','30 % de risque de détruire l’équipement.')}</td>
    </tr><tr>
      <th>Reset — ${itemLink('Zelstar')}</th>
      <td>${itemLink(name)} ${navLabel('with at least one enchant','avec au moins un enchant')}</td>
      <td>${itemLink('Zelstar')} ×1</td>
      <td>100%</td>
      <td>${mdNoBreak()}</td>
      <td>${navLabel('Removes the enchants without destroying the equipment.','Retire les enchants sans détruire l’équipement.')}</td>
    </tr>`;
    const mdItemTable = ({name, normalSlots, essenceSlot=null, essencePools=[], open=false}) => `<details class="enchant-item-block" ${open?'open':''}>
      <summary>${itemLink(name)}</summary>
      <div class="table-wrap"><table class="enchant-simple-table">
        <thead><tr><th>Enchant</th><th>${navLabel('Requirement / slot','Prérequis / slot')}</th><th>${navLabel('Cost','Coût')}</th><th>%</th><th>${navLabel('Break?','Casse ?')}</th><th>${navLabel('Description','Description')}</th></tr></thead>
        <tbody>
          ${mdNormalRows(name, normalSlots)}
          ${essenceSlot ? mdExtraPlus9Rows(name, essenceSlot) : ''}
          ${essenceSlot ? mdEssenceRows(name, essenceSlot, essencePools) : ''}
          ${mdResetRows(name)}
        </tbody>
      </table></div>
    </details>`;

    const mdSubjugationItems = [
      {name:"Subjugation Team's Armor", normalSlots:['4th slot'], essenceSlot:'4th slot', essencePools:['first'], open:true},
      {name:"Subjugation Team's Shoulder Belt", normalSlots:['4th slot']},
      {name:"Subjugation Team's Boots", normalSlots:['4th slot']},
      {name:"Subjugation Team's Ring", normalSlots:['4th slot']}
    ];
    const mdExpeditionItems = [
      {name:'Expedition Armor', normalSlots:['4th slot'], essenceSlot:'4th slot', essencePools:['first','second'], open:true},
      {name:'Expedition Robe', normalSlots:['4th slot'], essenceSlot:'4th slot', essencePools:['first','second'], open:true},
      {name:'Expedition Manteau', normalSlots:['4th slot']},
      {name:'Expedition Muffler', normalSlots:['4th slot']},
      {name:'Expedition Boots', normalSlots:['4th slot']},
      {name:'Expedition Shoes', normalSlots:['4th slot']},
      {name:'Expedition Ring', normalSlots:['4th slot']},
      {name:'Expedition Magic Ring', normalSlots:['4th slot']}
    ];
    const mdDispatchingItems = [
      {name:'Dispatching Chain Mail', normalSlots:['4th slot'], essenceSlot:'3rd slot', essencePools:['first','second'], open:true},
      {name:'Dispatching Robe', normalSlots:['4th slot'], essenceSlot:'3rd slot', essencePools:['first','second'], open:true},
      {name:'Dispatching Garment', normalSlots:['4th slot'], essenceSlot:'3rd slot', essencePools:['first','second'], open:true},
      {name:'Dispatching Cloth', normalSlots:['4th slot'], essenceSlot:'3rd slot', essencePools:['first','second'], open:true},
      {name:'Dispatching Shoes', normalSlots:['3rd slot','4th slot']},
      {name:'Dispatching Magic Shoes', normalSlots:['3rd slot','4th slot']},
      {name:'Dispatching Boots', normalSlots:['3rd slot','4th slot']},
      {name:'Dispatching Greaves', normalSlots:['3rd slot','4th slot']},
      {name:'Dispatching Cape', normalSlots:['3rd slot','4th slot']},
      {name:'Dispatching Muffler', normalSlots:['3rd slot','4th slot']},
      {name:'Dispatching Manteau', normalSlots:['3rd slot','4th slot']},
      {name:'Dispatching Scouting Manteau', normalSlots:['3rd slot','4th slot']},
      {name:'Dispatching Necklace', normalSlots:['3rd slot','4th slot']},
      {name:'Dispatching Glove', normalSlots:['3rd slot','4th slot']},
      {name:'Dispatching Magic Ring', normalSlots:['3rd slot','4th slot']},
      {name:'Dispatching Ring', normalSlots:['3rd slot','4th slot']}
    ];
    const mdConquerorItems = [
      {name:'Conqueror Chain Mail', normalSlots:['3rd slot','4th slot'], essenceSlot:'2nd slot', essencePools:['first','second'], open:true},
      {name:'Conqueror Robe', normalSlots:['3rd slot','4th slot'], essenceSlot:'2nd slot', essencePools:['first','second'], open:true},
      {name:'Conqueror Garment', normalSlots:['3rd slot','4th slot'], essenceSlot:'2nd slot', essencePools:['first','second'], open:true},
      {name:'Conqueror Cloth', normalSlots:['3rd slot','4th slot'], essenceSlot:'2nd slot', essencePools:['first','second'], open:true},
      {name:'Conqueror Shoes', normalSlots:['2nd slot','3rd slot','4th slot']},
      {name:'Conqueror Magic Shoes', normalSlots:['2nd slot','3rd slot','4th slot']},
      {name:'Conqueror Boots', normalSlots:['2nd slot','3rd slot','4th slot']},
      {name:'Conqueror Greaves', normalSlots:['2nd slot','3rd slot','4th slot']},
      {name:'Conqueror Cape', normalSlots:['2nd slot','3rd slot','4th slot']},
      {name:'Conqueror Muffler', normalSlots:['2nd slot','3rd slot','4th slot']},
      {name:'Conqueror Manteau', normalSlots:['2nd slot','3rd slot','4th slot']},
      {name:'Conqueror Scouting Manteau', normalSlots:['2nd slot','3rd slot','4th slot']},
      {name:'Conqueror Necklace', normalSlots:['2nd slot','3rd slot','4th slot']},
      {name:'Conqueror Glove', normalSlots:['2nd slot','3rd slot','4th slot']},
      {name:'Conqueror Magic Ring', normalSlots:['2nd slot','3rd slot','4th slot']},
      {name:'Conqueror Ring', normalSlots:['2nd slot','3rd slot','4th slot']}
    ];

'''
    f = f.replace(return_marker, helpers + return_marker, 1)

mem_start = f.index('          <section class="enchant-tab-panel" id="enchant-panel-memorial">')
mem_end = f.index('          <section class="enchant-tab-panel" id="enchant-panel-taming">', mem_start)

new_mem = r'''          <section class="enchant-tab-panel" id="enchant-panel-memorial">
            <h2 id="memorial-gear">Memorial Dungeon Enchant</h2>

            <div class="table-wrap"><table class="enchant-simple-table">
              <thead><tr><th>${navLabel('Action','Action')}</th><th>${navLabel('Cost','Coût')}</th><th>%</th><th>${navLabel('Break?','Casse ?')}</th></tr></thead>
              <tbody>
                <tr><th>Enchant</th><td>100 000 zeny</td><td>—</td><td>${mdNoBreak()}</td></tr>
                <tr><th>Reset — zeny</th><td><strong>100 000 zeny</strong></td><td>70%</td><td>${mdBreak()}</td></tr>
                <tr><th>Reset — ${itemLink('Zelstar')}</th><td>${itemLink('Zelstar')} ×1</td><td>100%</td><td>${mdNoBreak()}</td></tr>
              </tbody>
            </table></div>
            <p class="enchant-simple-note">${navLabel('Zeny reset: 30% chance to destroy the equipment. Zelstar reset does not destroy it.','Reset zeny : 30 % de risque de détruire l’équipement. Le reset avec Zelstar ne détruit pas l’objet.')}</p>

            <h3>${navLabel('NPCs','NPC')}</h3>
            <div class="table-wrap"><table class="enchant-simple-table"><thead><tr><th>${navLabel('Equipment','Équipement')}</th><th>/navi</th></tr></thead><tbody>
              <tr><td>Subjugation</td><td><code>/navi prt_fild05 251/193</code></td></tr>
              <tr><td>Expedition / Dispatching / Conqueror</td><td><code>/navi prt_in 135/35</code> · <code>/navi prt_in 135/28</code></td></tr>
            </tbody></table></div>

            <h3 class="enchant-grade-heading" id="md-subjugation">Subjugation — Grade IV</h3>
            <p class="enchant-grade-intro">${navLabel('Each item is shown separately. Only Subjugation Team\'s Armor can roll Job Essence at +9.','Chaque objet est séparé. Seule Subjugation Team\'s Armor peut recevoir des Job Essence à +9.')}</p>
            ${mdSubjugationItems.map(mdItemTable).join('')}

            <h3 class="enchant-grade-heading" id="md-expedition">Expedition — Grade III</h3>
            <p class="enchant-grade-intro">${navLabel('Expedition Armor and Expedition Robe can roll Job Essence at +9. Other Expedition pieces use the normal enchant pool.','Expedition Armor et Expedition Robe peuvent recevoir des Job Essence à +9. Les autres pièces Expedition utilisent le pool normal.')}</p>
            ${mdExpeditionItems.map(mdItemTable).join('')}

            <h3 class="enchant-grade-heading" id="md-dispatching">Dispatching — Grade II</h3>
            <p class="enchant-grade-intro">${navLabel('Chain Mail, Robe, Garment and Cloth use the 3rd slot for Job Essence at +9. Their 4th slot remains a normal enchant slot.','Chain Mail, Robe, Garment et Cloth utilisent le 3rd slot pour les Job Essence à +9. Leur 4th slot reste un slot d’enchant normal.')}</p>
            ${mdDispatchingItems.map(mdItemTable).join('')}

            <h3 class="enchant-grade-heading" id="md-conqueror">Conqueror — Grade I</h3>
            <p class="enchant-grade-intro">${navLabel('Chain Mail, Robe, Garment and Cloth use the 2nd slot for Job Essence at +9. Their 3rd and 4th slots remain normal enchant slots.','Chain Mail, Robe, Garment et Cloth utilisent le 2nd slot pour les Job Essence à +9. Les 3rd et 4th slots restent des slots d’enchant normaux.')}</p>
            ${mdConquerorItems.map(mdItemTable).join('')}
          </section>

'''
f = f[:mem_start] + new_mem + f[mem_end:]

# Ensure the dangerous reset is red and every grade is represented.
for needle in [
    'enchant-break-yes', 'Yes — 30% destruction', 'Oui — 30 % de destruction',
    "Subjugation Team's Armor", 'Expedition Armor', 'Dispatching Chain Mail', 'Conqueror Chain Mail',
    'mdSubjugationItems.map(mdItemTable)', 'mdExpeditionItems.map(mdItemTable)',
    'mdDispatchingItems.map(mdItemTable)', 'mdConquerorItems.map(mdItemTable)'
]:
    assert needle in f or needle in s, needle

# Remove the previous mixed Memorial summary tables from the rendered panel.
for old in [
    'Equipment, slot and Job Essence access',
    'Équipement, slot et accès Job Essence',
    '<h3>1st Job Essence</h3>',
    '<h3>2nd Job Essence</h3>',
    'Normal random options'
]:
    assert old not in f[mem_start:mem_start+len(new_mem)+100], old

s = s[:fn_start] + f + s[fn_end:]
p.write_text(s, encoding='utf-8')
