(() => {
  'use strict';

  const ZERO_ICON = id => `https://ragnarokzero.net/images/items/${id}.gif`;
  const DP_ICON = id => `https://static.divine-pride.net/images/items/item/${id}.png`;
  const ITEMS = () => (window.RO_DATA && Array.isArray(window.RO_DATA.items) ? window.RO_DATA.items : []);
  let cachedItems = null;
  let cachedLookup = null;

  function normaliseName(value) {
    return String(value || '')
      .trim()
      .toLowerCase()
      .replace(/\s+/g, ' ')
      .replace(/\s*\[\d+\]\s*$/, '');
  }

  function maps() {
    const rows = ITEMS();
    if (cachedItems === rows && cachedLookup) return cachedLookup;
    const byId = new Map();
    const byName = new Map();
    for (const item of rows) {
      const id = Number(item.clientId || item.id);
      if (!Number.isFinite(id) || !item.name) continue;
      byId.set(String(id), item);
      const nameKey = normaliseName(item.name);
      if (nameKey && !byName.has(nameKey)) byName.set(nameKey, item);
    }
    cachedItems = rows;
    cachedLookup = { byId, byName };
    return cachedLookup;
  }

  function anchorDisplayName(anchor) {
    // Monster drops keep the item name in their direct <span>; using the whole
    // anchor text would incorrectly include the trailing "???" / drop rate.
    const directName = anchor.querySelector?.(':scope > span')?.textContent;
    return String(directName || anchor.dataset.rzDropItemName || anchor.textContent || '').trim();
  }

  function resolveItem(anchor, lookup) {
    const displayName = anchorDisplayName(anchor);
    const byName = lookup.byName.get(normaliseName(displayName)) || null;
    const explicit = anchor.dataset.rzDropItemId;

    // Some monster-drop sources still carry an old/non-Zero item ID. Prefer the
    // official client item with the same display name before synthesising an ID.
    if (explicit && /^\d+$/.test(explicit)) {
      if (lookup.byId.has(explicit)) return lookup.byId.get(explicit);
      if (byName) return byName;
      return { id:explicit, clientId:explicit, name:displayName };
    }

    const href = anchor.getAttribute('href') || '';
    const m = href.match(/#\/(?:items|cards)\/([^?#]+)/i);
    if (m) {
      const token = decodeURIComponent(m[1]);
      if (lookup.byId.has(token)) return lookup.byId.get(token);
      if (byName) return byName;
      if (/^\d+$/.test(token)) return { id:token, clientId:token, name:displayName };
    }
    return byName;
  }

  function makeIcon(item, size, priority='auto') {
    const id = Number(item.clientId || item.id);
    if (!Number.isFinite(id)) return null;
    const img = document.createElement('img');
    img.className = 'rz-item-icon';
    img.width = size;
    img.height = size;
    img.alt = '';
    img.decoding = 'async';
    img.loading = 'eager';
    try { img.fetchPriority = priority; } catch (_) {}
    img.dataset.fallback = DP_ICON(id);
    img.style.cssText = `width:${size}px;height:${size}px;object-fit:contain;image-rendering:pixelated;vertical-align:middle;display:inline-block;flex:0 0 ${size}px;`;
    let fallbackUsed=false;
    img.addEventListener('error', () => {
      if(!fallbackUsed && img.dataset.fallback){fallbackUsed=true;img.src=img.dataset.fallback;return;}
      img.remove();
    });
    // Immediate only for the currently rendered pagination slice.
    img.src = ZERO_ICON(id);
    return img;
  }

  function decorateLinks(root = document) {
    if(!root?.querySelectorAll) return;
    const lookup = maps();
    for (const a of root.querySelectorAll('a[href^="#/items/"],a[href^="#/cards/"],a[data-rz-drop-item-id]')) {
      if (a.dataset.rzItemIcon === '1' || a.closest('.brand')) continue;
      const item = resolveItem(a, lookup);
      if (!item) continue;
      const icon = makeIcon(item, 22, 'auto');
      if (!icon) continue;
      a.dataset.rzItemIcon = '1';
      a.style.display = 'inline-flex';
      a.style.alignItems = 'center';
      a.style.gap = '5px';
      a.insertBefore(icon, a.firstChild);
    }
  }

  function decorateHeading() {
    const m = location.hash.match(/^#\/(?:items|cards)\/([^?#]+)/i);
    if (!m) return;
    const lookup = maps();
    const token = decodeURIComponent(m[1]);
    const item = lookup.byId.get(token) || lookup.byName.get(normaliseName(token.replace(/[-_]+/g, ' '))) || (/^\d+$/.test(token)?{id:token,clientId:token}:null);
    if (!item) return;
    const h1 = document.querySelector('.main-content h1');
    if (!h1 || h1.dataset.rzItemIcon === '1') return;
    const icon = makeIcon(item, 32, 'high');
    if (!icon) return;
    h1.dataset.rzItemIcon = '1';
    h1.style.display = 'flex';
    h1.style.alignItems = 'center';
    h1.style.gap = '8px';
    h1.insertBefore(icon, h1.firstChild);
  }

  function currentPageScope() {
    const monsterResults=document.querySelector('#list-results .rz-monster-db-results, #list-output .rz-monster-db-results');
    if(monsterResults) return monsterResults;
    return document.querySelector('.main-content') || document;
  }

  function decorate(root) {
    const scoped = !!root;
    const scope = root?.querySelectorAll ? root : currentPageScope();
    decorateLinks(scope);
    if(!scoped) decorateHeading();
  }

  window.RZ_ITEM_ICON_SOURCES = id => ({primary:ZERO_ICON(id),fallback:DP_ICON(id)});
  window.RZ_DECORATE_ITEM_ICONS = decorate;

  const run=()=>decorate();
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, { once: true });
  else run();
  window.addEventListener('hashchange', () => queueMicrotask(run));
  document.addEventListener('input', e => {
    if (e.target && e.target.closest && e.target.closest('.global-search-wrap')) queueMicrotask(run);
  });
})();
