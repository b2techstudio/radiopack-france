# Sprint 64 — contrat deux mémoires RX / sessions de preuve

Date : 11 août 2026

## Objectif

Lever l'ambiguïté entre :

- le **nombre de fréquences/mémoires RX** nécessaires pour écouter une liaison duplex ou split ;
- le **nombre de sessions de validation terrain** nécessaires pour démontrer une réception locale.

Aucune fréquence nouvelle n'est ajoutée et aucun pack public n'est modifié.

## R3 / F1ZBX Brocéliande

La paire reste :

- 145.075 MHz — entrée relais, écoutée en RX ;
- 145.675 MHz — sortie relais, écoutée en RX.

Le contrat fixe **2 mémoires RX distinctes** si la porte R3 est un jour franchie.

La porte terrain reste indépendante : elle exige toujours **2 sessions RX indépendantes** avec réception identifiée et répétable de la sortie 145.675 MHz depuis Mortain-Bocage.

Les 2 sessions sont des preuves ; elles ne créent pas de troisième ou quatrième mémoire.

Le mini-pack `r3-validation-pack.json` contient toujours trois lignes parce que `CTRL-ZHY` 145.6875 MHz reste une sonde facultative de contrôle récepteur/antenne. Seules `R3-OUT` et `R3-IN` sont membres de la paire R3.

État : porte non franchie, delta candidat actuel 0, delta futur si porte franchie +2.

## CROSS Étel — canal 64

La paire duplex reste :

- 156.225 MHz — navire vers côte ;
- 160.825 MHz — côte vers navire.

Le contrat fixe **2 mémoires RX distinctes** si le canal devient publiable dans Bretagne v0.1.

Les deux fréquences étaient déjà présentes dans le plan de recherche. Le conflit de sources primaires actuel et l'absence de site Ch64 réconcilié restent bloquants.

État : aucune promotion, nouveau delta RF 0.

## CROSS Corsen — canal 79

La paire duplex reste :

- 156.975 MHz — navire vers côte ;
- 161.575 MHz — côte vers navire.

Le contrat fixe **2 mémoires RX distinctes** si le canal devient publiable dans Bretagne v0.1.

Les deux fréquences étaient déjà présentes dans le plan de recherche. L'émetteur/site actuel Ch79 reste sans validation primaire suffisante.

État : aucune promotion, nouveau delta RF 0.

## Garde-fous ajoutés

`research/paired-rx-policy.json` passe au schéma 1.1 et distingue explicitement sessions de preuve et mémoires RX.

`research/sprint-64-dual-rx-contract.json` fige les trois exemples R3 / Ch64 / Ch79.

`tests/test_sprint64_dual_rx_contract.py` vérifie notamment :

- exactement 2 membres de paire R3 ;
- 2 sessions R3 indépendantes sans lien avec le nombre de mémoires ;
- Ch64 = 156.225 + 160.825 MHz ;
- Ch79 = 156.975 + 161.575 MHz ;
- 2 sens RX pour chaque voie maritime duplex ;
- aucun changement de pack public tant que les portes restent fermées ;
- TX toujours bloqué avec `Duplex=off` et `Offset=0.000000`.

## État global après Sprint 64

Normandie v0.4 reste à :

- candidat interne 142 ;
- preview 142 ;
- plafond connu 147 ;
- revue 3/9 ;
- 6 blocages ;
- 0 ajout éligible.

Packs publics inchangés :

- Normandie v0.3.1 : 139 mémoires ;
- Annecy–Alpes–Léman v0.2 : 65 mémoires, variante 48 sans aviation ;
- Bretagne : toujours non publique.
