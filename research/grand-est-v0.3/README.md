# Grand Est v0.3 — Sprint 102

Statut : **recherche uniquement — aucune mutation publique**.

Base publique immuable : **Grand Est v0.2 / 59 mémoires RX**.
SHA-256 public v0.2 : `a50416bd8a88af249bb691daa657ffd4b578daf1324bd0ca4dd632a2f1a0e5c1`.

## Objectif

Construire une future v0.3 à partir de la v0.2 publiée, sans remplissage artificiel et sans reconduire automatiquement des relais dont le mode ou l'état courant a changé.

Le Sprint 102 commence par un audit radio actuel. L'aviation reste figée sur la base AIRAC 08/26 de la v0.2 tant qu'une révision aviation n'est pas explicitement lancée ; toute révision sur ou après le 3 septembre 2026 devra être faite sur AIRAC 09/26.

## Premier constat radio

La v0.2 contient huit relais 2 m paired-RX. Sept restent compatibles avec un inventaire analogique courant au premier passage. `F1ZAX` demande une résolution de mode avant toute reconduction : l'inventaire REF courant le classe en C4FM, alors que des annuaires secondaires peuvent encore l'afficher FM/Fusion.

Le premier balayage fait aussi apparaître plusieurs infrastructures analogiques actuelles absentes de la v0.2, notamment :

- `F5ZUD` — Vandoeuvre/Nancy — 145.7125 / 145.1125 MHz ;
- `F1ZUV` — Strasbourg — crossband 144.750 / 439.750 MHz ;
- `F5ZAW` — Bellefosse / Champ du Feu — crossband 145.2125 / 433.425 MHz ;
- `F5ZYS` — Dogneville — 439.775 / 430.375 MHz ;
- ainsi qu'un backlog plus large en Ardennes, Aube, Meuse, Moselle, Bas-Rhin, Haut-Rhin et Vosges.

Aucun de ces éléments ne modifie encore le CSV public. Les ajouts ne seront promus qu'après validation suffisante de la fréquence, du mode, de l'état courant et de la pertinence pour un pack d'écoute analogique.

## Règles

- réception uniquement ;
- `Duplex=off` ;
- `Offset=0.000000` ;
- paired RX pour chaque paire distincte vérifiée ;
- déduplication par fréquence RF ;
- maximum 200 mémoires ;
- pas d'inférence de fréquence ou de mode manquant ;
- pas de données opérationnelles privées / PPDR ;
- versions publiques déjà publiées immuables.

## Fichiers du Sprint 102

- `radio-validation-pass1-2026-08-22.json` : audit radio initial ;
- `backlog.json` : éléments à confirmer / résoudre ;
- `release-scope.json` : limites de la phase de recherche ;
- `tests/test_grand_est_v03_initialization.py` : garde-fous de démarrage ;
- `.github/workflows/grand-est-v03-research.yml` : CI dédiée.
