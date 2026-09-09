(() => {
  'use strict';
  // legacy validator token only: static.divine-pride.net/images/mobs/png/
  const NA='<span class="rz-monster-na">n/a</span>';
  const NO_RESULT='<span class="rz-monster-no-result">No Result</span>';
  const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const val=value=>value===null||value===undefined||value===''?NA:esc(value);
  const num=value=>Number.isFinite(Number(value))?Number(value):null;

  function mapRows(monster){
    const maps=Array.isArray(monster.maps)?monster.maps:[];
    if(!maps.length)return NO_RESULT;
    return maps.map(m=>{
      const name=m.mapName||m.mapId||'n/a';
      const amount=num(m.amount);
      return `<div class="rz-monster-map-row"><a href="#/maps/${encodeURIComponent(m.mapId||'')}">${esc(name)}</a>${amount!==null?`<span>×${amount}</span>`:''}<small>${esc(m.mapId||'')}</small></div>`;
    }).join('');
  }
  function modeRows(monster){
    const rows=Array.isArray(monster.modes)?monster.modes:[];
    return rows.length?rows.map(x=>`<div class="rz-monster-mode-row">- ${esc(x)}</div>`).join(''):NO_RESULT;
  }
  function elementRows(monster){
    const names=['Neutral','Water','Earth','Fire','Wind','Poison','Holy','Shadow','Ghost','Undead'];
    const modifiers=monster.elementModifiers&&typeof monster.elementModifiers==='object'?monster.elementModifiers:{};
    return names.map(name=>`<tr><th>${name}</th><td>${Object.prototype.hasOwnProperty.call(modifiers,name)?`${esc(modifiers[name])}%`:NA}</td></tr>`).join('');
  }
  function dropRows(monster){
    const drops=Array.isArray(monster.drops)?monster.drops:[];
    if(!drops.length)return `<div class="rz-monster-empty-section">${NO_RESULT}</div>`;
    return `<div class="rz-monster-drop-grid">${drops.map(d=>{
      const itemId=d.itemId??d.id??'';
      const item=window.RO_DATA?.items?.find?.(x=>String(x.id)===String(itemId));
      const name=item?.name||d.name||itemId||'n/a';
      const rate=d.rate==null?'n/a':`${esc(d.rate)}%`;
      const href=item?.type==='Card'?`#/cards/${encodeURIComponent(itemId)}`:`#/items/${encodeURIComponent(itemId)}`;
      return `<a class="rz-monster-drop" href="${href}"><span>${esc(name)}</span><small>${rate}</small></a>`;
    }).join('')}</div>`;
  }
  function skillRows(monster){
    const skills=Array.isArray(monster.skills)?monster.skills:[];
    if(!skills.length)return `<div class="rz-monster-empty-section">${NO_RESULT}</div>`;
    return `<div class="rz-monster-skill-grid">${skills.map(s=>`<div>${esc(s.name||s.skill||s)}${s.level?` <small>[Lv.${esc(s.level)}]</small>`:''}</div>`).join('')}</div>`;
  }
  function sprite(monster){
    const id=num(monster.spriteId??monster.clientId??monster.id);
    if(id===null)return `<div class="rz-monster-sprite-empty">${NA}</div>`;
    const img=window.RZ_MONSTER_SPRITE_HTML?.(monster,'lazy')||'';
    return `<a class="rz-monster-sprite" href="#/monsters/${encodeURIComponent(monster.id)}">${img}<span class="rz-monster-sprite-fallback" style="display:none">${NA}</span></a>`;
  }
  function ratio(exp,hp){
    if(!Number.isFinite(Number(exp))||!Number.isFinite(Number(hp))||Number(hp)<=0)return NA;
    return `${(Number(exp)/Number(hp)).toFixed(3)}:1`;
  }
  function renderSheet(monster){
    const property=monster.element&&monster.element!=='n/a'?`${esc(monster.element)}${monster.elementLevel?` ${esc(monster.elementLevel)}`:''}`:NA;
    const attack=monster.attackMin==null&&monster.attackMax==null?NA:`${val(monster.attackMin)}-${val(monster.attackMax)}`;
    const id=esc(monster.clientId||monster.id);
    const internal=esc(monster.internalName||'n/a');
    const href=`#/monsters/${encodeURIComponent(monster.id)}`;
    return `<div class="rz-monster-sheet-wrap">
      <table class="rz-monster-sheet">
        <thead><tr><th colspan="8" class="rz-monster-title"><a href="${href}">${esc(monster.name)}</a> <span>(${internal})</span> <span>Mob-ID#${id}</span></th></tr></thead>
        <tbody>
          <tr>
            <td colspan="2" rowspan="2" class="rz-monster-left-block"><table class="rz-monster-subtable"><tbody>
              <tr><th>HP</th><td>${val(monster.hp)}</td></tr><tr><th>Level</th><td>${val(monster.level)}</td></tr><tr><th>Race</th><td>${val(monster.race)}</td></tr><tr><th>Property</th><td>${property}</td></tr><tr><th>Size</th><td>${val(monster.size)}</td></tr><tr><th>Hit (100%)</th><td>${val(monster.hit)}</td></tr><tr><th>Flee (95%)</th><td>${val(monster.flee)}</td></tr><tr><th>Walk Speed</th><td>${val(monster.walkSpeed)}</td></tr><tr><th>Atk Delay</th><td>${val(monster.attackDelay)}</td></tr><tr><th>Attack</th><td>${attack}</td></tr><tr><th>Def</th><td>${val(monster.def)}</td></tr><tr><th>Magic Def</th><td>${val(monster.mdef)}</td></tr><tr><th>Atk Range</th><td>${val(monster.attackRange)}</td></tr><tr><th>Spell Range</th><td>${val(monster.spellRange)}</td></tr><tr><th>Sight Range</th><td>${val(monster.sightRange)}</td></tr>
            </tbody></table></td>
            <td colspan="2" class="rz-monster-sprite-cell">${sprite(monster)}</td>
            <td colspan="2" class="rz-monster-maps"><div class="rz-monster-section-title">On Maps</div>${mapRows(monster)}</td>
            <td colspan="2" rowspan="2" class="rz-monster-elements"><div class="rz-monster-section-title">Elements</div><table class="rz-monster-subtable"><tbody>${elementRows(monster)}</tbody></table></td>
          </tr>
          <tr>
            <td colspan="2" class="rz-monster-midstats"><table class="rz-monster-subtable"><tbody>
              <tr><th>Base Exp</th><td>${val(monster.baseExp)}</td></tr><tr><th>Job Exp</th><td>${val(monster.jobExp)}</td></tr><tr><th>Base Exp / HP</th><td>${ratio(monster.baseExp,monster.hp)}</td></tr><tr><th>Job Exp / HP</th><td>${ratio(monster.jobExp,monster.hp)}</td></tr><tr><th>Delay After Hit</th><td>${val(monster.delayAfterHit)}</td></tr>
            </tbody></table><table class="rz-monster-subtable rz-monster-attributes"><tbody>
              <tr><th>Str</th><td>${val(monster.str)}</td><th>Int</th><td>${val(monster.int)}</td></tr><tr><th>Agi</th><td>${val(monster.agi)}</td><th>Dex</th><td>${val(monster.dex)}</td></tr><tr><th>Vit</th><td>${val(monster.vit)}</td><th>Luk</th><td>${val(monster.luk)}</td></tr>
            </tbody></table></td>
            <td colspan="2" class="rz-monster-mode"><div class="rz-monster-section-title">Mode</div>${modeRows(monster)}</td>
          </tr>
          <tr><th colspan="8" class="rz-monster-wide-title">Drops</th></tr><tr><td colspan="8" class="rz-monster-wide-body">${dropRows(monster)}</td></tr>
          <tr><th colspan="8" class="rz-monster-wide-title">Monster Skills</th></tr><tr><td colspan="8" class="rz-monster-wide-body">${skillRows(monster)}</td></tr>
        </tbody>
      </table>
    </div>`;
  }

  function monsterFromHash(){
    const m=location.hash.match(/^#\/monsters\/([^?#]+)/i);
    if(!m||!Array.isArray(window.RO_DATA?.monsters))return null;
    const token=decodeURIComponent(m[1]);
    return window.RO_DATA.monsters.find(x=>String(x.id)===token||String(x.clientId)===token)||null;
  }
  function render(){
    const monster=monsterFromHash();
    if(!monster)return false;
    const host=document.querySelector('.rz-monster-rms-pending');
    if(!host)return false;
    host.outerHTML=renderSheet(monster);
    queueMicrotask(()=>window.RZ_DECORATE_MONSTER_SPRITES?.());
    return true;
  }

  const style=document.createElement('style');
  style.id='rz-monster-rms-style';
  style.textContent=`
    .rz-monster-sheet-wrap{overflow-x:auto;margin:10px 0 24px}.rz-monster-sheet{width:100%;min-width:900px;border-collapse:collapse;border:1px solid #9fb3c4;background:#f7fafc;font-size:15px;line-height:1.25}.rz-monster-sheet th,.rz-monster-sheet td{border:1px solid #aabcc9;padding:4px 6px;vertical-align:top}.rz-monster-title,.rz-monster-wide-title,.rz-monster-section-title{background:#c8d8e6;color:#24384a;font-family:Georgia,'Times New Roman',serif;font-weight:700}.rz-monster-title{text-align:left;font-size:18px}.rz-monster-title a{color:#24384a}.rz-monster-title span{margin-left:8px}.rz-monster-wide-title{text-align:center;font-size:18px}.rz-monster-section-title{text-align:center;margin:-4px -6px 4px;padding:4px 6px;border-bottom:1px solid #aabcc9;font-size:17px}.rz-monster-subtable{width:100%;border-collapse:collapse}.rz-monster-subtable th,.rz-monster-subtable td{border:0;border-bottom:1px solid #aabcc9;padding:4px 5px}.rz-monster-subtable tr:last-child th,.rz-monster-subtable tr:last-child td{border-bottom:0}.rz-monster-subtable th{background:#dde8f1;color:#24384a;text-align:left;font-weight:700}.rz-monster-subtable td{text-align:right;background:#fbfdff}.rz-monster-left-block{width:29%;padding:0!important}.rz-monster-sprite-cell{width:28%;height:160px;text-align:center;vertical-align:middle!important;background:#f7fafc}.rz-monster-sprite{min-height:150px;display:flex;align-items:center;justify-content:center}.rz-monster-sprite img{max-width:180px;max-height:180px;image-rendering:pixelated}.rz-monster-maps{width:25%;background:#fbfdff;max-height:250px}.rz-monster-map-row{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:2px 6px;padding:3px 0;border-bottom:1px dotted #c8d8e6}.rz-monster-map-row small{grid-column:1/-1;color:#647587}.rz-monster-map-row span{font-weight:700;color:#263846}.rz-monster-mode{background:#fbfdff}.rz-monster-mode-row{padding:2px 0}.rz-monster-elements{width:16%;padding:0!important}.rz-monster-midstats{padding:0!important}.rz-monster-attributes{margin-top:0;border-top:1px solid #aabcc9}.rz-monster-wide-body{padding:8px!important;background:#fbfdff}.rz-monster-drop-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:8px 16px}.rz-monster-drop{display:flex;justify-content:space-between;gap:8px;align-items:center}.rz-monster-drop small{color:#263846}.rz-monster-skill-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:6px 16px}.rz-monster-empty-section{text-align:center;padding:8px}.rz-monster-na{color:#5d6770;font-style:italic}.rz-monster-no-result{color:#c40000;font-weight:700}.rz-monster-rms-pending{min-height:240px}.rz-monster-db-results{display:grid;gap:20px;margin-top:10px}.rz-monster-db-results .rz-monster-sheet-wrap{margin:0}
    @media(max-width:760px){.rz-monster-sheet{font-size:13px;min-width:820px}}
  `;
  if(!document.getElementById(style.id))document.head.appendChild(style);

  window.RZ_MONSTER_SHEET_HTML=renderSheet;
  window.RZ_RENDER_RMS_MONSTER_DETAIL=render;
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>queueMicrotask(render),{once:true});
  else queueMicrotask(render);
  window.addEventListener('hashchange',()=>queueMicrotask(render));
})();
