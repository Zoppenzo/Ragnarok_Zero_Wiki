(() => {
  'use strict';

  const STYLE_ID='rz-monster-element-colors-style';
  if(!document.getElementById(STYLE_ID)){
    const style=document.createElement('style');
    style.id=STYLE_ID;
    style.textContent=`
      .rz-monster-elements td.rz-element-more{color:#008000!important;font-weight:700}
      .rz-monster-elements td.rz-element-less{color:#d00000!important;font-weight:700}
      .rz-monster-elements td.rz-element-neutral{color:#263846}
    `;
    document.head.appendChild(style);
  }

  function decorate(root=document){
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

  window.RZ_COLOR_MONSTER_ELEMENTS=decorate;
  const run=()=>queueMicrotask(()=>decorate(document));
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run,{once:true});
  else run();
  window.addEventListener('hashchange',run);
  new MutationObserver(run).observe(document.documentElement,{childList:true,subtree:true});
})();
