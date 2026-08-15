# Normandie v0.5 — recherche

État : **Sprint 84 / 0.21.73 — candidat interne 142 mémoires RX, delta 0 ; kit terrain R3/F5ZHA prêt sans publication**.

Base publique immuable : **Normandie v0.4, 142 mémoires RX**. Le plafond potentiel connu reste **147 mémoires** hors F6ZES.

## Sprint 84 — kit terrain R3 / F5ZHA

Le fichier `field-validation-kit.json` regroupe six sondes RX-only et les gates associés. Le builder `tools/build_normandie_v05_field_validation_kit.py` génère un CSV CHIRP de diagnostic, un journal de sessions vide et un manifeste machine.

Ce kit ne modifie pas le candidat : **142 → 142, delta 0**. Les sessions terrain sont des preuves, jamais des mémoires supplémentaires.

## Sprint 83 — revalidation actuelle

- R3 F1ZBX : `145.075 / 145.675 MHz`, opérationnel chez l’ARA35, mais deux sessions RX indépendantes depuis Mortain restent requises ;
- F5ZHA Laval : paire REF actuelle `145.4675 / 432.575 MHz`; conflit secondaire RepeaterBook `431.4125 MHz` daté 2017 ; couverture Mortain non validée ;
- F1ZOV : toujours en maintenance selon F6KFW, malgré REF actif ;
- F6ZES : Sourdeval confirmé sans fréquence, mode ni état opérationnel exploitables.

Aucun de ces dossiers n’est promu : **142 → 142, delta 0**.

Le builder `tools/build_normandie_v05_internal_candidate.py` vérifie le record de publication v0.4, son SHA-256, le contrat RX-only et l’unicité des positions, noms et RF, puis reproduit exactement le CSV v0.4 comme candidat interne v0.5.

Preuve : `current-blocker-revalidation.json`.

Règles : RX-only, `Duplex=off`, `Offset=0.000000`, pas de fréquence devinée, deux mémoires RX pour une paire distincte vérifiée, géométrie ≠ preuve de réception, et un gate terrain ne peut pas être satisfait par une recherche web.
