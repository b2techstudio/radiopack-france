# Sprint 108 — Auvergne-Rhône-Alpes v0.3 : candidat VHF fluviale figé

Date : 2026-08-22

## Objectif

Poursuivre la file d'action du Sprint 103 après les publications Grand Est v0.4, Île-de-France v0.4 et Bourgogne-Franche-Comté v0.4, en préparant puis en figeant le prochain delta non côtier : Auvergne-Rhône-Alpes v0.3.

## État de départ

- version publique : Auvergne-Rhône-Alpes v0.2 ;
- 62 mémoires RX ;
- SHA-256 public figé : `60b4f96467419db40e9f3f33076057f4e093853c81d9e3315b8fe7f0459daa53` ;
- 18 mémoires aviation AIRAC 08/26 ;
- aucun bloc VHF de navigation intérieure ;
- v0.2 publiée et immuable.

## Scope vérifié pour le candidat v0.3

Le minimum officiel actuellement vérifié ajoute **9 RF** de navigation intérieure :

| Mémoire | RF RX (MHz) | Usage retenu |
| --- | ---: | --- |
| FLV10 | 156.500 | voie 10 bateau-bateau, Rhône hors PK 0–4 |
| FLV12 | 156.600 | voie 12, entrée Port Édouard Herriot |
| FLV18 | 156.900 | voie 18, Rhône PK 0–4 / Pierre-Bénite, côté bateau uniquement |
| FL19-B | 156.950 | voie 19, côté bateau, écluses Rhône ARA |
| FL19-T | 161.550 | voie 19, côté station terrestre |
| FL20-B | 157.000 | voie 20, côté bateau, écluses Rhône ARA |
| FL20-T | 161.600 | voie 20, côté station terrestre |
| FL22-B | 157.100 | voie 22, côté bateau, écluses Rhône ARA |
| FL22-T | 161.700 | voie 22, côté station terrestre |

La seconde RF du canal 18 (`161.500 MHz`) n'est pas ajoutée : le scope documenté du secteur Pierre-Bénite est retenu comme usage bateau-bateau. Le canal maritime 16 n'est pas ajouté à ce pack intérieur.

## Sources officielles

- ANFR — Manuel CRR fluvial, version 6, mai 2025 : plan national des voies et fréquences VHF fluviales.
- VNF Direction territoriale Rhône Saône — Avis à la batellerie n°1, édition 2026 : canal 10 sur le Rhône hors PK 0–4, canal 18 à Pierre-Bénite, canal 12 à l'entrée du Port Édouard Herriot et canaux 19/20/22 pour les écluses selon l'ouvrage.
- Audit national : `research/sprint-103-inland-vhf-audit-pass2.json`.

## Implémentation Sprint 108

- dataset : `data/regional/auvergne-rhone-alpes-inland-vhf-rx.json` ;
- validation de scope : `research/auvergne-rhone-alpes-v0.3/inland-vhf-validation-2026-08-22.json` ;
- gel candidat : `research/auvergne-rhone-alpes-v0.3/candidate-freeze.json` ;
- builder déterministe : `tools/build_ara_v03_candidate.py` ;
- test : `tests/test_ara_v03_candidate.py` ;
- workflow CI : `.github/workflows/ara-v03-inland-vhf.yml`.

Le builder part du CSV v0.2 issu d'un build Astro frais, vérifie son SHA public figé, conserve strictement les 62 lignes de base, ajoute les 9 mémoires aux emplacements 120 à 128 et produit un candidat interne de **71 RX**.

## Gel du candidat

Le premier passage complet du workflow ARA v0.3, run **32590524382**, a reconstruit deux fois le candidat avec succès et validé les invariants. Le candidat est figé sur :

`b44a95486af5fd89fa72246ed7c8f0ab79e3084f6b0429df5215fba9918d691e`

Ce SHA est désormais enregistré littéralement dans `candidate-freeze.json` et contrôlé par le test ARA. Toute dérive d'un octet doit donc faire échouer la CI avant fusion ou promotion.

## Contrat contrôlé

- 71 mémoires exactement ;
- SHA candidat exact : `b44a95486af5fd89fa72246ed7c8f0ab79e3084f6b0429df5215fba9918d691e` ;
- `Duplex=off`, `Offset=0.000000` partout ;
- RF, noms et emplacements uniques ;
- limite 200 mémoires respectée ;
- 62 lignes v0.2 préservées ;
- canaux 19/20/22 en paired RX ;
- canal 18 côté bateau uniquement ;
- aucun canal maritime 16 ;
- aucune affectation locale non prouvée inventée ;
- aucune modification du registre, de la page région ou de la route publique v0.2.

## Statut de publication

`internal_candidate_frozen_not_public` — **aucune publication v0.3 à cette étape**.

Le registre public et la page région restent sur v0.2 / 62 RX. Le gel du candidat n'autorise pas à lui seul une publication publique.

## Suite

1. reconstruire le candidat et vérifier son identité stricte avec le SHA figé ;
2. fusionner Sprint 108 comme candidat interne non public ;
3. préparer dans un sprint/PR séparé la route v0.3, la bascule du registre et la page région ;
4. exiger une identité byte-for-byte avec ce candidat figé avant la promotion publique ;
5. conserver l'AIRAC 08/26 uniquement jusqu'au 2 septembre 2026 inclus, avec revalidation AIRAC 09/26 requise à partir du 3 septembre 2026.
