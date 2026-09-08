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

  function iconHtml(item, size = 22) {
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
    ['weight-desc', 'Weight: high → low', 'Weight : décroissant', 'weight'],
    ['weight-asc', 'Weight: low → high', 'Weight : croissant', 'weight'],
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
    const [field, dirName] = mode.split('-');
    const dir = dirName === 'asc' ? 1 : -1;
    if (field === 'name') {
      rows.sort((a,b) => a.name.localeCompare(b.name, 'en', {sensitivity:'base'}) * dir);
      return;
    }
    const key = {
      weight:'weight', sell:'sellPrice', atk:'atk', matk:'matk', def:'def', mdef:'mdef'
    }[field];
    if (!key) return;
    rows.sort((a,b) => {
      const cmp = compareNullable(a[key], b[key], dir);
      return cmp || a.name.localeCompare(b.name, 'en', {sensitivity:'base'});
    });
  }

  function renderRows(type, rows, showSellPrice) {
    const cardRoute = type === 'cards';
    const body = rows.map(item => {
      const href = `${cardRoute ? '#/cards/' : '#/items/'}${encodeURIComponent(item.id)}`;
      return `<tr>
        <td><a class="table-link rz-item-db-link" href="${href}">${iconHtml(item,22)}<span>${esc(item.name)}</span></a></td>
        <td>${esc(item.type || '—')}</td>
        <td>${esc(item.subtype || '—')}</td>
        <td>${fmt(item.weight)}</td>
        <td>${fmt(item.atk)}</td>
        <td>${fmt(item.matk)}</td>
        <td>${fmt(item.def)}</td>
        <td>${fmt(item.mdef)}</td>
        ${showSellPrice ? `<td>${fmt(item.sellPrice)}</td>` : ''}
        <td>${fmt(item.requiredLevel)}</td>
      </tr>`;
    }).join('');
    return `<div class="table-wrap rz-item-db-table"><table>
      <thead><tr>
        <th>${langFr()?'Nom':'Name'}</th><th>Type</th><th>${langFr()?'Sous-type':'Subtype'}</th>
        <th>Weight</th><th>ATK</th><th>MATK</th><th>DEF</th><th>MDEF</th>${showSellPrice?'<th>Sell Price</th>':''}<th>Required Lv.</th>
      </tr></thead><tbody>${body}</tbody>
    </table></div>`;
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
      .rz-item-db-link{display:inline-flex;align-items:center;gap:6px;min-height:24px}
      .rz-item-db-table table{min-width:920px}
      .rz-item-db-table th:nth-child(n+4),.rz-item-db-table td:nth-child(n+4){text-align:right;white-space:nowrap}
      .rz-db-pager{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin:12px 0}
      .rz-db-pages{display:flex;align-items:center;gap:4px;flex-wrap:wrap}
      .rz-db-page{min-width:34px;padding:5px 8px}
      .rz-db-page.current{background:#eaecf0;border-color:#72777d;font-weight:700}
      .rz-db-page:disabled{opacity:.45;cursor:not-allowed}
      .rz-db-ellipsis{padding:0 3px;color:#72777d}
      .rz-db-range{color:#54595d;font-size:12px}
      .filters .rz-db-sort-field,.filters .rz-db-size-field{min-width:190px}
      @media(max-width:800px){.rz-db-pager{align-items:flex-start;flex-direction:column}.filters .rz-db-sort-field,.filters .rz-db-size-field{min-width:145px}}
    `;
    document.head.appendChild(style);
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
    const showSellPrice = source.some(item => num(item.sellPrice) != null);
    const state = { page:1, pageSize:DEFAULT_PAGE_SIZE, sort:'name-asc' };

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
      let rows = source.filter(item => {
        if (q && !(`${item.name} ${item.type||''} ${item.subtype||''} ${item.id}`).toLowerCase().includes(q)) return false;
        if (type === 'items' && f && item.type !== f) return false;
        return true;
      });
      sortRows(rows, state.sort);
      const pages = Math.max(1, Math.ceil(rows.length / state.pageSize));
      state.page = Math.min(Math.max(1,state.page), pages);
      const start = (state.page - 1) * state.pageSize;
      const visible = rows.slice(start, start + state.pageSize);
      count.textContent = `${rows.length.toLocaleString()} ${langFr()?'résultats':'results'}`;
      output.innerHTML = renderRows(type, visible, showSellPrice);
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
    sortSelect.addEventListener('change', () => { state.sort=sortSelect.value; state.page=1; refresh(); });
    sizeSelect.addEventListener('change', () => { state.pageSize=Number(sizeSelect.value)||DEFAULT_PAGE_SIZE; state.page=1; refresh(); });
    refresh();
    return true;
  }

  window.RZ_ITEM_DB_OPT = { wire };
})();
