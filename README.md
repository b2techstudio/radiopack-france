# RadioPack France

Codeplugs CHIRP régionaux, documentés et générés à partir de données publiques vérifiables pour les radios Quansheng UV-K5.

Le projet privilégie une approche prudente : aucune fréquence n'est ajoutée uniquement pour remplir un pack, les sources doivent être identifiables et les exports publics sont configurés en réception seule.

## État actuel — Sprint 26

Deux packs régionaux sont publiés :

- **Normandie v0.3.1** — 139 mémoires RX ;
- **Annecy–Alpes–Léman v0.2** — 65 mémoires RX, avec variante **48 mémoires sans aviation**.

Une troisième région est maintenant ouverte en **recherche uniquement** :

- **Bretagne v0.1 — recherche** — 0 fréquence retenue, aucun nombre cible de mémoires, aucune publication autorisée.

Le Sprint 23 a rendu le générateur public multi-régions. Le Sprint 24 a isolé les tests de génération et figé les versions régionales déjà publiées. Le Sprint 25 a ajouté un starter sécurisé. Le Sprint 26 utilise ce cadre pour initialiser réellement `research/bretagne-v0.1/` sans ajouter Bretagne au site public ni au générateur.

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

## Bretagne v0.1 — recherche Sprint 26

Le troisième chantier régional est initialisé ici :

```text
research/bretagne-v0.1/
```

L'espace contient :

- `README.md` ;
- `pack-plan.json` ;
- `source-registry.json` ;
- `publication-gates.json` ;
- `memory-plan.json`.

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

Les premiers points d'entrée officiels recensés sont :

- SIA / AIP France — Brest Bretagne `LFRB` ;
- SIA / AIP France — Rennes Saint-Jacques `LFRN` ;
- portail Open Data de l'ANFR ;
- services ANFR liés aux radioamateurs ;
- annuaire officiel ANFR des radioamateurs autorisés.

Ils sont enregistrés uniquement comme **sources de départ**. Toutes les entrées restent à `frequency_data_promoted: false`.

Bretagne n'existe volontairement pas dans :

```text
website/src/lib/packRegistry.ts
website/src/data/regions.json
website/src/pages/regions/
website/src/pages/downloads/
website/public/downloads/
```

Voir [SPRINT-26-BRETAGNE-INITIALIZATION.md](SPRINT-26-BRETAGNE-INITIALIZATION.md).

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

Albertville `LFKA`, Megève `LFHM` et Genève `LSGG` restent volontairement hors v0.2 faute de tableau primaire suffisamment extractible dans le workflow retenu. Sallanches `LFHZ` est exclu car l'aérodrome est fermé. Le cas F1ZJV reste hors production tant que son statut analogique/numérique n'est pas recoupé sans ambiguïté.

Satellites retenus :

- `SAT-SO50` — descente 436.795 MHz ;
- `SAT-AO91` — descente 145.960 MHz, passages éclairés uniquement en raison de la batterie ;
- `SAT-AO123` — descente 435.400 MHz.

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

Normandie v0.3.1 est un **artefact publié immuable**. Les commentaires ISS du jeu national ont évolué depuis sa publication ; ses fréquences et positions restent inchangées. Toute actualisation devra créer une nouvelle version avec une nouvelle revue.

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

initialise un espace de recherche non public.

La Bretagne a été initialisée sur ce modèle au Sprint 26. Le starter impose dès le départ : RX-only, `Duplex=off`, `Offset=0.000000`, noms de 10 caractères maximum, maximum 200 mémoires, pas de remplissage artificiel, préférence pour les sources primaires, revue obligatoire et immutabilité des versions publiées.

Il ne crée jamais automatiquement de page, de route CSV, de fichier sous `website/public`, d'entrée dans `packRegistry.ts` ou d'entrée dans `regions.json`.

Voir [SPRINT-25-REGIONAL-STARTER.md](SPRINT-25-REGIONAL-STARTER.md) et [REGIONAL-PACK-WORKFLOW.md](REGIONAL-PACK-WORKFLOW.md).

## Tests de génération isolés

Le générateur Python générique :

```text
generator/generate_chirp_csv.py
```

accepte :

```text
--output-root <dossier>
```

`tests/test_generator.py` utilise un dossier temporaire et ne réécrit plus les CSV suivis par Git. Normandie v0.3.1 n'est volontairement plus une sortie du générateur générique.

## Contrôle NOTAM

L'option NOTAM reste facultative et limitée aux packs qui la prennent explicitement en charge.

Pour Annecy, le générateur propose SOFIA-Briefing pour la France et Skybriefing pour la Suisse. La confirmation NOTAM n'altère jamais le CSV et n'empêche jamais son téléchargement.

## Revue et garde-fous

La carte de revue Annecy :

```text
research/annecy-alpes-leman-v0.2/prepublication-reviewed-memory-map.json
```

fige chaque mémoire validée.

La CI vérifie notamment :

- Annecy complet : 65 mémoires ;
- Annecy sans aviation : 48 mémoires ;
- Normandie : 139 mémoires ;
- les exports RX-only ;
- le registre multi-régions public ;
- les fichiers réellement présents dans `website/dist` ;
- la génération Python en sortie temporaire ;
- l'immutabilité de Normandie v0.3.1 ;
- le starter régional ;
- le scaffold Bretagne ;
- zéro fréquence Bretagne promue ;
- tous les drapeaux de publication Bretagne à `false` ;
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

## Lancer le site en local

```powershell
cd website
npm install
npm run dev
```

Puis ouvre notamment :

```text
http://localhost:4321/generateur
http://localhost:4321/regions/annecy-haute-savoie
http://localhost:4321/regions/normandie
```

Il ne doit pas encore exister de page publique Bretagne.

## Prochaine étape Bretagne

Le prochain sprint Bretagne devra rester dans `research/bretagne-v0.1/` et :

1. définir le périmètre géographique et les catégories à étudier ;
2. compléter le registre de sources officielles ;
3. rechercher les inventaires domaine par domaine ;
4. ne promouvoir aucune fréquence sans validation ;
5. ne fixer aucun nombre cible artificiel de mémoires.

## Maintenance du projet

Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint afin de refléter l'état réel du dépôt, les fonctions disponibles, les commandes utiles et les prochaines étapes.

La CI doit être ajustée en même temps lorsque le contrat du sprint évolue.

Les caches Python (`__pycache__/` et `*.py[cod]`) sont ignorés par Git.

Le détail historique des évolutions reste conservé dans [CHANGELOG.md](CHANGELOG.md).

## Sécurité et usage

Les exports RadioPack sont destinés à l'écoute. Voir [NOTICE_LEGAL.md](NOTICE_LEGAL.md) pour les précautions et limites d'utilisation.
