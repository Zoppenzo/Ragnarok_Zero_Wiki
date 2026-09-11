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
  'assets/client-monster-navigation-metadata.js',
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
const rosterIds=new Set(roster.map(r=>Number(r[0])));
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
function fieldCounts(subset){
  return Object.fromEntries(required.map(f=>[f,subset.filter(r=>r.missing.includes(f)).length]));
}
function snapshot(m){
  return {
    id:Number(m?.clientId??m?.id), internalName:m?.internalName||'', name:m?.name||'',
    level:m?.level??null, race:m?.race??null, size:m?.size??null,
    element:m?.element??null, elementLevel:m?.elementLevel??null, propertyCode:m?.propertyCode??null,
    hp:m?.hp??null, attackMin:m?.attackMin??null, attackMax:m?.attackMax??null,
    magicAttackMin:m?.magicAttackMin??null, magicAttackMax:m?.magicAttackMax??null,
    def:m?.def??null, mdef:m?.mdef??null, hit:m?.hit??null, flee:m?.flee??null,
    baseExp:m?.baseExp??null, jobExp:m?.jobExp??null, walkSpeed:m?.walkSpeed??null,
    maps:Array.isArray(m?.maps)?m.maps.length:0, drops:Array.isArray(m?.drops)?m.drops.length:0,
    skills:Array.isArray(m?.skills)?m.skills.length:0
  };
}

const rows=roster.map(r=>{
  const id=Number(r[0]),internalName=String(r[1]||''),m=byId.get(id);
  if(!m)throw new Error(`Roster #${id} missing from runtime`);
  if(!m.strictVerificationApplied)throw new Error(`Strict layer missing on #${id}`);
  return {id,internalName,name:m.name||internalName,category:category(id,internalName),missing:missing(m)};
});
const allIncomplete=rows.filter(r=>r.missing.length);
const normal=rows.filter(r=>r.category==='normal');
const normalIncomplete=normal.filter(r=>r.missing.length);

const categoryNames=[...new Set(rows.map(r=>r.category))].sort();
const categories={};
for(const cat of categoryNames){
  const subset=rows.filter(r=>r.category===cat);
  const incomplete=subset.filter(r=>r.missing.length);
  categories[cat]={
    total:subset.length,
    complete:subset.length-incomplete.length,
    incomplete:incomplete.length,
    missingFieldCounts:fieldCounts(incomplete)
  };
}
if(Object.values(categories).reduce((sum,x)=>sum+x.total,0)!==598)throw new Error('Category totals do not equal roster');

const consensus=sandbox.RZ_MONSTER_ZERO_CONSENSUS||{};
let strictFields=0,strictDrops=0,strictDropsWithRate=0,strictDropsUnknownRate=0;
for(const [id,rec] of Object.entries(consensus)){
  for(const [field,meta] of Object.entries(rec.fields||{})){
    if(meta?.status!=='strict-consensus'||new Set(meta?.verifiedSources||[]).size<2)throw new Error(`Non-strict field ${id}/${field}`);
    strictFields++;
  }
  for(const drop of rec.drops||[]){
    if(drop?.relationVerified!==true||new Set(drop?.verifiedSources||[]).size<2)throw new Error(`Non-strict drop relation ${id}`);
    strictDrops++;
    if(drop.rate===null||drop.rate===undefined)strictDropsUnknownRate++; else strictDropsWithRate++;
  }
}

const digitPrefixed=rows.filter(r=>/^\d/.test(r.internalName)).map(r=>({id:r.id,internalName:r.internalName,name:r.name}));
const extraRuntime=monsters.filter(m=>!rosterIds.has(Number(m?.clientId??m?.id))).map(snapshot);
const boulders=[25327,25328,25329,25336].map(id=>snapshot(byId.get(id)));
const argos=byId.get(1100),ak=byId.get(1219);
const regressions={
  argos:{drops:Array.isArray(argos?.drops)?argos.drops.length:0,hasSpiderWings:Boolean(argos?.drops?.some(d=>Number(d.itemId)===480573))},
  abysmalKnight:{drops:Array.isArray(ak?.drops)?ak.drops.length:0,hasAbyssHelm:Boolean(ak?.drops?.some(d=>Number(d.itemId)===401072)),hasLance:Boolean(ak?.drops?.some(d=>Number(d.itemId)===630036))},
  boulderDwarfs:boulders
};
if(!regressions.argos.hasSpiderWings)throw new Error('Argos Spider Wings regression');
if(regressions.abysmalKnight.drops<8||!regressions.abysmalKnight.hasAbyssHelm||!regressions.abysmalKnight.hasLance)throw new Error('Abysmal Knight drops regression');

const expectedBoulderServer={25327:[32952,198,15],25328:[55602,179,30],25329:[54704,224,23]};
for(const [id,vals] of Object.entries(expectedBoulderServer)){
  const m=byId.get(Number(id));
  if(Number(m?.hp)!==vals[0]||Number(m?.def)!==vals[1]||Number(m?.mdef)!==vals[2])throw new Error(`Boulder Dwarf #${id} verified stats regression`);
}
const expectedBoulderClient={
  25327:{level:64,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:2,propertyCode:42},
  25328:{level:65,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:2,propertyCode:42},
  25329:{level:64,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:3,propertyCode:62},
  25336:{level:64,race:'Demi-Human',size:'Medium',element:'Earth',elementLevel:3,propertyCode:62}
};
for(const [id,expected] of Object.entries(expectedBoulderClient)){
  const m=byId.get(Number(id));
  for(const [field,value] of Object.entries(expected)){
    if(m?.[field]!==value)throw new Error(`Boulder Dwarf #${id} client Navi ${field} regression: expected ${value}, got ${m?.[field]}`);
  }
  if(m?.clientVerified!==true)throw new Error(`Boulder Dwarf #${id} is not marked client verified`);
}
const sword=byId.get(25336);
if(known(sword?.hp)||known(sword?.def)||known(sword?.mdef))throw new Error('Boulder Dwarf Swordmaster must remain unknown for HP/DEF/MDEF');

const result={
  generatedAt:new Date().toISOString(),
  policy:'client exact identity/Navi + at least two independent Ragnarok Zero databases for server data',
  runtimeMonsters:monsters.length,
  roster:rows.length,
  extraRuntime,
  complete:rows.length-allIncomplete.length,
  incomplete:allIncomplete.length,
  allMissingFieldCounts:fieldCounts(allIncomplete),
  categories,
  normal:normal.length,
  normalComplete:normal.length-normalIncomplete.length,
  normalIncomplete:normalIncomplete.length,
  normalMissingFieldCounts:fieldCounts(normalIncomplete),
  strictExternalMonsters:Object.keys(consensus).length,
  strictExternalFields:strictFields,
  strictDropRelations:strictDrops,
  strictDropRelationsWithVerifiedRate:strictDropsWithRate,
  strictDropRelationsWithUnknownRate:strictDropsUnknownRate,
  digitPrefixedSpecialCount:digitPrefixed.length,
  digitPrefixedSpecial:digitPrefixed,
  regressions,
  incompleteRows:allIncomplete
};
fs.mkdirSync(path.join(root,'audit'),{recursive:true});
fs.writeFileSync(path.join(root,'audit/monster-strict-audit.json'),JSON.stringify(result,null,2));
console.log(JSON.stringify({
  generatedAt:result.generatedAt,policy:result.policy,runtimeMonsters:result.runtimeMonsters,roster:result.roster,
  complete:result.complete,incomplete:result.incomplete,allMissingFieldCounts:result.allMissingFieldCounts,
  categories:result.categories,normal:result.normal,normalComplete:result.normalComplete,normalIncomplete:result.normalIncomplete,
  normalMissingFieldCounts:result.normalMissingFieldCounts,strictExternalMonsters:result.strictExternalMonsters,
  strictExternalFields:result.strictExternalFields,strictDropRelations:result.strictDropRelations,
  strictDropRelationsWithVerifiedRate:result.strictDropRelationsWithVerifiedRate,
  strictDropRelationsWithUnknownRate:result.strictDropRelationsWithUnknownRate,
  digitPrefixedSpecialCount:result.digitPrefixedSpecialCount,regressions:result.regressions
},null,2));
