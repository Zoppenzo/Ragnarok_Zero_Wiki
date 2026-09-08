from pathlib import Path

# Keep the final visual override loaded after the database renderers.
p = Path('index.html')
s = p.read_text(encoding='utf-8')
tag = '<script src="assets/item-visual-cleanup.js"></script>'
if tag not in s:
    s = s.replace('</body>', f'  {tag}\n</body>')
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
detail.write_text(text, encoding='utf-8')
