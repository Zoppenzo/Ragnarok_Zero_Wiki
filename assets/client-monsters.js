(() => {
  'use strict';
  const raw = Array.isArray(window.RZ_CLIENT_MONSTERS_RAW) ? window.RZ_CLIENT_MONSTERS_RAW : [];
  if (!window.RO_DATA || !raw.length) return;

  const races = ['Formless','Undead','Brute','Plant','Insect','Fish','Demon','Demi-Human','Angel','Dragon'];
  const sizes = ['Small','Medium','Large'];
  const labels = Array.isArray(window.RZ_CLIENT_MONSTER_MAP_LABELS) ? window.RZ_CLIENT_MONSTER_MAP_LABELS : [];
  const mapIndex = window.RZ_CLIENT_MONSTER_MAP_INDEX || {};

  const pretty = value => String(value || '')
    .replace(/^C[12]_/, '')
    .replace(/_{1,2}\d+$/, '')
    .replace(/_+/g, ' ')
    .toLowerCase()
    .replace(/\b\w/g, c => c.toUpperCase());

  const canonicalKey = internal => String(internal || '')
    .replace(/^C[12]_/, '')
    .replace(/_{1,2}\d+$/, '')
    .replace(/_+$/, '');

  const seen = new Set();
  const rows = [];
  for (const r of raw) {
    const [id, internal, level, raceCode, sizeCode, flags, rawMaps] = r;
    if (!Number.isFinite(Number(id)) || !internal) continue;
    if (/^C[12]_/.test(internal)) continue;
    const key = canonicalKey(internal);
    if (seen.has(key)) continue;
    seen.add(key);

    const maps = (Array.isArray(rawMaps) ? rawMaps : []).map(([mapId, amount]) => {
      const idx = mapIndex[mapId];
      return {
        mapId: String(mapId),
        mapName: Number.isInteger(idx) && labels[idx] ? labels[idx] : String(mapId),
        amount: Number(amount) || null,
        respawn: null,
        verified: true,
        clientVerified: true
      };
    });

    rows.push({
      id: String(id),
      clientId: Number(id),
      internalName: String(internal),
      name: pretty(internal),
      aliases: [],
      level: Number.isFinite(Number(level)) ? Number(level) : null,
      hp: null,
      sp: null,
      baseExp: null,
      jobExp: null,
      race: races[Number(raceCode)] || 'n/a',
      element: 'n/a',
      elementLevel: null,
      size: sizes[Number(sizeCode)] || 'n/a',
      attackMin: null,
      attackMax: null,
      def: null,
      mdef: null,
      hit: null,
      flee: null,
      aggressive: null,
      boss: null,
      mvp: null,
      flags: Number(flags) || 0,
      image: null,
      description: {en:'',fr:''},
      drops: [],
      maps,
      skills: [],
      notes: {en:'',fr:''},
      verified: false,
      clientVerified: true
    });
  }

  window.RO_DATA.monsters = rows;
  window.RZ_CLIENT_MONSTERS = rows;
})();
