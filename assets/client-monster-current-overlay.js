(() => {
  'use strict';

  const rows = window.RO_DATA?.monsters;
  const roster = Array.isArray(window.RZ_CLIENT_MONSTER_ROSTER) ? window.RZ_CLIENT_MONSTER_ROSTER : [];
  const nav = window.RZ_CLIENT_MONSTER_NAV_CURRENT && typeof window.RZ_CLIENT_MONSTER_NAV_CURRENT === 'object'
    ? window.RZ_CLIENT_MONSTER_NAV_CURRENT : {};
  if (!Array.isArray(rows) || !roster.length) return;

  const races = ['Formless','Undead','Brute','Plant','Insect','Fish','Demon','Demi-Human','Angel','Dragon'];
  const sizes = ['Small','Medium','Large'];
  const elements = ['Neutral','Water','Earth','Fire','Wind','Poison','Holy','Shadow','Ghost','Undead'];

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
    currentNavigationEntries:Object.keys(nav).length,
    currentNavigationApplied:navApplied,
    currentNavigationMissing:navMissing,
    legacyNumericIdMismatch,
    rosterMissingFromRuntime,
    legacyMapsRemaining,
    legacyMapsDisabled:window.RZ_CLIENT_MONSTER_LEGACY_MAPS_DISABLED === true
  };
})();
