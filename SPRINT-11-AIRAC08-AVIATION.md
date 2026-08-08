# RadioPack France — Sprint 11

Ce sprint lève partiellement le gel aviation d'Annecy–Alpes–Léman v0.2 après l'entrée en vigueur du cycle AIRAC 08/26, sans publier le pack régional.

## Résultat

Le candidat interne passe de 48 à 57 mémoires.

```text
000–015  PMR446                              16
020–025  APRS / ISS                           6
026–028  Satellites FM                        3
030–031  Canaux d'appel                       2
040–058  Radioamateur France                 19
090–091  Radioamateur Suisse                  2
125–131  Aviation France / bassin genevois    7
155–156  Aviation Suisse                      2
Total                                        57
```

Toutes les mémoires restent en réception seule avec `Duplex=off`.

## Aviation France / bassin genevois

Le fichier `research/annecy-alpes-leman-v0.2/aviation-france-airac-08.json` contient sept lignes autorisées dans le candidat interne :

- Annecy-Meythet — 118.200 MHz ;
- Annemasse — 125.875 MHz ;
- Grenoble-Le Versoud — 121.000 MHz ;
- Grenoble-Alpes-Isère GND — 121.930 MHz ;
- Grenoble-Alpes-Isère TWR/VDF — 119.300 MHz ;
- Grenoble-Alpes-Isère ATIS — 133.855 MHz ;
- Genève Information — 126.350 MHz.

Le cycle courant est AIRAC 08/26, effectif du 6 août au 2 septembre 2026 inclus.

Le pré-inventaire `aviation-france-pre-airac-08.json` reste conservé comme historique mais l'assembleur refuse toujours ce fichier.

## Aviation française encore en attente

Les quatre fréquences de Chambéry présentes dans le pré-inventaire ne sont pas promues automatiquement. Chambéry reste en attente de l'extraction publique du tableau courant.

Albertville, Megève et Sallanches restent également hors candidat jusqu'à extraction et recoupement d'une publication officielle courante suffisamment précise.

## Aviation Suisse

Skyguide indique comme cycle courant `AIP AIRAC AMDT: 06 AUG 2026`.

Le site officiel de l'aéroport de Lausanne publie :

- LSGL AD — 123.205 MHz ;
- APCH INFO — 118.830 MHz.

Ces deux fréquences sont ajoutées au candidat interne aux mémoires 155 et 156.

Genève-aéroport et Sion restent en attente d'un recoupement courant suffisamment précis. Genève Information 126.350 MHz est déjà présente une seule fois dans le bloc transfrontalier et n'est pas dupliquée.

## Garde-fous

L'assembleur :

- accepte uniquement `verified_airac08_public` pour le fichier aviation France ;
- accepte uniquement `verified_current_public` pour le fichier aviation Suisse ;
- refuse toujours le pré-inventaire AIRAC 07/26 ;
- refuse toujours les données lacustres ;
- refuse les statuts `pending_*`, `pre_airac_recheck` et les données radioamateur suisses non confirmées ;
- vérifie l'absence de doublons de fréquences et de positions mémoire ;
- produit uniquement un candidat local avec `public_export_allowed: false`.

## Tests

Le nouveau test :

```powershell
python tests\test_annecy_airac08.py
```

contrôle les deux inventaires AIRAC 08, les statuts, le mode AM, le pas 8.33 kHz, les fréquences et les éléments encore en attente.

Le test du candidat interne vérifie maintenant les 57 mémoires et les positions aviation.

## Ce qui ne change pas

- aucun CSV Annecy v0.2 n'est publié ;
- aucune page publique n'annonce la v0.2 disponible ;
- le pack historique v0.1 reste non proposé au téléchargement ;
- les lacs restent à zéro mémoire ;
- le générateur public n'est pas relié aux fichiers de recherche v0.2.

## Synchronisation locale

Depuis PowerShell :

```powershell
cd "C:\Users\cross\Documents\CODE\PROJETS\RadioPack-France"
git pull --ff-only
python tools\build_annecy_internal_candidate.py
python tests\test_annecy_airac08.py
python tests\test_annecy_internal_candidate.py
git status
```

Le candidat local est généré dans `research\annecy-alpes-leman-v0.2\generated\`, dossier ignoré par Git.

## Prochaine étape

Compléter les fréquences encore en attente, effectuer le contrôle NOTAM avant publication, puis seulement préparer un candidat v0.2 publiable avec CSV CHIRP et documentation.
