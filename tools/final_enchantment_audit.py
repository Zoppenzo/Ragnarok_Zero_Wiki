from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
a=s.index('  function enchantmentPage(topic) {')
b=s.index('\n  function ', a+10)
f=s[a:b]

# Bard & Dancer Essence I: the fixed 60-second cooldown reduction is a separate effect,
# not a cap on the lesson-level reduction.
old1="i1:fx('Amp cooldown is reduced by the Music Lessons / Dance Lessons level, up to 60 seconds.||Every 2 armor refines: Max SP +30.','Le cooldown d’Amp est réduit selon le niveau de Music Lessons / Dance Lessons, jusqu’à 60 secondes.||Tous les 2 raffinages de l’armure : Max SP +30.'),"
new1="i1:fx('Amp cooldown is reduced by 1 second per Music Lessons / Dance Lessons level.||Amp cooldown -60 seconds.||Every 2 armor refines: Max SP +30.','Cooldown d’Amp -1 seconde par niveau de Music Lessons / Dance Lessons.||Cooldown d’Amp -60 secondes.||Tous les 2 raffinages de l’armure : Max SP +30.'),"
assert old1 in f
f=f.replace(old1,new1,1)

old2="i2:fx('Amp cooldown reduction is 3× the Music Lessons / Dance Lessons level, up to 60 seconds.||When equipped by Archer Class, using Service For You or A Poem of Bragi grants Natural SP Recovery +50% for 60 seconds.||Every 2 armor refines: Max SP +30.','La réduction du cooldown d’Amp vaut 3× le niveau de Music Lessons / Dance Lessons, jusqu’à 60 secondes.||Équipé par Archer Class, utiliser Service For You ou A Poem of Bragi donne Natural SP Recovery +50 % pendant 60 secondes.||Tous les 2 raffinages de l’armure : Max SP +30.'),"
new2="i2:fx('Amp cooldown is reduced by 3 seconds per Music Lessons / Dance Lessons level.||Amp cooldown -60 seconds.||When equipped by Archer Class, using Service For You or A Poem of Bragi grants Natural SP Recovery +50% for 60 seconds.||Every 2 armor refines: Max SP +30.','Cooldown d’Amp -3 secondes par niveau de Music Lessons / Dance Lessons.||Cooldown d’Amp -60 secondes.||Équipé par Archer Class, utiliser Service For You ou A Poem of Bragi donne Natural SP Recovery +50 % pendant 60 secondes.||Tous les 2 raffinages de l’armure : Max SP +30.'),"
assert old2 in f
f=f.replace(old2,new2,1)

# The exact current Global zeny reset cost/rate is not available in the live client data.
# Remove the disputed precise zeny-reset row rather than presenting one regional value as Global fact.
old_summary="              [navLabel('Zeny reset','Reset zeny'),`100 000 zeny · ${risk('danger','30% destruction','30 % de destruction')}`],\n              [navLabel('Safe reset','Reset sécurisé'),`${itemLink('Zelstar')} ×1 · ${risk('safe','0% destruction','0 % de destruction')}`],"
if old_summary in f:
    f=f.replace(old_summary,"              [navLabel('Safe reset','Reset sécurisé'),`${itemLink('Zelstar')} ×1 · ${risk('safe','No item destruction','Pas de destruction de l’objet')}`],",1)

old_reset="""                <tr><td>${navLabel('Zeny reset','Reset en zeny')}</td><td>100 000 zeny</td><td>${risk('warn','70% without destruction','70 % sans destruction')}</td><td>${risk('danger','30% destruction','30 % de destruction')}</td></tr>
                <tr><td>${navLabel('Safe reset','Reset sécurisé')}</td><td>${itemLink('Zelstar')} ×1</td><td>${risk('safe','100% reset','100 % de reset')}</td><td>${risk('safe','0%','0 %')}</td></tr>"""
new_reset="""                <tr><td>${navLabel('Zeny reset','Reset en zeny')}</td><td>—</td><td>—</td><td>—</td></tr>
                <tr><td>${navLabel('Safe reset','Reset sécurisé')}</td><td>${itemLink('Zelstar')} ×1</td><td>${navLabel('Removes the current enchant','Retire l’enchantement actuel')}</td><td>${risk('safe','No item destruction','Pas de destruction de l’objet')}</td></tr>"""
assert old_reset in f
f=f.replace(old_reset,new_reset,1)

reset_table_end=new_reset+"\n              </tbody>\n            </table></div>"
assert reset_table_end in f
reset_note="""\n            <div class=\"enchant-detail-note\">${navLabel(
              'The exact zeny-reset cost and success/destruction rate are not displayed until they are confirmed on the current Global server. This avoids mixing a regional or older value into the Global guide.',
              'Le coût exact et le taux de réussite/destruction du reset en zeny ne sont pas affichés tant qu’ils ne sont pas confirmés sur le serveur Global actuel. Cela évite d’intégrer une ancienne valeur ou une valeur d’une autre région dans le guide.'
            )}</div>"""
f=f.replace(reset_table_end,reset_table_end+reset_note,1)

# +9 armor has an expanded HP pool in addition to Job Essence entries.
old_options="""              <tr><th>${navLabel('Stats','Stats')}</th><td>STR +1/+2 · AGI +1/+2 · VIT +1/+2 · INT +1/+2 · DEX +1/+2 · LUK +1/+2</td></tr>
              <tr><th>${navLabel('Utility','Utilitaire')}</th><td>FLEE +3 · CRI +1 · DEF +15 · MDEF +2</td></tr>
              <tr><th>HP</th><td>Max HP +50 · +100 · +200</td></tr>"""
new_options="""              <tr><th>${navLabel('Stats','Stats')}</th><td>STR +1/+2 · AGI +1/+2 · VIT +1/+2 · INT +1/+2 · DEX +1/+2 · LUK +1/+2</td></tr>
              <tr><th>${navLabel('Utility','Utilitaire')}</th><td>FLEE +3 · CRI +1 · DEF +15 · MDEF +2</td></tr>
              <tr><th>${navLabel('Standard HP pool','Pool HP standard')}</th><td>Max HP +50 · +100 · +200</td></tr>
              <tr><th>${navLabel('+9 armor HP additions','Ajouts HP sur armure +9')}</th><td>Max HP +300 · +400</td></tr>"""
assert old_options in f
f=f.replace(old_options,new_options,1)

# Audit notice: make the scope explicit and prevent future flattening of temporary effects.
anchor='            <div class="essence-reading-key"><strong>${navLabel(\'How to read the effects\',\'Comment lire les effets\')}:''
assert anchor in f
# Existing reading key is already good; append a short completeness note after its block.
key_end="            )}</div>\n\n            <h3 id=\"md-base-essence\">1st Job Essence</h3>"
assert key_end in f
extra="""            )}</div>
            <div class=\"enchant-detail-note\">${navLabel(
              'Temporary Essence effects are written as Trigger → Effect → Duration. For example: Pierce → Brandish Spear damage +40% → 60 seconds. A displayed +40% without its trigger/duration would be incomplete.',
              'Les effets temporaires des Essences sont écrits sous la forme Déclencheur → Effet → Durée. Exemple : Pierce → dégâts de Brandish Spear +40 % → 60 secondes. Afficher seulement +40 % sans le déclencheur et la durée serait incomplet.'
            )}</div>

            <h3 id=\"md-base-essence\">1st Job Essence</h3>"""
f=f.replace(key_end,extra,1)

s=s[:a]+f+s[b:]

# Regression checks for the final audit.
a=s.index('  function enchantmentPage(topic) {')
b=s.index('\n  function ', a+10)
g=s[a:b]
for x in [
    'Using Pierce increases Brandish Spear damage by 40% for 60 seconds.',
    'Amp cooldown -60 seconds.',
    'Amp cooldown is reduced by 3 seconds per Music Lessons / Dance Lessons level.',
    'Max HP +300 · +400',
    'Le coût exact et le taux de réussite/destruction du reset en zeny ne sont pas affichés',
    'Trigger → Effect → Duration'
]: assert x in g, x
for x in ['up to 60 seconds','100 000 zeny</td><td>${risk(\'warn\'','30% destruction']:
    assert x not in g, x

# Provenance names remain in Sources only.
body=g.split('${officialSources([',1)[0]
for site in ['Criatura','MidgardHub','iRO Wiki','TWRo','KRO']:
    assert site not in body, site

p.write_text(s,encoding='utf-8')
