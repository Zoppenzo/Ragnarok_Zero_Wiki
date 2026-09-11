(() => {
  'use strict';

  // Metadata-only rows recovered from the supplied current Ragnarok Zero client
  // Navigation tables. These monsters are not present in the map-filtered Navi
  // export, but the client still provides Level / Race / Size / Property.
  // Row format: [Mob-ID, Level, RaceCode, SizeCode, PropertyCode].
  const rows = {
    BOULDERDWARF_HAMMER_MJ: [25327, 64, 7, 1, 42],
    BOULDERDWARF_MACE_MJ:   [25328, 65, 7, 1, 42],
    BOULDERDWARF_LEADER_MJ: [25329, 64, 7, 1, 62],
    BOULDERDWARF_SM:        [25336, 64, 7, 1, 62]
  };

  const identity = window.RZ_CLIENT_MONSTER_IDENTITY && typeof window.RZ_CLIENT_MONSTER_IDENTITY === 'object'
    ? window.RZ_CLIENT_MONSTER_IDENTITY
    : (window.RZ_CLIENT_MONSTER_IDENTITY = {});

  for (const [internalName, row] of Object.entries(rows)) {
    const current = identity[internalName];
    if (Array.isArray(current)) {
      if (Number(current[0]) !== Number(row[0])) {
        console.error(`[RZ client Navi metadata] Mob-ID mismatch for ${internalName}: ${current[0]} != ${row[0]}`);
      }
      continue;
    }
    identity[internalName] = [...row];
  }

  window.RZ_CLIENT_MONSTER_NAV_METADATA = Object.freeze(rows);
})();
