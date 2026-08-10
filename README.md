# RadioPack France

Codeplugs CHIRP régionaux, documentés et générés à partir de données publiques vérifiables pour les radios Quansheng UV-K5.

## État actuel — Sprint 44

Repère de compatibilité documentaire conservé pour les garde-fous historiques : **État actuel — Sprint 39**.

Packs publics immuables :

- **Normandie v0.3.1** — 139 mémoires RX ;
- **Annecy–Alpes–Léman v0.2** — 65 mémoires RX, variante 48 sans aviation.

Recherche : **Normandie v0.4** à **142 mémoires** internes, plafond de travail connu **147 mémoires**, **Bretagne v0.1** non publique et Annecy–Alpes–Léman v0.3 non publique.

Le générateur public ne propose que les versions publiées. Point de reprise : `PROJECT_STATUS.md` et `research/project-resume-state.json`.

## Règles permanentes

- RX uniquement : `Duplex=off`, `Offset=0.000000`.
- Pas de remplissage artificiel ; maximum 200 mémoires.
- Versions publiées immuables.
- Géométrie, altitude, puissance ou rayon annoncé ne valent pas preuve de réception.
- Une recherche infructueuse n'est pas une preuve d'arrêt.
- Une fréquence non résolue n'est jamais devinée.
- `research/paired-rx-policy.json` impose les deux côtés RX lorsqu'une liaison duplex/split distincte est vérifiée.
- Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint.

## Normandie v0.4 — Mortain-Bocage / Sud-Manche

Le périmètre suit la couverture radio utile dans les départements 50, 35, 53 et 61. Stations suivies : **F5ZHY**, **F6ZES**, **F6ZCE**, **F1ZBX**, **F5ZHA**, **F1ZOV**.

Fichiers de vérité :

```text
research/normandie-v0.4/mortain-bocage-coverage.json
research/normandie-v0.4/candidate-memory-delta.json
research/normandie-v0.4/internal-candidate-map.json
research/normandie-v0.4/promotion-gates.json
research/normandie-v0.4/blocked-station-revalidation.json
research/normandie-v0.4/external-evidence-matrix.json
research/normandie-v0.4/r3-mortain-field-validation.json
research/normandie-v0.4/f5zha-mortain-validation.json
```

Le candidat interne ajoute actuellement seulement 145.0875 MHz, 145.1000 MHz et 431.2500 MHz aux 139 mémoires figées de v0.3.1.

### Portes encore fermées

- F1ZBX / R3 : 145.075 / 145.675 MHz, validation réelle depuis Mortain requise.
- F5ZHA : 145.4675 / 432.575 MHz, conflit source + couverture utile à fermer.
- F1ZOV : 431.975 MHz, opérateur local toujours en maintenance.
- F6ZES Sourdeval : site connu mais fréquence/mode non résolus ; `sourdeval_must_not_be_guessed: true`.

### Terrain R3 et F5ZHA

```powershell
python tools\build_normandie_v04_r3_validation_pack.py
python tools\record_normandie_v04_r3_observation.py --help
python tools\build_normandie_v04_f5zha_validation_pack.py
python tools\record_normandie_v04_f5zha_observation.py --help
```

Le protocole `research/normandie-v0.4/f5zha-mortain-validation.json` conserve la valeur historique 431.4125 MHz uniquement comme sonde diagnostique. Une observation terrain ne peut jamais fermer le conflit de source.

### Readiness, scénarios et preuves — Sprints 40 à 44

```powershell
python tools\build_normandie_v04_readiness_report.py
python tools\build_normandie_v04_promotion_scenarios.py
python tools\build_normandie_v04_evidence_report.py
python tools\build_normandie_v04_internal_promotion_plan.py
```

`build_normandie_v04_readiness_report.py` conserve la publication bloquée. `build_normandie_v04_promotion_scenarios.py` couvre les 8 scénarios 142→147. Le nouveau rapport de preuves sépare paramètres techniques, statut opérateur, réception terrain et conflits de sources. Le plan de promotion interne ne modifie jamais le candidat et, au Sprint 44, doit contenir 0 ajout éligible.

## Bretagne v0.1

Dossier principal : `research/bretagne-v0.1/public-maritime-radio.json`. Les recherches conservent les contextes CROSS Corsen / Étel, Baie du Mont-Saint-Michel, Pointe de Penmarc'h, Pointe du Raz, CROSS Nouvelle génération, Penmarc'h, Groix, Belle-Ile, Étel et les fréquences 156.800 MHz, 161.575 MHz, 161.625 MHz, 160.775 MHz, 160.825 MHz. Les relais F5ZZH, F5ZIS, F5ZIT, F1ZBZ et F5ZPE restent documentés sans publication.

## Historique et architecture

- [SPRINT-29-MORTAIN-BRETAGNE-RADIO-RESEARCH.md](SPRINT-29-MORTAIN-BRETAGNE-RADIO-RESEARCH.md)
- [research/sprint-30-34-summary.md](research/sprint-30-34-summary.md)
- [research/sprint-35-39-summary.md](research/sprint-35-39-summary.md)
- [research/sprint-40-44-summary.md](research/sprint-40-44-summary.md)

Architecture publique : `website/src/lib/chirpPack.ts`, `website/src/lib/annecyPack.ts`, `website/src/lib/packRegistry.ts`.

## Tests principaux

```powershell
python tests\test_paired_rx_policy.py
python tests\test_mortain_bretagne_radio_research.py
python tests\test_normandie_v04_readiness.py
python tests\test_normandie_v04_evidence_pipeline.py
python tests\test_bretagne_research_scaffold.py
python tests\test_emergency_relay_research.py
python tests\test_site_files.py
python tests\test_pack_registry.py
```

## Synchronisation locale

```powershell
cd "C:\Users\cross\Documents\CODE\PROJETS\RadioPack-France"

git pull --ff-only

python tests\test_bretagne_research_scaffold.py
python tests\test_emergency_relay_research.py
python tests\test_site_files.py
python tests\test_pack_registry.py
python tests\test_normandie_v04_readiness.py
python tests\test_normandie_v04_evidence_pipeline.py

git status
```

Résultat attendu : `nothing to commit, working tree clean`.

Les détails historiques restent dans `CHANGELOG.md` et les dossiers `research/`. Les exports RadioPack sont destinés à l'écoute ; voir `NOTICE_LEGAL.md`.
