# RadioPack France

Codeplugs CHIRP régionaux, documentés et générés à partir de données publiques vérifiables pour les radios Quansheng UV-K5.

Le projet privilégie une approche prudente : aucune fréquence n'est ajoutée uniquement pour remplir un pack, les sources doivent être identifiables et les exports publics sont configurés en réception seule.

## État actuel — Sprint 21

Deux packs régionaux sont maintenant disponibles :

- **Normandie v0.3.1** — 139 mémoires RX ;
- **Annecy–Alpes–Léman v0.2** — 65 mémoires RX, avec variante 48 mémoires sans aviation.

Annecy–Alpes–Léman v0.2 est officiellement publié. Le plan est passé à `published_v0.2` après la revue Sprint 19 des **65/65 mémoires**, l'intégration du générateur web au Sprint 20 et la publication explicite au Sprint 21.

Le générateur public est disponible sur :

```text
/generateur
```

Il permet :

- d'inclure ou retirer les 17 mémoires aviation ;
- de passer de 65 à 48 mémoires sans renuméroter artificiellement les autres blocs ;
- d'activer un contrôle NOTAM facultatif ;
- de confirmer « J'ai vérifié les NOTAM applicables » ;
- de générer et télécharger directement le CSV choisi.

Le contrôle NOTAM est **informatif et non bloquant**. Il ne modifie jamais automatiquement les fréquences du CSV.

## Principes permanents

- Réception seule : `Duplex=off` sur les exports RadioPack.
- Noms de mémoires limités à 10 caractères.
- Maximum 200 mémoires par pack.
- Pas de remplissage artificiel.
- Les fréquences contestées ou insuffisamment recoupées restent hors production.
- Pour l'ISS et les satellites, seule la liaison descendante est mémorisée ; la liaison montante reste une métadonnée.
- Les données aéronautiques sont destinées à l'écoute et ne constituent pas une source de préparation ou de conduite d'un vol.

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

La variante sans aviation retire uniquement les 17 mémoires aviation et conserve **48 mémoires**.

Albertville `LFKA`, Megève `LFHM` et Genève `LSGG` restent volontairement hors v0.2 faute de tableau primaire suffisamment extractible dans le workflow retenu. Sallanches `LFHZ` est exclu car l'aérodrome est fermé. Le cas F1ZJV reste également hors production tant que son statut analogique/numérique n'est pas recoupé sans ambiguïté.

### Satellites retenus

- `SAT-SO50` — descente 436.795 MHz ;
- `SAT-AO91` — descente 145.960 MHz, passages éclairés uniquement en raison de la batterie ;
- `SAT-AO123` — descente 435.400 MHz.

## Génération publique

La bibliothèque commune est :

```text
website/src/lib/annecyPack.ts
```

Elle assemble les mêmes données validées que le backend de vérification et sert à la fois aux routes CSV publiques prérendues par Astro et au générateur web `/generateur`.

Routes publiques :

```text
/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv
/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2-sans-aviation.csv
```

Le générateur historique `generator/generate_chirp_csv.py` ne régénère plus les anciens fichiers Annecy v0.1. La v0.2 est produite par la bibliothèque Astro ci-dessus.

## Revue et garde-fous

La carte :

```text
research/annecy-alpes-leman-v0.2/prepublication-reviewed-memory-map.json
```

fige pour chaque mémoire : emplacement, nom, fréquence, mode, pas et empreinte SHA-256 du commentaire validé.

La CI vérifie :

- les 65 mémoires de la variante complète ;
- les 48 mémoires de la variante sans aviation ;
- `Duplex=off` et `Offset=0.000000` ;
- l'absence de doublons et les noms ≤ 10 caractères ;
- l'identité du CSV avec ou sans confirmation NOTAM ;
- le générateur web et les routes CSV publiques ;
- le build Astro ;
- **les deux CSV réellement produits dans `website/dist` après le build**, comparés ligne par ligne à la carte de revue par `tests/test_built_annecy_public_csv.py`.

Ainsi, une CI verte valide aussi les fichiers qui seront réellement déployés sur le site.

## Synchroniser le dépôt local

```powershell
cd "C:\Users\cross\Documents\CODE\PROJETS\RadioPack-France"
git pull --ff-only
git status
```

Les archives de sprint sont uniquement des sauvegardes de référence. Elles ne doivent pas être copiées ou décompressées dans le dépôt quand les mêmes changements sont déjà sur GitHub.

## Tests principaux

Depuis la racine :

```powershell
python tests\test_generator.py
python tests\test_site_files.py
python tests\test_annecy_research.py
python tests\test_annecy_aviation_lakes.py
python tests\test_annecy_airac08.py
python tests\test_annecy_internal_candidate.py
python tests\test_annecy_release_readiness.py
python tests\test_annecy_prepublication.py
python tests\test_annecy_prepublication_review.py
python tests\test_web_generator.py
```

Après un build Astro, le contrôle des véritables fichiers publics peut aussi être lancé :

```powershell
cd website
npm run build
cd ..
python tests\test_built_annecy_public_csv.py
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
```

## Maintenance du projet

Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint. La CI doit être ajustée en même temps afin de vérifier l'état courant du dépôt.

Les caches Python (`__pycache__/` et `*.py[cod]`) sont ignorés par Git.

Le détail historique des évolutions reste conservé dans [CHANGELOG.md](CHANGELOG.md).

## Sécurité et usage

Les exports RadioPack sont destinés à l'écoute. Voir [NOTICE_LEGAL.md](NOTICE_LEGAL.md) pour les précautions et limites d'utilisation.
