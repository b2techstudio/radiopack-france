# Sprint 21 — Publication Annecy–Alpes–Léman v0.2

Date : 2026-08-08

## Résultat

Annecy–Alpes–Léman v0.2 passe de la prépublication revue à la publication explicite.

- Pack standard : 65 mémoires RX.
- Variante sans aviation : 48 mémoires RX.
- Toutes les mémoires utilisent `Duplex=off`.
- Les positions restent celles validées au Sprint 19.
- Le contrôle NOTAM reste facultatif et n'altère jamais le CSV.

## Génération publique

Une bibliothèque commune `website/src/lib/annecyPack.ts` assemble les données validées et génère le format CHIRP.

Deux routes Astro prérendues sont publiées :

- `/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv`
- `/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2-sans-aviation.csv`

Le générateur `/generateur` utilise la même bibliothèque et peut télécharger la variante correspondant au choix Aviation.

## NOTAM

Le contrôle NOTAM est informatif :

- `disabled` : aucun contrôle déclaré ;
- `requested_unconfirmed` : contrôle demandé mais non confirmé ;
- `user_confirmed` : l'utilisateur indique avoir vérifié les NOTAM applicables.

Aucun de ces états ne modifie les fréquences du CSV.

## Historique Annecy v0.1

Le générateur Python historique ne régénère plus les fichiers Annecy v0.1. Les anciens fichiers peuvent rester dans l'historique du dépôt, mais ne sont plus utilisés pour la publication courante.

## Sécurité

RadioPack France reste un projet d'écoute. Les données aéronautiques ne constituent pas une source de préparation ou de conduite d'un vol.
