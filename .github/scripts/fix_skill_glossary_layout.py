from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
index_path = ROOT / "index.html"
text = index_path.read_text(encoding="utf-8")

# Keep Ragnarok/stat glossary terms in English even when the surrounding UI is French.
# Normal explanatory prose remains translated, while canonical game terms do not.
old_short = r'''  function skillShortDescription(sk) {
    let value = String(txt(sk && sk.description ? sk.description : '') || '').trim();
    value = value
      .replace(/\s*\[(?:Lv\.?|Level|Niv\.?)\s*1\][\s\S]*$/i, '')
      .replace(/\s*\[SP\s+\d+[\s\S]*$/i, '')
      .trim();

    // Canonical Ragnarok glossary terms are never localized.
    value = value
      .replace(/\bM\.?ATQ\b/gi, 'MATK')
      .replace(/\bATQ\b/gi, 'ATK')
      .replace(/\bMax\s*PV\b/gi, 'Max HP')
      .replace(/\bMax\s*PM\b/gi, 'Max SP')
      .replace(/\bPV\b/g, 'HP')
      .replace(/\bPM\b/g, 'SP')
      .replace(/\bprécision\b/gi, 'Accuracy');

    // Keep the class overview iRO-like: usually one or two short sentences.
    const parts = value.match(/[^.!?]+[.!?]+|[^.!?]+$/g) || [];
    if (parts.length > 2) value = parts.slice(0, 2).join(' ').trim();
    if (value.length > 330) {
      const cut = value.slice(0, 330);
      value = cut.slice(0, Math.max(cut.lastIndexOf(' '), 250)).trim() + '…';
    }
    return value;
  }'''

new_short = r'''  function skillShortDescription(sk) {
    let value = String(txt(sk && sk.description ? sk.description : '') || '').trim();
    value = value
      .replace(/\s*\[(?:Lv\.?|Level|Niv\.?)\s*1\][\s\S]*$/i, '')
      .replace(/\s*\[SP\s+\d+[\s\S]*$/i, '')
      .trim();

    // Canonical Ragnarok glossary terms are never localized.
    value = value
      .replace(/\bM\.?ATQ\b/gi, 'MATK')
      .replace(/\bATQ\b/gi, 'ATK')
      .replace(/\bDÉF\.?M\b/gi, 'MDEF')
      .replace(/\bDÉF\.?P\b/gi, 'DEF')
      .replace(/\bMax\s*PV\b/gi, 'Max HP')
      .replace(/\bMax\s*PM\b/gi, 'Max SP')
      .replace(/\bMPV\b/g, 'MHP')
      .replace(/\bMSP\b/g, 'MSP')
      .replace(/\bPV\b/g, 'HP')
      .replace(/\bPM\b/g, 'SP')
      .replace(/\bprécision\b/gi, 'Accuracy')
      .replace(/\besquive parfaite\b/gi, 'Perfect Dodge')
      .replace(/\bvitesse d[’']attaque\b/gi, 'ASPD');

    // Keep the class overview iRO-like: usually one or two short sentences.
    const parts = value.match(/[^.!?]+[.!?]+|[^.!?]+$/g) || [];
    if (parts.length > 2) value = parts.slice(0, 2).join(' ').trim();
    if (value.length > 330) {
      const cut = value.slice(0, 330);
      value = cut.slice(0, Math.max(cut.lastIndexOf(' '), 250)).trim() + '…';
    }
    return value;
  }'''

if old_short in text:
    text = text.replace(old_short, new_short, 1)
else:
    text = re.sub(
        r"  function skillShortDescription\(sk\) \{.*?\n  \}",
        lambda _m: new_short,
        text,
        count=1,
        flags=re.S,
    )

# The Effect column always uses the English client terminology. The French client
# text is intentionally not used here because it localizes canonical terms such
# as ATK -> ATQ and Accuracy -> précision.
old_effect_block = r'''    const enEffects = Array.isArray(r.le) ? r.le : [];
    const frEffects = [];
    const frText = String(r.df || '');
    const frRe = /\[Niv\.\s*(\d+)\]\s*([\s\S]*?)(?=\[Niv\.\s*\d+\]|$)/gi;
    let match;
    while ((match = frRe.exec(frText))) {
      frEffects[Number(match[1]) - 1] = String(match[2] || '').trim();
    }

    const rows = [];
    for (let i = 0; i < max; i++) {
      let en = String(enEffects[i] || '').trim();
      let fr = String(frEffects[i] || '').trim();

      // Heal is the only current first-job multi-level skill whose client text
      // exposes level scaling without listing a separate per-level Effect line.
      if (r.a === 'AL_HEAL' && !en) {
        en = `Heal strength: skill-level factor ×${i + 1}; final amount also scales with Base Level, total INT and weapon MATK.`;
        fr = `Puissance de Heal : facteur de niveau ×${i + 1} ; le montant final dépend aussi du Base Level, de l’INT totale et de la MATK de l’arme.`;
      }

      if (!en && fr) en = fr;
      if (!fr && en) fr = en;
      const effect = en || fr ? navLabel(en || fr, fr || en) : '—';'''

new_effect_block = r'''    const enEffects = Array.isArray(r.le) ? r.le : [];

    const rows = [];
    for (let i = 0; i < max; i++) {
      let effect = String(enEffects[i] || '').trim();

      // Heal exposes its scaling through the formula rather than separate
      // client Effect rows, so provide the level factor explicitly.
      if (r.a === 'AL_HEAL' && !effect) {
        effect = `Heal strength: Skill Level factor ×${i + 1}; final amount also scales with Base Level, total INT and weapon MATK.`;
      }

      if (!effect) effect = '—';'''

if old_effect_block in text:
    text = text.replace(old_effect_block, new_effect_block, 1)
else:
    text = re.sub(
        r"    const enEffects = Array\.isArray\(r\.le\) \? r\.le : \[\];.*?      const effect = en \|\| fr \? navLabel\(en \|\| fr, fr \|\| en\) : '—';",
        lambda _m: new_effect_block,
        text,
        count=1,
        flags=re.S,
    )

# Put the heading and its table together below the floating infobox. Without
# clear:both the h2 can sit beside the infobox while the wide table is pushed
# below it, creating a large empty gap between them.
text = text.replace(
    '<h2 id="level-effects">${navLabel(\'Effects by level\',\'Effets par niveau\')}</h2>',
    '<h2 id="level-effects" style="clear:both;margin-bottom:10px">${navLabel(\'Effects by level\',\'Effets par niveau\')}</h2>',
)

# Defensive normalization in case an older generated index still contains the
# localized heading/table implementation.
text = text.replace("const effect = en || fr ? navLabel(en || fr, fr || en) : '—';", "const effect = en || '—';")

# Global glossary/entity lock. This runs once after each page render and after a
# language switch. It does NOT use a MutationObserver, so it does not recreate
# the performance loop that previously affected skill pages.
global_lock = r'''  <script id="rz-global-glossary-lock">
  (() => {
    'use strict';

    const fixedRules = [
      [/\bM\.?ATQ\b/gi, 'MATK'],
      [/\bATQ\b/gi, 'ATK'],
      [/\bDÉF\.?M\b/gi, 'MDEF'],
      [/\bDÉF\.?P\b/gi, 'DEF'],
      [/\bMax\s*PV\b/gi, 'Max HP'],
      [/\bMax\s*PM\b/gi, 'Max SP'],
      [/\bMPV\b/g, 'MHP'],
      [/\bPV\b/g, 'HP'],
      [/\bPM\b/g, 'SP'],
      [/\bprécision\b/gi, 'Accuracy'],
      [/\besquive parfaite\b/gi, 'Perfect Dodge'],
      [/\bvitesse d[’']attaque\b/gi, 'ASPD'],
      [/\bdéfense magique\b/gi, 'MDEF'],
      [/\bdéfense physique\b/gi, 'DEF'],
      [/\bÉtourdissement\b/g, 'Stun'],
      [/\bPétrification\b/g, 'Stone'],
      [/\bCongélation\b/g, 'Freeze'],
      [/\bEmpoisonnement\b/g, 'Poison'],
      [/\bAveuglement\b/g, 'Blind'],
      [/\bSaignement\b/g, 'Bleeding'],
      [/\bMalédiction\b/g, 'Curse'],
      [/\bSommeil\b/g, 'Sleep'],
      [/\bPropriété Feu\b/g, 'Fire property'],
      [/\bPropriété Eau\b/g, 'Water property'],
      [/\bPropriété Vent\b/g, 'Wind property'],
      [/\bPropriété Terre\b/g, 'Earth property'],
      [/\bPropriété Sacrée\b/g, 'Holy property'],
      [/\bPropriété Ombre\b/g, 'Shadow property'],
      [/\bPropriété Neutre\b/g, 'Neutral property'],
      [/\bMort-vivant\b/g, 'Undead']
    ];

    const escRe = value => String(value).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const slugify = value => String(value || '')
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .toLowerCase().replace(/['’]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

    function canonicalCollections() {
      const root = window.RO_DATA || {};
      const skillMap = new Map();
      const itemMap = new Map();
      const exactNames = [];

      const addAliases = (map, row, english) => {
        if (!row || !english) return;
        for (const key of [row.id, row.slug, slugify(english), english]) {
          if (key != null && String(key)) map.set(String(key).toLowerCase(), english);
        }
      };

      for (const row of Array.isArray(root.skills) ? root.skills : []) {
        const english = typeof row.name === 'string' ? row.name : row.name?.en;
        const french = typeof row.name === 'object' ? row.name?.fr : (row.nameFr || row.frName);
        addAliases(skillMap, row, english);
        if (french && english && french !== english) exactNames.push([french, english]);
      }

      for (const row of Array.isArray(root.items) ? root.items : []) {
        const english = typeof row.name === 'string' ? row.name : row.name?.en;
        const french = typeof row.name === 'object' ? row.name?.fr : (row.nameFr || row.frName);
        addAliases(itemMap, row, english);
        if (french && english && french !== english) exactNames.push([french, english]);
      }

      // Client skill names are bilingual. Use this to undo localized skill names
      // inside otherwise-French descriptions (e.g. Coup fatal -> Fatal Blow).
      const client = window.RZ_OFFICIAL_CLIENT_SKILLS || {};
      for (const row of Object.values(client)) {
        if (!row || !row.n) continue;
        addAliases(skillMap, {id:row.id, slug:slugify(row.n)}, row.n);
        if (row.fr && row.fr !== row.n) exactNames.push([row.fr, row.n]);
      }

      return {skillMap, itemMap, exactNames};
    }

    function normalizeText(value, exactNames) {
      let out = String(value || '');
      for (const [from, to] of fixedRules) out = out.replace(from, to);
      for (const [from, to] of exactNames) {
        if (from && to && from !== to && out.includes(from)) {
          out = out.replace(new RegExp(escRe(from), 'g'), to);
        }
      }
      return out;
    }

    function humanizeSlug(value) {
      return decodeURIComponent(String(value || ''))
        .replace(/[-_]+/g, ' ')
        .replace(/\b\w/g, c => c.toUpperCase());
    }

    function canonicalFromHref(href, map, marker) {
      const pos = href.indexOf(marker);
      if (pos < 0) return null;
      const raw = href.slice(pos + marker.length).split(/[?#/]/)[0];
      const decoded = decodeURIComponent(raw || '');
      return map.get(decoded.toLowerCase()) || map.get(slugify(decoded)) || (decoded ? humanizeSlug(decoded) : null);
    }

    function setAnchorName(anchor, english) {
      if (!anchor || !english) return;
      if (!anchor.children.length) {
        anchor.textContent = english;
        return;
      }
      const directText = [...anchor.childNodes].find(n => n.nodeType === Node.TEXT_NODE && n.nodeValue.trim());
      if (directText) {
        directText.nodeValue = english;
        return;
      }
      const leaf = [...anchor.querySelectorAll('span,strong,em')].find(el => !el.children.length && el.textContent.trim());
      if (leaf) leaf.textContent = english;
    }

    function lockEntityLinks(scope, skillMap, itemMap) {
      for (const a of scope.querySelectorAll('a[href]')) {
        const href = a.getAttribute('href') || '';
        let english = null;
        if (href.includes('#/skills/')) english = canonicalFromHref(href, skillMap, '#/skills/');
        else if (href.includes('#/items/')) english = canonicalFromHref(href, itemMap, '#/items/');
        else if (href.includes('#/item/')) english = canonicalFromHref(href, itemMap, '#/item/');
        if (english) setAnchorName(a, english);
      }
    }

    function applyGlobalGlossaryLock() {
      const scope = document.querySelector('.wiki-shell') || document.body;
      if (!scope) return;
      const {skillMap, itemMap, exactNames} = canonicalCollections();

      const walker = document.createTreeWalker(scope, NodeFilter.SHOW_TEXT, {
        acceptNode(node) {
          const parent = node.parentElement;
          if (!parent || parent.closest('script,style,textarea,input,select,option')) return NodeFilter.FILTER_REJECT;
          return node.nodeValue.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
        }
      });

      const nodes = [];
      while (walker.nextNode()) nodes.push(walker.currentNode);
      for (const node of nodes) {
        const next = normalizeText(node.nodeValue, exactNames);
        if (next !== node.nodeValue) node.nodeValue = next;
      }

      lockEntityLinks(scope, skillMap, itemMap);
    }

    let raf1 = 0, raf2 = 0;
    function schedule() {
      if (raf1) cancelAnimationFrame(raf1);
      if (raf2) cancelAnimationFrame(raf2);
      raf1 = requestAnimationFrame(() => {
        raf2 = requestAnimationFrame(applyGlobalGlossaryLock);
      });
    }

    window.addEventListener('hashchange', schedule);
    document.addEventListener('click', event => {
      if (event.target.closest('.lang-toggle')) setTimeout(schedule, 0);
    });
    window.addEventListener('rz-client-skills-ready', schedule);
    schedule();
  })();
  </script>
'''

# Replace the global lock atomically if it already exists, otherwise append it
# after client-sync and before </body>.
text = re.sub(
    r'\n?\s*<script id="rz-global-glossary-lock">.*?</script>\s*',
    '\n',
    text,
    count=1,
    flags=re.S,
)
text = text.replace('</body>', global_lock + '</body>', 1)

index_path.write_text(text, encoding="utf-8")
print("Global English glossary, skill names and item names enforced across wiki pages; skill table spacing fixed.")
