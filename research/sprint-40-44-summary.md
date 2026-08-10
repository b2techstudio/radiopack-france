# RadioPack France — Sprints 40 à 44

Date : **10 août 2026**

Cette passe prolonge Normandie v0.4 sans modifier aucun pack public. Normandie v0.3.1 reste figée à 139 mémoires et le candidat interne v0.4 reste à 142 mémoires.

## Sprint 40 — 0.21.29 — observations terrain F5ZHA

- Passage de `f5zha-mortain-validation.json` au schéma 1.1.
- Ajout d'un journal `observations` et de critères explicites d'intelligibilité / identification.
- Ajout de `tools/record_normandie_v04_f5zha_observation.py`.
- Une observation terrain peut documenter la couverture utile mais ne peut jamais fermer le conflit de source.

## Sprint 41 — 0.21.30 — matrice de preuves externes

Ajout de `research/normandie-v0.4/external-evidence-matrix.json` pour séparer :

- paramètres techniques ;
- état opérateur ;
- réception terrain ;
- conflit de source ;
- autorisation de promotion.

Revalidation courante : R3 opérationnel chez ARA35, F5ZHA actif dans le REF sur 145.4675/432.575 MHz, F1ZOV toujours marqué En Maintenance par F6KFW, F6ZES toujours sans fréquence/mode exploitable dans le REF.

## Sprint 42 — 0.21.31 — rapport de preuves consolidé

Ajout de `tools/build_normandie_v04_evidence_report.py`.

Le rapport combine les observations R3/F5ZHA et la matrice externe sans modifier `promotion-gates.json`.

## Sprint 43 — 0.21.32 — plan de promotion interne gardé

Ajout de `tools/build_normandie_v04_internal_promotion_plan.py`.

Le plan :

- lit l'état réel des portes ;
- ne propose que les fréquences d'une porte réellement franchie ;
- attribue seulement des positions internes prospectives ;
- ne modifie jamais le candidat interne ;
- ne publie rien.

À l'état courant : **0 ajout éligible**, candidat futur inchangé à **142 mémoires**.

## Sprint 44 — 0.21.33 — tests, CI et documentation

- Ajout de `tests/test_normandie_v04_evidence_pipeline.py`.
- Intégration du test dans `tools/run_normandie_v04_checks.py` et GitHub Actions.
- Mise à jour du `pack-plan.json`, README et des points de reprise.
- Le plafond connu reste 147 uniquement si les trois portes actuelles sont réellement levées ; F6ZES reste hors calcul tant que sa fréquence est inconnue.

## État fin de passe

- Normandie v0.3.1 publique : **139 mémoires**, inchangée.
- Normandie v0.4 candidat interne : **142 mémoires**, inchangé.
- Ajouts internes actuels : **3**.
- Fréquences encore bloquées : **5**.
- Plan de promotion gardé : **0 ajout éligible**.
- Publication v0.4 : **interdite**.
