# Normandie v0.5 — recherche

État : **Sprint 85 / 0.21.74 — candidat interne 142 mémoires RX, delta 0 ; kit terrain et évaluateur R3/F5ZHA prêts, aucune publication**.

Base publique immuable : **Normandie v0.4, 142 mémoires RX**. Le plafond potentiel connu reste **147 mémoires** hors F6ZES.

## Chaîne terrain

1. Générer le kit RX-only et le journal vide :

```bash
python tools/build_normandie_v05_field_validation_kit.py --output-dir field-kit
```

2. Renseigner `field-kit/normandie-v0.5-field-session-template.csv` pendant ou après les écoutes.

3. Évaluer le journal :

```bash
python tools/evaluate_normandie_v05_field_sessions.py --input observations.csv --output evaluation.json
```

Le rapport distingue `satisfied`, `insufficient` et `indeterminate`, compte les sessions indépendantes par `session_id`, signale les lignes invalides et n’effectue jamais de promotion automatique.

## Gates

- **R3 F1ZBX** : 145.675 MHz est la sonde principale ; deux sessions indépendantes identifiées sont nécessaires. 145.075 MHz est facultative.
- **F5ZHA Laval** : deux sessions indépendantes qualifiantes sur 145.4675 ou 432.575 MHz, intelligibilité ≥ 3/5 et confiance reconnue. Les deux côtés de la paire n’ont pas besoin d’être entendus pour le seul gate de couverture terrain.
- **431.4125 MHz** : diagnostic historique uniquement, ne compte jamais pour le gate et ne ferme jamais le conflit de source.
- **CTRL-ZHY 145.6875 MHz** : contrôle facultatif du matériel, ne compte pour aucun gate.

Une non-réception n’est jamais une preuve d’arrêt. Même si un gate terrain est satisfait, `promotion_ready` reste faux : une revue humaine et des sources courantes restent nécessaires.

Fichiers : `field-validation-kit.json`, `field-evaluation-policy.json`, `current-blocker-revalidation.json`.

Règles : RX-only, `Duplex=off`, `Offset=0.000000`, aucune fréquence devinée, géométrie ≠ réception, aucune mutation automatique du candidat, aucune publication automatique, Normandie v0.4 immuable.
