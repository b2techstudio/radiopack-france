# Bretagne v0.3 — recherche

État : **Sprint 111 / 0.21.99 — préparation AIRAC 09/26 structurée, candidat toujours 151 mémoires RX, delta RF 0, aucune publication v0.3**.

La base publique reste **Bretagne v0.2 / 151 RX**, immuable, SHA-256 `73aa3d530ae9f6c572eb01794b0861ecba61df0faf7884ee766085d3de7601a4`. Le candidat v0.3 interne reproduit toujours exactement cette base tant qu'aucune revalidation future ne justifie un changement.

## Sprint 111 — readiness AIRAC 09/26

Le 22 août 2026, le produit SIA **Données aéronautiques XML AIRAC 09/26** est déjà disponible publiquement, mais sa période d'effet commence seulement le **3 septembre 2026** et se termine le **30 septembre 2026**. Sa disponibilité anticipée n'en fait donc jamais une source *courante* avant le 3 septembre.

Fichiers ajoutés :

- `airac09-readiness.json` — source future, dates, baseline et règles de transition ;
- `airac09-revalidation-template.json` — matrice vide couvrant exactement les **16 mémoires aviation** actuelles aux positions 130–145 ;
- `tools/check_bretagne_v03_airac09_revalidation.py` — validateur déterministe de la future revue.

Chaque mémoire devra recevoir une décision explicite : `unchanged`, `changed` ou `removed`. Une décision résolue doit être associée au cycle **AIRAC 09/26**, à sa date d'effet, à une source et à une note de preuve. Une seule mémoire laissée non résolue bloque la reconstruction interne.

Le validateur impose également :

- cycle 09/26 réellement courant à la date d'évaluation ;
- vérification d'une source primaire courante ;
- revue humaine datée dans la fenêtre AIRAC 09/26 ;
- aucune revendication de correspondance XML champ par champ si les octets XML n'ont pas été extraits ;
- aucune mutation automatique du candidat ;
- aucune publication automatique.

Avant le 3 septembre, ce contrôle doit rester bloqué :

```bash
python tools/check_bretagne_v03_airac09_revalidation.py --as-of 2026-08-22
```

Le 3 septembre ou après, copier le template vers un nouveau fichier de preuve, le renseigner à partir des sources alors courantes, puis exécuter par exemple :

```bash
python tools/check_bretagne_v03_airac09_revalidation.py \
  --as-of 2026-09-03 \
  --evidence research/bretagne-v0.3/airac09-revalidation-2026-09-03.json \
  --require-candidate-rebuild-ready
```

Même si ce contrôle devient vert, il autorise seulement la **reconstruction du candidat interne**. Une publication v0.3 nécessite encore des gates de prépublication séparés et une nouvelle version immuable.

## Baseline aviation à revalider

Les 16 mémoires héritées d'AIRAC 08/26 sont :

- `AIR-EMERG` 121.500 ;
- `RNS-COT-A` 120.350 ;
- `RNS-NORD` 126.950 ;
- `RNS-SUD` 134.000 ;
- `RNS-COT-B` 134.200 ;
- `RNS-GND` 121.730 ;
- `RNS-TWR` 120.505 ;
- `RNS-ATIS` 136.405 ;
- `BES-IRO1` 119.575 ;
- `BES-IRO2` 135.830 ;
- `BES-APP` 125.860 ;
- `BES-TWR` 120.105 ;
- `BES-ATIS` 129.355 ;
- `DIN-TWR` 120.155 ;
- `DIN-ATIS` 124.580 ;
- `QUIM-TWR` 118.625 MHz.

Cette liste est une **baseline AIRAC 08/26**, pas une affirmation sur AIRAC 09/26.

## Sprint 82 — dossiers non-AIRAC

`public-service-revalidation.json` reste la dernière revue des six dossiers non-AIRAC. Aucun ne produit de nouvelle RF : **delta 0**.

- F1ZUG APRS 144.800 MHz reste déjà couvert nationalement ; le transpondeur ADRASEC35 reste sans fréquence publique ;
- F5ZZC-4 reste non résolu faute de source actuelle de fréquence ;
- F5ZPV et F5ZZH restent arrêtés selon l'opérateur local ;
- CROSS Étel Ch64 et CROSS Corsen Ch79 restent des paires génériques sans attribution locale suffisamment prouvée.

Ils ne sont rouverts que si une nouvelle preuve publique actuelle apparaît.

## Transition AIRAC

AIRAC 08/26 reste la référence applicable jusqu'au **2 septembre 2026 inclus**. AIRAC 09/26 devient la référence requise à partir du **3 septembre 2026**. La v0.2 publiée ne change jamais lors de cette transition : seule une future v0.3 peut être reconstruite puis éventuellement publiée après revue complète.

Voir `airac-transition-policy.json`, `airac09-handoff.json` et `airac09-readiness.json`.

## Règles permanentes

- RX uniquement : `Duplex=off`, `Offset=0.000000` ;
- base v0.2 immuable ;
- aucune donnée future traitée comme courante avant sa date d'effet ;
- aucune RF déjà présente dupliquée pour une simple métadonnée locale ;
- aucune donnée opérationnelle privée PPDR/ADRASEC recherchée ou déduite ;
- aucune fréquence ou attribution ambiguë devinée ;
- une infrastructure arrêtée n'est pas promue ;
- une transition AIRAC déclenche une revue de fraîcheur, jamais un ajout automatique ;
- reconstruction interne et publication restent deux opérations distinctes.
