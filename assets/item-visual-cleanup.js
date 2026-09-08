(() => {
  'use strict';

  function installStyles() {
    if (document.getElementById('rz-item-neutral-style')) return;
    const style = document.createElement('style');
    style.id = 'rz-item-neutral-style';
    style.textContent = `
      /* Item database: neutral wiki palette, no blue table fills. */
      .rz-rms-result-title,
      .rz-rms-titlebar {
        background: #f3f4f5 !important;
        color: #202122 !important;
        border-color: #c8ccd1 !important;
      }
      .rz-rms-result-title a,
      .rz-rms-titlebar h1,
      .rz-rms-titlebar .rz-rms-class,
      .rz-rms-titlebar .rz-rms-id,
      .rz-rms-titlebar .rz-rms-slot {
        color: #202122 !important;
      }

      .rz-rms-result-sheet,
      .rz-rms-sheet {
        background: #fff !important;
        color: #202122 !important;
        border-color: #c8ccd1 !important;
      }
      .rz-rms-result-sheet th,
      .rz-rms-result-sheet td,
      .rz-rms-sheet th,
      .rz-rms-sheet td {
        border-color: #c8ccd1 !important;
        color: #202122 !important;
      }
      .rz-rms-result-sheet th,
      .rz-rms-sheet th {
        background: #f1f2f3 !important;
      }
      .rz-rms-result-sheet td,
      .rz-rms-sheet td {
        background: #fff !important;
      }
      .rz-rms-result-sheet tr:nth-child(even) td,
      .rz-rms-sheet tr:nth-child(even) td {
        background: #fafafa !important;
      }
      .rz-rms-result-sheet code,
      .rz-rms-sheet code {
        color: #202122 !important;
      }
    `;
    document.head.appendChild(style);
  }

  function protectRenderedItemTitles(root = document) {
    /* The RMS list has two links in its title: icon + item name.
       If the renderer already supplied an icon, neither link should be
       decorated again by client-item-icons.js. */
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
