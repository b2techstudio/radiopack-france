# RadioPack France

**Couverture publique au 19 août 2026 : les 13 régions administratives de France métropolitaine disposent désormais d'un pack RadioPack France. Le catalogue compte 14 packs publics avec Annecy–Alpes–Léman comme pack territorial spécialisé supplémentaire. Toutes les mémoires distribuées restent en réception seule.**

**État courant : Sprint 97 / 0.21.86 — socle officiel conservé ; publication post-Sprint 97 de onze packs régionaux v0.1 et mise à jour du site public vers une couverture métropolitaine 13/13.**

RadioPack France fournit des codeplugs CSV CHIRP régionaux documentés à partir de données publiques vérifiables pour les radios Quansheng UV-K5. Le projet privilégie une donnée recoupée et bornée plutôt qu'un remplissage artificiel des 200 mémoires.

## Couverture métropolitaine complète — 19 août 2026

La couverture administrative métropolitaine est maintenant **13/13**. Normandie et Bretagne conservent leurs versions publiques matures ; les onze autres régions démarrent avec une **v0.1 volontairement non exhaustive**. Annecy–Alpes–Léman reste un pack territorial spécialisé en complément.

Packs publics actuels :

- **Normandie v0.4** — 142 mémoires RX ;
- **Bretagne v0.2** — 151 mémoires RX ;
- **Hauts-de-France v0.1** — 36 mémoires RX ;
- **Île-de-France v0.1** — 34 mémoires RX ;
- **Grand Est v0.1** — 36 mémoires RX ;
- **Centre-Val de Loire v0.1** — 32 mémoires RX ;
- **Pays de la Loire v0.1** — 30 mémoires RX ;
- **Bourgogne-Franche-Comté v0.1** — 30 mémoires RX ;
- **Nouvelle-Aquitaine v0.1** — 42 mémoires RX ;
- **Auvergne-Rhône-Alpes v0.1** — 38 mémoires RX ;
- **Occitanie v0.1** — 44 mémoires RX ;
- **Provence-Alpes-Côte d’Azur v0.1** — 42 mémoires RX ;
- **Corse v0.1** — 28 mémoires RX ;
- **Annecy–Alpes–Léman v0.4** — 77 mémoires RX, variante 60 sans aviation.

Les variantes par défaut représentent **762 mémoires RX cumulées** dans le catalogue public. Ce total est un indicateur de catalogue : chaque fichier reste indépendant et respecte la limite de la radio.

### Périmètre des onze nouvelles v0.1

Chaque nouveau socle régional utilise :

- 16 mémoires PMR446 RX ;
- 2 appels radioamateur RX ;
- 6 mémoires APRS / ISS RX ;
- une sélection régionale, publique et recoupée de relais FM 2 m ;
- pour chaque paire split retenue, une mémoire RX de sortie et une mémoire RX d'entrée vérifiée ;
- aucune aviation, aucun UHF/numérique et aucune extension maritime régionale dans cette première v0.1.

La VHF marine reste disponible comme module national séparé. Les extensions futures passent par une nouvelle revue et une nouvelle version ; une v0.1 n'est pas présentée comme un inventaire exhaustif de la région.

La synthèse et les sources de cette publication sont documentées dans `research/metropolitan-regions-v0.1-release.md`. La source déterministe des onze nouvelles versions est `website/src/lib/metropolitanPack.ts`, tandis que `website/src/lib/packRegistry.ts` reste la source de vérité du catalogue public.

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

La sélection FM 2 m des nouvelles v0.1 a été revue le 19 août 2026 à partir de sources publiques complémentaires :

- plan de bande 144–146 MHz du REF ;
- annuaire France RepeaterBook pour les fréquences et sites actuellement publiés ;
- roster français F5AIB/REF comme seconde vérification des relais et indicatifs ;
- Open Data ANFR comme contexte institutionnel sur les installations radio.

Le dépôt ne transforme pas une présence dans un annuaire en garantie absolue de disponibilité terrain. Les v0.1 restent des bases d'écoute publiques et traçables ; les évolutions nécessitent une nouvelle validation.

## Site public

Le site Astro expose désormais le même registre sur toutes les vues principales :

- `/regions` — 14 cartes publiques, dont les 13 régions administratives métropolitaines ;
- `/regions/<slug>` — pages détaillées des onze nouvelles v0.1 générées depuis la définition déterministe ;
- `/generateur` — sélection de tous les packs publics ;
- `/telechargements` — tous les CSV régionaux et les modules nationaux ;
- `/versions` — état et nombre de mémoires de chaque version ;
- `/sitemap.xml` — toutes les pages régionales publiées.

Les onze nouvelles URL CSV sont générées au build par `website/src/pages/downloads/[slug]/[file].csv.ts`. Les versions historiques Normandie, Bretagne et Annecy restent des artefacts publics immuables.

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
