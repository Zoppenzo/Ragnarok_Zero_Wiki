(() => {
  'use strict';

  const esc = value => String(value ?? '').replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const has = value => value !== null && value !== undefined && value !== '';
  const fmt = value => has(value) && Number.isFinite(Number(value)) ? Number(value).toLocaleString('en-US') : (has(value) ? String(value) : 'n/a');
  const items = () => Array.isArray(window.RO_DATA?.items) ? window.RO_DATA.items : [];

  const WEAPON_CLASSES = new Set([
    'Dagger','Sword','Two-Handed Sword','One-Handed Axe','Two-Handed Axe','One-Handed Spear','Two-Handed Spear',
    'Mace','One-Handed Staff','Two-Handed Staff','Bow','Knuckle','Katar','Book','Whip','Instrument','Musical Instrument'
  ]);

  function currentItem() {
    const m = location.hash.match(/^#\/(?:items|cards)\/([^?#]+)/i);
    if (!m) return null;
    const token = decodeURIComponent(m[1]);
    const lower = token.replace(/[-_]+/g,' ').toLowerCase();
    return items().find(item => String(item.id) === token || String(item.clientId || '') === token || String(item.name || '').toLowerCase() === lower) || null;
  }

  function rmsType(item) {
    if (item.type === 'Card') return 'Card';
    if (item.type !== 'Equipment') return item.type || 'Item';
    if (WEAPON_CLASSES.has(item.subtype)) return 'Weapon';
    return 'Armor';
  }

  function rmsClass(item) {
    if (item.type === 'Card') return 'Card';
    return item.subtype || item.type || 'n/a';
  }

  function valueCell(value, cls='') {
    return `<td${cls ? ` class="${cls}"` : ''}>${has(value) ? esc(value) : 'n/a'}</td>`;
  }

  function pair(label, value, cls='') {
    return `<th>${esc(label)}</th>${valueCell(has(value) ? value : 'n/a', cls)}`;
  }

  function numberPair(label, value, suffix='') {
    return pair(label, has(value) ? `${fmt(value)}${suffix}` : 'n/a');
  }

  function inferredRefinable(item) {
    const d = String(item.description || '').toLowerCase();
    if (/cannot be refined|can not be refined|unable to refine|not refinable/.test(d)) return 'No';
    if (has(item.refinable)) return item.refinable ? 'Yes' : 'No';
    return 'n/a';
  }

  function inferredJobs(item) {
    if (has(item.applicableJobs)) return item.applicableJobs;
    if (has(item.jobs)) return item.jobs;
    const d = String(item.description || '');
    const m = d.match(/(?:Applicable Jobs?|Equipped on|Equippable Jobs?|Jobs?)\s*:\s*([^\n]+)/i);
    return m ? m[1].trim() : 'n/a';
  }

  function topCombatPairs(item) {
    const weapon = item.type === 'Equipment' && WEAPON_CLASSES.has(item.subtype);
    const equipment = item.type === 'Equipment';
    if (weapon) {
      return [
        ['Attack', has(item.atk) ? fmt(item.atk) : 'n/a'],
        ['Required Lvl', has(item.requiredLevel) ? fmt(item.requiredLevel) : 'None'],
        ['Weapon Lvl', has(item.weaponLevel) ? fmt(item.weaponLevel) : 'n/a'],
        ['Slot', has(item.slotCount) ? fmt(item.slotCount) : '0'],
        ['MATK', has(item.matk) ? fmt(item.matk) : 'n/a']
      ];
    }
    if (equipment) {
      return [
        ['Defense', has(item.def) ? fmt(item.def) : '0'],
        ['Required Lvl', has(item.requiredLevel) ? fmt(item.requiredLevel) : 'None'],
        ['MDEF', has(item.mdef) ? fmt(item.mdef) : 'n/a'],
        ['Slot', has(item.slotCount) ? fmt(item.slotCount) : '0'],
        ['', '']
      ];
    }
    return [
      ['Defense', has(item.def) ? fmt(item.def) : '0'],
      ['Required Lvl', has(item.requiredLevel) ? fmt(item.requiredLevel) : 'None'],
      ['', ''],
      ['Slot', has(item.slotCount) ? fmt(item.slotCount) : '0'],
      ['', '']
    ];
  }

  function ensureStyles() {
    if (document.getElementById('rz-rms-item-style')) return;
    const style = document.createElement('style');
    style.id = 'rz-rms-item-style';
    style.textContent = `
      .rz-rms-wrap{width:min(100%,980px);margin:0}
      .rz-rms-back{margin:0 0 8px;font-size:12px}
      .rz-rms-titlebar{display:flex;align-items:center;gap:8px;min-height:37px;padding:4px 8px;border:1px solid #5d8fb4;border-bottom:0;background:#bfe3fb;color:#064d7d;font-family:Georgia,'Times New Roman',serif}
      .rz-rms-title-icon{display:inline-grid!important;place-items:center;width:28px;height:28px;flex:0 0 28px}
      .rz-rms-title-icon .rz-item-icon{width:24px!important;height:24px!important}
      .rz-rms-name{font-size:17px;font-weight:700;color:#064d7d;text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:2px}
      .rz-rms-slots{font-size:15px;color:#064d7d}
      .rz-rms-class-link,.rz-rms-id{margin-left:8px;font-size:14px;color:#064d7d}
      .rz-rms-sheet{width:100%;border-collapse:collapse;table-layout:fixed;border:1px solid #4f86ad;background:#dff1ff;color:#073e64;font-family:Arial,Helvetica,sans-serif;font-size:13px}
      .rz-rms-sheet col.rz-rms-label{width:14.4%}.rz-rms-sheet col.rz-rms-value{width:15.6%}
      .rz-rms-sheet col.rz-rms-label-small{width:9.5%}.rz-rms-sheet col.rz-rms-value-small{width:10.5%}
      .rz-rms-sheet th,.rz-rms-sheet td{border:1px solid #4f86ad;padding:4px 6px;vertical-align:middle}
      .rz-rms-sheet th{background:#cae8fb;color:#064d7d;font-family:Georgia,'Times New Roman',serif;font-size:15px;font-weight:700;text-align:left;line-height:1.05}
      .rz-rms-sheet td{background:#e6f4fd;color:#073e64;text-align:center;line-height:1.25}
      .rz-rms-sheet .rz-rms-empty{background:#e6f4fd}
      .rz-rms-sheet .rz-rms-wide{text-align:left;white-space:pre-line;line-height:1.35}
      .rz-rms-sheet .rz-rms-script{text-align:left;font-family:Consolas,'Courier New',monospace;font-size:12px;white-space:pre-wrap;word-break:break-word}
      .rz-rms-sheet .rz-rms-no{color:#e00000;font-weight:700}
      .rz-rms-sheet .rz-rms-missing{color:#e00000;font-weight:700}
      .rz-rms-note{margin-top:8px;color:#72777d;font-size:11px}
      @media(max-width:760px){
        .rz-rms-wrap{width:100%}.rz-rms-sheet{font-size:11px;table-layout:auto}.rz-rms-sheet th{font-size:12px;padding:4px}.rz-rms-sheet td{padding:4px}.rz-rms-class-link,.rz-rms-id{margin-left:2px;font-size:12px}.rz-rms-name{font-size:15px}
      }
    `;
    document.head.appendChild(style);
  }

  function render() {
    const item = currentItem();
    if (!item) return false;
    const main = document.querySelector('.main-content');
    if (!main || main.dataset.rzRmsItem === String(item.id)) return !!main;
    ensureStyles();

    const slots = item.type === 'Equipment' && has(item.slotCount) ? Number(item.slotCount) : (item.type === 'Card' ? null : (has(item.slotCount) ? Number(item.slotCount) : 0));
    const slotTitle = slots != null ? ` [${slots}]` : '';
    const buy = has(item.buyPrice) ? fmt(item.buyPrice) : 'n/a';
    const sell = has(item.sellPrice) ? fmt(item.sellPrice) : 'n/a';
    const refinable = inferredRefinable(item);
    const jobs = inferredJobs(item);
    const script = item.itemScript || item.script || 'n/a';
    const droppedBy = item.droppedBy || 'No Result';
    const soldBy = item.soldBy || item.npcVendors || 'No Result';
    const description = item.description || 'No description available.';
    const combat = topCombatPairs(item);
    const route = item.type === 'Card' ? 'cards' : 'items';

    main.dataset.rzRmsItem = String(item.id);
    main.innerHTML = `<div class="rz-rms-wrap">
      <div class="rz-rms-back"><a href="#/database/${item.type === 'Card' ? 'cards' : 'items'}">← ${item.type === 'Card' ? 'Card Database' : 'Item Database'}</a></div>
      <div class="rz-rms-titlebar">
        <a class="rz-rms-title-icon" href="#/${route}/${encodeURIComponent(item.id)}"></a>
        <span class="rz-rms-name">${esc(item.name)}</span><span class="rz-rms-slots">${esc(slotTitle)}</span>
        <span class="rz-rms-class-link">[${esc(rmsClass(item))}]</span>
        <span class="rz-rms-id">Item ID# ${esc(item.id)}</span>
      </div>
      <table class="rz-rms-sheet">
        <colgroup>
          <col class="rz-rms-label"><col class="rz-rms-value">
          <col class="rz-rms-label"><col class="rz-rms-value">
          <col class="rz-rms-label-small"><col class="rz-rms-value-small">
          <col class="rz-rms-label-small"><col class="rz-rms-value-small">
          <col class="rz-rms-label-small"><col class="rz-rms-value-small">
        </colgroup>
        <tbody>
          <tr>
            ${pair('Type', rmsType(item))}
            ${pair('Class', rmsClass(item))}
            ${pair('Buy', buy)}
            ${pair('Sell', sell)}
            ${numberPair('Weight', item.weight)}
          </tr>
          <tr>
            ${combat.map(([label,value]) => label ? pair(label,value) : '<th class="rz-rms-empty"></th><td class="rz-rms-empty"></td>').join('')}
          </tr>
          <tr>
            <th>Refinable</th><td class="${refinable === 'No' ? 'rz-rms-no' : ''}">${esc(refinable)}</td><td colspan="8" class="rz-rms-empty"></td>
          </tr>
          <tr>
            <th>Applicable<br>Jobs</th><td colspan="9" class="rz-rms-wide">${esc(jobs)}</td>
          </tr>
          <tr>
            <th>Description</th><td colspan="9" class="rz-rms-wide">${esc(description)}</td>
          </tr>
          <tr>
            <th>Item Script</th><td colspan="9" class="rz-rms-script">${esc(script)}</td>
          </tr>
          <tr>
            <th>Dropped By</th><td colspan="9" class="rz-rms-wide ${droppedBy === 'No Result' ? 'rz-rms-missing' : ''}">${esc(droppedBy)}</td>
          </tr>
          <tr>
            <th>Sold By</th><td colspan="9" class="rz-rms-wide ${soldBy === 'No Result' ? 'rz-rms-missing' : ''}">${esc(soldBy)}</td>
          </tr>
        </tbody>
      </table>
      <div class="rz-rms-note">Client-side fields come from the Zero client. Buy/Sell, NPC vendors, Item Script and drops remain n/a until verified server-side data is imported.</div>
    </div>`;

    requestAnimationFrame(() => window.RZ_DECORATE_ITEM_ICONS?.());
    return true;
  }

  function afterRender() {
    requestAnimationFrame(() => requestAnimationFrame(render));
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', afterRender, {once:true});
  else afterRender();
  window.addEventListener('hashchange', afterRender);
  window.RZ_RENDER_RMS_ITEM_DETAIL = render;
})();
