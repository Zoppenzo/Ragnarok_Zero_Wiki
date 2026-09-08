/* Ragnarok Zero Global client synchronizer.
 * Gameplay values are synchronized from the current client tables.
 * Notes follow the iRO Wiki approach: only useful, non-obvious mechanics are
 * shown, and only when they are compatible with the current Zero data.
 */
(function () {
  'use strict';

  const JOB_BY_CLASS = {
    novice:0,swordman:1,mage:2,archer:3,acolyte:4,merchant:5,thief:6,
    knight:7,priest:8,wizard:9,blacksmith:10,hunter:11,assassin:12,
    crusader:14,monk:15,sage:16,rogue:17,alchemist:18,bard:19,dancer:20
  };

  const SLUG_AEGIS = {
    'basic-skill':'NV_BASIC','first-aid':'NV_FIRSTAID','play-dead':'NV_TRICKDEAD',
    'sword-mastery':'SM_SWORD','increase-hp-recovery':'SM_RECOVERY','bash':'SM_BASH','provoke':'SM_PROVOKE',
    'berserk-swordman':'SM_AUTOBERSERK','hp-recovery-while-moving':'SM_MOVINGRECOVERY','two-handed-sword-mastery':'SM_TWOHAND',
    'magnum-break':'SM_MAGNUM','endure':'SM_ENDURE','fatal-blow':'SM_FATALBLOW','spear-mastery':'KN_SPEARMASTERY',
    'stone-curse':'MG_STONECURSE','cold-bolt':'MG_COLDBOLT','lightning-bolt':'MG_LIGHTNINGBOLT','napalm-beat':'MG_NAPALMBEAT',
    'fire-bolt':'MG_FIREBOLT','sight':'MG_SIGHT','earth-spike':'WZ_EARTHSPIKE','frost-diver':'MG_FROSTDIVER','frost-driver':'MG_FROSTDIVER',
    'thunder-storm':'MG_THUNDERSTORM','soul-strike':'MG_SOULSTRIKE','fire-ball':'MG_FIREBALL','energy-coat':'MG_ENERGYCOAT',
    'increase-sp-recovery':'MG_SRECOVERY','safety-wall':'MG_SAFETYWALL','fire-wall':'MG_FIREWALL',
    'double-strafe':'AC_DOUBLE','owls-eye':'AC_OWL','vultures-eye':'AC_VULTURE','improve-concentration':'AC_CONCENTRATION',
    'arrow-shower':'AC_SHOWER','arrow-crafting':'AC_MAKINGARROW','arrow-repel':'AC_CHARGEARROW',
    'enlarge-weight-limit':'MC_INCCARRY','axe-mastery':'AM_AXEMASTERY','discount':'MC_DISCOUNT','overcharge':'MC_OVERCHARGE',
    'pushcart':'MC_PUSHCART','item-appraisal':'MC_IDENTIFY','vending':'MC_VENDING','mammonite':'MC_MAMMONITE',
    'cart-revolution':'MC_CARTREVOLUTION','change-cart':'MC_CHANGECART','crazy-uproar':'MC_LOUD','cart-boost':'WS_CARTBOOST',
    'double-attack':'TF_DOUBLE','improve-dodge':'TF_MISS','steal':'TF_STEAL','hiding':'TF_HIDING','envenom':'TF_POISON',
    'detoxify':'TF_DETOXIFY','sand-attack':'TF_SPRINKLESAND','back-slide':'TF_BACKSLIDING','find-stone':'TF_PICKSTONE','stone-fling':'TF_THROWSTONE',
    'divine-protection':'AL_DP','demon-bane':'AL_DEMONBANE','ruwach':'AL_RUWACH','pneuma':'AL_PNEUMA','teleport':'AL_TELEPORT',
    'warp-portal':'AL_WARP','heal':'AL_HEAL','increase-agility':'AL_INCAGI','decrease-agility':'AL_DECAGI','aqua-benedicta':'AL_HOLYWATER',
    'signum-crucis':'AL_CRUCIS','angelus':'AL_ANGELUS','blessing':'AL_BLESSING','cure':'AL_CURE','holy-light':'AL_HOLYLIGHT','mace-mastery':'PR_MACEMASTERY'
  };

  const N = (en,fr) => ({en,fr});

  const SKILL_NOTES = {
    /* Swordman */
    'increase-hp-recovery': [
      N('The healing-item bonus stacks with the healing increase obtained from VIT.','Le bonus sur les objets de soin se cumule avec l’augmentation des soins apportée par la VIT.'),
      N('Natural recovery from this skill does not occur when normal HP regeneration is disabled, such as while overweight.','La récupération naturelle de ce skill ne se déclenche pas lorsque la régénération normale des HP est désactivée, notamment en surcharge.'),
      N('The character may still attack while standing on the same cell and receive the periodic recovery; moving to another cell resets the stationary condition.','Le personnage peut continuer à attaquer sans changer de case et recevoir la récupération périodique ; se déplacer sur une autre case interrompt la condition stationnaire.')
    ],
    'bash': [
      N('Bash’s Accuracy bonus is applied to the user’s hit chance rather than being a flat HIT value. At Lv.10, the 50% bonus multiplies the current chance to hit by 1.5.','Le bonus de précision de Bash s’applique à la chance de toucher du personnage et non comme une valeur HIT fixe. Au Lv.10, le bonus de 50 % multiplie la chance de toucher actuelle par 1,5.'),
      N('When Fatal Blow is learned, Bash can Stun from Bash Lv.6 onward. Base Level further increases the Stun chance.','Lorsque Fatal Blow est appris, Bash peut infliger Stun à partir de Bash Lv.6. Le Base Level augmente également la chance de Stun.')
    ],
    'provoke': [
      N('Against players, Provoke reduces only soft DEF.','Contre les joueurs, Provoke réduit uniquement la soft DEF.'),
      N('Provoke does not affect Undead-property monsters or Boss monsters.','Provoke n’affecte pas les monstres de propriété Undead ni les Boss.'),
      N('Because it deals no damage, Provoke can be used to draw a normal monster’s attention without damaging it.','Comme il n’inflige pas de dégâts, Provoke peut servir à attirer l’attention d’un monstre normal sans le blesser.')
    ],
    'berserk-swordman': [
      N('The Provoked effect remains while HP is below 25% Max HP and ends when HP rises above that threshold or the Provoke-like effect is removed.','L’effet Provoked reste actif tant que les HP sont sous 25 % des HP max et disparaît lorsque les HP repassent au-dessus de ce seuil ou lorsque l’effet de type Provoke est retiré.'),
      N('The skill itself costs no SP, but it cannot be activated while the character has 0 SP.','Le skill ne consomme pas de SP, mais il ne peut pas être activé lorsque le personnage est à 0 SP.')
    ],
    'hp-recovery-while-moving': [
      N('Moving HP Recovery enables natural HP recovery while walking, but it does not activate the extra recovery from Increase HP Recovery until the character stops moving or sits.','Moving HP Recovery permet la régénération naturelle en marchant, mais n’active pas la récupération supplémentaire de Increase HP Recovery tant que le personnage ne s’arrête pas ou ne s’assoit pas.')
    ],
    'two-handed-sword-mastery': [
      N('As a Weapon Mastery bonus, it does not increase skills whose damage formula ignores Weapon Mastery / Weapon ATK bonuses.','En tant que bonus de Weapon Mastery, il n’augmente pas les skills dont la formule ignore les bonus de Weapon Mastery / Weapon ATK.')
    ],
    'magnum-break': [
      N('The 10-second buff does not change the weapon itself to Fire property. It adds a separate 20% Fire-property damage component while the normal part keeps its own element.','Le buff de 10 secondes ne transforme pas l’arme en propriété Feu. Il ajoute une composante séparée de 20 % de dégâts Feu tandis que la partie normale conserve son propre élément.'),
      N('The additional Fire-property component pierces DEF and is also applied to Magnum Break’s own hit.','La composante supplémentaire de propriété Feu ignore la DEF et s’applique également au coup de Magnum Break lui-même.'),
      N('When an attack skill is pseudo-elemental, Magnum Break’s added 20% Fire component follows that pseudo-elemental behavior as well.','Lorsqu’un skill d’attaque est pseudo-élémental, la composante Feu supplémentaire de 20 % de Magnum Break suit elle aussi ce comportement pseudo-élémental.')
    ],
    'endure': [
      N('The flinch immunity is removed after the character has received enough hits; the current client specifies 7 hits.','L’immunité au flinch disparaît après avoir reçu suffisamment de coups ; le client actuel indique 7 coups.'),
      N('The client description states that Endure cannot be used in Siege areas.','La description du client indique que Endure ne peut pas être utilisé dans les zones de Siege.')
    ],
    'fatal-blow': [
      N('Fatal Blow does not attack by itself; it enables Bash Lv.6–10 to inflict Stun.','Fatal Blow n’attaque pas directement ; il permet à Bash Lv.6–10 d’infliger Stun.'),
      N('Base Level further increases the Stun chance granted to Bash.','Le Base Level augmente également la chance de Stun ajoutée à Bash.')
    ],

    /* Mage */
    'stone-curse': [
      N('Petrification is not instantaneous: the target first enters the pre-petrified state before becoming fully Stone.','La pétrification n’est pas instantanée : la cible passe d’abord par l’état de pré-pétrification avant de devenir complètement Stone.'),
      N('A fully Petrified target becomes Earth Lv.1 regardless of its original element.','Une cible complètement Petrified devient Earth Lv.1, quel que soit son élément d’origine.'),
      N('Boss and Undead-property monsters cannot be petrified by Stone Curse.','Les Boss et les monstres de propriété Undead ne peuvent pas être pétrifiés par Stone Curse.')
    ],
    'cold-bolt': [N('Although several hit animations are shown, the damage is resolved as one bundled attack.','Même si plusieurs impacts sont affichés, les dégâts sont résolus comme une seule attaque groupée.')],
    'lightning-bolt': [N('Although several hit animations are shown, the damage is resolved as one bundled attack.','Même si plusieurs impacts sont affichés, les dégâts sont résolus comme une seule attaque groupée.')],
    'fire-bolt': [N('Although several hit animations are shown, the damage is resolved as one bundled attack.','Même si plusieurs impacts sont affichés, les dégâts sont résolus comme une seule attaque groupée.')],
    'sight': [N('Sight reveals normal hidden targets around the caster but does not reveal targets protected by the separate Stealth mechanic.','Sight révèle les cibles normalement cachées autour du lanceur mais ne révèle pas les cibles protégées par la mécanique distincte Stealth.')],
    'earth-spike': [
      N('Despite the animation, all hits are resolved as one bundled attack.','Malgré l’animation, tous les impacts sont résolus comme une seule attaque groupée.'),
      N('Earth Spike can still hit a target that becomes hidden after the cast has already started, as long as the target was visible when targeted.','Earth Spike peut encore toucher une cible qui se cache après le début du cast, tant qu’elle était visible au moment du ciblage.'),
      N('Earth Spike is not treated as a Bolt skill.','Earth Spike n’est pas traité comme un Bolt skill.')
    ],
    'frost-diver': [
      N('A Frozen target becomes Water Lv.1 regardless of its original element, making Wind-property attacks especially effective while the status lasts.','Une cible Frozen devient Water Lv.1 quel que soit son élément d’origine, ce qui rend les attaques Wind particulièrement efficaces pendant le statut.'),
      N('Boss and Undead-property monsters cannot be Frozen by Frost Diver, although the skill can still damage them.','Les Boss et les monstres de propriété Undead ne peuvent pas être Frozen par Frost Diver, même si le skill peut toujours leur infliger des dégâts.')
    ],
    'thunder-storm': [N('Despite the repeated lightning animation, the damage is resolved as one bundled attack.','Malgré les éclairs répétés de l’animation, les dégâts sont résolus comme une seule attaque groupée.')],
    'soul-strike': [N('Despite the multiple spirit animations, all damage is resolved as one bundled attack.','Malgré les multiples esprits affichés, tous les dégâts sont résolus comme une seule attaque groupée.')],
    'energy-coat': [
      N('Energy Coat’s protection depends on the caster’s remaining SP and consumes SP when physical damage is reduced.','La protection de Energy Coat dépend des SP restants du lanceur et consomme des SP lorsqu’elle réduit des dégâts physiques.')
    ],
    'increase-sp-recovery': [
      N('The SP-restoration bonus from items stacks with the restoration increase obtained from INT.','Le bonus de récupération SP des objets se cumule avec l’augmentation de récupération apportée par l’INT.'),
      N('No SP is restored when normal SP regeneration is disabled, such as while overweight.','Aucun SP n’est récupéré lorsque la régénération normale des SP est désactivée, notamment en surcharge.'),
      N('Casting or attacking without changing cells does not by itself stop the periodic recovery.','Caster ou attaquer sans changer de case n’interrompt pas à lui seul la récupération périodique.')
    ],
    'safety-wall': [
      N('Safety Wall cannot overlap Pneuma, and Pneuma cannot be placed on a Safety Wall cell.','Safety Wall ne peut pas se superposer à Pneuma, et Pneuma ne peut pas être placé sur une case occupée par Safety Wall.'),
      N('It does not prevent status effects or knockback unless those effects come from an attack that Safety Wall successfully blocks.','Il n’empêche pas les statuts ou le knockback sauf lorsque ces effets proviennent d’une attaque effectivement bloquée par Safety Wall.'),
      N('The hit that exhausts the wall is still fully absorbed, so a Safety Wall always blocks at least one valid hit.','Le coup qui épuise le mur est tout de même entièrement absorbé ; un Safety Wall bloque donc toujours au moins un coup valide.')
    ],
    'fire-wall': [
      N('A maximum of three Fire Walls can exist from the same caster at the same time.','Un même lanceur peut avoir au maximum trois Fire Walls actifs simultanément.'),
      N('Boss monsters are not knocked back by Fire Wall, but they still consume the hits of the cells they cross.','Les Boss ne sont pas repoussés par Fire Wall, mais ils consomment tout de même les impacts des cases qu’ils traversent.'),
      N('If the caster becomes incapacitated by a status such as Stun, Frozen or Stone, active Fire Walls stop processing hits until the caster can act again.','Si le lanceur est neutralisé par un statut comme Stun, Frozen ou Stone, les Fire Walls actifs cessent de traiter leurs impacts jusqu’à ce que le lanceur puisse de nouveau agir.')
    ],

    /* Archer */
    'double-strafe': [N('Despite the double-shot animation, both hits are resolved as one bundled damage event.','Malgré l’animation en double tir, les deux impacts sont résolus comme un seul événement de dégâts groupé.')],
    'vultures-eye': [N('The HIT bonus from Vulture’s Eye is implicit and may not be shown directly in the Status Window.','Le bonus de HIT de Vulture’s Eye est implicite et peut ne pas apparaître directement dans la fenêtre de statut.')],
    'improve-concentration': [
      N('The percentage stat increase is based on the character’s underlying AGI/DEX sources; temporary buffs and several bonus-stat sources are not recursively multiplied by Improve Concentration.','L’augmentation en pourcentage se base sur les sources de base d’AGI/DEX du personnage ; les buffs temporaires et plusieurs sources de stats bonus ne sont pas remultipliés par Improve Concentration.'),
      N('Activating the skill also reveals hidden enemies in the small area around the caster.','L’activation du skill révèle également les ennemis cachés dans la petite zone autour du lanceur.')
    ],
    'arrow-shower': [
      N('Knockback direction is based on the enemy’s position relative to the targeted cell; a target on the exact center cell is pushed west.','La direction du knockback dépend de la position de l’ennemi par rapport à la case ciblée ; une cible exactement sur la case centrale est repoussée vers l’ouest.'),
      N('Arrow Shower can hit cloaked targets.','Arrow Shower peut toucher les cibles sous Cloaking.'),
      N('The skill can push traps in the same way it pushes monsters or players.','Le skill peut repousser les traps de la même manière qu’il repousse les monstres ou les joueurs.')
    ],
    'arrow-repel': [
      N('The cast cannot be interrupted.','Le cast ne peut pas être interrompu.'),
      N('Knockback direction follows the target’s position relative to the Archer; a target occupying the same cell is pushed west.','La direction du knockback dépend de la position de la cible par rapport à l’Archer ; une cible sur la même case est repoussée vers l’ouest.')
    ],

    /* Merchant */
    'axe-mastery': [N('As a Weapon Mastery bonus, it only contributes to damage formulas that accept Weapon Mastery bonuses.','En tant que bonus de Weapon Mastery, il ne contribue qu’aux formules de dégâts qui prennent en compte les Weapon Masteries.')],
    'discount': [N('The jump from Lv.9 to Lv.10 is only one additional percentage point, smaller than the earlier level increases.','Le passage du Lv.9 au Lv.10 n’ajoute qu’un point de pourcentage, soit une progression plus faible que les niveaux précédents.')],
    'overcharge': [N('The jump from Lv.9 to Lv.10 is only one additional percentage point, smaller than the earlier level increases.','Le passage du Lv.9 au Lv.10 n’ajoute qu’un point de pourcentage, soit une progression plus faible que les niveaux précédents.')],
    'pushcart': [N('The cart is a separate storage inventory. Increasing Pushcart level removes the movement-speed penalty progressively until normal movement speed is restored at Lv.10.','La charrette est un inventaire de stockage séparé. Monter Pushcart réduit progressivement la pénalité de vitesse de déplacement jusqu’au retour à la vitesse normale au Lv.10.')],
    'vending': [N('Normal Vending sells items stored in the Pushcart; the skill itself is distinct from any separate offline-vending system.','Vending normal vend les objets stockés dans la Pushcart ; le skill lui-même est distinct de tout système séparé de vending hors ligne.')],
    'mammonite': [N('Each additional skill level effectively pays another 100 Zeny for +50% ATK, reaching 600% ATK for 1,000 Zeny at Lv.10.','Chaque niveau supplémentaire revient à payer 100 Zeny de plus pour +50 % ATK, jusqu’à 600 % ATK pour 1 000 Zeny au Lv.10.')],
    'cart-revolution': [
      N('Cart Revolution ignores the normal accuracy check.','Cart Revolution ignore le check de précision normal.'),
      N('Damage increases with the current cart weight and reaches its maximum when the cart is full.','Les dégâts augmentent avec le poids actuel de la charrette et atteignent leur maximum lorsque la charrette est pleine.'),
      N('Its damage is pseudo-elemental.','Ses dégâts sont pseudo-élémentaux.')
    ],
    'change-cart': [N('The available cart appearances depend on the character’s Base Level.','Les apparences de charrette disponibles dépendent du Base Level du personnage.')],
    'find-stone': [N('The skill cannot be used when carried weight exceeds 70%.','Le skill ne peut pas être utilisé lorsque le poids transporté dépasse 70 %.')],

    /* Thief */
    'double-attack': [
      N('Despite the animation, the two hits are bundled into one displayed damage event.','Malgré l’animation, les deux coups sont regroupés dans un seul événement de dégâts affiché.'),
      N('Critical-damage bonuses are applied to each hit before the result is bundled into the displayed number.','Les bonus de dégâts critiques sont appliqués à chaque coup avant que le résultat soit regroupé dans le nombre affiché.'),
      N('The current Zero client explicitly states that with Katar weapons this skill affects the damage dealt by the left hand.','Le client Zero actuel précise explicitement qu’avec les Katar, ce skill affecte les dégâts infligés par la main gauche.')
    ],
    'improve-dodge': [N('The FLEE gain changes after second job: the current client states +3 FLEE per level before second job and +4 per level after second job. Assassin classes also receive the movement-speed effect.','Le gain de FLEE change après la seconde classe : le client actuel indique +3 FLEE par niveau avant la seconde classe et +4 par niveau après. Les classes Assassin reçoivent aussi l’effet de vitesse de déplacement.')],
    'steal': [
      N('A monster can only yield one successfully stolen item per spawn.','Un monstre ne peut fournir qu’un seul objet volé avec succès par apparition.'),
      N('Steal cannot be used successfully on Boss monsters or players.','Steal ne peut pas réussir sur les Boss ni sur les joueurs.'),
      N('The success chance is affected by the DEX difference between the Thief and the target in addition to skill level.','La chance de réussite dépend de la différence de DEX entre le Thief et la cible, en plus du niveau du skill.')
    ],
    'hiding': [
      N('Natural SP recovery is disabled while Hiding is active.','La récupération naturelle des SP est désactivée pendant Hiding.'),
      N('Detection skills and Demon-, Insect- and Boss-type monsters can reveal or detect a hidden character.','Les skills de détection ainsi que les monstres de type Demon, Insect et Boss peuvent révéler ou détecter un personnage caché.')
    ],
    'envenom': [N('Poison inflicted by Envenom deals HP-proportional damage over time and reduces physical DEF by 25% while the status is active.','Poison infligé par Envenom cause des dégâts proportionnels aux HP au fil du temps et réduit la DEF physique de 25 % pendant le statut.')],
    'detoxify': [N('Detoxify removes Poison and can be cast at range on another valid target; it is not limited to the caster.','Detoxify retire Poison et peut être lancé à distance sur une autre cible valide ; il n’est pas limité au lanceur.')],
    'sand-attack': [N('Sand Attack deals Earth-property melee physical damage; its Blind effect is a separate status application.','Sand Attack inflige des dégâts physiques de mêlée Earth ; son effet Blind est une application de statut séparée.')],
    'back-slide': [N('Back Slide moves the character five cells directly backward relative to the direction they are facing, provided the destination path is valid.','Back Slide déplace le personnage de cinq cases directement vers l’arrière par rapport à son orientation, si le trajet est valide.')],
    'stone-fling': [N('Stone Fling deals fixed 50 physical damage that ignores DEF and separately has a low chance to inflict Stun or Blind.','Stone Fling inflige 50 dégâts physiques fixes qui ignorent la DEF et possède séparément une faible chance d’infliger Stun ou Blind.')],

    /* Acolyte */
    'ruwach': [N('Ruwach only deals its Holy damage when it reveals an enemy; its primary function is detection around the caster.','Ruwach n’inflige ses dégâts Holy que lorsqu’il révèle un ennemi ; sa fonction principale reste la détection autour du lanceur.')],
    'heal': [
      N('Heal scales with skill level, Base Level, total INT and the equipped weapon’s MATK.','Heal dépend du niveau du skill, du Base Level, de l’INT totale et de la MATK de l’arme équipée.'),
      N('When used offensively on Undead-property monsters, it deals Holy special magic damage equal to 50% of the Heal effect.','Utilisé offensivement sur les monstres de propriété Undead, il inflige des dégâts magiques spéciaux Holy égaux à 50 % de l’effet de Heal.')
    ],
    'increase-agility': [N('Casting Increase Agility consumes 15 HP in addition to its SP cost.','Lancer Increase Agility consomme 15 HP en plus de son coût en SP.')],
    'decrease-agility': [N('Decrease AGI is an opposing movement/AGI debuff and can overwrite the movement benefit of Increase Agility when it lands.','Decrease AGI est un debuff opposé d’AGI/vitesse de déplacement et peut supprimer le bénéfice de déplacement de Increase Agility lorsqu’il réussit.')],
    'aqua-benedicta': [N('The caster must stand in shallow water and consumes one Empty Bottle to create one Holy Water.','Le lanceur doit se tenir dans de l’eau peu profonde et consomme une Empty Bottle pour créer une Holy Water.')],
    'blessing': [
      N('On players, Blessing increases STR, INT, DEX and HIT and can remove Curse/Petrification according to the current client description.','Sur les joueurs, Blessing augmente STR, INT, DEX et HIT et peut retirer Curse/Petrification selon la description du client actuel.'),
      N('When used on Demon or Undead monsters, it instead reduces STR, INT and DEX by 50%.','Utilisé sur les monstres Demon ou Undead, il réduit au contraire STR, INT et DEX de 50 %.')
    ],
    'cure': [N('Cure removes Silence, Confusion and Blind. A character affected by Silence generally needs another source to remove Silence because Silence prevents normal skill use.','Cure retire Silence, Confusion et Blind. Un personnage sous Silence a généralement besoin d’une autre source pour retirer Silence, puisque Silence empêche l’utilisation normale des skills.')],
    'holy-light': [N('The current Zero client states that Holy Light removes Kyrie Eleison from a target that has it.','Le client Zero actuel indique que Holy Light retire Kyrie Eleison d’une cible qui le possède.')],
    'pneuma': [
      N('Pneuma blocks ranged physical attacks inside its protected area but does not block magic merely because it is ranged.','Pneuma bloque les attaques physiques à distance dans sa zone protégée, mais ne bloque pas la magie simplement parce qu’elle est à distance.'),
      N('Pneuma cannot overlap Safety Wall, and Safety Wall cannot be placed on a Pneuma cell.','Pneuma ne peut pas se superposer à Safety Wall, et Safety Wall ne peut pas être placé sur une case Pneuma.')
    ],
    'teleport': [N('Lv.1 teleports to a random valid cell on the current map; Lv.2 adds the option to return to the saved point. Maps that disable teleport prevent the corresponding use.','Le Lv.1 téléporte vers une case valide aléatoire de la map actuelle ; le Lv.2 ajoute l’option de retour au point de sauvegarde. Les maps qui désactivent la téléportation empêchent l’utilisation correspondante.')],
    'warp-portal': [N('Warp Portal consumes a Blue Gemstone and creates a ground portal to one of the caster’s memorized destinations.','Warp Portal consomme une Blue Gemstone et crée un portail au sol vers l’une des destinations mémorisées par le lanceur.')],
    'angelus': [N('Angelus increases the VIT-based portion of Defense rather than simply multiplying every source of equipment DEF.','Angelus augmente la partie de la défense basée sur la VIT au lieu de multiplier directement toutes les sources de DEF d’équipement.')],
    'divine-protection': [N('The reduction applies specifically against Demon-race and Undead-property enemies; those are two separate monster classifications.','La réduction s’applique spécifiquement aux ennemis de race Demon et de propriété Undead ; il s’agit de deux classifications distinctes.')],
    'demon-bane': [N('The damage bonus applies specifically against Demon-race and Undead-property targets, and the current client also states that the effect increases with character level.','Le bonus de dégâts s’applique spécifiquement aux cibles de race Demon et de propriété Undead, et le client actuel précise également que l’effet augmente avec le niveau du personnage.')]
  };

  const norm = s => String(s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9]+/g,'');
  const arrAt = (a,i) => Array.isArray(a) && a.length ? a[Math.min(i,a.length-1)] : null;

  function time(ms) {
    if (ms == null) return null;
    const n=Number(ms);
    if (!Number.isFinite(n)) return null;
    if (n===0) return 'None';
    if (n%1000===0) return (n/1000)+' s';
    return (n/1000).toFixed(3).replace(/0+$/,'').replace(/\.$/,'')+' s';
  }

  function castAt(r,i) {
    if (!r.d) return 'None';
    const f=arrAt(r.d.cf,i), v=arrAt(r.d.cv,i);
    if (f==null && v==null) return 'None';
    const fn=Number(f||0), vn=Number(v||0), total=fn+vn;
    if (!total) return 'None';
    if (fn && vn) return `${time(total)} (${time(fn).replace(' s','')} fixed + ${time(vn).replace(' s','')} variable)`;
    if (fn) return `${time(fn)} fixed`;
    return `${time(vn)} variable`;
  }

  function delayAt(r,i,key) {
    if (!r.d) return null;
    if (!Array.isArray(r.d[key])) return 'None';
    return time(arrAt(r.d[key],i)) || 'None';
  }

  function summarize(max,getter,fallback) {
    const values=[];
    for (let i=0;i<Math.max(1,max||1);i++) {
      const value=getter(i);
      if (value!=null) values.push(String(value));
    }
    if (!values.length) return fallback;
    const unique=[...new Set(values)];
    return unique.length===1 ? unique[0] : 'Variable';
  }

  function install(client) {
    const rows=Object.values(client);
    const byAegis=new Map(rows.map(x=>[x.a,x]));
    const byName=new Map(rows.map(x=>[norm(x.n),x]));
    window.RZ_OFFICIAL_CLIENT_SKILLS=client;

    const clientForSkill=sk => {
      if (!sk) return null;
      const aegis=SLUG_AEGIS[sk.id];
      return (aegis && byAegis.get(aegis)) || byName.get(norm(sk.name)) || null;
    };
    window.RZ_CLIENT_SKILL_FOR=clientForSkill;

    function applyData() {
      const root=window.RO_DATA;
      if (!root || !Array.isArray(root.skills)) return false;

      const idToWiki=new Map();
      for (const sk of root.skills) {
        const r=clientForSkill(sk);
        if (r) idToWiki.set(Number(r.id),sk);
      }

      for (const sk of root.skills) {
        const r=clientForSkill(sk);
        if (!r) continue;
        const max=r.m || sk.maxLevel || 1;

        sk.clientId=r.id;
        sk.clientAegis=r.a;
        sk.maxLevel=max;
        if (r.sp) sk.spCost=summarize(max,i=>arrAt(r.sp,i),sk.spCost);
        if (r.r) sk.range=summarize(max,i=>arrAt(r.r,i),sk.range);
        sk.castTime=summarize(max,i=>castAt(r,i),sk.castTime);
        sk.castDelay=summarize(max,i=>delayAt(r,i,'gd'),sk.castDelay);
        sk.cooldown=summarize(max,i=>delayAt(r,i,'cd'),sk.cooldown);

        if (r.de) {
          sk.description=sk.description && typeof sk.description==='object' ? sk.description : {};
          sk.description.en=r.de;
          sk.description.fr=r.df || r.de;
        }

        const job=JOB_BY_CLASS[sk.classId];
        const prereqs=(r.po && job!=null && r.po[String(job)]) || r.p;
        if (Array.isArray(prereqs)) {
          const mapped=prereqs.map(([id,level])=>{
            const dep=idToWiki.get(Number(id));
            return dep ? {skillId:dep.id,level:Number(level),verified:true} : null;
          }).filter(Boolean);
          if (mapped.length===prereqs.length) sk.prerequisites=mapped;
        }

        sk.noteList=SKILL_NOTES[sk.id] || [];
        sk.verified=true;
      }
      return true;
    }

    function currentSkill() {
      const match=location.hash.match(/^#\/skills\/([^/?#]+)/);
      if (!match || !window.RO_DATA) return null;
      const id=decodeURIComponent(match[1]);
      return (window.RO_DATA.skills||[]).find(x=>x.id===id || (id==='frost-driver' && x.id==='frost-diver')) || null;
    }

    function patchInfobox(sk,r) {
      const table=document.querySelector('aside.infobox table');
      if (!table) return;
      const max=r.m || sk.maxLevel || 1;
      const vals={
        max:String(max),
        sp:summarize(max,i=>arrAt(r.sp,i),'—'),
        range:summarize(max,i=>arrAt(r.r,i),'—'),
        cast:summarize(max,i=>castAt(r,i),'—'),
        delay:summarize(max,i=>delayAt(r,i,'gd'),'—'),
        cd:summarize(max,i=>delayAt(r,i,'cd'),'—')
      };
      for (const tr of table.querySelectorAll('tr')) {
        const th=tr.querySelector('th'), td=tr.querySelector('td');
        if (!th || !td) continue;
        const label=norm(th.textContent);
        if (label.includes('maxlevel') || label.includes('niveaumax')) td.textContent=vals.max;
        else if (label.includes('spcost') || label.includes('coutsp')) td.textContent=vals.sp;
        else if (label==='range' || label==='portee') td.textContent=vals.range;
        else if (label.includes('casttime') || label.includes('tempsdecast')) td.textContent=vals.cast;
        else if (label.includes('castdelay') || label.includes('delaiapreslancement') || label.includes('delaiaprescast')) td.textContent=vals.delay;
        else if (label.includes('cooldown') || label.includes('recharge')) td.textContent=vals.cd;
      }
    }

    function patchRendered() {
      const sk=currentSkill();
      if (!sk) return;
      const r=clientForSkill(sk);
      if (r) patchInfobox(sk,r);
    }

    let frameA=0, frameB=0;
    function schedulePatch() {
      if (frameA) cancelAnimationFrame(frameA);
      if (frameB) cancelAnimationFrame(frameB);
      frameA=requestAnimationFrame(()=>{ frameB=requestAnimationFrame(patchRendered); });
    }

    if (applyData()) {
      try { window.dispatchEvent(new HashChangeEvent('hashchange')); }
      catch (_) { window.dispatchEvent(new Event('hashchange')); }
      schedulePatch();
    }

    window.addEventListener('hashchange',schedulePatch);
  }

  fetch('assets/client-data/skills.json')
    .then(r=>{if(!r.ok) throw new Error('client skill data '+r.status); return r.json();})
    .then(install)
    .catch(err=>console.error('[RZ client sync]',err));
})();
