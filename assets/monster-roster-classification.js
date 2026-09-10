// Conservative workflow classification for sprite-backed client identities.
// This file does not hide or delete anything. It only prevents known quest/event/
// technical, duplicate, or not-yet-released identities from being treated as
// ordinary current-world monsters in data audits.
window.RZ_MONSTER_ROSTER_CLASSIFICATION_OVERRIDES={
  "1185":{
    category:"variant",
    internalName:"WHISPER_",
    reason:"Alternate/duplicate Whisper identity (trailing-underscore internal name), kept in the client roster but not treated as a separate ordinary world monster"
  },
  "1250":{
    category:"normal",
    internalName:"CHEPET",
    reason:"Ordinary monster identity retained as normal; current Global combat/spawn values remain unverified"
  },
  "1840":{
    category:"event",
    internalName:"GOLDEN_SAVAGE",
    reason:"Event-monster identity"
  },
  "2248":{
    category:"event",
    internalName:"GOLDPORING",
    reason:"Legacy Golden Poring identity; current ROZ Global Gold Poring uses a different Mob-ID"
  },
  "2288":{
    category:"special",
    internalName:"GLD_TREASURE",
    reason:"Guild/WoE treasure entity rather than an ordinary world monster"
  },
  "2414":{
    category:"quest",
    internalName:"RUNAWAY_BOOK",
    reason:"Rebirth quest target; not an ordinary world-grinding monster"
  },
  "20175":{
    category:"upcoming",
    internalName:"EXTRA_JOKER",
    reason:"Marked UPCOMING for the October 2026 Global Clock Tower Dungeon update; not current world content as of 2026-09-10"
  },
  "20176":{
    category:"upcoming",
    internalName:"ERZSEBET",
    reason:"Marked UPCOMING for the October 2026 Global Clock Tower Dungeon update; not current world content as of 2026-09-10"
  },
  "20177":{
    category:"upcoming",
    internalName:"JENIFFER",
    reason:"Marked UPCOMING for the October 2026 Global Clock Tower Dungeon update; not current world content as of 2026-09-10"
  },
  "20178":{
    category:"upcoming",
    internalName:"GENERAL_ORC",
    reason:"Marked UPCOMING for the October 2026 Global Clock Tower Dungeon update; not current world content as of 2026-09-10"
  },
  "20179":{
    category:"upcoming",
    internalName:"SIEGLOUSE",
    reason:"Marked UPCOMING for the October 2026 Global Clock Tower Dungeon update; not current world content as of 2026-09-10"
  },
  "20425":{
    category:"variant",
    internalName:"PHREEONI2",
    reason:"Alternate MVP identity in the BACSOJIN2 / MOONLIGHT2 / PHREEONI2 family"
  }
};
