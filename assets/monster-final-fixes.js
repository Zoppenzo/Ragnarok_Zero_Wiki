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
      /* Compact RMS-like monster sheet: every card uses the same desktop width. */
      .rz-monster-sheet-wrap{width:min(100%,1050px)!important;max-width:1050px!important;margin:8px auto 16px!important;box-sizing:border-box}
      .rz-monster-sheet{width:100%!important;table-layout:fixed!important;font-size:13px!important;line-height:1.12!important}
      .rz-monster-sheet th,.rz-monster-sheet td{padding:2px 4px!important}
      .rz-monster-title{font-size:15px!important;line-height:1.15!important;padding:4px 6px!important}
      .rz-monster-title span{margin-left:5px!important}
      .rz-monster-wide-title{font-size:15px!important;line-height:1.1!important;padding:4px 5px!important}
      .rz-monster-section-title{font-size:14px!important;line-height:1.1!important;margin:-2px -4px 2px!important;padding:3px 4px!important}

      .rz-monster-subtable{table-layout:fixed!important}
      .rz-monster-subtable th,.rz-monster-subtable td{padding:2px 4px!important;line-height:1.12!important}
      .rz-monster-left-block{width:27%!important}
      .rz-monster-sprite-cell{width:22%!important;min-height:150px!important}
      .rz-monster-sprite{min-height:150px!important}
      .rz-monster-sprite img{max-width:145px!important;max-height:145px!important}
      .rz-monster-maps{width:32%!important;max-height:none!important}
      .rz-monster-elements{width:19%!important}

      .rz-monster-map-row{gap:0 5px!important;padding:1px 0!important;line-height:1.08!important}
      .rz-monster-map-row small{font-size:11px!important;line-height:1.05!important}
      .rz-monster-map-more{margin-top:2px!important}
      .rz-monster-map-more summary{padding:2px 0!important;font-size:12px!important}

      .rz-monster-midstats{width:50%!important}
      .rz-monster-mode{width:50%!important;padding:2px 4px!important}
      .rz-monster-mode-grid{gap:1px 10px!important}
      .rz-monster-mode-row{padding:1px 0!important;line-height:1.1!important}

      .rz-monster-wide-body{padding:5px!important}
      .rz-monster-drop-grid{gap:4px 10px!important;grid-template-columns:repeat(auto-fit,minmax(155px,1fr))!important}
      .rz-monster-drop{font-size:13px!important;line-height:1.08!important}
      .rz-monster-drop .rz-item-icon{width:20px!important;height:20px!important;flex-basis:20px!important}
      .rz-monster-skill-grid{gap:3px 10px!important;grid-template-columns:repeat(auto-fit,minmax(185px,1fr))!important}
      .rz-monster-empty-section{padding:4px!important}

      .rz-monster-db-results{justify-items:center!important;gap:14px!important}
      .rz-monster-db-results .rz-monster-sheet-wrap{width:min(100%,1050px)!important;max-width:1050px!important;margin:0 auto!important}

      .rz-monster-sheet-wrap-memorial{position:relative;border:3px solid #8057ad!important;border-radius:4px;padding:2px;background:linear-gradient(135deg,#f7f0ff 0,#a982cf 18%,#eee0ff 38%,#744a9d 58%,#e6d2fa 78%,#8c62b7 100%)!important;box-shadow:0 0 0 1px #5a367d,0 3px 12px rgba(74,42,105,.24)!important}
      .rz-monster-sheet-wrap-memorial>.rz-monster-sheet{border-color:#8057ad!important;box-shadow:inset 0 0 0 1px #d8c0ef!important}
      .rz-monster-sheet-wrap-memorial .rz-monster-title{background:linear-gradient(#eee1fb,#c9ace4)!important;color:#44275f!important;border-color:#8057ad!important}
      .rz-monster-sheet-wrap-memorial .rz-monster-title a{color:#44275f!important}

      .rz-monster-drop-grid{justify-items:start!important}
      .rz-monster-drop{justify-self:start!important;justify-content:flex-start!important;width:max-content!important;max-width:100%;gap:5px!important;white-space:nowrap}
      .rz-monster-drop small{margin-left:0!important;white-space:nowrap}

      @media(max-width:1100px){
        .rz-monster-sheet-wrap{width:100%!important;max-width:none!important}
        .rz-monster-db-results .rz-monster-sheet-wrap{width:100%!important;max-width:none!important}
      }
      @media(max-width:760px){
        .rz-monster-sheet{font-size:12px!important}
        .rz-monster-title,.rz-monster-wide-title{font-size:14px!important}
        .rz-monster-section-title{font-size:13px!important}
      }
    `;
    document.head.appendChild(style);
  }

  window.RZ_DECORATE_MONSTER_FINAL=decorate;
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',decorateDetailOnce,{once:true});
  else decorateDetailOnce();
  window.addEventListener('hashchange',decorateDetailOnce);
})();
