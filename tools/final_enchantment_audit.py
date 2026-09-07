from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
a = s.index('  function enchantmentPage(topic) {')
b = s.index('\n  function ', a + 10)
f = s[a:b]

# Remove editorial/workflow explanations from the visible guide.
start = f.index('            <div class="essence-reading-key">')
end = f.index('            <h3 id="md-base-essence">1st Job Essence</h3>', start)
f = f[:start] + f[end:]

# Keep each temporary Essence effect short and self-contained while preserving
# any class condition, trigger, effect and duration that matter to gameplay.
replacements = {
    'When equipped by Thief Class, using Steal grants ATK +30 for 60 seconds.': 'Thief Class — Steal: ATK +30 for 60 seconds.',
    'Équipé par Thief Class, utiliser Steal donne ATK +30 pendant 60 secondes.': 'Thief Class — Steal : ATK +30 pendant 60 secondes.',
    'When equipped by Swordsman Class, using Two-Hand Quicken grants Critical Damage +7% for 60 seconds.': 'Swordsman Class — Two-Hand Quicken: Critical Damage +7% for 60 seconds.',
    'Équipé par Swordsman Class, utiliser Two-Hand Quicken donne Critical Damage +7 % pendant 60 secondes.': 'Swordsman Class — Two-Hand Quicken : Critical Damage +7 % pendant 60 secondes.',
    'Using Pierce increases Brandish Spear damage by 40% for 60 seconds.': 'Pierce: Brandish Spear damage +40% for 60 seconds.',
    'Utiliser Pierce augmente les dégâts de Brandish Spear de 40 % pendant 60 secondes.': 'Pierce : dégâts de Brandish Spear +40 % pendant 60 secondes.',
    'When equipped by Merchant Class, using Weapon Perfection grants CRIT +10 for 60 seconds.': 'Merchant Class — Weapon Perfection: CRIT +10 for 60 seconds.',
    'Équipé par Merchant Class, utiliser Weapon Perfection donne CRIT +10 pendant 60 secondes.': 'Merchant Class — Weapon Perfection : CRIT +10 pendant 60 secondes.',
    'Using Adrenaline Rush grants an additional DEX +10 and LUK +10 for 60 seconds.': 'Adrenaline Rush: DEX +10 and LUK +10 for 60 seconds.',
    'Utiliser Adrenaline Rush donne en plus DEX +10 et LUK +10 pendant 60 secondes.': 'Adrenaline Rush : DEX +10 et LUK +10 pendant 60 secondes.',
    'When equipped by Thief Class, using Sonic Blow grants After Attack Delay -7% for 60 seconds.': 'Thief Class — Sonic Blow: After Attack Delay -7% for 60 seconds.',
    'Équipé par Thief Class, utiliser Sonic Blow donne After Attack Delay -7 % pendant 60 secondes.': 'Thief Class — Sonic Blow : After Attack Delay -7 % pendant 60 secondes.',
    'Using Cloaking grants an additional Venom Splasher damage +20% for 60 seconds (40% total during the effect).': 'Cloaking: Venom Splasher damage +20% for 60 seconds (40% total).',
    'Utiliser Cloaking donne +20 % de dégâts supplémentaires à Venom Splasher pendant 60 secondes (40 % au total pendant l’effet).': 'Cloaking : dégâts de Venom Splasher +20 % pendant 60 secondes (40 % au total).',
    'When equipped by Mage Class, using Quagmire grants FLEE +30 for 60 seconds.': 'Mage Class — Quagmire: FLEE +30 for 60 seconds.',
    'Équipé par Mage Class, utiliser Quagmire donne FLEE +30 pendant 60 secondes.': 'Mage Class — Quagmire : FLEE +30 pendant 60 secondes.',
    'Using Frost Nova grants an additional Jupitel Thunder damage +20% for 60 seconds (40% total during the effect).': 'Frost Nova: Jupitel Thunder damage +20% for 60 seconds (40% total).',
    'Utiliser Frost Nova donne +20 % de dégâts supplémentaires à Jupitel Thunder pendant 60 secondes (40 % au total pendant l’effet).': 'Frost Nova : dégâts de Jupitel Thunder +20 % pendant 60 secondes (40 % au total).',
    'When equipped by Acolyte Class, using Gloria grants MATK +7% and Heal Amount +15% for 60 seconds.': 'Acolyte Class — Gloria: MATK +7% and Heal Amount +15% for 60 seconds.',
    'Équipé par Acolyte Class, utiliser Gloria donne MATK +7 % et Heal Amount +15 % pendant 60 secondes.': 'Acolyte Class — Gloria : MATK +7 % et Heal Amount +15 % pendant 60 secondes.',
    'When equipped by Acolyte Class, after using Status Recovery, normal melee attacks have a high chance to trigger Bash Lv.10 for 60 seconds.': 'Acolyte Class — Status Recovery: normal melee attacks have a high chance to trigger Bash Lv.10 for 60 seconds.',
    'Équipé par Acolyte Class, après avoir utilisé Status Recovery, les attaques normales au corps-à-corps ont une forte chance de déclencher Bash Lv.10 pendant 60 secondes.': 'Acolyte Class — Status Recovery : les attaques normales au corps-à-corps ont une forte chance de déclencher Bash Lv.10 pendant 60 secondes.',
    'Using Improve Concentration grants an additional Blitz Beat damage +40% for 60 seconds (80% total during the effect).': 'Improve Concentration: Blitz Beat damage +40% for 60 seconds (80% total).',
    'Utiliser Improve Concentration donne +40 % de dégâts supplémentaires à Blitz Beat pendant 60 secondes (80 % au total pendant l’effet).': 'Improve Concentration : dégâts de Blitz Beat +40 % pendant 60 secondes (80 % au total).',
    'Using Detect grants an additional Double Strafe damage +20% for 60 seconds (40% total during the effect).': 'Detect: Double Strafe damage +20% for 60 seconds (40% total).',
    'Utiliser Detect donne +20 % de dégâts supplémentaires à Double Strafe pendant 60 secondes (40 % au total pendant l’effet).': 'Detect : dégâts de Double Strafe +20 % pendant 60 secondes (40 % au total).',
    'When equipped by Swordsman Class, using Auto Guard grants DEF +80 for 60 seconds.': 'Swordsman Class — Auto Guard: DEF +80 for 60 seconds.',
    'Équipé par Swordsman Class, utiliser Auto Guard donne DEF +80 pendant 60 secondes.': 'Swordsman Class — Auto Guard : DEF +80 pendant 60 secondes.',
    'Using Endure increases Heal Received by 15% for 60 seconds.': 'Endure: Heal Received +15% for 60 seconds.',
    'Utiliser Endure augmente Heal Received de 15 % pendant 60 secondes.': 'Endure : Heal Received +15 % pendant 60 secondes.',
    'When equipped by Merchant Class, after using Potion Pitcher, normal melee attacks have a high chance to trigger Bash Lv.10 for 60 seconds.': 'Merchant Class — Potion Pitcher: normal melee attacks have a high chance to trigger Bash Lv.10 for 60 seconds.',
    'Équipé par Merchant Class, après avoir utilisé Potion Pitcher, les attaques normales au corps-à-corps ont une forte chance de déclencher Bash Lv.10 pendant 60 secondes.': 'Merchant Class — Potion Pitcher : les attaques normales au corps-à-corps ont une forte chance de déclencher Bash Lv.10 pendant 60 secondes.',
    'Using Hide reduces Sightless Mind SP cost by 15% for 60 seconds.': 'Hide: Sightless Mind SP cost -15% for 60 seconds.',
    'Utiliser Hide réduit le coût en SP de Sightless Mind de 15 % pendant 60 secondes.': 'Hide : coût en SP de Sightless Mind -15 % pendant 60 secondes.',
    'Using Envenom grants an additional Back Stab damage +20% for 60 seconds (40% total during the effect).': 'Envenom: Back Stab damage +20% for 60 seconds (40% total).',
    'Utiliser Envenom donne +20 % de dégâts supplémentaires à Back Stab pendant 60 secondes (40 % au total pendant l’effet).': 'Envenom : dégâts de Back Stab +20 % pendant 60 secondes (40 % au total).',
    'After using Earth Spike, Fire Bolt, Cold Bolt and Lightning Bolt gain an additional damage +20% for 60 seconds (40% total during the effect).': 'Earth Spike: Fire Bolt, Cold Bolt and Lightning Bolt damage +20% for 60 seconds (40% total).',
    'Après avoir utilisé Earth Spike, Fire Bolt, Cold Bolt et Lightning Bolt gagnent +20 % de dégâts supplémentaires pendant 60 secondes (40 % au total pendant l’effet).': 'Earth Spike : dégâts de Fire Bolt, Cold Bolt et Lightning Bolt +20 % pendant 60 secondes (40 % au total).',
    'When equipped by Acolyte Class, using Explosion Spirits activates a 60-second effect during which normal melee attacks have a high chance to trigger Hindsight and Summon Spirit Sphere.': 'Acolyte Class — Explosion Spirits: normal melee attacks have a high chance to trigger Hindsight and Summon Spirit Sphere for 60 seconds.',
    'Équipé par Acolyte Class, utiliser Explosion Spirits active pendant 60 secondes un effet durant lequel les attaques normales au corps-à-corps ont une forte chance de déclencher Hindsight et Summon Spirit Sphere.': 'Acolyte Class — Explosion Spirits : les attaques normales au corps-à-corps ont une forte chance de déclencher Hindsight et Summon Spirit Sphere pendant 60 secondes.',
    'After using Blessing, for 60 seconds using Occult Impaction has a high chance to trigger Summon Spirit Sphere.': 'Blessing: Occult Impaction has a high chance to trigger Summon Spirit Sphere for 60 seconds.',
    'Après avoir utilisé Blessing, pendant 60 secondes Occult Impaction a une forte chance de déclencher Summon Spirit Sphere.': 'Blessing : Occult Impaction a une forte chance de déclencher Summon Spirit Sphere pendant 60 secondes.',
    'When equipped by Archer Class, using Service For You or A Poem of Bragi grants Natural SP Recovery +50% for 60 seconds.': 'Archer Class — Service For You / A Poem of Bragi: Natural SP Recovery +50% for 60 seconds.',
    'Équipé par Archer Class, utiliser Service For You ou A Poem of Bragi donne Natural SP Recovery +50 % pendant 60 secondes.': 'Archer Class — Service For You / A Poem of Bragi : Natural SP Recovery +50 % pendant 60 secondes.',
    'After using Encore, Melody Strike and Slinging Arrow gain an additional damage +20% for 60 seconds (40% total during the effect).': 'Encore: Melody Strike and Slinging Arrow damage +20% for 60 seconds (40% total).',
    'Après avoir utilisé Encore, Melody Strike et Slinging Arrow gagnent +20 % de dégâts supplémentaires pendant 60 secondes (40 % au total pendant l’effet).': 'Encore : dégâts de Melody Strike et Slinging Arrow +20 % pendant 60 secondes (40 % au total).',
}

for old, new in replacements.items():
    if old in f:
        f = f.replace(old, new)

s = s[:a] + f + s[b:]

# Regression checks: no editorial instructions remain in the visible Enchantment guide.
a = s.index('  function enchantmentPage(topic) {')
b = s.index('\n  function ', a + 10)
g = s[a:b]
for forbidden in [
    'How to read the effects',
    'Comment lire les effets',
    'Trigger → Effect → Duration',
    'Déclencheur → Effet → Durée',
    'A displayed +40% without its trigger/duration would be incomplete',
    'Afficher seulement +40 % sans le déclencheur et la durée serait incomplet'
]:
    assert forbidden not in g, forbidden

for required in [
    'Pierce: Brandish Spear damage +40% for 60 seconds.',
    'Pierce : dégâts de Brandish Spear +40 % pendant 60 secondes.',
    'Swordsman Class — Two-Hand Quicken: Critical Damage +7% for 60 seconds.',
    'Thief Class — Sonic Blow: After Attack Delay -7% for 60 seconds.',
    'Improve Concentration: Blitz Beat damage +40% for 60 seconds (80% total).',
    'Encore: Melody Strike and Slinging Arrow damage +20% for 60 seconds (40% total).'
]:
    assert required in g, required

p.write_text(s, encoding='utf-8')
