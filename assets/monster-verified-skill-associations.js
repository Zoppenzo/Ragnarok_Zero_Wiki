(() => {
  'use strict';

  // Monster -> skill links verified from Zero Global-specific source pages.
  // Keep level/rate/conditions unset unless the Zero source explicitly proves them.
  const associations={
    '1250':[
      {
        internalName:'WZ_FIREPILLAR',
        name:'Fire Pillar',
        source:'ragnaplace-rozg',
        associationVerified:true
      }
    ]
  };

  window.RZ_MONSTER_VERIFIED_SKILL_ASSOCIATIONS=associations;

  const monsters=Array.isArray(window.RO_DATA?.monsters)?window.RO_DATA.monsters:[];
  for(const monster of monsters){
    const id=String(monster?.clientId??monster?.id??'');
    const extra=associations[id];
    if(!Array.isArray(extra)||!extra.length)continue;

    const skills=Array.isArray(monster.skills)?monster.skills:[];
    const seen=new Set(skills.map(skill=>String(skill?.internalName||skill?.name||skill?.skill||'').trim().toUpperCase()).filter(Boolean));
    for(const skill of extra){
      const key=String(skill?.internalName||skill?.name||'').trim().toUpperCase();
      if(!key||seen.has(key))continue;
      skills.push({...skill});
      seen.add(key);
    }
    monster.skills=skills;
  }
})();
