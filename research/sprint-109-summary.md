# Sprint 109 — Auvergne-Rhône-Alpes v0.3 : promotion publique

Date : 2026-08-22

## Objectif

Promouvoir vers le site public le candidat Auvergne-Rhône-Alpes v0.3 figé au Sprint 108, sans modifier son contenu radio.

## Base de publication

- version publique précédente : v0.2 ;
- base : **62 RX** ;
- SHA public v0.2 : `60b4f96467419db40e9f3f33076057f4e093853c81d9e3315b8fe7f0459daa53` ;
- candidat Sprint 108 : **71 RX** ;
- delta : **+9 mémoires VHF navigation intérieure** ;
- SHA candidat figé : `b44a95486af5fd89fa72246ed7c8f0ab79e3084f6b0429df5215fba9918d691e`.

Le Sprint 109 n'est autorisé à publier que si le CSV produit par Astro est strictement identique, octet par octet, à ce candidat figé.

## Scope VHF navigation intérieure

- emplacements : 120–128 ;
- canal 10 : 156.500 MHz ;
- canal 12 : 156.600 MHz ;
- canal 18 : 156.900 MHz, côté bateau uniquement ;
- canal 19 : 156.950 / 161.550 MHz ;
- canal 20 : 157.000 / 161.600 MHz ;
- canal 22 : 157.100 / 161.700 MHz ;
- canaux 19/20/22 conservés en paired RX ;
- 161.500 MHz n'est pas ajouté pour le canal 18 ;
- canal maritime 16 / 156.800 MHz exclu.

## Implémentation publique

- builder site : `website/src/lib/araPack.ts` ;
- route CSV : `website/src/pages/downloads/auvergne-rhone-alpes/radiopack-france-auvergne-rhone-alpes-v0.3.csv.ts` ;
- registre : `website/src/lib/packRegistry.ts` → v0.3 / 71 RX ;
- métadonnées région : `website/src/data/regions.json` ;
- page région : affichage du bloc VHF navigation intérieure 120–128 ;
- release scope : `research/auvergne-rhone-alpes-v0.3/release-scope.json` ;
- gates : `research/auvergne-rhone-alpes-v0.3/publication-gates.json` ;
- publication record : `research/auvergne-rhone-alpes-v0.3/publication-record.json` ;
- garde public : `tests/test_ara_v03_publication.py`.

## Gates obligatoires

La publication est refusée si l'un des points suivants échoue :

- v0.2 n'est plus exactement à 62 RX / SHA figé ;
- les 62 lignes de base dérivent ;
- le candidat reconstruit dérive de `b44a9548…d691e` ;
- le CSV public v0.3 diffère du candidat, même d'un seul octet ;
- les 71 RF, noms ou emplacements ne sont plus uniques ;
- le contrat RX-only n'est plus respecté ;
- la voie 18 ajoute 161.500 MHz ;
- le canal maritime 16 apparaît ;
- le registre ou la page région n'annoncent pas 71 RX / v0.3.

## Aviation

Les 18 mémoires aviation sont héritées sans modification de v0.2, dans le contexte AIRAC 08/26 valable jusqu'au **2 septembre 2026 inclus**. Toute nouvelle révision aviation à partir du **3 septembre 2026** nécessite une revalidation AIRAC 09/26.

## Immuabilité

Après validation CI et fusion :

- ARA v0.3 devient la version publique immuable à 71 RX ;
- ARA v0.2 reste conservée comme publication historique immuable à 62 RX ;
- le SHA public v0.3 doit être exactement `b44a95486af5fd89fa72246ed7c8f0ab79e3084f6b0429df5215fba9918d691e`.
