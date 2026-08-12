# Sprint 73 — publication Bretagne v0.1

Date : 12 août 2026
État logique : `0.21.62`

## Publication

Bretagne v0.1 est publiée avec **135 mémoires RX** et devient immuable. Le CSV public correspond octet pour octet au candidat interne figé et revu en Sprint 72.

Le pack conserve :

- 16 PMR446 ;
- 90 voies VHF maritimes génériques ;
- 6 écoutes radioamateur ;
- 2 appels radioamateur ;
- 21 mémoires régionales après déduplication RF.

Ch64 (156.225 / 160.825 MHz) et Ch79 (156.975 / 161.575 MHz) restent deux paires RX génériques de deux mémoires chacune, sans attribution locale de site non prouvée.

## Périmètre différé

Aviation AIRAC courante, fréquences opérationnelles ADRASEC non publiées, mappings locaux CROSS et infrastructures amateur arrêtées/non résolues restent explicitement reportés à Bretagne v0.2. Leur report ne vaut jamais validation.

## Immutabilité

`research/bretagne-v0.1/publication-record.json` enregistre le SHA-256 du CSV public et interdit toute mutation silencieuse de cette version.

Les artefacts de prépublication du Sprint 72 restent inchangés comme preuves historiques ; `publication-record.json` porte seul la transition explicite vers la publication.
