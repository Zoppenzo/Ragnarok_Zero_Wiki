(() => {
  'use strict';

  // Strict wiki policy (2026-09-11): monster -> skill associations and explicit
  // zero-skill claims are displayed only after at least two independent
  // Ragnarok Zero databases confirm the same information. The previous
  // single-source candidates are intentionally not applied to runtime data.
  const associations={};
  const verifiedEmpty={};

  window.RZ_MONSTER_VERIFIED_SKILL_ASSOCIATIONS=associations;
  window.RZ_MONSTER_VERIFIED_SKILL_EMPTY=verifiedEmpty;
  window.RZ_MONSTER_SKILL_VERIFICATION_POLICY={
    policy:'two-independent-zero-databases-required',
    unknownDisplay:'???'
  };
})();
