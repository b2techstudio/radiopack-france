# RadioPack France

Codeplugs CHIRP régionaux, documentés et générés à partir de données publiques vérifiables pour les radios Quansheng UV-K5.

Le projet privilégie une approche prudente : aucune fréquence n'est ajoutée uniquement pour remplir un pack, les sources doivent être identifiables et les exports publics sont configurés en réception seule.

## État actuel — Sprint 25

Deux packs régionaux sont disponibles :

- **Normandie v0.3.1** — 139 mémoires RX ;
- **Annecy–Alpes–Léman v0.2** — 65 mémoires RX, avec variante **48 mémoires sans aviation**.

Le Sprint 23 a rendu le générateur public multi-régions. Le Sprint 24 a isolé les tests de génération et figé les versions régionales déjà publiées. Le Sprint 25 ajoute un **starter de recherche sécurisé** pour initialiser un futur pack régional sans créer de page publique, de route CSV ou d'entrée dans le registre du générateur.

Le générateur public reste disponible sur :

```text
/generateur
```

Il permet de sélectionner **Annecy–Alpes–Léman** ou **Normandie**, puis n'affiche que les options réellement prises en charge par le pack choisi.

Pour Annecy :

- aviation activée : 65 mémoires ;
- aviation désactivée : 48 mémoires ;
- contrôle NOTAM facultatif ;
- liens SOFIA-Briefing et Skybriefing ;
- téléchargement direct de la variante publique validée.

Pour Normandie :

- variante publique fixe de 139 mémoires ;
- téléchargement direct du CSV v0.3.1 existant ;
- la version v0.3.1 est figée et ne doit plus être réécrite par le générateur générique.

Le contrôle NOTAM est **informatif et non bloquant**. Il ne modifie jamais automatiquement les fréquences du CSV.

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

Les deux routes sont prérendues par Astro et contrôlées après build.

## Normandie v0.3.1

Le pack Normandie public contient 139 mémoires RX et reste disponible ici :

```text
/downloads/normandie/radiopack-france-normandie-v0.3.1.csv
```

Il est enregistré dans le même catalogue public qu'Annecy et peut être sélectionné depuis `/generateur`.

Normandie v0.3.1 est désormais traitée comme un **artefact publié immuable**. Les commentaires ISS du jeu national ont évolué depuis sa publication ; les fréquences et positions de v0.3.1 restent inchangées. Toute actualisation Normandie devra donc créer une nouvelle version avec une nouvelle revue.

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

Il décrit actuellement :

- Annecy–Alpes–Léman v0.2 complet — 65 mémoires ;
- Annecy–Alpes–Léman v0.2 sans aviation — 48 mémoires ;
- Normandie v0.3.1 — 139 mémoires.

La méthode complète d'ajout d'une région est documentée dans [REGIONAL-PACK-WORKFLOW.md](REGIONAL-PACK-WORKFLOW.md).

## Starter de pack régional — Sprint 25

Le nouvel outil :

```text
tools/create_regional_pack.py
```

initialise uniquement un **espace de recherche non public**.

Exemple :

```powershell
python tools\create_regional_pack.py --name "Bretagne" --slug bretagne --version 0.1
```

La commande crée :

```text
research/bretagne-v0.1/
```

avec :

- `README.md` ;
- `pack-plan.json` ;
- `source-registry.json` ;
- `publication-gates.json` ;
- `memory-plan.json`.

L'état initial ne contient **aucune fréquence**, **aucun bloc mémoire** et **aucun nombre cible de mémoires**. Tous les drapeaux de publication sont à `false`.

Le starter impose dès le départ les règles permanentes : RX-only, `Duplex=off`, `Offset=0.000000`, noms de 10 caractères maximum, maximum 200 mémoires, pas de remplissage artificiel, préférence pour les sources primaires, revue obligatoire et immutabilité des versions publiées.

Il ne crée jamais :

- de page régionale ;
- de route CSV ;
- de fichier sous `website/public` ;
- d'entrée dans `website/src/lib/packRegistry.ts` ;
- d'entrée dans `website/src/data/regions.json`.

Si le dossier cible existe déjà, le starter refuse de l'écraser.

Voir [SPRINT-25-REGIONAL-STARTER.md](SPRINT-25-REGIONAL-STARTER.md) pour le détail.

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

Le starter régional possède le même principe de sécurité : `tests/test_regional_pack_starter.py` l'exécute sous une racine temporaire et vérifie qu'aucun fichier public du dépôt n'est modifié.

## Contrôle NOTAM

L'option NOTAM reste facultative et limitée aux packs qui la prennent explicitement en charge.

Pour Annecy, le générateur propose :

- **SOFIA-Briefing** pour la France ;
- **Skybriefing** pour la Suisse.

La confirmation NOTAM n'altère jamais le CSV et n'empêche jamais son téléchargement.

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
- `Duplex=off` et `Offset=0.000000` ;
- les noms ≤ 10 caractères ;
- le registre `packRegistry.ts` ;
- le sélecteur multi-régions ;
- les fichiers réellement présents dans `website/dist` après `astro build` ;
- la génération Python dans un dossier temporaire ;
- l'absence de réécriture de Normandie v0.3.1 ;
- le starter régional dans un dossier temporaire ;
- le refus d'une publication ou d'un écrasement implicite par le starter ;
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

Le catalogue final doit valider :

```text
Annecy 65 / 48 + Normandie 139
```

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

## Ajouter une future région

Le chemin recommandé est maintenant :

1. créer le starter avec `tools/create_regional_pack.py` ;
2. documenter les sources et le périmètre ;
3. construire les inventaires sans remplir artificiellement le pack ;
4. définir les blocs et positions ;
5. créer le wrapper `<pack>Pack.ts` utilisant `chirpPack.ts` ;
6. fermer les portes de publication ;
7. geler une carte de revue ;
8. créer les routes ou fichiers publics validés ;
9. enregistrer explicitement le pack dans `packRegistry.ts` ;
10. contrôler les fichiers finaux de `website/dist` ;
11. publier seulement après revue et CI verte ;
12. ne jamais réécrire une ancienne version publiée.

Voir [REGIONAL-PACK-WORKFLOW.md](REGIONAL-PACK-WORKFLOW.md) pour le détail.

## Maintenance du projet

Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint afin de refléter l'état réel du dépôt, les fonctions disponibles, les commandes utiles et les prochaines étapes.

La CI doit être ajustée en même temps lorsque le contrat du sprint évolue.

Les caches Python (`__pycache__/` et `*.py[cod]`) sont ignorés par Git.

Le détail historique des évolutions reste conservé dans [CHANGELOG.md](CHANGELOG.md).

## Sécurité et usage

Les exports RadioPack sont destinés à l'écoute. Voir [NOTICE_LEGAL.md](NOTICE_LEGAL.md) pour les précautions et limites d'utilisation.
