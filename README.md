# RadioPack France

**État courant : Sprint 76 / 0.21.65 — Bretagne v0.2 reste à 151 mémoires RX après revalidation radioamateur, delta RF 0.**

Codeplugs CHIRP régionaux documentés et générés à partir de données publiques vérifiables pour les radios Quansheng UV-K5.

## État actuel — Sprint 76 / 0.21.65

Repère historique conservé pour les garde-fous du dépôt : **État actuel — Sprint 39**.

Packs publics immuables :

- **Normandie v0.4** — 142 mémoires RX ;
- Normandie v0.3.1 — 139 mémoires RX, historique immuable ;
- **Annecy–Alpes–Léman v0.2** — 65 mémoires RX, variante 48 sans aviation ;
- **Bretagne v0.1** — 135 mémoires RX, publiée et immuable.

Recherche : Normandie v0.5 reste à 142 mémoires, avec un plafond potentiel connu de **147 mémoires** hors F6ZES. Bretagne v0.2 est à **151 mémoires RX** : base publique v0.1=135 + 16 mémoires aviation AIRAC 08/26. Aucun CSV public Bretagne v0.2 n'existe et le registre public reste sur v0.1.

Point de reprise : `PROJECT_STATUS.md`, `research/project-resume-state.json`, `research/sprint-75-summary.md` et `research/sprint-76-summary.md`.

## Sprint 76 — revalidation radioamateur Bretagne v0.2

Le dossier `research/bretagne-v0.2/amateur-infrastructure-revalidation.json` revalide F5ZPV, F5ZZH, F1ZBZ et F5ZZC-4 sans ajouter de mémoire.

- **F1ZBZ Lorient** : les cinq valeurs RF du système multipath sont déjà toutes représentées dans `research/paired-rx-deduplicated-memory-plan.json`. La revue de direction est donc résolue à **delta 0**.
- **F5ZPV** : conflit de statut entre l'annuaire général et l'ARA35 ; le statut opérateur local reste prioritaire et indique toujours le relais temporairement arrêté. Pas de promotion.
- **F5ZZH** : toujours arrêté et à la recherche d'un nouveau site. Pas de promotion.
- **F5ZZC-4** : rôle APRS/ADRASEC35 conservé comme contexte, mais aucune fréquence actuelle n'est validée. L'entrée distincte F5ZZC analogique ne doit pas être assimilée automatiquement à F5ZZC-4.

Résultat : candidat **151**, delta radioamateur **0**, public inchangé.

Garde-fou : `tests/test_sprint76_bretagne_amateur_revalidation.py`.

## Sprint 75 — aviation Bretagne v0.2

Le candidat interne est passé de 135 à **151 mémoires RX** avec 16 mémoires aviation aux positions 130–145. Les positions 146–149 restent libres : aucun remplissage artificiel.

Le contexte courant est **AIRAC 08/26**, du 6 août au 2 septembre 2026 inclus. La méthode suit le précédent Annecy–Alpes–Léman : produit AIRAC courant vérifié + dernière page AIP primaire publique effective pour le service. Le dépôt ne prétend pas avoir extrait les octets de l'XML courant ni avoir effectué une comparaison champ par champ avec cet XML.

Périmètre : Rennes Saint-Jacques (7 fréquences uniques), Brest Bretagne (5), Dinard Pleurtuit Saint-Malo (2), Quimper Pluguffan (1) et aviation urgence 121.500 MHz (1). Toutes les mémoires sont en AM, **avec un pas de 8,33 kHz**, RX-only.

Fichiers principaux :

```text
research/bretagne-v0.2/aviation-airac-08.json
research/bretagne-v0.2/candidate-memory-delta.json
research/bretagne-v0.2/pack-plan.json
research/bretagne-v0.2/backlog.json
tools/build_bretagne_v02_internal_candidate.py
tests/test_sprint75_bretagne_aviation.py
```

## Bretagne v0.1 — version publique immuable

Bretagne v0.1 reste publiée avec 135 mémoires RX. Le CSV public correspond au candidat revu avant publication et reste immuable.

Sources et garde-fous historiques :

```text
research/bretagne-v0.1/public-maritime-radio.json
research/bretagne-v0.1/publication-record.json
research/bretagne-v0.1/release-scope.json
research/bretagne-v0.1/review-checklist.json
research/sprint-73-summary.md
tools/build_bretagne_internal_candidate.py
tools/build_bretagne_review_snapshot.py
tools/run_bretagne_prepublication_audit.py
tests/test_bretagne_internal_candidate.py
tests/test_bretagne_prepublication_review.py
tests/test_bretagne_public_release.py
tests/test_sprint73_bretagne_publication.py
website/src/pages/regions/bretagne.astro
website/public/downloads/bretagne/radiopack-france-bretagne-v0.1.csv
```

Ch64 et Ch79 restent des paires RX génériques sans attribution locale de site non prouvée. Une future attribution locale ne crée pas de doublon RF.

## Normandie v0.4 / v0.5 — Mortain-Bocage / Sud-Manche

Le périmètre de suivi couvre notamment **F5ZHY**, **F6ZES**, **F6ZCE**, **F1ZBX**, **F5ZHA** et **F1ZOV**.

Source principale : `research/normandie-v0.4/mortain-bocage-coverage.json`.

- R3 / F1ZBX : une paire vérifiée représente 2 mémoires RX ; les sessions terrain sont des preuves, pas des mémoires.
- F5ZHA : conflit documentaire toujours à réconcilier ; protocole `research/normandie-v0.4/f5zha-mortain-validation.json`.
- F1ZOV : statut opérateur local prioritaire.
- F6ZES : fréquence et mode toujours non résolus ; `sourdeval_must_not_be_guessed: true`.

Outils historiques : `build_normandie_v04_readiness_report.py` et `build_normandie_v04_promotion_scenarios.py`.

## Règles permanentes

- RX uniquement : `Duplex=off`, `Offset=0.000000`.
- Pas de remplissage artificiel ; maximum 200 mémoires.
- Versions publiées immuables.
- `research/paired-rx-policy.json` : une paire split/duplex vérifiée de deux fréquences distinctes utilise deux mémoires RX.
- Une fréquence ou un mode non résolu n'est jamais deviné.
- Le statut opérateur local prime sur un annuaire général pour l'état opérationnel courant.
- Une observation terrain ne ferme pas un conflit de source.
- Une infrastructure radio actuelle ne permet pas d'attribuer automatiquement un canal.
- Une source secondaire ne remplace pas une validation primaire lorsqu'elle est exigée.
- Une preuve de rôle ancienne ne valide pas une fréquence actuelle.
- Des indicatifs proches ne prouvent pas qu'il s'agit du même service.
- Une revue de direction ou une métadonnée locale ne crée pas de doublon d'une RF déjà présente.
- Les données privées PPDR restent exclues.
- Une promotion dans un candidat interne n'est jamais une publication.
- Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint.

## Historique utile

- `SPRINT-29-MORTAIN-BRETAGNE-RADIO-RESEARCH.md`
- `research/sprint-30-34-summary.md`
- `research/sprint-35-39-summary.md`
- `research/sprint-55-60-summary.md`
- `research/sprint-61-summary.md` à `research/sprint-76-summary.md`

## Tests principaux

```powershell
python tests\test_paired_rx_policy.py
python tests\test_mortain_bretagne_radio_research.py
python tests\test_normandie_v04_readiness.py
python tests\test_sprint74_bretagne_v02_initialization.py
python tests\test_sprint75_bretagne_aviation.py
python tests\test_sprint76_bretagne_amateur_revalidation.py
python tests\test_bretagne_public_release.py
python tests\test_site_files.py
python tests\test_pack_registry.py
```

## Synchronisation locale

```powershell
cd "C:\Users\cross\Documents\CODE\PROJETS\RadioPack-France"
git pull --ff-only

python tools\build_bretagne_v02_internal_candidate.py
python tests\test_sprint75_bretagne_aviation.py
python tests\test_sprint76_bretagne_amateur_revalidation.py
python tests\test_site_files.py
python tests\test_pack_registry.py

cd website
npm ci
npm run build
cd ..

git status
```

Résultat attendu : `nothing to commit, working tree clean`.

Les exports RadioPack sont destinés à l'écoute ; voir `NOTICE_LEGAL.md`.
