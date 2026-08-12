# Changelog

## 0.21.68 - 2026-08-12

- **Sprint 79** : revue de maturité Bretagne v0.2 et gel du périmètre à **151 mémoires RX**.
- Checklist de prépublication portée à **10/10**, **0 bloqueur**, `prepublication_ready=true` ; aucune publication effectuée.
- AIRAC 08/26 recontrôlé comme cycle courant au 12 août 2026, valable jusqu'au 2 septembre 2026 inclus ; aucune comparaison XML champ par champ non effectuée n'est revendiquée.
- F1ZUG/ADRASEC35, mappings locaux CROSS Ch64/Ch79 et F5ZPV/F5ZZH/F5ZZC-4 sont explicitement reportés hors du scope figé et classés non bloquants.
- Ajout de `maturity-review.json`, `release-scope.json`, `review-checklist.json`, `publication-gates.json`, de l'audit v0.2 reproductible et du garde-fou Sprint 79.
- Le CSV public et le registre restent sur Bretagne v0.1 ; la publication v0.2 nécessite un sprint séparé explicite.

## 0.21.67 - 2026-08-12

- **Sprint 78** : revalidation des mappings locaux CROSS Étel Ch64 et Corsen Ch79 ; Bretagne v0.2 reste à **151 mémoires RX**, delta RF **0**.
- Étel : affirmation ministérielle régionale 63/64 conservée, mais la documentation opérationnelle actuelle associe explicitement Étel à Ch63 ; aucun site Ch64 n'est promu et le conflit primaire reste ouvert.
- Corsen : réseau VHF/MHF actuel confirmé sans mapping primaire actuel Ch79 → site ; Fréhel/Bodic/Batz/Stiff/Raz restent des pistes non promotables.
- Guide Marine 2026 identifié comme référence primaire mais non extractible dans le workflow ; aucune preuve négative ni attribution n'en est déduite.
- Ajout de `cross-local-mapping-revalidation.json` et du garde-fou Sprint 78 ; aucune mutation publique Bretagne v0.2.

## 0.21.66 - 2026-08-12

- **Sprint 77** : revalidation publique ADRASEC Bretagne (22/29/35/56), candidat Bretagne v0.2 maintenu à **151 mémoires RX**, delta RF **0**.
- ADRASEC 29 : F1ZBH-3 et F1ZGQ-3 recoupés publiquement sur APRS 144.800 MHz, déjà présent dans le bloc national ; aucune duplication.
- ADRASEC 35 : F1ZUG APRS 144.800 MHz reste distinct du transpondeur ADRASEC 35 dont la fréquence n'est pas publiée.
- ADRASEC 56 : activité publique confirmée sans fréquence de service ADRASEC actuelle distincte promue ; association historique de F1ZKU non transformée en rôle courant.
- ADRASEC 22 : appartenance FNRASEC confirmée, sans fréquence actuelle explicitement attribuée dans le périmètre public retenu.
- Données opérationnelles privées et PPDR explicitement exclues ; ajout du garde-fou Sprint 77 à la CI.

## 0.21.65 - 2026-08-12

- **Sprint 76** : revalidation des infrastructures radioamateur Bretagne v0.2, candidat maintenu à **151 mémoires RX**, delta RF **0**.
- F1ZBZ résolu sans nouvelle RF car les cinq valeurs utiles sont déjà représentées ; F5ZPV/F5ZZH restent arrêtés selon l'opérateur local ; F5ZZC-4 reste sans fréquence actuelle validée.
- Ajout de `amateur-infrastructure-revalidation.json` et du garde-fou Sprint 76.

## 0.21.64 - 2026-08-12

- **Sprint 75** : Bretagne v0.2 passe de 135 à **151 mémoires RX** avec **16 mémoires aviation** AIRAC 08/26 aux positions 130–145.
- Rennes, Brest, Dinard, Quimper et 121.500 MHz urgence sont intégrés au candidat interne RX-only ; positions 146–149 laissées libres.
- Aucun CSV public v0.2 ni changement de registre ; Bretagne v0.1 reste immuable à 135.

## 0.21.63 - 2026-08-12

- **Sprint 74** : initialisation de Bretagne v0.2 en recherche à partir de Bretagne v0.1 immuable = **135 mémoires RX**.
- Six dossiers de backlog créés : aviation, ADRASEC public, F1ZUG/ADRASEC35, CROSS Étel Ch64, CROSS Corsen Ch79 et infrastructures radioamateur ambiguës/arrêtées.
- Candidat initial 135, delta 0, aucune publication v0.2.

## 0.21.62 - 2026-08-12

- **Sprint 73** : publication de **Bretagne v0.1 à 135 mémoires RX** et gel immuable de cette version.
- Le CSV public correspond octet pour octet au candidat interne figé/revu au Sprint 72 ; SHA-256 enregistré dans `research/bretagne-v0.1/publication-record.json`.
- Registre public, générateur, page Bretagne, téléchargements, versions, carte et sitemap mis à jour pour le troisième pack régional public.
- Ch64 (156.225 / 160.825 MHz) et Ch79 (156.975 / 161.575 MHz) restent deux paires RX génériques, sans attribution locale de site non prouvée.
- Aviation AIRAC courante, fréquences opérationnelles ADRASEC non publiées, mappings locaux CROSS et infrastructures amateur arrêtées/non résolues restent différés à Bretagne v0.2.
- Les artefacts de prépublication Sprint 72 restent historiques ; la publication est enregistrée séparément et les garde-fous postpublication vérifient l'identité exacte du CSV.
- Ajout des tests de publication Bretagne et du garde-fou Sprint 73 dans la CI.

## 0.21.61 - 2026-08-12

- **Sprint 72** : clôture de périmètre Bretagne v0.1 à **135 mémoires RX** et passage en prépublication, toujours non publique.
- Revue Bretagne portée à **8/8**, **0 blocage** pour le périmètre figé, audit prépublication reproductible et candidat inchangé à 135.
- Le cycle SIA courant **AIRAC 08/26** (06/08/2026–02/09/2026) est enregistré comme frontière de fraîcheur ; l'aviation est reportée à v0.2 plutôt que de promouvoir des fréquences exactes d'un cycle antérieur.
- Fréquences opérationnelles ADRASEC non publiées, mappings locaux CROSS Ch64/Ch79 et infrastructures arrêtées/non résolues sont différés sans inférence négative.
- Ch64 et Ch79 restent présents génériquement en deux mémoires RX chacun ; aucun site émetteur local n'est revendiqué.
- Ajout de `release-scope.json`, `review-checklist.json`, `sia-airac-08-review.json`, du snapshot/audit Bretagne et des garde-fous Sprint 72.
- Aucun CSV public Bretagne, registre public ou route publique ajouté.

## 0.21.60 - 2026-08-11

- **Sprint 71** : revalidation Normandie v0.5 sans promotion ; candidat maintenu à 142 mémoires.
- Bretagne v0.1 passe du plan mémoire vide à un **candidat interne de 135 mémoires RX**, toujours non public.
- Composition Bretagne : 16 PMR446 + 90 VHF maritime + 6 écoutes amateur + 2 appels amateur + 21 mémoires régionales uniques après déduplication.
- Ch64 (156.225 / 160.825 MHz) et Ch79 (156.975 / 161.575 MHz) sont présents en deux mémoires RX génériques chacun, sans attribution de site Étel/Corsen non prouvée.
- Aviation Bretagne maintenue à 0 mémoire, emplacements 130–149 réservés en attente d'une extraction SIA actuelle.
- Ajout du builder `tools/build_bretagne_internal_candidate.py` et des garde-fous Sprint 71 ; aucun fichier public Bretagne ajouté.

## 0.21.59 - 2026-08-11

- **Sprint 70** : initialisation de Normandie v0.5 en recherche sur la base publique immuable v0.4 = 142 mémoires.
- Backlog v0.5 créé pour R3/F1ZBX, F5ZHA, F1ZOV et F6ZES, sans validation implicite ni ajout RF.
- R3 reste une paire de 2 mémoires potentielles avec 2 sessions terrain comme preuves ; F6ZES reste strictement sans conjecture.
- Ajout de `tests/test_normandie_v05_initialization.py` et mise à jour du point de reprise.

## 0.21.58 - 2026-08-11

- **Sprint 69** : publication de **Normandie v0.4 à 142 mémoires RX**.
- Le CSV public v0.4 correspond exactement au candidat revu ; la v0.3.1 à 139 mémoires reste intacte et immuable.
- Registre public, générateur et pages du site basculés vers Normandie v0.4.
- Ajout de `research/normandie-v0.4/publication-record.json` et `tests/test_normandie_v04_public_release.py`.
- R3/F1ZBX, F5ZHA, F1ZOV et F6ZES restent exclus de v0.4 et reportés à v0.5.

## 0.21.57 - 2026-08-11

- **Sprint 68** : clôture de périmètre Normandie v0.4 à **142 mémoires RX**.
- Revue v0.4 portée à **9/9**, blocages de prépublication à **0**, audit d'intégrité **OK** et dry-run activation-ready avec baseline propre.
- R3/F1ZBX, F5ZHA, F1ZOV et F6ZES reportés explicitement à Normandie v0.5, sans validation implicite ni ajout RF.
- Aucun fichier public v0.4 ni registre public modifié dans ce sprint ; v0.3.1 reste immuable.
- Ajout de `release-scope.json`, `review-baseline.json` et du garde-fou `test_sprint68_scope_closure.py`.

## 0.21.56 - 2026-08-11

- **Sprint 67** : synthèse des références courantes sans promotion ni mutation publique.
- Le Guide ministériel des loisirs nautiques en mer **édition 2026** a été extrait et contrôlé : 79/80 et 63/64 sont confirmés au niveau canal, mais aucun site émetteur Ch64/Ch79 n'est nommé.
- Ch79 : convergence secondaire renforcée autour de Fréhel/Bodic/Stiff et de la chaîne Fréhel/Bodic/Batz/Stiff/Raz ; les infrastructures primaires actuelles de Fréhel/Stiff ne transforment pas ces indices en mapping primaire.
- F5ZHA : la fiche RepeaterBook 431.4125 affiche un indicateur vert tandis que la provenance de vérification reste `2017-02-17` / `Off-Air`; le badge courant n'écrase pas la provenance datée et la réconciliation autoritative reste ouverte.
- F6ZES et R3 inchangés ; R3 reste à 2 mémoires RX si promotion et 2 sessions terrain de preuve.
- Ajout de `research/sprint-67-current-reference-synthesis.json`, `research/sprint-67-summary.md` et `tests/test_sprint67_current_reference_synthesis.py`, avec intégration CI et garde-fous historiques adaptés.
- Passage du point de reprise au **Sprint 67 / 0.21.56** ; état Normandie v0.4 inchangé à **142**, plafond 147, revue **3/9**, **6 blocages**, **0 ajout éligible**.
- État public inchangé : Normandie v0.3.1 **139**, Annecy–Alpes–Léman v0.2 **65/48**, Bretagne non publique.

## 0.21.55 - 2026-08-11

- **Sprint 66** : recontrôle des inventaires techniques capables de relier stations et canaux, sans abaisser les portes de publication.
- CROSS Étel : l'offre DIRM `2026-2341297` confirme **17 stations radio** maintenues de Penmarc'h à Biarritz dans un contexte MHF/VHF, mais sans noms de stations ni canaux ; Ch64 reste sans site attribué.
- CROSS Corsen : Stiff/Ouessant reste revalidé comme infrastructure radio actuelle ; le marché `DGAMPA-SNC1-2025-03_STIFF` confirme un projet de rénovation 2026 sans mapping Ch79. Une source secondaire non datée restitue Fréhel/Bodic/Batz/Stiff/Raz sur Ch79 mais reste une piste, pas une validation primaire actuelle.
- F5ZHA : ARAM53 est identifiable comme association active, mais aucune publication technique locale actuelle exploitée ne valide la paire ; l'existence associative ne ferme pas le conflit. F6ZES reste sans fréquence/mode/état exploitable.
- Guide Marine 2026 : nouvelle tentative de lecture toujours en `cache miss`; aucune inférence Ch64/Ch79 depuis un PDF non lu.
- Mise à jour de `corsen-channel79-evidence.json` (schéma 1.2) et `etel-channel64-evidence.json` (schéma 1.1), ajout de `research/sprint-66-technical-inventory-boundaries.json` et `research/sprint-66-summary.md`.
- Ajout de `tests/test_sprint66_technical_inventory_boundaries.py`, intégration CI, passage du point de reprise au **Sprint 66 / 0.21.55** et maintien des anciens tests comme garde-fous historiques.
- État Normandie v0.4 inchangé : **142 mémoires**, preview 142, plafond 147, revue **3/9**, **6 blocages**, **0 ajout éligible**.
- État public inchangé : Normandie v0.3.1 **139**, Annecy–Alpes–Léman v0.2 **65/48**, Bretagne non publique.

## 0.21.54 - 2026-08-11

- **Sprint 65** : recontrôle daté des sources primaires encore utiles à F5ZHA/F6ZES et aux dossiers CROSS Étel Ch64 / Corsen Ch79, sans promotion ni mutation publique.
- Ajout de `research/sprint-65-primary-recheck.json` : F5ZHA reste affiché actif par le REF sur **145.4675 / 432.575 MHz**, mais la réconciliation locale/autoritative et le terrain Mortain restent requis ; F6ZES reste sans fréquence, mode ni état exploitable.
- Revalidation primaire Bretagne : la page ministérielle mise à jour le **19 juin 2026** maintient Ch79/80 pour les diffusions CROSS et Ch63/64 en diffusion permanente notamment dans le Morbihan, sans nommer de site Ch64.
- Les pages DIRM courantes maintiennent **Étel + Chassiron sur Ch63** et le réseau VHF/MHF côtier de **CROSS Corsen**, sans fournir respectivement de site Ch64 ni de mapping Ch79 ↔ station.
- Ajout des garde-fous `current_regional_channel_statement_does_not_identify_transmitter_site` et `current_cross_network_statement_does_not_map_channel_to_station` ; infrastructure, réseau et déclaration régionale ne valent jamais affectation automatique de canal/site.
- Le Guide Marine 2026 reste identifié mais non extractible dans le workflow (`cache miss`) ; aucune inférence Ch64/Ch79 n'en est tirée.
- Ajout de `tests/test_sprint65_primary_recheck.py`, intégration CI et mise à jour de `README.md`, `PROJECT_STATUS.md`, `research/project-resume-state.json` et des garde-fous de reprise au **Sprint 65 / 0.21.54**.
- État Normandie v0.4 inchangé : **142 mémoires**, preview 142, plafond 147, revue **3/9**, **6 blocages**, **0 ajout éligible**.
- État public inchangé : Normandie v0.3.1 **139**, Annecy–Alpes–Léman v0.2 **65/48**, Bretagne non publique.

## 0.21.53 - 2026-08-11

- **Sprint 64** : clarification définitive entre nombre de mémoires RX et nombre de sessions de validation pour R3/F1ZBX, CROSS Étel Ch64 et CROSS Corsen Ch79.
- `research/paired-rx-policy.json` passe au schéma 1.1 : une paire vérifiée de deux fréquences distinctes conserve exactement **2 mémoires RX**, tandis que le nombre de sessions terrain reste un nombre de preuves et ne crée aucune mémoire supplémentaire.
- `research/normandie-v0.4/r3-validation-pack.json` marque `R3-OUT` 145.675 et `R3-IN` 145.075 comme les **2 membres de paire R3** ; `CTRL-ZHY` reste un contrôle facultatif hors paire. La porte R3 exige toujours **2 sessions indépendantes**, avec delta futur +2 seulement si elle passe.
- Ajout de `research/sprint-64-dual-rx-contract.json` : Ch64 reste verrouillé en **156.225 / 160.825 MHz** et Ch79 en **156.975 / 161.575 MHz**, soit 2 mémoires RX par voie duplex si elles deviennent publiables.
- Ajout de `tests/test_sprint64_dual_rx_contract.py` et intégration CI pour empêcher toute confusion future entre sessions de preuve et mémoires, ou toute perte d'un sens RX sur Ch64/Ch79.
- Mise à jour de `README.md`, `PROJECT_STATUS.md`, `research/project-resume-state.json` et des garde-fous de reprise au **Sprint 64 / 0.21.53**.
- État Normandie v0.4 inchangé : **142 mémoires**, preview 142, plafond 147, revue **3/9**, **6 blocages**, **0 ajout éligible**.
- État public inchangé : Normandie v0.3.1 **139**, Annecy–Alpes–Léman v0.2 **65/48**, Bretagne non publique.

## 0.21.52 - 2026-08-11

- **Sprint 63** : revalidation ciblée des blocages externes Normandie v0.4 et nouvelle tentative d'exploitation du Guide Marine 2026, sans mutation des packs publics.
- Ajout de `research/sprint-63-source-revalidation.json` et `research/sprint-63-summary.md` : F1ZOV reste **En Maintenance** chez l'exploitant local, F6ZES reste sans fréquence/mode exploitable et R3 reste sans nouvelle observation terrain.
- F5ZHA : le REF conserve **145.4675 / 432.575 MHz** ; la valeur conflictuelle RepeaterBook **431.4125 MHz** est désormais qualifiée comme conflit secondaire stale car la page de vérification affiche **2017-02-17** et `Off-Air`. Cette requalification ne ferme ni l'exigence de réconciliation autoritative ni la validation de couverture Mortain.
- Guide Marine 2026 : URL PDF directe identifiée et chargement retenté le 11 août 2026 ; le workflow web retourne toujours un `cache miss`, donc aucun contenu/capture PDF exploitable et aucune conclusion Ch64/Ch79.
- Ajout de `tests/test_sprint63_blocker_revalidation.py`, intégration CI et mise à jour des garde-fous de reprise au **Sprint 63 / 0.21.52**.
- État Normandie v0.4 inchangé : **142 mémoires**, preview 142, plafond 147, revue **3/9**, **6 blocages**, **0 ajout éligible**.
- État public inchangé : Normandie v0.3.1 **139**, Annecy–Alpes–Léman v0.2 **65/48**, Bretagne non publique.

## 0.21.51 - 2026-08-11

- **Sprint 62** : séparation renforcée entre convergence documentaire, infrastructure radio actuelle, contexte primaire historique et affectation opérationnelle actuelle des canaux CROSS.
- `research/bretagne-v0.1/etel-channel64-evidence.json` formalise une convergence de trois sources opérationnelles locales actuelles vers le **canal 63**, tout en maintenant le canal 64 en conflit primaire non résolu : ni fonctionnement actuel, ni arrêt, ni site Ch64 ne sont considérés comme prouvés.
- Ajout du **Guide Marine 2026 de Météo-France** comme cible primaire de réconciliation pour Étel et Corsen ; sa page de présentation du 5 août 2026 indique que le guide contient horaires et fréquences radio des bulletins VHF, mais le PDF non extractible dans ce workflow ne produit aucune inférence.
- `research/bretagne-v0.1/corsen-channel79-evidence.json` qualifie **Cap Fréhel** et **Stiff / Ouessant** comme infrastructures CROSS actuelles vérifiées, sans leur attribuer Ch79 ; le contexte primaire historique 2003 reste explicitement distinct d'une validation 2026.
- Ajout de `tests/test_sprint62_primary_reference_boundaries.py` et intégration CI pour interdire qu'une convergence Ch63 réfute Ch64, qu'une infrastructure radio implique un canal, qu'une affectation historique soit traitée comme actuelle ou qu'une référence primaire non lue produise une conclusion.
- Ajout de `research/sprint-62-summary.md` et mise à jour de `README.md`, `PROJECT_STATUS.md`, `research/project-resume-state.json` et des garde-fous de reprise au **Sprint 62 / 0.21.51**.
- État Normandie v0.4 inchangé : **142 mémoires internes**, preview 142, plafond de travail connu 147, **3/9** points de revue, **6** blocages et **0** ajout éligible.
- État public inchangé : Normandie v0.3.1 reste figée à **139 mémoires**, Annecy–Alpes–Léman v0.2 à **65/48 mémoires** et Bretagne reste non publique.

## 0.21.50 - 2026-08-10

- **Sprint 61** : approfondissement de la recherche CROSS Étel/Corsen et relecture analogique autour de Mortain-Bocage, sans mutation des packs publics.
- Ajout de `research/bretagne-v0.1/etel-channel64-evidence.json` : le canal 64 Morbihan est désormais classé **conflit entre sources primaires actuelles**. Le ministère maintient l'affirmation 63/64 tandis que la page CROSS Étel, son planning météo lié et le bilan 2025 nomment les émetteurs/canaux courants sans mentionner 64 ; aucun site n'est attribué et l'absence locale n'est pas traitée comme preuve d'arrêt.
- `research/bretagne-v0.1/etel-network.json` passe au schéma 1.1 et conserve séparément les dimensions de réseau **17 stations radio** (offre technique 2026) et **16 VHF + 2 MF** (bilan 2025), sans réconciliation arithmétique faute de définition commune.
- `research/bretagne-v0.1/corsen-channel79-evidence.json` passe au schéma 1.1 : le bilan officiel Corsen 2025 est identifié mais son PDF volumineux n'est pas exploité dans ce workflow ; Cap Fréhel/Bodic restent des indices secondaires, sans attribution primaire Ch79.
- Ajout de `research/normandie-v0.4/mortain-adjacent-ref-scan.json` : recontrôle REF des départements 35, 50, 53 et 61, avec **0 nouveau relais analogique actif non déjà suivi** et delta candidat **0**.
- Ajout de `tests/test_sprint61_research.py`, mise à jour de `tests/test_etel_network_research.py` et des garde-fous de reprise Sprint 61 ; intégration du nouveau test à GitHub Actions.
- Mise à jour de `README.md`, `PROJECT_STATUS.md`, `research/project-resume-state.json` et ajout de `research/sprint-61-summary.md` au **Sprint 61 / 0.21.50**.
- État public inchangé : Normandie v0.3.1 reste figée à **139 mémoires**, Annecy–Alpes–Léman v0.2 à **65/48 mémoires**, Bretagne reste non publique et Normandie v0.4 reste un candidat interne non public à **142 mémoires** avec **3/9** points de revue, **6** blocages et **0** ajout éligible.

## 0.21.49 - 2026-08-10

- Consolidation des **Sprints 55 à 60** dans `research/sprint-55-60-summary.md` : snapshot de revue, manifeste SHA-256, détection de dérive, dry-run de publication, handoff de revue et reprise de recherche externe prioritaire.
- Ajout de `tools/build_normandie_v04_review_snapshot.py`, `tools/build_normandie_v04_review_manifest.py`, `tools/check_normandie_v04_review_drift.py` et `tools/run_normandie_v04_publication_dry_run.py` ; ces outils restent strictement non publics et non destructifs.
- Ajout de `tests/test_normandie_v04_review_handoff.py` et intégration CI : état courant **3/9 points de revue complétés**, **6 blocages ouverts**, candidat/preview **142/142**, `release_ready=false`.
- Ajout de `research/normandie-v0.4/f6zes-revalidation.json` : le REF courant confirme F6ZES Sourdeval, F1SMB, `IN98MR93XV` et 230 m, mais fréquence, bande, mode et état restent non résolus ; delta candidat **0** et aucune conjecture autorisée.
- Ajout de `research/bretagne-v0.1/corsen-channel79-evidence.json` : une source locale actuelle associe le canal 79 à **Cap Fréhel** et **Bodic**, conservés comme indices secondaires à revalider par source primaire ; aucun site n'est promu et le delta RF reste **0**.
- Ajout de `tests/test_sprint60_revalidation.py` et de l'étape GitHub Actions correspondante pour figer l'absence de fréquence F6ZES inventée et l'absence de promotion Ch79 depuis une source secondaire.
- Mise à jour de `README.md`, `PROJECT_STATUS.md` et `research/project-resume-state.json` au **Sprint 60 / 0.21.49**.
- État public inchangé : Normandie v0.3.1 reste figée à **139 mémoires**, Annecy–Alpes–Léman v0.2 à **65/48 mémoires**, Bretagne reste non publique et Normandie v0.4 reste un candidat interne non public à **142 mémoires**.

## 0.21.43 - 2026-08-10

- Consolidation des **Sprints 50 à 54** : politique de fraîcheur des sources, checklist de revue, diff structurel candidat et audit prépublication non public.
- Ajout de `research/normandie-v0.4/source-freshness-policy.json` et de `tools/check_normandie_v04_source_freshness.py` : une revalidation périmée bloque la revue sans devenir une preuve d'arrêt ou d'absence.
- Ajout de `tools/build_normandie_v04_review_checklist.py` : état courant **2/9 points complétés** et **7 blocages ouverts**.
- Ajout de `tools/build_normandie_v04_candidate_diff.py` : contrôle structurel exact **139 → 142 → preview 142**, sans réécriture de la base publiée et avec RX-only maintenu.
- Ajout de `tools/run_normandie_v04_prepublication_audit.py` et `tests/test_normandie_v04_prepublication_audit.py` : état courant `integrity_ok=true` mais `release_ready=false`.
- Intégration du nouvel audit au runner local et à GitHub Actions ; mise à jour de `README.md`, `PROJECT_STATUS.md`, `pack-plan.json` et `research/project-resume-state.json` au **Sprint 54 / 0.21.43**.
- Les étapes intermédiaires **0.21.19 à 0.21.42** sont détaillées dans `research/sprint-30-34-summary.md`, `research/sprint-35-39-summary.md`, `research/sprint-40-44-summary.md`, `research/sprint-45-49-summary.md` et `research/sprint-50-54-summary.md`.
- État public inchangé : Normandie v0.3.1 reste figée à **139 mémoires**, Annecy–Alpes–Léman v0.2 à **65/48 mémoires**, Bretagne reste non publique et Normandie v0.4 reste un candidat interne non public à **142 mémoires**.

## 0.21.18 - 2026-08-10

- Ajout de `research/normandie-v0.4/promotion-gates.json` pour centraliser les **5 fréquences encore exclues** du candidat interne 142 mémoires : R3/F1ZBX 145.075/145.675, F5ZHA 145.4675/432.575 et F1ZOV 431.975 MHz.
- Recontrôle courant : aucune preuve publique fiable de réception R3 depuis Mortain n'a été trouvée ; le Radio Club Nord Cotentin indique toujours F1ZOV **En Maintenance** ; F5ZHA reste en conflit entre REF + `manuel.la-radio.eu` sur 145.4675/432.575 MHz et RepeaterBook sur 431.4125 MHz.
- Ajout de `research/normandie-v0.4/r3-validation-pack.json` et de `tools/build_normandie_v04_r3_validation_pack.py` : mini-pack autonome de trois mémoires RX (`R3-OUT`, `R3-IN`, `CTRL-ZHY`), sans tonalité RX filtrante, `Duplex=off`, `Offset=0.000000` et TX bloqué.
- Ajout de `tools/check_normandie_v04_promotion_gates.py` : la porte R3 ne peut passer qu'après au moins **deux sessions RX indépendantes** identifiant la sortie 145.675 MHz avec intelligibilité suffisante ; F5ZHA et F1ZOV restent soumis à leurs preuves externes respectives.
- Renforcement de `r3-mortain-field-validation.json` et `pack-plan.json` avec les liens vers le mini-pack, l'évaluateur et les portes de promotion ; une recherche web infructueuse ne vaut jamais preuve d'arrêt ou d'absence.
- Ajout de `tests/test_normandie_v04_promotion_gates.py` et de l'étape CI correspondante : génération temporaire du mini-pack, contrôle RX-only, simulation de deux sessions R3 valides et interdiction de toute exposition publique.
- Le candidat interne Normandie v0.4 reste à **142 mémoires** : aucune des cinq fréquences bloquées n'est ajoutée automatiquement et les locations provisoires 175–177 restent les seuls ajouts internes actuels.
- État public inchangé : Normandie v0.3.1 reste figée à 139 mémoires, Annecy–Alpes–Léman v0.2 reste figé à 65/48 mémoires et Bretagne reste non publique.

## 0.21.17 - 2026-08-10

- Ajout de `research/normandie-v0.4/internal-candidate-map.json` et de `tools/build_normandie_v04_internal_candidate.py` pour matérialiser un **candidat interne Normandie v0.4 à 142 mémoires**, toujours hors publication.
- Le builder conserve les **139 lignes de Normandie v0.3.1 comme préfixe exact** et ajoute uniquement trois côtés paired RX revalidés : `50-ZHY-IN` 145.0875 MHz en location 175, `53-ZCE-IN` 145.1000 MHz en location 176 et `50-ZBL-U` 431.2500 MHz en location 177.
- Revalidation actuelle des trois ajouts : ARA50 pour F5ZHY 145.0875/145.6875, ARAS72 pour F6ZCE 145.700 MHz avec shift -600 kHz, et Radio Club Nord Cotentin F6KFW + ARA50 pour F1ZBL 145.250/431.250 MHz.
- Les locations 175–177 sont **internes et provisoires** ; le nombre final de mémoires publiques v0.4 reste `null` et le plan public final n'est pas encore numéroté.
- R3 Brocéliande reste hors candidat interne tant que la réception depuis Mortain n'est pas validée ; F5ZHA reste bloqué par conflit de source/couverture et F1ZOV 431.975 MHz reste bloqué tant que l'exploitant indique le relais en maintenance.
- Ajout de `tests/test_normandie_v04_internal_candidate.py` : reconstruction en répertoire temporaire, contrôle du préfixe byte-stable, des 142 lignes, des positions/noms/fréquences uniques, de `Duplex=off`, `Offset=0.000000`, de l'absence de tonalité RX imposée et de toute exposition publique.
- Ajout de `research/normandie-v0.4/generated/` au `.gitignore` et intégration du nouveau test à la CI ; aucun CSV interne généré n'est suivi dans Git.
- État public inchangé : Normandie v0.3.1 reste figée à 139 mémoires, Annecy–Alpes–Léman v0.2 reste figé à 65/48 mémoires et Bretagne reste non publique.

## 0.21.16 - 2026-08-10

- Ajout de `research/normandie-v0.4/candidate-memory-delta.json` pour comparer explicitement les **12 fréquences paired RX de recherche** avec les **139 mémoires figées de Normandie v0.3.1**, sans créer de CSV ni attribuer de positions mémoire.
- Quatre fréquences paired RX sont déjà présentes dans la base publiée (`145.6875`, `145.7000`, `145.2500`, `430.3750 MHz`) ; le delta maximal actuellement étudié est donc de **8 nouvelles fréquences RX**.
- Classification du delta : **3 ajouts prêts au niveau recherche** (`145.0875`, `145.1000`, `431.2500 MHz`), **2 fréquences R3 Brocéliande** soumises à validation RX depuis Mortain, **2 fréquences F5ZHA** bloquées par conflit de source/couverture et **1 fréquence F1ZOV** bloquée par le statut maintenance de l'exploitant local.
- Ajout de `research/normandie-v0.4/r3-mortain-field-validation.json` comme protocole RX-only : aucune transmission, réception répétable requise, un simple porteuse faible ne suffit pas et la géométrie 119,3 km / 150 km n'est jamais une preuve de couverture.
- Réconciliation F1ZOV : la paire **430.375 / 431.975 MHz** est recoupée, mais le Radio Club Nord Cotentin indique actuellement le relais en maintenance ; la mémoire 430.375 MHz de v0.3.1 reste immuable et le nouveau côté 431.975 MHz reste bloqué jusqu'au retour en service vérifié.
- Ajout de `tests/test_normandie_v04_candidate_delta.py`, intégration à la CI et mise à niveau des garde-fous `test_site_files.py` / `test_analog_coverage_redundancy_review.py` sans affaiblir les contrôles existants.
- Le plan mémoire v0.4 devient un **delta candidat défini mais non public** ; le nombre final de mémoires reste volontairement `null` et aucune position n'est attribuée.
- État public inchangé : Normandie v0.3.1 reste figée à 139 mémoires, Annecy–Alpes–Léman v0.2 reste figé à 65/48 mémoires et Bretagne reste non publique.

## 0.21.15 - 2026-08-10

- Qualification géométrique de `F1ZBX` / R3 Brocéliande depuis Mortain : distance directe d'environ **119,3 km** à partir des coordonnées opérateur ARA35 et du référentiel géographique de Mortain.
- Le rayon d'usage de **150 km** publié par l'ARA35 place Mortain géométriquement environ **30,7 km** à l'intérieur de ce rayon ; R3 devient une priorité de validation terrain, mais `actual_reception_from_mortain_verified` reste à `false`.
- Ajout du garde-fou `geometric_inclusion_in_operator_radius_is_not_reception_proof` dans le système R3/R71 et la couverture Mortain afin d'interdire toute promotion basée sur la seule géométrie.
- Canal 64 Morbihan : la page ministérielle mise à jour le **19 juin 2026** reconfirme les canaux 63/64 pour le bulletin côtier permanent dans le Morbihan, tandis que la page HTML actuelle du CROSS Étel nomme Étel sur 63 mais aucun site Bretagne sur 64.
- Ajout du garde-fou `ministry_regional_channel_statement_does_not_identify_transmitter_site` ; le site actuel du canal 64 reste non identifié et aucune attribution n'est inventée.
- `F5ZHA` Laval, `F6ZES` Sourdeval et l'émetteur actuel du canal 79 Corsen restent ouverts faute de nouvelle preuve suffisamment forte ; les comptes paired RX restent **Normandie 12 / Annecy 10 / Bretagne 29** avec TX toujours bloqué.
- État public inchangé : Normandie v0.3.1 reste figée à 139 mémoires, Annecy–Alpes–Léman v0.2 reste figé à 65/48 mémoires et Bretagne reste non publique.

## 0.21.14 - 2026-08-10

- Ajout de `research/bretagne-v0.1/rennes-broceliande-linked-system.json` pour modéliser le système analogique actuellement lié **R3 Brocéliande / R71 Rennes** à partir des pages de l'exploitant ARA35.
- La chaîne liée est représentée par quatre fréquences RX distinctes déjà présentes dans le plan Bretagne : **431.075, 145.075, 145.675 et 438.675 MHz** ; aucun doublon ni mémoire RF supplémentaire n'est créé.
- Le R3 `F1ZBX` conserve sa paire 145.075/145.675 MHz et gagne un contexte de couverture opérateur : rayon d'usage annoncé de **150 km** et liaison R71 documentée à **46,51 km** ; ces valeurs renforcent la priorité de vérification depuis Mortain sans constituer une garantie de réception.
- Passage de `paired-rx-next-version-plan.json` et `paired-rx-deduplicated-memory-plan.json` au schéma 1.3 afin d'enrichir les rôles R3/R71 tout en conservant les comptes **Normandie 12 / Annecy 10 / Bretagne 29**.
- Renforcement de `tests/test_paired_rx_memory_plan.py` : contrôle des quatre rôles RF du système lié, de l'absence de nouvelle mémoire Bretagne et du contrat `Duplex=off` / `Offset=0.000000` / TX désactivé.
- `F6ZES` Sourdeval, le site actuel du canal 64 Morbihan et l'émetteur actuel du canal 79 Corsen restent non résolus ; aucune valeur n'est inventée.
- État public inchangé : Normandie v0.3.1 reste figée à 139 mémoires, Annecy–Alpes–Léman v0.2 reste figé à 65/48 mémoires et Bretagne reste non publique.

## 0.21.13 - 2026-08-10

- Ajout d'une règle explicite de hiérarchie pour les statuts opérationnels des relais : lorsqu'une association exploitante actuelle et un annuaire général divergent, l'état de l'exploitant local est retenu pour la recherche courante et le conflit reste enregistré.
- Rennes : l'ARA35 maintient `F5ZEB` / R71 opérationnel depuis le 25 septembre 2025 alors que le REF l'affiche arrêté ; R71 reste une donnée opérationnelle de recherche mais non sélectionnée avant revue de couverture.
- Rennes : l'ARA35 indique `F5ZPV` / RU19 temporairement arrêté sans redémarrage confirmé alors que le REF l'affiche actif ; RU19 reste hors candidats actifs. `F5ZZH` / R7X est arrêté dans les deux sources.
- `F5ZHA` Laval : la paire REF **145.4675 / 432.575 MHz** est désormais corroborée par `manuel.la-radio.eu` ; l'ancien conflit RepeaterBook 431.4125 devient moins crédible mais la publication reste bloquée jusqu'à une source locale actuelle.
- `F6ZES` Sourdeval, le canal 64 Morbihan et l'émetteur actuel du canal 79 Corsen restent non résolus après recontrôle ciblé du 10 août 2026 ; aucune valeur n'est inventée.
- Passage des revues Bretagne/Normandie au schéma 1.2 et renforcement du test couverture/redondance avec les conflits de statuts exploitant/annuaire.
- Comptes paired RX inchangés : **Normandie 12, Annecy 10, Bretagne 29** ; ces nombres restent des comptes de recherche et non des tailles cibles.
- État public inchangé : Normandie v0.3.1 reste figée à 139 mémoires, Annecy–Alpes–Léman v0.2 reste figé à 65/48 mémoires et Bretagne reste non publique.

## 0.21.12 - 2026-08-10

- Renforcement de la qualité des sources paired RX : un conflit secondaire ancien ne remplace plus une paire actuelle recoupée, mais déclenche explicitement une porte de réconciliation avant publication lorsqu'il n'est pas fermé par une seconde source actuelle.
- `F1ZBL` Équeurdreville est confirmé en **145.250 / 431.250 MHz** par le REF actuel et le Radio Club Nord Cotentin ; la valeur secondaire RepeaterBook 431.225 MHz est rejetée comme conflit non concordant.
- `F5ZHA` Laval reste en recherche sur **145.4675 / 432.575 MHz** selon le REF actuel, mais une ancienne fiche RepeaterBook indique 431.4125 MHz ; la paire reste donc `publication_blocked_by_source_conflict: true` jusqu'à recoupement local actuel supplémentaire.
- Cluster Côtes-d'Armor **432.650 MHz** : une cartographie radioamateur actuelle indépendante corrobore la présence des cinq sites F5ZIS/F5ZIT/F5ZIU/F5ZIV/F5ZJR, sans prouver leur interconnexion ; `current_primary_linkage_verified` et `current_association_linkage_verified` restent à `false`.
- Passage de `research/normandie-v0.4/paired-rx-refresh.json` et `research/bretagne-v0.1/analog-coverage-redundancy-review.json` au schéma 1.1 ; renforcement de `tests/test_analog_coverage_redundancy_review.py` pour figer les niveaux de confiance et les conflits de sources.
- Les comptes paired RX restent inchangés à **12 fréquences uniques pour Normandie v0.4**, **10 pour Annecy–Alpes–Léman v0.3** et **29 pour Bretagne v0.1** ; F5ZHA est compté comme paire de recherche mais non publiable tant que le conflit n'est pas réconcilié.
- Le canal 64 Morbihan, l'émetteur actuel du canal 79 Corsen et F6ZES Sourdeval restent non résolus ; aucune donnée n'est inventée pour fermer artificiellement ces dossiers.
- État public inchangé : Normandie v0.3.1 reste figée à 139 mémoires, Annecy–Alpes–Léman v0.2 reste figé à 65/48 mémoires et Bretagne reste non publique.

## 0.21.11 - 2026-08-10

- Ajout de `research/bretagne-v0.1/analog-coverage-redundancy-review.json` pour qualifier la diversité géographique et la redondance des relais/transpondeurs analogiques sans transformer locators, altitudes, puissances ou gains d'antenne en preuve de couverture radio.
- Cluster Côtes-d'Armor 432.650 MHz : cinq sites REF actuels restent actifs sur la même fréquence avec F6HRP et CTCSS 71.9 Hz ; les centres des locators Matignon / Perros-Guirec sont distants d'environ 90,6 km, ce qui justifie une priorité élevée d'efficacité mémoire mais ne prouve aucune portée radio.
- Conservation d'une ancienne mention RepeaterBook reliant F5ZIT à F5ZIV/F5ZIU/F5ZIS/F5ZJR comme indice historique secondaire uniquement ; l'interconnexion actuelle du cluster reste `current_primary_linkage_verified: false` faute de source primaire/associative actuelle explicite.
- Revue Morbihan : F1ZMU reste un candidat distinct avec sa paire 439.725/430.325 MHz malgré sa proximité géométrique avec F5ZPE ; F1ZBZ ajoute trois fréquences RF nouvelles après déduplication avec F5ZPE et reste soumis à une revue de couverture locale.
- Ajout de `research/normandie-v0.4/paired-rx-refresh.json` : F1ZBL Équeurdreville est désormais résolu en 145.250/431.250 MHz dans les deux sens et F5ZHA Laval en 145.4675/432.575 MHz ; F6ZES Sourdeval reste sans fréquence/mode exploitable.
- Passage des plans `paired-rx-next-version-plan.json` et `paired-rx-deduplicated-memory-plan.json` au schéma 1.2 ; la carte paired RX atteint désormais **12 fréquences uniques pour Normandie v0.4**, **10 pour Annecy–Alpes–Léman v0.3** et **29 pour Bretagne v0.1**.
- Ajout de `tests/test_analog_coverage_redundancy_review.py`, mise à jour de `tests/test_paired_rx_memory_plan.py` et ajout de l'étape CI `Test analog coverage and redundancy review`.
- Le canal 64 Morbihan et l'émetteur actuel du canal 79 Corsen restent non résolus ; aucune attribution n'est inventée.
- État public inchangé : Normandie v0.3.1 reste figée à 139 mémoires, Annecy–Alpes–Léman v0.2 reste figé à 65/48 mémoires et Bretagne reste non publique.

## 0.21.10 - 2026-08-10

- Ajout de `research/bretagne-v0.1/ref-analog-expansion.json` après recontrôle du répertoire REF actuel pour étendre l'inventaire analogique Bretagne sans publication.
- Ajout de trois transpondeurs actifs Côtes-d'Armor partageant 432.650 MHz : `F5ZIU` La Harmoye 145.4625/432.6500, `F5ZIV` Saint-Brieuc 145.4875/432.6500 et `F5ZJR` Plessala 145.2875/432.6500 MHz ; le cluster 432.650 regroupe désormais cinq sites avec F5ZIS/F5ZIT.
- Ajout de `F1ZMU` Saint-Nolff comme relais analogique actif Morbihan, sortie 430.325 MHz / entrée 439.725 MHz, 50 W selon le REF.
- Résolution du cas `F1ZBZ` Lorient comme transpondeur multi-chemins : conservation exacte des lignes REF autour de 431.200 MHz et des fréquences 145.6250, 145.0250, 145.7375 et 145.1375 MHz, sans déduire de couverture.
- Passage de la carte paired RX Bretagne de **21 à 29 fréquences RF uniques de recherche** après déduplication ; 145.1375 et 145.7375 restent partagées avec F5ZPE, 432.650 reste une seule mémoire RF pour cinq transpondeurs.
- Passage de `research/paired-rx-next-version-plan.json` et `research/paired-rx-deduplicated-memory-plan.json` au schéma 1.1 ; F1ZBZ sort de la liste non résolue mais reste soumis à revue de couverture/redondance.
- Ajout de `tests/test_bretagne_ref_analog_expansion.py`, mise à jour de `tests/test_paired_rx_memory_plan.py` et ajout de l'étape CI correspondante ; aucune couverture ni rôle ADRASEC n'est inféré des seules métadonnées techniques.
- Le canal 64 Morbihan et l'émetteur actuel du canal 79 Corsen restent non résolus ; aucune attribution n'est inventée.
- État public inchangé : Normandie v0.3.1 reste figée à 139 mémoires, Annecy–Alpes–Léman v0.2 reste figé à 65/48 mémoires et Bretagne reste non publique.

## 0.21.9 - 2026-08-09

- Ajout de `research/paired-rx-deduplicated-memory-plan.json` pour matérialiser les fréquences RX uniques issues des paires duplex/split déjà documentées, sans attribuer de positions mémoire ni publier de nouvelle version.
- Déduplication régionale explicite : **8 fréquences uniques** dans le sous-plan Normandie v0.4, **10** dans Annecy–Alpes–Léman v0.3 et **21** dans Bretagne v0.1 ; ces nombres sont des comptes de recherche et non des tailles finales de packs.
- Bretagne : fusion de 432.650 MHz pour F5ZIS/F5ZIT et de 145.2625 MHz pour F1ZGS/F5ZDV/F5ZZL ; F5ZPV et F5ZZH restent exclus de la liste active car arrêtés, F1ZUG et F1ZBZ restent non résolus.
- Annecy v0.3 : 145.850 MHz est fusionné pour les montées SO-50/AO-123, 432.5125 MHz pour F1ZHG/F5ZGT et la paire F1ZJV/F1ZYT est dédupliquée ; les satellites restent soumis à recontrôle opérationnel avant publication.
- Normandie v0.4 : les paires F5ZHY, F6ZCE, F1ZBX et F1ZOV sont matérialisées en RX entrée/sortie ou côtés A/B ; F6ZES et F1ZBL restent hors liste active tant que leurs données ne sont pas suffisamment résolues.
- Ajout de `tests/test_paired_rx_memory_plan.py` et de l'étape CI `Test paired RX deduplicated memory plan`, avec contrôle des comptes, de l'unicité RF, des noms ≤ 10 caractères, du contrat TX-off et de l'absence de mutation publique.
- Les recherches officielles poursuivies sur CROSS Étel n'ont pas encore fourni de liste nominative des 17 stations ni d'émetteur primaire actuel pour le canal 64 ; le bilan 2025 publié n'est pas utilisé faute de lecture PDF fiable dans ce workflow.
- État public inchangé : Normandie v0.3.1 reste figée à 139 mémoires, Annecy–Alpes–Léman v0.2 reste figé à 65/48 mémoires et Bretagne reste non publique.

## 0.21.8 - 2026-08-09

- Ajout de `research/bretagne-v0.1/etel-network.json` à partir d'une source officielle DIRM NAMO 2026 indiquant que le service technique du CROSS Etel maintient **17 stations radio réparties sur le littoral, de la Pointe de Penmarc'h à Biarritz**.
- Séparation explicite entre le dimensionnement du réseau et son inventaire nominatif : le nombre de 17 stations ne permet pas d'en déduire leurs noms, leurs canaux ni leur couverture individuelle.
- Conservation des émetteurs météo déjà primaire-vérifiés comme inventaire partiel : Penmarc'h, Groix et Belle-Ile sur le canal 80, Étel sur le canal 63 ; Chassiron sur 63 est conservé comme contexte hors Bretagne.
- Renforcement du dossier **canal 64 Morbihan** : le réseau Étel est plus large que les seuls émetteurs météo nommés, mais aucun site primaire actuel n'est encore identifié pour 64 ; `channel_64_site_must_not_be_guessed` reste obligatoire.
- Ajout de `tests/test_etel_network_research.py` et de l'étape CI correspondante afin de figer le nombre de 17 stations, l'inventaire météo partiel, l'absence de site 64 et l'absence de promotion publique.
- La politique paired RX reste inchangée : les deux fréquences du canal 64 sont conservées comme données RX, mais aucune attribution territoriale n'est inventée tant que le site n'est pas validé.
- État public inchangé : Normandie v0.3.1 reste figée à 139 mémoires, Annecy–Alpes–Léman v0.2 reste figé à 65/48 mémoires et Bretagne reste non publique.

## 0.21.7 - 2026-08-09

- Nouvelle politique globale `research/paired-rx-policy.json` : toute liaison publique nativement duplex/split dont les deux fréquences distinctes sont vérifiées doit permettre l'écoute des deux sens avec deux mémoires RX, tout en conservant `Duplex=off` et `Offset=0.000000` sur chacune.
- Ajout de `research/paired-rx-next-version-plan.json` pour préparer la double écoute des relais/transpondeurs analogiques, des voies maritimes duplex et des satellites split dans Normandie v0.4, Annecy–Alpes–Léman v0.3 et Bretagne v0.1, avec déduplication des fréquences RF partagées.
- Bretagne maritime : les canaux 63, 64, 79 et 80 conservent désormais explicitement les deux côtés RX navire→côte et côte→navire ; le canal 16 simplex reste une seule mémoire. `public-maritime-radio.json` passe au schéma 1.7.
- Annecy–Alpes–Léman v0.3 : préparation de l'écoute des montées et descentes de SO-50, AO-91 et AO-123 après recontrôle opérationnel ; la montée 145.850 MHz commune à SO-50/AO-123 restera dédupliquée. La v0.2 publiée reste immuable.
- Normandie v0.4 : adoption de la double écoute entrée/sortie pour les futurs relais analogiques sélectionnés ; la v0.3.1 publiée est déjà conforme pour la VHF marine avec ses paires `-S` / `-C` et reste immuable.
- Validation complémentaire du zonage SAR : la SRR actuelle de CROSS Corsen est enregistrée de la baie du Mont-Saint-Michel à la pointe de Penmarc'h, en raccord avec la compétence CROSS Étel à partir de Penmarc'h ; cette frontière ne permet pas de déduire les recouvrements VHF ni les sites émetteurs.
- Ajout de `tests/test_paired_rx_policy.py`, intégration à la CI et renforcement des garde-fous globaux/Mortain/Bretagne afin d'empêcher tout retour à une politique « descente seulement » tout en maintenant le TX bloqué.
- État public inchangé : Normandie v0.3.1 reste figée à 139 mémoires, Annecy–Alpes–Léman v0.2 reste figé à 65/48 mémoires et Bretagne reste non publique.

## 0.21.6 - 2026-08-09

- Validation primaire d'une **couverture VHF opérationnelle actuelle dans le secteur de la Pointe du Raz** : un communiqué de la Préfecture maritime documente un contact VHF établi par le CROSS Corsen avec un navire au nord de la pointe le 21 septembre 2025, sans identifier le site émetteur ni le canal.
- Maintien de l'installation VHF/MF historique de la **Pointe du Raz** à `current_validation: false` : une preuve de couverture sectorielle ne vaut pas revalidation du site émetteur historique et ne permet pas d'attribuer le canal 79.
- Séparation du centre opérationnel actuel de **Pointe de Corsen / Plouarzel** de l'inventaire des stations radio déportées ; l'implantation actuelle du CROSS ne suffit pas à revalider son ancienne installation radio locale multicanal.
- Ajout du contexte futur **CROSS Nouvelle génération** : regroupement fonctionnel Étel/Corsen prévu à l'horizon 2027, conservé comme métadonnée de transition sans modifier les fréquences ou sites actuels.
- Ajout de `F5ZZH` / R7X Rennes-Beaulieu à l'inventaire de recherche : sortie 145.7875 MHz, entrée 145.1875 MHz, FM, actuellement indiqué par l'ARA35 comme temporairement arrêté et à la recherche d'un nouveau site ; `rx_pack_candidate: false`.
- Passage de `public-maritime-radio.json` au schéma 1.5, de `maritime-zones.json` au schéma 1.4 et de `emergency-relays.json` au schéma 1.4 ; renforcement des garde-fous distinguant infrastructure, couverture, site émetteur et canal.
- Le canal 79 reste sans émetteur actuel primaire-vérifié, le canal 64 reste sans émetteur Bretagne réconcilié, F6ZES Sourdeval reste sans fréquence/mode et les rôles ADRASEC 22/29/56 restent ouverts.
- État public inchangé : Normandie v0.3.1 reste figée à 139 mémoires, Annecy–Alpes–Léman v0.2 reste figé à 65/48 mémoires et Bretagne reste non publique.

## 0.21.5 - 2026-08-09

- Revalidation actuelle primaire du **Stiff / Ouessant** comme infrastructure radio du CROSS Corsen : une offre officielle DIRM NAMO 2026 indique que la tour abrite les radars et des équipements de radiocommunications, et un marché public DGAMPA confirme que la vigie héberge aujourd'hui les équipements radio et informatiques nécessaires aux missions du CROSS.
- Passage du Stiff de simple piste historique 2003 à `current_validation: true`, avec maintien de `radio_service_or_channel: null` : la présence actuelle d'équipements radio ne suffit pas à attribuer un canal précis.
- Maintien du **canal 79** en revalidation : son usage Corsen/Ouessant est documenté par une source primaire de 2003, mais aucune source primaire actuelle exploitée ne rattache encore explicitement le canal 79 au Stiff ou à un autre émetteur Corsen.
- Maintien de **Pointe du Raz** et du site de **Corsen** comme pistes radio historiques non revalidées actuellement ; aucune donnée actuelle n'est inventée à partir de l'architecture de 2003.
- Passage de `research/bretagne-v0.1/public-maritime-radio.json` au schéma 1.4 et de `maritime-zones.json` au schéma 1.3, avec ajout de la règle interdisant de déduire un canal de la seule validation d'une infrastructure radio.
- Renforcement de `tests/test_mortain_bretagne_radio_research.py`, `tests/test_bretagne_research_scaffold.py` et `tests/test_site_files.py` pour figer Cap Fréhel et Stiff comme infrastructures actuelles vérifiées tout en conservant leurs canaux à `null`.
- État public inchangé : Normandie v0.3.1 reste figée à 139 mémoires, Annecy–Alpes–Léman v0.2 reste figé à 65/48 mémoires et Bretagne reste non publique.

## 0.21.4 - 2026-08-09

- Ajout du dimensionnement actuel du réseau CROSS Corsen à partir d'une communication officielle DGAMPA : **10 stations radio VHF et 2 stations MF**, avec liste nominative et canaux encore à inventorier.
- Ajout comme pistes primaires historiques du décret de 2003 documentant des équipements radio au Stiff / Ouessant, à la Pointe du Raz et sur le site de Corsen ; ces sites restent explicitement `current_validation: false` tant qu'une source actuelle ne les recoupe pas.
- Documentation historique primaire d'une diffusion régulière Corsen/Ouessant sur le canal 79 après appel sur le canal 16 ; le canal 79 reste une donnée de recherche à revalider pour l'architecture actuelle.
- Recontrôle 2026 de la page ministérielle mentionnant les canaux 63/64 pour le bulletin côtier permanent dans le Morbihan ; maintien du canal 64 sans émetteur Bretagne attribué car les sources locales actuelles du CROSS Étel exploitées identifient Étel sur 63 et aucun site sur 64.
- Passage de `research/bretagne-v0.1/public-maritime-radio.json` au schéma 1.3 avec séparation stricte entre réseau actuel, infrastructure Cap Fréhel primaire-vérifiée et architecture historique à revalider.
- Renforcement de `tests/test_mortain_bretagne_radio_research.py` et `tests/test_site_files.py` pour empêcher toute promotion d'un site ou canal historique comme donnée actuelle sans revalidation.
- F6ZES Sourdeval reste sans fréquence ni mode et les rôles ADRASEC 22/29/56 restent non attribués faute de sources dédiées suffisamment précises.
- État public inchangé : Normandie v0.3.1 reste figée à 139 mémoires, Annecy–Alpes–Léman v0.2 reste figé à 65/48 mémoires et Bretagne reste non publique.

## 0.21.3 - 2026-08-09

- Validation primaire d'une infrastructure radio CROSS Corsen au phare du Cap Fréhel : la DIRM NAMO confirme des équipements de suivi et de liaison avec les navires pour la surveillance du trafic et la coordination des secours.
- Séparation stricte entre cette infrastructure radio vérifiée et l'inventaire des stations VHF météo : aucun service radio ni canal, notamment le 79, n'est attribué à Cap Fréhel sans source primaire supplémentaire.
- Extension de l'inventaire analogique Finistère à partir du répertoire REF actuel : `F1ZGS` Plouhinec 431.425/145.2625 MHz, `F5ZDV` Morlaix 438.700/145.2625 MHz et `F5ZZL` Cast 431.375/145.2625 MHz, tous en FM avec CTCSS 71.9 Hz et uniquement candidats de recherche.
- Ajout de `F1ZAJ` Plouray 144.800 MHz comme métadonnée APRS Morbihan sans dupliquer la mémoire APRS nationale.
- Le canal 64 reste sans émetteur Bretagne primaire-vérifié, les rôles ADRASEC 22/29/56 restent non attribués faute de source dédiée et F6ZES Sourdeval reste sans fréquence ni mode.
- Renforcement des tests Bretagne/Mortain et secours/ADRASEC ; aucun fichier public, registre public ou version régionale publiée n'est modifié.
- État public inchangé : Normandie v0.3.1 reste figée à 139 mémoires, Annecy–Alpes–Léman v0.2 reste figé à 65/48 mémoires et Bretagne reste non publique.

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