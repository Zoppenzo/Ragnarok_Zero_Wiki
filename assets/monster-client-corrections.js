(() => {
  'use strict';
  const rows = window.RO_DATA?.monsters;
  if (!Array.isArray(rows)) return;

  const cleanSkills = skills => {
    const seen = new Set();
    return (Array.isArray(skills) ? skills : []).filter(skill => {
      const internal = String(skill?.internalName || skill?.name || skill?.skill || '').trim().toUpperCase();
      if (internal === 'NPC_EMOTION' || internal === 'NPC_EMOTION_ON') return false;
      const key = `${internal}|${skill?.level ?? ''}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    }).map(skill => ({ ...skill, rate:null }));
  };

  const base = {
    clientId:null,spriteId:null,internalName:'',name:'',aliases:[],level:null,hp:null,sp:null,
    baseExp:null,jobExp:null,race:null,element:null,elementLevel:null,size:null,
    attackMin:null,attackMax:null,magicAttackMin:null,magicAttackMax:null,def:null,mdef:null,
    hit:null,flee:null,str:null,agi:null,vit:null,int:null,dex:null,luk:null,walkSpeed:null,
    attackDelay:null,delayAfterHit:null,attackRange:null,spellRange:null,sightRange:null,
    elementModifiers:{},aggressive:null,boss:false,mvp:false,modes:[],clientBossType:false,
    clientNavigationType:null,propertyCode:null,image:null,description:{en:'',fr:''},drops:[],maps:[],
    skills:[],notes:{en:'',fr:''},verified:false,clientVerified:true,fieldMeta:{},
    zeroOverlayApplied:false,zeroConsensusApplied:false,rmsWalkSpeedApplied:false,
    memorial:false,zeroDbSprite:false
  };

  function upsert(patch){
    const id = Number(patch.id);
    const index = rows.findIndex(m => Number(m?.clientId ?? m?.id) === id);
    const normalized = {
      ...patch,
      id:String(id),clientId:id,spriteId:id,
      skills:cleanSkills(patch.skills)
    };
    if (index >= 0) {
      const current = rows[index];
      rows[index] = {
        ...current,
        ...patch,
        id:String(id),clientId:id,spriteId:id,
        skills:cleanSkills(patch.skills ?? current.skills)
      };
      return rows[index];
    }
    rows.push({ ...base, ...normalized });
    return rows[rows.length - 1];
  }

  // Identity/sprite mapping verified against the supplied Ragnarok Zero Global client
  // (NPCIdentity.lub + JobName.lub + matching monster SPR resources).
  const clientIdentities = [
    [3810,'MD_KING_PORING','King Poring (Memorial)','king_poring',true],
    [3811,'MD_GOLDRING','Goldring (Memorial)','goldporing',true],
    [3812,'MD_AMERING','Amering (Memorial)','poring',true],
    [3813,'MD_DROPS','Drops (Memorial)','drops',true],
    [3814,'MD_POPORING','Poporing (Memorial)','poporing',true],
    [3815,'MD_PORING','Poring (Memorial)','poring',true],
    [3816,'MD_MARIN','Marin (Memorial)','marin',true],
    [3897,'MD_ORC_SKELETON','Orc Skeleton (Memorial)','orc_skeleton',true],
    [3898,'MD_ORC_ZOMBIE','Orc Zombie (Memorial)','orc_zombie',true],
    [3901,'MD_ORK_HERO','Fallen Orc Hero (Memorial)','ork_hero',true],
    [3903,'MD_ORC_FLOWER',"Shaman's Flower",'blue_flower',true],
    [3972,'MD_THIEF_BUG__','Thief Bug Male (Memorial)','thief_bug_male',true],
    [3973,'MD_THIEF_BUG','Thief Bug (Memorial)','thief_bug_larva',true],
    [3974,'MD_THIEF_BUG_EGG','Thief Bug Egg (Memorial)','thief_bug_egg',true],
    [3975,'MD_GOLDEN_BUG','Golden Thief Bug (Memorial)','golden_bug',true],
    [20076,'MD_MAYA','Maya (Memorial)','maya',true],
    [20077,'MD_DENIRO','Deniro (Memorial)','deniro',true],
    [20078,'MD_VITATA','Vitata (Memorial)','vitata',true],
    [20079,'MD_ANDRE','Andre (Memorial)','andre',true],
    [20080,'MD_PIERE','Piere (Memorial)','piere',true],
    [25321,'BOULDERDWARF_MACE','Boulder Dwarf Mace','boulderdwarf_mace',false],
    [25322,'BOULDERDWARF_HAMMER','Boulder Dwarf Hammer','boulderdwarf_hammer',false],
    [25323,'PORING_GEM','Gem Poring','poring_gem',false],
    [25324,'NORDIUM_GOLEM','Nordium Golem','nordium_golem',false],
    [25325,'BOULDERDWARF_PICK','Pickaxe Boulder Dwarf','boulderdwarf_pick',false],
    [25326,'BOULDERDWARF_CANNON','Boulder Dwarf Cannon','boulderdwarf_cannon',false],
    [25327,'BOULDERDWARF_HAMMER_MJ','Boulder Dwarf Siege Trooper','boulderdwarf_hammer_armor',false],
    [25328,'BOULDERDWARF_MACE_MJ','Boulder Dwarf Squad Leader','boulderdwarf_mace_armor',false],
    [25329,'BOULDERDWARF_LEADER_MJ','Boulder Dwarf Captain','boulderdwarf_leader',false],
    [25330,'MQ_BOULDERDWARF_HAMMER','Boulder Dwarf Hammer (Quest Variant)','boulderdwarf_hammer',false],
    [25331,'MQ_BOULDERDWARF_PICK','Boulder Dwarf Pick (Quest Variant)','boulderdwarf_pick',false],
    [25332,'MQ_BOULDERDWARF_CANNON','Boulder Dwarf Cannon (Quest Variant)','boulderdwarf_cannon',false],
    [25333,'MQ_BOULDERDWARF_LEADER','Boulder Dwarf Leader (Quest Variant)','boulderdwarf_leader',false],
    [25334,'MQ_APARGREL','Apargrel','devildwarf_hammer_armor',false],
    [25336,'BOULDERDWARF_SM','Boulder Dwarf Swordmaster','boulderdwarf_sm',false]
  ];

  clientIdentities.forEach(([id,internalName,name,clientSpriteKey,memorial]) => upsert({
    id,internalName,name,clientSpriteKey,memorial,
    clientIdentityVerified:true,clientSpriteVerified:true,zeroDbSprite:true
  }));

  // Nordfeld values cross-checked with current Zero databases. When they conflict,
  // the in-game Monster Info screenshots supplied for this Global server take priority.
  upsert({
    id:25321,internalName:'BOULDERDWARF_MACE',name:'Boulder Dwarf Mace',
    level:23,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:1,
    maps:[{mapId:'nrd_fild02',mapName:'Nordfeld Hills',amount:60}]
  });
  upsert({
    id:25322,internalName:'BOULDERDWARF_HAMMER',name:'Boulder Dwarf Hammer',
    level:22,hp:355,def:34,mdef:2,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:1,
    elementModifiers:{Neutral:100,Water:100,Earth:25,Fire:150,Wind:90,Poison:125,Holy:100,Shadow:100,Ghost:100,Undead:100},
    maps:[{mapId:'nrd_fild01',mapName:'Nordfeld Field',amount:100}]
  });
  upsert({
    id:25323,internalName:'PORING_GEM',name:'Gem Poring',
    level:17,race:'Plant',element:'Earth',
    maps:[{mapId:'nrd_fild01',mapName:'Nordfeld Field',amount:60},{mapId:'nrd_fild02',mapName:'Nordfeld Hills',amount:50}]
  });
  upsert({
    id:25324,internalName:'NORDIUM_GOLEM',name:'Nordium Golem',
    level:24,race:'Formless',size:'Large',element:'Earth',elementLevel:2,
    elementModifiers:{Neutral:100,Water:100,Earth:0,Fire:175,Wind:80,Poison:150,Holy:100,Shadow:100,Ghost:100,Undead:100},
    maps:[{mapId:'nrd_fild02',mapName:'Nordfeld Hills',amount:50}]
  });
  upsert({
    id:25325,internalName:'BOULDERDWARF_PICK',name:'Pickaxe Boulder Dwarf',
    level:25,hp:488,def:57,mdef:2,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:1,
    elementModifiers:{Neutral:100,Water:100,Earth:25,Fire:150,Wind:90,Poison:125,Holy:100,Shadow:100,Ghost:100,Undead:100},
    maps:[{mapId:'nrd_dun01',mapName:'Nordfeld Cave 1F',amount:80}]
  });
  upsert({
    id:25326,internalName:'BOULDERDWARF_CANNON',name:'Boulder Dwarf Cannon',
    level:24,race:'Demi-Human',element:'Earth',
    maps:[{mapId:'nrd_dun01',mapName:'Nordfeld Cave 1F',amount:80}]
  });
  upsert({
    id:25327,internalName:'BOULDERDWARF_HAMMER_MJ',name:'Boulder Dwarf Siege Trooper',
    level:64,hp:53518,def:198,mdef:15,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:2,
    maps:[{mapId:'nrd_dun02',mapName:'Nordfeld Cave 2F',amount:70}],
    elementModifiers:{Neutral:100,Water:100,Earth:0,Fire:175,Wind:80,Poison:150,Holy:100,Shadow:100,Ghost:100,Undead:100},
    clientScreenshotVerified:true
  });
  upsert({
    id:25328,internalName:'BOULDERDWARF_MACE_MJ',name:'Boulder Dwarf Squad Leader',
    level:65,hp:55602,def:179,mdef:30,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:2,
    maps:[{mapId:'nrd_dun02',mapName:'Nordfeld Cave 2F',amount:70}],
    elementModifiers:{Neutral:100,Water:100,Earth:0,Fire:175,Wind:80,Poison:150,Holy:100,Shadow:100,Ghost:100,Undead:100},
    clientScreenshotVerified:true
  });
  upsert({
    id:25329,internalName:'BOULDERDWARF_LEADER_MJ',name:'Boulder Dwarf Captain',
    level:64,hp:49984,def:224,mdef:23,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:3,
    maps:[{mapId:'nrd_dun02',mapName:'Nordfeld Cave 2F',amount:70}],
    elementModifiers:{Neutral:100,Water:100,Earth:0,Fire:200,Wind:70,Poison:125,Holy:100,Shadow:100,Ghost:100,Undead:100},
    clientScreenshotVerified:true
  });
  upsert({
    id:25336,internalName:'BOULDERDWARF_SM',name:'Boulder Dwarf Swordmaster',
    level:64,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:3,
    elementModifiers:{Neutral:100,Water:100,Earth:0,Fire:200,Wind:70,Poison:175,Holy:100,Shadow:100,Ghost:100,Undead:100},
    maps:[{mapId:'nrd_dun02',mapName:'Nordfeld Cave 2F',amount:1}]
  });

  // Memorial identities are separate monsters in the client. Server-side stats
  // remain conservative where the Global client itself cannot confirm them.
  upsert({
    id:3901,internalName:'MD_ORK_HERO',name:'Fallen Orc Hero (Memorial)',memorial:true,
    level:70,hp:2110562,baseExp:166639,jobExp:118717,def:197,mdef:70,
    race:'Demi-Human',size:'Large',element:'Earth',elementLevel:2,
    elementModifiers:{Neutral:100,Water:100,Earth:0,Fire:175,Wind:80,Poison:150,Holy:100,Shadow:100,Ghost:100,Undead:100},
    boss:true,mvp:false,modes:['Boss Type'],clientIdentityVerified:true
  });
  upsert({
    id:3975,internalName:'MD_GOLDEN_BUG',name:'Golden Thief Bug (Memorial)',memorial:true,
    level:60,hp:1200000,baseExp:75000,jobExp:63000,def:159,mdef:81,
    race:'Insect',size:'Large',element:'Fire',elementLevel:2,
    attackMin:771,attackMax:1091,magicAttackMin:576,magicAttackMax:967,hit:337,flee:370,
    elementModifiers:{Neutral:100,Water:175,Earth:80,Fire:0,Wind:100,Poison:150,Holy:100,Shadow:100,Ghost:100,Undead:80},
    drops:[{itemId:701,name:'Ora Ora',rate:2},{itemId:985,name:'Elunium',rate:10},{itemId:984,name:'Oridecon',rate:10},{itemId:25429,name:'Mythril Ore',rate:null}],
    boss:true,mvp:false,modes:['Boss Type'],clientIdentityVerified:true
  });
  upsert({id:3897,memorial:true,race:'Undead',size:'Medium',element:'Undead'});
  upsert({id:3898,memorial:true,size:'Medium',element:'Undead'});
  upsert({id:3903,memorial:true,race:'Plant',size:'Medium',element:'Earth'});
  upsert({id:3972,memorial:true,name:'Thief Bug Male (Memorial)'});
  upsert({id:3973,memorial:true,name:'Thief Bug (Memorial)'});
  upsert({id:3974,memorial:true,name:'Thief Bug Egg (Memorial)'});
  [3810,3811,3812,3813,3814,3815,3816,20076,20077,20078,20079,20080].forEach(id=>upsert({id,memorial:true}));

  // Recover map locations and spawn counts directly from the supplied client's
  // navigation monster table. Match by exact Mob-ID first, avoiding internal-name
  // differences such as ORC_/ORK_ and suffix variants. Existing special maps are
  // preserved; client Navi only fills missing maps or adds missing map entries.
  const rawNav = Array.isArray(window.RZ_CLIENT_MONSTERS_RAW) ? window.RZ_CLIENT_MONSTERS_RAW : [];
  const mapLabels = Array.isArray(window.RZ_CLIENT_MONSTER_MAP_LABELS) ? window.RZ_CLIENT_MONSTER_MAP_LABELS : [];
  const mapIndex = window.RZ_CLIENT_MONSTER_MAP_INDEX && typeof window.RZ_CLIENT_MONSTER_MAP_INDEX === 'object' ? window.RZ_CLIENT_MONSTER_MAP_INDEX : {};
  const navById = new Map();
  for (const entry of rawNav) {
    if (!Array.isArray(entry) || entry.length < 7) continue;
    const mobId = Number(entry[0]);
    const rawMaps = Array.isArray(entry[6]) ? entry[6] : [];
    if (!Number.isFinite(mobId) || !rawMaps.length) continue;
    const bucket = navById.get(mobId) || new Map();
    for (const pair of rawMaps) {
      if (!Array.isArray(pair) || !pair.length) continue;
      const mapId = String(pair[0] ?? '').trim();
      if (!mapId) continue;
      const rawAmount = Number(pair[1]);
      const amount = Number.isFinite(rawAmount) && rawAmount > 0 ? rawAmount : null;
      const idx = mapIndex[mapId];
      const mapName = Number.isInteger(idx) && mapLabels[idx] ? mapLabels[idx] : mapId;
      const previous = bucket.get(mapId);
      if (!previous || (amount ?? 0) > (previous.amount ?? 0)) {
        bucket.set(mapId,{mapId,mapName,amount,respawn:null,verified:true,clientVerified:true,source:'client-navigation'});
      }
    }
    if (bucket.size) navById.set(mobId,bucket);
  }
  for (const monster of rows) {
    const mobId = Number(monster?.clientId ?? monster?.id);
    const navMaps = navById.get(mobId);
    if (!navMaps?.size) continue;
    const merged = new Map();
    for (const existing of (Array.isArray(monster.maps) ? monster.maps : [])) {
      const mapId = String(existing?.mapId ?? '').trim();
      if (mapId) merged.set(mapId,existing);
    }
    for (const [mapId,navMap] of navMaps) {
      const existing = merged.get(mapId);
      if (!existing) merged.set(mapId,navMap);
      else if (existing.amount == null && navMap.amount != null) merged.set(mapId,{...existing,amount:navMap.amount,clientVerified:true,source:existing.source||'client-navigation'});
    }
    monster.maps=[...merged.values()];
    monster.clientNavigationRecovered=true;
  }

  rows.forEach(m => { m.skills = cleanSkills(m.skills); });
  rows.sort((a,b)=>String(a.name||'').localeCompare(String(b.name||''),'en',{sensitivity:'base'}));
  window.RZ_CLIENT_MONSTERS = rows;
})();
