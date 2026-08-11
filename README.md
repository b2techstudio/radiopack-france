# RadioPack France

Codeplugs CHIRP régionaux, documentés et générés à partir de données publiques vérifiables pour les radios Quansheng UV-K5.

## État actuel — Sprint 66 / 0.21.55

Repère de compatibilité documentaire conservé pour les garde-fous historiques : **État actuel — Sprint 39**.

Packs publics immuables :

- **Normandie v0.3.1** — 139 mémoires RX ;
- **Annecy–Alpes–Léman v0.2** — 65 mémoires RX, variante 48 sans aviation.

Recherche : **Normandie v0.4** à **142 mémoires** internes, plafond de travail connu **147 mémoires**, **Bretagne v0.1** non publique et Annecy–Alpes–Léman v0.3 non publique.

Le générateur public ne propose que les versions publiées. Point de reprise : `PROJECT_STATUS.md`, `research/project-resume-state.json`, `research/sprint-55-60-summary.md`, `research/sprint-61-summary.md`, `research/sprint-62-summary.md`, `research/sprint-63-summary.md`, `research/sprint-64-summary.md`, `research/sprint-65-summary.md` et `research/sprint-66-summary.md`.

## Règles permanentes

- RX uniquement : `Duplex=off`, `Offset=0.000000`.
- Pas de remplissage artificiel ; maximum 200 mémoires.
- Versions publiées immuables.
- Géométrie, altitude, puissance ou rayon annoncé ne valent pas preuve de réception.
- Une recherche infructueuse n'est pas une preuve d'arrêt ou d'absence.
- Une source primaire identifiée mais non extractible n'est pas une preuve négative.
- Une source périmée bloque une revue mais n'est jamais une preuve négative.
- Une fréquence non résolue n'est jamais devinée.
- Le statut opérateur local prime sur un annuaire général pour l'état opérationnel courant.
- Une observation terrain ne ferme jamais un conflit de source.
- Une source secondaire actuelle peut orienter une recherche mais ne remplace pas une validation primaire lorsqu'elle est exigée.
- Une source secondaire stale ne remplace pas une réconciliation autoritative explicitement exigée par une porte.
- Un conflit entre sources primaires actuelles doit être réconcilié avant promotion.
- Une convergence locale sur un canal ne réfute pas automatiquement un autre canal mentionné par une source primaire conflictuelle.
- Une absence dans un document local actuel ne constitue pas automatiquement une preuve d'arrêt.
- Une infrastructure radio actuelle ne permet pas d'attribuer un canal précis.
- Une affectation historique primaire ne vaut pas validation opérationnelle actuelle.
- Une déclaration régionale courante sur un canal ne permet pas d'identifier automatiquement son site émetteur.
- La confirmation d'un réseau CROSS actuel ne permet pas de mapper automatiquement un canal vers une station.
- Des nombres de stations fondés sur des unités non définies identiquement ne sont pas réconciliés par simple calcul.
- `research/paired-rx-policy.json` impose les deux côtés RX lorsqu'une liaison duplex/split distincte est vérifiée.
- **Le nombre de sessions terrain est un nombre de preuves, pas un nombre de mémoires.** Une paire de deux fréquences distinctes conserve deux mémoires RX après validation, quel que soit le nombre de sessions nécessaires.
- Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint.

## Normandie v0.4 — Mortain-Bocage / Sud-Manche

Le périmètre suit la couverture radio utile dans les départements 50, 35, 53 et 61. Stations suivies : **F5ZHY**, **F6ZES**, **F6ZCE**, **F1ZBX**, **F5ZHA**, **F1ZOV**.

Fichiers de vérité principaux :

```text
research/normandie-v0.4/mortain-bocage-coverage.json
research/normandie-v0.4/candidate-memory-delta.json
research/normandie-v0.4/internal-candidate-map.json
research/normandie-v0.4/promotion-gates.json
research/normandie-v0.4/blocked-station-revalidation.json
research/normandie-v0.4/external-evidence-matrix.json
research/normandie-v0.4/source-consistency-contract.json
research/normandie-v0.4/source-freshness-policy.json
research/normandie-v0.4/r3-mortain-field-validation.json
research/normandie-v0.4/r3-validation-pack.json
research/normandie-v0.4/f5zha-mortain-validation.json
research/normandie-v0.4/f6zes-revalidation.json
research/normandie-v0.4/mortain-adjacent-ref-scan.json
research/sprint-63-source-revalidation.json
research/sprint-64-dual-rx-contract.json
research/sprint-65-primary-recheck.json
research/sprint-66-technical-inventory-boundaries.json
```

Le candidat interne ajoute actuellement seulement 145.0875 MHz, 145.1000 MHz et 431.2500 MHz aux 139 mémoires figées de v0.3.1.

### Portes encore fermées

- **F1ZBX / R3** : la paire 145.075 / 145.675 MHz représente **2 mémoires RX distinctes** si la porte est franchie. La validation réelle depuis Mortain exige toujours **2 sessions RX indépendantes** sur la sortie identifiée 145.675 MHz. Deux sessions ne créent pas deux mémoires supplémentaires.
- **F5ZHA** : recontrôle Sprint 65, le REF courant continue d'afficher F5ZHA actif avec **145.4675 / 432.575 MHz**. La valeur conflictuelle RepeaterBook 431.4125 MHz reste classée secondaire stale avec vérification affichée **2017-02-17** et `Off-Air`. La porte exige toujours une source locale actuelle ou autoritative équivalente et une validation de pertinence/réception depuis Mortain.
- **F1ZOV** : 431.975 MHz reste bloquée ; recontrôle du 11 août 2026, le Radio Club Nord Cotentin marque toujours le relais **En Maintenance**.
- **F6ZES Sourdeval** : recontrôle Sprint 65, le REF confirme toujours site/responsable/locator/altitude mais ne renseigne toujours ni fréquence, ni mode, ni état opérationnel exploitable. Delta candidat **0** et `sourdeval_must_not_be_guessed: true`.

### Inventaires techniques — Sprint 66

`research/sprint-66-technical-inventory-boundaries.json` pousse les recherches vers les inventaires nominatifs sans abaisser les portes de preuve.

- **F5ZHA** : l'association locale ARAM53 est identifiable comme active en 2026, mais son existence ne valide aucune fréquence ; aucune publication technique locale actuelle exploitée ne ferme la réconciliation.
- **F6ZES** : toujours aucun champ fréquence/mode/état exploitable ; delta 0, aucune conjecture.
- **Étel** : une offre DIRM 2026 confirme **17 stations radio** maintenues de Penmarc'h à Biarritz dans un contexte MHF/VHF, mais ne donne ni inventaire nominatif ni canaux ; aucun site Ch64 n'en découle.
- **Corsen** : le Stiff est encore revalidé comme infrastructure radio actuelle et par un marché de rénovation 2026, sans mapping Ch79. Une source secondaire non datée restitue Fréhel/Bodic/Batz/Stiff/Raz sur Ch79 : piste de recherche seulement, jamais validation primaire actuelle.
- Le Guide Marine 2026 a de nouveau retourné `cache miss` : aucune inférence depuis un PDF non lu.

Résultat : **0 porte franchie, 0 ajout éligible, candidat/preview 142/142, plafond 147, revue 3/9, 6 blocages**.

### Recontrôle primaire — Sprint 65

`research/sprint-65-primary-recheck.json` rafraîchit les limites courantes sans modifier les portes existantes.

- F5ZHA : paire REF inchangée, source locale/autoritative équivalente toujours manquante, terrain toujours requis.
- F6ZES : fréquence/mode toujours non résolus.
- Normandie : **0 porte franchie**, candidat/preview **142/142**, plafond connu **147**, revue **3/9**, **6 blocages**, **0 ajout éligible**.

### Contrat double RX — Sprint 64

`research/sprint-64-dual-rx-contract.json` verrouille la séparation entre mémoires et preuves terrain.

- R3 : `R3-OUT` 145.675 et `R3-IN` 145.075 sont les **2 membres de paire** ; `CTRL-ZHY` reste un contrôle facultatif hors paire.
- La porte R3 exige toujours 2 sessions indépendantes, mais le delta futur reste exactement **+2 mémoires** si elle passe.
- CROSS Étel Ch64 conserve **156.225 + 160.825 MHz**, soit 2 mémoires RX si le canal devient publiable.
- CROSS Corsen Ch79 conserve **156.975 + 161.575 MHz**, soit 2 mémoires RX si le canal devient publiable.
- Les portes de source/site restent obligatoires : ce contrat ne publie rien et n'ajoute aucune mémoire aujourd'hui.

### Revalidation Sprint 63

`research/sprint-63-source-revalidation.json` documente la passe sans modifier les critères de promotion ni le candidat.

Résultat : **0 porte franchie, 0 ajout éligible, candidat/preview 142/142, plafond connu 147, revue 3/9, 6 blocages**.

### Scan adjacent Sprint 61

Le recontrôle REF courant des départements **35 / 50 / 53 / 61** ne fait apparaître **aucun nouveau relais analogique actif non déjà suivi**. Delta candidat : **0**.

### Terrain R3 et F5ZHA

```powershell
python tools\build_normandie_v04_r3_validation_pack.py
python tools\record_normandie_v04_r3_observation.py --help
python tools\build_normandie_v04_f5zha_validation_pack.py
python tools\record_normandie_v04_f5zha_observation.py --help
```

Le protocole `research/normandie-v0.4/f5zha-mortain-validation.json` conserve la valeur 431.4125 MHz uniquement comme sonde diagnostique. Une observation terrain ne peut jamais fermer le conflit de source.

### Readiness, revue et handoff — Sprints 40 à 59

```powershell
python tools\build_normandie_v04_readiness_report.py
python tools\build_normandie_v04_promotion_scenarios.py
python tools\build_normandie_v04_evidence_report.py
python tools\build_normandie_v04_internal_promotion_plan.py
python tools\check_normandie_v04_source_consistency.py
python tools\check_normandie_v04_source_freshness.py
python tools\build_normandie_v04_decision_dossier.py
python tools\build_normandie_v04_candidate_preview.py
python tools\build_normandie_v04_candidate_diff.py
python tools\build_normandie_v04_release_blockers.py
python tools\build_normandie_v04_review_checklist.py
python tools\run_normandie_v04_prepublication_audit.py
python tools\build_normandie_v04_review_snapshot.py
python tools\build_normandie_v04_review_manifest.py
python tools\check_normandie_v04_review_drift.py --baseline <manifest.json> --require-clean
python tools\run_normandie_v04_publication_dry_run.py --baseline <manifest.json>
```

État courant vérifié : **3/9 points de revue**, **6 blocages ouverts**, **0 ajout éligible**, candidat/preview **142/142**, release toujours non prête.

## Bretagne v0.1

Dossier principal : `research/bretagne-v0.1/public-maritime-radio.json`.

### Inventaire technique — Sprint 66

Le périmètre technique courant est mieux borné sans attribution nouvelle : l'offre DIRM `2026-2341297` confirme les **17 stations radio** du CROSS Étel et le contexte MHF/VHF, mais pas leurs noms/canaux ; côté Corsen, Stiff reste une infrastructure radio actuelle sans mapping Ch79. La chaîne secondaire Fréhel/Bodic/Batz/Stiff/Raz reste une cible de recherche uniquement.

### Recontrôle primaire — Sprint 65

La page du ministère chargée de la mer, mise à jour le **19 juin 2026**, maintient actuellement deux informations distinctes : le canal 16 annonce les diffusions météo CROSS sur **79 et 80**, et les canaux **63 et 64** diffusent un bulletin côtier permanent notamment dans le Morbihan. Cette déclaration reste régionale et **ne nomme aucun site Ch64**.

La page DIRM du CROSS Étel, mise à jour le **24 novembre 2025**, maintient les vacations annoncées sur 16 puis diffusées sur 79/80 et la diffusion continue **Étel + Chassiron sur Ch63**. Elle ne nomme toujours aucun site Ch64 ; cette absence ne prouve ni fonctionnement ni arrêt du canal 64.

La page DIRM du CROSS Corsen, mise à jour le **24 mars 2026**, confirme toujours le réseau VHF/MHF permanent et les bulletins météo diffusés depuis des stations littorales, mais ne fournit toujours aucun mapping **Ch79 ↔ station**.

Ces trois sources primaires actuelles renforcent les frontières documentaires, sans produire de nouvelle attribution ni de nouveau delta RF.

### CROSS Corsen — canal 79

`research/bretagne-v0.1/corsen-channel79-evidence.json` reste le dossier courant.

- La paire RX **156.975 / 161.575 MHz** représente **2 mémoires RX distinctes** si Ch79 devient publiable ; elle était déjà connue et ne crée aucun nouveau delta RF aujourd'hui.
- Le contexte primaire actuel confirme le réseau radio Corsen sans identifier le site Ch79.
- Une source locale actuelle du Club de Voile de la Baie d'Erquy associe Ch79 à **Cap Fréhel** et **Bodic** ; elle reste secondaire.
- **Cap Fréhel** et **Stiff / Ouessant** sont revalidés comme infrastructures radio CROSS actuelles, sans attribution Ch79.
- Une source primaire historique 2003 documente Ch79 dans l'architecture Corsen/Ouessant, mais ne vaut pas validation actuelle.
- Le bilan officiel Corsen 2025 reste identifié mais non extractible dans le workflow courant.
- Le **Guide Marine 2026 de Météo-France** reste une cible primaire. Une nouvelle tentative le 11 août 2026 retourne toujours `cache miss` ; le PDF n'a pas été lu et aucune attribution Ch79 n'en est déduite.

### CROSS Étel — canal 64

`research/bretagne-v0.1/etel-channel64-evidence.json` documente toujours un **conflit entre sources primaires actuelles** :

- le ministère maintient l'affirmation **canaux 63 et 64 dans le Morbihan** ;
- la page actuelle du CROSS Étel nomme Étel et Chassiron en diffusion continue sur **63** ;
- le planning météo lié actuellement par le CROSS liste ses émetteurs/canaux sans aucun 64 ;
- le bilan 2025 décrit **16 stations VHF + 2 MF** et les stations renforcées **Étel / Chassiron / Ferret sur 63**, sans mentionner 64.

La paire RX **156.225 / 160.825 MHz** représente **2 mémoires RX distinctes** si Ch64 devient publiable. Elle était déjà présente dans la recherche : delta RF actuel **0**. La convergence opérationnelle locale sur Ch63 ne prouve ni l'opération actuelle de Ch64 ni son arrêt, et aucun site Ch64 n'est attribué.

L'offre technique DIRM 2026 mentionne **17 stations radio** maintenues ; ce nombre n'est pas assimilé arithmétiquement aux 16 VHF + 2 MF faute de définition commune.

## Historique et architecture

- [SPRINT-29-MORTAIN-BRETAGNE-RADIO-RESEARCH.md](SPRINT-29-MORTAIN-BRETAGNE-RADIO-RESEARCH.md)
- [research/sprint-30-34-summary.md](research/sprint-30-34-summary.md)
- [research/sprint-35-39-summary.md](research/sprint-35-39-summary.md)
- [research/sprint-40-44-summary.md](research/sprint-40-44-summary.md)
- [research/sprint-45-49-summary.md](research/sprint-45-49-summary.md)
- [research/sprint-50-54-summary.md](research/sprint-50-54-summary.md)
- [research/sprint-55-60-summary.md](research/sprint-55-60-summary.md)
- [research/sprint-61-summary.md](research/sprint-61-summary.md)
- [research/sprint-62-summary.md](research/sprint-62-summary.md)
- [research/sprint-63-summary.md](research/sprint-63-summary.md)
- [research/sprint-64-summary.md](research/sprint-64-summary.md)
- [research/sprint-65-summary.md](research/sprint-65-summary.md)
- [research/sprint-66-summary.md](research/sprint-66-summary.md)

Architecture publique : `website/src/lib/chirpPack.ts`, `website/src/lib/annecyPack.ts`, `website/src/lib/packRegistry.ts`.

## Tests principaux

```powershell
python tests\test_paired_rx_policy.py
python tests\test_mortain_bretagne_radio_research.py
python tests\test_normandie_v04_readiness.py
python tests\test_normandie_v04_evidence_pipeline.py
python tests\test_normandie_v04_decision_pipeline.py
python tests\test_normandie_v04_prepublication_audit.py
python tests\test_normandie_v04_review_handoff.py
python tests\test_sprint60_revalidation.py
python tests\test_sprint61_research.py
python tests\test_sprint62_primary_reference_boundaries.py
python tests\test_sprint63_blocker_revalidation.py
python tests\test_sprint64_dual_rx_contract.py
python tests\test_sprint65_primary_recheck.py
python tests\test_sprint66_technical_inventory_boundaries.py
python tests\test_etel_network_research.py
python tests\test_bretagne_research_scaffold.py
python tests\test_emergency_relay_research.py
python tests\test_site_files.py
python tests\test_pack_registry.py
```

## Synchronisation locale

```powershell
cd "C:\Users\cross\Documents\CODE\PROJETS\RadioPack-France"

git pull --ff-only

python tools\run_normandie_v04_checks.py --extended
python tests\test_sprint60_revalidation.py
python tests\test_sprint61_research.py
python tests\test_sprint62_primary_reference_boundaries.py
python tests\test_sprint63_blocker_revalidation.py
python tests\test_sprint64_dual_rx_contract.py
python tests\test_sprint65_primary_recheck.py
python tests\test_sprint66_technical_inventory_boundaries.py
python tests\test_etel_network_research.py
python tests\test_bretagne_research_scaffold.py
python tests\test_emergency_relay_research.py
python tests\test_site_files.py
python tests\test_pack_registry.py

git status
```

Résultat attendu : `nothing to commit, working tree clean`.

Les détails historiques restent dans `CHANGELOG.md` et les dossiers `research/`. Les exports RadioPack sont destinés à l'écoute ; voir `NOTICE_LEGAL.md`.
