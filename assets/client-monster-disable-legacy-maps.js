(() => {
  'use strict';

  // RZ_CLIENT_MONSTERS_RAW comes from the obsolete Navi extraction whose first
  // numeric field was once mistaken for the current Mob-ID. Keep the rows only
  // for non-map compatibility, but make it impossible for those positions to
  // enter the runtime monster database.
  const raw = Array.isArray(window.RZ_CLIENT_MONSTERS_RAW) ? window.RZ_CLIENT_MONSTERS_RAW : [];
  let clearedRows = 0;
  let clearedMapPairs = 0;

  for (const row of raw) {
    if (!Array.isArray(row) || row.length < 7) continue;
    if (Array.isArray(row[6]) && row[6].length) {
      clearedMapPairs += row[6].length;
      clearedRows += 1;
    }
    row[6] = [];
  }

  window.RZ_CLIENT_MONSTER_LEGACY_MAPS_DISABLED = true;
  window.RZ_CLIENT_MONSTER_LEGACY_MAP_AUDIT = {
    rows: raw.length,
    clearedRows,
    clearedMapPairs
  };
})();
