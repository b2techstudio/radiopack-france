# RadioPack France

Codeplugs CHIRP régionaux, documentés et générés à partir de données publiques vérifiables pour les radios Quansheng UV-K5.

Le projet privilégie une approche prudente : aucune fréquence n'est ajoutée uniquement pour remplir un pack, les sources doivent être identifiables et les exports publics sont configurés en réception seule.

## État actuel — Sprint 22

Deux packs régionaux sont disponibles :

- **Normandie v0.3.1** — 139 mémoires RX ;
- **Annecy–Alpes–Léman v0.2** — 65 mémoires RX, avec variante **48 mémoires sans aviation**.

Annecy–Alpes–Léman reste au statut `published_v0.2`. La revue Sprint 19 a validé les **65/65 mémoires**, le Sprint 21 a publié les routes CSV et le Sprint 22 termine la finition post-publication.

Le générateur public est disponible sur :

```text
/generateur
```

Il permet :

- d'inclure ou retirer les 17 mémoires aviation ;
- de passer de 65 à 48 mémoires sans renuméroter artificiellement les autres blocs ;
- d'activer un contrôle NOTAM facultatif ;
- de confirmer « J'ai vérifié les NOTAM applicables » ;
- d'ouvrir directement SOFIA-Briefing ou Skybriefing ;
- de sélectionner automatiquement le bon nom de fichier ;
- d'effectuer un **téléchargement direct** de la variante publique validée.

Le contrôle NOTAM est **informatif et non bloquant**. Il ne modifie jamais automatiquement les fréquences du CSV.

## Nettoyage de l'ancienne v0.1

L'**ancienne v0.1** Annecy / Haute-Savoie n'a plus de rôle actif dans le dépôt.

Ont été retirés de l'arborescence courante :

- son manifeste régional ;
- son ancien inventaire aviation AIRAC 07/26 ;
- son ancien inventaire de relais ;
- son CSV régional ;
- son CSV relais ;
- son guide PDF.

L'historique reste disponible dans Git. Les anciennes URL publiques importantes sont redirigées vers Annecy–Alpes–Léman v0.2 ou vers la page régionale afin d'éviter des liens morts.

## Principes permanents

- Réception seule : `Duplex=off` sur les exports RadioPack.
- `Offset=0.000000` pour les fichiers RX-only.
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

Albertville `LFKA`, Megève `LFHM` et Genève `LSGG` restent volontairement hors v0.2 faute de tableau primaire suffisamment extractible dans le workflow retenu. Sallanches `LFHZ` est exclu car l'aérodrome est fermé. Le cas F1ZJV reste hors production tant que son statut analogique/numérique n'est pas recoupé sans ambiguïté.

### Satellites retenus

- `SAT-SO50` — descente 436.795 MHz ;
- `SAT-AO91` — descente 145.960 MHz, passages éclairés uniquement en raison de la batterie ;
- `SAT-AO123` — descente 435.400 MHz.

## Architecture de génération — Sprint 22

Les règles CHIRP génériques sont maintenant centralisées dans :

```text
website/src/lib/chirpPack.ts
```

Cette bibliothèque gère :

- le chargement des jeux de données ;
- le filtrage par statut de vérification ;
- l'assemblage des positions ;
- les doublons de positions, noms et fréquences ;
- la limite de 200 mémoires ;
- les noms de 10 caractères maximum ;
- la génération CSV en réception seule avec `Duplex=off` et `Offset=0.000000`.

La configuration propre à Annecy–Alpes–Léman est dans :

```text
website/src/lib/annecyPack.ts
```

Elle ne définit plus que les sources, positions de départ, groupes optionnels et nombres de mémoires attendus.

La méthode à suivre pour créer une nouvelle région est documentée dans [REGIONAL-PACK-WORKFLOW.md](REGIONAL-PACK-WORKFLOW.md).

## Téléchargements publics Annecy

Routes publiques :

```text
/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv
/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2-sans-aviation.csv
```

Les deux routes sont prérendues par Astro. Le générateur web ne reconstruit plus une copie du CSV avec un Blob JavaScript : il sélectionne directement l'une de ces deux routes déjà validées.

Cela garantit que le bouton du générateur et les téléchargements publics utilisent exactement les mêmes fichiers que ceux contrôlés après `astro build`.

## Contrôle NOTAM

L'option NOTAM reste entièrement facultative. Lorsqu'elle est activée, le générateur propose des liens vers :

- **SOFIA-Briefing** pour la France ;
- **Skybriefing** pour la Suisse.

La confirmation NOTAM n'altère jamais le CSV et n'empêche jamais son téléchargement. Le pack reste une liste d'écoute et non un outil de préparation de vol.

## Revue et garde-fous

La carte :

```text
research/annecy-alpes-leman-v0.2/prepublication-reviewed-memory-map.json
```

fige pour chaque mémoire : emplacement, nom, fréquence, mode, pas et empreinte SHA-256 du commentaire validé.

La CI vérifie notamment :

- les 65 mémoires de la variante complète ;
- les 48 mémoires de la variante sans aviation ;
- `Duplex=off` et `Offset=0.000000` ;
- l'absence de doublons ;
- les noms ≤ 10 caractères ;
- l'identité fréquentielle du CSV quel que soit l'état NOTAM ;
- le générateur web ;
- les deux routes CSV publiques ;
- les fichiers réellement produits dans `website/dist` ;
- l'absence des fichiers v0.1 supprimés ;
- les redirections des anciennes URL ;
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
python tests\test_annecy_research.py
python tests\test_annecy_aviation_lakes.py
python tests\test_annecy_airac08.py
python tests\test_annecy_internal_candidate.py
python tests\test_annecy_release_readiness.py
python tests\test_annecy_prepublication.py
python tests\test_annecy_prepublication_review.py
python tests\test_web_generator.py
```

Après un build Astro :

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

## Ajouter une future région

La nouvelle architecture évite de recopier le générateur Annecy.

Le principe est :

1. créer les inventaires de recherche ;
2. définir les blocs et positions ;
3. créer un wrapper `<pack>Pack.ts` utilisant `chirpPack.ts` ;
4. geler une carte de revue ;
5. créer les routes Astro de téléchargement ;
6. ajouter les options réellement utiles dans le générateur ;
7. faire contrôler les fichiers finaux de `website/dist` par la CI ;
8. publier explicitement après revue.

Voir [REGIONAL-PACK-WORKFLOW.md](REGIONAL-PACK-WORKFLOW.md) pour le détail.

## Maintenance du projet

Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint afin de refléter l'état réel du dépôt, les fonctions disponibles, les commandes utiles et les prochaines étapes.

La CI doit être ajustée en même temps lorsque le contrat du sprint évolue.

Les caches Python (`__pycache__/` et `*.py[cod]`) sont ignorés par Git.

Le détail historique des évolutions reste conservé dans [CHANGELOG.md](CHANGELOG.md).

## Sécurité et usage

Les exports RadioPack sont destinés à l'écoute. Voir [NOTICE_LEGAL.md](NOTICE_LEGAL.md) pour les précautions et limites d'utilisation.
