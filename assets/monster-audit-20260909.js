(() => {
  'use strict';
  const rows=window.RO_DATA?.monsters;
  if(!Array.isArray(rows))return;
  const byId=id=>rows.find(m=>Number(m?.clientId??m?.id)===Number(id));
  const patch=(id,data)=>{const m=byId(id);if(m)Object.assign(m,data,{id:String(id),clientId:Number(id),spriteId:Number(id)});};
  const skill=(internalName,name,level)=>({internalName,name,level,rate:null});
  const drop=(itemId,name,rate=null)=>({itemId,name,rate});

  // Server-side skill activation rates are not in the supplied client.
  // Keep only skill identity + level, remove visual Emotion helpers and duplicates.
  for(const m of rows){
    const seen=new Set(),clean=[];
    for(const s of (Array.isArray(m.skills)?m.skills:[])){
      const internal=String(s?.internalName||s?.name||s?.skill||'').trim().toUpperCase();
      if(!internal||internal==='NPC_EMOTION'||internal==='NPC_EMOTION_ON')continue;
      const key=`${internal}|${s?.level??''}`;
      if(seen.has(key))continue;
      seen.add(key);
      clean.push(typeof s==='object'?{...s,rate:null}:s);
    }
    m.skills=clean;
  }

  const neutral2={Neutral:100,Water:100,Earth:100,Fire:100,Wind:100,Poison:100,Holy:100,Shadow:100,Ghost:100,Undead:100};
  const earth1={Neutral:100,Water:100,Earth:25,Fire:150,Wind:90,Poison:125,Holy:100,Shadow:100,Ghost:100,Undead:100};
  const earth2={Neutral:100,Water:100,Earth:0,Fire:175,Wind:80,Poison:150,Holy:100,Shadow:100,Ghost:100,Undead:100};
  const fire1={Neutral:100,Water:150,Earth:90,Fire:25,Wind:100,Poison:125,Holy:100,Shadow:100,Ghost:100,Undead:100};
  const wind1={Neutral:100,Water:90,Earth:150,Fire:100,Wind:25,Poison:125,Holy:100,Shadow:100,Ghost:100,Undead:100};
  const water1={Neutral:100,Water:25,Earth:100,Fire:90,Wind:150,Poison:100,Holy:100,Shadow:100,Ghost:100,Undead:100};
  const poison1={Neutral:100,Water:100,Earth:100,Fire:100,Wind:100,Poison:0,Holy:100,Shadow:50,Ghost:100,Undead:50};
  const holy1={Neutral:100,Water:75,Earth:75,Fire:75,Wind:75,Poison:75,Holy:0,Shadow:125,Ghost:75,Undead:100};

  // ──────────────────────────────────────────────────────────────────────────
  // NORDFELD / BOULDER DWARFS
  // Identity + sprite are client-confirmed. Spawn counts and server fields are
  // retained only when corroborated by current Zero databases or screenshots.
  // Values not confirmed by those sources deliberately remain null / ???.
  // ──────────────────────────────────────────────────────────────────────────
  patch(25321,{name:'Boulder Dwarf Mace',internalName:'BOULDERDWARF_MACE',clientSpriteKey:'boulderdwarf_mace',level:23,hp:null,def:null,mdef:null,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:1,elementModifiers:earth1,maps:[{mapId:'nrd_fild02',mapName:'Nordfeld Hills',amount:60}],drops:[drop(507,'Red Herb'),drop(1002997,'Boulder Dwarf Token'),drop(300936,'Mace Boulder Dwarf Card')],zeroDatabaseCrossChecked:true});
  patch(25322,{name:'Boulder Dwarf Hammer',internalName:'BOULDERDWARF_HAMMER',clientSpriteKey:'boulderdwarf_hammer',level:22,hp:355,def:34,mdef:2,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:1,elementModifiers:earth1,maps:[{mapId:'nrd_fild01',mapName:'Nordfeld Plains',amount:100}],drops:[drop(507,'Red Herb'),drop(601,'Fly Wing'),drop(7067,'Stone Fragment'),drop(1002997,'Boulder Dwarf Token'),drop(300937,'Hammer Boulder Dwarf Card')],zeroDatabaseCrossChecked:true});
  patch(25323,{name:'Gem Poring',internalName:'PORING_GEM',clientSpriteKey:'poring_gem',level:17,hp:null,def:null,mdef:null,race:'Plant',size:'Medium',element:'Earth',elementLevel:1,elementModifiers:earth1,maps:[{mapId:'nrd_fild01',mapName:'Nordfeld Plains',amount:60},{mapId:'nrd_fild02',mapName:'Nordfeld Hills',amount:50}],drops:[drop(507,'Red Herb'),drop(512,'Apple'),drop(909,'Jellopy'),drop(910,'Garlet'),drop(1002995,'Gleaming Pebble'),drop(300938,'Gem Poring Card')],zeroDatabaseCrossChecked:true});
  patch(25324,{name:'Nordium Golem',internalName:'NORDIUM_GOLEM',clientSpriteKey:'nordium_golem',level:24,hp:null,def:null,mdef:null,race:'Formless',size:'Large',element:'Earth',elementLevel:2,elementModifiers:earth2,maps:[{mapId:'nrd_fild02',mapName:'Nordfeld Hills',amount:50}],drops:[drop(300939,'Nordium Golem Card'),drop(null,'Nordium Fragment')],zeroDatabaseCrossChecked:true});
  patch(25325,{name:'Pickaxe Boulder Dwarf',internalName:'BOULDERDWARF_PICK',clientSpriteKey:'boulderdwarf_pick',level:25,hp:488,def:57,mdef:2,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:1,elementModifiers:earth1,maps:[{mapId:'nrd_dun01',mapName:'Nordfeld Cave 1F',amount:80}],drops:[drop(507,'Red Herb'),drop(1002997,'Boulder Dwarf Token'),drop(300940,'Pickaxe Boulder Dwarf Card')],zeroDatabaseCrossChecked:true});
  patch(25326,{name:'Boulder Dwarf Cannon',internalName:'BOULDERDWARF_CANNON',clientSpriteKey:'boulderdwarf_cannon',level:24,hp:null,def:null,mdef:null,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:1,elementModifiers:earth1,maps:[{mapId:'nrd_dun01',mapName:'Nordfeld Cave 1F',amount:80}],drops:[drop(1002997,'Boulder Dwarf Token'),drop(300941,'Cannon Boulder Dwarf Card')],zeroDatabaseCrossChecked:true});

  // These three values come from the user's in-game Global Monster Info windows;
  // they override conflicting community database values.
  patch(25327,{name:'Boulder Dwarf Siege Trooper',internalName:'BOULDERDWARF_HAMMER_MJ',clientSpriteKey:'boulderdwarf_hammer_armor',level:64,hp:53518,def:198,mdef:15,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:2,elementModifiers:earth2,maps:[{mapId:'nrd_dun02',mapName:'Nordfeld Cave 2F',amount:70}],drops:[drop(1003,'Coal'),drop(470465,"Archeologist's Shoes"),drop(1002998,'Advanced Boulder Dwarf Token'),drop(300942,'Boulder Dwarf Siege Trooper Card')],clientScreenshotVerified:true,zeroDatabaseCrossChecked:true});
  patch(25328,{name:'Boulder Dwarf Squad Leader',internalName:'BOULDERDWARF_MACE_MJ',clientSpriteKey:'boulderdwarf_mace_armor',level:65,hp:55602,def:179,mdef:30,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:2,elementModifiers:earth2,maps:[{mapId:'nrd_dun02',mapName:'Nordfeld Cave 2F',amount:70}],drops:[drop(1002,'Iron Ore'),drop(470465,"Archeologist's Shoes"),drop(1002998,'Advanced Boulder Dwarf Token'),drop(300943,'Boulder Dwarf Squad Leader Card')],clientScreenshotVerified:true,zeroDatabaseCrossChecked:true});
  patch(25329,{name:'Boulder Dwarf Captain',internalName:'BOULDERDWARF_LEADER_MJ',clientSpriteKey:'boulderdwarf_leader',level:64,hp:49984,def:224,mdef:23,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:3,maps:[{mapId:'nrd_dun02',mapName:'Nordfeld Cave 2F',amount:70}],elementModifiers:{Neutral:100,Water:100,Earth:0,Fire:200,Wind:70,Poison:125,Holy:100,Shadow:100,Ghost:100,Undead:100},drops:[drop(590071,'Chain [3]'),drop(470464,"Guard's Boots"),drop(450586,'Nordium Plate'),drop(1002998,'Advanced Boulder Dwarf Token'),drop(300944,'Boulder Dwarf Captain Card')],clientScreenshotVerified:true,zeroDatabaseCrossChecked:true});
  patch(25336,{name:'Boulder Dwarf Swordmaster',internalName:'BOULDERDWARF_SM',clientSpriteKey:'boulderdwarf_sm',level:64,hp:null,def:null,mdef:null,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:3,elementModifiers:{Neutral:100,Water:100,Earth:0,Fire:200,Wind:70,Poison:175,Holy:100,Shadow:100,Ghost:100,Undead:100},maps:[{mapId:'nrd_dun02',mapName:'Nordfeld Cave 2F',amount:1}],drops:[drop(300964,'Boulder Dwarf Swordmaster Card')],zeroDatabaseCrossChecked:true});

  // ──────────────────────────────────────────────────────────────────────────
  // PORING VILLAGE MEMORIAL — current RO Zero database values. No EXP is
  // published for these instance mobs, so EXP remains ??? rather than inferred.
  // ──────────────────────────────────────────────────────────────────────────
  patch(3810,{name:'King Poring (Memorial)',internalName:'MD_KING_PORING',memorial:true,level:35,hp:140000,def:20,mdef:20,attackMin:189,attackMax:243,magicAttackMin:168,magicAttackMax:240,hit:295,flee:271,race:'Formless',size:'Large',element:'Neutral',elementLevel:2,elementModifiers:neutral2,boss:true,mvp:false,modes:['Boss Type','Aggressive','Physically Attackable','Can Move','Changes Target When Attacked','Changes Target on Melee','Cast Sensor (Chase)','Cast Sensor (Idle)','Changes Chase Target'],drops:[drop(508,'Yellow Herb',30),drop(509,'White Herb',30),drop(510,'Blue Herb',30),drop(511,'Green Herb',30),drop(6498,'Jejellopy',30),drop(7126,'Large Jellopy',30),drop(19238,'Poring Village Leek'),drop(19239,'Poring Village Carrot'),drop(23649,'Jellopy Fragment Box'),drop(25465,'Poring Jello Fragment'),drop(25466,'Poporing Jello Fragment'),drop(25467,'Drops Jello Fragment'),drop(25468,'Deviling Jello Fragment'),drop(25469,'Angeling Jello Fragment')],skills:[skill('MG_FIREBALL','Fire Ball',3),skill('AL_DECAGI','Decrease AGI',3),skill('MC_MAMMONITE','Mammonite',3),skill('AC_DOUBLE','Double Strafe',3),skill('SM_BASH','Bash',3),skill('TF_POISON','Envenom',3)],zeroDatabaseCrossChecked:true});
  patch(3811,{name:'Goldring (Memorial)',internalName:'MD_GOLDRING',memorial:true,level:35,hp:72118,def:10,mdef:10,attackMin:153,attackMax:193,magicAttackMin:137,magicAttackMax:191,hit:283,flee:258,race:'Formless',size:'Large',element:'Holy',elementLevel:1,elementModifiers:holy1,boss:true,mvp:false,modes:['Mini Boss','Aggressive','Physically Attackable','Can Move'],drops:[drop(508,'Yellow Herb',30),drop(6498,'Jejellopy',30),drop(546,'Yellow Slim Potion',0.1),drop(728,'Topaz',0.1)],skills:[skill('NPC_STUNATTACK','Stun Attack',5)],zeroDatabaseCrossChecked:true});
  patch(3812,{name:'Amering (Memorial)',internalName:'MD_AMERING',memorial:true,level:35,hp:72810,def:10,mdef:10,attackMin:152,attackMax:192,magicAttackMin:137,magicAttackMax:191,hit:283,flee:258,race:'Formless',size:'Large',element:'Poison',elementLevel:1,elementModifiers:poison1,boss:true,mvp:false,modes:['Mini Boss','Aggressive','Physically Attackable','Can Move'],drops:[drop(507,'Red Herb',30),drop(6498,'Jejellopy',30),drop(510,'Blue Herb',1),drop(719,'Amethyst',0.1)],skills:[skill('NPC_WIDECONFUSE','Wide Confuse',1)],zeroDatabaseCrossChecked:true});
  patch(3813,{name:'Drops (Memorial)',internalName:'MD_DROPS',memorial:true,level:35,hp:1095,def:10,mdef:10,attackMin:104,attackMax:130,magicAttackMin:70,magicAttackMax:84,hit:259,flee:231,race:'Formless',size:'Small',element:'Fire',elementLevel:1,elementModifiers:fire1,modes:['Physically Attackable','Can Move','Loots Items'],drops:[drop(909,'Jellopy',50),drop(512,'Apple',10),drop(938,'Sticky Mucus',6),drop(601,'Fly Wing',5),drop(550139,'Rod',0.8),drop(4004,'Drops Card',0.25),drop(620,'Orange Juice',0.2)],skills:[skill('NPC_BLINDATTACK','Blind Attack',3),skill('NPC_FIREATTACK','Fire Property Attack',1)],zeroDatabaseCrossChecked:true});
  patch(3814,{name:'Poporing (Memorial)',internalName:'MD_POPORING',memorial:true,level:36,hp:1167,def:10,mdef:12,attackMin:109,attackMax:137,magicAttackMin:72,magicAttackMax:88,hit:260,flee:232,race:'Formless',size:'Small',element:'Wind',elementLevel:1,elementModifiers:wind1,modes:['Physically Attackable','Can Move','Loots Items'],drops:[drop(938,'Sticky Mucus',50),drop(511,'Green Herb',10),drop(910,'Garlet',10),drop(506,'Green Potion',5),drop(601,'Fly Wing',5),drop(514,'Grape',2),drop(510129,'Main Gauche [4]',0.2),drop(4033,'Poporing Card',0.1)],skills:[skill('NPC_POISON','Poison',1),skill('NPC_POISONATTACK','Poison Property Attack',1)],zeroDatabaseCrossChecked:true});
  patch(3815,{name:'Poring (Memorial)',internalName:'MD_PORING',memorial:true,level:34,hp:1023,def:10,mdef:12,attackMin:100,attackMax:124,magicAttackMin:68,magicAttackMax:80,hit:258,flee:230,race:'Formless',size:'Small',element:'Earth',elementLevel:1,elementModifiers:earth1,modes:['Physically Attackable','Can Move','Loots Items'],drops:[drop(909,'Jellopy',50),drop(512,'Apple',10),drop(601,'Fly Wing',5),drop(938,'Sticky Mucus',4),drop(4001,'Poring Card',0.2)],skills:[skill('NPC_SILENCEATTACK','Silence Attack',2)],zeroDatabaseCrossChecked:true});
  patch(3816,{name:'Marin (Memorial)',internalName:'MD_MARIN',memorial:true,level:33,hp:960,def:10,mdef:10,attackMin:95,attackMax:117,magicAttackMin:66,magicAttackMax:78,hit:257,flee:229,race:'Formless',size:'Small',element:'Water',elementLevel:1,elementModifiers:water1,modes:['Physically Attackable','Can Move','Loots Items'],drops:[drop(910,'Garlet',16),drop(938,'Sticky Mucus',7.5),drop(601,'Fly Wing',5),drop(529,'Candy',1.75),drop(700,'Lv.1 Frost Diver',0.5),drop(510,'Blue Herb',0.38),drop(4196,'Marin Card',0.01),drop(5035,'Poring Hat',0.01)],skills:[skill('NPC_WATERATTACK','Water Property Attack',1),skill('AL_HEAL','Heal',1)],zeroDatabaseCrossChecked:true});

  // ──────────────────────────────────────────────────────────────────────────
  // OTHER MEMORIAL BOSSES. Identity/sprite comes from the supplied client.
  // These server values are kept only where the MD-specific monster ID itself
  // has a matching database entry; they are not copied from normal MVP IDs.
  // ──────────────────────────────────────────────────────────────────────────
  patch(3901,{name:'Fallen Orc Hero (Memorial)',internalName:'MD_ORK_HERO',memorial:true,level:70,hp:2110562,baseExp:166639,jobExp:118717,def:197,mdef:70,race:'Demi-Human',size:'Large',element:'Earth',elementLevel:2,elementModifiers:earth2,boss:true,mvp:false,modes:['Boss Type'],zeroDatabaseCrossChecked:true});
  patch(3975,{name:'Golden Thief Bug (Memorial)',internalName:'MD_GOLDEN_BUG',memorial:true,level:60,hp:1200000,baseExp:75000,jobExp:63000,def:159,mdef:81,attackMin:771,attackMax:1091,magicAttackMin:576,magicAttackMax:967,hit:337,flee:370,race:'Insect',size:'Large',element:'Fire',elementLevel:2,elementModifiers:{Neutral:100,Water:175,Earth:80,Fire:0,Wind:100,Poison:150,Holy:100,Shadow:100,Ghost:100,Undead:80},drops:[drop(701,'Ora Ora',2),drop(985,'Elunium',10),drop(984,'Oridecon',10),drop(25429,'Mythril Ore',0.1)],boss:true,mvp:false,modes:['Boss Type'],skills:[skill('SM_MAGNUM','Magnum Break',null),skill('MC_MAMMONITE','Mammonite',null),skill('NPC_GUIDEDATTACK','Guided Attack',null)],zeroDatabaseCrossChecked:true});

  rows.sort((a,b)=>String(a.name||'').localeCompare(String(b.name||''),'en',{sensitivity:'base'}));
})();
