(() => {
  'use strict';

  function installStyles() {
    if (document.getElementById('rz-item-neutral-style')) return;
    const style = document.createElement('style');
    style.id = 'rz-item-neutral-style';
    style.textContent = `
      /* Light blue-gray RMS-style item tables. */
      .rz-rms-result,
      .rz-rms-wrap {
        filter: none !important;
      }
      .rz-rms-result {
        border-radius: 7px !important;
        overflow: hidden !important;
        box-shadow: 0 2px 9px rgba(31, 41, 55, .08) !important;
      }
      .rz-rms-result-title,
      .rz-rms-titlebar {
        background: #c8d8e6 !important;
        color: #24384a !important;
        border-color: #9fb3c4 !important;
      }
      .rz-rms-titlebar {
        border-radius: 7px 7px 0 0 !important;
      }
      .rz-rms-result-title a,
      .rz-rms-result-title strong,
      .rz-rms-result-title span,
      .rz-rms-titlebar h1,
      .rz-rms-titlebar .rz-rms-class,
      .rz-rms-titlebar .rz-rms-id,
      .rz-rms-titlebar .rz-rms-slot,
      .rz-rms-titlebar .rz-rms-name,
      .rz-rms-titlebar .rz-rms-class-link,
      .rz-rms-titlebar a {
        color: #24384a !important;
      }

      .rz-rms-result-sheet,
      .rz-rms-sheet {
        background: #f7fafc !important;
        color: #263846 !important;
        border-color: #aabcc9 !important;
      }
      .rz-rms-result-sheet th,
      .rz-rms-result-sheet td,
      .rz-rms-sheet th,
      .rz-rms-sheet td {
        border-color: #aabcc9 !important;
      }
      .rz-rms-result-sheet th,
      .rz-rms-sheet th {
        background: #dde8f1 !important;
        color: #294052 !important;
        font-weight: 700 !important;
      }
      .rz-rms-result-sheet td,
      .rz-rms-sheet td {
        background: #fbfdff !important;
        color: #263846 !important;
      }
      .rz-rms-result-sheet tr:nth-child(even) td,
      .rz-rms-sheet tr:nth-child(even) td {
        background: #f1f6fa !important;
      }
      .rz-rms-result-sheet code,
      .rz-rms-sheet code {
        color: #263846 !important;
      }
      .rz-rms-table-scroll {
        border-radius: 0 0 7px 7px !important;
      }

      /* Missing database relations must stand out clearly. */
      .rz-rms-red,
      .rz-rms-result-sheet .rz-rms-red,
      .rz-rms-sheet .rz-rms-red,
      .rz-rms-missing {
        color: #c40000 !important;
        font-weight: 700 !important;
      }
    `;
    document.head.appendChild(style);
  }

  function protectRenderedItemTitles(root = document) {
    root.querySelectorAll('.rz-rms-result-title').forEach(title => {
      if (!title.querySelector('.rz-item-icon')) return;
      title.querySelectorAll('a[href^="#/items/"],a[href^="#/cards/"]').forEach(a => {
        a.dataset.rzItemIcon = '1';
      });
    });

    root.querySelectorAll('.rz-rms-titlebar').forEach(title => {
      if (!title.querySelector('.rz-item-icon')) return;
      title.querySelectorAll('a[href^="#/items/"],a[href^="#/cards/"]').forEach(a => {
        a.dataset.rzItemIcon = '1';
      });
    });

    root.querySelectorAll('a[href^="#/items/"],a[href^="#/cards/"]').forEach(a => {
      if (a.querySelector('.rz-item-icon')) a.dataset.rzItemIcon = '1';
    });
  }

  function pruneDuplicates(root = document) {
    root.querySelectorAll('.rz-rms-result-title, .rz-rms-titlebar').forEach(host => {
      const icons = [...host.querySelectorAll('.rz-item-icon')];
      icons.slice(1).forEach(icon => icon.remove());
      if (icons.length) {
        host.querySelectorAll('a[href^="#/items/"],a[href^="#/cards/"]').forEach(a => {
          a.dataset.rzItemIcon = '1';
        });
      }
    });
  }

  function wrapDecorator() {
    const current = window.RZ_DECORATE_ITEM_ICONS;
    if (typeof current !== 'function' || current.__rzNeutralWrapped) return;
    const wrapped = function(root = document) {
      protectRenderedItemTitles(root);
      current(root);
      pruneDuplicates(root);
    };
    wrapped.__rzNeutralWrapped = true;
    window.RZ_DECORATE_ITEM_ICONS = wrapped;
  }

  function refresh() {
    installStyles();
    wrapDecorator();
    protectRenderedItemTitles(document);
    requestAnimationFrame(() => {
      wrapDecorator();
      protectRenderedItemTitles(document);
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
