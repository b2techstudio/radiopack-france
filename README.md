# RadioPack France

**Couverture publique au 19 août 2026 : les 13 régions administratives de France métropolitaine disposent désormais d'un pack RadioPack France. Le catalogue compte 14 packs publics avec Annecy–Alpes–Léman comme pack territorial spécialisé supplémentaire. Toutes les mémoires distribuées restent en réception seule.**

**État courant : Sprint 97 / 0.21.86 — socle officiel conservé ; publication post-Sprint 97 des onze packs régionaux désormais enrichis en v0.2, avec couverture métropolitaine 13/13.**

RadioPack France fournit des codeplugs CSV CHIRP régionaux documentés à partir de données publiques vérifiables pour les radios Quansheng UV-K5. Le projet privilégie une donnée recoupée et bornée plutôt qu'un remplissage artificiel des 200 mémoires.

## Couverture métropolitaine complète — 19 août 2026

La couverture administrative métropolitaine est **13/13**. Normandie et Bretagne conservent leurs versions publiques matures ; les onze autres régions disposent maintenant d'une **v0.2 enrichie**, tandis que leur v0.1 reste historique et immuable. Annecy–Alpes–Léman reste un pack territorial spécialisé en complément.

Packs publics actuels :

- **Normandie v0.4** — 142 mémoires RX ;
- **Bretagne v0.2** — 151 mémoires RX ;
- **Hauts-de-France v0.2** — 144 mémoires RX ;
- **Île-de-France v0.2** — 58 mémoires RX ;
- **Grand Est v0.2** — 59 mémoires RX ;
- **Centre-Val de Loire v0.2** — 42 mémoires RX ;
- **Pays de la Loire v0.2** — 130 mémoires RX ;
- **Bourgogne-Franche-Comté v0.2** — 37 mémoires RX ;
- **Nouvelle-Aquitaine v0.2** — 151 mémoires RX ;
- **Auvergne-Rhône-Alpes v0.2** — 62 mémoires RX ;
- **Occitanie v0.2** — 156 mémoires RX ;
- **Provence-Alpes-Côte d’Azur v0.2** — 159 mémoires RX ;
- **Corse v0.2** — 137 mémoires RX ;
- **Annecy–Alpes–Léman v0.4** — 77 mémoires RX, variante 60 sans aviation.

Les variantes par défaut représentent **1505 mémoires RX cumulées** dans le catalogue public. Ce total est un indicateur de catalogue : chaque fichier reste indépendant et respecte la limite de la radio.

### Périmètre des onze v0.2 enrichies

Chaque pack v0.2 conserve le socle PMR446, appels radioamateur et APRS/ISS, puis ajoute une sélection aviation AM revue sur les pages publiques SIA eAIP AD 2.18 dans le contexte AIRAC 08/26 et une sélection régionale de relais FM 2 m en paired RX. Les six régions littorales concernées intègrent également le module national VHF marine de 90 mémoires.

Les v0.1 restent générables à leurs URL historiques et ne sont jamais réécrites. UHF, numérique et réseaux privés/PPDR restent hors publication tant qu'une revue dédiée ne justifie pas leur présence. Le but est d'enrichir utilement les packs, pas de remplir artificiellement les 200 mémoires.

La synthèse de l'enrichissement est `research/metropolitan-regions-v0.2-enrichment.md`. Chaque région dispose d'un dossier `research/<region>-v0.2/` avec un `README.md` et un `pack-plan.json` traçant blocs, sources, exclusions et compteurs.

## Contrat RX-only et paired RX

Règles permanentes :

- RX uniquement : `Duplex=off`, `Offset=0.000000` ;
- maximum 200 mémoires par CSV ;
- aucun remplissage artificiel ;
- versions publiées immuables ;
- `research/paired-rx-policy.json` : une paire split/duplex vérifiée de deux fréquences distinctes utilise deux mémoires RX ;
- une fréquence, un mode ou une attribution locale non résolus ne sont jamais devinés ;
- les données privées, PPDR, chiffrées ou non publiquement vérifiables restent exclues ;
- la présence d'une fréquence dans un fichier n'accorde jamais un droit d'émission.

Les CSV générés par `website/src/lib/chirpPack.ts` appliquent systématiquement le contrat public RX-only. Les nouvelles routes régionales utilisent le même validateur de noms, emplacements, fréquences, doublons et limite mémoire.

## Sources des nouvelles régions

La sélection FM 2 m des v0.2 a été revue le 19 août 2026 à partir de sources publiques complémentaires :

- plan de bande 144–146 MHz du REF ;
- annuaire France RepeaterBook pour les fréquences et sites actuellement publiés ;
- roster français F5AIB/REF comme seconde vérification des relais et indicatifs ;
- Open Data ANFR comme contexte institutionnel sur les installations radio.

L'aviation est en plus contrôlée sur les pages publiques SIA eAIP AD 2.18 dans le contexte AIRAC 08/26. Le dépôt ne transforme jamais une présence dans un annuaire en garantie absolue de disponibilité terrain ; toute évolution RF nécessite une nouvelle validation.

## Site public

Le site Astro expose désormais le même registre sur toutes les vues principales :

- `/regions` — 14 cartes publiques, dont les 13 régions administratives métropolitaines ;
- `/regions/<slug>` — pages détaillées des onze v0.2 enrichies générées depuis la définition déterministe ;
- `/generateur` — sélection de tous les packs publics ;
- `/telechargements` — tous les CSV régionaux et les modules nationaux ;
- `/versions` — état et nombre de mémoires de chaque version ;
- `/sitemap.xml` — toutes les pages régionales publiées.

Les onze URL CSV v0.2 et leurs URL historiques v0.1 sont générées au build par `website/src/pages/downloads/[slug]/[file].csv.ts`. Les versions historiques Normandie, Bretagne et Annecy restent des artefacts publics immuables.

## Publication post-Sprint 97 — enrichissement métropolitain v0.2

Les onze régions ajoutées lors de la couverture 13/13 ont été enrichies sans réécrire leurs v0.1. Les packs v0.2 combinent désormais aviation SIA, relais FM 2 m paired RX et, pour les régions littorales, VHF marine. Le contrôle SIA final a notamment corrigé les libellés/fichiers Hauts-de-France, Île-de-France et Grand Est avant publication ; la validation de déduplication reste active.

Cette publication reste postérieure au Sprint 97 et ne modifie pas l'état logique officiel **97 / 0.21.86**.

## État actuel — Sprint 97 / 0.21.86

Le **Sprint 97 / 0.21.86** reste le dernier état logique officiel synchronisé dans `PROJECT_STATUS.md`, `CHANGELOG.md` et `research/project-resume-state.json`. La couverture métropolitaine du 19 août 2026 constitue une publication post-Sprint 97 et ne réécrit pas rétrospectivement cet état historique.

Repère historique conservé pour les garde-fous du dépôt : **État actuel — Sprint 39**.

Versions historiques toujours conservées :

- Normandie v0.3.1 — 139 mémoires RX, historique immuable ;
- Annecy–Alpes–Léman v0.3 — 76 / 59, historique immuable ;
- Bretagne v0.1 — 135 mémoires RX, historique immuable.

Recherche active antérieure conservée : Normandie v0.5 reste à **142 RX** avec un plafond potentiel connu de **147 mémoires** hors F6ZES ; Bretagne v0.3 reste à **151 RX** en attente de la revalidation AIRAC 09/26 prévue à partir du 3 septembre 2026.

## Sprint 97 — consolidation de l’état post-Sprint 96

Le Sprint 97 a consolidé les raffinements UX ajoutés après le Sprint 96 : détails de canaux régionaux construits depuis les CSV publics, raccourcis du générateur accessibles au clavier et synchronisation officielle du dépôt sur **97 / 0.21.86**.

Références : `research/sprint-97-summary.md` et `research/sprint-97-post96-ui-state.json`.

## Sprint 91 — Bretagne v0.3 AIRAC09 handoff

Bretagne v0.3 reste à **151 RX**, delta 0, avec revalidation AIRAC 09/26 prévue à partir du 3 septembre 2026 ; aucune anticipation de publication.

## Sprint 90 — Normandie v0.5 source refresh

Normandie v0.5 reste à **142 RX**, delta 0. Les gates terrain/source R3, F5ZHA, F1ZOV et F6ZES restent inchangés.

## Sprint 89 — Annecy v0.4 candidat

Le candidat Annecy–Alpes–Léman v0.4 était figé à **77 RX / 60 sans aviation** avant sa publication ultérieure immuable.

## Repères historiques importants

### Normandie v0.4 / v0.5 — Mortain-Bocage / Sud-Manche

Le suivi historique couvre notamment F5ZHY, F6ZES, F6ZCE, F1ZBX, F5ZHA et F1ZOV. La source de synthèse est `research/normandie-v0.4/mortain-bocage-coverage.json`. Le principe `sourdeval_must_not_be_guessed: true` reste un garde-fou permanent. Les outils `build_normandie_v04_readiness_report.py` et `build_normandie_v04_promotion_scenarios.py` restent disponibles.

Le dossier F5ZHA conserve son historique de validation dans `research/normandie-v0.4/f5zha-mortain-validation.json`. Une observation terrain est une preuve de revue, jamais une autorisation automatique de publication.

### Bretagne

La v0.2 publique reste immuable à 151 RX et la v0.1 historique reste conservée. Les principaux dossiers de preuve restent :

- `research/bretagne-v0.1/public-maritime-radio.json` ;
- `research/bretagne-v0.1/publication-record.json` ;
- `research/bretagne-v0.1/release-scope.json` ;
- `research/bretagne-v0.1/review-checklist.json` ;
- `research/sprint-73-summary.md` ;
- `tools/build_bretagne_internal_candidate.py` ;
- `tools/build_bretagne_review_snapshot.py` ;
- `tools/run_bretagne_prepublication_audit.py` ;
- `tests/test_bretagne_internal_candidate.py` ;
- `tests/test_bretagne_prepublication_review.py` ;
- `tests/test_bretagne_public_release.py` ;
- `tests/test_sprint73_bretagne_publication.py` ;
- `website/src/pages/regions/bretagne.astro` ;
- `website/public/downloads/bretagne/radiopack-france-bretagne-v0.1.csv`.

Ch64 et Ch79 restent historiquement traités comme paires RX génériques lorsque l'attribution locale n'est pas prouvée ; une attribution future ne doit pas dupliquer une RF déjà présente.

### Annecy–Alpes–Léman

La v0.4 publique reste immuable à 77 RX / 60 sans aviation. Les travaux paired RX et la publication des versions v0.3/v0.4 restent documentés sous `research/annecy-alpes-leman-v0.3/` et `research/annecy-alpes-leman-v0.4/`.

## Workflow régional

Le processus est décrit dans `REGIONAL-PACK-WORKFLOW.md` :

1. collecter uniquement des sources publiques ;
2. enregistrer preuves, conflits et exclusions ;
3. ne promouvoir que les données qui franchissent les gates de revue ;
4. construire le pack de façon déterministe ;
5. valider RX-only, taille, noms et déduplication ;
6. publier sous une nouvelle version immuable ;
7. mettre à jour registre, site, tests et documentation.

Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint.

## Tests principaux

```powershell
python tests\test_paired_rx_policy.py
python tests\test_mortain_bretagne_radio_research.py
python tests\test_normandie_v04_readiness.py
python tests\test_bretagne_v02_public_release.py
python tests\test_site_files.py
python tests\test_pack_registry.py
python tests\test_web_generator.py
python tests\test_sprint97_state_sync.py

cd website
npm ci
npm run build
cd ..
```

Le build Astro génère aussi les onze nouveaux CSV métropolitains et les tests du catalogue construit vérifient les artefacts publics.

## Synchronisation locale

```powershell
cd "C:\Users\cross\Documents\CODE\PROJETS\RadioPack-France"
git pull --ff-only

python tests\test_site_files.py
python tests\test_pack_registry.py
python tests\test_web_generator.py
python tests\test_sprint97_state_sync.py

cd website
npm ci
npm run build
cd ..

git status
```

Résultat attendu : `nothing to commit, working tree clean`.

Les exports RadioPack sont destinés à l'écoute ; voir `NOTICE_LEGAL.md`.
