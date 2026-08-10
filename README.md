# RadioPack France

Codeplugs CHIRP régionaux, documentés et générés à partir de données publiques vérifiables pour les radios Quansheng UV-K5.

Le projet privilégie une approche prudente : aucune fréquence n'est ajoutée uniquement pour remplir un pack, les sources doivent être identifiables, les versions publiées sont immuables et les exports restent configurés pour l'écoute.

## État actuel — Sprint 44

Packs publics :

- **Normandie v0.3.1** — 139 mémoires RX, publiée et immuable ;
- **Annecy–Alpes–Léman v0.2** — 65 mémoires RX, variante 48 mémoires sans aviation, publiée et immuable.

Packs en recherche :

- **Normandie v0.4** — candidat interne non public à **142 mémoires** ;
- **Annecy–Alpes–Léman v0.3** — recherche uniquement ;
- **Bretagne v0.1** — recherche uniquement, aucune mémoire publique et aucun nombre cible artificiel.

Le générateur public `/generateur` continue de proposer uniquement les versions réellement publiées. Le point de reprise humain est `PROJECT_STATUS.md` et l'état machine correspondant est `research/project-resume-state.json`.

## Principes permanents

- Réception seule : `Duplex=off`.
- `Offset=0.000000`.
- Noms de mémoires limités à 10 caractères.
- Maximum 200 mémoires par pack.
- Pas de remplissage artificiel.
- Une source identifiée n'est pas automatiquement une fréquence validée.
- Une même fréquence RF n'est pas dupliquée uniquement pour changer son étiquette géographique, son site ou sa fonction.
- Une version régionale publiée est immuable ; toute évolution crée une nouvelle version et une nouvelle revue.
- Un rôle ADRASEC n'est jamais déduit uniquement de l'implantation géographique d'un relais.
- Une infrastructure radio actuelle vérifiée ne vaut pas automatiquement validation d'un canal ou d'une fréquence précise.
- Une preuve de couverture dans un secteur ne permet pas d'identifier automatiquement le site émetteur.
- La géométrie, l'altitude, la puissance ou un rayon d'usage annoncé ne valent pas preuve de réception réelle.
- Pour l'état courant d'un relais géré par une association locale, la page opérationnelle de l'exploitant est prioritaire sur un annuaire général lorsqu'ils divergent ; le conflit reste documenté.
- Une recherche infructueuse n'est jamais transformée en preuve d'arrêt ou d'absence.
- Une fréquence non résolue n'est jamais devinée.
- Les réseaux professionnels privés de sécurité/secours restent hors des packs lorsqu'ils ne sont pas explicitement destinés à l'écoute publique ou au service amateur ouvert.

## Politique paired RX

La règle commune est définie dans `research/paired-rx-policy.json`. Lorsqu'une liaison publique est nativement duplex ou split et que ses deux fréquences distinctes sont vérifiées, RadioPack prévoit les deux côtés en réception. Chaque mémoire reste `Duplex=off` et `Offset=0.000000`.

Plans communs :

```text
research/paired-rx-next-version-plan.json
research/paired-rx-deduplicated-memory-plan.json
```

Les comptes paired RX de recherche actuels restent 12 fréquences uniques pour Normandie v0.4, 10 pour Annecy–Alpes–Léman v0.3 et 29 pour Bretagne v0.1. Ce ne sont ni des tailles finales de packs ni des objectifs de remplissage.

## Politique secours / ADRASEC

La politique commune est `research/emergency-radio-policy.json`. Les relais/transpondeurs radioamateurs documentés, canaux maritimes publics et diffusions de sécurité explicitement destinées aux usagers peuvent être étudiés. Les réseaux opérationnels internes PPDR/PMR privés restent exclus.

# Normandie v0.4 — travail actif

Priorité géographique : **Mortain-Bocage / Sud-Manche**, avec contrôle volontaire des départements 50, 35, 53 et 61. Les stations suivies comprennent notamment **F5ZHY**, **F6ZES**, **F6ZCE**, **F1ZBX**, **F5ZHA** et **F1ZOV**.

Fichiers de vérité :

```text
research/normandie-v0.4/pack-plan.json
research/normandie-v0.4/mortain-bocage-coverage.json
research/normandie-v0.4/paired-rx-refresh.json
research/normandie-v0.4/candidate-memory-delta.json
research/normandie-v0.4/internal-candidate-map.json
research/normandie-v0.4/promotion-gates.json
research/normandie-v0.4/blocked-station-revalidation.json
research/normandie-v0.4/external-evidence-matrix.json
research/normandie-v0.4/r3-mortain-field-validation.json
research/normandie-v0.4/r3-validation-pack.json
research/normandie-v0.4/f5zha-mortain-validation.json
```

## Candidat interne actuel — 142 mémoires

Le candidat conserve les 139 lignes de Normandie v0.3.1 comme préfixe exact et ajoute seulement :

- location interne provisoire 175 — `50-ZHY-IN` — 145.0875 MHz — F5ZHY ;
- location interne provisoire 176 — `53-ZCE-IN` — 145.1000 MHz — F6ZCE ;
- location interne provisoire 177 — `50-ZBL-U` — 431.2500 MHz — F1ZBL.

Ces positions sont internes et provisoires. Elles ne définissent pas la numérotation publique finale.

```powershell
python tools\build_normandie_v04_internal_candidate.py
```

## Portes connues et plafond de travail

Cinq fréquences restent exclues :

- R3 / F1ZBX Brocéliande — 145.075 / 145.675 MHz — validation RX réelle depuis Mortain requise ;
- F5ZHA Laval — 145.4675 / 432.575 MHz — conflit de source et pertinence/couverture locale à fermer ;
- F1ZOV Équeurdreville-Hainneville — 431.975 MHz — retour en service à confirmer chez l'exploitant local.

Le candidat est à 142 mémoires. Les trois portes connues représentent au maximum +5 mémoires, soit un plafond interne connu de **147 mémoires**. Ce nombre n'est pas une taille publique finale et F6ZES reste hors calcul tant qu'aucune fréquence exploitable n'est résolue.

```powershell
python tools\check_normandie_v04_promotion_gates.py
python tools\build_normandie_v04_readiness_report.py
python tools\build_normandie_v04_promotion_scenarios.py
```

## R3 / F1ZBX

L'ARA35 publie la paire 145.075 MHz entrée / 145.675 MHz sortie. La géométrie place Mortain à environ 119,3 km du site, dans le rayon d'usage de 150 km annoncé, sans que cela constitue une preuve de réception.

```powershell
python tools\build_normandie_v04_r3_validation_pack.py
python tools\record_normandie_v04_r3_observation.py --help
```

La porte demande au moins deux sessions RX indépendantes suffisamment identifiées et intelligibles sur 145.675 MHz.

## F5ZHA Laval

Le REF courant publie 145.4675 / 432.575 MHz. Une ancienne valeur secondaire 431.4125 MHz reste un conflit historique diagnostique uniquement. Le centre du locator `IN98OB86BQ` est à environ 65,6 km de la référence Mortain : cette géométrie justifie un test local mais ne prouve aucune réception.

```powershell
python tools\build_normandie_v04_f5zha_validation_pack.py
python tools\record_normandie_v04_f5zha_observation.py --help
```

Le protocole `research/normandie-v0.4/f5zha-mortain-validation.json` conserve `ZHA-VHF`, `ZHA-UHF` et `ZHA-OLD`. Les observations terrain peuvent documenter la pertinence locale mais **ne peuvent jamais fermer le conflit de source**. La promotion exige à la fois une couverture locale utile documentée et une réconciliation autoritative de la source.

## F1ZOV

La paire 430.375 / 431.975 MHz reste recoupée, mais le Radio Club Nord Cotentin indique actuellement F1ZOV **En Maintenance**. Le nouveau côté 431.975 MHz reste bloqué jusqu'au retour en service explicitement confirmé.

## F6ZES Sourdeval

Le REF confirme F6ZES à Sourdeval, responsable F1SMB, locator IN98MR93XV, altitude 230 m, mais sans fréquence ni mode exploitable dans la fiche vérifiée.

```text
sourdeval_must_not_be_guessed: true
```

F6ZES reste sans fréquence candidate et sans delta mémoire chiffré.

## Pipeline de preuves — Sprints 40 à 44

La matrice `research/normandie-v0.4/external-evidence-matrix.json` sépare maintenant les paramètres techniques, l'état opérateur, la preuve de réception et les conflits de sources.

```powershell
python tools\build_normandie_v04_evidence_report.py
python tools\build_normandie_v04_internal_promotion_plan.py
```

`build_normandie_v04_evidence_report.py` consolide R3, F5ZHA, F1ZOV et F6ZES sans modifier les portes. `build_normandie_v04_internal_promotion_plan.py` ne propose des ajouts que pour les portes réellement franchies et **ne modifie jamais automatiquement le candidat interne**. À l'état Sprint 44, aucune porte n'est franchie : le plan attendu contient 0 ajout et reste à 142 mémoires.

## Contrôles Normandie v0.4

```powershell
python tools\run_normandie_v04_checks.py
python tools\run_normandie_v04_checks.py --extended
```

Tests dédiés :

```powershell
python tests\test_normandie_v04_candidate_delta.py
python tests\test_normandie_v04_internal_candidate.py
python tests\test_normandie_v04_promotion_gates.py
python tests\test_normandie_v04_field_tools.py
python tests\test_normandie_v04_readiness.py
python tests\test_normandie_v04_evidence_pipeline.py
```

# Annecy–Alpes–Léman v0.3 — recherche

La v0.2 publique reste figée. La recherche suivante est dans `research/annecy-alpes-leman-v0.3/`. Les relais/transpondeurs et satellites split restent soumis aux mêmes règles : source actuelle, déduplication RF, paired RX, TX bloqué, aucune publication avant revue explicite.

# Bretagne v0.1 — recherche

La Bretagne reste volontairement non publique. Le dossier principal VHF maritime reste `research/bretagne-v0.1/public-maritime-radio.json` avec les autres inventaires sous `research/bretagne-v0.1/`.

Le zonage conserve Bretagne Nord / Manche Ouest — CROSS Corsen, Bretagne Sud / Atlantique — CROSS Etel, et interface Penmarc'h / Finistère Sud. Les détails Baie du Mont-Saint-Michel, Pointe de Penmarc'h, Pointe du Raz, CROSS Nouvelle génération, Penmarc'h, Groix, Belle-Ile, Étel et les fréquences 156.800 MHz / 161.575 MHz / 161.625 MHz / 160.775 MHz / 160.825 MHz restent documentés dans les fichiers de recherche dédiés. Les relais F5ZZH, F5ZIS, F5ZIT, F1ZBZ et F5ZPE restent également documentés.

# Packs publics actuels

```text
/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv
/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2-sans-aviation.csv
/downloads/normandie/radiopack-france-normandie-v0.3.1.csv
```

Catalogue public : `Annecy 65 / 48 + Normandie 139`. Bretagne v0.1, Normandie v0.4 et Annecy–Alpes–Léman v0.3 restent hors de `website/src/lib/packRegistry.ts`.

# Architecture et historique

```text
website/src/lib/chirpPack.ts
website/src/lib/annecyPack.ts
website/src/lib/packRegistry.ts
```

Documents :

- [REGIONAL-PACK-WORKFLOW.md](REGIONAL-PACK-WORKFLOW.md)
- [SPRINT-29-MORTAIN-BRETAGNE-RADIO-RESEARCH.md](SPRINT-29-MORTAIN-BRETAGNE-RADIO-RESEARCH.md)
- [research/sprint-30-34-summary.md](research/sprint-30-34-summary.md)
- [research/sprint-35-39-summary.md](research/sprint-35-39-summary.md)
- [research/sprint-40-44-summary.md](research/sprint-40-44-summary.md)

# Tests principaux

```powershell
python tests\test_generator.py
python tests\test_site_files.py
python tests\test_pack_registry.py
python tests\test_regional_pack_starter.py
python tests\test_paired_rx_policy.py
python tests\test_paired_rx_memory_plan.py
python tests\test_normandie_v04_candidate_delta.py
python tests\test_normandie_v04_internal_candidate.py
python tests\test_normandie_v04_promotion_gates.py
python tests\test_normandie_v04_field_tools.py
python tests\test_normandie_v04_readiness.py
python tests\test_normandie_v04_evidence_pipeline.py
python tests\test_bretagne_research_scaffold.py
python tests\test_emergency_relay_research.py
python tests\test_mortain_bretagne_radio_research.py
```

Après les tests :

```powershell
git status
```

Résultat attendu :

```text
nothing to commit, working tree clean
```

# Synchroniser le dépôt local

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

# Prochaines priorités

1. exécuter le protocole R3 depuis Mortain-Bocage ;
2. utiliser le mini-pack F5ZHA et l'enregistreur pour mesurer sa pertinence locale ;
3. fermer le conflit F5ZHA par une source suffisamment autoritative ;
4. surveiller le retour en service de F1ZOV ;
5. trouver une seconde source actuelle donnant fréquence et mode pour F6ZES ;
6. ne définir une taille publique Normandie v0.4 qu'après revue explicite ;
7. poursuivre Bretagne / CROSS / ADRASEC et Annecy v0.3 sans modifier les packs publics ;
8. ne publier aucune nouvelle mémoire tant que le readiness reste négatif.

# Maintenance

Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint. La CI doit évoluer avec le contrat du sprint.

Les caches Python (`__pycache__/` et `*.py[cod]`) et les dossiers `generated/` prévus sont ignorés par Git. Le détail historique reste dans [CHANGELOG.md](CHANGELOG.md) et dans les résumés de sprint du dossier `research/`.

# Sécurité et usage

Les exports RadioPack sont destinés à l'écoute. Voir [NOTICE_LEGAL.md](NOTICE_LEGAL.md) pour les précautions et limites d'utilisation.
