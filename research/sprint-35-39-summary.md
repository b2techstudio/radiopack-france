# RadioPack France — Sprints 35 à 39

Date : **10 août 2026**

Cette passe prolonge les Sprints 30–34 sans modifier aucun pack public. Normandie v0.3.1 reste figée à 139 mémoires ; le candidat interne Normandie v0.4 reste à 142 mémoires et n'est pas une prépublication.

## Sprint 35 — 0.21.24 — validation diagnostique F5ZHA

Ajout de `research/normandie-v0.4/f5zha-mortain-validation.json`.

Le centre du locator REF `IN98OB86BQ` place F5ZHA à environ **65,6 km** de la référence Mortain. Cette valeur sert uniquement à justifier une vérification locale ; elle n'est jamais considérée comme preuve de réception.

Le plan conserve la paire actuelle REF **145.4675 / 432.575 MHz** et la valeur secondaire historique conflictuelle **431.4125 MHz** comme sonde diagnostique uniquement. Le conflit reste ouvert tant qu'il n'est pas fermé par une source actuelle suffisamment autoritative.

## Sprint 36 — 0.21.25 — mini-pack RX-only F5ZHA

Ajout de `tools/build_normandie_v04_f5zha_validation_pack.py`.

Le builder produit un mini-pack local de trois mémoires :

- `ZHA-VHF` — 145.4675 MHz ;
- `ZHA-UHF` — 432.575 MHz ;
- `ZHA-OLD` — 431.4125 MHz, diagnostic historique uniquement.

Toutes les mémoires utilisent `Duplex=off`, `Offset=0.000000`, aucune tonalité RX filtrante et aucun TX. Le pack reste dans `research/normandie-v0.4/generated/`, ignoré par Git et hors publication.

## Sprint 37 — 0.21.26 — readiness report Normandie v0.4

Ajout de `tools/build_normandie_v04_readiness_report.py`.

Le rapport agrège le candidat interne, les portes, les revalidations externes, R3 et F5ZHA. Il distingue :

- le candidat actuel : **142 mémoires** ;
- les **5 fréquences** encore bloquées par les trois portes connues ;
- le plafond interne connu de **147 mémoires** si ces trois portes sont toutes réellement levées ;
- F6ZES comme priorité non chiffrable tant qu'aucune fréquence n'est résolue ;
- la taille publique finale, qui reste volontairement `null`.

Une levée de porte ne devient jamais une publication automatique.

## Sprint 38 — 0.21.27 — matrice des scénarios de promotion

Ajout de `tools/build_normandie_v04_promotion_scenarios.py`.

Les trois portes connues donnent **8 combinaisons** possibles :

- R3 : +2 mémoires ;
- F5ZHA : +2 mémoires ;
- F1ZOV : +1 mémoire.

La plage interne connue va donc de **142 à 147 mémoires**. Chaque scénario reste non public, nécessite une revue finale explicite et exclut F6ZES jusqu'à résolution de sa fréquence.

## Sprint 39 — 0.21.28 — tests, CI et reprise

Ajout de `tests/test_normandie_v04_readiness.py` et de l'étape CI correspondante.

Le runner local `tools/run_normandie_v04_checks.py` inclut désormais le test readiness. `pack-plan.json`, `PROJECT_STATUS.md` et `research/project-resume-state.json` sont synchronisés sur le Sprint 39 / état 0.21.28.

La CI vérifie notamment :

- le mini-pack F5ZHA RX-only ;
- l'absence de fermeture automatique du conflit ;
- le candidat interne à 142 mémoires ;
- le plafond connu à 147 mémoires ;
- les huit scénarios non publics ;
- l'absence de Normandie v0.4 dans le registre public et les téléchargements publics.

## État à la fin de la passe

- Normandie v0.3.1 publique : **139 mémoires**, inchangée ;
- Normandie v0.4 candidat interne : **142 mémoires**, inchangé ;
- plafond interne connu après les trois portes actuelles : **147 mémoires** ;
- taille publique finale : **non définie** ;
- R3 : validation terrain Mortain toujours requise ;
- F5ZHA : diagnostic RX possible, conflit source toujours ouvert ;
- F1ZOV : maintenance toujours bloquante ;
- F6ZES : fréquence toujours non résolue et hors plafond connu ;
- publication Normandie v0.4 : **interdite**.
