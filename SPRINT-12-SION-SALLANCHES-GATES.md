# RadioPack France — Sprint 12

Ce sprint complète une partie du bloc aviation suisse, retire définitivement Sallanches des recherches de fréquences actives et ajoute des portes opérationnelles obligatoires avant toute publication d'Annecy–Alpes–Léman v0.2.

## Résultat

Le candidat interne passe de 57 à 61 mémoires.

```text
000–015  PMR446                              16
020–025  APRS / ISS                           6
026–028  Satellites FM                        3
030–031  Canaux d'appel                       2
040–058  Radioamateur France                 19
090–091  Radioamateur Suisse                  2
125–131  Aviation France / bassin genevois    7
155–160  Aviation Suisse                      6
Total                                        61
```

Toutes les mémoires restent en réception seule avec `Duplex=off`.

## Sion

La page officielle « Infos pilotes » de l'Aéroport de Sion permet de retenir quatre canaux voix ATS/ATIS :

- `CH-SIONGND` — 121.705 MHz ;
- `CH-SIONTWR` — 118.275 MHz ;
- `CH-SIONATI` — 130.630 MHz ;
- `CH-SIONAPP` — 126.825 MHz.

Ils sont ajoutés aux mémoires 157 à 160, après les deux mémoires Lausanne.

Les fréquences de handling 131.475, 131.670 et 131.955 MHz sont explicitement exclues. Les aides de radionavigation ILS 110.7 MHz et VOR SION 112.15 MHz ne sont pas des canaux voix et restent également hors pack.

Les six mémoires aviation suisses utilisent le mode `AM`, un pas de 8.33 kHz et `rx_only`.

## Sallanches-Mont-Blanc

LFHZ n'est plus considéré comme un aérodrome en attente d'extraction. L'arrêté du 24 juillet 2020 a fermé l'aérodrome de Sallanches-Mont-Blanc à toute circulation aérienne avec effet au 1er septembre 2020.

Le fichier aviation France le classe désormais :

```text
excluded_closed_aerodrome
```

Les tests vérifient cette exclusion afin d'éviter une réintroduction ultérieure depuis une ancienne source.

## Portes opérationnelles de publication

Le fichier :

```text
research/annecy-alpes-leman-v0.2/aviation-operational-gates.json
```

sépare désormais la validation documentaire des fréquences du contrôle opérationnel dynamique.

État actuel :

- AIRAC France : validation de recherche passée ;
- AIRAC Suisse : validation de recherche passée ;
- NOTAM France : contrôle SOFIA-Briefing à effectuer le jour de la publication ;
- NOTAM Suisse : contrôle Skybriefing à effectuer le jour de la publication ;
- aérodromes encore non clos : Chambéry LFLB, Albertville LFKA, Megève LFHM et Genève LSGG ;
- satellites FM : statut opérationnel à revérifier juste avant publication.

`public_release_allowed` reste donc à `false`.

Le SIA indique que les NOTAM français ne sont pas hébergés ni indexés sur son site public et renvoie vers SOFIA-Briefing. Un résultat NOTAM ne doit donc jamais être supposé ou conservé comme éternellement valide.

## Ce qui reste en attente

### France

- Chambéry LFLB ;
- Albertville LFKA ;
- Megève LFHM.

### Suisse

- Genève LSGG, hors Genève Information 126.350 MHz déjà couverte dans le bloc transfrontalier.

## Tests renforcés

`tests/test_annecy_airac08.py` vérifie désormais :

- les quatre fréquences Sion ;
- l'absence des fréquences de handling et des aides de navigation ;
- l'exclusion réglementaire de Sallanches ;
- les quatre aérodromes encore à clore ;
- l'état non publiable des portes NOTAM et satellites.

`tests/test_annecy_internal_candidate.py` vérifie :

- exactement 61 mémoires ;
- Sion aux positions 157 à 160 ;
- toutes les mémoires aviation en `AM` / `8.33` ;
- toutes les mémoires en `Duplex=off` ;
- aucune fréquence exclue dans le CSV interne.

## Ce qui ne change pas

- aucun CSV Annecy v0.2 n'est publié ;
- le générateur public reste déconnecté des fichiers de recherche v0.2 ;
- le site affiche toujours Annecy–Alpes–Léman « En préparation » ;
- les lacs restent à zéro mémoire publique ;
- le candidat interne reste dans le dossier `generated/` ignoré par Git.

## Synchronisation locale

```powershell
cd "C:\Users\cross\Documents\CODE\PROJETS\RadioPack-France"
git pull --ff-only
python tools\build_annecy_internal_candidate.py
python tests\test_annecy_airac08.py
python tests\test_annecy_internal_candidate.py
git status
```

Le résultat attendu de l'assembleur est :

```text
Internal candidate only: 61 memories
```

## Étape suivante

Fermer le périmètre de Chambéry, Albertville, Megève et Genève avec des sources officielles courantes suffisamment précises, puis effectuer les contrôles dynamiques NOTAM et satellites immédiatement avant une éventuelle publication v0.2.
