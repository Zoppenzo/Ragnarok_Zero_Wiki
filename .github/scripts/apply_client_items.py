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
<script src="assets/client-item-stats.js"></script>
<script src="assets/client-item-descriptions.js"></script>
<script src="assets/client-items.js"></script>
<script src="assets/item-db-optimized.js"></script>
<script>
(() => {
  const DATA = window.RO_DATA;"""
    if marker not in text:
        raise SystemExit("Could not locate RO_DATA/renderer boundary for item scripts")
    text = text.replace(marker, replacement, 1)
else:
    if 'assets/client-item-stats.js' not in text:
        marker = '<script src="assets/client-items-data.js"></script>\n<script src="assets/client-items.js"></script>'
        replacement = '<script src="assets/client-items-data.js"></script>\n<script src="assets/client-item-stats.js"></script>\n<script src="assets/client-items.js"></script>'
        if marker not in text:
            raise SystemExit('Could not insert client item stat overlay')
        text = text.replace(marker, replacement, 1)
    if 'assets/client-item-descriptions.js' not in text:
        marker = '<script src="assets/client-item-stats.js"></script>\n<script src="assets/client-items.js"></script>'
        replacement = '<script src="assets/client-item-stats.js"></script>\n<script src="assets/client-item-descriptions.js"></script>\n<script src="assets/client-items.js"></script>'
        if marker not in text:
            raise SystemExit('Could not insert client item description overlay')
        text = text.replace(marker, replacement, 1)
    if 'assets/item-db-optimized.js' not in text:
        marker = '<script src="assets/client-items.js"></script>'
        replacement = '<script src="assets/client-items.js"></script>\n<script src="assets/item-db-optimized.js"></script>'
        if marker not in text:
            raise SystemExit('Could not insert optimized item database script')
        text = text.replace(marker, replacement, 1)

# Use the optimized paginated renderer for Items and Cards. Other searchable
# databases keep the original renderer.
old_wire = '    setTimeout(() => wireList(type), 0);'
new_wire = "    setTimeout(() => { if (!window.RZ_ITEM_DB_OPT?.wire(type)) wireList(type); }, 0);"
if old_wire in text:
    text = text.replace(old_wire, new_wire, 1)
elif new_wire not in text:
    raise SystemExit('Could not patch list renderer for item pagination')

# Expand the legacy item infobox when it still exists. Once the canonical RMS
# renderer has replaced the legacy detail markup, these legacy-only patches are
# intentionally skipped so repeated workflow runs remain idempotent.
canonical_rms = 'rz-rms-pending' in text and 'RZ_RENDER_RMS_ITEM_DETAIL' in text
old_infobox = """${infoRow(t('type'),esc(item.type))}${infoRow(t('subtype'),esc(item.subtype||t('unknown')))}${infoRow(t('requiredLevel'),esc(val(item.requiredLevel)))}${infoRow(t('weight'),esc(val(item.weight)))}${item.type==='Card'?infoRow(t('slot'),esc(item.equipmentSlot||t('unknown'))):''}"""
new_infobox = """${infoRow(t('type'),esc(item.type))}${infoRow(t('subtype'),esc(item.subtype||t('unknown')))}${item.requiredLevel!=null?infoRow(t('requiredLevel'),esc(val(item.requiredLevel))):''}${item.weight!=null?infoRow(t('weight'),esc(val(item.weight))):''}${item.atk!=null?infoRow('ATK',esc(val(item.atk))):''}${item.matk!=null?infoRow('MATK',esc(val(item.matk))):''}${item.def!=null?infoRow('DEF',esc(val(item.def))):''}${item.mdef!=null?infoRow('MDEF',esc(val(item.mdef))):''}${item.buyPrice!=null?infoRow('NPC Buy',esc(val(item.buyPrice))+' Zeny'):''}${item.sellPrice!=null?infoRow('Sell Price',esc(val(item.sellPrice))+' Zeny'):''}${item.weaponLevel!=null?infoRow('Weapon Level',esc(val(item.weaponLevel))):''}${item.element?infoRow('Element',esc(item.element)):''}${item.slotCount!=null&&item.type==='Equipment'?infoRow('Slots',esc(val(item.slotCount))):''}${item.position?infoRow('Position',esc(item.position)):''}${item.equipmentSlot?infoRow('Equipped on',esc(item.equipmentSlot)):''}"""
if not canonical_rms:
    if old_infobox in text:
        text = text.replace(old_infobox, new_infobox, 1)
    else:
        old_price = "${item.mdef!=null?infoRow('MDEF',esc(val(item.mdef))):''}${item.sellPrice!=null?infoRow('Sell Price',esc(val(item.sellPrice))):''}"
        new_price = "${item.mdef!=null?infoRow('MDEF',esc(val(item.mdef))):''}${item.buyPrice!=null?infoRow('NPC Buy',esc(val(item.buyPrice))+' Zeny'):''}${item.sellPrice!=null?infoRow('Sell Price',esc(val(item.sellPrice))+' Zeny'):''}"
        if old_price in text:
            text = text.replace(old_price, new_price, 1)
        elif "item.buyPrice!=null?infoRow('NPC Buy'" not in text:
            old_mid = "${item.def!=null?infoRow('DEF',esc(val(item.def))):''}${item.weaponLevel!=null?infoRow('Weapon Level',esc(val(item.weaponLevel))):''}"
            new_mid = "${item.def!=null?infoRow('DEF',esc(val(item.def))):''}${item.mdef!=null?infoRow('MDEF',esc(val(item.mdef))):''}${item.buyPrice!=null?infoRow('NPC Buy',esc(val(item.buyPrice))+' Zeny'):''}${item.sellPrice!=null?infoRow('Sell Price',esc(val(item.sellPrice))+' Zeny'):''}${item.weaponLevel!=null?infoRow('Weapon Level',esc(val(item.weaponLevel))):''}"
            if old_mid in text:
                text = text.replace(old_mid, new_mid, 1)
            elif "item.mdef!=null?infoRow('MDEF'" not in text:
                raise SystemExit("Could not patch item infobox")

# Avoid rendering an empty lead paragraph for the compact client dataset when
# the legacy detail page is still present.
if not canonical_rms:
    old_lead = '<div class="article-body"><p class="article-lead">${esc(txt(item.description))}</p>${toc('
    new_lead = '<div class="article-body">${item.description?`<p class="article-lead">${esc(txt(item.description))}</p>`:\'\'}${toc('
    if old_lead in text:
        text = text.replace(old_lead, new_lead, 1)
    elif "item.description?`<p class=\"article-lead\"" not in text:
        raise SystemExit("Could not patch empty item description rendering")

# The homepage Ragnarok Database box must open the searchable database for each
# entity type instead of the explanatory overview pages.
database_links = {
    "['monster','#/monsters'": "['monster','#/database/monsters'",
    "['item','#/items'": "['item','#/database/items'",
    "['card','#/cards'": "['card','#/database/cards'",
    "['affix','#/affixes'": "['affix','#/database/affixes'",
    "['memorial','#/memorial-dungeons'": "['memorial','#/database/memorial-dungeons'",
    "['map','#/maps'": "['map','#/database/maps'",
    "['skill','#/skills'": "['skill','#/database/skills'",
    "['quest','#/quests'": "['quest','#/database/quests'",
    "['npc','#/npcs'": "['npc','#/database/npcs'",
}
for old, new in database_links.items():
    if old in text:
        text = text.replace(old, new, 1)

if 'function databaseRouteView(type)' not in text:
    marker = "  function listView(type) {"
    dispatcher = """  function databaseRouteView(type) {
    if (['monsters','items','cards','maps','skills','quests','npcs'].includes(type)) return listView(type);
    if (type === 'affixes') return affixDatabasePage();
    if (type === 'memorial-dungeons') return memorialDungeonDatabasePage();
    return notFound();
  }

"""
    if marker not in text:
        raise SystemExit('Could not locate listView for database dispatcher')
    text = text.replace(marker, dispatcher + marker, 1)

if "hash[0]==='database'&&hash[1]" not in text:
    marker = "    else if(hash[0]==='classes'&&!hash[1]) html=classIndexView();"
    replacement = "    else if(hash[0]==='database'&&hash[1]) html=databaseRouteView(hash[1]);\n" + marker
    if marker not in text:
        raise SystemExit('Could not locate router insertion point for database routes')
    text = text.replace(marker, replacement, 1)

old_item_route = "    else if(hash[0]==='items'&&hash[1]) html=memorialDatabaseEntityPage('items',hash[1]);"
new_item_route = "    else if(hash[0]==='items'&&hash[1]) html=getItem(hash[1])?itemDetail(hash[1],false):memorialDatabaseEntityPage('items',hash[1]);"
if old_item_route in text:
    text = text.replace(old_item_route, new_item_route, 1)
elif new_item_route not in text:
    raise SystemExit('Could not patch item detail routing')

if "hash[0]==='cards'&&hash[1]" not in text:
    marker = "    else if(hash[0]==='cards'&&!hash[1]) html=cardsOverviewPage();"
    replacement = "    else if(hash[0]==='cards'&&hash[1]) html=itemDetail(hash[1],true);\n" + marker
    if marker not in text:
        raise SystemExit('Could not patch card detail routing')
    text = text.replace(marker, replacement, 1)

old_monster_route = "    else if(hash[0]==='monsters'&&hash[1]) html=memorialDatabaseEntityPage('monsters',hash[1]);"
new_monster_route = "    else if(hash[0]==='monsters'&&hash[1]) html=getMonster(hash[1])?monsterDetail(hash[1]):memorialDatabaseEntityPage('monsters',hash[1]);"
if old_monster_route in text:
    text = text.replace(old_monster_route, new_monster_route, 1)
elif new_monster_route not in text:
    raise SystemExit('Could not patch monster detail routing')

index_path.write_text(text, encoding="utf-8")
print("Official client item UI, descriptions, pagination and direct database routing applied.")
