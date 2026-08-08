# Sprint 19 — revue finale du CSV de prépublication

Date : 2026-08-08

## Résultat

La variante complète Annecy–Alpes–Léman v0.2 a été revue ligne par ligne : **65 mémoires sur 65**.

La revue fige pour chaque mémoire :

- le numéro `Location` ;
- le nom affiché, limité à 10 caractères ;
- la fréquence reçue ;
- le mode CHIRP ;
- le pas `TStep` ;
- le bloc fonctionnel ;
- l'empreinte SHA-256 du commentaire validé.

La carte de référence est stockée dans :

`research/annecy-alpes-leman-v0.2/prepublication-reviewed-memory-map.json`

## Garde-fous CHIRP

La CI vérifie désormais pour chaque ligne :

- `Duplex=off` ;
- `Offset=0.000000` ;
- aucun `Tone` d'émission ;
- aucune puissance TX renseignée ;
- les champs D-STAR inutilisés restent vides ;
- les noms, emplacements et fréquences sont uniques ;
- le commentaire correspond exactement au commentaire revu grâce à son SHA-256.

## Variante sans aviation

La variante `--no-aviation` doit contenir **48 mémoires** et correspondre exactement à la carte de revue après retrait des deux blocs aviation. Les autres numéros de mémoire ne sont pas compactés.

## NOTAM

La variante `--notam-check user_confirmed` doit produire un CSV **octet pour octet identique** à la génération avec NOTAM désactivé. Le statut NOTAM reste uniquement dans le manifeste JSON.

## Publication

La revue est terminée, mais le téléchargement public n'est toujours pas créé. Le plan passe à `prepublication_reviewed_not_public` avec `public_export_allowed: false`.

La prochaine étape pourra préparer l'intégration du générateur au site et l'action explicite de publication de la v0.2.
