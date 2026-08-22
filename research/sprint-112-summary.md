# Sprint 112 — Normandie v0.5 : couverture théorique

Date : **22 août 2026**

## Décision

Le projet abandonne le caractère bloquant des écoutes terrain pour les décisions de couverture Normandie v0.5. Une station dont les paramètres et le statut courant sont publiquement vérifiés peut désormais être intégrée sur une **couverture théorique documentée**, à condition que la documentation n'assimile jamais cette théorie à une réception mesurée ou garantie.

## Candidat

- base publique immuable : Normandie v0.4 / **142 RX** ;
- candidat interne v0.5 : **146 RX** ;
- delta : **+4 RX** ;
- publication dans Sprint 112 : **non**.

Promotions :

- R3 / F1ZBX : 145.075 + 145.675 MHz, emplacements 178–179 ;
- F5ZHA Laval : 145.4675 + 432.575 MHz, emplacements 180–181.

Toutes les mémoires restent RX-only avec `Duplex=off` et `Offset=0.000000`.

## Base théorique

Point de référence : Mortain (48.64861, -0.93972), altitude représentative 232 m.

### R3 / F1ZBX

- opérateur ARA35 : relais opérationnel ;
- antenne publiée ~262 m ASL ;
- distance Mortain : ~118.32 km ;
- rayon d'usage publié : 150 km ;
- enveloppe géométrique 4/3 Terre d'extrémité : ~129.44 km ;
- FSPL à 145.675 MHz : ~117.17 dB.

Décision : couverture théoriquement plausible, paire intégrée.

### F5ZHA Laval

- REF : actif, paire analogique transparente 145.4675 / 432.575 MHz ;
- locator IN98OB86BQ, altitude publiée 55 m ;
- distance Mortain : ~65.66 km ;
- enveloppe géométrique 4/3 Terre d'extrémité : ~93.31 km ;
- FSPL : ~112.04 dB à 145.4675 MHz et ~121.51 dB à 432.575 MHz.

Décision : couverture théoriquement plausible, paire intégrée. L'ancienne fréquence secondaire 431.4125 MHz reste exclue.

## Toujours différés

- F1ZOV : opérateur local toujours en maintenance ;
- F6ZES : fréquence/mode toujours non résolus.

La théorie ne contourne ni un statut opérationnel courant défavorable ni l'absence de fréquence publiée.

## Limites

Le modèle est une estimation de plausibilité. Il ne modélise pas complètement relief intermédiaire, clutter, bâtiments, végétation, diagrammes d'antenne, sensibilité du récepteur ou fading. Les essais terrain restent utiles comme retour qualité facultatif, mais ne constituent plus un gate de publication.

## Sources de vérité

- `research/normandie-v0.5/theoretical-coverage-policy.json`
- `research/normandie-v0.5/sprint112-theoretical-coverage.json`
- `research/normandie-v0.5/backlog.json`
- `research/normandie-v0.5/pack-plan.json`
- `tools/build_normandie_v05_internal_candidate.py`
- `tests/test_sprint112_normandie_v05_theoretical.py`
