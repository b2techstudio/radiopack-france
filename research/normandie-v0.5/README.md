# Normandie v0.5 — recherche

État : **Sprint 110 / 0.21.98 — candidat interne 142 mémoires RX, delta 0 ; sources revalidées le 22 août 2026, gates terrain R3/F5ZHA toujours ouverts, aucune publication**.

Base publique immuable : **Normandie v0.4, 142 mémoires RX**. Le plafond potentiel connu reste **147 mémoires hors F6ZES**, mais aucune addition potentielle ne franchit actuellement ses gates.

Source de vérité la plus récente : `sprint110-source-field-refresh.json`.

## État des quatre dossiers

- **R3 / F1ZBX** : la paire publique reste 145.675 / 145.075 MHz. Le web confirme les paramètres du relais mais ne ferme pas le gate territorial : **deux sessions RX indépendantes et identifiées depuis Mortain-Bocage** restent nécessaires sur 145.675 MHz.
- **F5ZHA Laval** : la paire publique actuelle reste **145.4675 / 432.575 MHz**. Deux sessions indépendantes qualifiantes depuis Mortain-Bocage restent requises, avec intelligibilité ≥ 3/5 selon la politique Sprint 85.
- **F1ZOV** : l'opérateur local indique toujours **En Maintenance**. Aucune promotion tant que ce statut courant n'est pas levé.
- **F6ZES Sourdeval** : site et locator connus, mais fréquence et mode publics exploitables toujours non résolus. **Aucune fréquence n'est inférée.**

## Chaîne terrain

Le kit Sprint 84 et l'évaluateur Sprint 85 restent suffisants ; Sprint 110 n'ajoute aucune nouvelle sonde.

1. Générer le mini-pack RX-only et le journal CSV vide :

```bash
python tools/build_normandie_v05_field_validation_kit.py --output-dir field-kit
```

Le builder crée notamment `field-kit/normandie-v0.5-field-session-template.csv` : le dépôt ne conserve volontairement aucun faux journal d'observations prérempli.

2. Renseigner le journal pendant ou après de **vraies écoutes**. Un `session_id` désigne une session indépendante ; les métadonnées date/heure/lieu/récepteur/antenne doivent rester cohérentes pour toutes les lignes d'une même session.

3. Évaluer le journal sans muter le candidat :

```bash
python tools/evaluate_normandie_v05_field_sessions.py \
  --input field-kit/normandie-v0.5-field-session-template.csv \
  --output field-kit/evaluation.json
```

Le rapport distingue `satisfied`, `insufficient` et `indeterminate`, compte les sessions indépendantes, signale les lignes invalides et fixe toujours `promotion_ready=false`, `automatic_candidate_mutation_allowed=false` et `automatic_publication_allowed=false`.

## Gates

- **R3 F1ZBX** : 145.675 MHz est la sonde principale ; deux sessions indépendantes identifiées sont nécessaires. 145.075 MHz est facultative et ne compte pas pour le gate de couverture.
- **F5ZHA Laval** : deux sessions indépendantes qualifiantes sur 145.4675 ou 432.575 MHz, intelligibilité ≥ 3/5 et confiance reconnue. Les deux côtés de la paire n'ont pas besoin d'être entendus pour le seul gate de couverture terrain.
- **431.4125 MHz** : diagnostic historique uniquement ; ne compte jamais pour le gate et ne ferme jamais un conflit de source.
- **CTRL-ZHY 145.6875 MHz** : contrôle facultatif du matériel ; ne compte pour aucun gate.

Une non-réception n'est jamais une preuve d'arrêt. Même si un gate terrain est satisfait, une **revue humaine des sources courantes** reste obligatoire avant toute modification du candidat.

Fichiers de référence : `sprint110-source-field-refresh.json`, `field-validation-kit.json`, `field-evaluation-policy.json`, `current-blocker-revalidation.json` et `backlog.json`.

Règles permanentes : RX-only, `Duplex=off`, `Offset=0.000000`, aucune fréquence devinée, géométrie ≠ réception, sessions terrain = preuves et non mémoires, aucune mutation automatique du candidat, aucune publication automatique, Normandie v0.4 immuable.
