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
  const STYLE_ID='rz-monster-element-colors-style';
  const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

  function canonical(value){
    const raw=String(value||'').trim();
    if(/^dark$/i.test(raw))return 'Dark';
    return Object.keys(ELEMENTS).find(k=>k.toLowerCase()===raw.toLowerCase())||null;
  }
  function badge(value){
    const key=canonical(value);
    if(!key)return esc(value);
    const e=ELEMENTS[key];
    return `<span class="rz-element-badge rz-element-${key.toLowerCase()}" data-rz-element="${esc(key)}">${esc(e.label)}</span>`;
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

  function decorateResistanceValues(root=document){
    root.querySelectorAll?.('.rz-monster-elements .rz-monster-subtable td').forEach(td=>{
      td.classList.remove('rz-element-more','rz-element-less','rz-element-neutral');
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
      if(!th||!td||String(th.textContent||'').trim().toLowerCase()!=='property')return;
      const text=String(td.textContent||'').trim();
      const key=Object.keys(ELEMENTS).find(name=>new RegExp(`^${name}\\b`,'i').test(text));
      if(!key)return;
      td.classList.add('rz-monster-property-badge');
      td.innerHTML=badge(key);
    });
  }

  function decorateElementPage(root=document){
    const route=String(location.hash||'').toLowerCase();
    if(!route.includes('element'))return;
    const host=root.querySelector?.('.main-content')||root;
    host.querySelectorAll?.('td,th,a,span,strong,button,label').forEach(node=>{
      if(node.dataset?.rzElementDecorated==='1'||node.querySelector?.('.rz-element-badge'))return;
      if(node.children?.length)return;
      const key=canonical(String(node.textContent||'').trim());
      if(!key)return;
      node.innerHTML=badge(key);
      if(node.dataset)node.dataset.rzElementDecorated='1';
    });
  }

  function decorate(root=document){
    decorateResistanceValues(root);
    decorateMonsterProperty(root);
    decorateElementPage(root);
  }

  window.RZ_COLOR_MONSTER_ELEMENTS=decorate;
  const run=()=>queueMicrotask(()=>decorate(document));
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run,{once:true});
  else run();
  window.addEventListener('hashchange',run);
  new MutationObserver(run).observe(document.documentElement,{childList:true,subtree:true});
})();
