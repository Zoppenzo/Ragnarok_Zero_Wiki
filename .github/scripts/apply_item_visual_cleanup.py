from pathlib import Path

# Keep the final visual override loaded after the database renderers.
p = Path('index.html')
s = p.read_text(encoding='utf-8')
tag = '<script src="assets/item-visual-cleanup.js"></script>'
if tag not in s:
    s = s.replace('</body>', f'  {tag}\n</body>')

# The Item category PNG is a client UI capture and can render as an empty-looking
# transparent box at hub size. Reuse the local bag symbol already shipped in the
# wiki sprite so the Item/Objet category always has a visible icon.
old_icon = 'const icon = `<img class="database-category-icon database-category-icon-${key}" src="${src}" alt="">`;'
new_icon = 'const icon = key === \'item\' ? `<svg class="icon database-category-icon database-category-icon-item" aria-hidden="true"><use href="#i-item"></use></svg>` : `<img class="database-category-icon database-category-icon-${key}" src="${src}" alt="">`;'
if old_icon in s:
    s = s.replace(old_icon, new_icon)
elif new_icon not in s:
    raise SystemExit('Could not locate database category icon renderer')

# Item/Card detail pages used to render the legacy detail table first and then
# replace it with the RMS sheet a couple of animation frames later. Do not put
# the legacy table in the DOM at all: render only a neutral host and let the
# canonical RMS renderer fill it immediately.
legacy_head = """  function itemDetail(id, cardRoute=false) {
    const item = getItem(id);
    if (!item) return notFound();
"""
canonical_head = """  function itemDetail(id, cardRoute=false) {
    const item = getItem(id);
    if (!item) return notFound();
    queueMicrotask(() => window.RZ_RENDER_RMS_ITEM_DETAIL?.());
    return `<div class=\"rz-rms-pending\" data-item-id=\"${esc(item.id)}\"></div>`;
"""
if legacy_head in s:
    s = s.replace(legacy_head, canonical_head, 1)
elif canonical_head not in s:
    raise SystemExit('Could not locate legacy item detail renderer')

p.write_text(s, encoding='utf-8')

# Unknown information must stay neutral instead of being presented as prose.
for asset in [Path('assets/item-detail-rms.js'), Path('assets/item-db-optimized.js')]:
    text = asset.read_text(encoding='utf-8')
    text = text.replace("const description = item.description || 'No description available.';", "const description = item.description || 'n/a';")
    asset.write_text(text, encoding='utf-8')

# Do not expose implementation/source provenance inside the visible item page.
detail = Path('assets/item-detail-rms.js')
text = detail.read_text(encoding='utf-8')
text = text.replace("      <div class=\"rz-rms-note\">Client-side fields come from the Zero client. Buy/Sell, NPC vendors, Item Script and drops remain n/a until verified server-side data is imported.</div>\n", "")

# The old renderer deliberately waited two animation frames, which made the
# previous table visible as a flash. The router now gives us a clean host, so a
# microtask is enough and keeps the RMS sheet as the only rendered table.
text = text.replace(
    "  function afterRender() {\n    requestAnimationFrame(() => requestAnimationFrame(render));\n  }",
    "  function afterRender() {\n    queueMicrotask(render);\n  }"
)
detail.write_text(text, encoding='utf-8')
