(() => {
  'use strict';

  const rows = window.RO_DATA?.monsters;
  const roster = Array.isArray(window.RZ_CLIENT_MONSTER_ROSTER) ? window.RZ_CLIENT_MONSTER_ROSTER : [];
  const nav = window.RZ_CLIENT_MONSTER_NAV_CURRENT && typeof window.RZ_CLIENT_MONSTER_NAV_CURRENT === 'object'
    ? window.RZ_CLIENT_MONSTER_NAV_CURRENT : {};
  const zeroStats = window.RZ_MONSTER_ZERO_STATS && typeof window.RZ_MONSTER_ZERO_STATS === 'object'
    ? window.RZ_MONSTER_ZERO_STATS : {};
  const zeroConsensus = window.RZ_MONSTER_ZERO_CONSENSUS && typeof window.RZ_MONSTER_ZERO_CONSENSUS === 'object'
    ? window.RZ_MONSTER_ZERO_CONSENSUS : {};
  const rmsBehavior = window.RZ_MONSTER_RMS_BEHAVIOR && typeof window.RZ_MONSTER_RMS_BEHAVIOR === 'object'
    ? window.RZ_MONSTER_RMS_BEHAVIOR : {};
  if (!Array.isArray(rows) || !roster.length) return;

  const races = ['Formless','Undead','Brute','Plant','Insect','Fish','Demon','Demi-Human','Angel','Dragon'];
  const sizes = ['Small','Medium','Large'];
  const elements = ['Neutral','Water','Earth','Fire','Wind','Poison','Holy','Shadow','Ghost','Undead'];

  const MVP_IDS = new Set([1038,1039,1046,1086,1087,1112,1115,1147,1150,1157,1159,1190,1251,1252,1272,1312,1373,1389,1418,1492,1511,1583,1630,1688]);
  const BOSS_IDS = new Set([1089,1090,1091,1092,1093,1096,1120,1262,1283,1295,1302,1582]);

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

  const mapLabels = Array.isArray(window.RZ_CLIENT_MONSTER_MAP_LABELS) ? window.RZ_CLIENT_MONSTER_MAP_LABELS : [];
  const mapIndex = window.RZ_CLIENT_MONSTER_MAP_INDEX && typeof window.RZ_CLIENT_MONSTER_MAP_INDEX === 'object'
    ? window.RZ_CLIENT_MONSTER_MAP_INDEX : {};
  const wikiMaps = Array.isArray(window.RO_DATA?.maps) ? window.RO_DATA.maps : [];

  const displayNames = {
    FARMILIAR:'Familiar',
    KNIGHT_OF_ABYSS:'Abysmal Knight',
    C_TOWER_MANAGER:'Tower Keeper',
    KNIGHT_OF_WINDSTORM:'Stormy Knight',
    ORK_HERO:'Orc Hero',
    ORK_WARRIOR:'Orc Warrior',
    SWORD_FISH:'Swordfish',
    NERAID:'Nereid',
    GIANT_HONET:'Giant Hornet'
  };

  function pretty(internal) {
    if (displayNames[internal]) return displayNames[internal];
    return String(internal || '')
      .replace(/^JT_/,'')
      .replace(/^MD_/,'')
      .replace(/^MQ_/,'')
      .replace(/_+/g,' ')
      .trim()
      .toLowerCase()
      .replace(/\b\w/g,c=>c.toUpperCase());
  }

  function labelMap(mapId) {
    const direct = wikiMaps.find(m => String(m?.internalName || '') === mapId || String(m?.id || '') === mapId);
    if (direct?.name) return direct.name;
    const idx = mapIndex[mapId];
    if (Number.isInteger(idx) && mapLabels[idx]) return mapLabels[idx];
    return mapId;
  }

  function missingValue(value) {
    return value === null || value === undefined || value === '' || /^n\/?a$/i.test(String(value).trim()) || String(value).trim() === '—';
  }

  function fill(monster, key, value) {
    if (missingValue(monster[key]) && !missingValue(value)) monster[key] = value;
  }

  function normalizeMonsterSkills(skills) {
    const seen = new Set();
    return (Array.isArray(skills) ? skills : []).filter(skill => {
      const internal = String(skill?.internalName || skill?.name || skill?.skill || '').trim().toUpperCase();
      if (!internal || internal === 'NPC_EMOTION' || internal === 'NPC_EMOTION_ON') return false;
      const key = `${internal}|${skill?.level ?? ''}|${skill?.rate ?? ''}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    }).map(skill => {
      const internal = String(skill?.internalName || skill?.name || skill?.skill || '').trim();
      const clientName = clientNpcSkillNames[internal];
      return clientName ? {...skill, internalName:internal, name:clientName, clientNameVerified:true} : skill;
    });
  }

  function enrichWithVerifiedSources(monster, id) {
    const overlay = zeroStats[String(id)] || {};
    const consensus = zeroConsensus[String(id)] || {};
    const fields = consensus.fields && typeof consensus.fields === 'object' ? consensus.fields : {};
    const fv = key => fields[key]?.value ?? null;
    const rms = rmsBehavior[String(id)] || {};

    // Match client-monsters.js precedence. Existing values always win; this
    // primarily enriches the 308 roster identities inserted after that builder.
    fill(monster, 'hp', overlay.hp ?? fv('hp'));
    fill(monster, 'baseExp', overlay.baseExp ?? fv('baseExp'));
    fill(monster, 'jobExp', overlay.jobExp ?? fv('jobExp'));
    fill(monster, 'attackMin', fv('attackMin'));
    fill(monster, 'attackMax', fv('attackMax'));
    fill(monster, 'magicAttackMin', fv('magicAttackMin'));
    fill(monster, 'magicAttackMax', fv('magicAttackMax'));
    fill(monster, 'def', overlay.def ?? fv('def'));
    fill(monster, 'mdef', overlay.mdef ?? fv('mdef'));
    fill(monster, 'hit', fv('hit'));
    fill(monster, 'flee', fv('flee'));
    fill(monster, 'walkSpeed', rms.walkSpeed);

    if ((!monster.elementModifiers || !Object.keys(monster.elementModifiers).length) && overlay.elementModifiers && typeof overlay.elementModifiers === 'object') {
      monster.elementModifiers = {...overlay.elementModifiers};
    }
    if ((!Array.isArray(monster.drops) || !monster.drops.length) && Array.isArray(consensus.drops) && consensus.drops.length) {
      monster.drops = consensus.drops.map(drop => ({...drop}));
    }
    if ((!Array.isArray(monster.skills) || !monster.skills.length) && Array.isArray(consensus.skills) && consensus.skills.length) {
      monster.skills = normalizeMonsterSkills(consensus.skills);
    }

    const modes = Array.isArray(monster.modes) ? [...monster.modes] : [];
    for (const mode of (Array.isArray(consensus.modes) ? consensus.modes : [])) {
      const value = String(mode || '').trim();
      if (value && !modes.includes(value)) modes.push(value);
    }
    monster.modes = modes;
    if (monster.aggressive == null && modes.includes('Aggressive')) monster.aggressive = true;

    if (MVP_IDS.has(id)) {
      monster.mvp = true;
      monster.boss = false;
    } else if (BOSS_IDS.has(id)) {
      monster.boss = true;
    }

    monster.fieldMeta = {...(monster.fieldMeta || {}), ...fields};
    monster.zeroOverlayApplied = Boolean(monster.zeroOverlayApplied || Object.keys(overlay).length);
    monster.zeroConsensusApplied = Boolean(monster.zeroConsensusApplied || Object.keys(consensus).length);
    monster.rmsWalkSpeedApplied = Boolean(monster.rmsWalkSpeedApplied || rms.walkSpeed);
  }

  function baseMonster(id, internal, spriteKey) {
    return {
      id:String(id), clientId:id, spriteId:id, internalName:internal, name:pretty(internal), aliases:[],
      level:null, hp:null, sp:null, baseExp:null, jobExp:null,
      race:null, element:null, elementLevel:null, size:null,
      attackMin:null, attackMax:null, magicAttackMin:null, magicAttackMax:null,
      def:null, mdef:null, hit:null, flee:null,
      str:null, agi:null, vit:null, int:null, dex:null, luk:null, walkSpeed:null,
      attackDelay:null, delayAfterHit:null, attackRange:null, spellRange:null, sightRange:null,
      elementModifiers:{}, aggressive:null, boss:false, mvp:false, modes:[],
      clientBossType:false, clientNavigationType:null, propertyCode:null,
      image:null, description:{en:'',fr:''}, drops:[], maps:[], skills:[],
      notes:{en:'',fr:''}, verified:false, clientVerified:true, fieldMeta:{},
      memorial:/^MD_/.test(internal), clientSpriteKey:spriteKey
    };
  }

  const byId = new Map();
  for (const monster of rows) {
    const id = Number(monster?.clientId ?? monster?.id);
    if (Number.isFinite(id) && !byId.has(id)) byId.set(id, monster);
  }

  const rosterIdCounts = new Map();
  for (const entry of roster) {
    const id = Number(entry?.[0]);
    if (Number.isFinite(id)) rosterIdCounts.set(id, (rosterIdCounts.get(id) || 0) + 1);
  }

  let inserted = 0;
  let navApplied = 0;
  let navMissing = 0;
  let legacyNumericIdMismatch = 0;
  let sourceEnriched = 0;

  for (const entry of roster) {
    if (!Array.isArray(entry) || entry.length < 3) continue;
    const id = Number(entry[0]);
    const internal = String(entry[1] || '').trim();
    const spriteKey = String(entry[2] || '').trim();
    if (!Number.isFinite(id) || !internal) continue;

    let monster = byId.get(id);
    if (!monster) {
      monster = baseMonster(id, internal, spriteKey);
      rows.push(monster);
      byId.set(id, monster);
      inserted += 1;
    }

    // NPCIdentity + JobName + the actual SPR roster is the authoritative Mob-ID
    // and internal-identity layer.
    monster.clientRosterPresent = true;
    monster.clientIdentityVerified = true;
    monster.clientSpriteVerified = true;
    monster.clientVerified = true;
    monster.clientId = id;
    monster.spriteId = id;
    monster.internalName = internal;
    monster.clientSpriteKey = spriteKey || internal;
    if (!monster.name) monster.name = pretty(internal);
    if (/^MD_/.test(internal)) monster.memorial = true;

    // IMPORTANT: the first numeric field in the Navi row is NOT a reliable
    // current Mob-ID. The only valid join key is the exact internal identity.
    const current = nav[internal];

    if (Array.isArray(current) && current.length >= 7) {
      const [legacyNumericId,level,raceCode,sizeCode,propertyCode,type,rawMaps] = current;
      if (Number.isFinite(Number(legacyNumericId)) && Number(legacyNumericId) !== id) {
        legacyNumericIdMismatch += 1;
      }

      const elementIndex = ((Number(propertyCode) % 20) + 20) % 20;
      const elementLevel = Math.floor(Number(propertyCode) / 20);
      const navType = Number(type) || null;

      monster.level = Number.isFinite(Number(level)) ? Number(level) : monster.level;
      monster.race = races[Number(raceCode)] || monster.race || null;
      monster.size = sizes[Number(sizeCode)] || monster.size || null;
      monster.element = elements[elementIndex] || monster.element || null;
      monster.elementLevel = elementLevel > 0 ? elementLevel : monster.elementLevel;
      monster.propertyCode = Number.isFinite(Number(propertyCode)) ? Number(propertyCode) : monster.propertyCode;
      monster.clientNavigationType = navType;
      monster.clientBossType = navType === 301;

      const modes = (Array.isArray(monster.modes) ? monster.modes : [])
        .filter(mode => mode !== 'Normal Type' && mode !== 'Boss Type');
      if (navType === 301) modes.unshift('Boss Type');
      else if (navType === 300) modes.unshift('Normal Type');
      monster.modes = modes;

      // Exact internal-name join. Never join these maps through the legacy
      // numeric field above.
      monster.maps = (Array.isArray(rawMaps) ? rawMaps : []).map(pair => {
        const mapId = String(pair?.[0] || '').trim();
        const amount = Number(pair?.[1]);
        return {
          mapId,
          mapName:labelMap(mapId),
          amount:Number.isFinite(amount) && amount > 0 ? amount : null,
          respawn:null,
          verified:true,
          clientVerified:true,
          source:'client-navigation-current'
        };
      }).filter(m => m.mapId);

      monster.clientNavigationRecovered = true;
      monster.clientNavigationCurrent = true;
      navApplied += 1;
    } else {
      // No current Navi entry for this exact client identity. Never fall back to
      // the obsolete pseudo-ID map table. Preserve only maps supplied by another
      // explicit Zero/screenshot/Memorial source.
      monster.maps = (Array.isArray(monster.maps) ? monster.maps : []).filter(m => {
        if (m?.source === 'client-navigation' || m?.source === 'client-navigation-legacy') return false;
        return !(m?.clientVerified === true && m?.verified === true && !m?.source);
      });
      monster.clientNavigationRecovered = false;
      monster.clientNavigationCurrent = false;
      navMissing += 1;
    }

    const before = [monster.hp,monster.attackMin,monster.magicAttackMin,monster.def,monster.mdef,monster.hit,monster.flee,monster.baseExp,monster.jobExp,monster.walkSpeed,monster.drops?.length,monster.skills?.length].join('|');
    enrichWithVerifiedSources(monster, id);
    const after = [monster.hp,monster.attackMin,monster.magicAttackMin,monster.def,monster.mdef,monster.hit,monster.flee,monster.baseExp,monster.jobExp,monster.walkSpeed,monster.drops?.length,monster.skills?.length].join('|');
    if (before !== after) sourceEnriched += 1;
  }

  // Absolute safety net: obsolete automatic map positions can never survive.
  for (const monster of rows) {
    monster.maps = (Array.isArray(monster.maps) ? monster.maps : []).filter(m =>
      m?.source !== 'client-navigation' && m?.source !== 'client-navigation-legacy'
    );
  }

  const duplicateRosterIds = [...rosterIdCounts.entries()].filter(([,count]) => count > 1).map(([id,count]) => ({id,count}));
  const rosterMissingFromRuntime = roster.filter(entry => !byId.has(Number(entry?.[0]))).map(entry => Number(entry?.[0])).filter(Number.isFinite);
  const legacyMapsRemaining = rows.reduce((count, monster) => count + (Array.isArray(monster.maps) ? monster.maps.filter(m =>
    m?.source === 'client-navigation' || m?.source === 'client-navigation-legacy'
  ).length : 0), 0);

  rows.sort((a,b)=>String(a.name||a.internalName||'').localeCompare(String(b.name||b.internalName||''),'en',{sensitivity:'base'}));
  window.RZ_CLIENT_MONSTERS = rows;
  window.RZ_CLIENT_MONSTER_CURRENT_AUDIT = {
    rosterCount:roster.length,
    uniqueRosterIds:rosterIdCounts.size,
    duplicateRosterIds,
    inserted,
    sourceEnriched,
    currentNavigationEntries:Object.keys(nav).length,
    currentNavigationApplied:navApplied,
    currentNavigationMissing:navMissing,
    legacyNumericIdMismatch,
    rosterMissingFromRuntime,
    legacyMapsRemaining,
    legacyMapsDisabled:window.RZ_CLIENT_MONSTER_LEGACY_MAPS_DISABLED === true
  };
})();
