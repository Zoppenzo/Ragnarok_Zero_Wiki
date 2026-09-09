(() => {
  'use strict';
  const getId=monster=>Number(monster?.spriteId??monster?.clientId??monster?.id);
  const embedded=key=>key&&window.RZ_CLIENT_MONSTER_SPRITE_DATA?.[String(key).toLowerCase()]||null;
  const animated=id=>`https://render.ragnaplace.com/c/gateway-iro_job-${id}_action-0_enableShadow-false.png`;
  const fallback=id=>`https://game.ragnaplace.com/ro/job/${id}/0.png`;

  function decorate(root=document){
    root.querySelectorAll?.('img[data-rz-monster-sprite]:not([data-rz-monster-ready])').forEach(img=>{
      const id=Number(img.dataset.rzMonsterSprite);
      if(!Number.isFinite(id))return;
      img.dataset.rzMonsterReady='1';
      const local=embedded(img.dataset.rzClientSpriteKey);
      let stage=local?'local':'animated';
      img.onerror=()=>{
        if(stage==='local'){
          stage='animated'; img.src=animated(id); return;
        }
        if(stage==='animated'){
          stage='fallback'; img.src=fallback(id); return;
        }
        img.style.display='none';
        const next=img.nextElementSibling;if(next)next.style.display='inline';
      };
      img.src=local||animated(id);
    });
  }

  window.RZ_MONSTER_SPRITE_HTML=(monster,loading='lazy')=>{
    const id=getId(monster);
    if(!Number.isFinite(id))return'';
    const name=String(monster?.name||monster?.internalName||`Mob ${id}`).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    const key=String(monster?.clientSpriteKey||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    return `<img data-rz-monster-sprite="${id}"${key?` data-rz-client-sprite-key="${key}"`:''} alt="${name}" loading="${loading}" decoding="async" fetchpriority="low">`;
  };
  window.RZ_DECORATE_MONSTER_SPRITES=decorate;
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>decorate(),{once:true});else queueMicrotask(()=>decorate());
})();
