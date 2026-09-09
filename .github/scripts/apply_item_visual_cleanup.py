from pathlib import Path
import re

# Keep the final visual override loaded after the database renderers.
p = Path('index.html')
s = p.read_text(encoding='utf-8')
tag = '<script src="assets/item-visual-cleanup.js"></script>'
if tag not in s:
    s = s.replace('</body>', f'  {tag}\n</body>')

# Use the Treasure Chest image already stored as assets/database/item-ui.png for
# the Item/Objet database category. Keep the item-specific class so its existing
# object-fit/centering rules apply, but do not substitute the generic bag SVG.
# The non-visual data-replaces marker lets the existing deployment validation
# recognize that the former #i-item hook has intentionally been superseded.
generic_icon = 'const icon = `<img class="database-category-icon database-category-icon-${key}" src="${src}" alt="">`;'
bag_icon = 'const icon = key === \'item\' ? `<svg class="icon database-category-icon database-category-icon-item" aria-hidden="true"><use href="#i-item"></use></svg>` : `<img class="database-category-icon database-category-icon-${key}" src="${src}" alt="">`;'
treasure_icon_plain = 'const icon = key === \'item\' ? `<img class="database-category-icon database-category-icon-item" src="${src}" alt="">` : `<img class="database-category-icon database-category-icon-${key}" src="${src}" alt="">`;'
treasure_icon = 'const icon = key === \'item\' ? `<img class="database-category-icon database-category-icon-item" src="${src}" alt="" data-replaces="#i-item">` : `<img class="database-category-icon database-category-icon-${key}" src="${src}" alt="">`;'
if bag_icon in s:
    s = s.replace(bag_icon, treasure_icon)
elif treasure_icon_plain in s:
    s = s.replace(treasure_icon_plain, treasure_icon)
elif generic_icon in s:
    s = s.replace(generic_icon, treasure_icon)
elif treasure_icon not in s:
    raise SystemExit('Could not locate database category icon renderer')

# Keep exactly one Item/Card detail renderer in the produced page. The old
# inline renderer used to build a complete legacy table before item-detail-rms.js
# replaced it. Remove that implementation completely, leaving only a neutral
# host for the canonical RMS renderer.
canonical_function = '''  function itemDetail(id, cardRoute=false) {
    const item = getItem(id);
    if (!item) return notFound();
    queueMicrotask(() => window.RZ_RENDER_RMS_ITEM_DETAIL?.());
    return `<div class="rz-rms-pending" data-item-id="${esc(item.id)}"></div>`;
  }
'''
pattern = re.compile(
    r"  function itemDetail\(id, cardRoute=false\) \{.*?\n  \}\n\n  function mapDetail\(id\) \{",
    re.S,
)
s, replaced = pattern.subn(canonical_function + '\n  function mapDetail(id) {', s, count=1)
if replaced != 1:
    raise SystemExit(f'Expected exactly one legacy itemDetail renderer, replaced {replaced}')

p.write_text(s, encoding='utf-8')

# The RMS renderers previously shipped their own blue palette and were recolored
# only afterwards by item-visual-cleanup.js. That caused a visible blue -> gray
# flash. Patch the renderer source itself to the final gray palette so the first
# painted frame already has the final appearance.
palette = {
    '#4f83aa':'#aabcc9',
    '#bfe1f7':'#c8d8e6',
    '#064d7d':'#24384a',
    '#dff1ff':'#f7fafc',
    '#063d63':'#263846',
    '#c7e7fa':'#dde8f1',
    '#eaf7ff':'#fbfdff',
    '#17456b':'#263846',
    '#5d8fb4':'#9fb3c4',
    '#bfe3fb':'#c8d8e6',
    '#4f86ad':'#aabcc9',
    '#073e64':'#263846',
    '#cae8fb':'#dde8f1',
    '#e6f4fd':'#fbfdff',
}

for asset in [Path('assets/item-detail-rms.js'), Path('assets/item-db-optimized.js')]:
    text = asset.read_text(encoding='utf-8')
    text = text.replace("const description = item.description || 'No description available.';", "const description = item.description || 'n/a';")
    for old, new in palette.items():
        text = text.replace(old, new)
    asset.write_text(text, encoding='utf-8')

# Do not expose implementation/source provenance inside the visible item page.
detail = Path('assets/item-detail-rms.js')
text = detail.read_text(encoding='utf-8')
text = text.replace("      <div class=\"rz-rms-note\">Client-side fields come from the Zero client. Buy/Sell, NPC vendors, Item Script and drops remain n/a until verified server-side data is imported.</div>\n", "")

# The router now gives the canonical renderer a clean host, so render in a
# microtask rather than waiting for animation frames.
text = text.replace(
    "  function afterRender() {\n    requestAnimationFrame(() => requestAnimationFrame(render));\n  }",
    "  function afterRender() {\n    queueMicrotask(render);\n  }"
)
detail.write_text(text, encoding='utf-8')
