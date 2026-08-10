# RadioPack France

Codeplugs CHIRP régionaux, documentés et générés à partir de données publiques vérifiables pour les radios Quansheng UV-K5.

## État actuel — Sprint 61 / 0.21.50

Repère de compatibilité documentaire conservé pour les garde-fous historiques : **État actuel — Sprint 39**.

Packs publics immuables :

- **Normandie v0.3.1** — 139 mémoires RX ;
- **Annecy–Alpes–Léman v0.2** — 65 mémoires RX, variante 48 sans aviation.

Recherche : **Normandie v0.4** à **142 mémoires** internes, plafond de travail connu **147 mémoires**, **Bretagne v0.1** non publique et Annecy–Alpes–Léman v0.3 non publique.

Le générateur public ne propose que les versions publiées. Point de reprise : `PROJECT_STATUS.md`, `research/project-resume-state.json`, `research/sprint-55-60-summary.md` et `research/sprint-61-summary.md`.

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
- Un conflit entre sources primaires actuelles doit être réconcilié avant promotion.
- Une absence dans un document local actuel ne constitue pas automatiquement une preuve d'arrêt.
- Des nombres de stations fondés sur des unités non définies identiquement ne sont pas réconciliés par simple calcul.
- `research/paired-rx-policy.json` impose les deux côtés RX lorsqu'une liaison duplex/split distincte est vérifiée.
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
research/normandie-v0.4/f5zha-mortain-validation.json
research/normandie-v0.4/f6zes-revalidation.json
research/normandie-v0.4/mortain-adjacent-ref-scan.json
```

Le candidat interne ajoute actuellement seulement 145.0875 MHz, 145.1000 MHz et 431.2500 MHz aux 139 mémoires figées de v0.3.1.

### Portes encore fermées

- F1ZBX / R3 : 145.075 / 145.675 MHz, validation réelle depuis Mortain requise.
- F5ZHA : 145.4675 / 432.575 MHz, conflit source + couverture utile à fermer.
- F1ZOV : 431.975 MHz, opérateur local toujours en maintenance même si le REF général le liste actif.
- F6ZES Sourdeval : le REF courant confirme site/responsable/locator/altitude mais ne renseigne toujours ni fréquence, ni bande, ni mode, ni état. Delta candidat **0** et `sourdeval_must_not_be_guessed: true`.

### Scan adjacent Sprint 61

Le recontrôle REF courant des départements **35 / 50 / 53 / 61** ne fait apparaître **aucun nouveau relais analogique actif non déjà suivi**. Les autres lignes sont déjà documentées, numériques, arrêtées ou incomplètes. Delta candidat : **0**.

### Terrain R3 et F5ZHA

```powershell
python tools\build_normandie_v04_r3_validation_pack.py
python tools\record_normandie_v04_r3_observation.py --help
python tools\build_normandie_v04_f5zha_validation_pack.py
python tools\record_normandie_v04_f5zha_observation.py --help
```

Le protocole `research/normandie-v0.4/f5zha-mortain-validation.json` conserve la valeur historique 431.4125 MHz uniquement comme sonde diagnostique. Une observation terrain ne peut jamais fermer le conflit de source.

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

Le snapshot capture un état de revue déterministe. Le manifeste surveille onze entrées par SHA-256, y compris le CSV public Normandie v0.3.1 et `packRegistry.ts`. Toute dérive impose une nouvelle revue. Le dry-run ne modifie ni CSV public ni registre.

État courant vérifié : **3/9 points de revue**, **6 blocages ouverts**, **0 ajout éligible**, candidat/preview **142/142**, release toujours non prête.

## Bretagne v0.1

Dossier principal : `research/bretagne-v0.1/public-maritime-radio.json`. Les recherches conservent les contextes CROSS Corsen / Étel, Baie du Mont-Saint-Michel, Pointe de Penmarc'h, Pointe du Raz, CROSS Nouvelle génération, Penmarc'h, Groix, Belle-Ile, Étel et les fréquences 156.800 MHz, 161.575 MHz, 161.625 MHz, 160.775 MHz et 160.825 MHz.

### CROSS Corsen — canal 79

`research/bretagne-v0.1/corsen-channel79-evidence.json` reste le dossier courant.

- La paire RX **156.975 / 161.575 MHz** était déjà connue et ne crée aucun nouveau delta RF.
- Le contexte primaire actuel confirme le réseau radio Corsen sans identifier le site Ch79.
- Une source locale actuelle du Club de Voile de la Baie d'Erquy associe Ch79 à **Cap Fréhel** et **Bodic** ; elle est conservée comme indice secondaire local actuel uniquement.
- Le bilan officiel Corsen 2025 est identifié, mais son PDF de 14,6 Mio n'a pas pu être chargé dans le workflow courant ; aucune donnée canal/site n'en est déduite.
- Cap Fréhel et Bodic restent des priorités de revalidation primaire, sans attribution de site ni publication.

### CROSS Étel — canal 64

`research/bretagne-v0.1/etel-channel64-evidence.json` documente désormais un **conflit entre sources primaires actuelles** :

- le ministère, page mise à jour le 19 juin 2026, maintient l'affirmation **canaux 63 et 64 dans le Morbihan** ;
- la page actuelle du CROSS Étel nomme Étel en diffusion continue sur **63** ;
- le planning météo lié actuellement par le CROSS liste ses émetteurs/canaux sans aucun 64 ;
- le bilan 2025 décrit **16 stations VHF + 2 MF**, les émetteurs météo réguliers et les stations renforcées **Étel / Chassiron / Ferret sur 63**, sans mentionner 64.

Cette absence locale de 64 ne vaut pas preuve d'arrêt. Aucun site n'est attribué au canal 64 tant qu'une source primaire ne réconcilie pas la divergence. L'offre technique DIRM 2026 mentionne **17 stations radio** maintenues ; ce nombre n'est pas assimilé arithmétiquement aux 16 VHF + 2 MF faute de définition commune.

La paire RX **156.225 / 160.825 MHz** était déjà présente dans la recherche : delta RF **0**.

## Historique et architecture

- [SPRINT-29-MORTAIN-BRETAGNE-RADIO-RESEARCH.md](SPRINT-29-MORTAIN-BRETAGNE-RADIO-RESEARCH.md)
- [research/sprint-30-34-summary.md](research/sprint-30-34-summary.md)
- [research/sprint-35-39-summary.md](research/sprint-35-39-summary.md)
- [research/sprint-40-44-summary.md](research/sprint-40-44-summary.md)
- [research/sprint-45-49-summary.md](research/sprint-45-49-summary.md)
- [research/sprint-50-54-summary.md](research/sprint-50-54-summary.md)
- [research/sprint-55-60-summary.md](research/sprint-55-60-summary.md)
- [research/sprint-61-summary.md](research/sprint-61-summary.md)

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
python tests\test_etel_network_research.py
python tests\test_bretagne_research_scaffold.py
python tests\test_emergency_relay_research.py
python tests\test_site_files.py
python tests\test_pack_registry.py

git status
```

Résultat attendu : `nothing to commit, working tree clean`.

Les détails historiques restent dans `CHANGELOG.md` et les dossiers `research/`. Les exports RadioPack sont destinés à l'écoute ; voir `NOTICE_LEGAL.md`.
