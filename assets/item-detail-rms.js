(() => {
  'use strict';

  const esc = value => String(value ?? '').replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const has = value => value !== null && value !== undefined && value !== '';
  const fmt = value => has(value) && Number.isFinite(Number(value)) ? Number(value).toLocaleString('en-US') : (has(value) ? String(value) : 'n/a');
  const items = () => Array.isArray(window.RO_DATA?.items) ? window.RO_DATA.items : [];

  function currentItem() {
    const m = location.hash.match(/^#\/(?:items|cards)\/([^?#]+)/i);
    if (!m) return null;
    const token = decodeURIComponent(m[1]);
    const lower = token.replace(/[-_]+/g,' ').toLowerCase();
    return items().find(item => String(item.id) === token || String(item.clientId || '') === token || String(item.name || '').toLowerCase() === lower) || null;
  }

  function field(label, value, cls='') {
    return `<th>${esc(label)}</th><td${cls ? ` class="${cls}"` : ''}>${has(value) ? esc(value) : 'n/a'}</td>`;
  }

  function numberField(label, value, suffix='') {
    return field(label, has(value) ? `${fmt(value)}${suffix}` : 'n/a');
  }

  function combatLabel(item) {
    const bits = [];
    if (has(item.atk)) bits.push(`ATK ${fmt(item.atk)}`);
    if (has(item.matk)) bits.push(`MATK ${fmt(item.matk)}`);
    if (has(item.def)) bits.push(`DEF ${fmt(item.def)}`);
    if (has(item.mdef)) bits.push(`MDEF ${fmt(item.mdef)}`);
    return bits.join(' · ') || 'n/a';
  }

  function ensureStyles() {
    if (document.getElementById('rz-rms-item-style')) return;
    const style = document.createElement('style');
    style.id = 'rz-rms-item-style';
    style.textContent = `
      .rz-rms-wrap{max-width:1120px;margin:0 auto}
      .rz-rms-titlebar{display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding:7px 10px;border:1px solid #6f9fc2;border-bottom:0;background:#cfeafb;color:#064d7d}
      .rz-rms-titlebar h1{display:flex;align-items:center;gap:8px;margin:0;font-family:Georgia,'Times New Roman',serif;font-size:20px;font-weight:700;color:#064d7d}
      .rz-rms-titlebar .rz-rms-slot{font-weight:400;color:#0b4e78}
      .rz-rms-titlebar .rz-rms-class,.rz-rms-titlebar .rz-rms-id{font-size:13px;color:#064d7d}
      .rz-rms-sheet{width:100%;border-collapse:collapse;border:1px solid #5d8fb4;background:#dff1ff;font-size:13px}
      .rz-rms-sheet th,.rz-rms-sheet td{border:1px solid #5d8fb4;padding:5px 7px;vertical-align:top}
      .rz-rms-sheet th{width:118px;background:#cfeafb;color:#064d7d;font-family:Georgia,'Times New Roman',serif;font-size:14px;font-weight:700;white-space:nowrap}
      .rz-rms-sheet td{background:#eaf7ff;color:#063d63}
      .rz-rms-sheet .rz-rms-wide{line-height:1.5;white-space:pre-line}
      .rz-rms-sheet .rz-rms-none{color:#c41818;font-weight:700}
      .rz-rms-sheet code{white-space:pre-wrap;word-break:break-word;color:#17456b}
      .rz-rms-back{margin:0 0 10px;font-size:12px}
      .rz-rms-note{margin-top:10px;color:#54595d;font-size:11px}
      @media(max-width:760px){
        .rz-rms-sheet{font-size:12px}.rz-rms-sheet th{width:92px;font-size:12px}.rz-rms-titlebar h1{font-size:18px}
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

    const slots = item.type === 'Equipment' && has(item.slotCount) ? Number(item.slotCount) : null;
    const slotTitle = slots != null ? ` [${slots}]` : '';
    const buy = has(item.buyPrice) ? `${fmt(item.buyPrice)} Zeny` : 'n/a';
    const sell = has(item.sellPrice) ? `${fmt(item.sellPrice)} Zeny` : 'n/a';
    const refinable = has(item.refinable) ? (item.refinable ? 'Yes' : 'No') : 'n/a';
    const jobs = item.applicableJobs || item.jobs || 'n/a';
    const script = item.itemScript || item.script || 'n/a';
    const droppedBy = item.droppedBy || 'No verified data';
    const soldBy = item.soldBy || item.npcVendors || 'No verified data';
    const description = item.description || 'No description available.';

    main.dataset.rzRmsItem = String(item.id);
    main.innerHTML = `<div class="rz-rms-wrap">
      <div class="rz-rms-back"><a href="#/database/${item.type === 'Card' ? 'cards' : 'items'}">← ${item.type === 'Card' ? 'Card Database' : 'Item Database'}</a></div>
      <div class="rz-rms-titlebar">
        <h1>${esc(item.name)}<span class="rz-rms-slot">${esc(slotTitle)}</span></h1>
        <span class="rz-rms-class">[${esc(item.subtype || item.type || 'Item')}]</span>
        <span class="rz-rms-id">Item ID# ${esc(item.id)}</span>
      </div>
      <table class="rz-rms-sheet">
        <tbody>
          <tr>
            ${field('Type', item.type || 'Item')}
            ${field('Class', item.subtype || 'n/a')}
            ${field('Buy', buy)}
            ${field('Sell', sell)}
            ${numberField('Weight', item.weight)}
          </tr>
          <tr>
            ${field('Combat', combatLabel(item))}
            ${numberField('Required Lv.', item.requiredLevel)}
            ${numberField('Slot', slots)}
            ${numberField('Weapon Lv.', item.weaponLevel)}
            ${field('Element', item.element || 'n/a')}
          </tr>
          <tr>
            ${field('Refinable', refinable, refinable === 'No' ? 'rz-rms-none' : '')}
            <td colspan="8"></td>
          </tr>
          <tr>
            <th>Applicable Jobs</th><td colspan="9" class="rz-rms-wide">${esc(jobs)}</td>
          </tr>
          <tr>
            <th>Description</th><td colspan="9" class="rz-rms-wide">${esc(description)}</td>
          </tr>
          <tr>
            <th>Item Script</th><td colspan="9" class="rz-rms-wide"><code>${esc(script)}</code></td>
          </tr>
          <tr>
            <th>Dropped By</th><td colspan="9" class="rz-rms-wide ${droppedBy === 'No verified data' ? 'rz-rms-none' : ''}">${esc(droppedBy)}</td>
          </tr>
          <tr>
            <th>Sold By</th><td colspan="9" class="rz-rms-wide ${soldBy === 'No verified data' ? 'rz-rms-none' : ''}">${esc(soldBy)}</td>
          </tr>
        </tbody>
      </table>
      <div class="rz-rms-note">Only verified Zero data is displayed. Server-side prices, NPC vendors, scripts and drops remain n/a until a verified server source is imported.</div>
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
