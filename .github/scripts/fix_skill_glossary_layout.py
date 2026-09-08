from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
index_path = ROOT / "index.html"
text = index_path.read_text(encoding="utf-8")

# Keep Ragnarok/stat glossary terms in English even when the surrounding UI is French.
# This is intentionally conservative: normal explanatory prose can remain translated,
# while canonical game terms and abbreviations stay unchanged.
old_short = r'''  function skillShortDescription(sk) {
    let value = String(txt(sk && sk.description ? sk.description : '') || '').trim();
    value = value
      .replace(/\s*\[(?:Lv\.?|Level|Niv\.?)\s*1\][\s\S]*$/i, '')
      .replace(/\s*\[SP\s+\d+[\s\S]*$/i, '')
      .trim();

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
    # Idempotent fallback for small formatting differences.
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

index_path.write_text(text, encoding="utf-8")
print("Skill glossary terminology kept in English; level heading/table spacing fixed.")
