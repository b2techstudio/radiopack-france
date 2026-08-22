# Sprint 106 — Bourgogne-Franche-Comté v0.4 : candidat VHF fluviale

Date : 2026-08-22

## Objectif

Reprendre la file d'action du Sprint 103 après les publications Grand Est v0.4 et Île-de-France v0.4, en préparant le prochain delta non côtier : Bourgogne-Franche-Comté v0.4.

## État de départ

- version publique : Bourgogne-Franche-Comté v0.3 ;
- 54 mémoires RX ;
- SHA-256 public figé : `b5af25a6766b1181e735d376d3f70ab47ffb9ed67b9e38e35bee15e8a86ae7a5` ;
- 14 mémoires aviation AIRAC 08/26 ;
- aucun bloc VHF de navigation intérieure dans la v0.3 ;
- v0.3 publiée et immuable.

## Scope vérifié pour le candidat v0.4

Le minimum officiel actuellement vérifié ajoute 7 RF de navigation intérieure :

| Mémoire | RF RX (MHz) | Usage retenu |
| --- | ---: | --- |
| FLV10 | 156.500 | voie 10 bateau-bateau, Saône BFC / CRR branche Sud |
| FLV12 | 156.600 | voie 12, Centre-Bourgogne Auxerre–Joigny |
| FL20-B | 157.000 | voie 20, côté bateau, écluse d'Écuelles |
| FL20-T | 161.600 | voie 20, côté station terrestre |
| FL22-B | 157.100 | voie 22, côté bateau, écluses de Seurre / Ormes |
| FL22-T | 161.700 | voie 22, côté station terrestre |
| FLV69 | 156.475 | voie 69, secteur Saint-Aubin–Cannes-Écluse |

Le canal 18 n'est pas ajouté à BFC : l'affectation documentée concerne la traversée de Lyon et reste dans le scope Auvergne-Rhône-Alpes.

## Sources officielles

- ANFR — Manuel CRR fluvial, version 6, mai 2025 : plan national des voies et fréquences VHF fluviales.
- VNF Rhône Saône — Avis à la batellerie n°1, édition 2026 : Saône canal 10, Seurre 22, Écuelles 20, Ormes 22 et canal du Rhône au Rhin branche Sud canal 10.
- VNF Centre-Bourgogne — Avis à la batellerie n°01, V01 mars 2026 : canal 12 d'Auxerre à Joigny et canal 69 de Saint-Aubin à Cannes-Écluse.

## Implémentation du Sprint 106

- nouveau dataset : `data/regional/bourgogne-franche-comte-inland-vhf-rx.json` ;
- validation de scope : `research/bourgogne-franche-comte-v0.4/inland-vhf-validation-2026-08-22.json` ;
- scope figé : `research/bourgogne-franche-comte-v0.4/release-scope.json` ;
- gates de publication : `research/bourgogne-franche-comte-v0.4/publication-gates.json` ;
- builder déterministe : `tools/build_bfc_v04_candidate.py` ;
- test : `tests/test_bfc_v04_candidate.py` ;
- workflow CI : `.github/workflows/bfc-v04-inland-vhf.yml`.

Le builder part du CSV v0.3 produit par un build Astro frais, vérifie son SHA-256 public figé, conserve les 54 lignes de base, ajoute les 7 mémoires sur les emplacements 120 à 126, puis produit un candidat interne de 61 RX.

## Résultat CI et gel

La première exécution du workflow BFC v0.4 a réussi intégralement : build Astro, génération, reconstruction déterministe et test des invariants.

Le candidat est désormais figé sur :

`02dcba7e14a0cce331b63126ea4e552d41013ebd51aecec19907009f40236a72`

Le builder refuse désormais tout résultat dont le SHA-256 diffère de cette base gelée.

## Contrat contrôlé

- 61 mémoires exactement pour ce candidat ;
- toutes les lignes restent `Duplex=off` et `Offset=0.000000` ;
- aucune RF, aucun nom et aucun emplacement dupliqué ;
- limite CHIRP de 200 mémoires respectée ;
- les 54 lignes de v0.3 sont conservées strictement ;
- v0.3 publique inchangée ;
- aucun canal 18 ajouté dans BFC ;
- aucun canal maritime 16 ajouté ;
- aucune affectation locale non prouvée n'est inventée.

## Statut de publication

`release_candidate_frozen_internal` — **aucune publication v0.4 effectuée à cette étape**.

Le registre public, la page région et la route de téléchargement restent sur v0.3. Les gates gardent `public_release_allowed=false` tant que deux étapes ne sont pas réalisées : prouver l'identité byte-à-byte d'une route publique v0.4 avec le SHA figé, puis promouvoir le registre/site en conservant v0.3 historique.

## Suite

1. laisser la CI de la PR #44 revalider le candidat avec le SHA et les gates désormais figés ;
2. si elle reste verte, préparer la promotion publique v0.4 dans une étape séparée ;
3. vérifier que le CSV public v0.4 est strictement identique au candidat figé ;
4. basculer registre/page région vers v0.4 et enregistrer la publication immuable ;
5. passer ensuite à Auvergne-Rhône-Alpes v0.3 (+9 RF fluviales minimum vérifiées au Sprint 103).
