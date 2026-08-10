# RadioPack France

Codeplugs CHIRP régionaux, documentés et générés à partir de données publiques vérifiables pour les radios Quansheng UV-K5.

Le projet privilégie une approche prudente : aucune fréquence n'est ajoutée uniquement pour remplir un pack, les sources doivent être identifiables, les versions publiées sont immuables et les exports restent configurés pour l'écoute.

## État actuel — Sprint 39

Packs publics :

- **Normandie v0.3.1** — 139 mémoires RX, publiée et immuable ;
- **Annecy–Alpes–Léman v0.2** — 65 mémoires RX, variante **48 mémoires sans aviation**, publiée et immuable.

Packs en recherche :

- **Normandie v0.4** — candidat interne non public à **142 mémoires** ;
- **Annecy–Alpes–Léman v0.3** — recherche uniquement ;
- **Bretagne v0.1** — recherche uniquement, aucune mémoire publique et aucun nombre cible artificiel.

Le générateur public `/generateur` continue de proposer uniquement les versions réellement publiées.

Le point de reprise humain est :

```text
PROJECT_STATUS.md
```

L'état machine correspondant est :

```text
research/project-resume-state.json
```

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

## Politique paired RX — écouter les deux sens

La règle commune est définie dans :

```text
research/paired-rx-policy.json
```

Lorsqu'une liaison publique est nativement duplex ou split et que ses deux fréquences distinctes sont vérifiées, RadioPack prévoit les deux côtés en réception :

- VHF maritime duplex : navire → côte et côte → navire ;
- relais radioamateur : entrée et sortie ;
- transpondeur cross-band : les deux côtés publiés ;
- satellite split : montée et descente après revalidation opérationnelle.

Chaque mémoire reste `Duplex=off` et `Offset=0.000000`. Les tonalités CTCSS d'activation ou de montée restent documentaires et ne réactivent jamais le TX.

Plans communs :

```text
research/paired-rx-next-version-plan.json
research/paired-rx-deduplicated-memory-plan.json
```

Les comptes paired RX de recherche actuels restent **12 fréquences uniques pour Normandie v0.4**, **10 pour Annecy–Alpes–Léman v0.3** et **29 pour Bretagne v0.1**. Ce ne sont ni des tailles finales de packs ni des objectifs de remplissage.

## Politique secours / ADRASEC

La politique commune est :

```text
research/emergency-radio-policy.json
```

Peuvent être étudiés pour une future intégration RX : relais/transpondeurs radioamateurs ADRASEC/FNRASEC documentés, relais radioamateurs analogiques régionaux réellement utiles, canaux maritimes publics et diffusions de sécurité explicitement destinées aux usagers.

Les réseaux opérationnels internes PPDR/PMR de police, gendarmerie, SDIS, SAMU ou associations de secours restent exclus lorsqu'ils ne sont pas destinés à l'écoute publique ou au service amateur ouvert.

# Normandie v0.4 — travail actif

La v0.3.1 publique reste figée. Le travail courant est dans :

```text
research/normandie-v0.4/
```

Fichiers principaux :

```text
research/normandie-v0.4/pack-plan.json
research/normandie-v0.4/mortain-bocage-coverage.json
research/normandie-v0.4/paired-rx-refresh.json
research/normandie-v0.4/candidate-memory-delta.json
research/normandie-v0.4/internal-candidate-map.json
research/normandie-v0.4/promotion-gates.json
research/normandie-v0.4/blocked-station-revalidation.json
research/normandie-v0.4/r3-mortain-field-validation.json
research/normandie-v0.4/r3-validation-pack.json
research/normandie-v0.4/f5zha-mortain-validation.json
```

## Candidat interne actuel — 142 mémoires

Le candidat conserve les **139 lignes de Normandie v0.3.1 comme préfixe exact** et ajoute seulement trois côtés paired RX déjà suffisamment mûrs au niveau recherche :

- location interne provisoire `175` — `50-ZHY-IN` — **145.0875 MHz** ;
- location interne provisoire `176` — `53-ZCE-IN` — **145.1000 MHz** ;
- location interne provisoire `177` — `50-ZBL-U` — **431.2500 MHz**.

Ces positions sont internes et provisoires. Elles ne définissent pas la numérotation publique finale de v0.4.

Génération locale :

```powershell
python tools\build_normandie_v04_internal_candidate.py
```

## Portes de promotion connues

Cinq fréquences restent exclues du candidat interne :

- **R3 / F1ZBX Brocéliande** — 145.075 / 145.675 MHz — validation RX réelle depuis Mortain requise ;
- **F5ZHA Laval** — 145.4675 / 432.575 MHz — conflit de source et pertinence/couverture locale à fermer ;
- **F1ZOV Équeurdreville-Hainneville** — 431.975 MHz — retour en service à confirmer chez l'exploitant local.

Le checker est :

```powershell
python tools\check_normandie_v04_promotion_gates.py
```

Le candidat actuel est à **142 mémoires**. Les trois portes connues représentent un delta maximal de **+5 mémoires**, soit un plafond interne connu de **147 mémoires** si elles sont toutes réellement levées.

**147 n'est pas une taille publique finale.** F6ZES reste hors de ce plafond tant qu'aucune fréquence exploitable n'est résolue, et une levée de porte n'autorise jamais automatiquement une publication.

## R3 / F1ZBX — validation Mortain

L'ARA35 publie actuellement la paire :

- entrée : **145.075 MHz** ;
- sortie : **145.675 MHz**.

La géométrie place Mortain à environ 119,3 km du site, à l'intérieur du rayon d'usage de 150 km annoncé par l'opérateur, mais cela ne constitue pas une preuve de réception.

Mini-pack RX-only :

```powershell
python tools\build_normandie_v04_r3_validation_pack.py
```

Le pack contient :

- `R3-OUT` — 145.675 MHz — sonde principale ;
- `R3-IN` — 145.075 MHz — écoute opportuniste ;
- `CTRL-ZHY` — 145.6875 MHz — contrôle facultatif.

La porte R3 demande au moins **deux sessions RX indépendantes** avec identification suffisamment fiable et intelligibilité suffisante sur 145.675 MHz.

Enregistrer une observation :

```powershell
python tools\record_normandie_v04_r3_observation.py --help
```

## F5ZHA Laval — diagnostic Sprint 35–36

Le REF courant publie F5ZHA actif à Laval sur la paire analogique transparente :

- **145.4675 MHz** ;
- **432.575 MHz**.

Une ancienne valeur secondaire `431.4125 MHz` reste documentée comme conflit historique. Elle n'est pas retenue comme paire courante.

Le centre du locator REF `IN98OB86BQ` est à environ **65,6 km** de la référence Mortain. Cette géométrie justifie un test local mais ne prouve aucune réception.

Le mini-pack diagnostique contient :

- `ZHA-VHF` — 145.4675 MHz ;
- `ZHA-UHF` — 432.575 MHz ;
- `ZHA-OLD` — 431.4125 MHz — **sonde historique uniquement**.

Génération :

```powershell
python tools\build_normandie_v04_f5zha_validation_pack.py
```

Le mini-pack reste RX-only, non public et ne ferme jamais automatiquement le conflit de source.

## F1ZOV

La paire **430.375 / 431.975 MHz** reste recoupée, mais le Radio Club Nord Cotentin indique actuellement F1ZOV **En Maintenance**. La mémoire 430.375 MHz publiée en v0.3.1 reste immuable ; le nouveau côté 431.975 MHz reste bloqué jusqu'au retour en service explicitement confirmé par l'exploitant.

## F6ZES Sourdeval

Le REF courant confirme `F6ZES` à Sourdeval, responsable `F1SMB`, locator `IN98MR93XV`, altitude 230 m, mais sans fréquence ni mode exploitable dans la fiche vérifiée.

Règle obligatoire :

```text
sourdeval_must_not_be_guessed: true
```

F6ZES reste prioritaire mais sans fréquence candidate et sans delta mémoire chiffré.

## Readiness et scénarios — Sprints 37–38

Rapport de readiness :

```powershell
python tools\build_normandie_v04_readiness_report.py
```

Il produit localement un JSON et un Markdown dans `research/normandie-v0.4/generated/readiness/` avec :

- candidat actuel 142 ;
- cinq fréquences bloquées connues ;
- plafond interne connu 147 ;
- F6ZES séparé comme priorité non chiffrable ;
- `public_release_ready=false`.

Matrice des scénarios :

```powershell
python tools\build_normandie_v04_promotion_scenarios.py
```

Les trois portes connues donnent **8 combinaisons** possibles entre 142 et 147 mémoires. Chaque scénario reste un outil de planification, jamais une autorisation de promotion ou de publication.

## Contrôles Normandie v0.4

Commande locale ciblée :

```powershell
python tools\run_normandie_v04_checks.py
```

Commande étendue :

```powershell
python tools\run_normandie_v04_checks.py --extended
```

Tests dédiés :

```powershell
python tests\test_normandie_v04_candidate_delta.py
python tests\test_normandie_v04_internal_candidate.py
python tests\test_normandie_v04_promotion_gates.py
python tests\test_normandie_v04_field_tools.py
python tests\test_normandie_v04_readiness.py
```

# Annecy–Alpes–Léman v0.3 — recherche

La v0.2 publique reste figée. La recherche suivante est dans :

```text
research/annecy-alpes-leman-v0.3/
```

Les relais/transpondeurs et satellites split restent soumis aux mêmes règles : source actuelle, déduplication RF, paired RX lorsque pertinent, TX bloqué et aucune publication avant revue explicite.

# Bretagne v0.1 — recherche

La Bretagne reste volontairement non publique.

Principaux dossiers :

```text
research/bretagne-v0.1/public-maritime-radio.json
research/bretagne-v0.1/etel-network.json
research/bretagne-v0.1/emergency-relays.json
research/bretagne-v0.1/ref-analog-expansion.json
research/bretagne-v0.1/analog-coverage-redundancy-review.json
research/bretagne-v0.1/rennes-broceliande-linked-system.json
```

Le zonage conserve :

- Bretagne Nord / Manche Ouest — contexte CROSS Corsen ;
- Bretagne Sud / Atlantique — contexte CROSS Étel ;
- interface Penmarc'h / Finistère Sud.

Les canaux maritimes duplex conservent les deux côtés RX. Les émetteurs/sites non identifiés restent non attribués ; aucune infrastructure ou couverture sectorielle ne sert à inventer un canal.

Le cluster Côtes-d'Armor `432.650 MHz`, les dossiers ADRASEC, les réseaux CROSS et les relais régionaux restent documentés dans les fichiers de recherche plutôt que dupliqués en détail dans ce README.

# Packs publics actuels

Téléchargements Annecy :

```text
/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv
/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2-sans-aviation.csv
```

Téléchargement Normandie :

```text
/downloads/normandie/radiopack-france-normandie-v0.3.1.csv
```

Le catalogue public reste :

```text
Annecy 65 / 48 + Normandie 139
```

Bretagne v0.1, Normandie v0.4 et Annecy–Alpes–Léman v0.3 restent hors de `website/src/lib/packRegistry.ts`.

# Architecture

Moteur CHIRP générique :

```text
website/src/lib/chirpPack.ts
```

Configuration Annecy publique :

```text
website/src/lib/annecyPack.ts
```

Registre des packs téléchargeables :

```text
website/src/lib/packRegistry.ts
```

Documentation de workflow :

- [REGIONAL-PACK-WORKFLOW.md](REGIONAL-PACK-WORKFLOW.md)
- [SPRINT-27-BRETAGNE-MARITIME-ZONING.md](SPRINT-27-BRETAGNE-MARITIME-ZONING.md)
- [SPRINT-28-EMERGENCY-ADRASEC-RESEARCH.md](SPRINT-28-EMERGENCY-ADRASEC-RESEARCH.md)
- [SPRINT-29-MORTAIN-BRETAGNE-RADIO-RESEARCH.md](SPRINT-29-MORTAIN-BRETAGNE-RADIO-RESEARCH.md)
- [research/sprint-30-34-summary.md](research/sprint-30-34-summary.md)
- [research/sprint-35-39-summary.md](research/sprint-35-39-summary.md)

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
python tests\test_etel_network_research.py
python tests\test_bretagne_ref_analog_expansion.py
python tests\test_analog_coverage_redundancy_review.py
python tests\test_bretagne_research_scaffold.py
python tests\test_emergency_relay_research.py
python tests\test_mortain_bretagne_radio_research.py
python tests\test_web_generator.py
python tests\test_annecy_research.py
python tests\test_annecy_aviation_lakes.py
python tests\test_annecy_airac08.py
python tests\test_annecy_internal_candidate.py
python tests\test_annecy_release_readiness.py
python tests\test_annecy_prepublication.py
python tests\test_annecy_prepublication_review.py
```

Après les tests :

```powershell
git status
```

Résultat attendu :

```text
nothing to commit, working tree clean
```

Après un build Astro :

```powershell
cd website
npm run build
cd ..
python tests\test_built_annecy_public_csv.py
python tests\test_built_public_pack_catalog.py
```

# Synchroniser le dépôt local

Commande habituelle :

```powershell
cd "C:\Users\cross\Documents\CODE\PROJETS\RadioPack-France"

git pull --ff-only

python tests\test_bretagne_research_scaffold.py
python tests\test_emergency_relay_research.py
python tests\test_site_files.py
python tests\test_pack_registry.py
python tests\test_normandie_v04_readiness.py

git status
```

Les archives de sprint sont des sauvegardes de référence uniquement : ne pas les décompresser dans le dépôt local lorsque GitHub contient déjà les changements.

# Prochaines priorités

1. exécuter le protocole R3 depuis Mortain-Bocage et enregistrer au moins deux sessions RX indépendantes valides ;
2. utiliser le mini-pack F5ZHA pour mesurer sa pertinence locale sans traiter la non-réception comme preuve d'arrêt ;
3. fermer le conflit F5ZHA par une source locale ou équivalente suffisamment autoritative ;
4. surveiller le retour en service de F1ZOV avant toute promotion de 431.975 MHz ;
5. trouver une seconde source actuelle donnant fréquence et mode pour F6ZES Sourdeval ;
6. poursuivre les recherches Bretagne / CROSS / ADRASEC et Annecy v0.3 sans modifier les packs publics ;
7. ne définir une taille publique Normandie v0.4 qu'après revue explicite de la sélection complète ;
8. ne publier aucune nouvelle mémoire tant que le readiness reste négatif.

# Maintenance

Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint. La CI doit évoluer avec le contrat du sprint.

Les caches Python (`__pycache__/` et `*.py[cod]`) et les dossiers `research/*/generated/` prévus restent ignorés par Git.

Le détail historique reste dans [CHANGELOG.md](CHANGELOG.md) et dans les résumés de sprint du dossier `research/`.

# Sécurité et usage

Les exports RadioPack sont destinés à l'écoute. Voir [NOTICE_LEGAL.md](NOTICE_LEGAL.md) pour les précautions et limites d'utilisation.
