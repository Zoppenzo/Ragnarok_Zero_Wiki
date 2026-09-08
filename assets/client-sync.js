/* Ragnarok Zero Global official-client synchronizer.
 * Applies client-side skill facts without exposing internal/source annotations in the UI.
 */
(function () {
  'use strict';

  const JOB_BY_CLASS = {
    novice:0,swordman:1,mage:2,archer:3,acolyte:4,merchant:5,thief:6,
    knight:7,priest:8,wizard:9,blacksmith:10,hunter:11,assassin:12,
    crusader:14,monk:15,sage:16,rogue:17,alchemist:18,bard:19,dancer:20
  };

  const SLUG_AEGIS = {
    'basic-skill':'NV_BASIC','first-aid':'NV_FIRSTAID','play-dead':'NV_TRICKDEAD',
    'sword-mastery':'SM_SWORD','increase-hp-recovery':'SM_RECOVERY','bash':'SM_BASH','provoke':'SM_PROVOKE',
    'berserk-swordman':'SM_AUTOBERSERK','hp-recovery-while-moving':'SM_MOVINGRECOVERY','two-handed-sword-mastery':'SM_TWOHAND',
    'magnum-break':'SM_MAGNUM','endure':'SM_ENDURE','fatal-blow':'SM_FATALBLOW','spear-mastery':'KN_SPEARMASTERY',
    'stone-curse':'MG_STONECURSE','cold-bolt':'MG_COLDBOLT','lightning-bolt':'MG_LIGHTNINGBOLT','napalm-beat':'MG_NAPALMBEAT',
    'fire-bolt':'MG_FIREBOLT','sight':'MG_SIGHT','earth-spike':'WZ_EARTHSPIKE','frost-diver':'MG_FROSTDIVER','frost-driver':'MG_FROSTDIVER',
    'thunder-storm':'MG_THUNDERSTORM','soul-strike':'MG_SOULSTRIKE','fire-ball':'MG_FIREBALL','energy-coat':'MG_ENERGYCOAT',
    'increase-sp-recovery':'MG_SRECOVERY','safety-wall':'MG_SAFETYWALL','fire-wall':'MG_FIREWALL',
    'double-strafe':'AC_DOUBLE','owls-eye':'AC_OWL','vultures-eye':'AC_VULTURE','improve-concentration':'AC_CONCENTRATION',
    'arrow-shower':'AC_SHOWER','arrow-crafting':'AC_MAKINGARROW','arrow-repel':'AC_CHARGEARROW',
    'enlarge-weight-limit':'MC_INCCARRY','axe-mastery':'AM_AXEMASTERY','discount':'MC_DISCOUNT','overcharge':'MC_OVERCHARGE',
    'pushcart':'MC_PUSHCART','item-appraisal':'MC_IDENTIFY','vending':'MC_VENDING','mammonite':'MC_MAMMONITE',
    'cart-revolution':'MC_CARTREVOLUTION','change-cart':'MC_CHANGECART','crazy-uproar':'MC_LOUD','cart-boost':'WS_CARTBOOST',
    'double-attack':'TF_DOUBLE','improve-dodge':'TF_MISS','steal':'TF_STEAL','hiding':'TF_HIDING','envenom':'TF_POISON',
    'detoxify':'TF_DETOXIFY','sand-attack':'TF_SPRINKLESAND','back-slide':'TF_BACKSLIDING','find-stone':'TF_PICKSTONE','stone-fling':'TF_THROWSTONE',
    'divine-protection':'AL_DP','demon-bane':'AL_DEMONBANE','ruwach':'AL_RUWACH','pneuma':'AL_PNEUMA','teleport':'AL_TELEPORT',
    'warp-portal':'AL_WARP','heal':'AL_HEAL','increase-agility':'AL_INCAGI','decrease-agility':'AL_DECAGI','aqua-benedicta':'AL_HOLYWATER',
    'signum-crucis':'AL_CRUCIS','angelus':'AL_ANGELUS','blessing':'AL_BLESSING','cure':'AL_CURE','holy-light':'AL_HOLYLIGHT','mace-mastery':'PR_MACEMASTERY'
  };

  /*
   * Notes follow the iRO Wiki idea: only non-obvious gameplay mechanics belong
   * here. They are paraphrased and only kept when they also apply to Zero.
   * Skills without a useful special note intentionally have no Notes section.
   */
  const SKILL_NOTES = {
    'magnum-break': [
      {
        en:'The 10-second buff does not change the weapon itself to Fire property. It adds a separate 20% Fire-property damage component on top of attacks, while the normal part of the attack keeps its own element.',
        fr:'Le buff de 10 secondes ne transforme pas l’arme en propriété Feu. Il ajoute une composante séparée de 20 % de dégâts de propriété Feu aux attaques, tandis que la partie normale de l’attaque conserve son propre élément.'
      },
      {
        en:'The additional Fire-property damage is a separate component that pierces DEF. It is also applied to Magnum Break’s own hit.',
        fr:'Les dégâts supplémentaires de propriété Feu forment une composante séparée qui ignore la DEF. Cette composante s’applique également au coup de Magnum Break lui-même.'
      },
      {
        en:'When an attack skill is pseudo-elemental, Magnum Break’s added 20% Fire component follows that pseudo-elemental behavior as well.',
        fr:'Lorsqu’un skill d’attaque est pseudo-élémental, la composante Feu supplémentaire de 20 % de Magnum Break suit elle aussi ce comportement pseudo-élémental.'
      }
    ]
  };

  const norm = s => String(s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9]+/g,'');
  const arrAt = (a,i) => Array.isArray(a) && a.length ? a[Math.min(i,a.length-1)] : null;

  function time(ms) {
    if (ms == null) return null;
    const n=Number(ms);
    if (!Number.isFinite(n)) return null;
    if (n===0) return 'None';
    if (n%1000===0) return (n/1000)+' s';
    return (n/1000).toFixed(3).replace(/0+$/,'').replace(/\.$/,'')+' s';
  }

  function castAt(r,i) {
    if (!r.d) return 'None';
    const f=arrAt(r.d.cf,i), v=arrAt(r.d.cv,i);
    if (f==null && v==null) return 'None';
    const fn=Number(f||0), vn=Number(v||0), total=fn+vn;
    if (!total) return 'None';
    if (fn && vn) return `${time(total)} (${time(fn).replace(' s','')} fixed + ${time(vn).replace(' s','')} variable)`;
    if (fn) return `${time(fn)} fixed`;
    return `${time(vn)} variable`;
  }

  function delayAt(r,i,key) {
    if (!r.d) return null;
    if (!Array.isArray(r.d[key])) return 'None';
    return time(arrAt(r.d[key],i)) || 'None';
  }

  function summarize(max,getter,fallback) {
    const values=[];
    for (let i=0;i<Math.max(1,max||1);i++) {
      const value=getter(i);
      if (value!=null) values.push(String(value));
    }
    if (!values.length) return fallback;
    const unique=[...new Set(values)];
    return unique.length===1 ? unique[0] : 'Variable';
  }

  function install(client) {
    const rows=Object.values(client);
    const byAegis=new Map(rows.map(x=>[x.a,x]));
    const byName=new Map(rows.map(x=>[norm(x.n),x]));
    window.RZ_OFFICIAL_CLIENT_SKILLS=client;

    const clientForSkill=sk => {
      if (!sk) return null;
      const aegis=SLUG_AEGIS[sk.id];
      return (aegis && byAegis.get(aegis)) || byName.get(norm(sk.name)) || null;
    };
    window.RZ_CLIENT_SKILL_FOR=clientForSkill;

    function applyData() {
      const root=window.RO_DATA;
      if (!root || !Array.isArray(root.skills)) return false;

      const idToWiki=new Map();
      for (const sk of root.skills) {
        const r=clientForSkill(sk);
        if (r) idToWiki.set(Number(r.id),sk);
      }

      for (const sk of root.skills) {
        const r=clientForSkill(sk);
        if (!r) continue;
        const max=r.m || sk.maxLevel || 1;

        sk.clientId=r.id;
        sk.clientAegis=r.a;
        sk.maxLevel=max;
        if (r.sp) sk.spCost=summarize(max,i=>arrAt(r.sp,i),sk.spCost);
        if (r.r) sk.range=summarize(max,i=>arrAt(r.r,i),sk.range);
        sk.castTime=summarize(max,i=>castAt(r,i),sk.castTime);
        sk.castDelay=summarize(max,i=>delayAt(r,i,'gd'),sk.castDelay);
        sk.cooldown=summarize(max,i=>delayAt(r,i,'cd'),sk.cooldown);

        if (r.de) {
          sk.description=sk.description && typeof sk.description==='object' ? sk.description : {};
          sk.description.en=r.de;
          sk.description.fr=r.df || r.de;
        }

        const job=JOB_BY_CLASS[sk.classId];
        const prereqs=(r.po && job!=null && r.po[String(job)]) || r.p;
        if (Array.isArray(prereqs)) {
          const mapped=prereqs.map(([id,level])=>{
            const dep=idToWiki.get(Number(id));
            return dep ? {skillId:dep.id,level:Number(level),verified:true} : null;
          }).filter(Boolean);
          if (mapped.length===prereqs.length) sk.prerequisites=mapped;
        }

        /* Old generic notes are not displayed. Only curated mechanic notes survive. */
        sk.noteList=SKILL_NOTES[sk.id] || [];
        sk.verified=true;
      }
      return true;
    }

    function currentSkill() {
      const match=location.hash.match(/^#\/skills\/([^/?#]+)/);
      if (!match || !window.RO_DATA) return null;
      const id=decodeURIComponent(match[1]);
      return (window.RO_DATA.skills||[]).find(x=>x.id===id || (id==='frost-driver' && x.id==='frost-diver')) || null;
    }

    function patchInfobox(sk,r) {
      const table=document.querySelector('aside.infobox table');
      if (!table) return;
      const max=r.m || sk.maxLevel || 1;
      const vals={
        max:String(max),
        sp:summarize(max,i=>arrAt(r.sp,i),'—'),
        range:summarize(max,i=>arrAt(r.r,i),'—'),
        cast:summarize(max,i=>castAt(r,i),'—'),
        delay:summarize(max,i=>delayAt(r,i,'gd'),'—'),
        cd:summarize(max,i=>delayAt(r,i,'cd'),'—')
      };
      for (const tr of table.querySelectorAll('tr')) {
        const th=tr.querySelector('th'), td=tr.querySelector('td');
        if (!th || !td) continue;
        const label=norm(th.textContent);
        if (label.includes('maxlevel') || label.includes('niveaumax')) td.textContent=vals.max;
        else if (label.includes('spcost') || label.includes('coutsp')) td.textContent=vals.sp;
        else if (label==='range' || label==='portee') td.textContent=vals.range;
        else if (label.includes('casttime') || label.includes('tempsdecast')) td.textContent=vals.cast;
        else if (label.includes('castdelay') || label.includes('delaiapreslancement') || label.includes('delaiaprescast')) td.textContent=vals.delay;
        else if (label.includes('cooldown') || label.includes('recharge')) td.textContent=vals.cd;
      }
    }

    function patchRendered() {
      const sk=currentSkill();
      if (!sk) return;
      const r=clientForSkill(sk);
      if (r) patchInfobox(sk,r);
    }

    let frameA=0, frameB=0;
    function schedulePatch() {
      if (frameA) cancelAnimationFrame(frameA);
      if (frameB) cancelAnimationFrame(frameB);
      frameA=requestAnimationFrame(()=>{
        frameB=requestAnimationFrame(patchRendered);
      });
    }

    if (applyData()) {
      try { window.dispatchEvent(new HashChangeEvent('hashchange')); }
      catch (_) { window.dispatchEvent(new Event('hashchange')); }
      schedulePatch();
    }

    window.addEventListener('hashchange',schedulePatch);
  }

  fetch('assets/client-data/skills.json')
    .then(r=>{if(!r.ok) throw new Error('client skill data '+r.status); return r.json();})
    .then(install)
    .catch(err=>console.error('[RZ client sync]',err));
})();