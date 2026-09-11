(() => {
  'use strict';

  const normalize = value => String(value || '').normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,'');
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const numericRate = value => value!==null&&value!==undefined&&value!==''&&Number.isFinite(Number(value));

  function buildIndex(){
    const items = Array.isArray(window.RO_DATA?.items) ? window.RO_DATA.items : [];
    const monsters = Array.isArray(window.RO_DATA?.monsters) ? window.RO_DATA.monsters : [];
    const itemsById = new Map();
    const itemsByName = new Map();
    for(const item of items){
      const ids=[item?.id,item?.clientId].filter(v=>v!==null&&v!==undefined&&String(v)!=='');
      ids.forEach(id=>itemsById.set(String(id),item));
      const n=normalize(item?.name);
      if(n&&!itemsByName.has(n))itemsByName.set(n,item);
      item.droppedBy=[];
    }

    for(const monster of monsters){
      const monsterId=String(monster?.clientId??monster?.id??'');
      if(!monsterId)continue;
      for(const drop of (Array.isArray(monster?.drops)?monster.drops:[])){
        // Only strict two-database relations may reach item pages.
        if(drop?.relationVerified!==true && drop?.status!=='strict-consensus')continue;
        let item=null;
        if(drop?.itemId!==null&&drop?.itemId!==undefined)item=itemsById.get(String(drop.itemId))||null;
        if(!item&&drop?.name)item=itemsByName.get(normalize(drop.name))||null;
        if(!item)continue;
        const list=Array.isArray(item.droppedBy)?item.droppedBy:(item.droppedBy=[]);
        if(list.some(row=>String(row.monsterId)===monsterId))continue;
        const hasRate=numericRate(drop?.rate);
        list.push({
          monsterId,
          monsterName:monster?.name||monster?.internalName||`Mob ${monsterId}`,
          rate:hasRate?Number(drop.rate):null,
          relationVerified:true,
          rateVerified:hasRate,
        });
      }
    }

    for(const item of items){
      if(Array.isArray(item.droppedBy))item.droppedBy.sort((a,b)=>(b.rate??-1)-(a.rate??-1)||String(a.monsterName).localeCompare(String(b.monsterName)));
    }
    window.RZ_ITEM_DROP_INDEX_READY=true;
  }

  function currentItem(){
    const match=String(location.hash||'').match(/^#\/items\/([^?#/]+)/i);
    if(!match)return null;
    const token=decodeURIComponent(match[1]);
    return (window.RO_DATA?.items||[]).find(item=>String(item?.id)===token||String(item?.clientId)===token)||null;
  }

  function render(){
    if(typeof document==='undefined'||typeof location==='undefined')return;
    const old=document.getElementById('rz-item-dropped-by');
    if(old)old.remove();
    const item=currentItem();
    if(!item)return;
    const host=document.querySelector('.main-content');
    if(!host)return;

    const fr=String(document.documentElement.lang||'').toLowerCase().startsWith('fr');
    const title=fr?'Monstres qui drop cet objet':'Monsters that drop this item';
    const monsterLabel=fr?'Monstre':'Monster';
    const rateLabel=fr?'Taux de drop':'Drop rate';
    const rows=Array.isArray(item.droppedBy)?item.droppedBy:[];
    const section=document.createElement('section');
    section.id='rz-item-dropped-by';
    section.innerHTML=`<h2>${esc(title)}</h2>${rows.length?`
      <div class="table-wrap"><table class="rz-item-drop-table">
        <thead><tr><th>${esc(monsterLabel)}</th><th>${esc(rateLabel)}</th></tr></thead>
        <tbody>${rows.map(row=>`<tr><td><a href="#/monsters/${encodeURIComponent(row.monsterId)}">${esc(row.monsterName)}</a> <small>Mob-ID#${esc(row.monsterId)}</small></td><td>${row.rate==null?'???':`${esc(row.rate)}%`}</td></tr>`).join('')}</tbody>
      </table></div>`:'<p>???</p>'}`;
    host.appendChild(section);
  }

  function refresh(){
    buildIndex();
    if(typeof setTimeout==='function'){
      setTimeout(render,0);
      setTimeout(render,80);
    }
  }

  // Build the inverse database immediately so every item object has droppedBy,
  // even outside the visible item-detail route.
  buildIndex();

  if(typeof document!=='undefined'){
    if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',refresh,{once:true});
    else refresh();
    window.addEventListener('hashchange',refresh);
    const observer=new MutationObserver(()=>{
      if(/^#\/items\//i.test(String(location.hash||''))&&!document.getElementById('rz-item-dropped-by'))setTimeout(render,0);
    });
    observer.observe(document.documentElement,{childList:true,subtree:true});
  }

  window.RZ_REBUILD_ITEM_DROP_INDEX=refresh;
})();
