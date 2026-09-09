(() => {
  'use strict';
  const getId=monster=>Number(monster?.spriteId??monster?.clientId??monster?.id);
  const embedded=key=>key&&window.RZ_CLIENT_MONSTER_SPRITE_DATA?.[String(key).toLowerCase()]||null;
  const animated=id=>`https://render.ragnaplace.com/c/gateway-iro_job-${id}_action-0_enableShadow-false.png`;
  const fallback=id=>`https://game.ragnaplace.com/ro/job/${id}/0.png`;
  const correctedCache=new Map();

  // The first GRF sprite export interpreted the client palette as BGRA.
  // This client stores these SPR palette entries as RGBA, so red and blue
  // were reversed (orange/brown skin became blue). Correct every embedded
  // GRF sprite once in-browser while preserving the original alpha channel.
  function correctedEmbedded(key,done){
    const raw=embedded(key);
    if(!raw){done(null);return;}
    if(correctedCache.has(raw)){done(correctedCache.get(raw));return;}
    const source=new Image();
    source.onload=()=>{
      try{
        const canvas=document.createElement('canvas');
        canvas.width=source.naturalWidth||source.width;
        canvas.height=source.naturalHeight||source.height;
        const ctx=canvas.getContext('2d',{willReadFrequently:true});
        ctx.drawImage(source,0,0);
        const frame=ctx.getImageData(0,0,canvas.width,canvas.height);
        const px=frame.data;
        for(let i=0;i<px.length;i+=4){
          const r=px[i]; px[i]=px[i+2]; px[i+2]=r;
        }
        ctx.putImageData(frame,0,0);
        const fixed=canvas.toDataURL('image/png');
        correctedCache.set(raw,fixed);
        done(fixed);
      }catch(_){done(raw);}
    };
    source.onerror=()=>done(null);
    source.src=raw;
  }

  function decorate(root=document){
    root.querySelectorAll?.('img[data-rz-monster-sprite]:not([data-rz-monster-ready])').forEach(img=>{
      const id=Number(img.dataset.rzMonsterSprite);
      if(!Number.isFinite(id))return;
      img.dataset.rzMonsterReady='1';
      const rawLocal=embedded(img.dataset.rzClientSpriteKey);
      let stage=rawLocal?'local':'animated';
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
      if(rawLocal){
        correctedEmbedded(img.dataset.rzClientSpriteKey,fixed=>{
          if(fixed)img.src=fixed;
          else {stage='animated';img.src=animated(id);}
        });
      }else img.src=animated(id);
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
