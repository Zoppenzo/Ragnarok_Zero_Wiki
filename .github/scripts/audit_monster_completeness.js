const fs=require('fs');
const path=require('path');
const vm=require('vm');

const root=path.resolve(__dirname,'../..');
const sandbox={console, setTimeout, clearTimeout};
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
  'assets/monster-instance-maps.js'
];
for(const rel of files){
  const p=path.join(root,rel);
  if(!fs.existsSync(p)) throw new Error('Missing '+rel);
  vm.runInContext(fs.readFileSync(p,'utf8'),ctx,{filename:rel});
}

const monsters=Array.isArray(sandbox.RO_DATA.monsters)?sandbox.RO_DATA.monsters:[];
const identity=sandbox.RZ_CLIENT_MONSTER_IDENTITY||{};
const roster=Array.isArray(sandbox.RZ_CLIENT_MONSTER_ROSTER)?sandbox.RZ_CLIENT_MONSTER_ROSTER:[];
const nav=sandbox.RZ_CLIENT_MONSTER_NAV_CURRENT||{};
const navAudit=sandbox.RZ_CLIENT_MONSTER_CURRENT_AUDIT||{};
const races=['Formless','Undead','Brute','Plant','Insect','Fish','Demon','Demi-Human','Angel','Dragon'];
const sizes=['Small','Medium','Large'];
const elements=['Neutral','Water','Earth','Fire','Wind','Poison','Holy','Shadow','Ghost','Undead'];
const requiredFields=['HP','ATK','MATK','DEF','MDEF','HIT','FLEE','Base EXP','Job EXP','Walk Speed','Maps','Drops','Skills'];
const known=v=>v!==null&&v!==undefined&&v!==''&&!/^n\/?a$/i.test(String(v).trim())&&String(v).trim()!=='—';
const pairKnown=(a,b)=>known(a)||known(b);
const byId=id=>monsters.find(m=>Number(m?.clientId??m?.id)===Number(id));
const mapIds=m=>(Array.isArray(m?.maps)?m.maps:[]).map(x=>String(x?.mapId||''));
const useful=m=>[
  m.hp,m.level,m.race,m.element,m.size,m.hit,m.flee,m.walkSpeed,m.def,m.mdef,m.baseExp,m.jobExp
].some(known)||pairKnown(m.attackMin,m.attackMax)||pairKnown(m.magicAttackMin,m.magicAttackMax)||
(Array.isArray(m.maps)&&m.maps.length)||(Array.isArray(m.drops)&&m.drops.length)||(Array.isArray(m.skills)&&m.skills.length)||(Array.isArray(m.modes)&&m.modes.length)||m.clientRosterPresent;

function classifyInternalName(value){
  const key=String(value||'').trim().toUpperCase();
  if(!key)return 'unknown';

  // Deliberately conservative. These are workflow buckets, not claims that a
  // monster is absent from the live server. Nothing is hidden or deleted here.
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

function missing(m){
  const out=[];
  if(!known(m.hp))out.push('HP');
  if(!pairKnown(m.attackMin,m.attackMax))out.push('ATK');
  if(!pairKnown(m.magicAttackMin,m.magicAttackMax))out.push('MATK');
  if(!known(m.def))out.push('DEF');
  if(!known(m.mdef))out.push('MDEF');
  if(!known(m.hit))out.push('HIT');
  if(!known(m.flee))out.push('FLEE');
  if(!known(m.baseExp))out.push('Base EXP');
  if(!known(m.jobExp))out.push('Job EXP');
  if(!known(m.walkSpeed))out.push('Walk Speed');
  if(!(Array.isArray(m.maps)&&m.maps.length))out.push('Maps');
  if(!(Array.isArray(m.drops)&&m.drops.length))out.push('Drops');
  if(!(Array.isArray(m.skills)&&m.skills.length))out.push('Skills');
  return out;
}

function countMissingFields(rows){
  const counts=Object.fromEntries(requiredFields.map(k=>[k,0]));
  for(const row of rows){
    for(const field of row.missing||[]){
      counts[field]=(counts[field]||0)+1;
    }
  }
  return counts;
}

// Current-client navigation invariants. The Navi row's first numeric value is
// deliberately NOT used as a Mob-ID. Exact internal identity is the join key.
if(sandbox.RZ_CLIENT_MONSTER_LEGACY_MAPS_DISABLED!==true){
  throw new Error('Legacy pseudo-ID map source was not disabled before monster construction');
}
if(roster.length!==598){
  throw new Error(`Expected 598 sprite-backed client identities, got ${roster.length}`);
}
if(navAudit.rosterCount!==598 || navAudit.uniqueRosterIds!==598 || navAudit.rosterMissingFromRuntime?.length){
  throw new Error(`Full client roster was not preserved in runtime: ${JSON.stringify(navAudit)}`);
}
if(navAudit.legacyMapsRemaining!==0){
  throw new Error(`Obsolete client-navigation maps survived: ${navAudit.legacyMapsRemaining}`);
}
if((navAudit.currentNavigationApplied||0)+(navAudit.currentNavigationMissing||0)!==roster.length){
  throw new Error(`Every roster identity must be accounted for by exact-name Navi join or explicit no-Navi state: ${JSON.stringify(navAudit)}`);
}
// With the supplied current client extraction, 399 of the 400 Navi identities
// are present in the 598 sprite-backed roster. Do not regress below that known
// coverage. Numeric mismatches are expected and are reported separately.
if((navAudit.currentNavigationApplied||0)<399){
  throw new Error(`Current internal-name Navi coverage regressed: ${navAudit.currentNavigationApplied}`);
}

const alice=byId(1275);
if(!alice || alice.internalName!=='ALICE') throw new Error('Mob-ID 1275 must resolve to ALICE');
const aliceMaps=mapIds(alice);
if(!aliceMaps.length || aliceMaps.some(x=>!/^gl_/i.test(x))){
  throw new Error(`Alice must use only current Glast Heim Navi maps, got ${aliceMaps.join(',')}`);
}
if(!aliceMaps.includes('gl_cas01') || !aliceMaps.includes('gl_knt01')){
  throw new Error(`Alice current Navi sample maps missing: ${aliceMaps.join(',')}`);
}

const abyss=byId(1219);
if(!abyss || abyss.internalName!=='KNIGHT_OF_ABYSS') throw new Error('Mob-ID 1219 must resolve to KNIGHT_OF_ABYSS');
const abyssMaps=mapIds(abyss);
if(!abyssMaps.length || abyssMaps.some(x=>!/^gl/i.test(x))){
  throw new Error(`Abysmal Knight must use only Glast Heim current Navi maps, got ${abyssMaps.join(',')}`);
}
if(!abyssMaps.includes('gl_knt01') || !abyssMaps.includes('gl_knt02') || !abyssMaps.includes('gl_cas02')){
  throw new Error(`Abysmal Knight current Navi sample maps missing: ${abyssMaps.join(',')}`);
}

const rosterClassification=roster.map(row=>({
  id:Number(row?.[0]),
  internalName:String(row?.[1]||''),
  sprite:String(row?.[2]||''),
  category:classifyInternalName(row?.[1])
}));
const classificationCounts=rosterClassification.reduce((acc,row)=>{
  acc[row.category]=(acc[row.category]||0)+1;
  return acc;
},{});
if(rosterClassification.length!==598 || Object.values(classificationCounts).reduce((a,b)=>a+b,0)!==598){
  throw new Error('Roster classification must account for all 598 sprite-backed identities');
}

const visible=monsters.filter(useful);
const incomplete=visible.map(m=>({
  id:Number(m.clientId||m.id),internalName:m.internalName||'',name:m.name||'',missing:missing(m),
  category:classifyInternalName(m.internalName),
  memorial:/^MD_/i.test(String(m.internalName||'')),
  instanceLabel:m.instanceLabel||null,
  dwarf:/BOULDERDWARF|NORDIUM|PORING_GEM|APARGREL/i.test(String(m.internalName||''))
})).filter(x=>x.missing.length).sort((a,b)=>b.missing.length-a.missing.length||a.id-b.id);

const incompleteByCategory=incomplete.reduce((acc,row)=>{
  acc[row.category]=(acc[row.category]||0)+1;
  return acc;
},{});
const normalIncomplete=incomplete.filter(x=>x.category==='normal');
const missingFieldCounts=countMissingFields(incomplete);
const normalMissingFieldCounts=countMissingFields(normalIncomplete);
const normalComplete=(classificationCounts.normal||0)-normalIncomplete.length;
const normalFullyBlank=normalIncomplete.filter(x=>x.missing.length===requiredFields.length);
const normalNearlyComplete=normalIncomplete.filter(x=>x.missing.length<=2);
const normalOnlyExpMissing=normalIncomplete.filter(x=>x.missing.length>0&&x.missing.every(f=>f==='Base EXP'||f==='Job EXP'));
const normalMissingDistribution=normalIncomplete.reduce((acc,row)=>{
  const n=row.missing.length;
  acc[n]=(acc[n]||0)+1;
  return acc;
},{});

const contradictions=[];
for(const m of visible){
  const key=String(m.internalName||'');
  const c=identity[key];
  if(!Array.isArray(c)||c.length<5)continue;
  const [cid,level,raceCode,sizeCode,propertyCode]=c.map(Number);
  const expected={
    id:cid,level,
    race:races[raceCode]||null,
    size:sizes[sizeCode]||null,
    element:elements[((propertyCode%20)+20)%20]||null,
    elementLevel:Math.floor(propertyCode/20)||null
  };
  const actual={id:Number(m.clientId||m.id),level:Number(m.level),race:m.race||null,size:m.size||null,element:m.element||null,elementLevel:m.elementLevel==null?null:Number(m.elementLevel)};
  const diff={};
  for(const k of Object.keys(expected)){
    if(expected[k]===null)continue;
    if(String(actual[k])!==String(expected[k]))diff[k]={client:expected[k],wiki:actual[k]};
  }
  if(Object.keys(diff).length)contradictions.push({id:actual.id,internalName:key,name:m.name||'',diff});
}
contradictions.sort((a,b)=>a.id-b.id);

const summary={
  generatedAt:new Date().toISOString(),
  totalRuntime:monsters.length,
  totalVisible:visible.length,
  totalIncomplete:incomplete.length,
  totalNormalIncomplete:normalIncomplete.length,
  totalNormalComplete:normalComplete,
  totalNormalFullyBlank:normalFullyBlank.length,
  totalNormalNearlyComplete:normalNearlyComplete.length,
  totalNormalOnlyExpMissing:normalOnlyExpMissing.length,
  totalClientContradictions:contradictions.length,
  rosterCount:roster.length,
  rosterClassification:classificationCounts,
  incompleteByCategory,
  missingFieldCounts,
  normalMissingFieldCounts,
  normalMissingDistribution,
  currentNavigationEntries:Object.keys(nav).length,
  currentNavigationApplied:navAudit.currentNavigationApplied||0,
  currentNavigationMissing:navAudit.currentNavigationMissing||0,
  legacyNumericIdMismatch:navAudit.legacyNumericIdMismatch||0,
  legacyMapsRemaining:navAudit.legacyMapsRemaining||0,
  aliceMaps,
  abysmalKnightMaps:abyssMaps
};
const out={summary,navigationAudit:navAudit,rosterClassification,incomplete,normalFullyBlank,normalNearlyComplete,normalOnlyExpMissing,contradictions};
fs.mkdirSync(path.join(root,'audit'),{recursive:true});
fs.writeFileSync(path.join(root,'audit/monster-data-audit.json'),JSON.stringify(out,null,2));

const categoryOrder=['normal','variant','instance','quest','event','club','placeholder','projectile','special','unknown'];
const categoryLines=categoryOrder.filter(k=>classificationCounts[k]).map(k=>`- ${k}: **${classificationCounts[k]}**${incompleteByCategory[k]?` · incomplete: **${incompleteByCategory[k]}**`:''}`);
const fieldLines=requiredFields.map(k=>`- ${k}: **${missingFieldCounts[k]||0}** missing overall · **${normalMissingFieldCounts[k]||0}** missing among normal/world candidates`);
const lines=[
  '# Monster data audit','',
  `Generated: ${summary.generatedAt}`,'',
  `- Runtime monster rows: **${summary.totalRuntime}**`,
  `- Sprite-backed client roster: **${summary.rosterCount}**`,
  `- Current Navi entries: **${summary.currentNavigationEntries}**`,
  `- Current Navi entries applied by exact internal name: **${summary.currentNavigationApplied}**`,
  `- Roster identities without current Navi: **${summary.currentNavigationMissing}**`,
  `- Navi numeric-field mismatches intentionally ignored: **${summary.legacyNumericIdMismatch}**`,
  `- Legacy maps remaining: **${summary.legacyMapsRemaining}**`,
  `- Rows with useful data (visible): **${summary.totalVisible}**`,
  `- Visible rows still incomplete: **${summary.totalIncomplete}**`,
  `- Normal/world candidates complete: **${summary.totalNormalComplete}/${classificationCounts.normal||0}**`,
  `- Normal/world candidates still incomplete: **${summary.totalNormalIncomplete}**`,
  `- Normal/world candidates with all ${requiredFields.length} tracked fields missing: **${summary.totalNormalFullyBlank}**`,
  `- Normal/world candidates missing only 1-2 fields: **${summary.totalNormalNearlyComplete}**`,
  `- Normal/world candidates missing only Base/Job EXP: **${summary.totalNormalOnlyExpMissing}**`,
  `- Direct contradictions with client identity table: **${summary.totalClientContradictions}**`,'',
  '## Missing-field counts','',
  ...fieldLines,'',
  '## Roster classification','',
  ...categoryLines,'',
  '> Classification is conservative workflow metadata only. It does not hide, delete, or claim that a client identity is absent from the live server.','',
  '## Navigation regression checks','',
  `- **#1275 Alice** — ${aliceMaps.join(', ')}`,
  `- **#1219 Abysmal Knight** — ${abyssMaps.join(', ')}`,'',
  '## Client contradictions',''
];
if(!contradictions.length)lines.push('None.');
else contradictions.forEach(x=>lines.push(`- **#${x.id} ${x.name} (${x.internalName})** — ${Object.entries(x.diff).map(([k,v])=>`${k}: wiki=${v.wiki}, client=${v.client}`).join('; ')}`));
lines.push('','## Incomplete visible monsters','');
incomplete.forEach(x=>lines.push(`- **#${x.id} ${x.name} (${x.internalName})** [${x.category}] — ${x.missing.join(', ')}${x.instanceLabel?` · instance: ${x.instanceLabel}`:''}`));
fs.writeFileSync(path.join(root,'audit/monster-data-audit.md'),lines.join('\n')+'\n');
console.log(JSON.stringify(summary,null,2));
