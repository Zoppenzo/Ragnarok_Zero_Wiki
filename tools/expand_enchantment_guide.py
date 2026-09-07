from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

css_anchor = '/* Click-to-copy /navi commands */'
assert css_anchor in s
if '.enchant-guide-facts {' not in s:
    css = r'''
/* Detailed enchantment guide blocks */
.enchant-guide-facts {
  margin: 12px 0 18px;
  border: 1px solid var(--line);
  background: #fff;
}
.enchant-guide-facts .panel-heading {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 17px;
  font-weight: 400;
  background: #eaf3ff;
}
.enchant-guide-facts table { margin: 0; }
.enchant-guide-facts th { width: 190px; background: #f8f9fa; }
.enchant-risk {
  display: inline-block;
  padding: 1px 6px;
  border: 1px solid var(--line-soft);
  border-radius: 2px;
  font-size: 12px;
  font-weight: 700;
}
.enchant-risk.safe { border-color: var(--green-line); background: var(--green-pale); }
.enchant-risk.warn { border-color: var(--gold-line); background: var(--gold-pale); }
.enchant-risk.danger { border-color: var(--red-line); background: var(--red-pale); }
.enchant-steps {
  margin: 10px 0 18px 22px;
  padding-left: 12px;
}
.enchant-steps li { margin: 7px 0; padding-left: 4px; }
.enchant-subnav {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  margin: 9px 0 17px;
  padding: 8px 9px;
  border: 1px solid var(--line-soft);
  background: #f8f9fa;
}
.enchant-subnav a {
  padding: 3px 7px;
  border: 1px solid #c8ccd1;
  background: #fff;
  font-size: 12px;
}
.enchant-detail-note {
  margin: 12px 0 16px;
  padding: 9px 11px;
  border-left: 4px solid #8daac9;
  background: #f1f7fd;
  line-height: 1.5;
}
.enchant-rate-table td:last-child,
.enchant-rate-table th:last-child { white-space: nowrap; }
.essence-effect { min-width: 225px; line-height: 1.42; }
@media (max-width: 760px) {
  .enchant-guide-facts th { width: 130px; }
  .essence-effect { min-width: 190px; }
}

'''
    s = s.replace(css_anchor, css + css_anchor, 1)

start = s.index('  function enchantmentPage(topic) {')
end = s.index('\n  function ', start + 10)

new_func = r'''  function enchantmentPage(topic) {
    const title = navLabel('Enchantment','Enchantement');
    const itemLink = name => memorialDbLink('items', name);
    const fx = (en,fr) => navLabel(en,fr);
    const risk = (kind,en,fr) => `<span class="enchant-risk ${kind}">${navLabel(en,fr)}</span>`;
    const facts = rows => `<div class="enchant-guide-facts panel"><div class="panel-heading">${navLabel('System summary','Résumé du système')}</div><div class="table-wrap"><table><tbody>${rows.map(r=>`<tr><th>${r[0]}</th><td>${r[1]}</td></tr>`).join('')}</tbody></table></div></div>`;
    const steps = rows => `<ol class="enchant-steps">${rows.map(x=>`<li>${x}</li>`).join('')}</ol>`;
    const subnav = rows => `<div class="enchant-subnav">${rows.map(r=>`<a href="#${r[0]}">${r[1]}</a>`).join('')}</div>`;
    const stoneList = names => names.map(itemLink).join(' · ');
    const statStones = slot => ['STR','INT','AGI','DEX','VIT','LUK'].map(x=>`${x} Stone (${slot})`);
    const conversionStones = slot => ['STR','INT','AGI','DEX','VIT','LUK'].map(x=>`${x} Conversion Stone (${slot})`);
    const poringOptions = ['STR +1','VIT +1','INT +1','DEX +1','AGI +1','LUK +1','SP +10','SP +25','SP +50','HP +100','HP +200'];

    const baseRates = [
      ['FLEE +3','6.03%'],['CRI +1','6.03%'],['DEF +15','5.17%'],['MDEF +2','5.17%'],
      ['Max HP +50','6.18%'],['Max HP +100','4.31%'],['Max HP +200','3.45%'],
      ['AGI +1','10.52%'],['AGI +2','0.09%'],['DEX +1','10.52%'],['DEX +2','0.09%'],
      ['STR +1','10.52%'],['STR +2','0.09%'],['INT +1','10.52%'],['INT +2','0.09%'],
      ['VIT +1','10.52%'],['VIT +2','0.09%'],['LUK +1','10.52%'],['LUK +2','0.09%']
    ];
    const plus9Rates = [
      ['FLEE +3','3.48%','4.90%'],['CRI +1','3.48%','4.90%'],['DEF +15','3.48%','4.90%'],['MDEF +2','3.48%','4.90%'],
      ['Max HP +50','10.70%','4.90%'],['Max HP +100','8.91%','3.50%'],['Max HP +200','7.58%','2.60%'],['Max HP +300','6.31%','1.70%'],['Max HP +400','4.46%','0.80%'],
      ['AGI +1','7.13%','7.58%'],['AGI +2','0.89%','3.57%'],['DEX +1','7.13%','7.58%'],['DEX +2','0.89%','3.57%'],
      ['STR +1','7.13%','7.58%'],['STR +2','0.89%','3.57%'],['INT +1','7.13%','7.58%'],['INT +2','0.89%','3.57%'],
      ['VIT +1','7.13%','7.58%'],['VIT +2','0.89%','3.57%'],['LUK +1','7.13%','7.58%'],['LUK +2','0.89%','3.57%']
    ];

    const firstEssences = [
      {job:'Mage', lv1:fx('Cold Bolt, Fire Bolt and Lightning Bolt damage +20%. Every 2 Fire Wall levels: Variable Cast Time -1%.','Dégâts de Cold Bolt, Fire Bolt et Lightning Bolt +20 %. Tous les 2 niveaux de Fire Wall : Variable Cast Time -1 %.'), lv2:fx('Cold Bolt, Fire Bolt and Lightning Bolt damage +20%. Every Fire Wall level: Variable Cast Time -1%. Every 2 armor refines: Max SP +50.','Dégâts de Cold Bolt, Fire Bolt et Lightning Bolt +20 %. Par niveau de Fire Wall : Variable Cast Time -1 %. Tous les 2 raffinages de l’armure : Max SP +50.')},
      {job:'Acolyte', lv1:fx('Heal, Increase Agility and Blessing SP cost -15%. Every 2 Heal levels: healing +1%.','Coût en SP de Heal, Increase Agility et Blessing -15 %. Tous les 2 niveaux de Heal : soins +1 %.'), lv2:fx('Heal, Increase Agility and Blessing SP cost -15%. Every Heal level: healing +1%. Every 2 armor refines: Max HP +70 and Max SP +30.','Coût en SP de Heal, Increase Agility et Blessing -15 %. Par niveau de Heal : soins +1 %. Tous les 2 raffinages : Max HP +70 et Max SP +30.')},
      {job:'Archer', lv1:fx('Double Strafe SP cost -5. Every Vulture’s Eye level: Bow damage +1%.','Coût en SP de Double Strafe -5. Par niveau de Vulture’s Eye : dégâts à l’arc +1 %.'), lv2:fx('Double Strafe SP cost -5. Every Vulture’s Eye level: Bow damage +2%. Every 2 armor refines: Arrow Shower damage +5%.','Coût en SP de Double Strafe -5. Par niveau de Vulture’s Eye : dégâts à l’arc +2 %. Tous les 2 raffinages : dégâts d’Arrow Shower +5 %.')},
      {job:'Swordsman', lv1:fx('Magnum Break SP cost -10. Every 2 Bash levels: After Attack Delay -1%.','Coût en SP de Magnum Break -10. Tous les 2 niveaux de Bash : After Attack Delay -1 %.'), lv2:fx('Magnum Break SP cost -10. Every Bash level: After Attack Delay -1%. Every 2 armor refines: Magnum Break damage +15%.','Coût en SP de Magnum Break -10. Par niveau de Bash : After Attack Delay -1 %. Tous les 2 raffinages : dégâts de Magnum Break +15 %.')},
      {job:'Thief', lv1:fx('ATK +30 through the Thief essence effect. Every 2 Steal levels: After Attack Delay -1%.','ATK +30 via l’effet de l’Essence Thief. Tous les 2 niveaux de Steal : After Attack Delay -1 %.'), lv2:fx('ATK +30. Every Steal level: After Attack Delay -1%. Every 2 armor refines: FLEE +10.','ATK +30. Par niveau de Steal : After Attack Delay -1 %. Tous les 2 raffinages : FLEE +10.')},
      {job:'Merchant', lv1:fx('ATK +2 per Discount level. Every 2 Overcharge levels: After Attack Delay -1%.','ATK +2 par niveau de Discount. Tous les 2 niveaux d’Overcharge : After Attack Delay -1 %.'), lv2:fx('ATK +2 per Discount level. Every Overcharge level: After Attack Delay -1%. Every 2 armor refines: Max HP +100.','ATK +2 par niveau de Discount. Par niveau d’Overcharge : After Attack Delay -1 %. Tous les 2 raffinages : Max HP +100.')}
    ];

    const secondEssences = [
      {job:'Knight', i1:fx('CRI +3 per Cavalry Mastery level; Bowling Bash damage +20%; After Attack Delay -1% per armor refine.','CRI +3 par niveau de Cavalry Mastery ; dégâts de Bowling Bash +20 % ; After Attack Delay -1 % par raffinage.'), i2:fx('CRI +5 per Cavalry Mastery level; Bowling Bash damage +20%; Critical Damage +7%; After Attack Delay -1% per armor refine.','CRI +5 par niveau de Cavalry Mastery ; dégâts de Bowling Bash +20 % ; dégâts critiques +7 % ; After Attack Delay -1 % par raffinage.'), ii1:fx('HIT +1 per Spear Mastery level; Pierce damage +20%; ATK +2 per armor refine.','HIT +1 par niveau de Spear Mastery ; dégâts de Pierce +20 % ; ATK +2 par raffinage.'), ii2:fx('HIT +2 per Spear Mastery level; Pierce damage +20%; Brandish Spear damage +40%; ATK +2 per armor refine.','HIT +2 par niveau de Spear Mastery ; dégâts de Pierce +20 % ; dégâts de Brandish Spear +40 % ; ATK +2 par raffinage.')},
      {job:'Blacksmith', i1:fx('CRI +10; CRI scales with Maximize Power; After Attack Delay -1% per armor refine.','CRI +10 ; CRI augmente avec Maximize Power ; After Attack Delay -1 % par raffinage.'), i2:fx('CRI +10; CRI +5 per Maximize Power level; Critical Damage +1% per Weaponry Research level; After Attack Delay -1% per refine.','CRI +10 ; CRI +5 par niveau de Maximize Power ; dégâts critiques +1 % par niveau de Weaponry Research ; After Attack Delay -1 % par raffinage.'), ii1:fx('LUK +1 per Skin Tempering level; DEX +10; every 2 armor refines: LUK +1.','LUK +1 par niveau de Skin Tempering ; DEX +10 ; tous les 2 raffinages : LUK +1.'), ii2:fx('LUK +2 per Skin Tempering level; DEX +10; additional DEX/LUK bonus through the Merchant-class effect; every 2 refines: LUK +1.','LUK +2 par niveau de Skin Tempering ; DEX +10 ; bonus DEX/LUK supplémentaire via l’effet Merchant ; tous les 2 raffinages : LUK +1.')},
      {job:'Assassin', i1:fx('CRI +3 per Grimtooth level; Sonic Blow damage +20%; Critical Damage +1% per armor refine.','CRI +3 par niveau de Grimtooth ; dégâts de Sonic Blow +20 % ; dégâts critiques +1 % par raffinage.'), i2:fx('CRI +5 per Grimtooth level; Sonic Blow damage +20%; After Attack Delay -7% through the Thief-class effect; Critical Damage +1% per refine.','CRI +5 par niveau de Grimtooth ; dégâts de Sonic Blow +20 % ; After Attack Delay -7 % via l’effet Thief ; dégâts critiques +1 % par raffinage.'), ii1:fx('FLEE +3 per Left Hand Mastery level; Venom Splasher damage +20%; every 2 armor refines: Variable Cast Time -3%.','FLEE +3 par niveau de Left Hand Mastery ; dégâts de Venom Splasher +20 % ; tous les 2 raffinages : Variable Cast Time -3 %.'), ii2:fx('FLEE +5 per Left Hand Mastery level; Venom Splasher damage +40%; every 2 armor refines: Variable Cast Time -3%.','FLEE +5 par niveau de Left Hand Mastery ; dégâts de Venom Splasher +40 % ; tous les 2 raffinages : Variable Cast Time -3 %.')},
      {job:'Wizard', i1:fx('Variable Cast Time reduction scales with Heaven’s Drive; Meteor Storm, Lord of Vermilion and Storm Gust damage +20%; MATK +1% every 2 refines.','Réduction de Variable Cast Time selon Heaven’s Drive ; dégâts de Meteor Storm, Lord of Vermilion et Storm Gust +20 % ; MATK +1 % tous les 2 raffinages.'), i2:fx('Stronger Heaven’s Drive cast reduction; the three major AoEs +20%; FLEE +30 through the Mage-class effect; MATK +1% every 2 refines.','Réduction de cast renforcée via Heaven’s Drive ; les trois AoE principales +20 % ; FLEE +30 via l’effet Mage ; MATK +1 % tous les 2 raffinages.'), ii1:fx('Variable Cast Time reduction scales with Lord of Vermilion; Jupitel Thunder damage +20%; MATK +2 per armor refine.','Réduction de Variable Cast Time selon Lord of Vermilion ; dégâts de Jupitel Thunder +20 % ; MATK +2 par raffinage.'), ii2:fx('Stronger Lord of Vermilion cast reduction; Jupitel Thunder damage +40%; MATK +2 per armor refine.','Réduction de cast renforcée via Lord of Vermilion ; dégâts de Jupitel Thunder +40 % ; MATK +2 par raffinage.')},
      {job:'Priest', i1:fx('Variable Cast Time reduction scales with Magnificat; Magnus Exorcismus damage +20%; every 2 refines: Magnus Exorcismus damage +5%.','Réduction de Variable Cast Time selon Magnificat ; dégâts de Magnus Exorcismus +20 % ; tous les 2 raffinages : dégâts de Magnus Exorcismus +5 %.'), i2:fx('Stronger Magnificat cast reduction; Magnus Exorcismus damage +20%; MATK +7% and healing +15% through the Acolyte-class effect; refine scaling remains.','Réduction de cast renforcée via Magnificat ; dégâts de Magnus Exorcismus +20 % ; MATK +7 % et soins +15 % via l’effet Acolyte ; bonus de raffinage conservé.'), ii1:fx('ATK +3 per Mace Mastery level; Critical Damage +15%; ATK +2 per armor refine.','ATK +3 par niveau de Mace Mastery ; dégâts critiques +15 % ; ATK +2 par raffinage.'), ii2:fx('ATK +5 per Mace Mastery level; Critical Damage +15%; melee attacks can trigger Bash Lv.10 through the Acolyte-class effect; ATK +2 per refine.','ATK +5 par niveau de Mace Mastery ; dégâts critiques +15 % ; les attaques mêlée peuvent déclencher Bash Lv.10 via l’effet Acolyte ; ATK +2 par raffinage.')},
      {job:'Hunter', i1:fx('After Attack Delay improves with Blitz Beat; Blitz Beat damage +40%; LUK +1 per armor refine.','After Attack Delay s’améliore avec Blitz Beat ; dégâts de Blitz Beat +40 % ; LUK +1 par raffinage.'), i2:fx('Stronger Blitz Beat scaling; Blitz Beat damage up to +80%; LUK +1 per armor refine.','Scaling Blitz Beat renforcé ; dégâts de Blitz Beat jusqu’à +80 % ; LUK +1 par raffinage.'), ii1:fx('ATK +3 per Beast Bane level; Double Strafe damage +20%; every 2 refines: ranged physical damage +3%.','ATK +3 par niveau de Beast Bane ; dégâts de Double Strafe +20 % ; tous les 2 raffinages : dégâts physiques à distance +3 %.'), ii2:fx('ATK +5 per Beast Bane level; Double Strafe damage +40%; every 2 refines: ranged physical damage +3%.','ATK +5 par niveau de Beast Bane ; dégâts de Double Strafe +40 % ; tous les 2 raffinages : dégâts physiques à distance +3 %.')},
      {job:'Crusader', i1:fx('ATK +3 per Faith level; Holy Cross damage +15%; every 2 refines: Max HP +100.','ATK +3 par niveau de Faith ; dégâts de Holy Cross +15 % ; tous les 2 raffinages : Max HP +100.'), i2:fx('ATK +5 per Faith level; Holy Cross damage +15%; DEF +80 through the Swordsman-class effect; every 2 refines: Max HP +100.','ATK +5 par niveau de Faith ; dégâts de Holy Cross +15 % ; DEF +80 via l’effet Swordsman ; tous les 2 raffinages : Max HP +100.'), ii1:fx('MATK +3 per Faith level; Grand Cross damage +20%; MATK +2 per armor refine.','MATK +3 par niveau de Faith ; dégâts de Grand Cross +20 % ; MATK +2 par raffinage.'), ii2:fx('MATK +5 per Faith level; Grand Cross damage +20%; healing received +15% through the Swordsman-class effect; MATK +2 per refine.','MATK +5 par niveau de Faith ; dégâts de Grand Cross +20 % ; soins reçus +15 % via l’effet Swordsman ; MATK +2 par raffinage.')},
      {job:'Alchemist', i1:fx('ATK +3 per Potion Research level; After Attack Delay -10%; every 2 refines: CRI +5.','ATK +3 par niveau de Potion Research ; After Attack Delay -10 % ; tous les 2 raffinages : CRI +5.'), i2:fx('ATK +5 per Potion Research level; After Attack Delay -10%; Merchant-class stat bonus; every 2 refines: CRI +5.','ATK +5 par niveau de Potion Research ; After Attack Delay -10 % ; bonus de stats via l’effet Merchant ; tous les 2 raffinages : CRI +5.'), ii1:fx('ATK +3 per Prepare Potion level; Mammonite damage +100%; ATK +2 per armor refine.','ATK +3 par niveau de Prepare Potion ; dégâts de Mammonite +100 % ; ATK +2 par raffinage.'), ii2:fx('ATK +5 per Prepare Potion level; Mammonite damage +100%; melee attacks can trigger Bash Lv.10 through the Merchant-class effect; ATK +2 per refine.','ATK +5 par niveau de Prepare Potion ; dégâts de Mammonite +100 % ; les attaques mêlée peuvent déclencher Bash Lv.10 via l’effet Merchant ; ATK +2 par raffinage.')},
      {job:'Rogue', i1:fx('ATK +3 per Plagiarism level; Sightless Mind damage +20%; After Attack Delay -1% per armor refine.','ATK +3 par niveau de Plagiarism ; dégâts de Sightless Mind +20 % ; After Attack Delay -1 % par raffinage.'), i2:fx('ATK +5 per Plagiarism level; Sightless Mind damage +20%; Sightless Mind SP cost -15%; After Attack Delay -1% per refine.','ATK +5 par niveau de Plagiarism ; dégâts de Sightless Mind +20 % ; coût SP de Sightless Mind -15 % ; After Attack Delay -1 % par raffinage.'), ii1:fx('HIT +1 per Gank level; Back Stab damage +20%; ATK +2 per armor refine.','HIT +1 par niveau de Gank ; dégâts de Back Stab +20 % ; ATK +2 par raffinage.'), ii2:fx('HIT +2 per Gank level; Back Stab damage +40%; ATK +2 per armor refine.','HIT +2 par niveau de Gank ; dégâts de Back Stab +40 % ; ATK +2 par raffinage.')},
      {job:'Sage', i1:fx('MATK +3 per Hindsight level; Earth Spike and Heaven’s Drive damage +20%; After Attack Delay -1% per armor refine.','MATK +3 par niveau de Hindsight ; dégâts d’Earth Spike et Heaven’s Drive +20 % ; After Attack Delay -1 % par raffinage.'), i2:fx('MATK +5 per Hindsight level; Earth Spike and Heaven’s Drive damage +20%; ASPD +1 and Earth magic bonus; refine scaling remains.','MATK +5 par niveau de Hindsight ; dégâts d’Earth Spike et Heaven’s Drive +20 % ; ASPD +1 et bonus magie Terre ; scaling de raffinage conservé.'), ii1:fx('MATK +3 per Study level; Fire Bolt, Cold Bolt and Lightning Bolt damage +20%; MATK +2 per armor refine.','MATK +3 par niveau de Study ; dégâts de Fire Bolt, Cold Bolt et Lightning Bolt +20 % ; MATK +2 par raffinage.'), ii2:fx('MATK +5 per Study level; Fire Bolt, Cold Bolt and Lightning Bolt damage +40%; MATK +2 per armor refine.','MATK +5 par niveau de Study ; dégâts de Fire Bolt, Cold Bolt et Lightning Bolt +40 % ; MATK +2 par raffinage.')},
      {job:'Monk', i1:fx('ATK +3 per Demon Bane level; Raging Quadruple Blow damage +20%; every 2 refines: Raging Thrust damage +5%.','ATK +3 par niveau de Demon Bane ; dégâts de Raging Quadruple Blow +20 % ; tous les 2 raffinages : dégâts de Raging Thrust +5 %.'), i2:fx('ATK +5 per Demon Bane level; Raging Quadruple Blow damage +20%; spirit-sphere proc effect; refine scaling remains.','ATK +5 par niveau de Demon Bane ; dégâts de Raging Quadruple Blow +20 % ; effet de proc des Spirit Spheres ; scaling de raffinage conservé.'), ii1:fx('Occult Impaction cast time reduction scales with Demon Bane; Occult Impaction damage +20%; every 2 refines: additional damage +5%.','Réduction du cast d’Occult Impaction selon Demon Bane ; dégâts d’Occult Impaction +20 % ; tous les 2 raffinages : dégâts supplémentaires +5 %.'), ii2:fx('Stronger Occult Impaction cast reduction; damage +20%; using it can trigger Summon Spirit Sphere; every 2 refines: additional damage +5%.','Réduction du cast d’Occult Impaction renforcée ; dégâts +20 % ; son utilisation peut déclencher Summon Spirit Sphere ; tous les 2 raffinages : dégâts supplémentaires +5 %.')},
      {job:'Bard & Dancer', i1:fx('Amp cooldown reduction scales with Music Lessons / Dance Lessons; every 2 armor refines: Max SP +30.','Réduction du cooldown d’Amp selon Music Lessons / Dance Lessons ; tous les 2 raffinages : Max SP +30.'), i2:fx('Stronger Amp cooldown reduction; natural SP recovery +50% through the Archer-class effect; every 2 refines: Max SP +30.','Réduction du cooldown d’Amp renforcée ; récupération naturelle de SP +50 % via l’effet Archer ; tous les 2 raffinages : Max SP +30.'), ii1:fx('ATK +3 per Music Lessons / Dance Lessons level; Melody Strike / Slinging Arrow damage +20%; every 2 refines: ranged physical damage +1%.','ATK +3 par niveau de Music Lessons / Dance Lessons ; dégâts de Melody Strike / Slinging Arrow +20 % ; tous les 2 raffinages : dégâts physiques à distance +1 %.'), ii2:fx('ATK +5 per Music Lessons / Dance Lessons level; Melody Strike / Slinging Arrow damage +40%; every 2 refines: ranged physical damage +1%.','ATK +5 par niveau de Music Lessons / Dance Lessons ; dégâts de Melody Strike / Slinging Arrow +40 % ; tous les 2 raffinages : dégâts physiques à distance +1 %.')}
    ];

    return `${breadcrumbs([{label:title}])}
      <div class="article-heading"><h1>${icon('item')}${title}</h1><div class="page-subtitle">${t('fromWiki')}</div></div>
      <p class="article-lead">${navLabel(
        'This page is a full guide to the different enchantment systems: requirements, NPCs, costs, success and failure rules, item destruction, reset methods, slots and possible results. Random drop Affixes remain a separate mechanic.',
        'Cette page est un guide complet des différents systèmes d’enchantement : prérequis, NPC, coûts, réussite et échec, destruction des objets, méthodes de reset, slots et résultats possibles. Les Affixes aléatoires des drops restent une mécanique séparée.'
      )}</p>

      <div class="enchant-tabs">
        <input class="enchant-tab-input" type="radio" name="enchant-tabs" id="enchant-tab-costume" checked>
        <input class="enchant-tab-input" type="radio" name="enchant-tabs" id="enchant-tab-poring">
        <input class="enchant-tab-input" type="radio" name="enchant-tabs" id="enchant-tab-memorial">
        <input class="enchant-tab-input" type="radio" name="enchant-tabs" id="enchant-tab-essences">
        <input class="enchant-tab-input" type="radio" name="enchant-tabs" id="enchant-tab-taming">

        <div class="enchant-tab-labels" role="tablist" aria-label="${esc(navLabel('Enchantment categories','Catégories d’enchantement'))}">
          <label for="enchant-tab-costume">${navLabel('Costumes','Costumes')}</label>
          <label for="enchant-tab-poring">Poring Village</label>
          <label for="enchant-tab-memorial">${navLabel('Memorial Equipment','Équipement mémorial')}</label>
          <label for="enchant-tab-essences">${navLabel('Job Essences','Essences de classe')}</label>
          <label for="enchant-tab-taming">Taming Ring</label>
        </div>

        <div class="enchant-tab-panels">
          <section class="enchant-tab-panel" id="enchant-panel-costume">
            <h2 id="costume">${navLabel('Costume enchantments','Enchantements de costumes')}</h2>
            ${subnav([
              ['costume-requirements',navLabel('Requirements','Prérequis')],['costume-process',navLabel('Procedure','Procédure')],['costume-risk',navLabel('Success / failure','Réussite / échec')],['costume-pool',navLabel('Stone pools','Pools de pierres')]
            ])}
            ${facts([
              [navLabel('NPC / location','NPC / emplacement'),'<code>/navi prontera 263/270</code>'],
              [navLabel('Box price','Prix de la boîte'),'10 000 zeny'],
              [navLabel('Materials','Matériaux'),navLabel('5 unbound Costume (C) items','5 objets Costume (C) non liés')],
              [navLabel('Result','Résultat'),navLabel('1 random costume enchant-stone box, then a random stone from that box','1 boîte aléatoire de pierres de costume, puis une pierre aléatoire dans cette boîte')],
              [navLabel('Application failure','Échec de l’application'),risk('safe','No failure roll indicated','Aucun jet d’échec indiqué')],
              [navLabel('Item destruction','Destruction de l’objet'),risk('safe','No breaking step indicated','Aucune casse indiquée')]
            ])}

            <h3 id="costume-requirements">${navLabel('Requirements and compatibility','Prérequis et compatibilité')}</h3>
            <ul>
              <li>${navLabel('Use costumes marked as Costume (C) material. The current craft box accepts unbound costumes as material.','Utilise des costumes marqués Costume (C). La boîte de fabrication actuelle accepte les costumes non liés comme matériaux.')}</li>
              <li>${navLabel('A stone can only be applied to the costume slot written on the stone: Upper, Middle, Lower or Garment.','Une pierre ne peut être appliquée qu’au slot de costume indiqué sur son nom : Upper, Middle, Lower ou Garment.')}</li>
              <li>${navLabel('The five costumes used in the craft box are consumed by the conversion.','Les cinq costumes placés dans la boîte sont consommés par la conversion.')}</li>
            </ul>

            <h3 id="costume-process">${navLabel('Step-by-step procedure','Procédure étape par étape')}</h3>
            ${steps([
              navLabel('Go to the Costume Enchanter in Prontera.','Va auprès du Costume Enchanter à Prontera.'),
              navLabel('Buy the enchant-stone craft box for 10,000 zeny.','Achète la boîte de fabrication de pierres pour 10 000 zeny.'),
              navLabel('Place 5 compatible, unbound Costume (C) items into the box and confirm the conversion.','Place 5 objets Costume (C) compatibles et non liés dans la boîte puis confirme la conversion.'),
              navLabel('The box gives one random slot box. Open it to obtain one random enchantment stone from that slot pool.','La conversion donne une boîte de slot aléatoire. Ouvre-la pour obtenir une pierre d’enchantement aléatoire du pool correspondant.'),
              navLabel('Use the stone and select a costume matching its slot. The stone is then attached to that costume.','Utilise la pierre puis sélectionne un costume correspondant à son slot. La pierre est alors appliquée sur ce costume.')
            ])}

            <h3 id="costume-risk">${navLabel('Success, failure and item safety','Réussite, échec et sécurité de l’objet')}</h3>
            <div class="table-wrap"><table>
              <thead><tr><th>${navLabel('Step','Étape')}</th><th>${navLabel('Random?','Aléatoire ?')}</th><th>${navLabel('Failure / break','Échec / casse')}</th></tr></thead>
              <tbody>
                <tr><td>${navLabel('Convert 5 costumes','Convertir 5 costumes')}</td><td>${navLabel('Yes — the resulting slot box is random','Oui — la boîte de slot obtenue est aléatoire')}</td><td>${navLabel('No separate failure roll is indicated; the 5 costumes are the conversion cost.','Aucun jet d’échec séparé n’est indiqué ; les 5 costumes constituent le coût de la conversion.')}</td></tr>
                <tr><td>${navLabel('Open the slot box','Ouvrir la boîte de slot')}</td><td>${navLabel('Yes — one stone is selected from its pool','Oui — une pierre est tirée dans son pool')}</td><td>${navLabel('The box is consumed and gives its random result.','La boîte est consommée et donne son résultat aléatoire.')}</td></tr>
                <tr><td>${navLabel('Apply the stone','Appliquer la pierre')}</td><td>${navLabel('No result reroll: the chosen stone defines the effect','Pas de nouveau tirage : la pierre choisie définit l’effet')}</td><td>${risk('safe','No item-destruction mechanic indicated','Aucune mécanique de destruction indiquée')}</td></tr>
              </tbody>
            </table></div>
            <div class="enchant-detail-note">${navLabel('The current Zero flow does not expose a separate success percentage for applying a compatible costume stone. The RNG is documented at the box/result stages, so no extra percentage is invented here.','Le système Zero actuel n’affiche pas de pourcentage de réussite séparé pour l’application d’une pierre compatible. Le hasard intervient lors de la boîte et du résultat obtenu ; aucun pourcentage supplémentaire n’est donc inventé ici.')}</div>

            <h3 id="costume-pool">${navLabel('Current stone pools','Pools de pierres actuels')}</h3>
            <div class="table-wrap"><table>
              <thead><tr><th>${navLabel('Slot','Slot')}</th><th>${navLabel('Possible stones','Pierres possibles')}</th><th>${navLabel('General use','Utilisation générale')}</th></tr></thead>
              <tbody>
                <tr><th>Upper</th><td>${stoneList(statStones('Upper'))}</td><td>${navLabel('Primary stat +1 stones.','Pierres de statistique principale +1.')}</td></tr>
                <tr><th>Middle</th><td>${stoneList([...statStones('Middle'),...conversionStones('Middle')])}</td><td>${navLabel('Primary stat stones and the Middle part of Conversion Stone combinations.','Pierres de stats principales et partie Middle des combinaisons Conversion Stone.')}</td></tr>
                <tr><th>Lower</th><td>${stoneList(['Recovery Stone (Lower)','HIT Stone (Lower)','FLEE Stone (Lower)','HP Stone (Lower)','MSP Stone (Lower)','MDEF Stone (Lower)','ATK Stone (Lower)','MATK Stone (Lower)','Variable Casting Stone (Lower)','Critical Stone (Lower)',...conversionStones('Lower')])}</td><td>${navLabel('Utility/combat effects and the Lower part of Conversion Stone combinations.','Effets utilitaires/combat et partie Lower des combinaisons Conversion Stone.')}</td></tr>
                <tr><th>Garment</th><td>${stoneList(['Double Attack Stone (Garment)','Critical Stone (Garment)','Variable Casting Stone (Garment)'])}</td><td>${navLabel('Major combat effects. Double Attack Stone grants Double Attack Lv.3; Critical Stone grants Critical Damage +20%; Variable Casting Stone reduces Variable Cast Time by 10%.','Effets de combat majeurs. Double Attack Stone donne Double Attack Lv.3 ; Critical Stone donne Critical Damage +20 % ; Variable Casting Stone réduit le Variable Cast Time de 10 %.')}</td></tr>
              </tbody>
            </table></div>
          </section>

          <section class="enchant-tab-panel" id="enchant-panel-poring">
            <h2 id="poring-village">Poring Village</h2>
            ${subnav([
              ['poring-requirements',navLabel('Requirements','Prérequis')],['poring-process',navLabel('Procedure','Procédure')],['poring-risk',navLabel('Success / reset','Réussite / reset')],['poring-options',navLabel('Enchant pool','Pool d’enchantements')]
            ])}
            ${facts([
              [navLabel('NPC / location','NPC / emplacement'),'<code>/navi prt_fild05 174/238</code>'],
              [navLabel('Compatible items','Objets compatibles'),`${itemLink('Poring Village Leek')} · ${itemLink('Poring Village Carrot')}`],
              [navLabel('Enchant cost','Coût enchantement'),`${itemLink('Jellopy')} ×50 + 20 000 zeny`],
              [navLabel('Enchant success','Réussite enchantement'),risk('warn','70% success','70 % de réussite')],
              [navLabel('Enchant failure','Échec enchantement'),risk('warn','30% failure','30 % d’échec')],
              [navLabel('Break on failure','Casse en cas d’échec'),risk('safe','No — item remains intact','Non — l’objet reste intact')],
              [navLabel('Maximum enchants','Nombre maximum'),'1'],
              [navLabel('Reset','Reset'),`${itemLink('Jellopy')} ×50 + 20 000 zeny · ${risk('warn','70% success','70 % de réussite')} · ${risk('safe','No break','Pas de casse')}`]
            ])}

            <h3 id="poring-requirements">${navLabel('Requirements','Prérequis')}</h3>
            <ul>
              <li>${navLabel('You need a Poring Village Leek or Poring Village Carrot.','Il faut posséder un Poring Village Leek ou un Poring Village Carrot.')}</li>
              <li>${navLabel('The headgear must be equipped when using the Veggie Enchanter.','Le headgear doit être équipé lors de l’utilisation du Veggie Enchanter.')}</li>
              <li>${navLabel('You need 50 Jellopy and 20,000 zeny for every enchant attempt.','Chaque tentative d’enchantement demande 50 Jellopy et 20 000 zeny.')}</li>
              <li>${navLabel('Only one enchant can be present on the item at a time.','Un seul enchantement peut être présent sur l’objet à la fois.')}</li>
            </ul>

            <h3 id="poring-process">${navLabel('Enchant procedure','Procédure d’enchantement')}</h3>
            ${steps([
              navLabel('Equip the Leek or Carrot you want to enchant.','Équipe le Leek ou la Carrot que tu veux enchanter.'),
              navLabel('Talk to the Veggie Enchanter at prt_fild05 174/238.','Parle au Veggie Enchanter à prt_fild05 174/238.'),
              navLabel('Choose the enchant option and pay 50 Jellopy + 20,000 zeny.','Choisis l’option d’enchantement et paie 50 Jellopy + 20 000 zeny.'),
              navLabel('The attempt has a 70% success rate. On success, one random effect from the pool is added.','La tentative possède 70 % de réussite. En cas de succès, un effet aléatoire du pool est ajouté.'),
              navLabel('If the attempt fails, the headgear is not destroyed. You can pay the cost again for another attempt.','Si la tentative échoue, le headgear n’est pas détruit. Tu peux repayer le coût pour retenter.')
            ])}

            <h3 id="poring-risk">${navLabel('Reset and failure rules','Règles de reset et d’échec')}</h3>
            <div class="table-wrap"><table>
              <thead><tr><th>${navLabel('Action','Action')}</th><th>${navLabel('Cost','Coût')}</th><th>${navLabel('Success','Réussite')}</th><th>${navLabel('Failure','Échec')}</th><th>${navLabel('Item destroyed?','Objet détruit ?')}</th></tr></thead>
              <tbody>
                <tr><td>${navLabel('Enchant','Enchantement')}</td><td>50 Jellopy + 20 000 zeny</td><td>70%</td><td>30%</td><td>${risk('safe','No','Non')}</td></tr>
                <tr><td>${navLabel('Reset enchant','Reset enchantement')}</td><td>50 Jellopy + 20 000 zeny</td><td>70%</td><td>30%</td><td>${risk('safe','No','Non')}</td></tr>
              </tbody>
            </table></div>

            <h3 id="poring-options">${navLabel('Possible enchantments','Enchantements possibles')}</h3>
            <p>${navLabel('A successful attempt gives one random option from the following pool.','Une tentative réussie donne une option aléatoire parmi le pool suivant.')}</p>
            <div class="table-wrap"><table><thead><tr><th>${navLabel('Type','Type')}</th><th>${navLabel('Possible results','Résultats possibles')}</th></tr></thead><tbody>
              <tr><th>${navLabel('Primary stats','Stats principales')}</th><td>STR +1 · AGI +1 · VIT +1 · INT +1 · DEX +1 · LUK +1</td></tr>
              <tr><th>SP</th><td>SP +10 · SP +25 · SP +50</td></tr>
              <tr><th>HP</th><td>HP +100 · HP +200</td></tr>
            </tbody></table></div>
            <div class="hero-actions"><a class="button" href="#/memorial-dungeons/poring-village">${miniIcon('map')}${navLabel('Open Poring Village guide','Ouvrir le guide Poring Village')}</a></div>
          </section>

          <section class="enchant-tab-panel" id="enchant-panel-memorial">
            <h2 id="memorial-gear">${navLabel('Memorial Dungeon equipment','Équipement des Mémorial Donjons')}</h2>
            ${subnav([
              ['md-requirements',navLabel('Requirements / NPCs','Prérequis / NPC')],['md-process',navLabel('Procedure','Procédure')],['md-risk',navLabel('Enchant / reset risk','Risque enchant / reset')],['md-slots',navLabel('Enchant slots','Slots d’enchantement')],['md-rates',navLabel('Random-option rates','Taux des options')]
            ])}
            ${facts([
              [navLabel('Compatible equipment','Équipement compatible'),navLabel('Memorial Dungeon equipment by rank','Équipement de Mémorial Donjon selon son rang')],
              [navLabel('Standard enchant cost','Coût enchantement standard'),'100 000 zeny'],
              [navLabel('Enchant destruction chance','Risque de casse à l’enchantement'),risk('safe','0%','0 %')],
              [navLabel('Zeny reset','Reset zeny'),`100 000 zeny · ${risk('danger','30% destruction','30 % de destruction')}`],
              [navLabel('Safe reset','Reset sécurisé'),`${itemLink('Zelstar')} ×1 · ${risk('safe','0% destruction','0 % de destruction')}`],
              [navLabel('Job Essence requirement','Prérequis Essence'),navLabel('Compatible armor refined to +9','Armure compatible raffinée à +9')]
            ])}

            <h3 id="md-requirements">${navLabel('Requirements and enchanting NPCs','Prérequis et NPC d’enchantement')}</h3>
            <div class="table-wrap"><table><thead><tr><th>${navLabel('Equipment rank','Rang d’équipement')}</th><th>${navLabel('NPC / navigation','NPC / navigation')}</th><th>${navLabel('Notes','Notes')}</th></tr></thead><tbody>
              <tr><th>${navLabel('Subjugation — Rank IV','Répression — Rang IV')}</th><td><code>/navi prt_fild05 251/193</code></td><td>${navLabel('Base Memorial Dungeon equipment.','Équipement de base des Mémorial Donjons.')}</td></tr>
              <tr><th>${navLabel('Higher ranks','Rangs supérieurs')}</th><td><code>/navi prt_in 135/35</code></td><td>${navLabel('The association interior contains the employees used for higher-rank equipment and class Essence pools.','L’intérieur de l’association contient les employés utilisés pour les rangs supérieurs et les pools d’Essences de classe.')}</td></tr>
            </tbody></table></div>

            <h3 id="md-process">${navLabel('Step-by-step enchant procedure','Procédure d’enchantement')}</h3>
            ${steps([
              navLabel('Bring a compatible Memorial Dungeon equipment piece to the correct Enchant Association employee.','Apporte une pièce d’équipement de Mémorial Donjon compatible auprès du bon employé de l’Association d’enchantement.'),
              navLabel('Select the equipment and the enchant slot offered by the NPC. The maximum number of available slots depends on the item/rank.','Sélectionne l’équipement et le slot d’enchantement proposé par le NPC. Le nombre maximum de slots dépend de l’objet et de son rang.'),
              navLabel('Pay 100,000 zeny. The enchant itself does not destroy the equipment.','Paie 100 000 zeny. L’enchantement lui-même ne détruit pas l’équipement.'),
              navLabel('A random option is rolled from the pool corresponding to the equipment/refine state.','Une option aléatoire est tirée dans le pool correspondant à l’équipement et à son niveau de raffinage.'),
              navLabel('To reroll, remove/reset the enchant first. Choose between the risky zeny reset and the safe Zelstar reset.','Pour refaire un tirage, retire/reset d’abord l’enchantement. Choisis entre le reset zeny risqué et le reset Zelstar sécurisé.')
            ])}

            <h3 id="md-risk">${navLabel('Enchant and reset risk table','Tableau des risques enchantement / reset')}</h3>
            <div class="table-wrap"><table>
              <thead><tr><th>${navLabel('Action','Action')}</th><th>${navLabel('Cost','Coût')}</th><th>${navLabel('Success / result','Réussite / résultat')}</th><th>${navLabel('Destruction','Destruction')}</th></tr></thead>
              <tbody>
                <tr><td>${navLabel('Add an enchant','Ajouter un enchantement')}</td><td>100 000 zeny</td><td>${navLabel('Random option is applied','Une option aléatoire est appliquée')}</td><td>${risk('safe','0%','0 %')}</td></tr>
                <tr><td>${navLabel('Reset with zeny','Reset avec zeny')}</td><td>100 000 zeny</td><td>${risk('warn','70% safe reset','70 % de reset sans casse')}</td><td>${risk('danger','30% item destruction','30 % de destruction de l’objet')}</td></tr>
                <tr><td>${navLabel('Reset with Zelstar','Reset avec Zelstar')}</td><td>${itemLink('Zelstar')} ×1</td><td>${risk('safe','100% safe reset','100 % de reset sécurisé')}</td><td>${risk('safe','0%','0 %')}</td></tr>
              </tbody>
            </table></div>
            <div class="notice"><svg class="notice-icon"><use href="#i-warning"></use></svg><div><strong>${navLabel('Important','Important')}:</strong> ${navLabel('the risky zeny reset is the dangerous step. A normal enchant attempt does not carry the same destruction risk.','le reset en zeny est l’étape dangereuse. Une tentative normale d’enchantement n’a pas le même risque de destruction.')}</div></div>

            <h3 id="md-slots">${navLabel('Job Essence slot by equipment rank','Slot des Essences selon le rang')}</h3>
            <p>${navLabel('Job Essences require a compatible armor at +9. The slot used by the Essence moves earlier as the Memorial equipment rank increases.','Les Essences de classe demandent une armure compatible à +9. Le slot utilisé par l’Essence avance lorsque le rang de l’équipement mémorial augmente.')}</p>
            <div class="table-wrap"><table><thead><tr><th>${navLabel('Equipment family','Famille d’équipement')}</th><th>${navLabel('Rank','Rang')}</th><th>${navLabel('Essence slot','Slot de l’Essence')}</th><th>${navLabel('Requirement','Prérequis')}</th></tr></thead><tbody>
              <tr><td>Subjugation / Répression</td><td>IV</td><td>4th</td><td>Armor +9</td></tr>
              <tr><td>Expedition / Expédition</td><td>III</td><td>4th</td><td>Armor / Robe +9</td></tr>
              <tr><td>Dispatching / Contingent</td><td>II</td><td>3rd</td><td>${navLabel('Compatible armor-type piece +9','Pièce de type armure compatible +9')}</td></tr>
              <tr><td>Conqueror / Conquérant</td><td>I</td><td>2nd</td><td>${navLabel('Compatible armor-type piece +9','Pièce de type armure compatible +9')}</td></tr>
            </tbody></table></div>

            <h3 id="md-rates">${navLabel('Random option rates — refine +0 to +8','Taux des options aléatoires — raffinage +0 à +8')}</h3>
            <p>${navLabel('For equipment in this refine range, the common stat pool uses the following distribution.','Pour les équipements dans cette plage de raffinage, le pool commun de statistiques utilise la distribution suivante.')}</p>
            <div class="table-wrap"><table class="enchant-rate-table"><thead><tr><th>${navLabel('Enchant','Enchantement')}</th><th>${navLabel('Rate','Taux')}</th></tr></thead><tbody>${baseRates.map(r=>`<tr><td>${esc(r[0])}</td><td>${esc(r[1])}</td></tr>`).join('')}</tbody></table></div>

            <h3>${navLabel('Random option rates — +9 Garment / Shoes','Taux des options aléatoires — Garment / Shoes +9')}</h3>
            <div class="table-wrap"><table><thead><tr><th>${navLabel('Enchant','Enchantement')}</th><th>Garment +9</th><th>Shoes +9</th></tr></thead><tbody>${plus9Rates.map(r=>`<tr><td>${esc(r[0])}</td><td>${esc(r[1])}</td><td>${esc(r[2])}</td></tr>`).join('')}</tbody></table></div>
            <div class="hero-actions"><a class="button" href="#/memorial-dungeons">${miniIcon('map')}${navLabel('Open Memorial Dungeons','Ouvrir Mémorial Donjon')}</a></div>
          </section>

          <section class="enchant-tab-panel" id="enchant-panel-essences">
            <h2 id="job-essences">${navLabel('Job Essence enchantments','Enchantements Essences de classe')}</h2>
            ${subnav([
              ['essence-rules',navLabel('Requirements / rules','Prérequis / règles')],['essence-first',navLabel('1st Job Essences','Essences classe 1')],['essence-second',navLabel('2nd Job Essences','Essences classe 2')]
            ])}
            ${facts([
              [navLabel('Compatible equipment','Équipement compatible'),navLabel('Memorial Dungeon armor-type equipment','Équipement de type armure des Mémorial Donjons')],
              [navLabel('Minimum refine','Raffinage minimum'),'+9'],
              [navLabel('Enchant cost','Coût enchantement'),'100 000 zeny'],
              [navLabel('Enchant destruction','Casse à l’enchantement'),risk('safe','0%','0 %')],
              [navLabel('Result selection','Choix du résultat'),navLabel('Random — the exact Essence is not directly selected','Aléatoire — l’Essence exacte n’est pas choisie directement')],
              [navLabel('Reset','Reset'),`${navLabel('Same Memorial equipment reset rules','Mêmes règles de reset que l’équipement mémorial')} · ${risk('danger','Zeny reset can break','Le reset zeny peut casser')} · ${risk('safe','Zelstar reset is safe','Reset Zelstar sécurisé')}`]
            ])}

            <h3 id="essence-rules">${navLabel('Requirements and rules','Prérequis et règles')}</h3>
            <ul>
              <li>${navLabel('The equipment must be an eligible Memorial Dungeon armor-type piece refined to +9 or higher.','L’équipement doit être une pièce de type armure de Mémorial Donjon compatible, raffinée à +9 ou plus.')}</li>
              <li>${navLabel('The Essence occupies the rank-specific enchant slot shown in the Memorial Equipment tab.','L’Essence occupe le slot d’enchantement correspondant au rang indiqué dans l’onglet Équipement mémorial.')}</li>
              <li>${navLabel('The result is random inside the pool offered by the employee; you do not directly choose Lv.1/Lv.2 or Essence I/II.','Le résultat est aléatoire dans le pool proposé par l’employé ; tu ne choisis pas directement Lv.1/Lv.2 ni Essence I/II.')}</li>
              <li>${navLabel('The normal enchant action itself does not destroy the armor. The dangerous action is the zeny reset.','L’enchantement normal ne détruit pas l’armure. L’action dangereuse est le reset en zeny.')}</li>
            </ul>

            <h3 id="essence-first">${navLabel('First Job Essences','Essences de classe 1')}</h3>
            <div class="table-wrap"><table><thead><tr><th>${navLabel('Job','Classe')}</th><th>Lv.1</th><th>Lv.2</th></tr></thead><tbody>
              ${firstEssences.map(e=>`<tr><th>${esc(e.job)}</th><td class="essence-effect"><strong>${itemLink(`${e.job}'s Essence Lv.1`)}</strong><br>${esc(e.lv1)}</td><td class="essence-effect"><strong>${itemLink(`${e.job}'s Essence Lv.2`)}</strong><br>${esc(e.lv2)}</td></tr>`).join('')}
            </tbody></table></div>

            <h3 id="essence-second">${navLabel('Second Job Essences — Essence I and Essence II','Essences de classe 2 — Essence I et Essence II')}</h3>
            <p>${navLabel('Each second-job family has two different Essence lines. Essence I and Essence II support different parts of the class skill tree, and each line has Lv.1 and Lv.2 versions.','Chaque famille de seconde classe possède deux lignes d’Essence différentes. Essence I et Essence II renforcent des parties différentes du skill tree, et chaque ligne possède une version Lv.1 et Lv.2.')}</p>
            <div class="table-wrap"><table><thead><tr><th>${navLabel('Class','Classe')}</th><th>Essence I Lv.1</th><th>Essence I Lv.2</th><th>Essence II Lv.1</th><th>Essence II Lv.2</th></tr></thead><tbody>
              ${secondEssences.map(e=>`<tr><th>${esc(e.job)}</th><td class="essence-effect">${esc(e.i1)}</td><td class="essence-effect">${esc(e.i2)}</td><td class="essence-effect">${esc(e.ii1)}</td><td class="essence-effect">${esc(e.ii2)}</td></tr>`).join('')}
            </tbody></table></div>
          </section>

          <section class="enchant-tab-panel" id="enchant-panel-taming">
            <h2 id="taming-ring">Taming Ring</h2>
            ${subnav([
              ['taming-requirements',navLabel('Requirements','Prérequis')],['taming-process',navLabel('Procedure','Procédure')],['taming-risk',navLabel('Success / reset','Réussite / reset')],['taming-merchants',navLabel('Merchants','Marchands')]
            ])}
            ${facts([
              [navLabel('Item','Objet'),itemLink('Taming Ring')],
              [navLabel('Required level','Niveau requis'),'1'],
              [navLabel('Equippable by','Utilisable par'),navLabel('All jobs — Accessory Right','Toutes les classes — Accessory Right')],
              [navLabel('Ring price','Prix de la bague'),'50 000 zeny'],
              ['Lv.1',`${navLabel('1 Pet Egg + 10,000 zeny','1 Pet Egg + 10 000 zeny')} · ${risk('safe','100% success','100 % de réussite')}`],
              ['Lv.2',`${navLabel('2nd identical Pet Egg','2e Pet Egg identique')} · ${risk('warn','50% success','50 % de réussite')}`],
              [navLabel('Reset','Reset'),risk('safe','100% success','100 % de réussite')],
              [navLabel('Ring destruction','Destruction de la bague'),risk('safe','No breaking mechanic indicated','Aucune casse indiquée')]
            ])}

            <h3 id="taming-requirements">${navLabel('Requirements','Prérequis')}</h3>
            <ul>
              <li>${navLabel('Own and equip a Taming Ring in the right accessory slot.','Possède et équipe une Taming Ring dans le slot Accessory Right.')}</li>
              <li>${navLabel('For Lv.1, you need the Pet Egg whose bonus you want to seal into the ring.','Pour le Lv.1, il faut le Pet Egg dont tu veux sceller le bonus dans la bague.')}</li>
              <li>${navLabel('For Lv.2, you need a second egg of exactly the same pet.','Pour le Lv.2, il faut un second œuf exactement du même pet.')}</li>
            </ul>

            <h3 id="taming-process">${navLabel('Enchant interface and procedure','Interface et procédure d’enchantement')}</h3>
            ${steps([
              navLabel('Buy the Taming Ring from a Taming Merchant and equip it.','Achète la Taming Ring auprès d’un Taming Merchant et équipe-la.'),
              navLabel('Open the enchantment interface. The General tab lists the Pet Eggs that can be sealed into the ring.','Ouvre l’interface d’enchantement. L’onglet General liste les Pet Eggs pouvant être scellés dans la bague.'),
              navLabel('Select the egg and create the Lv.1 enchant. The Lv.1 step has a 100% success rate.','Sélectionne l’œuf et crée l’enchantement Lv.1. Cette étape possède 100 % de réussite.'),
              navLabel('To upgrade the same pet enchant, use the Growth tab with a second identical egg. Lv.2 has a 50% success rate.','Pour améliorer le même enchantement de pet, utilise l’onglet Growth avec un second œuf identique. Le Lv.2 possède 50 % de réussite.'),
              navLabel('Use the Reset tab when you want to remove the current pet enchant and start again with another egg.','Utilise l’onglet Reset lorsque tu veux retirer l’enchantement de pet actuel et recommencer avec un autre œuf.')
            ])}

            <h3 id="taming-risk">${navLabel('Success, failure and reset','Réussite, échec et reset')}</h3>
            <div class="table-wrap"><table><thead><tr><th>${navLabel('Action','Action')}</th><th>${navLabel('Material','Matériau')}</th><th>${navLabel('Success','Réussite')}</th><th>${navLabel('Ring destroyed?','Bague détruite ?')}</th></tr></thead><tbody>
              <tr><td>${navLabel('Create Lv.1','Créer Lv.1')}</td><td>1 Pet Egg + 10 000 zeny</td><td>${risk('safe','100%','100 %')}</td><td>${risk('safe','No','Non')}</td></tr>
              <tr><td>${navLabel('Upgrade to Lv.2','Passer Lv.2')}</td><td>${navLabel('2nd identical Pet Egg','2e Pet Egg identique')}</td><td>${risk('warn','50%','50 %')}</td><td>${risk('safe','No breaking mechanic indicated','Aucune casse indiquée')}</td></tr>
              <tr><td>Reset</td><td>${navLabel('Handled in the Reset tab','Géré dans l’onglet Reset')}</td><td>${risk('safe','100%','100 %')}</td><td>${risk('safe','No','Non')}</td></tr>
            </tbody></table></div>
            <div class="enchant-detail-note">${navLabel('The 50% Lv.2 roll concerns the upgrade attempt; it is not an item-refine style destruction roll on the Taming Ring.','Le jet à 50 % du Lv.2 concerne la tentative d’amélioration ; ce n’est pas un jet de destruction de type raffinage sur la Taming Ring.')}</div>

            <h3 id="taming-merchants">${navLabel('Taming Merchants','Taming Merchants')}</h3>
            <div class="table-wrap"><table><thead><tr><th>${navLabel('City','Ville')}</th><th>${navLabel('Navigation','Navigation')}</th></tr></thead><tbody>
              <tr><td>Payon</td><td><code>/navi payon 175/131</code></td></tr>
              <tr><td>Geffen</td><td><code>/navi geffen 193/152</code></td></tr>
              <tr><td>Izlude</td><td><code>/navi izlude 72/98</code></td></tr>
              <tr><td>Morocc</td><td><code>/navi morocc 203/83</code></td></tr>
              <tr><td>Prontera</td><td><code>/navi prontera 218/211</code></td></tr>
            </tbody></table></div>
            <div class="hero-actions"><a class="button" href="#/wiki/pet-system">${miniIcon('monster')}${navLabel('Open Pet System and egg bonuses','Ouvrir Système de Pet et les bonus des œufs')}</a></div>
          </section>
        </div>
      </div>

      ${officialSources([
        ['Memorial Dungeon Equipment Enchanting','https://old.criatura-academy.com/memorial-dungeons/equipment-enchanting/'],
        ['Poring Village','https://old.criatura-academy.com/memorial-dungeons/poring-village'],
        ['Memorial Dungeons — current guide','https://midgardhub.com/guides/memorial-dungeons'],
        ['Complete New Player Guide — costumes / pets','https://midgardhub.com/guides/new-player'],
        ['Ragnarok Zero Guide — enchantments / Taming Ring','https://sites.google.com/view/rozeroguide'],
        ['Memorial equipment enchanting — Global reference','https://roz-global.info/donjon-equipement-enchantement.html'],
        ['Qpets / Taming Ring — Global reference','https://roz-global.info/qpets.html'],
        ['Costume Stone Enchants — layout reference','https://irowiki.org/wiki/Costume_Stone_Enchants']
      ])}`;
  }
'''

s = s[:start] + new_func + s[end:]

# Keep the status map aligned with the detailed subsections.
old = "'#/wiki/enchantment': { costume:'partial', 'poring-village':'complete', 'memorial-gear':'partial', 'job-essences':'partial', 'taming-ring':'complete' },"
new = "'#/wiki/enchantment': { costume:'partial', 'poring-village':'complete', 'memorial-gear':'complete', 'job-essences':'partial', 'taming-ring':'complete' },"
if old in s:
    s = s.replace(old, new, 1)

# Basic assertions against accidental regressions.
for needle in [
    '70 % de réussite', 'l’objet reste intact', '100 000 zeny', '30 % de destruction de l’objet',
    'Zelstar', 'Random option rates — refine +0 to +8', 'Essence I Lv.1', 'Essence II Lv.2',
    '1 Pet Egg + 10 000 zeny', '50 % de réussite', '/navi prontera 218/211'
]:
    assert needle in s, needle

# Do not expose source-site provenance inside guide prose; names are allowed only in officialSources.
a = s.index('  function enchantmentPage(topic) {')
b = s.index('${officialSources([', a)
guide = s[a:b]
for site in ['Criatura','MidgardHub','iRO Wiki','roz-global','TWRo','KRO']:
    assert site not in guide, site

p.write_text(s, encoding='utf-8')
