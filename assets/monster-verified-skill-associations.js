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

  // Explicit Monster AI (0) records from the current Ragnarok Zero Global
  // community database. These are verified-empty skill lists, not missing data.
  // Identity is checked against the current client before the flag is applied.
  const verifiedEmpty={
    '1063':{internalName:'LUNATIC',source:'rozerodb-global',aiCount:0},
    '1078':{internalName:'RED_PLANT',source:'rozerodb-global',aiCount:0},
    '1079':{internalName:'BLUE_PLANT',source:'rozerodb-global',aiCount:0},
    '1080':{internalName:'GREEN_PLANT',source:'rozerodb-global',aiCount:0},
    '1081':{internalName:'YELLOW_PLANT',source:'rozerodb-global',aiCount:0},
    '1082':{internalName:'WHITE_PLANT',source:'rozerodb-global',aiCount:0},
    '1083':{internalName:'SHINING_PLANT',source:'rozerodb-global',aiCount:0},
    '1084':{internalName:'BLACK_MUSHROOM',source:'rozerodb-global',aiCount:0},
    '1085':{internalName:'RED_MUSHROOM',source:'rozerodb-global',aiCount:0},
    '1266':{internalName:'ASTER',source:'rozerodb-global',aiCount:0},
    '1687':{internalName:'GREEN_IGUANA',source:'rozerodb-global',aiCount:0},
    '2398':{internalName:'LITTLE_PORING',source:'rozerodb-global',aiCount:0},
    '2404':{internalName:'DEAD_PLANKTON',source:'rozerodb-global',aiCount:0},
    '2405':{internalName:'WEAK_SKELETON',source:'rozerodb-global',aiCount:0},
    '2406':{internalName:'WEAK_SKEL_SOLDIER',source:'rozerodb-global',aiCount:0},
    '25321':{internalName:'BOULDERDWARF_MACE',source:'rozerodb-global',aiCount:0},
    '25322':{internalName:'BOULDERDWARF_HAMMER',source:'rozerodb-global',aiCount:0},
    '25323':{internalName:'PORING_GEM',source:'rozerodb-global',aiCount:0},
    '25324':{internalName:'NORDIUM_GOLEM',source:'rozerodb-global',aiCount:0},
    '25325':{internalName:'BOULDERDWARF_PICK',source:'rozerodb-global',aiCount:0},
    '25326':{internalName:'BOULDERDWARF_CANNON',source:'rozerodb-global',aiCount:0},
    '25336':{internalName:'BOULDERDWARF_SM',source:'rozerodb-global',aiCount:0}
  };

  window.RZ_MONSTER_VERIFIED_SKILL_ASSOCIATIONS=associations;
  window.RZ_MONSTER_VERIFIED_SKILL_EMPTY=verifiedEmpty;

  const monsters=Array.isArray(window.RO_DATA?.monsters)?window.RO_DATA.monsters:[];
  for(const monster of monsters){
    const id=String(monster?.clientId??monster?.id??'');
    const empty=verifiedEmpty[id];
    if(empty){
      const currentInternal=String(monster?.internalName||'');
      if(!empty.internalName||currentInternal===empty.internalName){
        monster.skillsVerifiedEmpty=true;
        monster.skillsVerificationSource=empty.source;
        monster.skillAiCount=0;
      }
    }

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

  if(typeof document!=='undefined'&&typeof location!=='undefined'&&typeof setTimeout==='function'){
    // The main sheet renderer uses "No Result" for an empty array. Replace that
    // label only when the current Mob-ID has an explicit verified AI count of 0.
    function decorateVerifiedEmptySkills(){
      const match=location.hash.match(/^#\/monsters\/([^?#]+)/i);
      if(!match)return;
      const token=decodeURIComponent(match[1]);
      const monster=monsters.find(x=>String(x?.id)===token||String(x?.clientId)===token);
      if(!monster?.skillsVerifiedEmpty)return;
      const title=[...document.querySelectorAll('.rz-monster-wide-title')].find(x=>String(x.textContent||'').trim()==='Monster Skills');
      const body=title?.closest('tr')?.nextElementSibling?.querySelector('.rz-monster-wide-body');
      if(!body)return;
      body.innerHTML='<div class="rz-monster-empty-section"><span class="rz-monster-no-skills">No Skills</span></div>';
    }
    const scheduleDecoration=()=>setTimeout(decorateVerifiedEmptySkills,0);
    if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',scheduleDecoration,{once:true});
    else scheduleDecoration();
    window.addEventListener('hashchange',scheduleDecoration);
  }
})();
