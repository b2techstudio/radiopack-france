# RadioPack France

Codeplugs CHIRP régionaux, documentés et générés à partir de données publiques vérifiables pour les radios Quansheng UV-K5.

Le projet privilégie une approche prudente : aucune fréquence n'est ajoutée uniquement pour remplir un pack, les sources doivent être identifiables, et les exports publics sont configurés en réception seule.

## État actuel — Sprint 18

- Pack public disponible : **Normandie v0.3.1**.
- **Annecy–Alpes–Léman v0.2** est toujours en préparation.
- Toutes les portes bloquantes de prépublication sont validées.
- Le backend de prépublication est maintenant opérationnel via `tools/build_annecy_prepublication.py`.
- Variante complète : **65 mémoires avec aviation**.
- Variante personnalisée : **48 mémoires sans aviation**.
- Aucun CSV public Annecy–Alpes–Léman v0.2 n'est encore publié.
- AIRAC France : validé pour le périmètre retenu.
- AIRAC Suisse : validé pour le périmètre retenu.
- Périmètre aviation v0.2 : clos de manière conservatrice.
- Contrôle NOTAM France/Suisse : **facultatif et non bloquant** pour un pack d'écoute RX.
- Recontrôle satellites AMSAT : validé le 8 août 2026 pour SO-50, AO-91 et AO-123.
- Une revue finale explicite reste obligatoire avant la création du téléchargement public.

Le script `tools/check_annecy_release_readiness.py` centralise la décision de readiness. Le générateur de prépublication refuse de fonctionner si cette readiness repasse à l'état bloqué.

## Principes du projet

- Réception seule : les exports utilisent `Duplex=off`.
- Noms de mémoires limités à 10 caractères pour l'écran de l'UV-K5.
- Maximum 200 mémoires par pack.
- Pas de remplissage artificiel pour atteindre un nombre cible.
- Les fréquences contestées, non recoupées ou insuffisamment documentées restent hors production.
- Pour l'ISS et les satellites, seule la liaison descendante est mémorisée ; la liaison montante reste une métadonnée documentaire.
- Les données aéronautiques sont destinées à l'écoute et ne constituent pas une source de préparation ou de conduite d'un vol.

## Annecy–Alpes–Léman v0.2

Le candidat complet de 65 mémoires comprend :

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

Lorsque l'option aviation est désactivée, les 17 mémoires aviation sont retirées et le candidat contient **48 mémoires**. Les autres positions mémoire restent inchangées : elles ne sont pas compactées artificiellement.

Albertville `LFKA`, Megève `LFHM` et Genève `LSGG` sont volontairement exclus de la v0.2 faute de tableau primaire suffisamment extractible dans le workflow actuel. Sallanches `LFHZ` est exclu car l'aérodrome est fermé.

### Satellites retenus

- `SAT-SO50` : descente 436.795 MHz ; montée conservée en métadonnée 145.850 MHz, CTCSS 67 Hz ; activation 74.4 Hz.
- `SAT-AO91` : descente 145.960 MHz ; fonctionnement limité aux passages éclairés à cause de la batterie.
- `SAT-AO123` : descente 435.400 MHz ; montée conservée en métadonnée 145.850 MHz, CTCSS 67 Hz.

## Générateur de prépublication

Le backend est branché, mais **pas encore l'interface publique du site**.

Génération complète avec aviation et sans contrôle NOTAM demandé :

```powershell
python tools\build_annecy_prepublication.py
```

Génération sans aviation :

```powershell
python tools\build_annecy_prepublication.py --no-aviation
```

Génération avec contrôle NOTAM demandé mais non confirmé :

```powershell
python tools\build_annecy_prepublication.py --notam-check requested_unconfirmed
```

Génération avec contrôle NOTAM confirmé :

```powershell
python tools\build_annecy_prepublication.py --notam-check user_confirmed
```

Le contrôle NOTAM est enregistré dans le manifeste JSON, mais **ne modifie jamais le contenu des fréquences du CSV** et ne bloque pas la génération.

Les sorties de prépublication sont créées sous :

```text
research/annecy-alpes-leman-v0.2/generated/prepublication/
```

Ce dossier est ignoré par Git. La prépublication reste hors de `website/public`.

Le futur téléchargement public est réservé à :

```text
website/public/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv
```

Ce fichier **n'est pas encore créé**.

## Options du futur générateur web

Deux options indépendantes sont maintenant implémentées côté backend de prépublication :

- **Inclure les fréquences aviation** : ajoute ou retire les 17 mémoires aviation validées.
- **Contrôle NOTAM avant génération** : enregistre l'état de vérification dans le manifeste sans altérer le CSV.

États NOTAM pris en charge :

- `disabled`
- `requested_unconfirmed`
- `user_confirmed`
- `automatic_verified` reste réservé pour une future automatisation fiable.

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

Tester le générateur historique :

```powershell
python tests\test_generator.py
```

## Construire le candidat Annecy interne

```powershell
python tools\build_annecy_internal_candidate.py
```

Les fichiers internes restent sous :

```text
research/annecy-alpes-leman-v0.2/generated/
```

## Contrôler la readiness Annecy

```powershell
python tools\check_annecy_release_readiness.py
```

Résultat attendu depuis le Sprint 17 :

```text
READY: Annecy–Alpes–Léman v0.2 may enter public prepublication
ADVISORY: notam_fr (advisory_optional_pre_generation)
ADVISORY: notam_ch (advisory_optional_pre_generation)
```

Le statut `READY` autorise la génération de prépublication ; il ne publie rien automatiquement.

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
```

La CI GitHub exécute automatiquement les tests de données, le générateur de prépublication et le build Astro.

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

## Prochaine étape

La prochaine étape est la **revue finale du CSV de prépublication de 65 mémoires** : positions, noms, modes, pas, commentaires et cohérence CHIRP. Après cette revue, nous pourrons préparer l'intégration du générateur dans le site et seulement ensuite décider explicitement de créer le téléchargement public v0.2.

## Maintenance du projet

Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint afin de refléter l'état réel du dépôt, les fonctions disponibles, les commandes utiles et les prochaines portes de publication.

La CI vérifie la présence des informations correspondant au sprint courant dans le README. Lors d'un nouveau sprint, ce contrôle doit être mis à jour en même temps que le README.

Les caches Python (`__pycache__/` et `*.py[cod]`) sont ignorés par Git afin de garder le dépôt local propre après l'exécution des scripts et des tests.

Le détail historique des évolutions reste conservé dans [CHANGELOG.md](CHANGELOG.md).

## Sécurité et usage

Les exports RadioPack sont destinés à l'écoute. Voir [NOTICE_LEGAL.md](NOTICE_LEGAL.md) pour les précautions et limites d'utilisation.
