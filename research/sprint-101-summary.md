# Sprint 101 — Île-de-France v0.3 publiée

État logique : **0.21.90**
Publication finalisée : **22 août 2026**

Le Sprint 101 publie **Île-de-France v0.3 à 57 mémoires RX** à partir de la **v0.2 historique immuable de 58 RX**.

## Composition publiée

- **24 mémoires nationales** ;
- **18 mémoires aviation** ;
- **15 mémoires radio régionales** ;
- total : **57 RX**.

SHA-256 public et candidat :

`e04e6dbbf869661305068bac55cd8044abdcea7321d67e4c28111c9d057da125`

Le CSV public réutilise exactement le blob Git du candidat déterministe ; les guards vérifient également l'identité byte-à-byte, le SHA, les 57 fréquences uniques, RX-only et la limite mémoire.

## Radioamateur

Le scope final retient F5ZNG, F5ZNN, F5ZMH, F1ZHK, F6ZEE, F5ZMR, F5ZSY et l'extension crossband F5ZNN après déduplication. Le bloc régional contient **15 RF uniques**.

F5ZEQ reste non reconduit pendant sa maintenance. F1ZTC, F5ZDR, F5ZBK et F1ZDL restent hors scope faute de corroboration actuelle suffisante, sans affirmation de fermeture définitive.

## Aviation

Le sous-ensemble publié reste à **18 mémoires, delta 0**, sans expansion. LFPG, LFPO et LFPB ont été revalidés pour cette sélection dans la fenêtre AIRAC **08/26** avec les éléments SIA/NOTAM/SUP documentés.

La photographie publiée reste valable jusqu'au **2 septembre 2026 inclus**. Toute nouvelle révision aviation à partir du **3 septembre 2026** doit être revalidée sur **AIRAC 09/26**.

## Publication

- checklist : **12/12** ;
- blockers : **0** ;
- publication record : **`published_immutable`** ;
- registre public : **v0.3 / 57 RX** ;
- CSV public : créé ;
- v0.2 : conservée historique et immuable ;
- v0.3 : publiée et immuable.

Références principales :

- `research/ile-de-france-v0.3/publication-record.json` ;
- `research/ile-de-france-v0.3/publication-gates.json` ;
- `research/ile-de-france-v0.3/review-checklist.json` ;
- `research/ile-de-france-v0.3/release-scope.json` ;
- `research/ile-de-france-v0.3/aviation-validation-pass4-2026-08-21.json` ;
- `research/ile-de-france-v0.3/radio-validation-pass3-2026-08-21.json` ;
- `tests/test_idf_v03_publication.py` ;
- `tests/test_sprint101_state_sync.py`.
