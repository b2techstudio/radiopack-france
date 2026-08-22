# Sprint 107 — Bourgogne-Franche-Comté v0.4 publiée

Date : 2026-08-22

## Objectif

Promouvoir le candidat Bourgogne-Franche-Comté v0.4 figé au Sprint 106 vers le site public sans modifier son contenu radio ni son SHA-256.

## Résultat

Bourgogne-Franche-Comté v0.4 est publiée à **61 mémoires RX**, soit **+7** par rapport à la v0.3 de 54 RX.

SHA-256 public et candidat :

`02dcba7e14a0cce331b63126ea4e552d41013ebd51aecec19907009f40236a72`

La CI de la PR #45 a construit la route Astro v0.4 et a prouvé l'identité byte-à-byte avec le candidat figé : `byte_identity=true`.

## VHF navigation intérieure

Le delta public retient 7 RF vérifiées sur les emplacements **120–126** :

| Mémoire | RF RX (MHz) | Usage |
| --- | ---: | --- |
| FLV10 | 156.500 | voie 10 bateau-bateau, Saône BFC / CRR branche Sud |
| FLV12 | 156.600 | voie 12, Centre-Bourgogne Auxerre–Joigny |
| FL20-B | 157.000 | voie 20, côté bateau, écluse d'Écuelles |
| FL20-T | 161.600 | voie 20, côté station terrestre |
| FL22-B | 157.100 | voie 22, côté bateau, écluses Seurre / Ormes |
| FL22-T | 161.700 | voie 22, côté station terrestre |
| FLV69 | 156.475 | voie 69, Saint-Aubin–Cannes-Écluse |

Le canal 18 n'est pas ajouté : l'affectation documentée concerne la traversée de Lyon et reste dans le scope Auvergne-Rhône-Alpes. Aucun canal maritime 16 n'est ajouté.

## Publication web

- route publique v0.4 créée ;
- registre public : v0.4 / 61 RX ;
- page région : bloc navigation intérieure affiché sur 120–126 ;
- v0.3 / 54 RX conservée comme historique immuable ;
- builder TypeScript `buildBfcV04Pack()` ajouté ;
- builder Python lié au SHA public figé ;
- publication record : `published_immutable` ;
- publication gates : **0 blocker**.

## Aviation

Les **14 mémoires aviation** sont héritées sans modification de v0.3. AIRAC 08/26 reste la base de cette publication jusqu'au **2 septembre 2026 inclus**. Toute nouvelle révision aviation à partir du **3 septembre 2026** exige AIRAC 09/26.

## Contrat permanent vérifié

- RX-only : `Duplex=off`, `Offset=0.000000` ;
- 61 mémoires, limite 200 respectée ;
- paired RX pour les canaux 20 et 22 ;
- RF, noms et emplacements uniques ;
- 54 lignes de v0.3 préservées strictement ;
- aucune fréquence locale ambiguë devinée ;
- aucune donnée privée/PPDR ajoutée ;
- versions publiées immuables.

## Suite

La prochaine priorité issue du Sprint 103 est **Auvergne-Rhône-Alpes v0.3**, avec un delta fluvial vérifié d'au moins **+9 RF** à préparer sur Rhône/Saône. Bretagne v0.3 reste bloquée jusqu'à AIRAC 09/26 le 3 septembre 2026 et Normandie v0.5 reste dépendante de ses preuves terrain/source.
