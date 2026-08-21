# RadioPack France

**Couverture publique au 21 août 2026 : les 13 régions administratives de France métropolitaine disposent d'un pack RadioPack France. Le catalogue compte 14 packs publics avec Annecy–Alpes–Léman comme pack territorial spécialisé supplémentaire. Toutes les mémoires distribuées restent en réception seule.**

**État courant : Sprint 100 / 0.21.89 — Bourgogne-Franche-Comté v0.3 et Centre-Val de Loire v0.3 sont publiées et immuables ; les neuf autres régions métropolitaines issues de l'enrichissement restent en v0.2 avant leur future passe v0.3.**

RadioPack France fournit des codeplugs CSV CHIRP régionaux documentés à partir de données publiques vérifiables pour les radios Quansheng UV-K5. Le projet privilégie une donnée recoupée et bornée plutôt qu'un remplissage artificiel des 200 mémoires.

## Couverture métropolitaine complète

La couverture administrative métropolitaine est **13/13**. Les packs publics actuels sont :

- **Normandie v0.4** — 142 mémoires RX ;
- **Bretagne v0.2** — 151 mémoires RX ;
- **Hauts-de-France v0.2** — 144 mémoires RX ;
- **Île-de-France v0.2** — 58 mémoires RX ;
- **Grand Est v0.2** — 59 mémoires RX ;
- **Centre-Val de Loire v0.3** — 51 mémoires RX, dont 7 aviation ;
- **Pays de la Loire v0.2** — 130 mémoires RX ;
- **Bourgogne-Franche-Comté v0.3** — 54 mémoires RX, dont 14 aviation ;
- **Nouvelle-Aquitaine v0.2** — 151 mémoires RX ;
- **Auvergne-Rhône-Alpes v0.2** — 62 mémoires RX ;
- **Occitanie v0.2** — 156 mémoires RX ;
- **Provence-Alpes-Côte d’Azur v0.2** — 159 mémoires RX ;
- **Corse v0.2** — 137 mémoires RX ;
- **Annecy–Alpes–Léman v0.4** — 77 mémoires RX, variante 60 sans aviation.

Les variantes par défaut représentent **1531 mémoires RX cumulées** dans le catalogue public. Chaque fichier reste indépendant et respecte la limite de la radio.

Le projet couvre actuellement les **13 régions métropolitaines**. Les cinq régions d'outre-mer ne sont pas encore incluses dans cette couverture.

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

Les CSV générés par `website/src/lib/chirpPack.ts` appliquent ce contrat, ainsi que la validation des noms, emplacements, doublons RF et limite mémoire.

## Méthode d'enrichissement v0.3

Chaque future v0.3 régionale suit désormais le même processus :

1. partir de la dernière version publique immuable ;
2. revalider les relais et transpondeurs analogiques 2 m / 70 cm / crossband à partir de sources publiques actuelles ;
3. représenter les paires distinctes en paired RX ;
4. revoir systématiquement l'aviation sur les sources SIA/eAIP du cycle AIRAC applicable, avec NOTAM/SUP AIP lorsque nécessaire ;
5. différer les fréquences ambiguës plutôt que les deviner ;
6. construire le CSV de façon déterministe, vérifier RX-only, déduplication et taille ;
7. figer scope, checklist, gates, `publication-record.json` et SHA-256 du build Astro avant publication.

Les régions littorales conservent aussi leur périmètre VHF marine lorsque celui-ci est déjà validé.

## Sprint 100 — Centre-Val de Loire v0.3

Le **Sprint 100 / 0.21.89** publie Centre-Val de Loire v0.3 à **51 RX**. La v0.2 de 42 RX reste historique et immuable.

La version comprend **20 mémoires radioamateur analogiques** sur dix infrastructures et **7 mémoires aviation AM**. La revue aviation corrige Châteauroux-Déols de 125.875 à **125.880 MHz** et ajoute Saint-Denis-de-l'Hôtel **122.405 MHz**. F5ZQY n'est pas reconduit dans la v0.3 ; F5ZNX et les dossiers insuffisamment prouvés restent différés.

SHA-256 public : `0882c84133576fae7f6b3cba64efc32e915355c254e533ed9850eb0edf2ebaae`.

Références : `research/centre-val-de-loire-v0.3/publication-record.json` et `research/sprint-100-summary.md`.

## Sprint 99 — Bourgogne-Franche-Comté v0.3

Le **Sprint 99 / 0.21.88** publie Bourgogne-Franche-Comté v0.3 à **54 RX**. La v0.2 de 37 RX reste historique et immuable.

La v0.3 ajoute dix mémoires radioamateur analogiques validées et porte l'aviation à **14 mémoires**. Les pistes encore insuffisamment corroborées restent différées.

SHA-256 public : `b5af25a6766b1181e735d376d3f70ab47ffb9ed67b9e38e35bee15e8a86ae7a5`.

Références : `research/bourgogne-franche-comte-v0.3/publication-record.json` et `research/sprint-99-summary.md`.

## Sprint 98 — consolidation des onze v0.2

Le Sprint 98 / 0.21.87 a consolidé les onze packs métropolitains v0.2 avec scopes figés, checklists 10/10, gates satisfaits, publication records et SHA-256 issus d'un build Astro frais. Le manifeste commun est `research/sprint-98-metropolitan-publication-manifest.json` et le résumé est `research/sprint-98-summary.md`.

Le Sprint 98 n'a modifié aucune mémoire RF : il a rendu la publication reproductible et verrouillé l'immuabilité des v0.2 et de leurs v0.1 historiques.

## Sprint 97 — consolidation de l’état post-Sprint 96

Le Sprint 97 / 0.21.86 a consolidé les raffinements UX ajoutés après le Sprint 96 : détails de canaux régionaux construits depuis les CSV publics, raccourcis du générateur accessibles au clavier et synchronisation du registre public.

Références : `research/sprint-97-summary.md` et `research/sprint-97-post96-ui-state.json`.

## Travaux encore ouverts

**Bretagne v0.3** reste à 151 RX, delta 0, en attente de la revalidation AIRAC 09/26 à partir du **3 septembre 2026**. **Normandie v0.5** reste à 142 RX, delta 0 ; R3/F1ZBX et F5ZHA nécessitent toujours du terrain, F1ZOV reste sous surveillance d'état opérateur et F6ZES demeure sans fréquence/mode public suffisamment établi.

Après BFC et Centre, les neuf régions métropolitaines encore en v0.2 seront traitées une par une, en commençant par **Île-de-France**.

## Site public

Le site Astro expose un registre commun sur les vues principales :

- `/regions` — 14 cartes publiques, dont les 13 régions administratives métropolitaines ;
- `/regions/<slug>` — détail de chaque pack ;
- `/generateur` — sélection des packs publics ;
- `/telechargements` — CSV régionaux et modules nationaux ;
- `/versions` — versions et compteurs ;
- `/sitemap.xml` — pages régionales publiées.

Les versions historiques restent disponibles sous leurs URLs immuables lorsqu'elles font partie du contrat de publication.

## Workflow régional

Le processus détaillé est décrit dans `REGIONAL-PACK-WORKFLOW.md` : collecter uniquement des sources publiques, enregistrer preuves/conflits/exclusions, ne promouvoir que les données franchissant les gates de revue, construire de façon déterministe, tester, puis publier une nouvelle version immuable.

Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint.

## Tests principaux

```powershell
python tests\test_site_files.py
python tests\test_pack_registry.py
python tests\test_web_generator.py
python tests\test_sprint97_state_sync.py
python tests\test_sprint98_state_sync.py
python tests\test_sprint100_state_sync.py

cd website
npm ci
npm run build
cd ..
```

Les exports RadioPack sont destinés à l'écoute ; voir `NOTICE_LEGAL.md`.
