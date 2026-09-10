const fs=require('fs');
const path=require('path');
const vm=require('vm');
const root=path.resolve(__dirname,'../..');
const sandbox={console,setTimeout,clearTimeout};
sandbox.window=sandbox;
sandbox.globalThis=sandbox;
sandbox.RO_DATA={monsters:[],items:[],maps:[]};
const ctx=vm.createContext(sandbox);
for(const rel of [
  'assets/client-monsters-data.js',
  'assets/client-monster-disable-legacy-maps.js',
  'assets/client-monster-identity.js',
  'assets/client-monster-navigation-current.js',
  'assets/client-monster-roster.js',
  'assets/monster-zero-stats.js',
  'assets/monster-zero-consensus.js',
  'assets/rms-monster-behavior.js',
  'assets/client-monsters.js',
  'assets/monster-client-corrections.js',
  'assets/monster-audit-20260909.js',
  'assets/client-monster-current-overlay.js',
  'assets/monster-instance-maps.js'
]) vm.runInContext(fs.readFileSync(path.join(root,rel),'utf8'),ctx,{filename:rel});
const rows=sandbox.RO_DATA.monsters||[];
const roster=sandbox.RZ_CLIENT_MONSTER_ROSTER||[];
const nav=sandbox.RZ_CLIENT_MONSTER_NAV_CURRENT||{};
const byId=id=>rows.find(m=>Number(m?.clientId??m?.id)===Number(id));
const snap=m=>m?{id:Number(m.clientId??m.id),internalName:m.internalName,name:m.name,maps:(m.maps||[]).map(x=>({mapId:x.mapId,amount:x.amount,source:x.source||null}))}:null;
const out={
  rosterCount:roster.length,
  uniqueRosterIds:new Set(roster.map(x=>Number(x?.[0])).filter(Number.isFinite)).size,
  currentNavigationEntries:Object.keys(nav).length,
  legacyDisabled:sandbox.RZ_CLIENT_MONSTER_LEGACY_MAPS_DISABLED===true,
  legacyAudit:sandbox.RZ_CLIENT_MONSTER_LEGACY_MAP_AUDIT||null,
  runtimeAudit:sandbox.RZ_CLIENT_MONSTER_CURRENT_AUDIT||null,
  alice:snap(byId(1275)),
  abysmalKnight:snap(byId(1219))
};
fs.mkdirSync(path.join(root,'audit'),{recursive:true});
fs.writeFileSync(path.join(root,'audit/navigation-debug.json'),JSON.stringify(out,null,2));
console.log(JSON.stringify(out,null,2));
