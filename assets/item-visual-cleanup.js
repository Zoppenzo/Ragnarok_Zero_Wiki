(() => {
  'use strict';

  function installStyles() {
    if (document.getElementById('rz-item-neutral-style')) return;
    const style = document.createElement('style');
    style.id = 'rz-item-neutral-style';
    style.textContent = `
      /* Neutral RMS-style item tables: white / very light gray, no blue fill. */
      .rz-item-result-table,
      .rz-rms-sheet {
        border-color: #b8bdc3 !important;
        background: #fff !important;
        color: #202122 !important;
      }
      .rz-item-result-table th,
      .rz-rms-sheet th {
        background: #f1f2f3 !important;
        color: #202122 !important;
        border-color: #b8bdc3 !important;
      }
      .rz-item-result-table td,
      .rz-rms-sheet td {
        background: #fff !important;
        color: #202122 !important;
        border-color: #b8bdc3 !important;
      }
      .rz-item-result-table tr:nth-child(even) td,
      .rz-rms-sheet tr:nth-child(even) td {
        background: #fafafa !important;
      }
      .rz-item-result-title,
      .rz-rms-titlebar {
        background: #f3f4f5 !important;
        color: #202122 !important;
        border-color: #b8bdc3 !important;
      }
      .rz-item-result-title a,
      .rz-item-result-title strong,
      .rz-rms-titlebar h1,
      .rz-rms-titlebar .rz-rms-class,
      .rz-rms-titlebar .rz-rms-id,
      .rz-rms-titlebar .rz-rms-slot {
        color: #202122 !important;
      }

      /* A renderer already providing an icon owns that icon. Hide accidental duplicates. */
      .rz-item-result-title a > .rz-item-icon ~ .rz-item-icon,
      .rz-rms-titlebar h1 > .rz-item-icon ~ .rz-item-icon,
      .rz-item-result-title a > img.rz-item-icon:nth-of-type(n+2),
      .rz-rms-titlebar h1 > img.rz-item-icon:nth-of-type(n+2) {
        display: none !important;
      }
    `;
    document.head.appendChild(style);
  }

  function markExistingIcons(root = document) {
    root.querySelectorAll('a[href^="#/items/"],a[href^="#/cards/"]').forEach(a => {
      if (a.querySelector('.rz-item-icon')) a.dataset.rzItemIcon = '1';
    });
    root.querySelectorAll('.main-content h1').forEach(h1 => {
      if (h1.querySelector('.rz-item-icon')) h1.dataset.rzItemIcon = '1';
    });
  }

  function pruneDuplicates(root = document) {
    root.querySelectorAll('.rz-item-result-title a, .rz-rms-titlebar h1').forEach(host => {
      const icons = [...host.querySelectorAll(':scope > .rz-item-icon')];
      icons.slice(1).forEach(icon => icon.remove());
      if (icons.length) host.dataset.rzItemIcon = '1';
    });
  }

  const originalDecorator = window.RZ_DECORATE_ITEM_ICONS;
  if (typeof originalDecorator === 'function') {
    window.RZ_DECORATE_ITEM_ICONS = function(root = document) {
      markExistingIcons(root);
      originalDecorator(root);
      pruneDuplicates(root);
    };
  }

  function refresh() {
    installStyles();
    markExistingIcons(document);
    requestAnimationFrame(() => {
      markExistingIcons(document);
      pruneDuplicates(document);
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', refresh, {once:true});
  else refresh();
  window.addEventListener('hashchange', refresh);
  document.addEventListener('input', e => {
    if (e.target?.closest?.('.filters, .global-search-wrap')) requestAnimationFrame(refresh);
  });
  document.addEventListener('change', e => {
    if (e.target?.closest?.('.filters')) requestAnimationFrame(refresh);
  });
  document.addEventListener('click', e => {
    if (e.target?.closest?.('.rz-db-page')) requestAnimationFrame(() => requestAnimationFrame(refresh));
  });
})();
