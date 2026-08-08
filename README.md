# RadioPack France

Codeplugs CHIRP régionaux, documentés et générés à partir de données publiques vérifiables pour les radios Quansheng UV-K5.

Le projet privilégie une approche prudente : aucune fréquence n'est ajoutée uniquement pour remplir un pack, les sources doivent être identifiables, et les exports sont configurés en réception seule.

## État actuel — Sprint 20

- Pack public disponible : **Normandie v0.3.1**.
- **Annecy–Alpes–Léman v0.2** est toujours en préparation.
- Toutes les portes bloquantes de prépublication sont validées.
- Le backend de prépublication est opérationnel via `tools/build_annecy_prepublication.py`.
- La variante complète a été revue ligne par ligne : **65/65 mémoires** validées.
- Variante personnalisée : **48 mémoires sans aviation**, contrôlée comme sous-ensemble exact.
- La carte de référence est `research/annecy-alpes-leman-v0.2/prepublication-reviewed-memory-map.json`.
- Statut du plan : `prepublication_reviewed_not_public`.
- L'**aperçu web du générateur** est maintenant accessible sur `/generateur`.
- Les options Aviation et NOTAM y sont interactives et le compteur passe réellement de 65 à 48 mémoires lorsque l'aviation est retirée.
- Contrôle NOTAM France/Suisse : **facultatif et non bloquant** pour un pack d'écoute RX.
- Le **téléchargement Annecy v0.2 reste verrouillé** et aucun CSV public v0.2 n'est encore créé.
- Recontrôle satellites AMSAT : validé le 8 août 2026 pour SO-50, AO-91 et AO-123.

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

## Revue finale Sprint 19

La carte `prepublication-reviewed-memory-map.json` fige pour chacune des 65 mémoires :

- `Location` ;
- `Name` ;
- `Frequency` ;
- `Mode` ;
- `TStep` ;
- le bloc fonctionnel ;
- l'empreinte SHA-256 du commentaire validé.

La CI compare chaque génération à cette carte. Elle vérifie également `Duplex=off`, `Offset=0.000000`, l'absence de tone d'émission et l'absence de champs TX inutiles.

La variante sans aviation doit correspondre exactement à la carte après retrait des deux blocs aviation. Une génération avec NOTAM confirmé doit produire un CSV octet pour octet identique à la génération avec NOTAM désactivé.

## Générateur web — Sprint 20

L'aperçu web est disponible sur :

```text
/generateur
```

Il est relié aux mêmes règles fonctionnelles que le backend de prépublication :

- **Inclure les fréquences aviation** : le compteur passe de 65 à 48 mémoires lorsqu'on décoche l'option ;
- **Contrôle NOTAM avant génération** : affiche une confirmation facultative « J'ai vérifié les NOTAM applicables » ;
- le résumé indique en direct le nombre de mémoires, l'état aviation et l'état NOTAM ;
- le contrôle NOTAM ne modifie jamais les fréquences ;
- le bouton de génération CSV Annecy reste désactivé tant que la publication n'a pas été déclenchée explicitement.

L'aperçu web visible ne signifie donc pas que la v0.2 est publiée. Le futur CSV reste absent de `website/public`.

## Générateur de prépublication local

Génération complète avec aviation :

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

## Synchroniser le dépôt local

Depuis PowerShell :

```powershell
cd "C:\Users\cross\Documents\CODE\PROJETS\RadioPack-France"
git pull --ff-only
git status
```

Les archives de sprint sont uniquement des sauvegardes de référence. Elles ne doivent plus être copiées ou décompressées dans le dépôt local lorsque les mêmes fichiers sont déjà présents sur GitHub.

## Contrôler Annecy localement

```powershell
python tools\check_annecy_release_readiness.py
python tools\build_annecy_prepublication.py
python tests\test_annecy_prepublication.py
python tests\test_annecy_prepublication_review.py
python tests\test_web_generator.py
```

Le test web doit terminer par :

```text
Tests RadioPack Sprint 20 web generator preview: OK
```

## Générer les CSV publics existants

```powershell
python generator\generate_chirp_csv.py
```

Tester le générateur historique :

```powershell
python tests\test_generator.py
```

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

La CI GitHub exécute automatiquement les tests de données, la revue du CSV, le contrat du générateur web et le build Astro.

## Lancer le site en local

```powershell
cd website
npm install
npm run dev
```

Ouvre ensuite notamment :

```text
http://localhost:4321/generateur
```

Pour reproduire le build de production :

```powershell
npm run build
```

## Déploiement

Le site Astro est prévu pour Cloudflare Pages. Les changements sur `main` déclenchent la CI et le déploiement configuré du projet.

## Prochaine étape

La prochaine étape sera le sprint de **publication explicite Annecy–Alpes–Léman v0.2** : création contrôlée du CSV public à partir de la carte revue, activation du téléchargement dans le générateur, mise à jour des pages publiques et contrôle final avant diffusion.

## Maintenance du projet

Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint afin de refléter l'état réel du dépôt, les fonctions disponibles, les commandes utiles et les prochaines portes de publication.

La CI vérifie la présence des informations correspondant au sprint courant dans le README. Lors d'un nouveau sprint, ce contrôle doit être mis à jour en même temps que le README.

Les caches Python (`__pycache__/` et `*.py[cod]`) sont ignorés par Git afin de garder le dépôt local propre après l'exécution des scripts et des tests.

Le détail historique des évolutions reste conservé dans [CHANGELOG.md](CHANGELOG.md).

## Sécurité et usage

Les exports RadioPack sont destinés à l'écoute. Voir [NOTICE_LEGAL.md](NOTICE_LEGAL.md) pour les précautions et limites d'utilisation.
