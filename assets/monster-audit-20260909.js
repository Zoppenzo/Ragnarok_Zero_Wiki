(() => {
  'use strict';
  const rows=window.RO_DATA?.monsters;
  if(!Array.isArray(rows))return;
  const byId=id=>rows.find(m=>Number(m?.clientId??m?.id)===Number(id));
  const patch=(id,data)=>{const m=byId(id);if(m)Object.assign(m,data,{id:String(id),clientId:Number(id),spriteId:Number(id)});};

  // Monster skill activation rates are server AI values and are not exposed by the supplied client.
  // Keep skill presence + level only, remove visual Emotion helpers and merge duplicates across states/rates.
  for(const m of rows){
    const seen=new Set(),clean=[];
    for(const skill of (Array.isArray(m.skills)?m.skills:[])){
      const internal=String(skill?.internalName||skill?.name||skill?.skill||'').trim().toUpperCase();
      if(!internal||internal==='NPC_EMOTION'||internal==='NPC_EMOTION_ON')continue;
      const key=`${internal}|${skill?.level??''}`;
      if(seen.has(key))continue;
      seen.add(key);
      clean.push(typeof skill==='object'?{...skill,rate:null}:skill);
    }
    m.skills=clean;
  }

  const earth1={Neutral:100,Water:100,Earth:25,Fire:150,Wind:90,Poison:125,Holy:100,Shadow:100,Ghost:100,Undead:100};
  const earth2={Neutral:100,Water:100,Earth:0,Fire:175,Wind:80,Poison:150,Holy:100,Shadow:100,Ghost:100,Undead:100};
  const earth3={Neutral:100,Water:100,Earth:0,Fire:200,Wind:70,Poison:175,Holy:100,Shadow:100,Ghost:100,Undead:100};

  // Nordfeld identities/sprites were checked in the supplied Zero client.
  // The roster below is cross-checked with current Zero databases; current in-game screenshots override database conflicts.
  patch(25321,{name:'Boulder Dwarf Mace',internalName:'BOULDERDWARF_MACE',clientSpriteKey:'boulderdwarf_mace',level:23,hp:338,def:32,mdef:5,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:1,elementModifiers:earth1,maps:[{mapId:'nrd_fild02',mapName:'Nordfeld Hills',amount:60}],drops:[{itemId:507,name:'Red Herb',rate:null},{itemId:1002997,name:'Boulder Dwarf Token',rate:null},{itemId:300936,name:'Mace Boulder Dwarf Card',rate:null}],zeroDatabaseCrossChecked:true});
  patch(25322,{name:'Boulder Dwarf Hammer',internalName:'BOULDERDWARF_HAMMER',clientSpriteKey:'boulderdwarf_hammer',level:22,hp:355,def:34,mdef:2,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:1,elementModifiers:earth1,maps:[{mapId:'nrd_fild01',mapName:'Nordfeld Plains',amount:100}],drops:[{itemId:507,name:'Red Herb',rate:null},{itemId:601,name:'Fly Wing',rate:null},{itemId:7067,name:'Stone Fragment',rate:null},{itemId:1002997,name:'Boulder Dwarf Token',rate:null},{itemId:300937,name:'Hammer Boulder Dwarf Card',rate:null}],zeroDatabaseCrossChecked:true});
  patch(25323,{name:'Gem Poring',internalName:'PORING_GEM',clientSpriteKey:'poring_gem',level:17,hp:235,def:20,mdef:11,race:'Plant',size:'Medium',element:'Earth',elementLevel:1,elementModifiers:earth1,maps:[{mapId:'nrd_fild01',mapName:'Nordfeld Plains',amount:60},{mapId:'nrd_fild02',mapName:'Nordfeld Hills',amount:50}],drops:[{itemId:507,name:'Red Herb',rate:null},{itemId:512,name:'Apple',rate:null},{itemId:909,name:'Jellopy',rate:null},{itemId:910,name:'Garlet',rate:null},{itemId:1002995,name:'Gleaming Pebble',rate:null},{itemId:300938,name:'Gem Poring Card',rate:null}],zeroDatabaseCrossChecked:true});
  patch(25324,{name:'Nordium Golem',internalName:'NORDIUM_GOLEM',clientSpriteKey:'nordium_golem',level:24,hp:410,def:40,mdef:4,race:'Formless',size:'Large',element:'Earth',elementLevel:2,elementModifiers:earth2,maps:[{mapId:'nrd_fild02',mapName:'Nordfeld Hills',amount:50}],drops:[{itemId:1002,name:'Iron Ore',rate:null},{itemId:300939,name:'Nordium Golem Card',rate:null}],zeroDatabaseCrossChecked:true});
  patch(25325,{name:'Pickaxe Boulder Dwarf',internalName:'BOULDERDWARF_PICK',clientSpriteKey:'boulderdwarf_pick',level:25,hp:488,def:57,mdef:2,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:1,elementModifiers:earth1,maps:[{mapId:'nrd_dun01',mapName:'Nordfeld Cave 1F',amount:80}],drops:[{itemId:507,name:'Red Herb',rate:null},{itemId:1002997,name:'Boulder Dwarf Token',rate:null},{itemId:300940,name:'Pickaxe Boulder Dwarf Card',rate:null}],zeroDatabaseCrossChecked:true});
  patch(25326,{name:'Boulder Dwarf Cannon',internalName:'BOULDERDWARF_CANNON',clientSpriteKey:'boulderdwarf_cannon',level:24,hp:356,def:33,mdef:7,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:1,elementModifiers:earth1,maps:[{mapId:'nrd_dun01',mapName:'Nordfeld Cave 1F',amount:80}],drops:[{itemId:1002997,name:'Boulder Dwarf Token',rate:null},{itemId:300941,name:'Cannon Boulder Dwarf Card',rate:null}],zeroDatabaseCrossChecked:true});
  patch(25327,{name:'Boulder Dwarf Siege Trooper',internalName:'BOULDERDWARF_HAMMER_MJ',clientSpriteKey:'boulderdwarf_hammer_armor',level:64,hp:53518,def:198,mdef:15,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:2,elementModifiers:earth2,maps:[{mapId:'nrd_dun02',mapName:'Nordfeld Cave 2F',amount:70}],clientScreenshotVerified:true,zeroDatabaseCrossChecked:true});
  patch(25328,{name:'Boulder Dwarf Squad Leader',internalName:'BOULDERDWARF_MACE_MJ',clientSpriteKey:'boulderdwarf_mace_armor',level:65,hp:55602,def:179,mdef:30,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:2,elementModifiers:earth2,maps:[{mapId:'nrd_dun02',mapName:'Nordfeld Cave 2F',amount:70}],clientScreenshotVerified:true,zeroDatabaseCrossChecked:true});
  patch(25329,{name:'Boulder Dwarf Captain',internalName:'BOULDERDWARF_LEADER_MJ',clientSpriteKey:'boulderdwarf_leader',level:64,hp:49984,def:224,mdef:23,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:3,maps:[{mapId:'nrd_dun02',mapName:'Nordfeld Cave 2F',amount:70}],elementModifiers:{Neutral:100,Water:100,Earth:0,Fire:200,Wind:70,Poison:125,Holy:100,Shadow:100,Ghost:100,Undead:100},clientScreenshotVerified:true,zeroDatabaseCrossChecked:true});
  patch(25336,{name:'Boulder Dwarf Swordmaster',internalName:'BOULDERDWARF_SM',clientSpriteKey:'boulderdwarf_sm',level:64,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:3,elementModifiers:earth3,maps:[{mapId:'nrd_dun02',mapName:'Nordfeld Cave 2F',amount:1}],drops:[{itemId:300964,name:'Boulder Dwarf Swordmaster Card',rate:null}],zeroDatabaseCrossChecked:true});

  rows.sort((a,b)=>String(a.name||'').localeCompare(String(b.name||''),'en',{sensitivity:'base'}));
})();
