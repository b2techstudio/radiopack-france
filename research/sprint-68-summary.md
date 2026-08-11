# Sprint 68 — clôture de périmètre Normandie v0.4

Date : 11 août 2026
État logique : `0.21.57`

## Décision

Normandie v0.4 est figée à **142 mémoires RX**. Les trois ajouts déjà suffisamment étayés restent :

- `50-ZHY-IN` — 145.0875 MHz ;
- `53-ZCE-IN` — 145.1000 MHz ;
- `50-ZBL-U` — 431.2500 MHz.

Les dossiers R3/F1ZBX, F5ZHA, F1ZOV et F6ZES sont explicitement **reportés à Normandie v0.5**. Ce report ne vaut ni validation ni preuve d'activité ; il signifie seulement qu'ils ne font pas partie du périmètre v0.4.

## Résultat de revue

- taille finale : **142** ;
- checklist : **9/9** ;
- blocages de prépublication : **0** ;
- audit d'intégrité : **OK** ;
- baseline de revue SHA-256 : capturée dans `research/normandie-v0.4/review-baseline.json` ;
- dry-run : **activation_ready=true** avec baseline propre ;
- aucun CSV public v0.4 ni registre public n'est encore modifié dans ce sprint.

## Règle de version

Une donnée non suffisamment prouvée ne doit plus immobiliser une version entière lorsqu'elle est hors candidat. Elle est reportée vers une version ultérieure, sans être inventée, supprimée de la recherche ni considérée comme validée.
