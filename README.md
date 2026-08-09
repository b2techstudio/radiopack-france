# RadioPack France

Codeplugs CHIRP régionaux, documentés et générés à partir de données publiques vérifiables pour les radios Quansheng UV-K5.

Le projet privilégie une approche prudente : aucune fréquence n'est ajoutée uniquement pour remplir un pack, les sources doivent être identifiables et les exports publics sont configurés en réception seule.

## État actuel — Sprint 27

Deux packs régionaux sont publiés :

- **Normandie v0.3.1** — 139 mémoires RX ;
- **Annecy–Alpes–Léman v0.2** — 65 mémoires RX, avec variante **48 mémoires sans aviation**.

Une troisième région reste en **recherche uniquement** :

- **Bretagne v0.1 — recherche** — 0 fréquence retenue, aucun nombre cible de mémoires, aucune publication autorisée.

Le Sprint 27 impose désormais un **zonage radio Bretagne Nord / Bretagne Sud**. La Bretagne ne sera pas traitée comme un bloc maritime unique : la recherche distingue le contexte **CROSS Corsen** côté Manche Ouest / Bretagne Nord-Ouest, le contexte **CROSS Etel** côté Atlantique / Bretagne Sud, ainsi qu'une zone de transition du Finistère Sud dont la limite opérationnelle exacte doit encore être confirmée sur la cartographie officielle actuelle.

Le générateur public reste disponible sur :

```text
/generateur
```

Il ne propose toujours que **Annecy–Alpes–Léman** et **Normandie**. Bretagne n'y apparaîtra qu'après recherche, revue et publication explicite.

## Principes permanents

- Réception seule : `Duplex=off` sur les exports RadioPack.
- `Offset=0.000000` pour les fichiers RX-only.
- Noms de mémoires limités à 10 caractères.
- Maximum 200 mémoires par pack.
- Pas de remplissage artificiel.
- Les fréquences contestées ou insuffisamment recoupées restent hors production.
- Pour l'ISS et les satellites, seule la liaison descendante est mémorisée ; la liaison montante reste une métadonnée.
- Les données aéronautiques sont destinées à l'écoute et ne constituent pas une source de préparation ou de conduite d'un vol.
- Un pack régional déjà publié n'est jamais réécrit silencieusement : une évolution exige une nouvelle version et une nouvelle revue.
- Une source identifiée n'est pas automatiquement une fréquence validée.
- Une même fréquence ne doit pas être dupliquée artificiellement uniquement pour changer son étiquette géographique.

## Bretagne v0.1 — recherche Sprint 27

Le troisième chantier régional est ici :

```text
research/bretagne-v0.1/
```

L'espace contient maintenant :

- `README.md` ;
- `pack-plan.json` ;
- `source-registry.json` ;
- `publication-gates.json` ;
- `memory-plan.json` ;
- `maritime-zones.json`.

État actuel :

```text
status: research_scaffold_not_public
frequences retenues: 0
expected_memory_count: null
public_export_allowed: false
public_registry_allowed: false
public_routes_allowed: false
review_completed: false
```

### Bretagne Nord / Bretagne Sud

Le fichier :

```text
research/bretagne-v0.1/maritime-zones.json
```

impose trois sous-zones de recherche :

- **Bretagne Nord / Manche Ouest** — contexte opérationnel `CROSS Corsen` ;
- **Bretagne Sud / Atlantique** — contexte opérationnel `CROSS Etel` ;
- **transition Finistère Sud** — frontière opérationnelle actuelle à confirmer précisément avant publication.

Cette séparation s'applique à la VHF maritime, aux stations VHF déportées des CROSS, aux diffusions météo / sécurité et aux relais radioamateurs lorsque leur implantation ou leur couverture justifie un rattachement territorial.

### Canal 16

Le futur pack ne créera pas deux mémoires identiques du canal 16 uniquement pour écrire « Corsen » et « Etel ».

Le canal reste commun, mais la recherche doit conserver en métadonnées :

- le CROSS responsable selon la zone ;
- les stations VHF déportées / relais de couverture ;
- les éventuelles zones de recouvrement ;
- les canaux météo et de sécurité utilisés localement.

Le registre officiel de recherche contient désormais des exemples opérationnels récents montrant notamment Corsen à Audierne / ouest Finistère et Etel à Concarneau / Finistère Sud. Ces exemples servent au cadrage ; la limite SRR actuelle exacte doit encore être extraite de la cartographie officielle avant promotion d'une fréquence maritime.

### Météo et sécurité maritime

Le contexte de recherche enregistre également :

- annonces météo via le canal 16 avant diffusion sur 79/80 ;
- diffusion météo côtière permanente sur 63/64 notamment dans le Morbihan.

Aucune de ces informations n'est encore promue en mémoire Bretagne.

### Relais et couverture

Deux inventaires séparés devront être construits :

1. stations VHF maritimes déportées / relais de couverture CROSS, avec distinction Bretagne Nord et Bretagne Sud ;
2. relais radioamateurs, rattachés à Bretagne Nord, Bretagne Sud ou à la zone de transition lorsque cela est pertinent.

Une nouvelle porte de publication `maritime_zoning` bloque toute sortie publique tant que ce travail n'est pas terminé.

### Sources Bretagne

Le registre de sources contient maintenant dix points d'entrée institutionnels ou opérationnels officiels, notamment :

- SIA / AIP France — Brest Bretagne `LFRB` ;
- SIA / AIP France — Rennes Saint-Jacques `LFRN` ;
- portail Open Data de l'ANFR ;
- services ANFR liés aux radioamateurs ;
- documentation officielle du ministère chargé de la mer sur le canal 16 et les diffusions météo ;
- documentation de la Préfecture maritime de l'Atlantique sur le partage des zones CROSS et des opérations récentes.

Toutes les entrées restent à :

```text
frequency_data_promoted: false
```

Bretagne n'existe volontairement pas dans :

```text
website/src/lib/packRegistry.ts
website/src/data/regions.json
website/src/pages/regions/
website/src/pages/downloads/
website/public/downloads/
```

Voir [SPRINT-26-BRETAGNE-INITIALIZATION.md](SPRINT-26-BRETAGNE-INITIALIZATION.md) et [SPRINT-27-BRETAGNE-MARITIME-ZONING.md](SPRINT-27-BRETAGNE-MARITIME-ZONING.md).

## Annecy–Alpes–Léman v0.2

| Bloc | Mémoires |
|---|---:|
| PMR446 | 16 |
| APRS / ISS | 6 |
| Satellites FM | 3 |
| Canaux d'appel | 2 |
| Radioamateur France | 19 |
| Radioamateur Suisse | 2 |
| Aviation France / bassin genevois | 11 |
| Aviation Suisse | 6 |
| **Total** | **65** |

La variante sans aviation retire uniquement les 17 mémoires aviation et conserve **48 mémoires** sans compacter les autres positions.

Téléchargements publics :

```text
/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv
/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2-sans-aviation.csv
```

## Normandie v0.3.1

Le pack Normandie public contient 139 mémoires RX :

```text
/downloads/normandie/radiopack-france-normandie-v0.3.1.csv
```

Normandie v0.3.1 est un **artefact publié immuable**. Toute actualisation devra créer une nouvelle version avec une nouvelle revue.

## Architecture de génération

Les règles CHIRP génériques du site sont centralisées dans :

```text
website/src/lib/chirpPack.ts
```

La configuration spécifique d'Annecy–Alpes–Léman est dans :

```text
website/src/lib/annecyPack.ts
```

Le registre public multi-régions est :

```text
website/src/lib/packRegistry.ts
```

Il décrit actuellement uniquement :

- Annecy–Alpes–Léman v0.2 complet — 65 mémoires ;
- Annecy–Alpes–Léman v0.2 sans aviation — 48 mémoires ;
- Normandie v0.3.1 — 139 mémoires.

Bretagne reste hors de ce registre tant que ses portes de publication ne sont pas fermées.

## Starter de pack régional

L'outil :

```text
tools/create_regional_pack.py
```

initialise un espace de recherche non public. Il ne crée jamais automatiquement de page, de route CSV, de fichier sous `website/public`, d'entrée dans `packRegistry.ts` ou d'entrée dans `regions.json`.

Voir [SPRINT-25-REGIONAL-STARTER.md](SPRINT-25-REGIONAL-STARTER.md) et [REGIONAL-PACK-WORKFLOW.md](REGIONAL-PACK-WORKFLOW.md).

## Tests de génération isolés

Le générateur Python générique accepte :

```text
--output-root <dossier>
```

`tests/test_generator.py` utilise un dossier temporaire et ne réécrit plus les CSV suivis par Git. Normandie v0.3.1 n'est volontairement plus une sortie du générateur générique.

## Revue et garde-fous

La CI vérifie notamment :

- Annecy complet : 65 mémoires ;
- Annecy sans aviation : 48 mémoires ;
- Normandie : 139 mémoires ;
- les exports RX-only ;
- le registre multi-régions public ;
- la génération Python en sortie temporaire ;
- l'immutabilité de Normandie v0.3.1 ;
- le starter régional ;
- zéro fréquence Bretagne promue ;
- Bretagne Nord / CROSS Corsen et Bretagne Sud / CROSS Etel obligatoires dans la recherche ;
- limite SRR actuelle laissée bloquante tant qu'elle n'est pas confirmée ;
- inventaire futur obligatoire des stations VHF déportées et relais radioamateurs par sous-zone ;
- l'absence de Bretagne dans le site et le générateur public ;
- le build Astro.

## Synchroniser le dépôt local

```powershell
cd "C:\Users\cross\Documents\CODE\PROJETS\RadioPack-France"
git pull --ff-only
git status
```

Les archives de sprint sont uniquement des sauvegardes de référence. Elles ne doivent pas être copiées ou décompressées dans le dépôt quand les mêmes changements sont déjà sur GitHub.

## Tests principaux

```powershell
python tests\test_generator.py
python tests\test_site_files.py
python tests\test_pack_registry.py
python tests\test_regional_pack_starter.py
python tests\test_bretagne_research_scaffold.py
python tests\test_web_generator.py
python tests\test_annecy_research.py
python tests\test_annecy_aviation_lakes.py
python tests\test_annecy_airac08.py
python tests\test_annecy_internal_candidate.py
python tests\test_annecy_release_readiness.py
python tests\test_annecy_prepublication.py
python tests\test_annecy_prepublication_review.py
```

Après les tests locaux, `git status` doit rester :

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

Le catalogue public doit toujours valider :

```text
Annecy 65 / 48 + Normandie 139
```

Bretagne ne doit pas encore apparaître dans ce résultat.

## Prochaine étape Bretagne

Le prochain travail restera dans `research/bretagne-v0.1/` et devra en priorité :

1. confirmer précisément la limite SRR actuelle entre CROSS Corsen et CROSS Etel ;
2. inventorier les stations VHF déportées / relais de couverture des deux CROSS ;
3. cartographier les diffusions météo / sécurité maritime par sous-zone ;
4. construire séparément l'inventaire des relais radioamateurs Bretagne Nord et Bretagne Sud ;
5. poursuivre ensuite les inventaires aviation et autres domaines ;
6. ne promouvoir aucune fréquence sans validation ;
7. ne fixer aucun nombre cible artificiel de mémoires.

## Maintenance du projet

Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint afin de refléter l'état réel du dépôt, les fonctions disponibles, les commandes utiles et les prochaines étapes.

La CI doit être ajustée en même temps lorsque le contrat du sprint évolue.

Les caches Python (`__pycache__/` et `*.py[cod]`) sont ignorés par Git.

Le détail historique des évolutions reste conservé dans [CHANGELOG.md](CHANGELOG.md).

## Sécurité et usage

Les exports RadioPack sont destinés à l'écoute. Voir [NOTICE_LEGAL.md](NOTICE_LEGAL.md) pour les précautions et limites d'utilisation.
