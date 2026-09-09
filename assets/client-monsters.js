(() => {
  'use strict';
  const raw = Array.isArray(window.RZ_CLIENT_MONSTERS_RAW) ? window.RZ_CLIENT_MONSTERS_RAW : [];
  const identity = window.RZ_CLIENT_MONSTER_IDENTITY && typeof window.RZ_CLIENT_MONSTER_IDENTITY === 'object' ? window.RZ_CLIENT_MONSTER_IDENTITY : {};
  const aliases = window.RZ_CLIENT_MONSTER_ALIASES && typeof window.RZ_CLIENT_MONSTER_ALIASES === 'object' ? window.RZ_CLIENT_MONSTER_ALIASES : {};
  if (!window.RO_DATA || !Object.keys(identity).length) return;

  const races = ['Formless','Undead','Brute','Plant','Insect','Fish','Demon','Demi-Human','Angel','Dragon'];
  const sizes = ['Small','Medium','Large'];
  const elements = ['Neutral','Water','Earth','Fire','Wind','Poison','Holy','Shadow','Ghost','Undead'];
  const labels = Array.isArray(window.RZ_CLIENT_MONSTER_MAP_LABELS) ? window.RZ_CLIENT_MONSTER_MAP_LABELS : [];
  const mapIndex = window.RZ_CLIENT_MONSTER_MAP_INDEX || {};
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
    rows.push({
      id:String(id), clientId:id, spriteId:id, internalName:internal, name:pretty(internal), aliases:[],
      level:Number.isFinite(level)?level:null, hp:null, sp:null, baseExp:null, jobExp:null,
      race:races[raceCode] || 'n/a', element:elements[elementIndex] || 'n/a', elementLevel:elementLevel || null,
      size:sizes[sizeCode] || 'n/a', attackMin:null, attackMax:null, def:null, mdef:null, hit:null, flee:null,
      aggressive:null, boss:null, mvp:null, propertyCode:Number.isFinite(propertyCode)?propertyCode:null,
      image:null, description:{en:'',fr:''}, drops:[], maps, skills:[], notes:{en:'',fr:''}, verified:false, clientVerified:true
    });
  }

  rows.sort((a,b)=>String(a.name).localeCompare(String(b.name),'en',{sensitivity:'base'}));
  window.RO_DATA.monsters = rows;
  window.RZ_CLIENT_MONSTERS = rows;
})();
