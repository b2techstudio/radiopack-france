# Grand Est v0.3 — Sprint 102

Statut : **publié — immuable**.

Publication : **84 mémoires RX**, dont **19 aviation** et **41 radio régionales**.
SHA-256 candidat/public : `45aef8547a701e7541e620fa9a2d8394595576921e793b75238146ff6e42e720`.

Base historique conservée : **Grand Est v0.2 / 59 RX**, SHA-256 `a50416bd8a88af249bb691daa657ffd4b578daf1324bd0ca4dd632a2f1a0e5c1`.

## Radio régionale

Le périmètre analogique non exhaustif a été fermé après trois passes de recherche à **41 fréquences RF uniques**. `432.5375 MHz`, utilisée par plusieurs infrastructures crossband, est dédupliquée en une seule mémoire.

Les dossiers ambigus ou insuffisamment corroborés n'ont pas été forcés : F1ZAX, F5ZBD, F5ZRP, F5ZTY, F5ZUK, F1ZFN et F1ZEF restent différés/exclus selon leur état ; F1ZBU reste hors scope analogique car son service courant est numérique.

## Aviation

La v0.3 reprend exactement les **19 mémoires aviation** déjà publiées en v0.2 sous le même cycle AIRAC 08/26.

Décision de publication :

- 19 avant / 19 après ;
- 0 ajout ;
- 0 retrait ;
- 0 changement de fréquence ;
- sous-ensemble hérité inchangé ;
- aucune nouvelle validation champ-par-champ revendiquée.

AIRAC 08/26 reste applicable jusqu'au **2 septembre 2026 inclus**. Toute nouvelle révision aviation le **3 septembre 2026 ou après** exige AIRAC 09/26.

## Construction et intégrité

Le builder `tools/build_grand_est_v03_candidate.py` reconstruit d'abord la v0.2 et exige son SHA historique exact. Le CSV public v0.3 est byte-identique au candidat canonique.

Règles garanties :

- réception uniquement ;
- `Duplex=off` ;
- `Offset=0.000000` ;
- paired RX pour les paires distinctes vérifiées ;
- déduplication RF ;
- maximum 200 mémoires ;
- pas d'inférence de fréquence/mode/état manquant ;
- pas de données opérationnelles privées / PPDR ;
- versions publiées immuables.

## Artefacts

- `radio-validation-pass1-2026-08-22.json` ;
- `radio-validation-pass2-2026-08-22.json` ;
- `radio-validation-pass3-2026-08-22.json` ;
- `aviation-airac08-publication-2026-08-22.json` ;
- `backlog.json` ;
- `release-scope.json` ;
- `review-checklist.json` ;
- `publication-gates.json` ;
- `publication-record.json` ;
- `generated/release-candidate/` ;
- `tools/build_grand_est_v03_candidate.py` ;
- `tests/test_grand_est_v03_*.py` ;
- `.github/workflows/grand-est-v03-research.yml`.
