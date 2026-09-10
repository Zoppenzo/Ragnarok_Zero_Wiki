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

  // TWRoZ fallback maps. Current-client Navi always wins. These records are only
  // allowed to fill an otherwise empty map list for an identity with no exact-name
  // Navi entry; estimated population/respawn values are deliberately not imported.
  const consensus=window.RZ_MONSTER_ZERO_CONSENSUS&&typeof window.RZ_MONSTER_ZERO_CONSENSUS==='object'
    ?window.RZ_MONSTER_ZERO_CONSENSUS:{};
  const mapLabels=Array.isArray(window.RZ_CLIENT_MONSTER_MAP_LABELS)?window.RZ_CLIENT_MONSTER_MAP_LABELS:[];
  const mapIndex=window.RZ_CLIENT_MONSTER_MAP_INDEX&&typeof window.RZ_CLIENT_MONSTER_MAP_INDEX==='object'
    ?window.RZ_CLIENT_MONSTER_MAP_INDEX:{};
  const wikiMaps=Array.isArray(window.RO_DATA?.maps)?window.RO_DATA.maps:[];
  const labelMap=mapId=>{
    const direct=wikiMaps.find(m=>String(m?.internalName||'')===mapId||String(m?.id||'')===mapId);
    if(direct?.name) return direct.name;
    const idx=mapIndex[mapId];
    return Number.isInteger(idx)&&mapLabels[idx]?mapLabels[idx]:mapId;
  };

  let sourceMonsters=0;
  let appliedMonsters=0;
  let mapsApplied=0;
  let naviProtected=0;
  let skippedExistingMaps=0;
  for(const monster of rows){
    const id=Number(monster?.clientId??monster?.id);
    if(!Number.isFinite(id)) continue;
    const spawns=Array.isArray(consensus[String(id)]?.spawns)?consensus[String(id)].spawns:[];
    if(!spawns.length) continue;
    sourceMonsters+=1;
    if(monster.clientNavigationCurrent===true){
      naviProtected+=1;
      continue;
    }
    if(Array.isArray(monster.maps)&&monster.maps.length){
      skippedExistingMaps+=1;
      continue;
    }
    const seen=new Set();
    monster.maps=spawns.map(spawn=>{
      const mapId=String(spawn?.mapId||'').trim();
      if(!mapId||seen.has(mapId)) return null;
      seen.add(mapId);
      return {
        mapId,
        mapName:labelMap(mapId),
        amount:null,
        respawn:null,
        verified:true,
        zeroVerified:true,
        source:'zero-spawn-twroz'
      };
    }).filter(Boolean);
    if(monster.maps.length){
      appliedMonsters+=1;
      mapsApplied+=monster.maps.length;
      monster.zeroSpawnFallbackApplied=true;
    }
  }

  const naviFallbackViolations=rows.filter(monster=>
    monster?.clientNavigationCurrent===true&&Array.isArray(monster.maps)&&monster.maps.some(map=>map?.source==='zero-spawn-twroz')
  ).map(monster=>Number(monster?.clientId??monster?.id)).filter(Number.isFinite);
  if(naviFallbackViolations.length){
    throw new Error(`TWRoZ fallback attempted to override current Navi: ${naviFallbackViolations.join(',')}`);
  }
  window.RZ_MONSTER_ZERO_SPAWN_AUDIT={sourceMonsters,appliedMonsters,mapsApplied,naviProtected,skippedExistingMaps,naviFallbackViolations};

  // The audit runs this file in Node without a DOM. Data mutations above still apply.
  if(typeof document==='undefined') return;

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
