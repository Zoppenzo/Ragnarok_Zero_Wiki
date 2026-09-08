(() => {
  const rows = Array.isArray(window.RZ_CLIENT_ITEMS) ? window.RZ_CLIENT_ITEMS : [];
  if (!window.RO_DATA || !rows.length) return;

  window.RO_DATA.items = rows.map(r => ({
    id: String(r.i),
    clientId: r.i,
    name: r.n,
    type: r.t || 'Item',
    subtype: r.s || 'Miscellaneous',
    description: '',
    effect: '',
    requiredLevel: r.l ?? null,
    weight: r.w ?? null,
    equipmentSlot: r.e || null,
    position: r.p || null,
    slotCount: r.c || 0,
    atk: r.a ?? null,
    matk: r.m ?? null,
    def: r.f ?? null,
    weaponLevel: r.v ?? null,
    element: r.el || null,
    verified: false,
    clientVerified: true,
    notes: ''
  }));
})();
