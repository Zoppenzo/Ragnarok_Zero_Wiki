from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
index_path = ROOT / "index.html"
text = index_path.read_text(encoding="utf-8")

# Load official item data after RO_DATA is declared but before the renderer
# captures window.RO_DATA. This keeps item names and client-side fields native
# to the database instead of rewriting them after render.
if 'assets/client-items-data.js' not in text:
    marker = """</script>
<script>
(() => {
  const DATA = window.RO_DATA;"""
    replacement = """</script>
<script src="assets/client-items-data.js"></script>
<script src="assets/client-items.js"></script>
<script>
(() => {
  const DATA = window.RO_DATA;"""
    if marker not in text:
        raise SystemExit("Could not locate RO_DATA/renderer boundary for item scripts")
    text = text.replace(marker, replacement, 1)

# Expand the item infobox with client-side fields when they exist. Drop/source
# information remains separate and is not inferred from the client.
old_infobox = """${infoRow(t('type'),esc(item.type))}${infoRow(t('subtype'),esc(item.subtype||t('unknown')))}${infoRow(t('requiredLevel'),esc(val(item.requiredLevel)))}${infoRow(t('weight'),esc(val(item.weight)))}${item.type==='Card'?infoRow(t('slot'),esc(item.equipmentSlot||t('unknown'))):''}"""
new_infobox = """${infoRow(t('type'),esc(item.type))}${infoRow(t('subtype'),esc(item.subtype||t('unknown')))}${item.requiredLevel!=null?infoRow(t('requiredLevel'),esc(val(item.requiredLevel))):''}${item.weight!=null?infoRow(t('weight'),esc(val(item.weight))):''}${item.atk!=null?infoRow('ATK',esc(val(item.atk))):''}${item.matk!=null?infoRow('MATK',esc(val(item.matk))):''}${item.def!=null?infoRow('DEF',esc(val(item.def))):''}${item.weaponLevel!=null?infoRow('Weapon Level',esc(val(item.weaponLevel))):''}${item.element?infoRow('Element',esc(item.element)):''}${item.slotCount?infoRow('Slots',esc(val(item.slotCount))):''}${item.position?infoRow('Position',esc(item.position)):''}${item.equipmentSlot?infoRow('Equipped on',esc(item.equipmentSlot)):''}"""
if old_infobox in text:
    text = text.replace(old_infobox, new_infobox, 1)
elif "item.atk!=null?infoRow('ATK'" not in text:
    raise SystemExit("Could not patch item infobox")

# Avoid rendering an empty lead paragraph for the compact client dataset.
old_lead = '<div class="article-body"><p class="article-lead">${esc(txt(item.description))}</p>${toc('
new_lead = '<div class="article-body">${item.description?`<p class="article-lead">${esc(txt(item.description))}</p>`:\'\'}${toc('
if old_lead in text:
    text = text.replace(old_lead, new_lead, 1)
elif "item.description?`<p class=\"article-lead\"" not in text:
    raise SystemExit("Could not patch empty item description rendering")

index_path.write_text(text, encoding="utf-8")
print("Official client item UI integration applied.")
