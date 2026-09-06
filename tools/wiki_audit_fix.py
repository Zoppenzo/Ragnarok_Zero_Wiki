from pathlib import Path
import re

PATH = Path('index.html')
text = PATH.read_text(encoding='utf-8')
original = text
changes = []


def replace(old, new, label, required=False):
    global text
    count = text.count(old)
    if required and count == 0:
        raise SystemExit(f'Missing required pattern: {label}')
    if count:
        text = text.replace(old, new)
        changes.append((label, count))
    return count


def regex(pattern, repl, label, flags=0, required=False):
    global text
    text2, count = re.subn(pattern, repl, text, flags=flags)
    if required and count == 0:
        raise SystemExit(f'Missing required regex: {label}')
    if count:
        text = text2
        changes.append((label, count))
    return count


# ---------------------------------------------------------------------------
# 1) General wording / footer: this is no longer a demo.
# ---------------------------------------------------------------------------
replace(
    '<span id="footer-note">Demo data are incomplete and may not match live game values.</span>',
    '<span id="footer-note">Some database sections are still being documented. Verification status is shown on each section.</span>',
    'static footer wording'
)
replace(
    "footer: 'Demo data are incomplete and may not match live game values.'",
    "footer: 'Some database sections are still being documented. Verification status is shown on each section.'",
    'English footer translation'
)
replace(
    "footer: 'Les données de démo sont incomplètes et peuvent différer des valeurs en jeu.'",
    "footer: 'Certaines bases de données sont encore en cours de documentation. Le statut de vérification est indiqué par section.'",
    'French footer translation'
)

# ---------------------------------------------------------------------------
# 2) September 3 live update: 2nd classes are live, current Base/Job cap 60.
#    Do not invent detailed class skill data; keep detailed content pending.
# ---------------------------------------------------------------------------
second_classes = {
    'knight': ('Knight', 'Swordman'),
    'crusader': ('Crusader', 'Swordman'),
    'wizard': ('Wizard', 'Mage'),
    'sage': ('Sage', 'Mage'),
    'hunter': ('Hunter', 'Archer'),
    'bard': ('Bard', 'Archer'),
    'dancer': ('Dancer', 'Archer'),
    'blacksmith': ('Blacksmith', 'Merchant'),
    'alchemist': ('Alchemist', 'Merchant'),
    'assassin': ('Assassin', 'Thief'),
    'rogue': ('Rogue', 'Thief'),
    'priest': ('Priest', 'Acolyte'),
    'monk': ('Monk', 'Acolyte'),
}
for cid, (name, parent) in second_classes.items():
    line_pattern = rf'^\s*\{{ id: "{re.escape(cid)}"[^\n]*\}}[,]?$'
    suffix = ',' if cid != 'monk' else ''
    newline = (
        f'    {{ id: "{cid}", name: "{name}", tier: "Second Class", group: "second", '
        f'parentId: "{parent.lower()}", releaseStatus: "available", image: "assets/classes/{cid}.png", '
        f'description: {{ en: "{name} is a currently playable second class branching from {parent} in Ragnarok Zero: Global.", '
        f'fr: "{name} est une seconde classe actuellement jouable issue de {parent} dans Ragnarok Zero: Global." }}, '
        f'notes: {{ en: "Available since the September 3, 2026 update. Detailed Global skill values are added only after current-version verification.", '
        f'fr: "Disponible depuis la mise à jour du 3 septembre 2026. Les valeurs détaillées des skills Global ne sont ajoutées qu’après vérification sur la version actuelle." }} }}{suffix}'
    )
    regex(line_pattern, newline, f'{name} set live', flags=re.M, required=True)

replace(
    "${second} <span class=\"badge unverified\" style=\"margin-left:8px\">${navLabel('Coming soon','Bientôt disponible')}</span>",
    "${second} <span class=\"badge verified\" style=\"margin-left:8px\">${navLabel('Available','Disponible')}</span>",
    'second-class navigation badge'
)
replace("Upcoming Second Classes", "Second Classes", 'second-class English heading')
replace("Secondes classes à venir", "Secondes classes", 'second-class French heading')

# Empty live 2nd-class pages should never say "None" as if the class has no skills.
replace(
    " : `<div class=\"empty\">${t('none')}</div>`;\n    const classGenders",
    " : c.group === 'second' ? `<div class=\"notice info-notice\"><svg class=\"notice-icon\"><use href=\"#i-info\"></use></svg><div><strong>${navLabel('Global skill documentation in progress','Documentation des skills Global en cours')}</strong><br>${navLabel('This class is playable. Its detailed skill tree is intentionally left unverified until the current Global values are documented; data from other RO versions is not substituted.','Cette classe est jouable. Son arbre de skills détaillé reste volontairement non vérifié tant que les valeurs Global actuelles ne sont pas documentées ; les données des autres versions de RO ne sont pas utilisées à la place.')}</div></div>` : `<div class=\"empty\">${t('none')}</div>`;\n    const classGenders",
    'empty live second-class skill tree message'
)

replace('Current Global scope — 1 September 2026', 'Current Global scope — 6 September 2026', 'English live-scope date')
replace('Périmètre Global actuel — 1er septembre 2026', 'Périmètre Global actuel — 6 septembre 2026', 'French live-scope date')
replace(
    'The live launch cap is Base Level 50. Novice changes job from Job Level 10, and the six currently available first classes can progress to Job Level 50. Future class and level-cap increases are deliberately not mixed into this live table.',
    'Since the September 3 update, the live cap is Base Level 60 / Job Level 60 and the thirteen second classes are available. Novice still changes to a first class from Job Level 10, and first classes can change to their second-job path from Job Level 40. Future cap increases are not mixed into this live table.',
    'English current cap notice', required=True
)
replace(
    'Le plafond actuellement en ligne est le Base Level 50. Le Novice peut changer de classe à partir du Job Level 10 et les six premières classes actuellement disponibles peuvent progresser jusqu’au Job Level 50. Les futures classes et hausses de niveau ne sont volontairement pas mélangées à ce tableau du contenu live.',
    'Depuis la mise à jour du 3 septembre, le plafond live est Base Level 60 / Job Level 60 et les treize secondes classes sont disponibles. Le Novice change toujours vers une première classe à partir du Job Level 10, puis les premières classes peuvent passer vers leur seconde classe à partir du Job Level 40. Les futures hausses de niveau ne sont pas mélangées à ce tableau du contenu live.',
    'French current cap notice', required=True
)
replace(
    'Base Level 50 / first-class Job Level 50 are the current live limits documented by this page.',
    'Base Level 60 / Job Level 60 are the current live limits documented by this page; second classes are now playable.',
    'English progression cap'
)
replace(
    'Base Level 50 / Job Level 50 de première classe sont les limites live actuellement documentées par cette page.',
    'Base Level 60 / Job Level 60 sont les limites live actuellement documentées par cette page ; les secondes classes sont désormais jouables.',
    'French progression cap'
)
replace(
    'The live launch cap documented by this wiki is Base Level 50 and Job Level 50 for the currently available first classes. See the Levels page for the progression flow and the current cap table.',
    'The current live cap documented by this wiki is Base Level 60 / Job Level 60 following the September 3 update, with second classes now available. See the Levels page for the progression flow and current cap.',
    'English experience cap'
)
replace(
    'Le plafond live documenté par ce wiki est le Base Level 50 et le Job Level 50 pour les premières classes actuellement disponibles. Consulte la page Niveaux pour le chemin de progression et le tableau des plafonds actuels.',
    'Le plafond live documenté par ce wiki est désormais Base Level 60 / Job Level 60 depuis la mise à jour du 3 septembre, avec les secondes classes disponibles. Consulte la page Niveaux pour le chemin de progression et le plafond actuel.',
    'French experience cap'
)

# Add the live patch note to the source list when the Levels page already cites official sources.
replace(
    "['Official GNJOY — EXP requirements / Game Guide 21','https://roz.mygnjoy.com/fr/intro/guide/21'],",
    "['Official GNJOY — September 3 update: 2nd Jobs / increased level cap','https://roz.mygnjoy.com/en/news/update/92'],\n        ['Official GNJOY — EXP requirements / Game Guide 21','https://roz.mygnjoy.com/fr/intro/guide/21'],",
    'official September update source'
)

# ---------------------------------------------------------------------------
# 3) Explicit database honesty: empty indexes should say they are not populated.
# ---------------------------------------------------------------------------
replace(
    "      <p>${t(cfg.intro)}</p>\n      ${demoAlert()}",
    "      <p>${t(cfg.intro)}</p>\n      ${listData(type).length ? '' : `<div class=\"notice info-notice\"><svg class=\"notice-icon\"><use href=\"#i-info\"></use></svg><div><strong>${navLabel('Database not populated yet','Base de données non remplie pour le moment')}</strong><br>${navLabel('The explanatory wiki pages are available, but this searchable index does not yet contain imported gameplay entries. No placeholder values are generated.','Les pages explicatives du wiki sont disponibles, mais cet index de recherche ne contient pas encore d’entrées de gameplay importées. Aucune valeur factice n’est générée.')}</div></div>`}\n      ${demoAlert()}",
    'empty database notice', required=True
)

# ---------------------------------------------------------------------------
# 4) Leveling Finder: make x1/x2/x3 actually affect the displayed Base EXP.
# ---------------------------------------------------------------------------
replace(
    "<div class=\"entity-meta\">Lv. ${m.level} · ${t('baseExp')}: ${val(m.baseExp)}</div>",
    "<div class=\"entity-meta\">Lv. ${m.level} · ${t('baseExp')}: ${m.baseExp == null ? t('unknown') : Math.round(Number(m.baseExp) * Number(mult.value || 1))}</div>",
    'leveling EXP multiplier', required=True
)

# ---------------------------------------------------------------------------
# 5) Build Planner wording: it currently sums stat values, not RO stat-point costs.
# ---------------------------------------------------------------------------
replace("buildTitle: 'Build Planner'", "buildTitle: 'Stat Allocator'", 'English stat tool title')
replace("buildPlanner: 'Build Planner'", "buildPlanner: 'Stat Allocator'", 'English stat tool panel')
replace("pointsUsed: 'Points used'", "pointsUsed: 'Stat total'", 'English stat total label')
replace(
    "buildText: 'Allocate STR, AGI, VIT, INT, DEX and LUK. Official stat-cost formulas are not guessed.'",
    "buildText: 'Preview STR, AGI, VIT, INT, DEX and LUK values. This tool does not claim to calculate stat-point costs until the current Global formula is verified.'",
    'English stat tool description'
)
replace("buildTitle: 'Build Planner'", "buildTitle: 'Répartiteur de stats'", 'French duplicate stat title')
replace("buildPlanner: 'Build Planner'", "buildPlanner: 'Répartiteur de stats'", 'French duplicate stat panel')
replace("pointsUsed: 'Points utilisés'", "pointsUsed: 'Total des stats'", 'French stat total label')
replace(
    'buildText: "Répartis STR, AGI, VIT, INT, DEX et LUK. Les formules officielles ne sont pas inventées."',
    'buildText: "Prévisualise STR, AGI, VIT, INT, DEX et LUK. Cet outil ne prétend pas calculer le coût en points tant que la formule Global actuelle n’est pas vérifiée."',
    'French stat tool description'
)
replace("'Build Planner','Build Planner','tools'", "'Stat Allocator','Répartiteur de stats','tools'", 'sidebar stat tool label')

# ---------------------------------------------------------------------------
# 6) Replace the empty Memorial Dungeon placeholder with a useful current page.
#    Detailed entry mechanics remain deliberately partial.
# ---------------------------------------------------------------------------
memorial_fn = r'''  function memorialDungeonDatabasePage() {
    const dungeons = [
      ['Poring Village', navLabel('Documented early-game Memorial Dungeon. Detailed rewards and reset rules remain on the dedicated guide backlog.','Mémorial Donjon de début de progression déjà documenté. Les récompenses détaillées et règles de reset restent à compléter dans la fiche dédiée.'), 'partial'],
      ['Prontera Culvert', navLabel('Part of the current September progression/content wave. Entry details, bosses and reward tables must be verified on Global before being marked complete.','Fait partie de la vague de contenu/progression de septembre. L’accès, les boss et les récompenses doivent être vérifiés sur Global avant passage en complet.'), 'partial'],
      ['Orc Memory', navLabel('Part of the current September progression/content wave. Detailed Global mechanics are still being documented.','Fait partie de la vague de contenu/progression de septembre. Les mécaniques Global détaillées sont encore en cours de documentation.'), 'partial']
    ];
    return `${breadcrumbs([{label:navLabel('Memorial Dungeons','Mémorial Donjon')}])}
      <div class="article-heading"><h1>${icon('map')}${navLabel('Memorial Dungeon Database','Base des Mémorial Donjons')}</h1><div class="page-subtitle">${t('fromWiki')}</div></div>
      <p class="article-lead">${navLabel('Memorial Dungeons are instanced cooperative content. This index separates confirmed live availability from detailed mechanics that are still being verified.','Les Mémorial Donjons sont des contenus instanciés coopératifs. Cet index sépare la disponibilité live confirmée des mécaniques détaillées encore en cours de vérification.')}</p>
      <div class="notice info-notice"><svg class="notice-icon"><use href="#i-info"></use></svg><div><strong>${navLabel('September 3 scope','Périmètre du 3 septembre')}</strong><br>${navLabel('The September update introduced new quests/content alongside second jobs and the increased level cap. Detailed dungeon values are never copied from another RO region without Global verification.','La mise à jour de septembre a ajouté de nouvelles quêtes et du contenu en même temps que les secondes classes et la hausse du level cap. Les valeurs détaillées des donjons ne sont jamais copiées d’une autre région RO sans vérification Global.')}</div></div>
      <div class="table-wrap"><table><thead><tr><th>${navLabel('Memorial Dungeon','Mémorial Donjon')}</th><th>${navLabel('Documentation status','État de la documentation')}</th><th>${navLabel('Status','Statut')}</th></tr></thead><tbody>
        ${dungeons.map(([name,desc,status])=>`<tr><th>${esc(name)}</th><td>${desc}</td><td>${sectionStatusPill(status)}</td></tr>`).join('')}
      </tbody></table></div>
      ${officialSources([
        ['Official GNJOY — September 3 update','https://roz.mygnjoy.com/en/news/update/92'],
        ['MidgardHub — Complete New Player Guide / Memorial Dungeon','https://midgardhub.com/guides/new-player'],
        ['Prontera.info — current release tracker','https://roz.prontera.info/release']
      ])}`;
  }
'''
regex(
    r"  function memorialDungeonDatabasePage\(\) \{.*?\n  \}\n\n  function statusEffectsPage",
    memorial_fn + "\n  function statusEffectsPage",
    'Memorial Dungeon page', flags=re.S, required=True
)

# ---------------------------------------------------------------------------
# 7) Dedicated pages for three menu entries that previously fell into the
#    generic 'No current data available' placeholder.
# ---------------------------------------------------------------------------
new_pages = r'''
  function craftingPage(topic) {
    const title = navLabel('Crafting','Craft');
    return `${breadcrumbs([{label:title}])}
      <div class="article-heading"><h1>${icon('item')}${title}</h1><div class="page-subtitle">${t('fromWiki')}</div></div>
      <p class="article-lead">${navLabel('Crafting groups together systems that create usable items or equipment from materials. Recipes are version-sensitive, so this page only promotes recipe tables after Global verification.','Le Craft regroupe les systèmes permettant de créer des objets ou équipements à partir de matériaux. Les recettes dépendent fortement de la version ; les tableaux détaillés ne passent en vérifié qu’après contrôle sur Global.')}</p>
      ${toc([{id:'overview',label:navLabel('Overview','Aperçu')},{id:'current-systems',label:navLabel('Current systems','Systèmes actuels')},{id:'verification',label:navLabel('Recipe verification','Vérification des recettes')}])}
      <h2 id="overview">${navLabel('Overview','Aperçu')}</h2>
      <p>${navLabel('Class skills such as Arrow Crafting and profession systems such as Blacksmith forging belong here, while Refinement and random Affixes remain separate mechanics with their own pages.','Les skills de classe comme Arrow Crafting et les systèmes de profession comme la forge Blacksmith sont regroupés ici, tandis que le Raffinement et les Affixes restent des mécaniques séparées avec leurs propres pages.')}</p>
      <h2 id="current-systems">${navLabel('Current crafting systems','Systèmes de craft actuels')}</h2>
      <div class="wiki-feature-list">
        <div><strong>Arrow Crafting</strong><p>${navLabel('Archer quest skill that converts compatible materials into arrows. Material-to-arrow outputs belong in a dedicated verified recipe table.','Skill de quête Archer transformant certains matériaux en flèches. Les conversions matériau → flèches seront ajoutées dans un tableau vérifié dédié.')}</p></div>
        <div><strong>Blacksmith Forging</strong><p>${navLabel('Blacksmith is now a playable second class. Forging recipes and Global-specific weapon results are documented separately from generic Renewal/iRO data.','Blacksmith est désormais une seconde classe jouable. Les recettes de forge et résultats propres à Global sont documentés séparément des données génériques Renewal/iRO.')}</p></div>
        <div><strong>${navLabel('Quest / system recipes','Recettes de quêtes / systèmes')}</strong><p>${navLabel('Some equipment and utility items are produced by NPC or system recipes. These are added recipe by recipe once the live inputs and outputs are confirmed.','Certains équipements et objets utilitaires sont produits via des recettes NPC ou système. Ils sont ajoutés recette par recette après confirmation des composants et résultats live.')}</p></div>
      </div>
      <h2 id="verification">${navLabel('Recipe verification','Vérification des recettes')}</h2>
      <div class="notice"><svg class="notice-icon"><use href="#i-warning"></use></svg><div>${navLabel('Do not use TWROZ/iRO recipe quantities as Global values unless they have been checked in the current client.','Ne pas utiliser les quantités de recettes TWROZ/iRO comme valeurs Global tant qu’elles n’ont pas été contrôlées dans le client actuel.')}</div></div>
      ${officialSources([
        ['Official GNJOY — September 3 update','https://roz.mygnjoy.com/en/news/update/92'],
        ['MidgardHub — current Global guides/database','https://midgardhub.com/']
      ])}`;
  }

  function enchantmentPage(topic) {
    const title = navLabel('Enchantment','Enchantement');
    return `${breadcrumbs([{label:title}])}
      <div class="article-heading"><h1>${icon('item')}${title}</h1><div class="page-subtitle">${t('fromWiki')}</div></div>
      <p class="article-lead">${navLabel('Enchantments are deterministic or system-specific bonuses applied through an enchantment mechanic. They are not the same thing as random drop Affixes.','Les Enchantements sont des bonus appliqués via un système d’enchantement précis. Ils ne doivent pas être confondus avec les Affixes aléatoires obtenus sur les drops.')}</p>
      ${toc([{id:'overview',label:navLabel('Overview','Aperçu')},{id:'costume',label:navLabel('Costume enchantments','Enchantements de costumes')},{id:'taming-ring',label:'Taming Ring'},{id:'content-enchants',label:navLabel('Content-specific enchantments','Enchantements liés au contenu')}])}
      <h2 id="overview">${navLabel('Enchantments vs Affixes','Enchantements vs Affixes')}</h2>
      <p>${navLabel('Affixes / Random Options are documented on their own page and database. Enchantment systems use their own NPCs, materials, slots and success rules, which must be recorded separately.','Les Affixes / Random Options sont documentés sur leur propre page et leur propre base. Les systèmes d’enchantement utilisent leurs propres NPC, matériaux, slots et règles de réussite, qui doivent être documentés séparément.')}</p>
      <h2 id="costume">${navLabel('Costume enchantments','Enchantements de costumes')}</h2>
      <p>${navLabel('The current Global guide documents a costume-enchantment loop in Prontera: costumes can be exchanged through the Enchanter flow to obtain enchantment gems, then a compatible gem can be applied to a costume. Exact gem pools remain a per-item verification task.','Le guide Global actuel documente un système d’enchantement de costumes à Prontera : des costumes passent par le système Enchanter pour obtenir des gemmes d’enchantement, puis une gemme compatible peut être appliquée à un costume. Les pools exacts de gemmes restent à vérifier objet par objet.')}</p>
      <h2 id="taming-ring">Taming Ring</h2>
      <p>${navLabel('The Pet System has its own Taming Ring enchant progression. Pet Egg bonuses and Lv.1/Lv.2 ring effects remain documented on the Pet System page so the two systems are not duplicated.','Le système de Pet possède sa propre progression d’enchantement Taming Ring. Les bonus des Pet Eggs et effets Lv.1/Lv.2 restent documentés sur la page Système de Pet afin d’éviter les doublons.')}</p>
      <div class="hero-actions"><a class="button" href="#/wiki/pet-system">${miniIcon('monster')}${navLabel('Open Pet System','Ouvrir Système de Pet')}</a><a class="button" href="#/wiki/affixes">${miniIcon('item')}${navLabel('Open Affixes','Ouvrir Affixes')}</a></div>
      <h2 id="content-enchants">${navLabel('Content-specific enchantments','Enchantements liés au contenu')}</h2>
      <div class="notice"><svg class="notice-icon"><use href="#i-warning"></use></svg><div>${navLabel('Detailed NPC costs, success rates and option pools stay Partial until confirmed on the current Global release.','Les coûts NPC, taux de réussite et pools d’options détaillés restent Partiels tant qu’ils ne sont pas confirmés sur la version Global actuelle.')}</div></div>
      ${officialSources([
        ['MidgardHub / Lymd — current Global guide','https://midgardhub.com/guides/new-player'],
        ['MidgardHub — current item database','https://midgardhub.com/database/items']
      ])}`;
  }

  function monsterSkillsPage(topic) {
    const title = navLabel('Monster Skills','Compétences des monstres');
    return `${breadcrumbs([{label:title}])}
      <div class="article-heading"><h1>${icon('skill')}${title}</h1><div class="page-subtitle">${t('fromWiki')}</div></div>
      <p class="article-lead">${navLabel('Monsters can use active and passive combat abilities that are separate from player-class skills. This page defines the database scope without importing Classic/Renewal monster skill tables as if they were Global data.','Les monstres peuvent utiliser des capacités de combat actives ou passives distinctes des skills de classes joueurs. Cette page définit le périmètre de la base sans importer les tables de skills Classic/Renewal comme s’il s’agissait de données Global.')}</p>
      ${toc([{id:'overview',label:navLabel('Overview','Aperçu')},{id:'database-status',label:navLabel('Database status','État de la base')},{id:'verification',label:navLabel('Verification rules','Règles de vérification')}])}
      <h2 id="overview">${navLabel('Monster skill data','Données des skills de monstres')}</h2>
      <p>${navLabel('Useful fields include the skill name, trigger/condition, target, level, cast time, cooldown, element, range and status effect. These fields are added only where current Global evidence exists.','Les champs utiles comprennent le nom du skill, son déclencheur/condition, la cible, le niveau, le cast, le cooldown, l’élément, la portée et les éventuels statuts. Ces champs ne sont ajoutés que lorsqu’une preuve Global actuelle existe.')}</p>
      <h2 id="database-status">${navLabel('Database status','État de la base')}</h2>
      <div class="notice info-notice"><svg class="notice-icon"><use href="#i-info"></use></svg><div>${navLabel('The searchable monster-skill table has not been imported yet. Monster overview pages remain usable, but missing skills must be shown as undocumented rather than assumed absent.','La table recherchable des skills de monstres n’est pas encore importée. Les pages générales Monstres restent utilisables, mais un skill manquant doit être affiché comme non documenté et non comme inexistant.')}</div></div>
      <h2 id="verification">${navLabel('Verification rules','Règles de vérification')}</h2>
      <ul><li>${navLabel('Current Global client/database evidence takes priority.','Les preuves provenant du client/de la base Global actuelle sont prioritaires.')}</li><li>${navLabel('iRO or another region may be used for layout/reference only, not to fill missing live values.','iRO ou une autre région peut servir de référence de présentation, pas à remplir des valeurs live manquantes.')}</li><li>${navLabel('Balance-patch-sensitive values remain Partial until rechecked.','Les valeurs sensibles aux patches d’équilibrage restent Partielles jusqu’à nouvelle vérification.')}</li></ul>
      <div class="hero-actions"><a class="button" href="#/monsters">${miniIcon('monster')}${navLabel('Open Monsters','Ouvrir Monstres')}</a></div>`;
  }

'''
replace('  function mechanicsPage(topic) {', new_pages + '  function mechanicsPage(topic) {', 'dedicated formerly-empty pages', required=True)

replace(
    "    if (id === 'status-effects') return statusEffectsPage(topic);",
    "    if (id === 'status-effects') return statusEffectsPage(topic);\n    if (id === 'monster-exclusive-skills') return monsterSkillsPage(topic);",
    'monster skills route', required=True
)
replace(
    "    if (id === 'refinement-system') return refinementSystemPage(topic);",
    "    if (id === 'refinement-system') return refinementSystemPage(topic);\n    if (id === 'crafting') return craftingPage(topic);\n    if (id === 'enchantment') return enchantmentPage(topic);",
    'craft/enchantment routes', required=True
)

# Add explicit section-status maps for the newly dedicated pages.
status_insert = """    '#/wiki/crafting': { overview:'complete', 'current-systems':'partial', verification:'partial' },\n    '#/wiki/enchantment': { overview:'complete', costume:'partial', 'taming-ring':'complete', 'content-enchants':'partial' },\n    '#/wiki/monster-exclusive-skills': { overview:'complete', 'database-status':'missing', verification:'complete' },\n"""
replace("    '#/wiki/pet-system': {", status_insert + "    '#/wiki/pet-system': {", 'new page verification maps', required=True)

# ---------------------------------------------------------------------------
# 8) Freshness cue: make the current audit date visible without pretending
#    that every partial database row has been reverified.
# ---------------------------------------------------------------------------
replace(
    "<span>Ragnarok Zero Wiki</span>\n        <span id=\"footer-note\">",
    "<span>Ragnarok Zero Wiki · ${navLabel ? '' : ''}</span>\n        <span id=\"footer-note\">",
    'skip invalid dynamic footer patch'
)
# The previous replacement is intentionally harmless if not found. Add a static audit cue to the sidebar note instead.
replace(
    "Community reference project for Ragnarok.",
    "Community reference project for Ragnarok Zero: Global. Content audit: 6 Sep 2026.",
    'static audit cue'
)
replace(
    "sidebarNote: 'Community reference project for Ragnarok.'",
    "sidebarNote: 'Community reference project for Ragnarok Zero: Global. Content audit: 6 Sep 2026.'",
    'English sidebar audit cue'
)
replace(
    "sidebarNote: 'Projet de référence communautaire pour Ragnarok.'",
    "sidebarNote: 'Projet de référence communautaire pour Ragnarok Zero: Global. Audit du contenu : 6 sept. 2026.'",
    'French sidebar audit cue'
)

# Guardrails: these obsolete states must be gone after the patch.
for bad in [
    'Current Global scope — 1 September 2026',
    'Périmètre Global actuel — 1er septembre 2026',
]:
    if bad in text:
        raise SystemExit(f'Obsolete live-scope text remains: {bad}')

for cid in second_classes:
    if re.search(rf'\{{ id: "{re.escape(cid)}"[^\n]*releaseStatus: "coming-soon"', text):
        raise SystemExit(f'{cid} is still marked coming-soon')

# Avoid accidental destructive rewrite.
if len(text) < len(original) * 0.90:
    raise SystemExit('Patched file unexpectedly shrank by more than 10%')
if text == original:
    raise SystemExit('No changes were produced')

PATH.write_text(text, encoding='utf-8')
print(f'Patched index.html: {len(original)} -> {len(text)} bytes')
for label, count in changes:
    print(f'- {label}: {count}')
