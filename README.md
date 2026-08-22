# RadioPack France

**Couverture publique au 22 août 2026 : les 13 régions administratives de France métropolitaine disposent d'un pack RadioPack France. Le catalogue compte 14 packs publics avec Annecy–Alpes–Léman comme pack territorial spécialisé supplémentaire. Toutes les mémoires distribuées restent en réception seule.**

**État courant : Sprint 107 / 0.21.95 — Bourgogne-Franche-Comté v0.4 est publiée et immuable à 61 RX, dont 14 aviation et 7 VHF de navigation intérieure.**

RadioPack France fournit des codeplugs CSV CHIRP régionaux documentés à partir de données publiques vérifiables pour les radios Quansheng UV-K5. Le projet privilégie une donnée recoupée et bornée plutôt qu'un remplissage artificiel des 200 mémoires.

## Couverture métropolitaine complète

La couverture administrative métropolitaine est **13/13**. Les packs publics actuels sont :

- **Normandie v0.4** — 142 mémoires RX ;
- **Bretagne v0.2** — 151 mémoires RX ;
- **Hauts-de-France v0.2** — 144 mémoires RX ;
- **Île-de-France v0.4** — 64 mémoires RX, dont 18 aviation et 7 VHF navigation intérieure ;
- **Grand Est v0.4** — 97 mémoires RX, dont 19 aviation et 13 VHF navigation intérieure ;
- **Centre-Val de Loire v0.3** — 51 mémoires RX, dont 7 aviation ;
- **Pays de la Loire v0.2** — 130 mémoires RX ;
- **Bourgogne-Franche-Comté v0.4** — 61 mémoires RX, dont 14 aviation et 7 VHF navigation intérieure ;
- **Nouvelle-Aquitaine v0.2** — 151 mémoires RX ;
- **Auvergne-Rhône-Alpes v0.2** — 62 mémoires RX ;
- **Occitanie v0.2** — 156 mémoires RX ;
- **Provence-Alpes-Côte d’Azur v0.2** — 159 mémoires RX ;
- **Corse v0.2** — 137 mémoires RX ;
- **Annecy–Alpes–Léman v0.4** — 77 mémoires RX, variante 60 sans aviation.

Les variantes par défaut représentent **1582 mémoires RX cumulées** dans le catalogue public. Chaque fichier reste indépendant et respecte la limite de la radio.

Les versions précédentes publiées restent historiques et immuables, notamment Île-de-France v0.3/v0.2, Grand Est v0.3/v0.2 et Bourgogne-Franche-Comté v0.3/v0.2.

## Contrat RX-only et paired RX

Règles permanentes :

- RX uniquement : `Duplex=off`, `Offset=0.000000` ;
- maximum 200 mémoires par CSV ;
- aucun remplissage artificiel ;
- versions publiées immuables ;
- `research/paired-rx-policy.json` : une paire split/duplex vérifiée de deux fréquences distinctes utilise deux mémoires RX ;
- une fréquence, un mode ou une attribution locale non résolus ne sont jamais devinés ;
- les données privées, PPDR, chiffrées ou non publiquement vérifiables restent exclues ;
- une fréquence présente dans un fichier n'accorde jamais un droit d'émission.

Les CSV générés par `website/src/lib/chirpPack.ts` appliquent ce contrat, ainsi que la validation des noms, emplacements, doublons RF et limite mémoire.

## Sprint 107 — Bourgogne-Franche-Comté v0.4 publiée

Bourgogne-Franche-Comté v0.4 est publiée à **61 RX** à partir de la v0.3 immuable de 54 RX. Le delta contient **7 mémoires VHF de navigation intérieure** sur les emplacements 120–126 : voies 10, 12 et 69 en simplex, voies 20 et 22 en paired RX.

Le canal 18 n'est pas ajouté à BFC : l'affectation documentée concerne la traversée de Lyon et relève du scope Auvergne-Rhône-Alpes. Les **14 mémoires aviation** sont héritées sans modification de v0.3.

SHA public et candidat : `02dcba7e14a0cce331b63126ea4e552d41013ebd51aecec19907009f40236a72`. La CI de publication a prouvé l'identité byte-à-byte entre le candidat figé et la route Astro publique v0.4. La v0.3 de 54 RX reste historique et immuable.

AIRAC 08/26 reste applicable jusqu'au **2 septembre 2026 inclus** ; toute nouvelle révision aviation à partir du **3 septembre 2026** exige AIRAC 09/26.

Références : `research/bourgogne-franche-comte-v0.4/publication-record.json` et `research/sprint-107-summary.md`.

## Sprint 106 — candidat BFC v0.4 figé

Le Sprint 106 a fermé le scope VHF navigation intérieure BFC à **+7 RF**, construit un candidat déterministe de **61 RX**, puis figé son SHA avant toute mutation publique. La promotion du Sprint 107 a réutilisé exactement ces octets.

## Sprint 105 — Île-de-France v0.4 publiée

Île-de-France v0.4 est publiée à **64 RX** à partir de la v0.3 immuable de 57 RX. Le delta est exclusivement constitué de **7 mémoires VHF de navigation intérieure** : canal 10 en simplex et canaux 18, 20 et 22 en paired RX. Aviation : **18, delta 0** ; radio régionale : **15, delta 0**.

SHA public : `14e1d1d95b38ef44d01b9cccb989a3f1567153ac64875594cc24bd4b57a1cdc2`.

## Sprint 104 — Grand Est v0.4 publiée

Grand Est v0.4 est publiée à **97 RX** : 84 mémoires héritées byte-identiques de v0.3 et **13 mémoires VHF de navigation intérieure** validées. Aviation : **19, delta 0** ; radio régionale : **41, delta 0**. SHA public : `ba34604b11b75ae7f0e7aa17e3734053ff37bbe7910218af1ab66e59f3428a5d`.

## Sprint 103 — audit VHF navigation intérieure

L'audit national distingue VHF maritime et VHF de navigation intérieure. Les packs côtiers ne dupliquent pas les RF déjà présentes ; la file non côtière vérifiée était Grand Est, Île-de-France, Bourgogne-Franche-Comté puis **Auvergne-Rhône-Alpes**, désormais prochaine priorité.

## Sprint 102 — Grand Est v0.3 publiée

Grand Est v0.3 a été publiée à **84 RX / 19 aviation / 41 radio régionales**, SHA `45aef8547a701e7541e620fa9a2d8394595576921e793b75238146ff6e42e720`. Elle est historique et immuable depuis la publication v0.4.

## Sprint 101 — Île-de-France v0.3 publiée

Île-de-France v0.3 est publiée et figée à **57 RX / 18 aviation / 15 radio régionales**. SHA public : `e04e6dbbf869661305068bac55cd8044abdcea7321d67e4c28111c9d057da125`. La v0.2 de 58 RX reste historique et immuable.

## Sprint 100 — Centre-Val de Loire v0.3

Centre-Val de Loire v0.3 est publiée à **51 RX**, dont **7 mémoires aviation**, avec SHA public `0882c84133576fae7f6b3cba64efc32e915355c254e533ed9850eb0edf2ebaae`.

## Sprint 99 — Bourgogne-Franche-Comté v0.3

Bourgogne-Franche-Comté v0.3 est publiée à **54 RX**, dont **14 aviation**, SHA `b5af25a6766b1181e735d376d3f70ab47ffb9ed67b9e38e35bee15e8a86ae7a5`. Elle reste historique et immuable après v0.4.

## Sprint 98 — consolidation des onze v0.2

Le Sprint 98 / 0.21.87 a consolidé les onze packs métropolitains v0.2 avec scopes figés, checklists, gates, publication records et SHA-256 issus d'un build Astro frais.

## Sprint 97 — consolidation de l’état post-Sprint 96

Le Sprint 97 / 0.21.86 a consolidé les détails de canaux régionaux, les raccourcis du générateur accessibles au clavier et la synchronisation du registre public, sans mutation RF.

## Travaux encore ouverts

- **Auvergne-Rhône-Alpes v0.3** : prochaine priorité ; audit Sprint 103 avec au moins **+9 RF VHF navigation intérieure** à préparer sur Rhône/Saône.
- **Bretagne v0.3** : 151 RX, delta 0, publication bloquée jusqu'à la revalidation AIRAC 09/26 à partir du **3 septembre 2026**.
- **Normandie v0.5** : 142 RX, delta 0, toujours dépendante des gates terrain/source historiques.

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
python tests\test_bfc_v03_prepublication.py
python tests\test_bfc_v04_candidate.py --dist website\dist
python tests\test_sprint105_state_sync.py

cd website
npm ci
npm run build
cd ..
```

Les exports RadioPack sont destinés à l'écoute ; voir `NOTICE_LEGAL.md`.
