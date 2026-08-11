# Sprint 71 — Normandie v0.5 revalidation / Bretagne v0.1 internal candidate

Date : 11 août 2026
État logique : `0.21.60`

## Normandie v0.5

La base reste la Normandie v0.4 publique immuable à **142 mémoires RX**. Le Sprint 71 ne promeut aucune fréquence : R3/F1ZBX manque toujours deux sessions RX indépendantes depuis Mortain, F5ZHA manque une réconciliation autoritative et une validation terrain, F1ZOV reste en maintenance chez l'opérateur local et F6ZES reste sans fréquence/mode prouvés. Candidat v0.5 : **142**, delta **0**.

## Bretagne v0.1

Un premier candidat interne reproductible de **135 mémoires RX** est construit par `tools/build_bretagne_internal_candidate.py` :

- 16 PMR446 ;
- 90 mémoires VHF maritime génériques ;
- 6 mémoires d'écoute amateur ;
- 2 mémoires d'appel amateur ;
- 21 mémoires régionales nouvelles après déduplication avec les blocs nationaux.

Les 29 fréquences du plan régional source fusionnent 8 fréquences maritimes déjà présentes dans le bloc national et ajoutent 21 RF uniques. Les canaux 64 et 79 restent chacun une paire de **deux mémoires RX génériques** ; aucun site local n'est revendiqué sans preuve primaire explicite.

L'aviation reste à **0 mémoire**, avec les emplacements 130–149 réservés en attente d'une extraction SIA actuelle. Bretagne reste strictement non publique.
