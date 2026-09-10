// Conservative workflow classification for sprite-backed client identities.
// This file does not hide or delete anything. It only prevents known quest/event/
// technical variants from being treated as ordinary world monsters in data audits.
window.RZ_MONSTER_ROSTER_CLASSIFICATION_OVERRIDES={
  "2414":{
    category:"quest",
    internalName:"RUNAWAY_BOOK",
    reason:"Rebirth quest target; not an ordinary world-grinding monster"
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
  "20425":{
    category:"variant",
    internalName:"PHREEONI2",
    reason:"Alternate MVP identity in the BACSOJIN2 / MOONLIGHT2 / PHREEONI2 family"
  },
  "2288":{
    category:"special",
    internalName:"GLD_TREASURE",
    reason:"Guild/WoE treasure entity rather than an ordinary world monster"
  }
};
