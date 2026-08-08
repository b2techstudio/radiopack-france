# RadioPack France — Sprint 13

Ce sprint ferme le dossier Chambéry Aix-les-Bains dans la recherche aviation Annecy–Alpes–Léman v0.2, sans publier le pack régional.

## Résultat

Le candidat interne passe de 61 à 65 mémoires.

```text
000–015  PMR446                              16
020–025  APRS / ISS                           6
026–028  Satellites FM                        3
030–031  Canaux d'appel                       2
040–058  Radioamateur France                 19
090–091  Radioamateur Suisse                  2
125–135  Aviation France / bassin genevois   11
155–160  Aviation Suisse                      6
Total                                        65
```

Toutes les mémoires restent en réception seule avec `Duplex=off`.

## Chambéry LFLB

Le tableau officiel SIA AIP France AD 2.18 confirme les quatre fréquences du pré-inventaire :

- `CHAM-INFO` — 123.700 MHz — FIS / APP / A/A selon le service actif ;
- `CHAM-APP` — 121.205 MHz — APP ;
- `CHAM-TWR` — 118.300 MHz — TWR ;
- `CHAM-ATIS` — 127.100 MHz — ATIS.

Les quatre entrées portent désormais le statut `verified_airac08_public`, utilisent le mode `AM`, un pas de `8.33` kHz et la politique `rx_only`.

## Positions mémoire

Le bloc aviation France est réorganisé ainsi :

```text
125 ANNCY-TWR
126 ANNMS-A-A
127 CHAM-INFO
128 CHAM-APP
129 CHAM-TWR
130 CHAM-ATIS
131 VERSD-A-A
132 GREN-GND
133 GREN-TWR
134 GREN-ATIS
135 GENEV-INFO
```

Le bloc aviation Suisse reste inchangé aux mémoires 155 à 160.

## Sources primaires encore incomplètes

Trois aérodromes restent dans la porte `pending_airfields` :

- Albertville LFKA ;
- Megève LFHM ;
- Genève LSGG.

Pour Albertville et Megève, le catalogue SIA référence bien les VAC courantes. Leur contenu radio primaire n'a toutefois pas pu être extrait de manière fiable dans le workflow actuel. Les fréquences visibles sur des sources secondaires ne sont donc pas intégrées.

Pour Genève-aéroport, les sources officielles identifient l'aérodrome et renvoient vers les publications Skyguide/AIP, mais le tableau radio courant n'est pas suffisamment extractible publiquement dans le workflow actuel. `GENEV-INFO` 126.350 MHz reste déjà présent une seule fois pour le bassin transfrontalier.

## Portes de publication

Le pack reste non publiable :

- AIRAC France : validation recherche passée ;
- AIRAC Suisse : validation recherche passée ;
- NOTAM France : briefing SOFIA à refaire le jour de publication ;
- NOTAM Suisse : briefing Skybriefing à refaire le jour de publication ;
- aérodromes restants : LFKA, LFHM et LSGG ;
- satellites FM : statut opérationnel à revérifier juste avant publication.

`public_release_allowed` et `public_export_allowed` restent à `false`.

## Tests

Les tests doivent vérifier :

- exactement 11 fréquences aviation France ;
- exactement 65 mémoires dans le candidat interne ;
- les quatre fréquences Chambéry et leurs positions 127 à 130 ;
- l'absence de données en attente ou secondaires ;
- `Duplex=off` pour toutes les mémoires ;
- le maintien de LFKA, LFHM et LSGG dans la porte de recherche restante.

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

Le candidat local doit annoncer `65 memories`. Le dossier `research\annecy-alpes-leman-v0.2\generated\` reste ignoré par Git.
