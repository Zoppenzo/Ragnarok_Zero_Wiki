(() => {
  'use strict';
  const getId=monster=>Number(monster?.spriteId??monster?.clientId??monster?.id);
  const ragnaplaceAnimated=id=>`https://render.ragnaplace.com/c/gateway-iro_job-${id}_action-0_enableShadow-false.png`;
  const ragnaplaceFallback=id=>`https://game.ragnaplace.com/ro/job/${id}/0.png`;
  const ZERO_SPECIAL_IDS=new Set([
    3810,3811,3812,3813,3814,3815,3816,3897,3898,3901,3903,3972,3973,3974,3975,
    20076,20077,20078,20079,20080,
    25321,25322,25323,25324,25325,25326,25327,25328,25329,25330,25331,25332,25333,25334,25336
  ]);
  const zeroAnimated=id=>`https://ragnarokzero.net/images/monsters/${id}.gif`;

  function decorate(root=document){
    root.querySelectorAll?.('img[data-rz-monster-sprite]:not([data-rz-monster-ready])').forEach(img=>{
      const id=Number(img.dataset.rzMonsterSprite);
      if(!Number.isFinite(id))return;
      img.dataset.rzMonsterReady='1';
      const stages=ZERO_SPECIAL_IDS.has(id)
        ? [zeroAnimated(id),ragnaplaceAnimated(id),ragnaplaceFallback(id)]
        : [ragnaplaceAnimated(id),ragnaplaceFallback(id)];
      let index=0;
      img.onerror=()=>{
        index+=1;
        if(index<stages.length){img.src=stages[index];return;}
        img.style.display='none';
        const next=img.nextElementSibling;if(next)next.style.display='inline';
      };
      img.src=stages[0];
    });
  }

  window.RZ_MONSTER_SPRITE_HTML=(monster,loading='lazy')=>{
    const id=getId(monster);
    if(!Number.isFinite(id))return'';
    const name=String(monster?.name||monster?.internalName||`Mob ${id}`).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    return `<img data-rz-monster-sprite="${id}" alt="${name}" loading="${loading}" decoding="async" fetchpriority="low">`;
  };
  window.RZ_MONSTER_SPRITE_HTML.source='Zero Global client identity + animated RagnarokZero sprite';
  window.RZ_DECORATE_MONSTER_SPRITES=decorate;
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>decorate(),{once:true});else queueMicrotask(()=>decorate());
})();
