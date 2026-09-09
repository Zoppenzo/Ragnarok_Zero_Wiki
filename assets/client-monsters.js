(() => {
  'use strict';
  const raw = Array.isArray(window.RZ_CLIENT_MONSTERS_RAW) ? window.RZ_CLIENT_MONSTERS_RAW : [];
  const identity = window.RZ_CLIENT_MONSTER_IDENTITY && typeof window.RZ_CLIENT_MONSTER_IDENTITY === 'object' ? window.RZ_CLIENT_MONSTER_IDENTITY : {};
  const aliases = window.RZ_CLIENT_MONSTER_ALIASES && typeof window.RZ_CLIENT_MONSTER_ALIASES === 'object' ? window.RZ_CLIENT_MONSTER_ALIASES : {};
  const zeroStats = window.RZ_MONSTER_ZERO_STATS && typeof window.RZ_MONSTER_ZERO_STATS === 'object' ? window.RZ_MONSTER_ZERO_STATS : {};
  const rmsBehavior = window.RZ_MONSTER_RMS_BEHAVIOR && typeof window.RZ_MONSTER_RMS_BEHAVIOR === 'object' ? window.RZ_MONSTER_RMS_BEHAVIOR : {};
  if (!window.RO_DATA || !Object.keys(identity).length) return;

  const races = ['Formless','Undead','Brute','Plant','Insect','Fish','Demon','Demi-Human','Angel','Dragon'];
  const sizes = ['Small','Medium','Large'];
  const elements = ['Neutral','Water','Earth','Fire','Wind','Poison','Holy','Shadow','Ghost','Undead'];
  const labels = Array.isArray(window.RZ_CLIENT_MONSTER_MAP_LABELS) ? window.RZ_CLIENT_MONSTER_MAP_LABELS : [];
  const mapIndex = window.RZ_CLIENT_MONSTER_MAP_INDEX || {};

  // Category tags only. These sets do not import HP/EXP/ATK/drop values.
  // MVP and Boss are intentionally exclusive in the UI: Boss means a
  // boss-class/miniboss that is not tagged MVP.
  const MVP_IDS = new Set([1038,1039,1046,1086,1087,1112,1115,1147,1150,1157,1159,1190,1251,1252,1272,1312,1373,1389,1418,1492,1511,1583,1630,1688]);
  const BOSS_IDS = new Set([1089,1090,1091,1092,1093,1096,1120,1262,1283,1295,1302,1582]);

  // Decoded directly from the Zero Global client navigation files:
  // Navi_Mob_data.lub + Navi_Mob_enUS.lub. Navigation type 301 marks
  // boss-type/special monster entries; type 300 is the normal entry type.
  // This is NOT a bitmask for Aggressive/Looter/Assist/etc.
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

  const pretty = value => displayNames[value] || String(value || '').replace(/^C[12]_/, '').replace(/_{1,2}\d+$/, '').replace(/_+/g, ' ').toLowerCase().replace(/\b\w/g, c => c.toUpperCase());
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
    const behavior=rmsBehavior[String(id)] || {};
    const isMvp=MVP_IDS.has(id);
    const isBoss=!isMvp && BOSS_IDS.has(id);
    const hasNavigation=mapsByKey.has(internal);
    const clientBossType=CLIENT_NAV_BOSS_TYPES.has(internal);
    const clientNavigationType=clientBossType?301:(hasNavigation?300:null);
    const modes=clientNavigationType===301?['Boss Type']:(clientNavigationType===300?['Normal Type']:[]);
    rows.push({
      id:String(id), clientId:id, spriteId:id, internalName:internal, name:pretty(internal), aliases:[],
      level:Number.isFinite(level)?level:null, hp:overlay.hp??null, sp:null, baseExp:overlay.baseExp??null, jobExp:overlay.jobExp??null,
      race:races[raceCode] || 'n/a', element:elements[elementIndex] || 'n/a', elementLevel:elementLevel || null,
      size:sizes[sizeCode] || 'n/a', attackMin:null, attackMax:null, def:overlay.def??null, mdef:overlay.mdef??null, hit:null, flee:null,
      walkSpeed:behavior.walkSpeed??null, attackDelay:null, delayAfterHit:behavior.delayAfterHit??null,
      attackRange:behavior.attackRange??null, spellRange:behavior.spellRange??null, sightRange:behavior.sightRange??null,
      elementModifiers:overlay.elementModifiers&&typeof overlay.elementModifiers==='object'?overlay.elementModifiers:{},
      aggressive:null, boss:isBoss, mvp:isMvp, modes, clientBossType, clientNavigationType,
      propertyCode:Number.isFinite(propertyCode)?propertyCode:null,
      image:null, description:{en:'',fr:''}, drops:[], maps, skills:[], notes:{en:'',fr:''}, verified:false, clientVerified:true,
      zeroOverlayApplied:Object.keys(overlay).length>0,
      rmsBehaviorApplied:Object.keys(behavior).length>0
    });
  }

  rows.sort((a,b)=>String(a.name).localeCompare(String(b.name),'en',{sensitivity:'base'}));
  window.RO_DATA.monsters = rows;
  window.RZ_CLIENT_MONSTERS = rows;
})();
