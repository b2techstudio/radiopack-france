# RadioPack France — Sprints 50 à 54

Date : **10 août 2026**

Cette passe prépare la revue prépublication de Normandie v0.4 sans modifier aucun pack public. Normandie v0.3.1 reste figée à 139 mémoires et le candidat interne v0.4 reste à 142 mémoires.

## Sprint 50 — 0.21.39 — fraîcheur des sources

- Ajout de `research/normandie-v0.4/source-freshness-policy.json`.
- Ajout de `tools/check_normandie_v04_source_freshness.py`.
- Fenêtre interne courte pour les états opérateur, plus large pour les répertoires techniques et les preuves terrain.
- Une source périmée bloque la revue mais ne devient jamais une preuve d'arrêt ou d'absence.

## Sprint 51 — 0.21.40 — checklist de revue

- Ajout de `tools/build_normandie_v04_review_checklist.py`.
- Neuf points de revue : cohérence, fraîcheur, R3, F5ZHA, F1ZOV, F6ZES, plan mémoire final, revue finale et registre public.
- État actuel : **2/9 complétés**, uniquement cohérence et fraîcheur ; **7 blocages ouverts**.

## Sprint 52 — 0.21.41 — diff structurel candidat

- Ajout de `tools/build_normandie_v04_candidate_diff.py`.
- Vérification de l'empilement exact base publique → candidat interne → preview gardé.
- État actuel : **139 → 142 → 142**, trois ajouts internes existants et zéro ajout futur actuellement éligible.
- Contrôle RX-only sur tous les ajouts et interdiction de réécrire le préfixe publié.

## Sprint 53 — 0.21.42 — audit prépublication

- Ajout de `tools/run_normandie_v04_prepublication_audit.py`.
- Agrégation cohérence des sources, fraîcheur, checklist, diff candidat et manifeste de blocages.
- Distinction explicite entre `integrity_ok` et `release_ready`.
- État actuel : **integrity_ok=true**, **release_ready=false**.

## Sprint 54 — 0.21.43 — tests, CI et reprise

- Ajout de `tests/test_normandie_v04_prepublication_audit.py`.
- Test d'un état courant frais et d'un état futur volontairement périmé.
- Intégration dans `tools/run_normandie_v04_checks.py` et GitHub Actions.
- Mise à jour de `pack-plan.json`, README, `PROJECT_STATUS.md` et `research/project-resume-state.json`.

## Revalidation externe de la passe

- R3/F1ZBX reste publié opérationnel par ARA35 sur 145.075 / 145.675 MHz.
- F1ZOV reste marqué **En Maintenance** par F6KFW ; le statut exploitant local reste prioritaire sur le statut général REF.
- Aucun élément nouveau suffisamment fort ne permet de lever les portes F5ZHA ou F6ZES.

## État fin de passe

- Normandie v0.3.1 publique : **139 mémoires**, inchangée.
- Normandie v0.4 candidat interne : **142 mémoires**, inchangé.
- Preview courant : **142 mémoires**.
- Ajouts futurs actuellement éligibles : **0**.
- Checklist revue : **2/9**.
- Blocages ouverts : **7**.
- Audit prépublication : **intégrité OK**, release non prête.
- Publication v0.4 : **interdite**.
