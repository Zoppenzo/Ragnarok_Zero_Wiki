(() => {
  'use strict';
  const raw = Array.isArray(window.RZ_CLIENT_MONSTERS_RAW) ? window.RZ_CLIENT_MONSTERS_RAW : [];
  const identity = window.RZ_CLIENT_MONSTER_IDENTITY && typeof window.RZ_CLIENT_MONSTER_IDENTITY === 'object' ? window.RZ_CLIENT_MONSTER_IDENTITY : {};
  const aliases = window.RZ_CLIENT_MONSTER_ALIASES && typeof window.RZ_CLIENT_MONSTER_ALIASES === 'object' ? window.RZ_CLIENT_MONSTER_ALIASES : {};
  const zeroStats = window.RZ_MONSTER_ZERO_STATS && typeof window.RZ_MONSTER_ZERO_STATS === 'object' ? window.RZ_MONSTER_ZERO_STATS : {};
  const zeroConsensus = window.RZ_MONSTER_ZERO_CONSENSUS && typeof window.RZ_MONSTER_ZERO_CONSENSUS === 'object' ? window.RZ_MONSTER_ZERO_CONSENSUS : {};
  const rmsBehavior = window.RZ_MONSTER_RMS_BEHAVIOR && typeof window.RZ_MONSTER_RMS_BEHAVIOR === 'object' ? window.RZ_MONSTER_RMS_BEHAVIOR : {};
  if (!window.RO_DATA || !Object.keys(identity).length) return;

  const races = ['Formless','Undead','Brute','Plant','Insect','Fish','Demon','Demi-Human','Angel','Dragon'];
  const sizes = ['Small','Medium','Large'];
  const elements = ['Neutral','Water','Earth','Fire','Wind','Poison','Holy','Shadow','Ghost','Undead'];
  const labels = Array.isArray(window.RZ_CLIENT_MONSTER_MAP_LABELS) ? window.RZ_CLIENT_MONSTER_MAP_LABELS : [];
  const mapIndex = window.RZ_CLIENT_MONSTER_MAP_INDEX || {};

  // Display labels extracted from the supplied Ragnarok Zero client.
  // These labels only rename skills already present in a Zero monster source.
  const clientNpcSkillNames = {
    NPC_ALLHEAL:'Full Heal', NPC_ALL_STAT_DOWN:'All Stats Down', NPC_ANTIMAGIC:'Deadzone',
    NPC_ARMORBRAKE:'Armor Break', NPC_ARROWSTORM:'Tempestade de Flechas', NPC_BLINDATTACK:'Blind Attack',
    NPC_CLOUD_KILL:'Killing Cloud', NPC_COMET:'Comet', NPC_CRITICALWOUND:'Critical Wounds',
    NPC_DAMAGE_HEAL:'Convert Damage to Heal', NPC_DARKNESSATTACK:'Dark Attribute Attack',
    NPC_DEADLYCURSE2:'Wide Deadly Curse', NPC_DEFENDER:'Defender', NPC_DRAGONBREATH:"Dragon's Breath",
    NPC_DRAGONFEAR:'Dragon Fear', NPC_EARTHQUAKE:'Earthquake', NPC_ELECTRICWALK:'Electric Walk',
    NPC_EVILLAND:'Evil Land', NPC_EVILLAND2:'Demonic Evil Land', NPC_FATALMENACE:'Fatal Menace',
    NPC_FIREATTACK:'Fire Attribute Attack', NPC_FIRESTORM:'Fire storm', NPC_FIREWALK:'Fire Walk',
    NPC_FLAMECROSS:'Flame cross', NPC_GRADUAL_GRAVITY:'Gravity Increase', NPC_GROUNDATTACK:'Earth Attribute Attack',
    NPC_GROUNDDRIVE:'Ground Drive', NPC_HALLUCINATIONWALK:'Hallucination Walk', NPC_HELLJUDGEMENT:"Hell's Judgement",
    NPC_HELLJUDGEMENT2:'Demonic Hell Judgment', NPC_HELLPOWER:"Hell's Power", NPC_ICEMINE:'Ice mine',
    NPC_IGNITIONBREAK:'Ignition Break', NPC_IMMUNE_PROPERTY:'Elemental Immunity', NPC_JACKFROST:'Jack Frost',
    NPC_LEASH:'Leash', NPC_LEX_AETERNA:'Wide area Lex Aeterna', NPC_MAGICMIRROR:'Magic Mirror',
    NPC_MAGMA_ERUPTION:'Lava Flow', NPC_MANDRAGORA:'Mandragora Howl', NPC_MAXPAIN:'Max Pain',
    NPC_MILLENNIUMSHIELD:'Millenium Shield', NPC_MOVE_COORDINATE:'Position Shift', NPC_PIERCINGATT:'Piercing Attack',
    NPC_POISON:'Poison', NPC_POISONATTACK:'Poison Attribute Attack', NPC_PSYCHIC_WAVE:'Psychic Wave',
    NPC_PULSESTRIKE:'Pulse Strike', NPC_RAINOFMETEOR:'Rain of Meteor', NPC_RAYOFGENESIS:'Genesis Ray',
    NPC_REVERBERATION:'Reverberation', NPC_SILENCEATTACK:'Silence Attack', NPC_SLOWCAST:'Slow Cast',
    NPC_SR_CURSEDCIRCLE:'Cursed Circle', NPC_STONESKIN:'Stone Skin', NPC_STUNATTACK:'Stun Attack',
    NPC_SUMMONSLAVE:'Summon Slave', NPC_VAMPIRE_GIFT:"Vampire's Gift", NPC_VENOMFOG:'Venom fog',
    NPC_WATERATTACK:'Water Attribute Attack', NPC_WIDEBLEEDING:'Bloody Party', NPC_WIDEBLEEDING2:'Demonic Mass Bleeding',
    NPC_WIDEBODYBURNNING:'Wide area burnning', NPC_WIDECOLD:'Wide area freeze', NPC_WIDECONFUSE:'Confusion Rule',
    NPC_WIDECONFUSE2:'Demonic Mass Confuse', NPC_WIDECURSE:'Cursed Fate', NPC_WIDECURSE2:'Demonic Mass Curse',
    NPC_WIDEFREEZE:'Frozen Heart', NPC_WIDEFREEZE2:'Demonic Mass Freeze', NPC_WIDEFROSTMISTY:'Wide area frost misty',
    NPC_WIDEHEALTHFEAR:'Wide area fear', NPC_WIDELEASH:'Wide Leash', NPC_WIDESIGHT:'Wide sight',
    NPC_WIDESILENCE:'Bedlam', NPC_WIDESILENCE2:'Demonic Mass Silence', NPC_WIDESIREN:'Wide area fascination',
    NPC_WIDESLEEP:'Morpheus Slumber', NPC_WIDESLEEP2:'Demonic Mass Sleep', NPC_WIDESOULDRAIN:'Souless Defeat',
    NPC_WIDESTONE:"Medusa's Stare", NPC_WIDESTONE2:'Demonic Mass Stone', NPC_WIDESTUN:'Stunning Gaze',
    NPC_WIDESTUN2:'Demonic Mass Stun', NPC_WIDESUCK:'Wide bloodsucking', NPC_WIDEWEB:'Wide web',
    NPC_WIDE_DEEP_SLEEP:'Wide area deep sleep', NPC_WINDATTACK:'Wind Attribute Attack'
  };

  const normalizeMonsterSkill = skill => {
    if (!skill || typeof skill !== 'object') return skill;
    const internal = String(skill.internalName || skill.name || skill.skill || '').trim();
    const clientName = clientNpcSkillNames[internal];
    return clientName ? { ...skill, internalName:internal, name:clientName, clientNameVerified:true } : skill;
  };
  const visibleMonsterSkills = skills => {
    const seen=new Set();
    return (Array.isArray(skills)?skills:[]).filter(skill=>{
      const internal=String(skill?.internalName || skill?.name || skill?.skill || '').trim().toUpperCase();
      // NPC_EMOTION / NPC_EMOTION_ON are visual emotes / AI mode helpers, not useful combat skills.
      if(internal==='NPC_EMOTION' || internal==='NPC_EMOTION_ON') return false;
      const key=`${internal}|${skill?.level??''}|${skill?.rate??''}`;
      if(seen.has(key)) return false;
      seen.add(key); return true;
    }).map(normalizeMonsterSkill);
  };

  const MVP_IDS = new Set([1038,1039,1046,1086,1087,1112,1115,1147,1150,1157,1159,1190,1251,1252,1272,1312,1373,1389,1418,1492,1511,1583,1630,1688]);
  const BOSS_IDS = new Set([1089,1090,1091,1092,1093,1096,1120,1262,1283,1295,1302,1582]);
  const CLIENT_NAV_BOSS_TYPES = new Set([
    'AMON_RA','BLOODY_KNIGHT','B_FLAME_GHOST','B_ICE_GHOST','DARK_LORD','DRAKE','EDDGA',
    'EXTRA_JOKER','FLAME_GHOST','GENERAL_ORC','GOLDEN_BUG','ICE_GHOST','JENIFFER','MAYA',
    'MOONLIGHT','ORC_LORD','ORK_HERO','OSIRIS','PHREEONI','SIEGLOUSE','TAO_GUNKA','VOCAL','ZHERLTHSH'
  ]);

  const displayNames = {
    KNIGHT_OF_ABYSS:'Abysmal Knight', FARMILIAR:'Familiar', C_TOWER_MANAGER:'Tower Keeper',
    KNIGHT_OF_WINDSTORM:'Stormy Knight', ORK_HERO:'Orc Hero', ORK_WARRIOR:'Orc Warrior',
    SWORD_FISH:'Swordfish', NERAID:'Nereid', GIANT_HONET:'Giant Hornet'
  };
  const pretty = value => displayNames[value] || String(value || '').replace(/^C[12]_/, '').replace(/_{1,2}\d+$/, '').replace(/_+$/,'').replace(/_+/g, ' ').toLowerCase().replace(/\b\w/g, c => c.toUpperCase());
  const canonicalKey = internal => {
    let key=String(internal || '').replace(/^C[12]_/, '').replace(/_{1,2}\d+$/, '').replace(/_+$/, '');
    return aliases[key] || key;
  };

  const mapsByKey = new Map();
  for (const r of raw) {
    const [, internal,,,,, rawMaps] = r;
    if (!internal || /^C[12]_/.test(internal)) continue;
    const key=canonicalKey(internal);
    const bucket=mapsByKey.get(key) || new Map();
    for (const [mapId, amount] of (Array.isArray(rawMaps) ? rawMaps : [])) {
      const n=Number(amount) || null;
      const prev=bucket.get(String(mapId));
      if (!prev || (n ?? 0) > (prev.amount ?? 0)) {
        const idx=mapIndex[mapId];
        bucket.set(String(mapId), {
          mapId:String(mapId), mapName:Number.isInteger(idx) && labels[idx] ? labels[idx] : String(mapId),
          amount:n, respawn:null, verified:true, clientVerified:true
        });
      }
    }
    mapsByKey.set(key,bucket);
  }

  const rows=[];
  for (const [internal, data] of Object.entries(identity)) {
    if (!Array.isArray(data) || data.length < 5) continue;
    const [id, level, raceCode, sizeCode, propertyCode] = data.map(Number);
    if (!Number.isFinite(id)) continue;
    const elementIndex=((propertyCode % 20)+20)%20;
    const elementLevel=Math.floor(propertyCode/20);
    const maps=[...(mapsByKey.get(internal)?.values?.() || [])];
    const overlay=zeroStats[String(id)] || {};
    const consensus=zeroConsensus[String(id)] || {};
    const fields=consensus.fields&&typeof consensus.fields==='object'?consensus.fields:{};
    const fv=key=>fields[key]?.value ?? null;
    const rms=rmsBehavior[String(id)] || {};
    const isMvp=MVP_IDS.has(id);
    const isBoss=!isMvp && BOSS_IDS.has(id);
    const hasNavigation=mapsByKey.has(internal);
    const clientBossType=CLIENT_NAV_BOSS_TYPES.has(internal);
    const clientNavigationType=clientBossType?301:(hasNavigation?300:null);
    const modes=[];
    const addMode=x=>{x=String(x||'').trim(); if(x&&!modes.includes(x))modes.push(x);};
    if(clientNavigationType===301)addMode('Boss Type'); else if(clientNavigationType===300)addMode('Normal Type');
    (Array.isArray(consensus.modes)?consensus.modes:[]).forEach(addMode);
    rows.push({
      id:String(id), clientId:id, spriteId:id, internalName:internal, name:pretty(internal), aliases:[],
      level:Number.isFinite(level)?level:null,
      hp:overlay.hp??fv('hp'), sp:null, baseExp:overlay.baseExp??fv('baseExp'), jobExp:overlay.jobExp??fv('jobExp'),
      race:races[raceCode] || 'n/a', element:elements[elementIndex] || 'n/a', elementLevel:elementLevel || null,
      size:sizes[sizeCode] || 'n/a',
      attackMin:fv('attackMin'), attackMax:fv('attackMax'), magicAttackMin:fv('magicAttackMin'), magicAttackMax:fv('magicAttackMax'),
      def:overlay.def??fv('def'), mdef:overlay.mdef??fv('mdef'), hit:fv('hit'), flee:fv('flee'),
      str:null, agi:null, vit:null, int:null, dex:null, luk:null,
      walkSpeed:rms.walkSpeed??null,
      attackDelay:null, delayAfterHit:null, attackRange:null, spellRange:null, sightRange:null,
      elementModifiers:overlay.elementModifiers&&typeof overlay.elementModifiers==='object'?overlay.elementModifiers:{},
      aggressive:modes.includes('Aggressive')?true:null, boss:isBoss, mvp:isMvp, modes, clientBossType, clientNavigationType,
      propertyCode:Number.isFinite(propertyCode)?propertyCode:null,
      image:null, description:{en:'',fr:''}, drops:Array.isArray(consensus.drops)?consensus.drops:[], maps,
      skills:visibleMonsterSkills(consensus.skills), notes:{en:'',fr:''},
      verified:false, clientVerified:true, fieldMeta:fields,
      zeroOverlayApplied:Object.keys(overlay).length>0,
      zeroConsensusApplied:Object.keys(consensus).length>0,
      rmsWalkSpeedApplied:Boolean(rms.walkSpeed)
    });
  }

  // Special/current Zero monsters that are absent from the navigation-derived client identity table.
  // Values below are Zero-specific records; unsupported fields intentionally remain null.
  const special = [
    {id:3810,internalName:'MD_KING_PORING',name:'MD King Poring',level:35,race:'Formless',size:'Large',element:'Neutral',elementLevel:2,hp:140000,def:20,mdef:20,attackMin:189,attackMax:243,magicAttackMin:168,magicAttackMax:240,hit:295,flee:271,boss:true,modes:['Aggressive','Physically Attackable','Can Move','Changes Target When Attacked','Changes Target on Melee','Cast Sensor (Chase)','Cast Sensor (Idle)','Changes Chase Target'],elementModifiers:{Neutral:100,Water:100,Earth:100,Fire:100,Wind:100,Poison:100,Holy:100,Shadow:100,Ghost:100,Undead:100},drops:[{itemId:508,name:'Yellow Herb',rate:30},{itemId:509,name:'White Herb',rate:30},{itemId:510,name:'Blue Herb',rate:30},{itemId:511,name:'Green Herb',rate:30},{itemId:6498,name:'Jejellopy',rate:30},{itemId:7126,name:'Large Jellopy',rate:30}],skills:[{name:'MG_FIREBALL',level:3,rate:10},{name:'AL_DECAGI',level:3,rate:10},{name:'MC_MAMMONITE',level:3,rate:10},{name:'AC_DOUBLE',level:3,rate:10},{name:'SM_BASH',level:3,rate:10},{name:'TF_POISON',level:3,rate:10}]},
    {id:3811,internalName:'MD_GOLDRING',name:'MD Goldring',level:35,race:'Formless',size:'Large',element:'Holy',elementLevel:1,hp:72118,def:10,mdef:10,attackMin:153,attackMax:193,magicAttackMin:137,magicAttackMax:191,hit:283,flee:258,boss:true,modes:['Mini Boss','Aggressive','Physically Attackable','Can Move','Changes Target When Attacked','Changes Target on Melee','Cast Sensor (Chase)','Cast Sensor (Idle)','Changes Chase Target'],elementModifiers:{Neutral:100,Water:75,Earth:75,Fire:75,Wind:75,Poison:75,Holy:0,Shadow:125,Ghost:75,Undead:100},drops:[{itemId:508,name:'Yellow Herb',rate:30},{itemId:6498,name:'Jejellopy',rate:30},{itemId:546,name:'Yellow Slim Potion',rate:0.1},{itemId:728,name:'Topaz',rate:0.1}],skills:[{name:'NPC_STUNATTACK',level:5,rate:35}]},
    {id:3812,internalName:'MD_AMERING',name:'MD Amering',level:35,race:'Formless',size:'Large',element:'Poison',elementLevel:1,hp:72810,def:10,mdef:10,attackMin:152,attackMax:192,magicAttackMin:137,magicAttackMax:191,hit:283,flee:258,boss:true,modes:['Mini Boss','Aggressive','Physically Attackable','Can Move','Changes Target When Attacked','Changes Target on Melee','Cast Sensor (Chase)','Cast Sensor (Idle)','Changes Chase Target'],elementModifiers:{Neutral:100,Water:100,Earth:100,Fire:100,Wind:100,Poison:0,Holy:100,Shadow:50,Ghost:100,Undead:50},drops:[{itemId:507,name:'Red Herb',rate:30},{itemId:6498,name:'Jejellopy',rate:30},{itemId:510,name:'Blue Herb',rate:1},{itemId:719,name:'Amethyst',rate:0.1}],skills:[{name:'NPC_WIDECONFUSE',level:1,rate:30}]},
    {id:3813,internalName:'MD_DROPS',name:'MD Drops',level:35,race:'Formless',size:'Small',element:'Fire',elementLevel:1,hp:1095,def:10,mdef:10,attackMin:104,attackMax:130,magicAttackMin:70,magicAttackMax:84,hit:259,flee:231,modes:['Physically Attackable','Can Move','Loots Items'],elementModifiers:{Neutral:100,Water:150,Earth:90,Fire:25,Wind:100,Poison:125,Holy:100,Shadow:100,Ghost:100,Undead:100},drops:[{itemId:909,name:'Jellopy',rate:50},{itemId:512,name:'Apple',rate:10},{itemId:938,name:'Sticky Mucus',rate:6},{itemId:601,name:'Fly Wing',rate:5},{itemId:550139,name:'Rod',rate:0.8},{itemId:4004,name:'Drops Card',rate:0.25},{itemId:620,name:'Orange Juice',rate:0.2}],skills:[{name:'NPC_BLINDATTACK',level:3,rate:20},{name:'NPC_FIREATTACK',level:1,rate:20}]},
    {id:3814,internalName:'MD_POPORING',name:'MD Poporing',level:36,race:'Formless',size:'Small',element:'Wind',elementLevel:1,hp:1167,def:10,mdef:12,attackMin:109,attackMax:137,magicAttackMin:72,magicAttackMax:88,hit:260,flee:232,modes:['Physically Attackable','Can Move','Loots Items'],elementModifiers:{Neutral:100,Water:90,Earth:150,Fire:100,Wind:25,Poison:125,Holy:100,Shadow:100,Ghost:100,Undead:100},drops:[{itemId:938,name:'Sticky Mucus',rate:50},{itemId:511,name:'Green Herb',rate:10},{itemId:910,name:'Garlet',rate:10},{itemId:506,name:'Green Potion',rate:5},{itemId:601,name:'Fly Wing',rate:5},{itemId:514,name:'Grape',rate:2},{itemId:510129,name:'Main Gauche',rate:0.2},{itemId:4033,name:'Poporing Card',rate:0.1}],skills:[{name:'NPC_POISON',level:1,rate:5},{name:'NPC_POISONATTACK',level:1,rate:20}]},
    {id:3815,internalName:'MD_PORING',name:'MD Poring',level:34,race:'Formless',size:'Small',element:'Earth',elementLevel:1,hp:1023,def:10,mdef:12,attackMin:100,attackMax:124,magicAttackMin:68,magicAttackMax:80,hit:258,flee:230,modes:['Physically Attackable','Can Move','Loots Items'],elementModifiers:{Neutral:100,Water:100,Earth:25,Fire:150,Wind:90,Poison:125,Holy:100,Shadow:100,Ghost:100,Undead:100},drops:[{itemId:909,name:'Jellopy',rate:50},{itemId:512,name:'Apple',rate:10},{itemId:601,name:'Fly Wing',rate:5},{itemId:938,name:'Sticky Mucus',rate:4},{itemId:1202,name:'Knife',rate:1},{itemId:619,name:'Unripe Apple',rate:0.4},{itemId:12846,name:'Little Unripe Apple',rate:0.4},{itemId:4001,name:'Poring Card',rate:0.2}],skills:[{name:'NPC_SILENCEATTACK',level:2,rate:15}]},
    {id:3816,internalName:'MD_MARIN',name:'MD Marin',level:33,race:'Formless',size:'Small',element:'Water',elementLevel:1,hp:960,def:10,mdef:10,attackMin:95,attackMax:117,magicAttackMin:66,magicAttackMax:78,hit:257,flee:229,modes:['Physically Attackable','Can Move','Loots Items'],elementModifiers:{Neutral:100,Water:25,Earth:100,Fire:90,Wind:150,Poison:100,Holy:100,Shadow:100,Ghost:100,Undead:100},drops:[{itemId:910,name:'Garlet',rate:16},{itemId:938,name:'Sticky Mucus',rate:7.5},{itemId:601,name:'Fly Wing',rate:5},{itemId:529,name:'Candy',rate:1.75},{itemId:700,name:'Lv.1 Frost Diver',rate:0.5},{itemId:510,name:'Blue Herb',rate:0.38},{itemId:4196,name:'Marin Card',rate:0.01},{itemId:5035,name:'Poring Hat',rate:0.01}],skills:[{name:'NPC_WATERATTACK',level:1,rate:20},{name:'AL_HEAL',level:1,rate:100}]},
    {id:25327,internalName:'BOULDERDWARF_HAMMER_MJ',name:'Boulder Dwarf Siege Trooper',level:64,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:2,hp:32952,def:198,mdef:15,maps:[{mapId:'nrd_dun02',mapName:'Nordfeld Cave 2F',amount:70}],elementModifiers:{Neutral:100,Water:100,Earth:0,Fire:175,Wind:80,Poison:150,Holy:100,Shadow:100,Ghost:100,Undead:100},drops:[{itemId:1003,name:'Coal',rate:null},{itemId:470465,name:"Archeologist's Shoes",rate:null},{itemId:1002998,name:'Advanced Boulder Dwarf Token',rate:null},{itemId:300942,name:'Boulder Dwarf Siege Trooper Card',rate:null}]},
    {id:25328,internalName:'BOULDERDWARF_MACE_MJ',name:'Boulder Dwarf Squad Leader',level:65,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:2,hp:55602,def:179,mdef:30,maps:[{mapId:'nrd_dun02',mapName:'Nordfeld Cave 2F',amount:70}],elementModifiers:{Neutral:100,Water:100,Earth:0,Fire:175,Wind:80,Poison:150,Holy:100,Shadow:100,Ghost:100,Undead:100},drops:[{itemId:1002,name:'Iron Ore',rate:null},{itemId:470465,name:"Archeologist's Shoes",rate:null},{itemId:1002998,name:'Advanced Boulder Dwarf Token',rate:null},{itemId:300943,name:'Boulder Dwarf Squad Leader Card',rate:null}]},
    {id:25329,internalName:'BOULDERDWARF_LEADER_MJ',name:'Boulder Dwarf Captain',level:64,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:3,hp:54704,def:224,mdef:23,maps:[{mapId:'nrd_dun02',mapName:'Nordfeld Cave 2F',amount:70}],elementModifiers:{Neutral:100,Water:100,Earth:0,Fire:200,Wind:70,Poison:175,Holy:100,Shadow:100,Ghost:100,Undead:100},drops:[{itemId:590071,name:'Chain [3]',rate:null},{itemId:1002998,name:'Advanced Boulder Dwarf Token',rate:null},{itemId:300944,name:'Boulder Dwarf Captain Card',rate:null}]},
    {id:25336,internalName:'BOULDERDWARF_SM',name:'Boulder Dwarf Swordmaster',level:64,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:3,maps:[{mapId:'nrd_dun02',mapName:'Nordfeld Cave 2F',amount:1}],elementModifiers:{Neutral:100,Water:100,Earth:0,Fire:200,Wind:70,Poison:175,Holy:100,Shadow:100,Ghost:100,Undead:100},drops:[{itemId:300964,name:'Boulder Dwarf Swordmaster Card',rate:null}]}
  ];

  const existingIds=new Set(rows.map(x=>String(x.id)));
  for(const s of special){
    if(existingIds.has(String(s.id))) continue;
    const modes=Array.isArray(s.modes)?s.modes:[];
    rows.push({
      id:String(s.id),clientId:s.id,spriteId:s.id,internalName:s.internalName,name:s.name,aliases:[],
      level:s.level??null,hp:s.hp??null,sp:null,baseExp:null,jobExp:null,race:s.race||'n/a',element:s.element||'n/a',elementLevel:s.elementLevel??null,size:s.size||'n/a',
      attackMin:s.attackMin??null,attackMax:s.attackMax??null,magicAttackMin:s.magicAttackMin??null,magicAttackMax:s.magicAttackMax??null,def:s.def??null,mdef:s.mdef??null,hit:s.hit??null,flee:s.flee??null,
      str:null,agi:null,vit:null,int:null,dex:null,luk:null,walkSpeed:null,attackDelay:null,delayAfterHit:null,attackRange:null,spellRange:null,sightRange:null,
      elementModifiers:s.elementModifiers||{},aggressive:modes.includes('Aggressive')?true:null,boss:Boolean(s.boss),mvp:false,modes,clientBossType:false,clientNavigationType:null,propertyCode:null,
      image:null,description:{en:'',fr:''},drops:Array.isArray(s.drops)?s.drops:[],maps:Array.isArray(s.maps)?s.maps:[],skills:visibleMonsterSkills(s.skills),notes:{en:'',fr:''},
      verified:false,clientVerified:false,fieldMeta:{},zeroOverlayApplied:false,zeroConsensusApplied:false,rmsWalkSpeedApplied:false,specialZeroRecord:true
    });
  }

  rows.sort((a,b)=>String(a.name).localeCompare(String(b.name),'en',{sensitivity:'base'}));
  window.RO_DATA.monsters = rows;
  window.RZ_CLIENT_MONSTERS = rows;
})();
