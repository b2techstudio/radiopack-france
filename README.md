# RadioPack France

Codeplugs CHIRP régionaux, documentés et générés à partir de données publiques vérifiables pour les radios Quansheng UV-K5.

Le projet privilégie une approche prudente : aucune fréquence n'est ajoutée uniquement pour remplir un pack, les sources doivent être identifiables, et les exports publics sont configurés en réception seule.

## État actuel — Sprint 16

- Pack public disponible : **Normandie v0.3.1**.
- **Annecy–Alpes–Léman v0.2** est toujours en préparation.
- Candidat interne Annecy–Alpes–Léman : **65 mémoires**.
- Aucun CSV public Annecy–Alpes–Léman v0.2 n'est encore publié.
- AIRAC France : validé pour le périmètre retenu.
- AIRAC Suisse : validé pour le périmètre retenu.
- Périmètre aviation v0.2 : clos de manière conservatrice.
- Contrôle NOTAM France/Suisse : **facultatif et non bloquant** pour un pack d'écoute RX.
- Dernière porte bloquante avant prépublication : **recontrôle dynamique des satellites FM**.

Le script `tools/check_annecy_release_readiness.py` centralise maintenant cette décision de prépublication.

## Principes du projet

- Réception seule : les exports publics utilisent `Duplex=off`.
- Noms de mémoires limités à 10 caractères pour l'écran de l'UV-K5.
- Maximum 200 mémoires par pack.
- Pas de remplissage artificiel pour atteindre un nombre cible.
- Les fréquences contestées, non recoupées ou insuffisamment documentées restent hors production.
- Pour l'ISS et les satellites, seule la liaison descendante est mémorisée ; la liaison montante reste une métadonnée documentaire.
- Les données aéronautiques sont destinées à l'écoute et ne constituent pas une source de préparation ou de conduite d'un vol.

## Annecy–Alpes–Léman v0.2

Le candidat interne de 65 mémoires comprend actuellement :

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

Albertville `LFKA`, Megève `LFHM` et Genève `LSGG` sont volontairement exclus de la v0.2 faute de tableau primaire suffisamment extractible dans le workflow actuel. Sallanches `LFHZ` est exclu car l'aérodrome est fermé.

## Futur générateur

Le contrat fonctionnel du futur générateur prévoit deux options indépendantes :

- **Inclure les fréquences aviation** : ajoute ou retire le bloc aviation du CSV généré.
- **Contrôle NOTAM avant génération** : contrôle facultatif qui n'ajoute, ne retire et ne remplace jamais automatiquement une fréquence AIP/AIRAC.

États NOTAM prévus :

- `disabled`
- `requested_unconfirmed`
- `user_confirmed`
- `automatic_verified` réservé pour une éventuelle intégration future fiable.

## Synchroniser le dépôt local

Depuis PowerShell :

```powershell
cd "C:\Users\cross\Documents\CODE\PROJETS\RadioPack-France"
git pull --ff-only
git status
```

Les archives de sprint sont uniquement des sauvegardes de référence. Elles ne doivent plus être copiées ou décompressées dans le dépôt local lorsque les mêmes fichiers sont déjà présents sur GitHub.

## Générer les CSV publics existants

Depuis la racine du dépôt :

```powershell
python generator\generate_chirp_csv.py
```

Tester le générateur :

```powershell
python tests\test_generator.py
```

## Construire le candidat Annecy interne

```powershell
python tools\build_annecy_internal_candidate.py
```

Les fichiers générés restent sous :

```text
research/annecy-alpes-leman-v0.2/generated/
```

Ce dossier est ignoré par Git et n'est pas publié sur le site.

## Contrôler la prépublication Annecy

```powershell
python tools\check_annecy_release_readiness.py
```

Tant que la porte satellite reste ouverte, le script répond volontairement `NOT READY` et retourne le code de sortie `2`.

## Tests principaux

```powershell
python tests\test_generator.py
python tests\test_site_files.py
python tests\test_annecy_research.py
python tests\test_annecy_aviation_lakes.py
python tests\test_annecy_airac08.py
python tests\test_annecy_internal_candidate.py
python tests\test_annecy_release_readiness.py
```

La CI GitHub exécute automatiquement les tests de données et le build Astro.

## Lancer le site en local

```powershell
cd website
npm install
npm run dev
```

Pour reproduire le build de production :

```powershell
npm run build
```

## Déploiement

Le site Astro est prévu pour Cloudflare Pages. Les changements sur `main` déclenchent la CI et le déploiement configuré du projet.

## Maintenance du projet

Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint afin de refléter l'état réel du dépôt, les fonctions disponibles, les commandes utiles et les prochaines portes de publication.

Le détail historique des évolutions reste conservé dans [CHANGELOG.md](CHANGELOG.md).

## Sécurité et usage

Les exports RadioPack sont destinés à l'écoute. Voir [NOTICE_LEGAL.md](NOTICE_LEGAL.md) pour les précautions et limites d'utilisation.
