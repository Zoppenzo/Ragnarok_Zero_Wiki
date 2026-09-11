(() => {
  'use strict';

  const consensus = window.RZ_MONSTER_ZERO_CONSENSUS && typeof window.RZ_MONSTER_ZERO_CONSENSUS === 'object'
    ? window.RZ_MONSTER_ZERO_CONSENSUS : {};
  const identity = window.RZ_CLIENT_MONSTER_IDENTITY && typeof window.RZ_CLIENT_MONSTER_IDENTITY === 'object'
    ? window.RZ_CLIENT_MONSTER_IDENTITY : {};
  const monsters = Array.isArray(window.RO_DATA?.monsters) ? window.RO_DATA.monsters : [];
  const races = ['Formless','Undead','Brute','Plant','Insect','Fish','Demon','Demi-Human','Angel','Dragon'];
  const sizes = ['Small','Medium','Large'];
  const elements = ['Neutral','Water','Earth','Fire','Wind','Poison','Holy','Shadow','Ghost','Undead'];

  const fieldMap = {
    hp:'hp', baseExp:'baseExp', jobExp:'jobExp',
    attackMin:'attackMin', attackMax:'attackMax',
    magicAttackMin:'magicAttackMin', magicAttackMax:'magicAttackMax',
    def:'def', mdef:'mdef', hit:'hit', flee:'flee'
  };
  const value = (fields, key) => Object.prototype.hasOwnProperty.call(fields, key) ? fields[key]?.value ?? null : null;

  for (const monster of monsters) {
    const id = Number(monster?.clientId ?? monster?.id);
    const key = String(id);
    const internal = String(monster?.internalName || '');
    const record = consensus[key] || {};
    const fields = record.fields && typeof record.fields === 'object' ? record.fields : {};

    // Identity fields may stay only when the supplied current client proves the
    // exact internal-name -> Mob-ID relation. This protects special/manual rows
    // from carrying server data as if it came from the client.
    const clientIdentity = identity[internal];
    const exactClientIdentity = Array.isArray(clientIdentity) && Number(clientIdentity[0]) === id;
    if (exactClientIdentity) {
      const [, level, raceCode, sizeCode, propertyCode] = clientIdentity.map(Number);
      const elementIndex = ((propertyCode % 20) + 20) % 20;
      monster.level = Number.isFinite(level) ? level : null;
      monster.race = races[raceCode] || 'n/a';
      monster.size = sizes[sizeCode] || 'n/a';
      monster.element = elements[elementIndex] || 'n/a';
      monster.elementLevel = Number.isFinite(propertyCode) ? Math.floor(propertyCode / 20) || null : null;
      monster.propertyCode = Number.isFinite(propertyCode) ? propertyCode : null;
      monster.clientVerified = true;
    } else {
      monster.level = null;
      monster.race = 'n/a';
      monster.size = 'n/a';
      monster.element = 'n/a';
      monster.elementLevel = null;
      monster.propertyCode = null;
      monster.clientVerified = false;
    }

    // All server-side combat/EXP values are rebuilt strictly from the filtered
    // two-source Zero consensus. Any old single-source overlay or manual value is
    // erased instead of being allowed to survive as a fallback.
    for (const [prop, field] of Object.entries(fieldMap)) {
      monster[prop] = value(fields, field);
    }
    monster.sp = null;
    monster.str = null; monster.agi = null; monster.vit = null;
    monster.int = null; monster.dex = null; monster.luk = null;

    const speedMs = value(fields, 'moveSpeedMs');
    monster.walkSpeed = speedMs == null ? null : `${speedMs} ms`;
    monster.attackDelay = null;
    monster.delayAfterHit = null;
    monster.attackRange = null;
    monster.spellRange = null;
    monster.sightRange = null;

    // Current-client exact Navi is authoritative for maps. All external
    // one-source spawn fallbacks are removed until a second Zero DB confirms them.
    monster.maps = (Array.isArray(monster.maps) ? monster.maps : []).filter(map =>
      map?.clientVerified === true || String(map?.source || '') === 'client-navigation-current'
    );

    // Drops are already filtered to two-source relation consensus by the strict
    // builder. A conflicting/missing rate remains null -> ??? while the verified
    // monster->item relation can still be shown.
    monster.drops = Array.isArray(record.drops) ? record.drops.map(drop => ({...drop})) : [];

    // No monster->skill mapping currently has two independent Zero DB proofs in
    // the generated consensus. Single-source associations are intentionally hidden.
    monster.skills = Array.isArray(record.skills) ? record.skills.map(skill => ({...skill})) : [];
    monster.skillsVerifiedEmpty = false;
    monster.skillsVerificationSource = null;
    monster.skillAiCount = null;

    // Only client Navi classification and future strict-consensus modes survive.
    const modes = [];
    if (monster.clientNavigationType === 301) modes.push('Boss Type');
    else if (monster.clientNavigationType === 300) modes.push('Normal Type');
    for (const mode of (Array.isArray(record.modes) ? record.modes : [])) {
      const clean = String(mode || '').trim();
      if (clean && !modes.includes(clean)) modes.push(clean);
    }
    monster.modes = modes;
    monster.aggressive = modes.includes('Aggressive') ? true : null;

    monster.fieldMeta = fields;
    monster.elementModifiers = {};
    monster.zeroOverlayApplied = false;
    monster.zeroConsensusApplied = Boolean(Object.keys(fields).length || monster.drops.length || monster.skills.length);
    monster.rmsWalkSpeedApplied = false;
    monster.strictVerificationApplied = true;
  }

  window.RZ_MONSTER_STRICT_POLICY = {
    client:'Exact current-client identity/property and current Navi are accepted.',
    external:'Server values and drop relations require agreement from at least two independent Ragnarok Zero databases.',
    unknown:'Anything not meeting those rules is displayed as ???.'
  };
})();
