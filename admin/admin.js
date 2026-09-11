import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const cfg = window.RZ_SUPABASE_CONFIG || {};
const ready = cfg.url && cfg.anonKey && !cfg.url.includes('YOUR_') && !cfg.anonKey.includes('YOUR_');
const supabase = ready ? createClient(cfg.url, cfg.anonKey) : null;
const $ = (id) => document.getElementById(id);
let tab = 'pages';
let rows = [];
let editing = null;

const defs = {
  pages:{table:'wiki_pages',title:'Pages',id:'id',columns:['title_en','slug','section','verification_status','published'],fields:[['slug','Slug','text'],['title_en','Titre EN','text'],['title_fr','Titre FR','text'],['section','Section','text'],['verification_status','Vérification','text'],['published','Publié','checkbox'],['content_en','Contenu EN','textarea'],['content_fr','Contenu FR','textarea']]},
  items:{table:'items',title:'Items',id:'id',columns:['id','name_en','item_type','attack','slots','verification_status'],fields:[['id','ID','number'],['name_en','Nom EN','text'],['name_fr','Nom FR','text'],['item_type','Type','text'],['attack','ATK','number'],['defense','DEF','number'],['slots','Slots','number'],['required_level','Niveau requis','number'],['verification_status','Vérification','text'],['published','Publié','checkbox'],['description_en','Description EN','textarea'],['description_fr','Description FR','textarea']]},
  monsters:{table:'monsters',title:'Monsters',id:'id',columns:['id','name_en','level','hp','race','element'],fields:[['id','ID','number'],['name_en','Nom EN','text'],['name_fr','Nom FR','text'],['level','Level','number'],['hp','HP','number'],['race','Race','text'],['element','Élément','text'],['size','Taille','text'],['verification_status','Vérification','text'],['published','Publié','checkbox'],['description_en','Description EN','textarea'],['description_fr','Description FR','textarea']]},
  skills:{table:'skills',title:'Skills',id:'id',columns:['id','technical_name','name_en','max_level','verification_status'],fields:[['id','ID','number'],['technical_name','Nom technique','text'],['name_en','Nom EN','text'],['name_fr','Nom FR','text'],['max_level','Niveau max','number'],['verification_status','Vérification','text'],['published','Publié','checkbox'],['description_en','Description EN','textarea'],['description_fr','Description FR','textarea']]}
};

function msg(el,text,kind=''){ el.textContent=text; el.className='status '+kind; el.classList.remove('hidden'); }
function hide(el){ el.classList.add('hidden'); }
function esc(v=''){ return String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }

if(!ready){
  msg($('configWarning'),'Supabase doit encore être relié : ajoute le Project URL et la clé anon/publishable dans assets/supabase-config.js.','error');
  $('loginBtn').disabled=true;
}

async function profileFor(user){
  const {data,error}=await supabase.from('profiles').select('role,email').eq('id',user.id).single();
  return error ? null : data;
}

async function showAdmin(user){
  const profile=await profileFor(user);
  if(!profile || !['admin','editor'].includes(profile.role)){
    await supabase.auth.signOut();
    msg($('loginStatus'),'Ce compte n’a pas accès à l’administration.','error');
    return;
  }
  $('loginView').classList.add('hidden');
  $('adminView').classList.remove('hidden');
  $('whoami').textContent=(profile.email||user.email)+' · '+profile.role;
  loadRows();
}

async function boot(){
  if(!supabase) return;
  const {data:{session}}=await supabase.auth.getSession();
  if(session) showAdmin(session.user);
}

$('loginBtn').addEventListener('click',async()=>{
  const {data,error}=await supabase.auth.signInWithPassword({email:$('email').value.trim(),password:$('password').value});
  if(error) return msg($('loginStatus'),error.message,'error');
  showAdmin(data.user);
});
$('logoutBtn').addEventListener('click',async()=>{await supabase.auth.signOut();$('adminView').classList.add('hidden');$('loginView').classList.remove('hidden');});

document.querySelectorAll('[data-tab]').forEach(b=>b.addEventListener('click',()=>{tab=b.dataset.tab;editing=null;$('editorCard').classList.add('hidden');loadRows();}));
$('refreshBtn').addEventListener('click',loadRows);
$('searchBox').addEventListener('input',render);
$('newBtn').addEventListener('click',()=>openEditor({}));
$('cancelBtn').addEventListener('click',()=>$('editorCard').classList.add('hidden'));
$('saveBtn').addEventListener('click',save);
$('deleteBtn').style.display='none';

async function loadRows(){
  const d=defs[tab]; $('sectionTitle').textContent=d.title;
  const {data,error}=await supabase.from(d.table).select('*').limit(500);
  if(error) return msg($('listStatus'),error.message,'error');
  hide($('listStatus')); rows=data||[]; render();
}

function render(){
  const d=defs[tab], q=$('searchBox').value.toLowerCase();
  $('tableHead').innerHTML='<tr>'+d.columns.map(c=>'<th>'+esc(c)+'</th>').join('')+'<th></th></tr>';
  const filtered=rows.filter(r=>!q||JSON.stringify(r).toLowerCase().includes(q));
  $('tableBody').innerHTML=filtered.map((r,i)=>'<tr>'+d.columns.map(c=>'<td>'+esc(r[c]??'')+'</td>').join('')+'<td><button data-edit="'+i+'">Modifier</button></td></tr>').join('');
  $('tableBody').querySelectorAll('[data-edit]').forEach(b=>b.addEventListener('click',()=>openEditor(filtered[Number(b.dataset.edit)])));
}

function openEditor(row){
  const d=defs[tab]; editing=Object.keys(row).length?row:null;
  $('editorTitle').textContent=(editing?'Modifier · ':'Ajouter · ')+d.title;
  $('entityForm').innerHTML=d.fields.map(([name,label,type])=>{
    const v=editing?.[name];
    if(type==='textarea') return '<label>'+esc(label)+'</label><textarea name="'+esc(name)+'">'+esc(v??'')+'</textarea>';
    if(type==='checkbox') return '<label><input style="width:auto" type="checkbox" name="'+esc(name)+'" '+((v??true)?'checked':'')+'> '+esc(label)+'</label>';
    return '<label>'+esc(label)+'</label><input type="'+type+'" name="'+esc(name)+'" value="'+esc(v??'')+'" '+(editing&&name===d.id?'readonly':'')+'>';
  }).join('');
  hide($('editStatus')); $('editorCard').classList.remove('hidden');
}

function payload(){
  const out={};
  for(const [name,,type] of defs[tab].fields){
    const el=$('entityForm').elements[name];
    if(type==='checkbox') out[name]=el.checked;
    else if(type==='number') out[name]=el.value===''?null:Number(el.value);
    else out[name]=el.value;
  }
  return out;
}

async function save(){
  const d=defs[tab], p=payload();
  const {data:{user}}=await supabase.auth.getUser();
  p.updated_by=user?.id||null;
  let result;
  if(editing) result=await supabase.from(d.table).update(p).eq(d.id,editing[d.id]).select().single();
  else { if(d.table==='wiki_pages') p.created_by=user?.id||null; result=await supabase.from(d.table).insert(p).select().single(); }
  if(result.error) return msg($('editStatus'),result.error.message,'error');
  editing=result.data; msg($('editStatus'),'Enregistré.','ok'); loadRows();
}

boot();
