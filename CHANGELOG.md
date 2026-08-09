# Changelog

## 0.21.2 - 2026-08-09

- Qualification plus précise du site F1ZUG de Châtillon-en-Vendelais : l'APRS `F1ZUG-4` reste sur 144.800 MHz et une publication ARA35 de juin 2024 confirme séparément la présence d'un transpondeur pour le réseau ADRASEC 35.
- Ajout d'un garde-fou interdisant de déduire la fréquence du transpondeur ADRASEC 35 de la fréquence APRS ; cette fréquence reste à `null` tant qu'une source actuelle ne la publie pas.
- Ajout de `F5ZEB` / R71 Rennes Est à l'inventaire de recherche : entrée 431.075 MHz, sortie 438.675 MHz, CTCSS 71.9 Hz, de nouveau opérationnel depuis le 25 septembre 2025 et relié au R3 de Brocéliande ; candidature RX maintenue à `false` en attente de revue de couverture et de redondance.
- Ajout de `F5ZPV` / RU19 Rennes-Beaulieu comme relais documenté mais temporairement arrêté selon la page ARA35 actuelle : sortie 439.875 MHz, entrée 430.475 MHz, CTCSS 71.9 Hz, FM/C4FM ; aucun retour parmi les candidats actifs sans confirmation de redémarrage.
- Mise à jour de `research/bretagne-v0.1/emergency-relays.json`, du README et du document Sprint 29 ; renforcement des tests secours/ADRASEC et Mortain/Bretagne.
- Les recherches ADRASEC 22/29 restent volontairement ouvertes faute de source départementale assez précise pour attribuer un relais sans spéculation.
- État public inchangé : Normandie v0.3.1 reste figée à 139 mémoires, Annecy–Alpes–Léman v0.2 reste figé à 65/48 mémoires et Bretagne reste non publique.

## 0.21.1 - 2026-08-09

- Validation primaire DIRM NAMO du début de compétence du CROSS Étel à la Pointe de Penmarc'h, jusqu'à la frontière espagnole ; l'interface Finistère Sud n'est plus laissée entièrement indéterminée.
- Ajout des émetteurs météo Bretagne explicitement publiés par le CROSS Étel : Penmarc'h, Groix et Belle-Ile sur le canal 80, Étel sur le canal 63 en diffusion continue.
- Maintien de CROSS Corsen en inventaire primaire en attente : la page DIRM confirme le réseau VHF/MHF et les diffusions depuis des stations littorales mais n'énumère pas les sites/canaux dans la source exploitée.
- Conservation prudente du canal 64 comme donnée réglementaire de recherche : le ministère mentionne 63/64 en diffusion permanente dans le Morbihan, tandis que le planning CROSS Étel exploité n'identifie pas d'émetteur Bretagne sur 64 ; aucun site n'est inventé.
- Mise à jour de `research/bretagne-v0.1/public-maritime-radio.json`, `maritime-zones.json`, `publication-gates.json` et du README de recherche Bretagne sans publier de mémoire.
- Renforcement de `tests/test_mortain_bretagne_radio_research.py`, `tests/test_bretagne_research_scaffold.py` et `tests/test_site_files.py` pour figer Penmarc'h/Groix/Belle-Ile/Étel tout en maintenant Corsen et le canal 64 à l'état de recherche.
- F6ZES Sourdeval reste volontairement sans fréquence ni mode : aucune seconde source actuelle suffisamment précise n'a été trouvée.
- État public inchangé : Normandie v0.3.1 reste figée à 139 mémoires, Annecy–Alpes–Léman v0.2 reste figé à 65/48 mémoires et Bretagne reste non publique.

## 0.21.0 - 2026-08-09

- Ajout de `research/normandie-v0.4/mortain-bocage-coverage.json` pour classer les infrastructures selon leur pertinence réelle autour de Mortain-Bocage / Sud-Manche, avec étude volontaire des départements 50, 35, 53 et 61.
- Confirmation de l'existence actuelle de F6ZES à Sourdeval, du responsable F1SMB, du locator `IN98MR93XV` et de l'altitude 230 m, tout en laissant fréquence et mode à `null` faute de seconde source actuelle suffisamment précise.
- Ajout de la règle `sourdeval_must_not_be_guessed` afin d'empêcher toute fréquence inventée ou historique non recoupée dans Normandie v0.4.
- Classement de F5ZHY Montabot/Percy, F6ZCE Mont des Avaloirs et F1ZBX Brocéliande parmi les candidats analogiques utiles au secteur ; ajout de F5ZHA en étude de couverture.
- Conservation de F5ZIX Tessy-sur-Vire et F5ZPO Gorron comme métadonnées APRS sans dupliquer 144.800 MHz, exclusion du relais C4FM F1ZKC du profil analogique et exclusion de F5ZTQ arrêté.
- Ajout de `research/bretagne-v0.1/public-maritime-radio.json` à partir du tableau VHF maritime ANFR : canal 16 RX 156.800 MHz, canal 79 RX côte 161.575 MHz, canal 80 RX côte 161.625 MHz, canal 63 RX côte 160.775 MHz et canal 64 RX côte 160.825 MHz.
- Ajout de la règle RX-only selon laquelle une voie maritime duplex utilise la fréquence émise par la station côtière et reçue par le navire.
- Maintien des sites VHF déportés de CROSS Corsen et CROSS Etel à l'état `official_inventory_pending` : aucun site n'est inventé avant source primaire exploitable.
- Extension de l'inventaire Bretagne avec F5ZIS Matignon, F5ZIT Perros-Guirec, F1ZBZ Lorient et F5ZPE Bignan, sans déduire de rôle ADRASEC de leur seule implantation.
- Ajout de `tests/test_mortain_bretagne_radio_research.py` et de l'étape CI `Test Mortain and Bretagne public radio research`.
- Ajout de `SPRINT-29-MORTAIN-BRETAGNE-RADIO-RESEARCH.md`, mise à jour du README au Sprint 29 et renforcement du garde-fou général.
- État public inchangé : Normandie v0.3.1 reste figée à 139 mémoires, Annecy–Alpes–Léman v0.2 reste figé à 65/48 mémoires et Bretagne reste non publique.

## 0.20.0 - 2026-08-09

- Ajout de `research/emergency-radio-policy.json` pour distinguer les relais radioamateurs/ADRASEC et services publics éligibles des réseaux opérationnels PPDR/PMR privés qui restent hors publication.
- Ouverture de `research/normandie-v0.4/` sans modifier Normandie v0.3.1, avec priorité Mortain-Bocage / Sud-Manche et contrôle de la couverture utile dans les départements voisins 35, 53 et 61.
- Ajout des premiers candidats Normandie v0.4 : F5ZHY Montabot/Percy, F6ZES Sourdeval à revalider, F6ZCE Mont des Avaloirs, F1ZBX Brocéliande et plusieurs infrastructures Manche conservées selon leur pertinence réelle.
- Classement des relais uniquement numériques comme métadonnées lorsqu'ils ne sont pas utiles au profil RX analogique cible.
- Ouverture de `research/annecy-alpes-leman-v0.3/` sans modifier Annecy–Alpes–Léman v0.2.
- Réouverture de F1ZJV Pointe des Brasses comme candidat analogique ADRASEC 74, conservation de F1ZYT Semnoz comme métadonnée sur la même fréquence de sortie et ajout des candidats ADRASEC 73 F1ZHG / F5ZGT.
- Ajout de `research/bretagne-v0.1/emergency-relays.json` avec inventaire initial ADRASEC 22/29/35/56, relais analogiques et digipeaters APRS, tout en conservant le zonage Bretagne Nord / Bretagne Sud.
- Ajout de la porte Bretagne `emergency_relay_inventory`, bloquante tant que les infrastructures secours radioamateur pertinentes ne sont pas inventoriées et zonées.
- Ajout de `tests/test_emergency_relay_research.py`, renforcement du test Bretagne et mise à jour du garde-fou général Sprint 28.
- Ajout de l'étape CI `Test emergency and ADRASEC research`, de `SPRINT-28-EMERGENCY-ADRASEC-RESEARCH.md` et mise à jour du README au Sprint 28.
- État public inchangé : Normandie v0.3.1 reste à 139 mémoires, Annecy–Alpes–Léman v0.2 à 65/48 mémoires et Bretagne reste non publique.

## 0.19.0 - 2026-08-09

- Découpage obligatoire de la recherche Bretagne en **Bretagne Nord / Manche Ouest**, **Bretagne Sud / Atlantique** et **zone de transition Finistère Sud**.
- Attribution du contexte opérationnel CROSS Corsen au nord / nord-ouest et CROSS Etel au sud, sans figer encore la frontière SAR exacte.
- Ajout de `research/bretagne-v0.1/maritime-zones.json` pour documenter le zonage, les stations VHF déportées à inventorier, la météo maritime et les relais radioamateurs par sous-zone.
- Ajout de la règle empêchant de dupliquer artificiellement le canal 16 uniquement pour changer le nom du CROSS ; le contexte CROSS restera une métadonnée de zone.
- Ajout d'une porte de publication `maritime_zoning` qui reste bloquante tant que la limite SRR actuelle Corsen / Etel et les couvertures VHF ne sont pas précisément confirmées.
- Extension du registre Bretagne à dix sources officielles ou opérationnelles, toutes avec `frequency_data_promoted: false`.
- Ajout du contexte météo officiel : annonces via le canal 16 avant diffusion sur 79/80 et diffusion permanente 63/64 notamment dans le Morbihan, sans promotion de fréquence dans le pack.
- Renforcement de `tests/test_bretagne_research_scaffold.py` et `tests/test_site_files.py` pour imposer le zonage nord/sud et empêcher toute publication prématurée.
- Ajout de `SPRINT-27-BRETAGNE-MARITIME-ZONING.md` et mise à jour du README au Sprint 27.
- Les packs publics restent inchangés : Annecy–Alpes–Léman v0.2 à 65/48 mémoires et Normandie v0.3.1 figée à 139 mémoires.

## 0.18.0 - 2026-08-09

- Choix de la Bretagne comme troisième région de travail de RadioPack France.
- Initialisation de `research/bretagne-v0.1/` à partir du starter régional sécurisé.
- Création de `README.md`, `pack-plan.json`, `source-registry.json`, `publication-gates.json` et `memory-plan.json` pour Bretagne.
- État initial strictement recherche : zéro fréquence retenue, aucun nombre cible de mémoires, aucun bloc mémoire et tous les droits de publication désactivés.
- Ajout de cinq sources institutionnelles de départ sans promotion de fréquence : SIA Brest-Bretagne LFRB, SIA Rennes-Saint-Jacques LFRN, ANFR Open Data, missions radioamateurs ANFR et annuaire radioamateurs ANFR.
- Ajout de la règle explicite `seed_source_does_not_equal_validated_frequency` : une source identifiée ne vaut pas validation d'une fréquence.
- Ajout de `tests/test_bretagne_research_scaffold.py` pour interdire toute apparition prématurée de Bretagne dans `packRegistry.ts`, `regions.json`, les pages ou les téléchargements publics.
- Ajout de l'étape CI `Test Bretagne research scaffold`.
- Ajout de `SPRINT-26-BRETAGNE-INITIALIZATION.md` et mise à jour du README au Sprint 26.
- Annecy–Alpes–Léman v0.2 reste publié à 65/48 mémoires et Normandie v0.3.1 reste figée à 139 mémoires.

## 0.17.0 - 2026-08-09

- Ajout de `tools/create_regional_pack.py` pour initialiser un espace de recherche régional sans créer de contenu public.
- Génération automatique de `README.md`, `pack-plan.json`, `source-registry.json`, `publication-gates.json` et `memory-plan.json` sous `research/<slug>-v<version>/`.
- État initial volontairement vide : aucune fréquence, aucun bloc mémoire et aucun nombre cible de mémoires ne sont imposés.
- Tous les drapeaux de publication commencent à `false` ; aucune page Astro, route CSV ou entrée `packRegistry.ts` n'est créée par le starter.
- Application immédiate des règles permanentes RX-only, `Duplex=off`, `Offset=0.000000`, noms ≤ 10 caractères, maximum 200 mémoires, pas de remplissage artificiel et immutabilité des versions publiées.
- Refus d'écraser un espace de recherche existant et validation stricte des slugs et versions.
- Ajout de `tests/test_regional_pack_starter.py`, exécuté sous racine temporaire afin de vérifier l'absence d'effet de bord sur le registre public et les régions publiées.
- Ajout de l'étape CI `Test regional pack research starter`, de `SPRINT-25-REGIONAL-STARTER.md` et mise à jour du README au Sprint 25.

## 0.16.0 - 2026-08-09

- Ajout de l'option `--output-root` au générateur Python afin de produire les CSV dans une racine de sortie séparée du dépôt source.
- Modification de `tests/test_generator.py` pour utiliser un répertoire temporaire système au lieu de réécrire `website/public` pendant les tests.
- Comparaison des sorties temporaires génériques avec les CSV publics suivis et vérification finale que les fichiers suivis n'ont changé d'aucun octet.
- Identification d'une dérive historique de Normandie v0.3.1 : les fréquences et positions restent identiques, mais les commentaires ISS nationaux ont été enrichis après la publication de cette version.
- Classement de Normandie v0.3.1 comme artefact versionné figé : le générateur générique ne la reconstruit plus et une évolution devra produire une nouvelle version régionale.
- Ajout de la règle générale d'immutabilité des packs régionaux publiés dans `REGIONAL-PACK-WORKFLOW.md`.
- Renommage de l'étape CI en `Test CSV generator in isolated output` et ajout de garde-fous contre la reconstruction accidentelle d'une version régionale figée.
- Ajout de `SPRINT-24-ISOLATED-GENERATOR-TESTS.md` et mise à jour du README au Sprint 24.

## 0.15.0 - 2026-08-09

- Passage du générateur public `/generateur` à une architecture multi-régions avec sélecteur de pack.
- Ajout du registre `website/src/lib/packRegistry.ts`, source de vérité des packs et variantes téléchargeables.
- Enregistrement d'Annecy–Alpes–Léman v0.2 avec ses variantes 65 mémoires et 48 mémoires sans aviation.
- Enregistrement de Normandie v0.3.1 comme variante publique fixe de 139 mémoires, sans modification de ses fréquences.
- Masquage automatique des options non prises en charge : Aviation et NOTAM restent propres au pack Annecy.
- Maintien du téléchargement direct des ressources publiques validées, sans génération de Blob CSV côté navigateur.
- Passage du contrat `generator/options.json` au schéma 3.0 `multi_region_public_generator`.
- Extension de `REGIONAL-PACK-WORKFLOW.md` avec l'étape obligatoire d'enregistrement dans le catalogue public.
- Ajout de `tests/test_pack_registry.py` pour valider le registre, les variantes et le CSV Normandie.
- Ajout de `tests/test_built_public_pack_catalog.py` pour contrôler après `astro build` les fichiers Annecy 65/48 et Normandie 139 réellement déployés.
- Mise à jour des tests AIRAC et readiness afin de conserver leurs validations métier tout en adoptant le nouveau contrat multi-régions.
- Mise à jour du README au Sprint 23 et de la CI pour vérifier le sélecteur, le registre et les trois CSV publics.

## 0.14.0 - 2026-08-09

- Revue finale ligne par ligne du candidat Annecy–Alpes–Léman v0.2 : 65/65 mémoires figées par carte de référence, avec variante 48 mémoires sans aviation.
- Validation automatique des emplacements, noms, fréquences, modes, pas, `Duplex=off`, `Offset=0.000000` et empreintes des commentaires.
- Ajout puis activation du générateur web `/generateur` avec option aviation et contrôle NOTAM facultatif/non bloquant.
- Publication explicite d'Annecy–Alpes–Léman v0.2 avec deux routes CSV Astro prérendues : 65 mémoires avec aviation et 48 sans aviation.
- Ajout d'un contrôle CI de bout en bout qui ouvre les CSV réellement produits dans `website/dist` et les compare à la carte de revue.
- Correction de l'interaction de la case « J'ai vérifié les NOTAM applicables » afin qu'elle reste indépendante du simple rafraîchissement du résumé.
- Simplification du générateur : le navigateur sélectionne désormais directement l'une des deux routes CSV validées au lieu de reconstruire un Blob CSV côté client.
- Ajout de liens directs vers SOFIA-Briefing et Skybriefing dans la section NOTAM du générateur.
- Extraction d'un moteur générique `website/src/lib/chirpPack.ts` pour réutiliser les règles CHIRP sur les futurs packs régionaux ; `annecyPack.ts` devient un wrapper spécifique au pack.
- Ajout de `REGIONAL-PACK-WORKFLOW.md` décrivant la méthode de création, revue, test et publication d'une nouvelle région.
- Retrait du dépôt actif des anciens fichiers Annecy/Haute-Savoie v0.1 : manifeste, données aviation/relais, CSV régional, CSV relais et guide PDF.
- Ajout de redirections permanentes pour les anciennes URL v0.1 afin d'éviter les liens morts tout en conservant l'historique dans Git.
- Mise à jour du README au Sprint 22 et extension des garde-fous CI pour empêcher le retour des fichiers v0.1 ou d'une génération divergente.

## 0.13.0 - 2026-08-08

- Reclassement des contrôles NOTAM France et Suisse en vérifications facultatives et non bloquantes pour les packs d'écoute RX.
- Ajout du contrat `generator/options.json` avec deux options indépendantes : inclusion de l'aviation et état du contrôle NOTAM.
- Ajout de `tools/check_annecy_release_readiness.py` pour distinguer les portes bloquantes des contrôles informatifs.
- Recontrôle officiel AMSAT de SO-50, AO-91 et AO-123 ; passage de `dynamic_satellites` à `passed_official_amsat_recheck`.
- Passage d'Annecy–Alpes–Léman v0.2 à l'état prêt pour la prépublication, tout en maintenant l'absence de téléchargement public.
- Ajout de `tools/build_annecy_prepublication.py`, backend de génération hors `website/public`.
- Génération contrôlée de deux variantes : 65 mémoires avec aviation et 48 mémoires sans aviation, sans renumérotation artificielle des autres blocs.
- Le choix NOTAM est enregistré dans le manifeste de génération mais ne modifie jamais automatiquement les fréquences du CSV.
- Ajout de `tests/test_annecy_prepublication.py` et exécution automatique dans la CI.
- Mise à jour systématique du `README.md` avec l'état courant du projet et ajout d'un garde-fou CI correspondant.
- Ajout de l'exclusion Git globale de `__pycache__/` et `*.py[cod]`.
- Le CSV public Annecy–Alpes–Léman v0.2 reste volontairement absent jusqu'à la revue finale explicite.

## 0.12.0 - 2026-08-08

- Clôture conservatrice du périmètre aviation Annecy–Alpes–Léman v0.2 sans ajout artificiel de fréquences.
- Reclassement d'Albertville LFKA et Megève LFHM en `excluded_scope_unverified_primary` : VAC primaires identifiées au catalogue SIA, mais blocs radio non extractibles de façon suffisamment fiable dans ce workflow.
- Reclassement de Genève LSGG en `excluded_scope_unverified_primary` : l'aéroport et le cycle courant sont documentés officiellement, mais le tableau radio opérationnel primaire courant n'est pas suffisamment extractible ici.
- Aucune fréquence provenant uniquement d'une source secondaire n'est intégrée au candidat.
- Passage de la porte `pending_airfields` à `passed_scope_closed`, avec liste d'attente vide et omissions documentées LFKA/LFHM/LSGG/LFHZ.
- Maintien du candidat interne à 65 mémoires, toutes en réception seule avec `Duplex=off`.
- Maintien de `public_release_allowed: false` : briefing NOTAM France, briefing NOTAM Suisse et recontrôle satellites restent requis au moment de la publication.
- Rafraîchissement du registre de sources et extension des tests pour empêcher la réintroduction accidentelle des terrains exclus.
- Aucun changement des téléchargements publics Annecy, du générateur public ou du statut « En préparation ».

## 0.11.0 - 2026-08-08

- Validation primaire des quatre fréquences Chambéry Aix-les-Bains dans le tableau officiel SIA AD 2.18 : 123,700 MHz, 121,205 MHz, 118,300 MHz et 127,100 MHz.
- Promotion de `CHAM-INFO`, `CHAM-APP`, `CHAM-TWR` et `CHAM-ATIS` au statut `verified_airac08_public`.
- Passage du bloc aviation France / bassin genevois de 7 à 11 mémoires et du candidat interne de 61 à 65 mémoires.
- Réduction de la porte `pending_airfields` à Albertville LFKA, Megève LFHM et Genève LSGG.
- Reclassement de LFKA et LFHM en `pending_primary_vac_frequency_extraction` : VAC courantes identifiées au SIA, mais aucune fréquence issue d'une source secondaire n'est promue sans extraction primaire fiable.
- Maintien de Genève-aéroport hors candidat tant que son tableau radio courant n'est pas recoupable sur une source primaire suffisamment précise.
- Extension des tests AIRAC et du candidat interne aux quatre mémoires Chambéry et à leurs positions 127 à 130.
- Aucun changement des téléchargements publics Annecy, du générateur public ou du statut « En préparation ».

## 0.10.0 - 2026-08-08

- Ajout de quatre fréquences aviation Sion recoupées sur le site officiel de l'aéroport : GND 121,705 MHz, TWR 118,275 MHz, ATIS 130,630 MHz et APP 126,825 MHz.
- Maintien hors candidat des fréquences de handling Sion 131,475 / 131,670 / 131,955 MHz et des aides de radionavigation 110,7 / 112,15 MHz.
- Passage du bloc aviation Suisse de 2 à 6 mémoires et du candidat interne de 57 à 61 mémoires.
- Reclassement de Sallanches-Mont-Blanc LFHZ en `excluded_closed_aerodrome` : fermeture officielle à toute circulation aérienne effective depuis le 1er septembre 2020.
- Réduction de la liste aviation encore à recouper à Chambéry LFLB, Albertville LFKA, Megève LFHM et Genève LSGG.
- Ajout d'un fichier `aviation-operational-gates.json` séparant validation des fréquences et contrôles dynamiques de pré-publication.
- Maintien des portes NOTAM France (SOFIA-Briefing), NOTAM Suisse (Skybriefing) et statut satellites en attente d'un contrôle daté au moment de la publication.
- Extension des tests AIRAC et du candidat interne pour interdire la réintroduction de Sallanches, des fréquences Sion exclues et de toute donnée non validée.
- Aucun changement des téléchargements publics Annecy, du générateur public ou du statut « En préparation ».

## 0.9.0 - 2026-08-08

- Revalidation partielle du bloc aviation Annecy–Alpes–Léman sur le cycle AIRAC 08/26 effectif depuis le 6 août 2026.
- Ajout de sept mémoires aviation France / bassin genevois recoupées publiquement : Annecy-Meythet, Annemasse, Grenoble-Le Versoud, Grenoble-Alpes-Isère et Genève Information.
- Ajout de deux mémoires Lausanne-La Bléchette recoupées sur le site officiel de l'exploitant : 123,205 MHz et 118,830 MHz.
- Conservation du pré-inventaire AIRAC 07/26 comme historique, avec interdiction explicite de l'utiliser dans l'assembleur.
- Maintien hors candidat de Chambéry, Albertville, Megève, Sallanches, Genève-aéroport et Sion tant que les données courantes ne sont pas suffisamment recoupées publiquement.
- Passage du candidat interne de 48 à 57 mémoires, toutes en réception seule avec `Duplex=off`.
- Ajout du test `tests/test_annecy_airac08.py` et extension des tests du candidat interne aux blocs aviation.
- Aucun changement du générateur public, des téléchargements Annecy ou du statut « En préparation ».

## 0.8.0 - 2026-08-04

- Ajout de SO-50, AO-91 et AO-123 dans un inventaire satellite FM de recherche.
- Conservation exclusive des liaisons descendantes comme mémoires RX ; les montantes restent des métadonnées.
- Exclusion prudente de PO-101, CAS-3H, IO-86, RS95S et TEVEL2 du candidat interne.
- Finalisation d'un plan mémoire provisoire de 48 mémoires validées.
- Ajout d'un assembleur interne qui refuse l'aviation non revalidée, les lacs et les lignes suisses non confirmées.
- Génération locale d'un JSON et d'un CSV internes marqués `public_export_allowed: false` dans un dossier ignoré par Git.
- Ajout du test `tests/test_annecy_internal_candidate.py` et de son exécution dans GitHub Actions.
- Aucun changement du générateur public, des téléchargements Annecy ou du statut « En préparation ».

## 0.7.1 - 2026-08-04

- Correction de la modélisation des fréquences ISS en distinguant explicitement liaison montante et liaison descendante.
- Voix équipage en Région 1 : montée 145,200 MHz et descente mondiale 145,800 MHz.
- Répéteur vocal croisé : montée 145,990 MHz avec CTCSS 67 Hz et descente 437,800 MHz.
- Packet/APRS VHF sur 145,825 MHz dans les deux sens et UHF sur 437,825 MHz dans les deux sens lorsque ces modes sont actifs.
- Confirmation de 437,550 MHz comme fréquence descendante SSTV utilisée lors de campagnes ARISS 2026 ; certaines autres campagnes peuvent utiliser 145,800 MHz.
- Conservation exclusive des fréquences descendantes dans les mémoires RX publiques ; les montantes restent des métadonnées documentaires.
- Ajout de tests empêchant l'export de 145,200 MHz et 145,990 MHz comme mémoires de réception séparées.
- Régénération du CSV national APRS/ISS sans changement du nombre de mémoires.

## 0.7.0 - 2026-08-04

- Ajout d'un pré-inventaire aviation France de 11 fréquences uniques pour Annecy–Alpes–Léman v0.2.
- Organisation des fréquences d'Annecy, Annemasse, Chambéry, Grenoble-Le Versoud, Grenoble-Alpes-Isère et Genève Information.
- Marquage obligatoire de toutes les lignes aviation pour revalidation à partir de l'AIRAC 08/26 du 6 août 2026.
- Maintien d'Albertville, Megève et Sallanches en attente d'extraction officielle.
- Ajout des conclusions officielles sur la navigation des lacs d'Annecy, du Bourget et du Léman.
- Exclusion du plan maritime de 57 canaux, de l'AIS suisse et des réseaux professionnels concédés autour de 173 MHz.
- Conservation du canal 16 suisse comme cas conditionnel de recherche, sans intégration au pack public.
- Ajout du test `tests/test_annecy_aviation_lakes.py` et de son exécution dans GitHub Actions.
- Aucun changement du générateur public, des CSV, du PDF ou du statut « En préparation » de la v0.2.

## 0.6.0 - 2026-08-04

- Ajout de l'inventaire de recherche radioamateur France pour Annecy–Alpes–Léman v0.2.
- Recensement de 19 fréquences analogiques uniques dans l'Ain, l'Isère, la Savoie et la Haute-Savoie.
- Fusion de quatre fréquences partagées afin d'éviter les doublons dans le futur plan mémoire.
- Ajout d'un inventaire séparé de huit candidats suisses pour Genève, Vaud et Valais.
- Validation actuelle de HB9G 145,725 MHz et 439,100 MHz ; les autres candidats suisses restent en attente de recoupement.
- Confirmation des conflits F1ZJV et F1ZYT, maintenus hors production.
- Ajout du test `tests/test_annecy_research.py` et de son exécution dans GitHub Actions.
- Aucun changement du générateur public, des CSV ou du statut « En préparation » de la v0.2.

## 0.5.1 - 2026-08-04

- Reclassification publique d'Annecy & Haute-Savoie v0.1 comme aperçu historique incomplet.
- Retrait des liens directs vers les CSV et PDF Annecy v0.1 des pages publiques.
- Renommage de la prochaine zone en Annecy–Alpes–Léman.
- Passage du statut public à « En préparation » pour la future v0.2.
- Mise à jour de l'accueil, de la liste des régions, des téléchargements et de la page des versions.
- Adaptation du composant de carte régionale aux packs non disponibles.
- Ajout de contrôles empêchant la republication accidentelle des liens Annecy v0.1.
- Ajout d'une base de recherche structurée pour Annecy–Alpes–Léman v0.2.

## 0.5.0 - 2026-08-04

- Ajout des URL canoniques et des metadonnees Open Graph / Twitter.
- Ajout des donnees structurees WebSite en JSON-LD.
- Ajout du manifeste web et du lien de sitemap.
- Ajout des routes dynamiques `robots.txt` et `sitemap.xml`.
- Ajout d'une page 404 personnalisee compatible Cloudflare Pages.
- Ajout de la page publique "Etat des packs".
- Mise a jour du bouton principal du menu pour les deux regions disponibles.
- Ajout d'un menu mobile accessible.
- Ajout des en-tetes de securite et de cache Cloudflare Pages.
- Ajout de redirections permanentes pour les anciens téléchargements Normandie.
- Ajout d'une integration continue GitHub Actions pour tester les CSV et compiler Astro.
- Ajout d'un test automatique des fichiers de production.

## 0.4.0 - 2026-08-04

- Publication du premier pack Annecy & Haute-Savoie v0.1.0.
- Ajout de 36 memoires en reception seule.
- Ajout de l'aviation d'Annecy-Meythet et d'Annemasse.
- Ajout de neuf sorties analogiques uniques en Haute-Savoie, dans l'Ain et en Savoie.
- Regroupement des frequences de transpondeurs partagees afin d'eviter les doublons.
- Ajout du CSV regional, du CSV des relais et du guide PDF.
- Mise a jour de l'accueil, des regions, des telechargements, du generateur et des tests.

## 0.3.1 - 2026-08-04

- Ajout du relais F6ZCE de Pré-en-Pail / Mont des Avaloirs.
- Fréquence de sortie : 145,700 MHz, réception seule.
- Pack Normandie porté à 139 mémoires.
- Liste des relais portée à 15 mémoires.
- Mise à jour du site, des tests et du guide PDF.

## 0.3.0 - 2026-08-04

- Ajout des canaux d'appel FM 145,500 MHz et 433,500 MHz en reception seule.
- Ajout de 14 sorties de relais ou voies de transpondeurs analogiques verifies en Normandie.
- Organisation du pack par plages fixes de memoires.
- Pack Normandie porte a 138 memoires.
- Ajout d'un guide PDF telechargeable.
- Ajout d'un export CSV specifique aux relais analogiques normands.
- Mise a jour du generateur et des tests pour gerer les intervalles de memoires.

## 0.2.0 - 2026-08-04

- Ajout de la VHF marine, APRS/ISS et de l'aviation normande.
- Pack Normandie porte a 122 memoires.

## 0.1.0 - 2026-08-04

- Premiere base PMR446 et generateur CSV CHIRP.
