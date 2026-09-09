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
  const has = value => value !== null && value !== undefined && value !== '';
  const fmt = value => num(value) == null ? 'n/a' : Number(value).toLocaleString('en-US');
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

  const WEAPON_TYPES = new Set([
    'Dagger','Sword','Two-Handed Sword','One-Handed Axe','Two-Handed Axe','One-Handed Spear','Two-Handed Spear',
    'Mace','One-Handed Staff','Two-Handed Staff','Bow','Knuckle','Katar','Book','Whip','Instrument','Musical Instrument'
  ]);

  function iconHtml(item, size = 26) {
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
    const hasField = field => source.some(item => num(item[field]) != null);
    return SORTS.filter(([, , , field]) => !field || hasField(field));
  }

  function sortRows(rows, mode) {
    const cut = mode.lastIndexOf('-');
    const field = cut < 0 ? mode : mode.slice(0, cut);
    const dirName = cut < 0 ? 'asc' : mode.slice(cut + 1);
    const dir = dirName === 'asc' ? 1 : -1;
    if (field === 'name') {
      rows.sort((a,b) => String(a.name).localeCompare(String(b.name), 'en', {sensitivity:'base'}) * dir);
      return;
    }
    const key = {
      requiredLevel:'requiredLevel', slots:'slotCount', weight:'weight', buy:'buyPrice', sell:'sellPrice',
      atk:'atk', matk:'matk', def:'def', mdef:'mdef'
    }[field];
    if (!key) return;
    rows.sort((a,b) => compareNullable(a[key], b[key], dir) || String(a.name).localeCompare(String(b.name), 'en', {sensitivity:'base'}));
  }

  function displayType(item) {
    if (item.type === 'Equipment') {
      if (WEAPON_TYPES.has(item.subtype)) return 'Weapon';
      return 'Armor';
    }
    if (item.type === 'Card') return 'Card';
    if (item.type === 'Consumable') return 'Usable Item';
    return item.type || 'Etc';
  }

  function displayClass(item) {
    return EQUIP_LABELS[item.subtype] || item.subtype || item.type || 'n/a';
  }

  function price(value) {
    return num(value) == null ? 'n/a' : `${Number(value).toLocaleString('en-US')} Zeny`;
  }

  function cellPair(label, value, extraClass='') {
    return `<th>${esc(label)}</th><td${extraClass ? ` class="${extraClass}"` : ''}>${has(value) ? esc(value) : 'n/a'}</td>`;
  }

  function itemSecondRow(item) {
    const isWeapon = item.type === 'Equipment' && WEAPON_TYPES.has(item.subtype);
    const isArmor = item.type === 'Equipment' && !isWeapon;
    const pairs = [];

    if (isWeapon) {
      pairs.push(cellPair('Attack', num(item.atk) == null ? 'n/a' : fmt(item.atk)));
      if (num(item.matk) != null) pairs.push(cellPair('MATK', fmt(item.matk)));
    } else if (isArmor) {
      pairs.push(cellPair('Defense', num(item.def) == null ? 'n/a' : fmt(item.def)));
      if (num(item.mdef) != null) pairs.push(cellPair('MDEF', fmt(item.mdef)));
    } else if (num(item.atk) != null || num(item.def) != null) {
      const label = num(item.atk) != null ? 'Attack' : 'Defense';
      pairs.push(cellPair(label, fmt(num(item.atk) != null ? item.atk : item.def)));
    }

    pairs.push(cellPair('Required Lvl', num(item.requiredLevel) == null ? 'None' : fmt(item.requiredLevel)));
    if (isWeapon && num(item.weaponLevel) != null) pairs.push(cellPair('Weapon Lvl', fmt(item.weaponLevel)));
    pairs.push(cellPair('Slot', num(item.slotCount) == null ? '0' : fmt(item.slotCount)));

    const maxPairs = 5;
    const shown = pairs.slice(0, maxPairs);
    const remainingPairs = maxPairs - shown.length;
    return `${shown.join('')}${remainingPairs > 0 ? `<td colspan="${remainingPairs * 2}"></td>` : ''}`;
  }

  function renderOne(item, cardRoute) {
    const href = `${cardRoute ? '#/cards/' : '#/items/'}${encodeURIComponent(item.id)}`;
    const slots = item.type === 'Equipment' && num(item.slotCount) != null ? Number(item.slotCount) : 0;
    const slotTitle = item.type === 'Equipment' ? ` [${slots}]` : '';
    const applicableJobs = item.applicableJobs || item.jobs || 'n/a';
    const script = item.itemScript || item.script || 'n/a';
    const droppedBy = item.droppedBy || 'No Result';
    const soldBy = item.soldBy || item.npcVendors || null;
    const refinable = has(item.refinable) ? (item.refinable ? 'Yes' : 'No') : 'n/a';
    const description = item.description || 'n/a';

    return `<section class="rz-rms-result">
      <div class="rz-rms-result-title">
        <a class="rz-rms-item-icon rz-item-db-link" href="${href}">${iconHtml(item,26)}</a>
        <a class="rz-rms-item-name" href="${href}">${esc(item.name)}${esc(slotTitle)}</a>
        <span class="rz-rms-bracket">[${esc(displayClass(item))}]</span>
        <span class="rz-rms-id">Item ID# ${esc(item.id)}</span>
      </div>
      <div class="rz-rms-table-scroll">
        <table class="rz-rms-result-sheet"><tbody>
          <tr>
            ${cellPair('Type', displayType(item))}
            ${cellPair('Class', displayClass(item))}
            ${cellPair('Buy', price(item.buyPrice))}
            ${cellPair('Sell', price(item.sellPrice))}
            ${cellPair('Weight', num(item.weight) == null ? 'n/a' : fmt(item.weight))}
          </tr>
          <tr>${itemSecondRow(item)}</tr>
          <tr>
            ${cellPair('Refinable', refinable, refinable === 'No' ? 'rz-rms-red' : '')}
            <td colspan="8"></td>
          </tr>
          <tr><th>Applicable Jobs</th><td colspan="9" class="rz-rms-wide">${esc(applicableJobs)}</td></tr>
          <tr><th>Description</th><td colspan="9" class="rz-rms-wide rz-rms-description">${esc(description)}</td></tr>
          <tr><th>Item Script</th><td colspan="9" class="rz-rms-wide"><code>${esc(script)}</code></td></tr>
          <tr><th>Dropped By</th><td colspan="9" class="rz-rms-wide ${droppedBy === 'No Result' ? 'rz-rms-red' : ''}">${esc(droppedBy)}</td></tr>
          ${soldBy ? `<tr><th>Sold By</th><td colspan="9" class="rz-rms-wide">${esc(soldBy)}</td></tr>` : ''}
        </tbody></table>
      </div>
    </section>`;
  }

  function renderRows(type, rows) {
    const cardRoute = type === 'cards';
    return `<div class="rz-rms-results">${rows.map(item => renderOne(item, cardRoute)).join('')}</div>`;
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
      .rz-rms-results{display:grid;gap:14px;margin-top:10px}
      .rz-rms-result{border:0;background:transparent}
      .rz-rms-result-title{min-height:36px;display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:5px 7px;border:1px solid #4f83aa;border-bottom:0;background:#bfe1f7;color:#064d7d;font-family:Georgia,'Times New Roman',serif;font-size:14px}
      .rz-rms-result-title a{color:#064d7d}
      .rz-rms-item-icon{width:28px;height:28px;display:inline-grid;place-items:center;flex:0 0 28px}
      .rz-rms-item-name{font-size:15px;font-weight:700}
      .rz-rms-bracket,.rz-rms-id{font-family:Arial,Helvetica,sans-serif;font-size:12px;color:#064d7d}
      .rz-rms-table-scroll{overflow-x:auto}
      .rz-rms-result-sheet{width:100%;min-width:900px;border-collapse:collapse;border:1px solid #4f83aa;background:#dff1ff;font-size:12px;color:#063d63}
      .rz-rms-result-sheet th,.rz-rms-result-sheet td{border:1px solid #4f83aa;padding:4px 6px;vertical-align:top}
      .rz-rms-result-sheet th{width:105px;background:#c7e7fa;color:#064d7d;font-family:Georgia,'Times New Roman',serif;font-size:13px;font-weight:700;white-space:nowrap;text-align:left}
      .rz-rms-result-sheet td{background:#eaf7ff}
      .rz-rms-result-sheet .rz-rms-wide{line-height:1.45;white-space:pre-line}
      .rz-rms-result-sheet .rz-rms-description{min-height:44px}
      .rz-rms-result-sheet .rz-rms-red{color:#c41818;font-weight:700}
      .rz-rms-result-sheet code{font-family:Consolas,monospace;font-size:11px;white-space:pre-wrap;word-break:break-word;color:#17456b}
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
        .filters .rz-db-sort-field,.filters .rz-db-size-field,.filters .rz-db-equip-field,.filters .rz-db-slot-field{min-width:145px}
        .rz-rms-result-title{font-size:13px}.rz-rms-item-name{font-size:14px}
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
        equipField.innerHTML = `<label>Equipment Type</label><select id="rz-db-equip" class="select"><option value="">${langFr()?'Tous les items':'Any item type'}</option><option value="__equipment__">All Equipment</option>${equipSubtypeOptions(source)}</select>`;
        filters.appendChild(equipField);
      }
      equipSelect = document.getElementById('rz-db-equip');

      let slotField = document.querySelector('.rz-db-slot-field');
      if (!slotField) {
        slotField = document.createElement('div');
        slotField.className = 'form-field rz-db-slot-field';
        slotField.innerHTML = `<label>Slots</label><select id="rz-db-slots" class="select"><option value="">All</option><option value="0">0</option><option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option></select>`;
        filters.appendChild(slotField);
      }
      slotSelect = document.getElementById('rz-db-slots');
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
      const ef = equipSelect?.value || '';
      const sf = slotSelect?.value ?? '';
      let rows = source.filter(item => {
        const haystack = `${item.name||''} ${item.type||''} ${item.subtype||''} ${item.id||''} ${item.description||''}`.toLowerCase();
        if (q && !haystack.includes(q)) return false;
        if (type === 'items' && f && item.type !== f) return false;
        if (ef === '__equipment__' && item.type !== 'Equipment') return false;
        if (ef && ef !== '__equipment__' && (item.type !== 'Equipment' || item.subtype !== ef)) return false;
        if (sf !== '' && (item.type !== 'Equipment' || Number(item.slotCount || 0) !== Number(sf))) return false;
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
      requestAnimationFrame(() => window.RZ_DECORATE_ITEM_ICONS?.());
      pager.querySelectorAll('[data-page]').forEach(btn => btn.addEventListener('click', () => {
        state.page = Number(btn.dataset.page) || 1;
        refresh();
        filters.scrollIntoView({block:'start'});
      }));
    };

    search.addEventListener('input', () => { state.page=1; refresh(); });
    typeFilter?.addEventListener('change', () => { state.page=1; refresh(); });
    equipSelect?.addEventListener('change', () => { state.page=1; refresh(); });
    slotSelect?.addEventListener('change', () => { state.page=1; refresh(); });
    sortSelect.addEventListener('change', () => { state.sort=sortSelect.value; state.page=1; refresh(); });
    sizeSelect.addEventListener('change', () => { state.pageSize=Number(sizeSelect.value)||DEFAULT_PAGE_SIZE; state.page=1; refresh(); });
    refresh();
    return true;
  }

  window.RZ_ITEM_DB_OPT = { wire };
})();
