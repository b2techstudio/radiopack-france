# RadioPack France

Codeplugs CHIRP régionaux, documentés et générés à partir de données publiques vérifiables pour les radios Quansheng UV-K5.

Le projet privilégie une approche prudente : aucune fréquence n'est ajoutée uniquement pour remplir un pack, les sources doivent être identifiables et les exports publics sont configurés en réception seule.

## État actuel — Sprint 23

Deux packs régionaux sont disponibles :

- **Normandie v0.3.1** — 139 mémoires RX ;
- **Annecy–Alpes–Léman v0.2** — 65 mémoires RX, avec variante **48 mémoires sans aviation**.

Annecy–Alpes–Léman reste au statut `published_v0.2`. La revue Sprint 19 a validé les **65/65 mémoires**, le Sprint 21 a publié les routes CSV, le Sprint 22 a nettoyé l'ancienne v0.1 et le Sprint 23 rend le générateur réellement multi-régions.

Le générateur public est maintenant multi-régions :

```text
/generateur
```

Il permet de sélectionner **Annecy–Alpes–Léman** ou **Normandie**, puis ne propose que les options réellement prises en charge par le pack choisi.

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
- aucune fréquence Normandie n'a été modifiée au Sprint 23.

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

## Normandie v0.3.1

Le pack Normandie public reste inchangé au Sprint 23 :

- 139 mémoires RX ;
- `Duplex=off` ;
- téléchargement public existant :

```text
/downloads/normandie/radiopack-france-normandie-v0.3.1.csv
```

Il est désormais enregistré dans le même catalogue public que les variantes Annecy et peut être sélectionné depuis `/generateur`.

## Architecture de génération

Les règles CHIRP génériques restent centralisées dans :

```text
website/src/lib/chirpPack.ts
```

Cette bibliothèque gère notamment :

- le chargement des jeux de données ;
- le filtrage par statut de vérification ;
- l'assemblage des positions ;
- les doublons de positions, noms et fréquences ;
- la limite de 200 mémoires ;
- les noms de 10 caractères maximum ;
- la génération CSV en réception seule avec `Duplex=off` et `Offset=0.000000`.

La configuration spécifique d'Annecy–Alpes–Léman reste dans :

```text
website/src/lib/annecyPack.ts
```

### Registre public — Sprint 23

Le nouveau registre :

```text
website/src/lib/packRegistry.ts
```

est la source de vérité du générateur public pour les packs et variantes téléchargeables.

Il contient actuellement :

- Annecy–Alpes–Léman v0.2 complet — 65 mémoires ;
- Annecy–Alpes–Léman v0.2 sans aviation — 48 mémoires ;
- Normandie v0.3.1 — 139 mémoires.

Chaque entrée indique le nom, la version, le nombre de mémoires, le fichier public, l'URL de téléchargement et les options réellement supportées.

Le générateur ne possède donc plus sa propre liste indépendante de packs : il lit ce registre et masque les options non supportées.

La méthode à suivre pour créer une nouvelle région est documentée dans [REGIONAL-PACK-WORKFLOW.md](REGIONAL-PACK-WORKFLOW.md).

## Téléchargements publics Annecy

```text
/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv
/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2-sans-aviation.csv
```

Les deux routes sont prérendues par Astro. Le générateur web ne reconstruit aucun Blob CSV côté navigateur : il sélectionne directement une ressource publique déjà validée.

## Contrôle NOTAM

L'option NOTAM reste facultative et limitée aux packs qui la prennent explicitement en charge.

Pour Annecy, le générateur propose :

- **SOFIA-Briefing** pour la France ;
- **Skybriefing** pour la Suisse.

La confirmation NOTAM n'altère jamais le CSV et n'empêche jamais son téléchargement.

## Ancienne Annecy / Haute-Savoie v0.1

L'**ancienne v0.1** n'a plus de rôle actif dans le dépôt. Son manifeste, ses anciennes données locales, ses CSV et son guide PDF ont été retirés de l'arborescence courante au Sprint 22.

L'historique reste disponible dans Git et les anciennes URL utiles sont redirigées vers la v0.2 ou vers la page régionale.

## Revue et garde-fous

La carte Annecy :

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
- l'absence des fichiers Annecy v0.1 supprimés ;
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

Après un build Astro :

```powershell
cd website
npm run build
cd ..
python tests\test_built_annecy_public_csv.py
python tests\test_built_public_pack_catalog.py
```

Le nouveau test de catalogue doit valider :

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

Sur `/generateur`, vérifie que le sélecteur passe correctement d'Annecy à Normandie et que les options Aviation / NOTAM disparaissent lorsque Normandie est sélectionnée.

## Ajouter une future région

La nouvelle architecture évite de recopier le générateur.

Le principe est :

1. créer les inventaires de recherche ;
2. définir les blocs et positions ;
3. créer un wrapper `<pack>Pack.ts` utilisant `chirpPack.ts` ;
4. geler une carte de revue ;
5. créer les routes ou fichiers publics validés ;
6. enregistrer le pack et ses variantes dans `packRegistry.ts` ;
7. ajouter uniquement les options réellement supportées ;
8. contrôler les fichiers finaux de `website/dist` par la CI ;
9. publier explicitement après revue.

Voir [REGIONAL-PACK-WORKFLOW.md](REGIONAL-PACK-WORKFLOW.md) pour le détail.

## Maintenance du projet

Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint afin de refléter l'état réel du dépôt, les fonctions disponibles, les commandes utiles et les prochaines étapes.

La CI doit être ajustée en même temps lorsque le contrat du sprint évolue.

Les caches Python (`__pycache__/` et `*.py[cod]`) sont ignorés par Git.

Le détail historique des évolutions reste conservé dans [CHANGELOG.md](CHANGELOG.md).

## Sécurité et usage

Les exports RadioPack sont destinés à l'écoute. Voir [NOTICE_LEGAL.md](NOTICE_LEGAL.md) pour les précautions et limites d'utilisation.
