const fs=require('fs');
const path=require('path');
const vm=require('vm');

const root=path.resolve(__dirname,'../..');
const sandbox={console,setTimeout,clearTimeout};
sandbox.window=sandbox;
sandbox.globalThis=sandbox;
sandbox.RO_DATA={monsters:[],items:[],maps:[]};
const ctx=vm.createContext(sandbox);
const files=[
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
  'assets/monster-verified-skill-associations.js',
  'assets/monster-instance-maps.js',
  'assets/monster-strict-verification.js',
  'assets/monster-roster-classification.js'
];
for(const rel of files){
  const p=path.join(root,rel);
  if(!fs.existsSync(p))throw new Error(`Missing ${rel}`);
  vm.runInContext(fs.readFileSync(p,'utf8'),ctx,{filename:rel});
}

const roster=Array.isArray(sandbox.RZ_CLIENT_MONSTER_ROSTER)?sandbox.RZ_CLIENT_MONSTER_ROSTER:[];
const monsters=Array.isArray(sandbox.RO_DATA?.monsters)?sandbox.RO_DATA.monsters:[];
const overrides=sandbox.RZ_MONSTER_ROSTER_CLASSIFICATION_OVERRIDES||{};
if(roster.length!==598)throw new Error(`Expected 598 roster entries, got ${roster.length}`);
const byId=new Map(monsters.map(m=>[Number(m?.clientId??m?.id),m]));
const required=['HP','ATK','MATK','DEF','MDEF','HIT','FLEE','Base EXP','Job EXP','Walk Speed','Maps','Drops','Skills'];
const known=v=>v!==null&&v!==undefined&&v!==''&&!/^n\/?a$/i.test(String(v).trim())&&String(v).trim()!=='—';
const pair=(a,b)=>known(a)||known(b);

function baseCategory(name){
  const key=String(name||'').trim().toUpperCase();
  if(/^(?:S_)?DUMMY_/.test(key)||/^TESTMON$/.test(key)||/^HIDDEN_MOB\d*$/.test(key)||key==='GUILD_SKILL_FLAG')return 'placeholder';
  if(/_BULLET$/.test(key))return 'projectile';
  if(/^(?:MQ_|QE_|TUTO_)/.test(key))return 'quest';
  if(/^MD_/.test(key))return 'instance';
  if(/^(?:ZG_E_|ZTW_|GP_|E_)/.test(key))return 'event';
  if(/^CLB_/.test(key))return 'club';
  if(/^(?:G_|C[1-5]_|R_|B_)/.test(key)||/_MJ$/.test(key))return 'variant';
  if(/^\d/.test(key))return 'special';
  return 'normal';
}
function category(id,name){return overrides[String(id)]?.category||baseCategory(name);}
function missing(m){
  const out=[];
  if(!known(m?.hp))out.push('HP');
  if(!pair(m?.attackMin,m?.attackMax))out.push('ATK');
  if(!pair(m?.magicAttackMin,m?.magicAttackMax))out.push('MATK');
  if(!known(m?.def))out.push('DEF');
  if(!known(m?.mdef))out.push('MDEF');
  if(!known(m?.hit))out.push('HIT');
  if(!known(m?.flee))out.push('FLEE');
  if(!known(m?.baseExp))out.push('Base EXP');
  if(!known(m?.jobExp))out.push('Job EXP');
  if(!known(m?.walkSpeed))out.push('Walk Speed');
  if(!(Array.isArray(m?.maps)&&m.maps.length))out.push('Maps');
  if(!(Array.isArray(m?.drops)&&m.drops.length))out.push('Drops');
  if(!(Array.isArray(m?.skills)&&m.skills.length))out.push('Skills');
  return out;
}

const rows=roster.map(r=>{
  const id=Number(r[0]),internalName=String(r[1]||''),m=byId.get(id);
  if(!m)throw new Error(`Roster #${id} missing from runtime`);
  if(!m.strictVerificationApplied)throw new Error(`Strict layer missing on #${id}`);
  return {id,internalName,name:m.name||internalName,category:category(id,internalName),missing:missing(m)};
});
const normal=rows.filter(r=>r.category==='normal');
const normalIncomplete=normal.filter(r=>r.missing.length);
const counts=Object.fromEntries(required.map(f=>[f,normalIncomplete.filter(r=>r.missing.includes(f)).length]));
const consensus=sandbox.RZ_MONSTER_ZERO_CONSENSUS||{};
let strictFields=0,strictDrops=0;
for(const [id,rec] of Object.entries(consensus)){
  for(const [field,meta] of Object.entries(rec.fields||{})){
    if(meta?.status!=='strict-consensus'||new Set(meta?.verifiedSources||[]).size<2)throw new Error(`Non-strict field ${id}/${field}`);
    strictFields++;
  }
  for(const drop of rec.drops||[]){
    if(drop?.relationVerified!==true||new Set(drop?.verifiedSources||[]).size<2)throw new Error(`Non-strict drop relation ${id}`);
    strictDrops++;
  }
}
const result={
  generatedAt:new Date().toISOString(),
  policy:'client exact identity/Navi + at least two independent Ragnarok Zero databases for server data',
  roster:rows.length,
  normal:normal.length,
  normalComplete:normal.length-normalIncomplete.length,
  normalIncomplete:normalIncomplete.length,
  normalMissingFieldCounts:counts,
  strictExternalMonsters:Object.keys(consensus).length,
  strictExternalFields:strictFields,
  strictDropRelations:strictDrops,
  incomplete:normalIncomplete
};
fs.mkdirSync(path.join(root,'audit'),{recursive:true});
fs.writeFileSync(path.join(root,'audit/monster-strict-audit.json'),JSON.stringify(result,null,2));
console.log(JSON.stringify({...result,incomplete:undefined},null,2));
