(() => {
  'use strict';

  const ELEMENTS={
    Neutral:{label:'Neutral',fg:'#5f5f5f',bg:'#f3f2f0',border:'#aaa7a2'},
    Water:{label:'Water',fg:'#1d6f9f',bg:'#eef8ff',border:'#78b3d4'},
    Earth:{label:'Earth',fg:'#98541f',bg:'#fff5ec',border:'#c99970'},
    Fire:{label:'Fire',fg:'#c63f29',bg:'#fff1ed',border:'#e78975'},
    Wind:{label:'Wind',fg:'#14756f',bg:'#eef9f8',border:'#6eb3ae'},
    Poison:{label:'Poison',fg:'#7443b4',bg:'#f5f0ff',border:'#ad8edf'},
    Holy:{label:'Holy',fg:'#956700',bg:'#fff9e8',border:'#cbaa55'},
    Shadow:{label:'Shadow',fg:'#514b8d',bg:'#f2f1fa',border:'#8e88b6'},
    Dark:{label:'Dark',fg:'#514b8d',bg:'#f2f1fa',border:'#8e88b6'},
    Ghost:{label:'Ghost',fg:'#3f72a3',bg:'#f0f7ff',border:'#89aed0'},
    Undead:{label:'Undead',fg:'#55694c',bg:'#f1f5ef',border:'#99aa90'}
  };
  const FALLBACK_ELEMENT_NAMES=['Neutral','Water','Earth','Fire','Wind','Poison','Holy','Shadow','Ghost','Undead'];

  // Exact copy of the element matrices used by the wiki Elements page.
  // Rows = defending element, columns = attacking element.
  // This local copy is required because index.html keeps its table in a lexical scope
  // that is not guaranteed to be visible from this external runtime script.
  const WIKI_ELEMENT_TABLES={
    1:[
      [100,100,100,100,100,100,100,100,90,100],
      [100,25,100,90,150,150,100,100,100,100],
      [100,100,25,150,90,150,100,100,100,100],
      [100,150,90,25,100,150,100,100,100,90],
      [100,90,150,100,25,150,100,100,100,100],
      [100,150,150,150,150,0,75,75,75,75],
      [100,100,100,100,100,75,0,125,90,125],
      [100,100,100,100,100,75,125,0,90,0],
      [90,100,100,100,100,75,100,100,125,100],
      [100,100,100,125,100,75,125,0,100,0]
    ],
    2:[
      [100,100,100,100,100,100,100,100,70,100],
      [100,0,100,80,175,150,100,100,100,100],
      [100,100,0,175,80,150,100,100,100,100],
      [100,175,80,0,100,150,100,100,100,80],
      [100,80,175,100,0,150,100,100,100,100],
      [100,150,150,150,150,0,75,75,75,50],
      [100,100,100,100,100,75,0,150,80,150],
      [100,100,100,100,100,75,150,0,80,0],
      [70,100,100,100,100,75,100,100,150,125],
      [100,100,100,150,100,50,150,0,125,0]
    ],
    3:[
      [100,100,100,100,100,100,100,100,50,100],
      [100,0,100,70,200,125,100,100,100,100],
      [100,100,0,200,70,125,100,100,100,100],
      [100,200,70,0,100,125,100,100,100,70],
      [100,70,200,100,0,125,100,100,100,100],
      [100,125,125,125,125,0,50,50,50,25],
      [100,100,100,100,100,50,0,175,70,175],
      [100,100,100,100,100,50,175,0,70,0],
      [50,100,100,100,100,50,100,100,175,150],
      [100,100,100,175,100,25,175,0,150,0]
    ],
    4:[
      [100,100,100,100,100,100,100,100,0,100],
      [100,0,100,60,200,125,100,100,100,100],
      [100,100,0,200,60,125,100,100,100,100],
      [100,200,60,0,100,125,100,100,100,60],
      [100,60,200,100,0,125,100,100,100,100],
      [100,125,125,125,125,0,50,50,50,0],
      [100,100,100,100,100,50,0,200,60,200],
      [100,100,100,100,100,50,200,0,60,0],
      [0,100,100,100,100,50,100,100,200,175],
      [100,100,100,200,100,0,200,0,175,0]
    ]
  };

  const STYLE_ID='rz-monster-element-colors-style';
  const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

  function parseElement(value){
    const raw=String(value||'').trim();
    if(!raw)return null;
    const match=raw.match(/^([A-Za-z]+)(?:\s+(?:Lv\.?\s*)?(\d+))?$/i);
    if(!match)return null;
    const requested=/^dark$/i.test(match[1])?'Shadow':match[1];
    const key=Object.keys(ELEMENTS).find(k=>k!=='Dark'&&k.toLowerCase()===requested.toLowerCase())||null;
    if(!key)return null;
    return {key,level:match[2]||''};
  }
  function canonical(value){return parseElement(value)?.key||null;}
  function badge(value){
    const parsed=parseElement(value);
    if(!parsed)return esc(value);
    const e=ELEMENTS[parsed.key]||ELEMENTS.Shadow;
    const suffix=parsed.level?` ${esc(parsed.level)}`:'';
    return `<span class="rz-element-badge rz-element-${parsed.key.toLowerCase()}" data-rz-element="${esc(parsed.key)}"${parsed.level?` data-rz-element-level="${esc(parsed.level)}"`:''}>${esc(e.label)}${suffix}</span>`;
  }
  window.RZ_ELEMENT_BADGE=badge;

  if(!document.getElementById(STYLE_ID)){
    const style=document.createElement('style');
    style.id=STYLE_ID;
    style.textContent=`
      .rz-monster-elements td.rz-element-more{color:#008000!important;font-weight:700}
      .rz-monster-elements td.rz-element-less{color:#d00000!important;font-weight:700}
      .rz-monster-elements td.rz-element-neutral{color:#263846}
      .rz-element-badge{display:inline-block;padding:4px 11px;border:1px solid;border-radius:999px;background:#fff;font-weight:500;line-height:1.15;white-space:nowrap}
      ${Object.entries(ELEMENTS).map(([k,e])=>`.rz-element-${k.toLowerCase()}{color:${e.fg};background:${e.bg};border-color:${e.border}}`).join('\n')}
      .rz-monster-property-badge{text-align:center!important;padding:6px!important}
    `;
    document.head.appendChild(style);
  }

  function matrixNames(){
    if(Array.isArray(window.RZ_ELEMENT_NAMES)&&window.RZ_ELEMENT_NAMES.length===10)return window.RZ_ELEMENT_NAMES;
    return FALLBACK_ELEMENT_NAMES;
  }
  function matrixForLevel(level){
    const globalTable=window.RZ_ELEMENT_TABLES_IRO?.[level];
    if(Array.isArray(globalTable)&&globalTable.length===10)return globalTable;
    return WIKI_ELEMENT_TABLES[level]||null;
  }
  function monsterForSheet(sheet){
    const link=sheet.querySelector('.rz-monster-title a[href^="#/monsters/"]');
    if(!link||!Array.isArray(window.RO_DATA?.monsters))return null;
    const token=decodeURIComponent(String(link.getAttribute('href')||'').replace(/^#\/monsters\//,''));
    return window.RO_DATA.monsters.find(x=>String(x.id)===token||String(x.clientId)===token)||null;
  }
  function monsterElementLevel(monster){
    let level=Number(monster?.elementLevel);
    if(level>=1&&level<=4)return level;
    const parsed=parseElement(monster?.element);
    level=Number(parsed?.level);
    if(level>=1&&level<=4)return level;
    const propertyCode=Number(monster?.propertyCode);
    if(Number.isFinite(propertyCode)){
      level=Math.floor(propertyCode/20);
      if(level>=1&&level<=4)return level;
    }
    return null;
  }

  // Single source of truth for monster elemental modifiers: same values as the Elements page.
  // Matrix orientation: source[defendingElement][attackingElement].
  function applyWikiElementMatrix(root=document){
    const names=matrixNames();
    root.querySelectorAll?.('.rz-monster-sheet').forEach(sheet=>{
      const monster=monsterForSheet(sheet);
      if(!monster)return;
      const defender=canonical(monster.element);
      const level=monsterElementLevel(monster);
      if(!defender||!level)return;
      const matrix=matrixForLevel(level);
      const defenderIndex=names.indexOf(defender);
      if(!matrix||defenderIndex<0||!Array.isArray(matrix[defenderIndex]))return;
      const signature=`${defender}:${level}`;
      const rows=sheet.querySelectorAll('.rz-monster-elements .rz-monster-subtable tbody tr');
      rows.forEach(row=>{
        const th=row.querySelector('th');
        const td=row.querySelector('td');
        if(!th||!td)return;
        const attacker=canonical(th.textContent);
        const attackerIndex=names.indexOf(attacker);
        if(attackerIndex<0)return;
        const value=matrix[defenderIndex][attackerIndex];
        if(!Number.isFinite(Number(value)))return;
        td.textContent=`${Number(value)}%`;
        td.removeAttribute('data-rz-resistance-decorated');
        td.classList.remove('rz-element-more','rz-element-less','rz-element-neutral');
        td.dataset.rzElementMatrix=`${signature}:${attacker}`;
      });
      sheet.dataset.rzElementMatrixApplied=signature;
    });
  }

  function decorateResistanceValues(root=document){
    root.querySelectorAll?.('.rz-monster-elements .rz-monster-subtable td:not([data-rz-resistance-decorated])').forEach(td=>{
      td.dataset.rzResistanceDecorated='1';
      const match=String(td.textContent||'').match(/-?\d+(?:\.\d+)?/);
      if(!match)return;
      const value=Number(match[0]);
      if(!Number.isFinite(value))return;
      if(value>100)td.classList.add('rz-element-more');
      else if(value<100)td.classList.add('rz-element-less');
      else td.classList.add('rz-element-neutral');
    });
  }

  function decorateMonsterProperty(root=document){
    root.querySelectorAll?.('.rz-monster-left-block .rz-monster-subtable tr').forEach(tr=>{
      const th=tr.querySelector('th');
      const td=tr.querySelector('td');
      if(!th||!td||td.dataset.rzPropertyDecorated==='1'||String(th.textContent||'').trim().toLowerCase()!=='property')return;
      const text=String(td.textContent||'').trim();
      if(!parseElement(text))return;
      td.dataset.rzPropertyDecorated='1';
      td.classList.add('rz-monster-property-badge');
      td.innerHTML=badge(text);
    });
  }

  function decorateElementPage(root=document){
    const route=String(location.hash||'').toLowerCase();
    if(!route.includes('element'))return;
    const host=root.querySelector?.('.main-content')||root;
    host.querySelectorAll?.('td,th,a,span,strong,button,label').forEach(node=>{
      if(node.dataset?.rzElementDecorated==='1'||node.querySelector?.('.rz-element-badge')||node.children?.length)return;
      const text=String(node.textContent||'').trim();
      if(!parseElement(text))return;
      node.innerHTML=badge(text);
      if(node.dataset)node.dataset.rzElementDecorated='1';
    });
  }

  function decorate(root=document){
    applyWikiElementMatrix(root);
    decorateResistanceValues(root);
    decorateMonsterProperty(root);
    decorateElementPage(root);
  }
  window.RZ_COLOR_MONSTER_ELEMENTS=decorate;
  window.RZ_APPLY_MONSTER_ELEMENT_MATRIX=applyWikiElementMatrix;
  window.RZ_MONSTER_ELEMENT_TABLES=WIKI_ELEMENT_TABLES;

  // Runtime assertion for the exact case that exposed the bug.
  const p=WIKI_ELEMENT_TABLES[1][FALLBACK_ELEMENT_NAMES.indexOf('Poison')];
  if(JSON.stringify(p)!==JSON.stringify([100,150,150,150,150,0,75,75,75,75])){
    console.error('[RZ] Poison Lv.1 element matrix mismatch',p);
  }

  let scheduled=false;
  const schedule=()=>{
    if(scheduled)return;
    scheduled=true;
    requestAnimationFrame(()=>{scheduled=false;decorate(document);});
  };
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',schedule,{once:true});else schedule();
  window.addEventListener('hashchange',()=>requestAnimationFrame(schedule));
  new MutationObserver(mutations=>{
    if(mutations.some(m=>m.addedNodes&&m.addedNodes.length))schedule();
  }).observe(document.documentElement,{childList:true,subtree:true});
})();
