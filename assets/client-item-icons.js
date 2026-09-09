(() => {
  'use strict';

  const ZERO_ICON = id => `https://ragnarokzero.net/images/items/${id}.gif`;
  const DP_ICON = id => `https://static.divine-pride.net/images/items/item/${id}.png`;
  const ITEMS = () => (window.RO_DATA && Array.isArray(window.RO_DATA.items) ? window.RO_DATA.items : []);
  let observer = null;
  let cachedItems = null;
  let cachedLookup = null;

  function maps() {
    const rows = ITEMS();
    if (cachedItems === rows && cachedLookup) return cachedLookup;
    const byId = new Map();
    const byName = new Map();
    for (const item of rows) {
      const id = Number(item.clientId || item.id);
      if (!Number.isFinite(id) || !item.name) continue;
      byId.set(String(id), item);
      byName.set(String(item.name).trim().toLowerCase(), item);
    }
    cachedItems = rows;
    cachedLookup = { byId, byName };
    return cachedLookup;
  }

  function resolveItem(anchor, lookup) {
    const explicit=anchor.dataset.rzDropItemId;
    if(explicit && /^\d+$/.test(explicit)) return lookup.byId.get(explicit) || {id:explicit,clientId:explicit,name:(anchor.textContent||'').trim()};
    const href = anchor.getAttribute('href') || '';
    const m = href.match(/#\/(?:items|cards)\/([^?#]+)/i);
    if (m) {
      const token = decodeURIComponent(m[1]);
      if (lookup.byId.has(token)) return lookup.byId.get(token);
      if(/^\d+$/.test(token)) return {id:token,clientId:token,name:(anchor.textContent||'').trim()};
    }
    const name = (anchor.textContent || '').trim().toLowerCase();
    return lookup.byName.get(name) || null;
  }

  function ensureObserver() {
    if (observer || !('IntersectionObserver' in window)) return observer;
    observer = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        const img = entry.target;
        if (img.dataset.src && !img.src) img.src = img.dataset.src;
        observer.unobserve(img);
      }
    }, { rootMargin: '40px 0px' });
    return observer;
  }

  function makeIcon(item, size) {
    const id = Number(item.clientId || item.id);
    if (!Number.isFinite(id)) return null;
    const img = document.createElement('img');
    img.className = 'rz-item-icon';
    img.width = size;
    img.height = size;
    img.alt = '';
    img.decoding = 'async';
    img.loading = 'lazy';
    try { img.fetchPriority = 'low'; } catch (_) {}
    img.dataset.src = ZERO_ICON(id);
    img.dataset.fallback = DP_ICON(id);
    img.style.cssText = `width:${size}px;height:${size}px;object-fit:contain;image-rendering:pixelated;vertical-align:middle;display:inline-block;flex:0 0 ${size}px;`;
    let fallbackUsed=false;
    img.addEventListener('error', () => {
      if(!fallbackUsed && img.dataset.fallback){fallbackUsed=true;img.src=img.dataset.fallback;return;}
      img.remove();
    });
    const io = ensureObserver();
    if (io) io.observe(img); else img.src = img.dataset.src;
    return img;
  }

  function decorateLinks(root = document) {
    const lookup = maps();
    for (const a of root.querySelectorAll('a[href^="#/items/"],a[href^="#/cards/"],a[data-rz-drop-item-id]')) {
      if (a.dataset.rzItemIcon === '1' || a.closest('.brand')) continue;
      const item = resolveItem(a, lookup);
      if (!item) continue;
      const icon = makeIcon(item, 22);
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
    const item = lookup.byId.get(token) || lookup.byName.get(token.replace(/[-_]+/g, ' ').toLowerCase()) || (/^\d+$/.test(token)?{id:token,clientId:token}:null);
    if (!item) return;
    const h1 = document.querySelector('.main-content h1');
    if (!h1 || h1.dataset.rzItemIcon === '1') return;
    const icon = makeIcon(item, 32);
    if (!icon) return;
    h1.dataset.rzItemIcon = '1';
    h1.style.display = 'flex';
    h1.style.alignItems = 'center';
    h1.style.gap = '8px';
    h1.insertBefore(icon, h1.firstChild);
  }

  function decorate() {
    const main = document.querySelector('.main-content') || document;
    decorateLinks(main);
    decorateHeading();
  }

  function afterRender() {
    requestAnimationFrame(() => {
      decorate();
      requestAnimationFrame(decorate);
    });
  }

  window.RZ_DECORATE_ITEM_ICONS = decorate;
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', afterRender, { once: true });
  else afterRender();
  window.addEventListener('hashchange', afterRender);
  document.addEventListener('input', e => {
    if (e.target && e.target.closest && e.target.closest('.global-search-wrap')) requestAnimationFrame(decorate);
  });
})();
