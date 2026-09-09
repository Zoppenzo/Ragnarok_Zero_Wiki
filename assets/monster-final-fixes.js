(() => {
  'use strict';
  const STYLE_ID='rz-monster-final-fixes-style';

  function monsterForWrap(wrap){
    const title=wrap?.querySelector?.('.rz-monster-title');
    const id=title?.textContent?.match(/Mob-ID#\s*(\d+)/i)?.[1];
    return id ? window.RO_DATA?.monsters?.find?.(m=>String(m.clientId||m.id)===String(id)) : null;
  }

  function fixUnknowns(wrap){
    wrap.querySelectorAll?.('.rz-monster-na').forEach(node=>{ node.textContent='???'; });
    wrap.querySelectorAll?.('.rz-monster-drop small').forEach(node=>{
      for(const child of node.childNodes){
        if(child.nodeType!==Node.TEXT_NODE) continue;
        const txt=String(child.nodeValue||'');
        if(/^\s*n\/a\b/i.test(txt)) child.nodeValue=txt.replace(/^\s*n\/a\b/i,'???');
        break;
      }
    });
  }

  function fixSkillRates(wrap){
    wrap.querySelectorAll?.('.rz-monster-skill-grid small').forEach(node=>{
      if(/%\s*$/.test(String(node.textContent||''))) node.remove();
    });
  }

  function fixMemorialFrame(wrap){
    const monster=monsterForWrap(wrap);
    if(!monster || !/^MD_/i.test(String(monster.internalName||''))) return;
    wrap.classList.remove('rz-monster-sheet-wrap-mvp');
    wrap.classList.add('rz-monster-sheet-wrap-memorial');
    wrap.dataset.rzMemorial='1';
  }

  function wrapsIn(root){
    if(!root) return [];
    if(root.matches?.('.rz-monster-sheet-wrap')) return [root];
    return [...(root.querySelectorAll?.('.rz-monster-sheet-wrap')||[])];
  }

  function decorate(root=document){
    const wraps=wrapsIn(root);
    if(!wraps.length) return;
    for(const wrap of wraps){
      fixUnknowns(wrap);
      fixSkillRates(wrap);
      fixMemorialFrame(wrap);
    }
    window.RZ_DECORATE_ITEM_ICONS?.(root);
  }

  function decorateDetailOnce(){
    if(!/^#\/monsters\//i.test(location.hash)) return;
    requestAnimationFrame(()=>{
      const main=document.querySelector('.main-content')||document;
      const wrap=main.querySelector('.rz-monster-sheet-wrap');
      if(wrap) decorate(wrap);
    });
  }

  if(!document.getElementById(STYLE_ID)){
    const style=document.createElement('style');
    style.id=STYLE_ID;
    style.textContent=`
      .rz-monster-sheet-wrap-memorial{position:relative;border:3px solid #8057ad!important;border-radius:4px;padding:2px;background:linear-gradient(135deg,#f7f0ff 0,#a982cf 18%,#eee0ff 38%,#744a9d 58%,#e6d2fa 78%,#8c62b7 100%)!important;box-shadow:0 0 0 1px #5a367d,0 3px 12px rgba(74,42,105,.24)!important}
      .rz-monster-sheet-wrap-memorial>.rz-monster-sheet{border-color:#8057ad!important;box-shadow:inset 0 0 0 1px #d8c0ef!important}
      .rz-monster-sheet-wrap-memorial .rz-monster-title{background:linear-gradient(#eee1fb,#c9ace4)!important;color:#44275f!important;border-color:#8057ad!important}
      .rz-monster-sheet-wrap-memorial .rz-monster-title a{color:#44275f!important}
      .rz-monster-drop-grid{justify-items:start!important}
      .rz-monster-drop{justify-self:start!important;justify-content:flex-start!important;width:max-content!important;max-width:100%;gap:5px!important;white-space:nowrap}
      .rz-monster-drop small{margin-left:0!important;white-space:nowrap}
    `;
    document.head.appendChild(style);
  }

  window.RZ_DECORATE_MONSTER_FINAL=decorate;
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',decorateDetailOnce,{once:true});
  else decorateDetailOnce();
  window.addEventListener('hashchange',decorateDetailOnce);
})();
