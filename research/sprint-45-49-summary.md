# RadioPack France — Sprints 45 à 49

Date : **10 août 2026**

Cette passe renforce la chaîne de décision Normandie v0.4 sans modifier aucun pack public. Normandie v0.3.1 reste figée à 139 mémoires et le candidat interne v0.4 reste à 142 mémoires.

## Sprint 45 — 0.21.34 — cohérence des sources

- Ajout de `research/normandie-v0.4/source-consistency-contract.json`.
- Ajout de `tools/check_normandie_v04_source_consistency.py`.
- Le contrôle compare portes de promotion, revalidation externe et matrice de preuves.
- La priorité de l'exploitant local est verrouillée : le statut général REF « actif » de F1ZOV ne peut pas écraser le statut « En Maintenance » publié par F6KFW.

## Sprint 46 — 0.21.35 — dossier de décision interne

- Ajout de `tools/build_normandie_v04_decision_dossier.py`.
- Agrégation de la cohérence des sources, du rapport de preuves, du readiness et du plan de promotion.
- Toutes les décisions restent non publiques et exigent une revue explicite.

## Sprint 47 — 0.21.36 — preview candidat gardé

- Ajout de `tools/build_normandie_v04_candidate_preview.py`.
- Preview CSV/JSON à blanc, RX-only, sans mutation du candidat.
- Vérification des collisions de location, nom et fréquence.
- Au statut actuel : 0 ajout éligible et preview identique au candidat 142 mémoires.

## Sprint 48 — 0.21.37 — manifeste des blocages de publication

- Ajout de `tools/build_normandie_v04_release_blockers.py`.
- Les blocages stations sont complétés par la revue finale, le plan mémoire public final et le changement explicite du registre public.
- État actuel : **7 blocages actifs**, publication interdite.

## Sprint 49 — 0.21.38 — tests, CI et documentation

- Ajout de `tests/test_normandie_v04_decision_pipeline.py`.
- Le test couvre la cohérence des sources, le dossier de décision, le preview courant 142 et un preview synthétique 144 RX-only.
- Intégration dans `tools/run_normandie_v04_checks.py` et GitHub Actions.
- Mise à jour du `pack-plan.json`, du README, de `PROJECT_STATUS.md` et de l'état machine.

## État fin de passe

- Normandie v0.3.1 publique : **139 mémoires**, inchangée.
- Normandie v0.4 candidat interne : **142 mémoires**, inchangé.
- Ajouts internes actuels : **3**.
- Fréquences bloquées connues : **5**.
- Plan de promotion gardé : **0 ajout éligible**.
- Preview candidat courant : **142 mémoires**.
- Blocages de publication : **7**.
- Plafond connu si les trois portes actuelles passent réellement : **147 mémoires**, non final.
- Publication v0.4 : **interdite**.
