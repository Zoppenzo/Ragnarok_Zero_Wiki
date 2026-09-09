(() => {
  'use strict';

  function emblem(){
    return `<span class="rz-monster-mvp-emblem" aria-label="MVP" title="MVP"><span>MVP</span></span>`;
  }
  const isMemorial=monster=>Boolean(monster?.memorial)||String(monster?.internalName||'').startsWith('MD_')||/\(Memorial\)/i.test(String(monster?.name||''));

  function decorate(root=document){
    root.querySelectorAll?.('.rz-monster-sheet-wrap:not([data-rz-mvp-checked])').forEach(wrap=>{
      wrap.dataset.rzMvpChecked='1';
      const title=wrap.querySelector('.rz-monster-title');
      const match=title?.textContent?.match(/Mob-ID#\s*(\d+)/i);
      if(!match)return;
      const monster=window.RO_DATA?.monsters?.find?.(m=>String(m.clientId||m.id)===match[1]);
      if(isMemorial(monster)){
        wrap.classList.add('rz-monster-sheet-wrap-memorial');
        wrap.querySelector('.rz-monster-mvp-emblem')?.remove();
        return;
      }
      if(!monster?.mvp)return;
      wrap.classList.add('rz-monster-sheet-wrap-mvp');
      if(!wrap.querySelector('.rz-monster-mvp-emblem'))wrap.insertAdjacentHTML('beforeend',emblem());
    });
  }

  const oldSheet=window.RZ_MONSTER_SHEET_HTML;
  if(typeof oldSheet==='function'){
    window.RZ_MONSTER_SHEET_HTML=monster=>{
      const html=oldSheet(monster);
      if(isMemorial(monster)){
        return html.replace('class="rz-monster-sheet-wrap"','class="rz-monster-sheet-wrap rz-monster-sheet-wrap-memorial" data-rz-mvp-checked="1"');
      }
      if(!monster?.mvp)return html;
      return html
        .replace('class="rz-monster-sheet-wrap"','class="rz-monster-sheet-wrap rz-monster-sheet-wrap-mvp" data-rz-mvp-checked="1"')
        .replace('</div>',`${emblem()}</div>`);
    };
  }

  const oldDetail=window.RZ_RENDER_RMS_MONSTER_DETAIL;
  if(typeof oldDetail==='function'){
    window.RZ_RENDER_RMS_MONSTER_DETAIL=(...args)=>{
      const result=oldDetail(...args);
      queueMicrotask(()=>decorate(document));
      return result;
    };
  }

  const style=document.createElement('style');
  style.id='rz-monster-mvp-style';
  style.textContent=`
    .rz-monster-sheet-wrap-mvp{position:relative;border:3px solid #d4a72c;border-radius:4px;padding:2px;background:linear-gradient(135deg,#fff8d8 0,#d4a72c 18%,#fff3b0 38%,#b88718 58%,#ffeaa0 78%,#d4a72c 100%);box-shadow:0 0 0 1px #8b6512,0 3px 12px rgba(96,67,5,.24)}
    .rz-monster-sheet-wrap-mvp>.rz-monster-sheet{border-color:#b88718;box-shadow:inset 0 0 0 1px #f8dc7a}
    .rz-monster-sheet-wrap-mvp .rz-monster-title{background:linear-gradient(#fff3bd,#e7c45a);color:#5b4300;border-color:#b88718}
    .rz-monster-sheet-wrap-mvp .rz-monster-title a{color:#5b4300}
    .rz-monster-sheet-wrap-memorial{position:relative;border:3px solid #7b4fc6;border-radius:4px;padding:2px;background:linear-gradient(135deg,#f4edff 0,#9a6cda 20%,#e3d2ff 42%,#6740a8 63%,#d8c1ff 82%,#7b4fc6 100%);box-shadow:0 0 0 1px #4d2d83,0 3px 12px rgba(73,42,122,.25)}
    .rz-monster-sheet-wrap-memorial>.rz-monster-sheet{border-color:#7650ad;box-shadow:inset 0 0 0 1px #d9c4ff}
    .rz-monster-sheet-wrap-memorial .rz-monster-title{background:linear-gradient(#eadfff,#c9afea);color:#40266c;border-color:#7650ad}
    .rz-monster-sheet-wrap-memorial .rz-monster-title a{color:#40266c}
    .rz-monster-mvp-emblem{position:absolute;right:12px;bottom:12px;width:72px;height:72px;display:grid;place-items:center;z-index:3;filter:drop-shadow(0 2px 2px rgba(0,0,0,.28));pointer-events:none}
    .rz-monster-mvp-emblem::before,.rz-monster-mvp-emblem::after{content:'';position:absolute;inset:5px;background:linear-gradient(135deg,#fff6a5 0%,#ffc928 32%,#ff7a18 67%,#e53522 100%);clip-path:polygon(50% 0,61% 23%,82% 8%,77% 34%,100% 34%,81% 51%,98% 67%,73% 68%,79% 94%,58% 78%,50% 100%,42% 78%,21% 94%,27% 68%,2% 67%,19% 51%,0 34%,23% 34%,18% 8%,39% 23%);border-radius:8px}
    .rz-monster-mvp-emblem::after{inset:12px;background:#fff2a3;opacity:.75;transform:rotate(11deg)}
    .rz-monster-mvp-emblem>span{position:relative;z-index:2;font-family:Impact,Arial Black,sans-serif;font-size:23px;font-style:italic;letter-spacing:-1px;color:#e84722;-webkit-text-stroke:1px #fff9ce;text-shadow:1px 1px 0 #8f2e12,-1px -1px 0 #8f2e12}
    @media(max-width:760px){.rz-monster-mvp-emblem{width:58px;height:58px;right:8px;bottom:8px}.rz-monster-mvp-emblem>span{font-size:18px}}
  `;
  if(!document.getElementById(style.id))document.head.appendChild(style);

  window.RZ_DECORATE_MONSTER_MVP=decorate;
  queueMicrotask(()=>decorate(document));
})();
