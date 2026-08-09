# RadioPack France

Codeplugs CHIRP régionaux, documentés et générés à partir de données publiques vérifiables pour les radios Quansheng UV-K5.

Le projet privilégie une approche prudente : aucune fréquence n'est ajoutée uniquement pour remplir un pack, les sources doivent être identifiables et les exports publics sont configurés en réception seule.

## État actuel — Sprint 24

Deux packs régionaux sont disponibles :

- **Normandie v0.3.1** — 139 mémoires RX ;
- **Annecy–Alpes–Léman v0.2** — 65 mémoires RX, avec variante **48 mémoires sans aviation**.

Le Sprint 23 a rendu le générateur public multi-régions. Le Sprint 24 sécurise la génération locale : **les tests du générateur n'écrivent plus dans les CSV suivis par Git** et les packs régionaux déjà publiés sont désormais considérés comme des **artefacts versionnés figés**.

Le générateur public est disponible sur :

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
- pas d'option Annecy affichée ;
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

### Version publiée figée

Le Sprint 24 a révélé que les commentaires ISS du jeu national avaient été enrichis après la publication de Normandie v0.3.1. Les fréquences et positions du pack publié n'ont pas changé, mais une reconstruction depuis les jeux partagés actuels ne reproduit plus exactement les commentaires historiques de v0.3.1.

La règle retenue est donc : **Normandie v0.3.1 reste immuable**. Le générateur générique ne la reconstruit plus. Toute actualisation des données Normandie devra passer par une nouvelle version, avec revue explicite avant publication.

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

Chaque variante déclare son nombre de mémoires, son nom de fichier, son URL publique et les options réellement supportées.

La méthode d'ajout d'une nouvelle région est documentée dans [REGIONAL-PACK-WORKFLOW.md](REGIONAL-PACK-WORKFLOW.md).

## Tests de génération isolés — Sprint 24

Le générateur Python générique :

```text
generator/generate_chirp_csv.py
```

accepte désormais une racine de sortie séparée :

```text
--output-root <dossier>
```

Les données sont toujours lues depuis `--root`, mais les sorties génériques planifiées sont écrites sous `--output-root` en conservant leurs chemins relatifs.

Ces sorties génériques sont actuellement :

- PMR446 national ;
- VHF marine nationale ;
- APRS / ISS national ;
- canaux d'appel nationaux ;
- relais analogiques Normandie.

Le pack complet **Normandie v0.3.1 n'est volontairement plus une sortie du générateur générique**.

`tests/test_generator.py` utilise automatiquement un dossier temporaire système. Il :

1. mémorise les octets des CSV suivis concernés, y compris Normandie v0.3.1 ;
2. génère les sorties génériques dans un dossier temporaire ;
3. compare les lignes temporaires aux CSV publiés correspondants ;
4. contrôle les nombres de mémoires et les règles RX-only ;
5. vérifie que Normandie v0.3.1 n'est pas reconstruite ;
6. contrôle séparément le CSV Normandie publié de 139 mémoires ;
7. vérifie qu'aucun fichier suivi n'a changé d'un octet.

Cela corrige définitivement le problème observé sous Windows où un simple test pouvait faire apparaître le CSV Normandie comme modifié dans `git status`.

Sans `--output-root`, le générateur générique écrit toujours ses sorties génériques planifiées dans leurs emplacements publics normaux. Il ne réécrit plus les packs régionaux versionnés figés.

Voir [SPRINT-24-ISOLATED-GENERATOR-TESTS.md](SPRINT-24-ISOLATED-GENERATOR-TESTS.md) pour le détail.

## Contrôle NOTAM

L'option NOTAM reste facultative et limitée aux packs qui la prennent explicitement en charge.

Pour Annecy, le générateur propose :

- **SOFIA-Briefing** pour la France ;
- **Skybriefing** pour la Suisse.

La confirmation NOTAM n'altère jamais le CSV et n'empêche jamais son téléchargement.

## Ancienne Annecy / Haute-Savoie v0.1

L'ancienne v0.1 n'a plus de rôle actif dans le dépôt. Ses anciens fichiers ont été retirés de l'arborescence courante au Sprint 22.

L'historique reste disponible dans Git et les anciennes URL utiles sont redirigées vers la v0.2 ou vers la page régionale.

## Revue et garde-fous

La carte de revue Annecy :

```text
research/annecy-alpes-leman-v0.2/prepublication-reviewed-memory-map.json
```

fige pour chaque mémoire : emplacement, nom, fréquence, mode, pas et empreinte SHA-256 du commentaire validé.

La CI vérifie notamment :

- Annecy complet : 65 mémoires ;
- Annecy sans aviation : 48 mémoires ;
- Normandie : 139 mémoires ;
- `Duplex=off` et `Offset=0.000000` ;
- les noms ≤ 10 caractères ;
- l'absence de doublons ;
- le registre `packRegistry.ts` ;
- le sélecteur multi-régions ;
- le masquage des options non prises en charge ;
- les fichiers réellement présents dans `website/dist` après `astro build` ;
- la génération Python dans un dossier temporaire ;
- l'absence de réécriture de Normandie v0.3.1 ;
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
python tests\test_web_generator.py
python tests\test_annecy_research.py
python tests\test_annecy_aviation_lakes.py
python tests\test_annecy_airac08.py
python tests\test_annecy_internal_candidate.py
python tests\test_annecy_release_readiness.py
python tests\test_annecy_prepublication.py
python tests\test_annecy_prepublication_review.py
```

Après `python tests\test_generator.py`, cette commande doit maintenant rester propre :

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

Le principe est :

1. créer les inventaires de recherche ;
2. définir les blocs et positions ;
3. créer un wrapper `<pack>Pack.ts` utilisant `chirpPack.ts` ;
4. geler une carte de revue ;
5. créer les routes ou fichiers publics validés ;
6. enregistrer le pack et ses variantes dans `packRegistry.ts` ;
7. ajouter uniquement les options réellement supportées ;
8. contrôler les fichiers finaux de `website/dist` par la CI ;
9. publier explicitement après revue ;
10. ne jamais réécrire une ancienne version publiée : toute évolution produit une nouvelle version.

Voir [REGIONAL-PACK-WORKFLOW.md](REGIONAL-PACK-WORKFLOW.md) pour le détail.

## Maintenance du projet

Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint afin de refléter l'état réel du dépôt, les fonctions disponibles, les commandes utiles et les prochaines étapes.

La CI doit être ajustée en même temps lorsque le contrat du sprint évolue.

Les caches Python (`__pycache__/` et `*.py[cod]`) sont ignorés par Git.

Le détail historique des évolutions reste conservé dans [CHANGELOG.md](CHANGELOG.md).

## Sécurité et usage

Les exports RadioPack sont destinés à l'écoute. Voir [NOTICE_LEGAL.md](NOTICE_LEGAL.md) pour les précautions et limites d'utilisation.
