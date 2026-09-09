(() => {
  'use strict';

  const DEFAULT_PAGE_SIZE = 5;
  const PAGE_SIZES = [5, 10, 25, 50];
  const esc = value => String(value ?? '').replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const langFr = () => (document.documentElement.lang || '').toLowerCase().startsWith('fr');
  const num = value => value == null || value === '' ? null : (Number.isFinite(Number(value)) ? Number(value) : null);

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
    return `<div class="rz-db-pager"><span class="rz-db-range">${start.toLocaleString()}–${end.toLocaleString()} / ${total.toLocaleString()}</span><div class="rz-db-pages">${buttons.join('')}</div></div>`;
  }

  function ensureStyles() {
    if (document.getElementById('rz-monster-db-opt-style')) return;
    const style = document.createElement('style');
    style.id = 'rz-monster-db-opt-style';
    style.textContent = `
      .rz-db-pager{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin:14px 0}
      .rz-db-pages{display:flex;align-items:center;gap:4px;flex-wrap:wrap}
      .rz-db-page{min-width:34px;padding:5px 8px}.rz-db-page.current{background:#eaecf0;border-color:#72777d;font-weight:700}.rz-db-page:disabled{opacity:.45;cursor:not-allowed}
      .rz-db-ellipsis{padding:0 3px;color:#72777d}.rz-db-range{color:#54595d;font-size:12px}
      .filters .rz-monster-sort-field,.filters .rz-monster-page-size-field{min-width:170px}
      @media(max-width:800px){.rz-db-pager{align-items:flex-start;flex-direction:column}.filters .rz-monster-sort-field,.filters .rz-monster-page-size-field{min-width:145px}}
    `;
    document.head.appendChild(style);
  }

  function sortRows(rows, mode) {
    const nameSort = (a,b) => String(a.name || '').localeCompare(String(b.name || ''), 'en', {sensitivity:'base'});
    if (mode === 'name-desc') return rows.sort((a,b)=>-nameSort(a,b));
    if (mode === 'level-asc') return rows.sort((a,b)=>(num(a.level) ?? Infinity)-(num(b.level) ?? Infinity) || nameSort(a,b));
    if (mode === 'level-desc') return rows.sort((a,b)=>(num(b.level) ?? -Infinity)-(num(a.level) ?? -Infinity) || nameSort(a,b));
    if (mode === 'id-asc') return rows.sort((a,b)=>(num(a.clientId || a.id) ?? Infinity)-(num(b.clientId || b.id) ?? Infinity));
    if (mode === 'id-desc') return rows.sort((a,b)=>(num(b.clientId || b.id) ?? -Infinity)-(num(a.clientId || a.id) ?? -Infinity));
    return rows.sort(nameSort);
  }

  function wire(type) {
    if (type !== 'monsters') return false;
    if (typeof window.RZ_MONSTER_SHEET_HTML !== 'function') return false;
    ensureStyles();

    const source = Array.isArray(window.RO_DATA?.monsters) ? window.RO_DATA.monsters : [];
    const search = document.getElementById('list-search');
    const raceFilter = document.getElementById('list-filter');
    const count = document.getElementById('result-count');
    const output = document.getElementById('list-results') || document.getElementById('list-output');
    const filters = search?.closest('.filters');
    if (!search || !count || !output || !filters) return false;

    const state = {page:1, pageSize:DEFAULT_PAGE_SIZE, sort:'name-asc'};

    let sortSelect = document.getElementById('rz-monster-sort');
    if (!sortSelect) {
      const field = document.createElement('div');
      field.className = 'form-field rz-monster-sort-field';
      field.innerHTML = `<label>${langFr()?'Trier par':'Sort by'}</label><select id="rz-monster-sort" class="select"><option value="name-asc">${langFr()?'Nom A → Z':'Name A → Z'}</option><option value="name-desc">${langFr()?'Nom Z → A':'Name Z → A'}</option><option value="level-asc">${langFr()?'Niveau croissant':'Level low → high'}</option><option value="level-desc">${langFr()?'Niveau décroissant':'Level high → low'}</option><option value="id-asc">Mob-ID ↑</option><option value="id-desc">Mob-ID ↓</option></select>`;
      filters.appendChild(field);
      sortSelect = field.querySelector('select');
    }

    let sizeSelect = document.getElementById('rz-monster-page-size');
    if (!sizeSelect) {
      const field = document.createElement('div');
      field.className = 'form-field rz-monster-page-size-field';
      field.innerHTML = `<label>${langFr()?'Monstres par page':'Monsters per page'}</label><select id="rz-monster-page-size" class="select">${PAGE_SIZES.map(v=>`<option value="${v}" ${v===DEFAULT_PAGE_SIZE?'selected':''}>${v}</option>`).join('')}</select>`;
      filters.appendChild(field);
      sizeSelect = field.querySelector('select');
    }

    let pager = document.getElementById('rz-monster-pager-host');
    if (!pager) {
      pager = document.createElement('div');
      pager.id = 'rz-monster-pager-host';
      output.insertAdjacentElement('afterend', pager);
    }

    const refresh = () => {
      const q = (search.value || '').trim().toLowerCase();
      const race = raceFilter?.value || '';
      let rows = source.filter(m => {
        const maps = Array.isArray(m.maps) ? m.maps.map(x=>`${x.mapName||''} ${x.mapId||''}`).join(' ') : '';
        const haystack = `${m.name||''} ${m.internalName||''} ${m.id||''} ${m.clientId||''} ${m.race||''} ${m.size||''} ${m.level||''} ${maps}`.toLowerCase();
        if (q && !haystack.includes(q)) return false;
        if (race && m.race !== race) return false;
        return true;
      });
      sortRows(rows, state.sort);
      const pages = Math.max(1, Math.ceil(rows.length / state.pageSize));
      state.page = Math.min(Math.max(1, state.page), pages);
      const start = (state.page - 1) * state.pageSize;
      const visible = rows.slice(start, start + state.pageSize);
      count.textContent = `${rows.length.toLocaleString()} ${langFr()?'résultats':'results'}`;
      output.innerHTML = `<div class="rz-monster-db-results">${visible.map(m=>window.RZ_MONSTER_SHEET_HTML(m)).join('')}</div>`;
      pager.innerHTML = pagerHtml(state.page, pages, rows.length, state.pageSize);
      pager.querySelectorAll('[data-page]').forEach(btn => btn.addEventListener('click', () => {
        state.page = Number(btn.dataset.page) || 1;
        refresh();
        filters.scrollIntoView({block:'start'});
      }));
    };

    search.addEventListener('input', ()=>{state.page=1;refresh();});
    raceFilter?.addEventListener('change', ()=>{state.page=1;refresh();});
    sortSelect.addEventListener('change', ()=>{state.sort=sortSelect.value;state.page=1;refresh();});
    sizeSelect.addEventListener('change', ()=>{state.pageSize=Number(sizeSelect.value)||DEFAULT_PAGE_SIZE;state.page=1;refresh();});
    refresh();
    return true;
  }

  window.RZ_MONSTER_DB_OPT = {wire};
})();