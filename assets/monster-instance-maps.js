(() => {
  'use strict';
  const rows=window.RO_DATA?.monsters;
  if(!Array.isArray(rows)) return;

  const byId=id=>rows.find(m=>Number(m?.clientId??m?.id)===Number(id));
  const setMap=(id,mapId,mapName)=>{
    const monster=byId(id);
    if(!monster) return;
    if(!Array.isArray(monster.maps)||!monster.maps.length){
      monster.maps=[{mapId,mapName,amount:null,respawn:null,instance:true,externalVerified:true}];
    }
  };
  const setLabel=(id,label,mapId=null)=>{
    const monster=byId(id);
    if(!monster) return;
    monster.instanceLabel=label;
    if(mapId) monster.instanceMapHint=mapId;
  };

  // Confirmed technical instance map: Poring Village / Poring Town.
  [3810,3811,3812,3813,3814,3815,3816].forEach(id=>setMap(id,'1@begi','Poring Village (Instance)'));

  // Zero memorial map table identifies the Prontera Culvert instance as 1@sewb2.
  [3972,3973,3974,3975].forEach(id=>setMap(id,'1@sewb2','Prontera Culvert (Instance)'));

  // Orc's Memory is confirmed, but the exact 1@orcs / 2@orcs split per Global mob
  // is not sufficiently verified. Show the instance name instead of inventing a floor.
  [3897,3898,3901,3903].forEach(id=>setLabel(id,"Orc's Memory · Instance"));

  // Ant Hell's Zero technical map is known, but this Memorial is not live on Global yet.
  // Keep it as a hint only so these future client records are not exposed as live spawns.
  [20076,20077,20078,20079,20080].forEach(id=>setLabel(id,'Ant Hell · Memorial','1@ant01'));

  function monsterForWrap(wrap){
    const title=wrap?.querySelector?.('.rz-monster-title');
    const id=title?.textContent?.match(/Mob-ID#\s*(\d+)/i)?.[1];
    return id?byId(id):null;
  }
  function decorate(root=document){
    const wraps=root?.matches?.('.rz-monster-sheet-wrap')?[root]:[...(root?.querySelectorAll?.('.rz-monster-sheet-wrap')||[])];
    for(const wrap of wraps){
      const monster=monsterForWrap(wrap);
      if(!monster) continue;
      const maps=Array.isArray(monster.maps)?monster.maps:[];
      if(maps.length) continue;
      const host=wrap.querySelector('.rz-monster-maps');
      const empty=host?.querySelector('.rz-monster-no-result');
      if(!empty) continue;
      const isMemorial=monster.memorial||/^MD_/i.test(String(monster.internalName||''));
      const label=monster.instanceLabel||(isMemorial?'Memorial':null);
      if(!label) continue;
      const span=document.createElement('span');
      span.className='rz-monster-instance-label';
      span.textContent=label;
      if(monster.instanceMapHint) span.title=`Instance map: ${monster.instanceMapHint}`;
      empty.replaceWith(span);
    }
  }

  const previous=window.RZ_DECORATE_MONSTER_FINAL;
  window.RZ_DECORATE_MONSTER_FINAL=root=>{ previous?.(root); decorate(root); };

  if(!document.getElementById('rz-monster-instance-map-style')){
    const style=document.createElement('style');
    style.id='rz-monster-instance-map-style';
    style.textContent=`
      .rz-monster-instance-label{display:inline-block;margin:5px 3px;padding:3px 8px;border:1px solid #8057ad;border-radius:999px;background:#eee1fb;color:#68418d;font-weight:700;line-height:1.15}
    `;
    document.head.appendChild(style);
  }

  const decorateDetail=()=>requestAnimationFrame(()=>decorate(document.querySelector('.main-content')||document));
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',decorateDetail,{once:true});
  else decorateDetail();
  window.addEventListener('hashchange',decorateDetail);
})();
