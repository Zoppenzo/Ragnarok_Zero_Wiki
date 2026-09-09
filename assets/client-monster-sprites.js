(() => {
  'use strict';
  const getId=monster=>Number(monster?.spriteId??monster?.clientId??monster?.id);
  const animated=id=>`https://render.ragnaplace.com/c/gateway-iro_job-${id}_action-0_enableShadow-false.png`;
  const fallback=id=>`https://game.ragnaplace.com/ro/job/${id}/0.png`;

  function load(img){
    if(!img||img.dataset.rzMonsterReady==='1')return;
    const id=Number(img.dataset.rzMonsterSprite);
    if(!Number.isFinite(id))return;
    img.dataset.rzMonsterReady='1';
    img.onerror=()=>{
      const fb=fallback(id);
      if(img.src!==fb){img.src=fb;return;}
      img.style.display='none';
      const next=img.nextElementSibling;if(next)next.style.display='inline';
    };
    img.src=animated(id);
  }

  const io='IntersectionObserver' in window?new IntersectionObserver(entries=>{
    for(const entry of entries){
      if(!entry.isIntersecting)continue;
      io.unobserve(entry.target);
      load(entry.target);
    }
  },{rootMargin:'350px 0px'}):null;

  function decorate(root=document){
    root.querySelectorAll?.('img[data-rz-monster-sprite]:not([data-rz-monster-watch])').forEach(img=>{
      img.dataset.rzMonsterWatch='1';
      if(io)io.observe(img);else load(img);
    });
  }

  window.RZ_MONSTER_SPRITE_HTML=(monster,loading='lazy')=>{
    const id=getId(monster);
    if(!Number.isFinite(id))return'';
    const name=String(monster?.name||monster?.internalName||`Mob ${id}`).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    return `<img data-rz-monster-sprite="${id}" alt="${name}" loading="${loading}" decoding="async">`;
  };
  window.RZ_DECORATE_MONSTER_SPRITES=decorate;
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>decorate(),{once:true});else queueMicrotask(()=>decorate());
})();
