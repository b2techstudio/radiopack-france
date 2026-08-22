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
- builder déterministe : `tools/build_bfc_v04_candidate.py` ;
- test : `tests/test_bfc_v04_candidate.py` ;
- workflow CI : `.github/workflows/bfc-v04-inland-vhf.yml`.

Le builder part du CSV v0.3 produit par un build Astro frais, vérifie son SHA-256 public figé, conserve les 54 lignes de base, ajoute les 7 mémoires sur les emplacements 120 à 126, puis produit un candidat interne de 61 RX avec manifeste et SHA-256.

## Contrat contrôlé

- 61 mémoires maximum attendu pour ce candidat ;
- toutes les lignes restent `Duplex=off` et `Offset=0.000000` ;
- aucune RF, aucun nom et aucun emplacement dupliqué ;
- limite CHIRP de 200 mémoires respectée ;
- v0.3 publique inchangée ;
- aucun canal 18 ajouté dans BFC ;
- aucun canal maritime 16 ajouté ;
- aucune affectation locale non prouvée n'est inventée.

## Statut de publication

`internal_candidate` — **aucune publication v0.4 effectuée à cette étape**.

Le registre public, la page région et la route de téléchargement restent sur v0.3 tant que le candidat n'a pas passé la CI et que sa base de publication n'a pas été explicitement gelée.

## Suite

1. ouvrir la PR du Sprint 106 et laisser exécuter les workflows BFC v0.3 existants et BFC v0.4 ;
2. relever le SHA-256 déterministe du candidat 61 RX après CI verte ;
3. figer le candidat et les gates de publication v0.4 si aucune anomalie n'est détectée ;
4. publier v0.4 seulement après ce gel, tout en conservant v0.3 comme historique immuable ;
5. passer ensuite à Auvergne-Rhône-Alpes v0.3 (+9 RF fluviales minimum vérifiées au Sprint 103).
