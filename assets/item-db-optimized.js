(() => {
  'use strict';

  const DEFAULT_PAGE_SIZE = 25;
  const PAGE_SIZES = [25, 50, 100, 200];

  const esc = value => String(value ?? '').replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const num = value => {
    if (value == null || value === '') return null;
    const n = Number(value);
    return Number.isFinite(n) ? n : null;
  };
  const fmt = value => num(value) == null ? '—' : Number(value).toLocaleString();
  const langFr = () => (document.documentElement.lang || '').toLowerCase().startsWith('fr');

  const EQUIP_LABELS = {
    'Sword':'Sword (1H)',
    'Two-Handed Sword':'Sword (2H)',
    'One-Handed Axe':'Axe (1H)',
    'Two-Handed Axe':'Axe (2H)',
    'One-Handed Spear':'Spear (1H)',
    'Two-Handed Spear':'Spear (2H)',
    'One-Handed Staff':'Staff (1H)',
    'Two-Handed Staff':'Staff (2H)',
    'Dagger':'Dagger',
    'Bow':'Bow',
    'Mace':'Mace',
    'Knuckle':'Knuckle',
    'Katar':'Katar',
    'Book':'Book',
    'Whip':'Whip',
    'Instrument':'Instrument',
    'Musical Instrument':'Instrument',
    'Shield':'Shield',
    'Armor':'Armor',
    'Garment':'Garment',
    'Shoes':'Shoes',
    'Accessory':'Accessory',
    'Accessory (Left)':'Accessory (Left)',
    'Accessory (Right)':'Accessory (Right)',
    'Headgear':'Headgear',
    'Helmet':'Headgear',
    'Helm':'Headgear',
    'Costume':'Costume',
    'Costume Gear':'Costume',
    'Shadow Equipment':'Shadow Equipment',
    'Special Equipment':'Special Equipment'
  };

  const EQUIP_ORDER = [
    'Dagger','Sword','Two-Handed Sword','One-Handed Axe','Two-Handed Axe','One-Handed Spear','Two-Handed Spear',
    'Mace','One-Handed Staff','Two-Handed Staff','Bow','Knuckle','Katar','Book','Whip','Instrument','Musical Instrument',
    'Shield','Armor','Garment','Shoes','Accessory','Accessory (Left)','Accessory (Right)','Headgear','Helmet','Helm',
    'Costume','Costume Gear','Shadow Equipment','Special Equipment'
  ];

  function iconHtml(item, size = 34) {
    if (window.RZ_ITEM_ICON_HTML) return window.RZ_ITEM_ICON_HTML(item, size);
    return '';
  }

  function compareNullable(a, b, dir = 1) {
    const an = num(a), bn = num(b);
    if (an == null && bn == null) return 0;
    if (an == null) return 1;
    if (bn == null) return -1;
    return (an - bn) * dir;
  }

  const SORTS = [
    ['name-asc', 'Name A → Z', 'Nom A → Z', null],
    ['name-desc', 'Name Z → A', 'Nom Z → A', null],
    ['requiredLevel-asc', 'Required Lv.: low → high', 'Required Lv. : croissant', 'requiredLevel'],
    ['requiredLevel-desc', 'Required Lv.: high → low', 'Required Lv. : décroissant', 'requiredLevel'],
    ['slots-desc', 'Slots: high → low', 'Slots : décroissant', 'slotCount'],
    ['slots-asc', 'Slots: low → high', 'Slots : croissant', 'slotCount'],
    ['weight-desc', 'Weight: high → low', 'Weight : décroissant', 'weight'],
    ['weight-asc', 'Weight: low → high', 'Weight : croissant', 'weight'],
    ['buy-desc', 'NPC Buy: high → low', 'NPC Buy : décroissant', 'buyPrice'],
    ['buy-asc', 'NPC Buy: low → high', 'NPC Buy : croissant', 'buyPrice'],
    ['sell-desc', 'Sell Price: high → low', 'Sell Price : décroissant', 'sellPrice'],
    ['sell-asc', 'Sell Price: low → high', 'Sell Price : croissant', 'sellPrice'],
    ['atk-desc', 'ATK: high → low', 'ATK : décroissant', 'atk'],
    ['atk-asc', 'ATK: low → high', 'ATK : croissant', 'atk'],
    ['matk-desc', 'MATK: high → low', 'MATK : décroissant', 'matk'],
    ['matk-asc', 'MATK: low → high', 'MATK : croissant', 'matk'],
    ['def-desc', 'DEF: high → low', 'DEF : décroissant', 'def'],
    ['def-asc', 'DEF: low → high', 'DEF : croissant', 'def'],
    ['mdef-desc', 'MDEF: high → low', 'MDEF : décroissant', 'mdef'],
    ['mdef-asc', 'MDEF: low → high', 'MDEF : croissant', 'mdef'],
  ];

  function usableSorts(source) {
    const has = field => source.some(item => num(item[field]) != null);
    return SORTS.filter(([, , , field]) => !field || has(field));
  }

  function sortRows(rows, mode) {
    const cut = mode.lastIndexOf('-');
    const field = cut < 0 ? mode : mode.slice(0, cut);
    const dirName = cut < 0 ? 'asc' : mode.slice(cut + 1);
    const dir = dirName === 'asc' ? 1 : -1;
    if (field === 'name') {
      rows.sort((a,b) => a.name.localeCompare(b.name, 'en', {sensitivity:'base'}) * dir);
      return;
    }
    const key = {
      requiredLevel:'requiredLevel', slots:'slotCount', weight:'weight', buy:'buyPrice', sell:'sellPrice',
      atk:'atk', matk:'matk', def:'def', mdef:'mdef'
    }[field];
    if (!key) return;
    rows.sort((a,b) => {
      const cmp = compareNullable(a[key], b[key], dir);
      return cmp || a.name.localeCompare(b.name, 'en', {sensitivity:'base'});
    });
  }

  function statChip(label, value, suffix='') {
    if (num(value) == null && !value) return '';
    const display = num(value) == null ? esc(value) : `${fmt(value)}${suffix}`;
    return `<span class="rz-item-stat"><b>${esc(label)}</b> ${display}</span>`;
  }

  function itemMeta(item) {
    const equipment = item.type === 'Equipment';
    const chunks = [];
    if (equipment) {
      chunks.push(statChip('ATK', item.atk));
      chunks.push(statChip('MATK', item.matk));
      chunks.push(statChip('DEF', item.def));
      chunks.push(statChip('MDEF', item.mdef));
      chunks.push(statChip('Slots', item.slotCount));
      chunks.push(statChip('Required Lv.', item.requiredLevel));
      chunks.push(statChip('Weapon Lv.', item.weaponLevel));
    } else if (item.requiredLevel != null) {
      chunks.push(statChip('Required Lv.', item.requiredLevel));
    }
    chunks.push(statChip('Weight', item.weight));
    if (item.buyPrice != null) chunks.push(statChip('NPC Buy', item.buyPrice, ' Zeny'));
    if (item.sellPrice != null) chunks.push(statChip('Sell', item.sellPrice, ' Zeny'));
    return chunks.filter(Boolean).join('');
  }

  function renderRows(type, rows) {
    const cardRoute = type === 'cards';
    return `<div class="rz-item-results">${rows.map(item => {
      const href = `${cardRoute ? '#/cards/' : '#/items/'}${encodeURIComponent(item.id)}`;
      const subtype = item.type === 'Equipment' ? (EQUIP_LABELS[item.subtype] || item.subtype || 'Equipment') : (item.subtype || item.type || 'Item');
      return `<article class="rz-item-result">
        <div class="rz-item-result-icon"><a href="${href}" class="rz-item-db-link">${iconHtml(item,42)}<span class="rz-item-icon-fallback"></span></a></div>
        <div class="rz-item-result-body">
          <div class="rz-item-result-head">
            <div>
              <a class="table-link rz-item-name-link" href="${href}"><strong>${esc(item.name)}</strong></a>
              <div class="rz-item-kicker">#${esc(item.id)} · ${esc(item.type || 'Item')} · ${esc(subtype)}</div>
            </div>
            <div class="rz-item-result-stats">${itemMeta(item)}</div>
          </div>
          ${item.description ? `<div class="rz-item-description">${esc(item.description)}</div>` : ''}
        </div>
      </article>`;
    }).join('')}</div>`;
  }

  function pagerHtml(page, pages, total, pageSize) {
    const start = total ? (page - 1) * pageSize + 1 : 0;
    const end = Math.min(page * pageSize, total);
    const buttons = [];
    const push = (p, label, disabled=false, current=false) => buttons.push(`<button class="button rz-db-page${current?' current':''}" data-page="${p}" ${disabled?'disabled':''}>${label}</button>`);
    push(Math.max(1,page-1), '‹', page<=1);
    const candidates = new Set([1, pages, page-2, page-1, page, page+1, page+2].filter(p=>p>=1&&p<=pages));
    let prev = 0;
    for (const p of [...candidates].sort((a,b)=>a-b)) {
      if (prev && p > prev + 1) buttons.push('<span class="rz-db-ellipsis">…</span>');
      push(p, String(p), false, p===page);
      prev = p;
    }
    push(Math.min(pages,page+1), '›', page>=pages);
    return `<div class="rz-db-pager">
      <span class="rz-db-range">${start.toLocaleString()}–${end.toLocaleString()} / ${total.toLocaleString()}</span>
      <div class="rz-db-pages">${buttons.join('')}</div>
    </div>`;
  }

  function ensureStyles() {
    if (document.getElementById('rz-item-db-opt-style')) return;
    const style = document.createElement('style');
    style.id = 'rz-item-db-opt-style';
    style.textContent = `
      .rz-item-results{display:grid;gap:8px}
      .rz-item-result{display:grid;grid-template-columns:58px minmax(0,1fr);gap:10px;padding:10px 12px;border:1px solid var(--line-soft);background:#fff}
      .rz-item-result:nth-child(even){background:#f8f9fa}
      .rz-item-result-icon{width:58px;min-height:54px;display:flex;align-items:flex-start;justify-content:center;padding-top:2px}
      .rz-item-result-icon a{width:48px;height:48px;display:grid;place-items:center;border-radius:4px;background:#f5f7fa}
      .rz-item-result-head{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;flex-wrap:wrap}
      .rz-item-name-link{font-size:15px;line-height:1.25}
      .rz-item-kicker{margin-top:2px;color:#72777d;font-size:11px}
      .rz-item-description{margin-top:7px;color:#3a3a3a;line-height:1.45;font-size:12px}
      .rz-item-result-stats{display:flex;gap:4px;flex-wrap:wrap;justify-content:flex-end;max-width:720px}
      .rz-item-stat{padding:3px 6px;border:1px solid #c8ccd1;background:#f8f9fa;border-radius:3px;white-space:nowrap;font-size:11px;color:#54595d}
      .rz-item-stat b{color:#202122}
      .rz-db-pager{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin:12px 0}
      .rz-db-pages{display:flex;align-items:center;gap:4px;flex-wrap:wrap}
      .rz-db-page{min-width:34px;padding:5px 8px}
      .rz-db-page.current{background:#eaecf0;border-color:#72777d;font-weight:700}
      .rz-db-page:disabled{opacity:.45;cursor:not-allowed}
      .rz-db-ellipsis{padding:0 3px;color:#72777d}
      .rz-db-range{color:#54595d;font-size:12px}
      .filters .rz-db-sort-field,.filters .rz-db-size-field,.filters .rz-db-equip-field,.filters .rz-db-slot-field{min-width:170px}
      @media(max-width:800px){
        .rz-db-pager{align-items:flex-start;flex-direction:column}
        .rz-item-result{grid-template-columns:48px minmax(0,1fr);padding:9px}
        .rz-item-result-icon{width:48px}.rz-item-result-icon a{width:42px;height:42px}
        .rz-item-result-stats{justify-content:flex-start}
        .filters .rz-db-sort-field,.filters .rz-db-size-field,.filters .rz-db-equip-field,.filters .rz-db-slot-field{min-width:145px}
      }
    `;
    document.head.appendChild(style);
  }

  function equipSubtypeOptions(source) {
    const set = new Set(source.filter(x => x.type === 'Equipment' && x.subtype).map(x => x.subtype));
    const ordered = [...set].sort((a,b) => {
      const ai = EQUIP_ORDER.indexOf(a), bi = EQUIP_ORDER.indexOf(b);
      if (ai !== -1 || bi !== -1) return (ai === -1 ? 999 : ai) - (bi === -1 ? 999 : bi);
      return (EQUIP_LABELS[a] || a).localeCompare(EQUIP_LABELS[b] || b);
    });
    return ordered.map(v => `<option value="${esc(v)}">${esc(EQUIP_LABELS[v] || v)}</option>`).join('');
  }

  function wire(type) {
    if (!['items','cards'].includes(type)) return false;
    ensureStyles();

    const allItems = Array.isArray(window.RO_DATA?.items) ? window.RO_DATA.items : [];
    const source = type === 'cards' ? allItems.filter(x => x.type === 'Card') : allItems;
    const search = document.getElementById('list-search');
    const typeFilter = document.getElementById('list-filter');
    const count = document.getElementById('result-count');
    if (!search || !count) return false;

    let output = document.getElementById('list-results') || document.getElementById('list-output');
    if (!output) {
      output = count.nextElementSibling;
      if (!output) {
        output = document.createElement('div');
        count.insertAdjacentElement('afterend', output);
      }
    }

    const filters = search.closest('.filters');
    if (!filters) return false;

    const availableSorts = usableSorts(source);
    const state = { page:1, pageSize:DEFAULT_PAGE_SIZE, sort:'name-asc' };

    let equipSelect = null;
    let slotSelect = null;
    if (type === 'items') {
      let equipField = document.querySelector('.rz-db-equip-field');
      if (!equipField) {
        equipField = document.createElement('div');
        equipField.className = 'form-field rz-db-equip-field';
        equipField.innerHTML = `<label>${langFr()?'Equipment Type':'Equipment Type'}</label><select id="rz-db-equip" class="select"><option value="">${langFr()?'Tous les équipements':'All equipment'}</option>${equipSubtypeOptions(source)}</select>`;
        filters.appendChild(equipField);
      }
      equipSelect = equipField.querySelector('select');

      let slotField = document.querySelector('.rz-db-slot-field');
      if (!slotField) {
        slotField = document.createElement('div');
        slotField.className = 'form-field rz-db-slot-field';
        slotField.innerHTML = `<label>Slots</label><select id="rz-db-slots" class="select"><option value="">${langFr()?'Tous':'All'}</option><option value="0">0</option><option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4+</option></select>`;
        filters.appendChild(slotField);
      }
      slotSelect = slotField.querySelector('select');
    }

    let sortSelect = document.getElementById('rz-db-sort');
    if (!sortSelect) {
      const field = document.createElement('div');
      field.className = 'form-field rz-db-sort-field';
      field.innerHTML = `<label>${langFr()?'Trier par':'Sort by'}</label><select id="rz-db-sort" class="select">${availableSorts.map(([v,en,fr])=>`<option value="${v}">${esc(langFr()?fr:en)}</option>`).join('')}</select>`;
      filters.appendChild(field);
      sortSelect = field.querySelector('select');
    }

    let sizeSelect = document.getElementById('rz-db-size');
    if (!sizeSelect) {
      const field = document.createElement('div');
      field.className = 'form-field rz-db-size-field';
      field.innerHTML = `<label>${langFr()?'Items par page':'Items per page'}</label><select id="rz-db-size" class="select">${PAGE_SIZES.map(v=>`<option value="${v}" ${v===DEFAULT_PAGE_SIZE?'selected':''}>${v}</option>`).join('')}</select>`;
      filters.appendChild(field);
      sizeSelect = field.querySelector('select');
    }

    let pager = document.getElementById('rz-db-pager-host');
    if (!pager) {
      pager = document.createElement('div');
      pager.id = 'rz-db-pager-host';
      output.insertAdjacentElement('afterend', pager);
    }

    const refresh = () => {
      const q = (search.value || '').trim().toLowerCase();
      const f = typeFilter?.value || '';
      const equip = equipSelect?.value || '';
      const slots = slotSelect?.value ?? '';
      let rows = source.filter(item => {
        if (q && !(`${item.name} ${item.description||''} ${item.type||''} ${item.subtype||''} ${item.id}`).toLowerCase().includes(q)) return false;
        if (type === 'items' && f && item.type !== f) return false;
        if (equip && !(item.type === 'Equipment' && item.subtype === equip)) return false;
        if (slots !== '') {
          const sc = num(item.slotCount) ?? 0;
          if (slots === '4' ? sc < 4 : sc !== Number(slots)) return false;
        }
        return true;
      });
      sortRows(rows, state.sort);
      const pages = Math.max(1, Math.ceil(rows.length / state.pageSize));
      state.page = Math.min(Math.max(1,state.page), pages);
      const start = (state.page - 1) * state.pageSize;
      const visible = rows.slice(start, start + state.pageSize);
      count.textContent = `${rows.length.toLocaleString()} ${langFr()?'résultats':'results'}`;
      output.innerHTML = renderRows(type, visible);
      pager.innerHTML = pagerHtml(state.page, pages, rows.length, state.pageSize);
      requestAnimationFrame(() => window.RZ_DECORATE_ITEM_ICONS?.(output));
      pager.querySelectorAll('[data-page]').forEach(btn => btn.addEventListener('click', () => {
        state.page = Number(btn.dataset.page) || 1;
        refresh();
        filters.scrollIntoView({block:'start'});
      }));
    };

    search.addEventListener('input', () => { state.page=1; refresh(); });
    typeFilter?.addEventListener('change', () => { state.page=1; refresh(); });
    equipSelect?.addEventListener('change', () => {
      if (equipSelect.value && typeFilter) typeFilter.value = 'Equipment';
      state.page=1; refresh();
    });
    slotSelect?.addEventListener('change', () => { state.page=1; refresh(); });
    sortSelect.addEventListener('change', () => { state.sort=sortSelect.value; state.page=1; refresh(); });
    sizeSelect.addEventListener('change', () => { state.pageSize=Number(sizeSelect.value)||DEFAULT_PAGE_SIZE; state.page=1; refresh(); });
    refresh();
    return true;
  }

  window.RZ_ITEM_DB_OPT = { wire };
})();
