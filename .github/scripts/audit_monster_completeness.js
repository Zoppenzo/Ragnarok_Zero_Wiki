const fs=require('fs');
const path=require('path');
const vm=require('vm');

const root=path.resolve(__dirname,'../..');
const sandbox={console, setTimeout, clearTimeout};
sandbox.window=sandbox;
sandbox.globalThis=sandbox;
sandbox.RO_DATA={monsters:[],items:[]};
const ctx=vm.createContext(sandbox);
const files=[
  'assets/client-monsters-data.js',
  'assets/client-monster-identity.js',
  'assets/monster-zero-stats.js',
  'assets/monster-zero-consensus.js',
  'assets/rms-monster-behavior.js',
  'assets/client-monsters.js',
  'assets/monster-client-corrections.js',
  'assets/monster-audit-20260909.js',
  'assets/monster-instance-maps.js'
];
for(const rel of files){
  const p=path.join(root,rel);
  if(!fs.existsSync(p)) throw new Error('Missing '+rel);
  vm.runInContext(fs.readFileSync(p,'utf8'),ctx,{filename:rel});
}

const monsters=Array.isArray(sandbox.RO_DATA.monsters)?sandbox.RO_DATA.monsters:[];
const identity=sandbox.RZ_CLIENT_MONSTER_IDENTITY||{};
const races=['Formless','Undead','Brute','Plant','Insect','Fish','Demon','Demi-Human','Angel','Dragon'];
const sizes=['Small','Medium','Large'];
const elements=['Neutral','Water','Earth','Fire','Wind','Poison','Holy','Shadow','Ghost','Undead'];
const known=v=>v!==null&&v!==undefined&&v!==''&&!/^n\/?a$/i.test(String(v).trim())&&String(v).trim()!=='—';
const pairKnown=(a,b)=>known(a)||known(b);
const useful=m=>[
  m.hp,m.level,m.race,m.element,m.size,m.hit,m.flee,m.walkSpeed,m.def,m.mdef,m.baseExp,m.jobExp
].some(known)||pairKnown(m.attackMin,m.attackMax)||pairKnown(m.magicAttackMin,m.magicAttackMax)||
(Array.isArray(m.maps)&&m.maps.length)||(Array.isArray(m.drops)&&m.drops.length)||(Array.isArray(m.skills)&&m.skills.length)||(Array.isArray(m.modes)&&m.modes.length);

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

const visible=monsters.filter(useful);
const incomplete=visible.map(m=>({
  id:Number(m.clientId||m.id),internalName:m.internalName||'',name:m.name||'',missing:missing(m),
  memorial:/^MD_/i.test(String(m.internalName||'')),
  instanceLabel:m.instanceLabel||null,
  dwarf:/BOULDERDWARF|NORDIUM|PORING_GEM|APARGREL/i.test(String(m.internalName||''))
})).filter(x=>x.missing.length).sort((a,b)=>b.missing.length-a.missing.length||a.id-b.id);

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

const summary={generatedAt:new Date().toISOString(),totalRuntime:monsters.length,totalVisible:visible.length,totalIncomplete:incomplete.length,totalClientContradictions:contradictions.length};
const out={summary,incomplete,contradictions};
fs.mkdirSync(path.join(root,'audit'),{recursive:true});
fs.writeFileSync(path.join(root,'audit/monster-data-audit.json'),JSON.stringify(out,null,2));

const lines=[
  '# Monster data audit','',
  `Generated: ${summary.generatedAt}`,'',
  `- Runtime monster rows: **${summary.totalRuntime}**`,
  `- Rows with useful data (visible): **${summary.totalVisible}**`,
  `- Visible rows still incomplete: **${summary.totalIncomplete}**`,
  `- Direct contradictions with client identity table: **${summary.totalClientContradictions}**`,'',
  '## Client contradictions',''
];
if(!contradictions.length)lines.push('None.');
else contradictions.forEach(x=>lines.push(`- **#${x.id} ${x.name} (${x.internalName})** — ${Object.entries(x.diff).map(([k,v])=>`${k}: wiki=${v.wiki}, client=${v.client}`).join('; ')}`));
lines.push('','## Incomplete visible monsters','');
incomplete.forEach(x=>lines.push(`- **#${x.id} ${x.name} (${x.internalName})** — ${x.missing.join(', ')}${x.instanceLabel?` · instance: ${x.instanceLabel}`:''}`));
fs.writeFileSync(path.join(root,'audit/monster-data-audit.md'),lines.join('\n')+'\n');
console.log(JSON.stringify(summary,null,2));
