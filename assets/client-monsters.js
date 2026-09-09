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

  // Display labels extracted from the supplied Ragnarok Zero client
  // SkillID.lub + SkillInfoList_enUS.lub. These do not prove that a monster
  // uses the skill; they only replace external/internal labels when a monster
  // skill entry is already present in the Zero consensus layer.
  const clientNpcSkillNames = {
    NPC_ALLHEAL:'Full Heal',
    NPC_ALL_STAT_DOWN:'All Stats Down',
    NPC_ANTIMAGIC:'Deadzone',
    NPC_ARMORBRAKE:'Armor Break',
    NPC_ARROWSTORM:'Tempestade de Flechas',
    NPC_CLOUD_KILL:'Killing Cloud',
    NPC_COMET:'Comet',
    NPC_CRITICALWOUND:'Critical Wounds',
    NPC_DAMAGE_HEAL:'Convert Damage to Heal',
    NPC_DARKNESSATTACK:'Dark Attribute Attack',
    NPC_DEADLYCURSE2:'Wide Deadly Curse',
    NPC_DEFENDER:'Defender',
    NPC_DRAGONBREATH:"Dragon's Breath",
    NPC_DRAGONFEAR:'Dragon Fear',
    NPC_EARTHQUAKE:'Earthquake',
    NPC_ELECTRICWALK:'Electric Walk',
    NPC_EMOTION:'Emotion',
    NPC_EVILLAND:'Evil Land',
    NPC_EVILLAND2:'Demonic Evil Land',
    NPC_FATALMENACE:'Fatal Menace',
    NPC_FIREATTACK:'Fire Attribute Attack',
    NPC_FIRESTORM:'Fire storm',
    NPC_FIREWALK:'Fire Walk',
    NPC_FLAMECROSS:'Flame cross',
    NPC_GRADUAL_GRAVITY:'Gravity Increase',
    NPC_GROUNDATTACK:'Earth Attribute Attack',
    NPC_GROUNDDRIVE:'Ground Drive',
    NPC_HALLUCINATIONWALK:'Hallucination Walk',
    NPC_HELLJUDGEMENT:"Hell's Judgement",
    NPC_HELLJUDGEMENT2:'Demonic Hell Judgment',
    NPC_HELLPOWER:"Hell's Power",
    NPC_ICEMINE:'Ice mine',
    NPC_IGNITIONBREAK:'Ignition Break',
    NPC_IMMUNE_PROPERTY:'Elemental Immunity',
    NPC_JACKFROST:'Jack Frost',
    NPC_LEASH:'Leash',
    NPC_LEX_AETERNA:'Wide area Lex Aeterna',
    NPC_MAGICMIRROR:'Magic Mirror',
    NPC_MAGMA_ERUPTION:'Lava Flow',
    NPC_MANDRAGORA:'Mandragora Howl',
    NPC_MAXPAIN:'Max Pain',
    NPC_MILLENNIUMSHIELD:'Millenium Shield',
    NPC_MOVE_COORDINATE:'Position Shift',
    NPC_PIERCINGATT:'Piercing Attack',
    NPC_POISON:'Poison',
    NPC_PSYCHIC_WAVE:'Psychic Wave',
    NPC_PULSESTRIKE:'Pulse Strike',
    NPC_RAINOFMETEOR:'Rain of Meteor',
    NPC_RAYOFGENESIS:'Genesis Ray',
    NPC_REVERBERATION:'Reverberation',
    NPC_SLOWCAST:'Slow Cast',
    NPC_SR_CURSEDCIRCLE:'Cursed Circle',
    NPC_STONESKIN:'Stone Skin',
    NPC_SUMMONSLAVE:'Summon Slave',
    NPC_VAMPIRE_GIFT:"Vampire's Gift",
    NPC_VENOMFOG:'Venom fog',
    NPC_WATERATTACK:'Water Attribute Attack',
    NPC_WIDEBLEEDING:'Bloody Party',
    NPC_WIDEBLEEDING2:'Demonic Mass Bleeding',
    NPC_WIDEBODYBURNNING:'Wide area burnning',
    NPC_WIDECOLD:'Wide area freeze',
    NPC_WIDECONFUSE:'Confusion Rule',
    NPC_WIDECONFUSE2:'Demonic Mass Confuse',
    NPC_WIDECURSE:'Cursed Fate',
    NPC_WIDECURSE2:'Demonic Mass Curse',
    NPC_WIDEFREEZE:'Frozen Heart',
    NPC_WIDEFREEZE2:'Demonic Mass Freeze',
    NPC_WIDEFROSTMISTY:'Wide area frost misty',
    NPC_WIDEHEALTHFEAR:'Wide area fear',
    NPC_WIDELEASH:'Wide Leash',
    NPC_WIDESIGHT:'Wide sight',
    NPC_WIDESILENCE:'Bedlam',
    NPC_WIDESILENCE2:'Demonic Mass Silence',
    NPC_WIDESIREN:'Wide area fascination',
    NPC_WIDESLEEP:'Morpheus Slumber',
    NPC_WIDESLEEP2:'Demonic Mass Sleep',
    NPC_WIDESOULDRAIN:'Souless Defeat',
    NPC_WIDESTONE:"Medusa's Stare",
    NPC_WIDESTONE2:'Demonic Mass Stone',
    NPC_WIDESTUN:'Stunning Gaze',
    NPC_WIDESTUN2:'Demonic Mass Stun',
    NPC_WIDESUCK:'Wide bloodsucking',
    NPC_WIDEWEB:'Wide web',
    NPC_WIDE_DEEP_SLEEP:'Wide area deep sleep',
    NPC_WINDATTACK:'Wind Attribute Attack'
  };
  const normalizeMonsterSkill = skill => {
    if (!skill || typeof skill !== 'object') return skill;
    const internal = String(skill.name || skill.skill || '').trim();
    const clientName = clientNpcSkillNames[internal];
    return clientName ? { ...skill, internalName:internal, name:clientName, clientNameVerified:true } : skill;
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
      // Removed from the public sheet: these are not available in the supplied Zero client files.
      str:null, agi:null, vit:null, int:null, dex:null, luk:null,
      // Explicit exception requested by the wiki owner: Walk Speed may use the RMS-compatible reference layer.
      walkSpeed:rms.walkSpeed??null,
      attackDelay:null, delayAfterHit:null, attackRange:null, spellRange:null, sightRange:null,
      elementModifiers:overlay.elementModifiers&&typeof overlay.elementModifiers==='object'?overlay.elementModifiers:{},
      aggressive:modes.includes('Aggressive')?true:null, boss:isBoss, mvp:isMvp, modes, clientBossType, clientNavigationType,
      propertyCode:Number.isFinite(propertyCode)?propertyCode:null,
      image:null, description:{en:'',fr:''}, drops:Array.isArray(consensus.drops)?consensus.drops:[], maps,
      skills:Array.isArray(consensus.skills)?consensus.skills.map(normalizeMonsterSkill):[], notes:{en:'',fr:''},
      verified:false, clientVerified:true, fieldMeta:fields,
      zeroOverlayApplied:Object.keys(overlay).length>0,
      zeroConsensusApplied:Object.keys(consensus).length>0,
      rmsWalkSpeedApplied:Boolean(rms.walkSpeed)
    });
  }

  rows.sort((a,b)=>String(a.name).localeCompare(String(b.name),'en',{sensitivity:'base'}));
  window.RO_DATA.monsters = rows;
  window.RZ_CLIENT_MONSTERS = rows;
})();
