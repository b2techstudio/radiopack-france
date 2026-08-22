# RadioPack France

**Couverture publique au 22 août 2026 : les 13 régions administratives de France métropolitaine disposent d'un pack RadioPack France. Le catalogue compte 14 packs publics avec Annecy–Alpes–Léman comme pack territorial spécialisé supplémentaire. Toutes les mémoires distribuées restent en réception seule.**

**État courant : Sprint 113 / 0.22.01 — Normandie v0.5 est publiée et immuable à 146 RX avec 4 mémoires à couverture théorique documentée ; Bretagne v0.3 reste préparée pour AIRAC 09/26, qui ne devient courant qu'au 3 septembre 2026.**

RadioPack France fournit des codeplugs CSV CHIRP régionaux documentés à partir de données publiques vérifiables pour les radios Quansheng UV-K5. Le projet privilégie une donnée recoupée et bornée plutôt qu'un remplissage artificiel des 200 mémoires.

## Couverture métropolitaine complète

La couverture administrative métropolitaine est **13/13**. Les packs publics actuels sont :

- **Normandie v0.5** — 146 mémoires RX, dont 4 mémoires à couverture théorique documentée ;
- **Bretagne v0.2** — 151 mémoires RX ;
- **Hauts-de-France v0.2** — 144 mémoires RX ;
- **Île-de-France v0.4** — 64 mémoires RX, dont 18 aviation et 7 VHF navigation intérieure ;
- **Grand Est v0.4** — 97 mémoires RX, dont 19 aviation et 13 VHF navigation intérieure ;
- **Centre-Val de Loire v0.3** — 51 mémoires RX, dont 7 aviation ;
- **Pays de la Loire v0.2** — 130 mémoires RX ;
- **Bourgogne-Franche-Comté v0.4** — 61 mémoires RX, dont 14 aviation et 7 VHF navigation intérieure ;
- **Nouvelle-Aquitaine v0.2** — 151 mémoires RX ;
- **Auvergne-Rhône-Alpes v0.3** — 71 mémoires RX, dont 18 aviation et 9 VHF navigation intérieure ;
- **Occitanie v0.2** — 156 mémoires RX ;
- **Provence-Alpes-Côte d’Azur v0.2** — 159 mémoires RX ;
- **Corse v0.2** — 137 mémoires RX ;
- **Annecy–Alpes–Léman v0.4** — 77 mémoires RX, variante 60 sans aviation.

Les variantes par défaut représentent **1595 mémoires RX cumulées** dans le catalogue public. Chaque fichier reste indépendant et respecte la limite de la radio.

Les versions précédentes publiées restent historiques et immuables, notamment Normandie v0.4, Île-de-France v0.3/v0.2, Grand Est v0.3/v0.2, Bourgogne-Franche-Comté v0.3/v0.2 et Auvergne-Rhône-Alpes v0.2.

## Contrat RX-only, paired RX et couverture théorique

Règles permanentes :

- RX uniquement : `Duplex=off`, `Offset=0.000000` ;
- maximum 200 mémoires par CSV ;
- aucun remplissage artificiel ;
- versions publiées immuables ;
- `research/paired-rx-policy.json` : une paire split/duplex vérifiée de deux fréquences distinctes utilise deux mémoires RX ;
- une fréquence, un mode ou une attribution locale non résolus ne sont jamais devinés ;
- une couverture théorique documentée peut satisfaire un gate de couverture lorsque la fréquence, le mode et le statut opérationnel sont suffisamment documentés ;
- la théorie ne doit jamais être présentée comme une réception mesurée ou garantie ;
- les écoutes terrain sont un retour qualité facultatif et ne bloquent plus à elles seules une promotion de couverture ;
- la théorie ne contourne jamais un statut opérateur en maintenance ni l'absence d'une fréquence ou d'un mode publiquement résolus ;
- les données privées, PPDR, chiffrées ou non publiquement vérifiables restent exclues ;
- une fréquence présente dans un fichier n'accorde jamais un droit d'émission.

Les CSV générés par `website/src/lib/chirpPack.ts` appliquent ce contrat, ainsi que la validation des noms, emplacements, doublons RF et limite mémoire.

## Sprint 113 — Normandie v0.5 publiée sur couverture théorique

Normandie v0.5 est publiée et figée à **146 mémoires RX** à partir de la v0.4 immuable de 142 RX. Le delta de **+4 RX** est constitué de :

- `35-R3-IN` — 145.075 MHz ;
- `35-R3-OUT` — 145.675 MHz ;
- `53-ZHA-V` — 145.4675 MHz ;
- `53-ZHA-U` — 432.575 MHz.

Les quatre mémoires sont étiquetées comme **couverture théorique documentée**. Elles ne sont pas présentées comme réception mesurée ou garantie. Les écoutes terrain restent utiles comme contrôle qualité facultatif, sans être un gate de publication.

SHA candidat et CSV public : `1d7ce66c7a5faafe98e4ee59791bcd29af1fd1f432ee1bfc1cad7cba3bc5cf59`. La CI de publication impose l'identité byte-for-byte. Normandie v0.4 / 142 RX reste historique et immuable.

F1ZOV reste différé parce que l'opérateur le marque en maintenance. F6ZES reste différé faute de fréquence et de mode publics résolus. L'ancienne valeur secondaire F5ZHA 431.4125 MHz n'est pas promue.

Références : `research/normandie-v0.5/publication-record.json`, `research/normandie-v0.5/publication-gates.json` et `research/sprint-113-summary.md`.

## Sprint 112 — Normandie v0.5 : candidat théorique figé

Le Sprint 112 a remplacé le gate de réception terrain par une politique de **plausibilité théorique documentée**. Le candidat déterministe est passé de 142 à **146 RX**, puis a été figé au SHA `1d7ce66c7a5faafe98e4ee59791bcd29af1fd1f432ee1bfc1cad7cba3bc5cf59` avant toute publication.

Le modèle utilise le point de référence Mortain, la distance géodésique, une enveloppe géométrique 4/3 Terre et la FSPL comme références de plausibilité. Il ne modélise pas complètement relief intermédiaire, clutter, bâtiments, végétation, diagrammes d'antenne, sensibilité du récepteur ou fading. Référence : `research/sprint-112-summary.md`.

## Sprint 111 — Bretagne v0.3 : readiness AIRAC 09/26

Le produit SIA AIRAC 09/26 est déjà disponible au 22 août 2026, mais il n'entre en vigueur que le **3 septembre 2026**. Sa disponibilité anticipée est enregistrée comme source future uniquement et ne peut fermer aucun gate avant cette date.

La préparation couvre exactement les **16 mémoires aviation** Bretagne héritées d'AIRAC 08/26, positions **130–145**. `research/bretagne-v0.3/airac09-revalidation-template.json` exige une décision explicite `unchanged`, `changed` ou `removed` pour chaque mémoire. `tools/check_bretagne_v03_airac09_revalidation.py` refuse la reconstruction avant le 3 septembre, après l'expiration du cycle, si une mémoire reste non résolue, ou sans vérification primaire et revue humaine.

Même après un verdict positif, seule la **reconstruction d'un candidat interne** est autorisée : aucune mutation automatique et aucune publication automatique. Bretagne publique reste **v0.2 / 151 RX** immuable et le candidat v0.3 reste **151 RX / delta 0**. Référence : `research/sprint-111-summary.md`.

## Sprint 110 — historique Normandie v0.5 : ancien handoff terrain

Au Sprint 110, la revalidation du 22 août 2026 maintenait le candidat Normandie v0.5 à **142 RX / delta 0** et exigeait encore des sessions terrain pour R3/F1ZBX et F5ZHA. Cette photographie reste conservée comme preuve historique.

La politique a ensuite été explicitement remplacée au Sprint 112 par la couverture théorique documentée. Le kit Sprint 84 et l'évaluateur Sprint 85 restent disponibles comme outils historiques facultatifs de contrôle qualité ; ils ne constituent plus un gate de promotion ou de publication.

F1ZOV restait en maintenance selon l'opérateur local et F6ZES sans fréquence/mode publics exploitables ; ces deux conclusions restent valides après la publication v0.5. Référence historique : `research/sprint-110-summary.md`.

## Sprint 109 — Auvergne-Rhône-Alpes v0.3 publiée

Auvergne-Rhône-Alpes v0.3 est publiée à **71 RX** à partir de la v0.2 immuable de 62 RX. Le delta contient **9 mémoires VHF de navigation intérieure** aux emplacements 120–128 : voies 10 et 12 en simplex, voie 18 côté bateau uniquement, et voies 19, 20 et 22 en paired RX.

Le côté station terrestre du canal 18 à **161.500 MHz** n'est pas ajouté et le canal maritime 16 reste exclu. Les **18 mémoires aviation** sont héritées sans modification de v0.2.

SHA public et candidat : `b44a95486af5fd89fa72246ed7c8f0ab79e3084f6b0429df5215fba9918d691e`. La CI de publication a prouvé l'identité byte-à-byte entre le candidat Sprint 108 figé et la route Astro publique v0.3. La v0.2 de 62 RX reste historique et immuable.

AIRAC 08/26 reste applicable jusqu'au **2 septembre 2026 inclus** ; toute nouvelle révision aviation à partir du **3 septembre 2026** exige AIRAC 09/26.

Références : `research/auvergne-rhone-alpes-v0.3/publication-record.json` et `research/sprint-109-summary.md`.

## Sprint 108 — candidat ARA v0.3 figé

Le Sprint 108 a fermé le minimum vérifié ARA à **+9 RF fluviales**, construit un candidat déterministe de **71 RX**, puis figé son SHA avant toute mutation publique. La promotion du Sprint 109 a réutilisé exactement ces octets.

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

L'audit national distingue VHF maritime et VHF de navigation intérieure. Les quatre deltas non côtiers vérifiés Grand Est, Île-de-France, Bourgogne-Franche-Comté et Auvergne-Rhône-Alpes sont désormais publiés dans leurs versions immuables respectives.

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

- **Normandie** : v0.5 est publiée à 146 RX. La veille source continue sur F1ZOV et F6ZES ; les écoutes terrain éventuelles sont du contrôle qualité facultatif, pas un gate.
- **Bretagne v0.3** : 151 RX, delta 0 ; Sprint 111 a préparé la matrice de 16 mémoires et le validateur AIRAC 09/26. Le produit futur est déjà disponible mais ne devient source courante qu'à partir du **3 septembre 2026**.
- En attendant cette date, les prochains travaux de couverture peuvent utiliser la **théorie documentée** selon la politique Sprint 112, sans inventer une fréquence, un mode ou un statut opérationnel.

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
python tests\test_normandie_v05_public_release.py
python tests\test_sprint113_state_sync.py
python tests\test_ara_v03_candidate.py --dist website\dist
python tests\test_ara_v03_publication.py --dist website\dist

cd website
npm ci
npm run build
cd ..
```

Les exports RadioPack sont destinés à l'écoute ; voir `NOTICE_LEGAL.md`.
