# Sprint 85 — évaluateur de sessions terrain Normandie v0.5

État logique cible : **0.21.74**.

Le Sprint 85 ajoute une évaluation reproductible du journal terrain préparé au Sprint 84. Le candidat Normandie v0.5 reste strictement à **142 mémoires RX, delta 0** et aucune publication v0.5 n'est autorisée.

## Outil

L'évaluateur `tools/evaluate_normandie_v05_field_sessions.py` lit un CSV rempli à partir du modèle généré par `tools/build_normandie_v05_field_validation_kit.py` :

```bash
python tools/evaluate_normandie_v05_field_sessions.py --input observations.csv --output evaluation.json
```

Le rapport JSON conserve les lignes valides, les erreurs de saisie, les `session_id` incohérents, les sessions réellement qualifiantes et le verdict de chaque gate.

## Verdicts

Trois états sont possibles :

- **`satisfied`** : au moins deux sessions indépendantes satisfont le gate terrain ;
- **`insufficient`** : il existe au moins une observation exploitable sur une fréquence qui compte pour le gate, mais les critères sont incomplets ;
- **`indeterminate`** : aucune observation exploitable sur les fréquences qui comptent pour le gate.

L'unité d'indépendance est `session_id`. Plusieurs lignes portant le même identifiant ne créent jamais plusieurs sessions indépendantes. Un même `session_id` avec des métadonnées incompatibles (date/heure, lieu, récepteur ou antenne) est exclu et signalé.

## R3 F1ZBX

Seule la sortie **145.675 MHz** compte pour le gate de couverture. L'entrée **145.075 MHz** reste une écoute opportuniste.

Une session R3 est qualifiante si la sortie est détectée et identifiée avec une confiance `high`, `unmistakable` ou `confirmed`. Avec `high`, une intelligibilité d'au moins **3/5** est exigée ; une identification `unmistakable` ou `confirmed` peut rester qualifiante avec une intelligibilité inférieure si l'identification elle-même est sans ambiguïté.

Deux `session_id` distincts sont requis. Une simple porteuse faible n'est jamais suffisante.

## F5ZHA Laval

Les fréquences courantes de terrain restent **145.4675 MHz** et **432.575 MHz**. Une session qualifiante peut être observée sur l'une ou l'autre de ces deux fréquences, avec :

- signal détecté ;
- confiance `high`, `unmistakable` ou `confirmed` ;
- intelligibilité au moins **3/5**.

Deux `session_id` distincts sont requis. Il n'est pas nécessaire d'avoir entendu les deux côtés de la paire pour satisfaire le gate de **couverture terrain** ; le rapport indique néanmoins quelles fréquences ont été effectivement entendues.

La fréquence historique **431.4125 MHz** reste diagnostique uniquement. Elle ne compte jamais pour le gate et ne peut jamais fermer le conflit de source.

## Sécurité décisionnelle

Même lorsqu'un gate terrain est `satisfied` :

- `promotion_ready` reste toujours `false` ;
- aucune modification automatique du candidat n'est autorisée ;
- aucune publication automatique n'est autorisée ;
- une revue humaine et des sources courantes restent nécessaires avant toute promotion ;
- une non-réception ne constitue jamais une preuve que le relais est arrêté ;
- Normandie v0.4 reste immuable.

Le contrôle `CTRL-ZHY` est rapporté pour diagnostic du matériel mais ne compte pour aucun gate.

## Tests

Le garde-fou `tests/test_sprint85_normandie_v05_field_evaluator.py` couvre les cas `satisfied`, `insufficient` et `indeterminate`, les sessions dupliquées, les métadonnées incohérentes, les non-réceptions, la sonde historique F5ZHA, le contrôle local et les CSV incomplets.

Effet sur le pack : **142 → 142, delta 0, aucune publication**.
