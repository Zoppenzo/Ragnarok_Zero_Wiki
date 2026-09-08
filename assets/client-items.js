(() => {
  const rows = Array.isArray(window.RZ_CLIENT_ITEMS) ? window.RZ_CLIENT_ITEMS : [];
  if (!window.RO_DATA || !rows.length) return;
  const statRows = Array.isArray(window.RZ_ITEM_STAT_OVERLAY) ? window.RZ_ITEM_STAT_OVERLAY : [];
  const statMap = new Map(statRows.map(x => [Number(x.i), x]));

  window.RO_DATA.items = rows.map(r => {
    const extra = statMap.get(Number(r.i)) || {};
    return {
      id: String(r.i),
      clientId: r.i,
      name: r.n,
      type: r.t || 'Item',
      subtype: r.s || 'Miscellaneous',
      description: r.d || '',
      effect: '',
      requiredLevel: r.l ?? null,
      weight: r.w ?? null,
      equipmentSlot: r.e || null,
      position: r.p || null,
      slotCount: r.c || 0,
      atk: r.a ?? null,
      matk: r.m ?? extra.matk ?? null,
      def: r.f ?? null,
      mdef: extra.mdef ?? null,
      sellPrice: r.sp ?? null,
      weaponLevel: r.v ?? null,
      element: r.el || null,
      verified: false,
      clientVerified: true,
      notes: ''
    };
  });
})();
