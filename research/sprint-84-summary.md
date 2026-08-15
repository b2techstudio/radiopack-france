# Sprint 84 — kit terrain Normandie v0.5

État logique cible : **0.21.73**.

Le Sprint 84 ne modifie pas le candidat Normandie v0.5 : **142 mémoires RX, delta 0**. Il prépare uniquement un kit terrain reproductible pour les deux dossiers qui nécessitent encore une preuve locale depuis Mortain-Bocage : **R3 F1ZBX** et **F5ZHA Laval**.

## Kit CHIRP RX-only

Le nouveau fichier `research/normandie-v0.5/field-validation-kit.json` définit six sondes distinctes :

- `R3-OUT` — 145.675 MHz, sonde principale R3 ;
- `R3-IN` — 145.075 MHz, écoute opportuniste de l'autre côté de la paire ;
- `ZHA-VHF` — 145.4675 MHz, paire REF actuelle F5ZHA ;
- `ZHA-UHF` — 432.575 MHz, paire REF actuelle F5ZHA ;
- `ZHA-OLD` — 431.4125 MHz, ancienne valeur secondaire conservée uniquement pour diagnostic ;
- `CTRL-ZHY` — 145.6875 MHz, contrôle local facultatif du récepteur/antenne.

Toutes les mémoires sont RX-only : `Duplex=off`, `Offset=0.000000`, aucun filtre CTCSS RX et aucune émission autorisée.

## Journal terrain

Le builder `tools/build_normandie_v05_field_validation_kit.py` génère :

1. `normandie-v0.5-field-rx.csv` — mini-pack CHIRP de six mémoires ;
2. `normandie-v0.5-field-session-template.csv` — journal vide avec les champs nécessaires à une session reproductible ;
3. `normandie-v0.5-field-kit-manifest.json` — rappel machine des gates et règles.

Le journal prévoit notamment date/heure, lieu, récepteur, antenne, fréquence, détection, confiance d'identification, intelligibilité 0–5, force de signal observée et notes.

## Gates conservés

### R3 F1ZBX

Le gate reste inchangé : au moins **deux sessions RX indépendantes** avec réception identifiée et répétable de la sortie **145.675 MHz** depuis Mortain. Une porteuse faible isolée ne suffit pas. L'entrée 145.075 MHz reste facultative pour le gate de couverture. Si le gate est franchi, la paire représente toujours **deux mémoires RX distinctes**.

### F5ZHA Laval

La paire de diagnostic courante reste **145.4675 / 432.575 MHz**. Il faut au moins **deux sessions indépendantes**, avec réception identifiée et intelligibilité minimale 3/5. La sonde 431.4125 MHz reste strictement diagnostique : elle ne constitue jamais à elle seule une preuve de promotion et ne remplace pas la paire REF actuelle.

## Effet sur le pack

- candidat v0.5 avant : **142** ;
- candidat v0.5 après : **142** ;
- delta RF : **0** ;
- aucun CSV public v0.5 ;
- aucun changement du registre ;
- Normandie v0.4 reste immuable.

Garde-fou : `tests/test_sprint84_normandie_v05_field_validation_kit.py`.

## Clôture

Le HEAD de clôture passe la CI complète et déclenche une archive de référence exacte via `[reference-archive]`. Cette étape ne modifie ni les gates terrain, ni le candidat 142, ni les packs publics.
