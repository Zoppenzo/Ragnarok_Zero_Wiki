const fs=require('fs');
const path=require('path');
const vm=require('vm');

const root=path.resolve(__dirname,'../..');
const auditPath=path.join(root,'audit/monster-data-audit.json');
const mdPath=path.join(root,'audit/monster-data-audit.md');
const overridesPath=path.join(root,'assets/monster-roster-classification.js');
if(!fs.existsSync(auditPath)) throw new Error('Run audit_monster_completeness.js first');
if(!fs.existsSync(overridesPath)) throw new Error('Missing monster roster classification overrides');

const sandbox={window:{}};
vm.createContext(sandbox);
vm.runInContext(fs.readFileSync(overridesPath,'utf8'),sandbox,{filename:'monster-roster-classification.js'});
const overrides=sandbox.window.RZ_MONSTER_ROSTER_CLASSIFICATION_OVERRIDES||{};
const audit=JSON.parse(fs.readFileSync(auditPath,'utf8'));
const requiredFields=['HP','ATK','MATK','DEF','MDEF','HIT','FLEE','Base EXP','Job EXP','Walk Speed','Maps','Drops','Skills'];

const overrideFor=row=>{
  const id=String(row?.id??'');
  const o=overrides[id];
  if(!o) return null;
  if(o.internalName&&String(row?.internalName||'')!==String(o.internalName)){
    throw new Error(`Classification override identity mismatch for #${id}: expected ${o.internalName}, got ${row?.internalName}`);
  }
  return o;
};

for(const row of audit.rosterClassification||[]){
  const o=overrideFor(row);
  if(o){ row.category=o.category; row.classificationReason=o.reason||null; row.classificationOverride=true; }
}
for(const row of audit.incomplete||[]){
  const o=overrideFor(row);
  if(o){ row.category=o.category; row.classificationReason=o.reason||null; row.classificationOverride=true; }
}

const countBy=(rows,key)=>rows.reduce((acc,row)=>{ const v=row[key]||'unknown'; acc[v]=(acc[v]||0)+1; return acc; },{});
const classificationCounts=countBy(audit.rosterClassification||[],'category');
const incompleteByCategory=countBy(audit.incomplete||[],'category');
const normalIncomplete=(audit.incomplete||[]).filter(x=>x.category==='normal');
const normalCount=classificationCounts.normal||0;
const normalMissingFieldCounts=Object.fromEntries(requiredFields.map(k=>[k,0]));
for(const row of normalIncomplete){
  for(const field of row.missing||[]) normalMissingFieldCounts[field]=(normalMissingFieldCounts[field]||0)+1;
}
const normalMissingDistribution={};
for(const row of normalIncomplete){ const n=(row.missing||[]).length; normalMissingDistribution[n]=(normalMissingDistribution[n]||0)+1; }
const normalFullyBlank=normalIncomplete.filter(x=>(x.missing||[]).length===requiredFields.length);
const normalNearlyComplete=normalIncomplete.filter(x=>(x.missing||[]).length<=2);
const normalOnlyExpMissing=normalIncomplete.filter(x=>(x.missing||[]).length>0&&(x.missing||[]).every(f=>f==='Base EXP'||f==='Job EXP'));

Object.assign(audit.summary,{
  rosterClassification:classificationCounts,
  incompleteByCategory,
  totalNormalIncomplete:normalIncomplete.length,
  totalNormalComplete:normalCount-normalIncomplete.length,
  totalNormalFullyBlank:normalFullyBlank.length,
  totalNormalNearlyComplete:normalNearlyComplete.length,
  totalNormalOnlyExpMissing:normalOnlyExpMissing.length,
  normalMissingFieldCounts,
  normalMissingDistribution,
  classificationOverridesApplied:Object.keys(overrides).length
});
audit.normalFullyBlank=normalFullyBlank;
audit.normalNearlyComplete=normalNearlyComplete;
audit.normalOnlyExpMissing=normalOnlyExpMissing;
audit.classificationOverrides=overrides;
fs.writeFileSync(auditPath,JSON.stringify(audit,null,2));

if(fs.existsSync(mdPath)){
  let md=fs.readFileSync(mdPath,'utf8');
  md=md.replace(/- Normal\/world candidates complete: \*\*\d+\/\d+\*\*/,`- Normal/world candidates complete: **${audit.summary.totalNormalComplete}/${normalCount}**`);
  md=md.replace(/- Normal\/world candidates still incomplete: \*\*\d+\*\*/,`- Normal/world candidates still incomplete: **${audit.summary.totalNormalIncomplete}**`);
  md=md.replace(/- Normal\/world candidates with all \d+ tracked fields missing: \*\*\d+\*\*/,`- Normal/world candidates with all ${requiredFields.length} tracked fields missing: **${audit.summary.totalNormalFullyBlank}**`);
  md=md.replace(/- Normal\/world candidates missing only 1-2 fields: \*\*\d+\*\*/,`- Normal/world candidates missing only 1-2 fields: **${audit.summary.totalNormalNearlyComplete}**`);
  md=md.replace(/- Normal\/world candidates missing only Base\/Job EXP: \*\*\d+\*\*/,`- Normal/world candidates missing only Base/Job EXP: **${audit.summary.totalNormalOnlyExpMissing}**`);
  for(const field of requiredFields){
    const escaped=field.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
    md=md.replace(new RegExp(`- ${escaped}: \\*\\*\\d+\\*\\* missing overall · \\*\\*\\d+\\*\\* missing among normal/world candidates`),m=>m.replace(/\*\*\d+\*\* missing among normal\/world candidates$/,`**${normalMissingFieldCounts[field]||0}** missing among normal/world candidates`));
  }
  for(const [category,count] of Object.entries(classificationCounts)){
    const incomplete=incompleteByCategory[category]||0;
    const re=new RegExp(`- ${category}: \\*\\*\\d+\\*\\*(?: · incomplete: \\*\\*\\d+\\*\\*)?`);
    const replacement=`- ${category}: **${count}**${incomplete?` · incomplete: **${incomplete}**`:''}`;
    if(re.test(md)) md=md.replace(re,replacement);
  }
  for(const [id,o] of Object.entries(overrides)){
    const re=new RegExp(`(- \\*\\*#${id} [^\\n]+?\\*\\*) \\[normal\\]`);
    md=md.replace(re,`$1 [${o.category}]`);
  }
  md += `\n## Classification overrides\n\n` + Object.entries(overrides).map(([id,o])=>`- **#${id} ${o.internalName}** → ${o.category} — ${o.reason}`).join('\n') + '\n';
  fs.writeFileSync(mdPath,md);
}

const normalMissingMaps=normalIncomplete.filter(x=>(x.missing||[]).includes('Maps'));
console.log(JSON.stringify({
  overridesApplied:Object.keys(overrides).length,
  normalCount,
  normalIncomplete:normalIncomplete.length,
  normalComplete:audit.summary.totalNormalComplete,
  normalMissingMaps:normalMissingMaps.map(x=>({id:x.id,internalName:x.internalName,name:x.name,missing:x.missing}))
},null,2));
