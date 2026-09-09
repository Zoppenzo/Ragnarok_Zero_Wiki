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
    let index = rows.findIndex(m => Number(m?.clientId ?? m?.id) === id);
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

  // Current Ragnarok Zero Global client screenshots supplied by the wiki owner.
  // These values override conflicting community database values.
  upsert({
    id:25327,internalName:'BOULDERDWARF_HAMMER_MJ',name:'Boulder Dwarf Siege Trooper',
    level:64,hp:53518,def:198,mdef:15,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:2,
    maps:[{mapId:'nrd_dun02',mapName:'Nordfeld Cave 2F',amount:70}],
    elementModifiers:{Neutral:100,Water:100,Earth:0,Fire:175,Wind:80,Poison:150,Holy:100,Shadow:100,Ghost:100,Undead:100},
    drops:[
      {itemId:1002,name:'Iron Ore',rate:null},{itemId:1003,name:'Coal',rate:null},{itemId:985,name:'Elunium',rate:0.1},
      {itemId:1002998,name:'Advanced Boulder Dwarf Token',rate:2},{itemId:470466,name:'Hill Patrol Boots',rate:1},
      {itemId:450588,name:"Nordtfelt Soldier's Armor",rate:1},{itemId:null,name:'Hammer',rate:1},
      {itemId:300942,name:'Boulder Dwarf Siege Trooper Card',rate:null}
    ],clientScreenshotVerified:true
  });
  upsert({
    id:25328,internalName:'BOULDERDWARF_MACE_MJ',name:'Boulder Dwarf Captain',
    level:64,hp:49984,def:224,mdef:23,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:3,
    maps:[{mapId:'nrd_dun02',mapName:'Nordfeld Cave 2F',amount:70}],
    elementModifiers:{Neutral:100,Water:100,Earth:0,Fire:200,Wind:70,Poison:125,Holy:100,Shadow:100,Ghost:100,Undead:100},
    drops:[
      {itemId:1002,name:'Iron Ore',rate:null},{itemId:1003,name:'Coal',rate:null},{itemId:985,name:'Elunium',rate:0.1},
      {itemId:1002998,name:'Advanced Boulder Dwarf Token',rate:2},{itemId:null,name:'Nordium Plate',rate:1},
      {itemId:null,name:"Guard's Boots",rate:1},{itemId:null,name:'Flail',rate:1},
      {itemId:300944,name:'Boulder Dwarf Captain Card',rate:null}
    ],clientScreenshotVerified:true
  });
  upsert({
    id:25329,internalName:'BOULDERDWARF_LEADER_MJ',name:'Boulder Dwarf Squad Leader',
    level:65,hp:55602,def:179,mdef:30,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:2,
    maps:[{mapId:'nrd_dun02',mapName:'Nordfeld Cave 2F',amount:70}],
    elementModifiers:{Neutral:100,Water:100,Earth:0,Fire:175,Wind:80,Poison:150,Holy:100,Shadow:100,Ghost:100,Undead:100},
    drops:[
      {itemId:1002,name:'Iron Ore',rate:null},{itemId:1003,name:'Coal',rate:null},{itemId:985,name:'Elunium',rate:0.1},
      {itemId:1002998,name:'Advanced Boulder Dwarf Token',rate:2},{itemId:null,name:'Nordtfelt Mantle',rate:1},
      {itemId:470465,name:"Archeologist's Shoes",rate:1},{itemId:null,name:'Chain',rate:1},
      {itemId:300943,name:'Boulder Dwarf Squad Leader Card',rate:null}
    ],clientScreenshotVerified:true
  });

  // Additional Boulder Dwarf identities confirmed in the supplied official data.grf.
  // Community sources currently do not expose reliable HP/DEF/MDEF for these four, so those stay n/a.
  upsert({id:25321,internalName:'BOULDERDWARF_MACE',name:'Boulder Dwarf Mace',level:23,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:1,maps:[{mapId:'nrd_fild02',mapName:'Nordfeld Field 2',amount:null}],elementModifiers:{Neutral:100,Water:100,Earth:25,Fire:150,Wind:90,Poison:125,Holy:100,Shadow:100,Ghost:100,Undead:100},drops:[{itemId:1002997,name:'Boulder Dwarf Token',rate:null},{itemId:300936,name:'Mace Boulder Dwarf Card',rate:null}],clientIdentityVerified:true});
  upsert({id:25322,internalName:'BOULDERDWARF_HAMMER',name:'Boulder Dwarf Hammer',level:22,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:1,maps:[{mapId:'nrd_fild01',mapName:'Nordfeld Field 1',amount:null}],elementModifiers:{Neutral:100,Water:100,Earth:25,Fire:150,Wind:90,Poison:125,Holy:100,Shadow:100,Ghost:100,Undead:100},drops:[{itemId:1002997,name:'Boulder Dwarf Token',rate:null},{itemId:300937,name:'Hammer Boulder Dwarf Card',rate:null}],clientIdentityVerified:true});
  upsert({id:25325,internalName:'BOULDERDWARF_PICK',name:'Boulder Dwarf Pick',level:25,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:1,maps:[{mapId:'nrd_dun01',mapName:'Nordfeld Cave 1F',amount:null}],elementModifiers:{Neutral:100,Water:100,Earth:25,Fire:150,Wind:90,Poison:125,Holy:100,Shadow:100,Ghost:100,Undead:100},drops:[{itemId:1002997,name:'Boulder Dwarf Token',rate:null},{itemId:null,name:'Pickaxe Boulder Dwarf Card',rate:null}],clientIdentityVerified:true});
  upsert({id:25326,internalName:'BOULDERDWARF_CANNON',name:'Boulder Dwarf Cannon',level:24,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:1,maps:[{mapId:'nrd_dun01',mapName:'Nordfeld Cave 1F',amount:null}],elementModifiers:{Neutral:100,Water:100,Earth:25,Fire:150,Wind:90,Poison:125,Holy:100,Shadow:100,Ghost:100,Undead:100},drops:[{itemId:1002997,name:'Boulder Dwarf Token',rate:null},{itemId:300941,name:'Cannon Boulder Dwarf Card',rate:null}],clientIdentityVerified:true});

  // Memorial Dungeon identities confirmed directly in the supplied official data.grf.
  // Non-boss entries are kept intentionally conservative when the current client does not expose server combat values.
  upsert({id:3897,internalName:'MD_ORC_SKELETON',name:'Orc Skeleton (Memorial)',level:60,hp:4458,race:'Undead',size:'Medium',element:'Undead',elementLevel:1,clientIdentityVerified:true});
  upsert({id:3898,internalName:'MD_ORC_ZOMBIE',name:'Orc Zombie (Memorial)',level:60,hp:4475,size:'Medium',element:'Undead',elementLevel:1,clientIdentityVerified:true});
  upsert({id:3903,internalName:'MD_ORC_FLOWER',name:"Shaman's Flower",level:98,hp:5,race:'Plant',size:'Medium',element:'Earth',elementLevel:1,clientIdentityVerified:true});
  upsert({
    id:3901,internalName:'MD_ORK_HERO',name:'Fallen Orc Hero (Memorial)',level:70,hp:2110562,
    baseExp:166639,jobExp:118717,def:197,mdef:70,race:'Demi-Human',size:'Large',element:'Earth',elementLevel:2,
    elementModifiers:{Neutral:100,Water:100,Earth:0,Fire:175,Wind:80,Poison:150,Holy:100,Shadow:100,Ghost:100,Undead:100},
    boss:true,mvp:true,modes:['Boss Type'],clientIdentityVerified:true
  });

  upsert({id:3972,internalName:'MD_THIEF_BUG__',name:'Thief Bug Male (Memorial)',level:60,hp:3330,def:40,mdef:20,race:'Formless',size:'Medium',element:'Shadow',elementLevel:1,attackMin:206,attackMax:262,magicAttackMin:98,magicAttackMax:122,hit:334,flee:292,elementModifiers:{Neutral:100,Water:100,Earth:100,Fire:100,Wind:100,Poison:75,Holy:125,Shadow:0,Ghost:90,Undead:0},clientIdentityVerified:true});
  upsert({id:3973,internalName:'MD_THIEF_BUG',name:'Thief Bug (Memorial)',level:60,hp:200,def:24,mdef:3,race:'Insect',size:'Small',element:'Neutral',elementLevel:3,attackMin:122,attackMax:134,magicAttackMin:74,magicAttackMax:86,hit:274,flee:254,elementModifiers:{Neutral:100,Water:100,Earth:100,Fire:100,Wind:100,Poison:100,Holy:100,Shadow:100,Ghost:50,Undead:100},clientIdentityVerified:true});
  upsert({id:3974,internalName:'MD_THIEF_BUG_EGG',name:'Thief Bug Egg (Memorial)',level:60,hp:10,def:64,mdef:10,race:'Insect',size:'Small',element:'Shadow',elementLevel:1,attackMin:68,attackMax:72,magicAttackMin:67,magicAttackMax:73,hit:260,flee:230,elementModifiers:{Neutral:100,Water:100,Earth:100,Fire:100,Wind:100,Poison:75,Holy:125,Shadow:0,Ghost:90,Undead:0},clientIdentityVerified:true});
  upsert({
    id:3975,internalName:'MD_GOLDEN_BUG',name:'Golden Thief Bug (Memorial)',level:60,hp:1200000,
    baseExp:75000,jobExp:63000,def:159,mdef:81,race:'Insect',size:'Large',element:'Fire',elementLevel:2,
    attackMin:771,attackMax:1091,magicAttackMin:576,magicAttackMax:967,hit:337,flee:370,
    elementModifiers:{Neutral:100,Water:175,Earth:80,Fire:0,Wind:100,Poison:150,Holy:100,Shadow:100,Ghost:100,Undead:80},
    drops:[{itemId:701,name:'Ora Ora',rate:2},{itemId:985,name:'Elunium',rate:10},{itemId:984,name:'Oridecon',rate:10},{itemId:25429,name:'Mythril Ore',rate:0.1}],
    boss:true,mvp:true,modes:['Boss Type'],clientIdentityVerified:true
  });

  rows.forEach(m => { m.skills = cleanSkills(m.skills); });
  rows.sort((a,b)=>String(a.name||'').localeCompare(String(b.name||''),'en',{sensitivity:'base'}));
  window.RZ_CLIENT_MONSTERS = rows;
})();
