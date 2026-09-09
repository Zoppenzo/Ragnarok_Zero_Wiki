(() => {
  'use strict';
  const rows = window.RO_DATA?.monsters;
  if (!Array.isArray(rows)) return;

  const cleanSkills = skills => (Array.isArray(skills) ? skills : []).filter(skill => {
    const internal = String(skill?.internalName || skill?.name || skill?.skill || '').trim().toUpperCase();
    return internal !== 'NPC_EMOTION' && internal !== 'NPC_EMOTION_ON';
  });

  const base = {
    clientId:null,spriteId:null,internalName:'',name:'',aliases:[],level:null,hp:null,sp:null,
    baseExp:null,jobExp:null,race:'n/a',element:'n/a',elementLevel:null,size:'n/a',
    attackMin:null,attackMax:null,magicAttackMin:null,magicAttackMax:null,def:null,mdef:null,
    hit:null,flee:null,str:null,agi:null,vit:null,int:null,dex:null,luk:null,walkSpeed:null,
    attackDelay:null,delayAfterHit:null,attackRange:null,spellRange:null,sightRange:null,
    elementModifiers:{},aggressive:null,boss:false,mvp:false,modes:[],clientBossType:false,
    clientNavigationType:null,propertyCode:null,image:null,description:{en:'',fr:''},drops:[],maps:[],
    skills:[],notes:{en:'',fr:''},verified:false,clientVerified:true,fieldMeta:{},
    zeroOverlayApplied:false,zeroConsensusApplied:false,rmsWalkSpeedApplied:false
  };

  function upsert(patch){
    const id = Number(patch.id);
    const index = rows.findIndex(m => Number(m?.clientId ?? m?.id) === id);
    if (index >= 0) {
      const current = rows[index];
      rows[index] = {
        ...current,
        ...patch,
        id:String(id),clientId:id,spriteId:id,
        skills:cleanSkills(patch.skills ?? current.skills)
      };
      return;
    }
    rows.push({
      ...base,
      ...patch,
      id:String(id),clientId:id,spriteId:id,
      skills:cleanSkills(patch.skills)
    });
  }

  // Complete special-monster identity audit from the supplied 2026-09-03
  // Ragnarok Zero Global client: NPCIdentity.lub + JobName.lub + actual
  // data\\sprite\\몬스터\\*.spr presence. Every entry below has a real monster sprite.
  const clientIdentities = [
    [3810,'MD_KING_PORING','King Poring (Memorial)','king_poring'],
    [3811,'MD_GOLDRING','Goldring (Memorial)','goldporing'],
    [3812,'MD_AMERING','Amering (Memorial)','poring'],
    [3813,'MD_DROPS','Drops (Memorial)','drops'],
    [3814,'MD_POPORING','Poporing (Memorial)','poporing'],
    [3815,'MD_PORING','Poring (Memorial)','poring'],
    [3816,'MD_MARIN','Marin (Memorial)','marin'],
    [3897,'MD_ORC_SKELETON','Orc Skeleton (Memorial)','orc_skeleton'],
    [3898,'MD_ORC_ZOMBIE','Orc Zombie (Memorial)','orc_zombie'],
    [3901,'MD_ORK_HERO','Fallen Orc Hero (Memorial)','ork_hero'],
    [3903,'MD_ORC_FLOWER',"Shaman's Flower",'blue_flower'],
    [3972,'MD_THIEF_BUG__','Thief Bug Male (Memorial)','thief_bug_male'],
    [3973,'MD_THIEF_BUG','Thief Bug (Memorial)','thief_bug_larva'],
    [3974,'MD_THIEF_BUG_EGG','Thief Bug Egg (Memorial)','thief_bug_egg'],
    [3975,'MD_GOLDEN_BUG','Golden Thief Bug (Memorial)','golden_bug'],
    [20076,'MD_MAYA','Maya (Memorial)','maya'],
    [20077,'MD_DENIRO','Deniro (Memorial)','deniro'],
    [20078,'MD_VITATA','Vitata (Memorial)','vitata'],
    [20079,'MD_ANDRE','Andre (Memorial)','andre'],
    [20080,'MD_PIERE','Piere (Memorial)','piere'],
    [25321,'BOULDERDWARF_MACE','Boulder Dwarf Mace','boulderdwarf_mace'],
    [25322,'BOULDERDWARF_HAMMER','Boulder Dwarf Hammer','boulderdwarf_hammer'],
    [25323,'PORING_GEM','Poring Gem','poring_gem'],
    [25324,'NORDIUM_GOLEM','Nordium Golem','nordium_golem'],
    [25325,'BOULDERDWARF_PICK','Boulder Dwarf Pick','boulderdwarf_pick'],
    [25326,'BOULDERDWARF_CANNON','Boulder Dwarf Cannon','boulderdwarf_cannon'],
    [25327,'BOULDERDWARF_HAMMER_MJ','Boulder Dwarf Siege Trooper','boulderdwarf_hammer_armor'],
    [25328,'BOULDERDWARF_MACE_MJ','Boulder Dwarf Captain','boulderdwarf_mace_armor'],
    [25329,'BOULDERDWARF_LEADER_MJ','Boulder Dwarf Squad Leader','boulderdwarf_leader'],
    [25330,'MQ_BOULDERDWARF_HAMMER','Boulder Dwarf Hammer (Quest Variant)','boulderdwarf_hammer'],
    [25331,'MQ_BOULDERDWARF_PICK','Boulder Dwarf Pick (Quest Variant)','boulderdwarf_pick'],
    [25332,'MQ_BOULDERDWARF_CANNON','Boulder Dwarf Cannon (Quest Variant)','boulderdwarf_cannon'],
    [25333,'MQ_BOULDERDWARF_LEADER','Boulder Dwarf Leader (Quest Variant)','boulderdwarf_leader'],
    [25334,'MQ_APARGREL','Apargrel','devildwarf_hammer_armor'],
    [25336,'BOULDERDWARF_SM','Boulder Dwarf Swordmaster','boulderdwarf_sm']
  ];
  clientIdentities.forEach(([id,internalName,name,clientSpriteKey]) => upsert({
    id,internalName,name,clientSpriteKey,clientIdentityVerified:true,clientSpriteVerified:true
  }));

  // Exact current Global in-game Monster Info screenshots supplied by the wiki owner.
  // Element level is inferred only when the complete weakness signature uniquely matches the Zero element table.
  upsert({
    id:25327,internalName:'BOULDERDWARF_HAMMER_MJ',name:'Boulder Dwarf Siege Trooper',
    level:64,hp:53518,def:198,mdef:15,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:2,
    maps:[{mapId:'nrd_dun02',mapName:'Nordfeld Cave 2F',amount:70}],
    elementModifiers:{Neutral:100,Water:100,Earth:0,Fire:175,Wind:80,Poison:150,Holy:100,Shadow:100,Ghost:100,Undead:100},
    clientScreenshotVerified:true
  });
  upsert({
    id:25328,internalName:'BOULDERDWARF_MACE_MJ',name:'Boulder Dwarf Captain',
    level:64,hp:49984,def:224,mdef:23,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:3,
    maps:[{mapId:'nrd_dun02',mapName:'Nordfeld Cave 2F',amount:70}],
    elementModifiers:{Neutral:100,Water:100,Earth:0,Fire:200,Wind:70,Poison:125,Holy:100,Shadow:100,Ghost:100,Undead:100},
    clientScreenshotVerified:true
  });
  upsert({
    id:25329,internalName:'BOULDERDWARF_LEADER_MJ',name:'Boulder Dwarf Squad Leader',
    level:65,hp:55602,def:179,mdef:30,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:2,
    maps:[{mapId:'nrd_dun02',mapName:'Nordfeld Cave 2F',amount:70}],
    elementModifiers:{Neutral:100,Water:100,Earth:0,Fire:175,Wind:80,Poison:150,Holy:100,Shadow:100,Ghost:100,Undead:100},
    clientScreenshotVerified:true
  });

  // These two boss records are separate IDs in the official client, not aliases
  // of normal Orc Hero #1087 / Golden Thief Bug #1086.
  upsert({
    id:3901,internalName:'MD_ORK_HERO',name:'Fallen Orc Hero (Memorial)',level:70,hp:2110562,
    baseExp:166639,jobExp:118717,def:197,mdef:70,race:'Demi-Human',size:'Large',element:'Earth',elementLevel:2,
    elementModifiers:{Neutral:100,Water:100,Earth:0,Fire:175,Wind:80,Poison:150,Holy:100,Shadow:100,Ghost:100,Undead:100},
    boss:true,mvp:true,modes:['Boss Type'],clientIdentityVerified:true
  });
  upsert({
    id:3975,internalName:'MD_GOLDEN_BUG',name:'Golden Thief Bug (Memorial)',level:60,hp:1200000,
    baseExp:75000,jobExp:63000,def:159,mdef:81,race:'Insect',size:'Large',element:'Fire',elementLevel:2,
    attackMin:771,attackMax:1091,magicAttackMin:576,magicAttackMax:967,hit:337,flee:370,
    elementModifiers:{Neutral:100,Water:175,Earth:80,Fire:0,Wind:100,Poison:150,Holy:100,Shadow:100,Ghost:100,Undead:80},
    drops:[{itemId:701,name:'Ora Ora',rate:2},{itemId:985,name:'Elunium',rate:10},{itemId:984,name:'Oridecon',rate:10},{itemId:25429,name:'Mythril Ore',rate:0.1}],
    boss:true,mvp:true,modes:['Boss Type'],clientIdentityVerified:true
  });

  // Keep the remaining Memorial identities conservative if no server-side value
  // is available from the client. Existing Zero-source values are preserved when present.
  upsert({id:3897,race:'Undead',size:'Medium',element:'Undead'});
  upsert({id:3898,size:'Medium',element:'Undead'});
  upsert({id:3903,race:'Plant',size:'Medium',element:'Earth'});
  upsert({id:3972,name:'Thief Bug Male (Memorial)'});
  upsert({id:3973,name:'Thief Bug (Memorial)'});
  upsert({id:3974,name:'Thief Bug Egg (Memorial)'});

  rows.forEach(m => { m.skills = cleanSkills(m.skills); });
  rows.sort((a,b)=>String(a.name||'').localeCompare(String(b.name||''),'en',{sensitivity:'base'}));
  window.RZ_CLIENT_MONSTERS = rows;
})();
