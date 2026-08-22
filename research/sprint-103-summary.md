# Sprint 103 — VHF navigation intérieure

Date : 2026-08-22

## Décision

La VHF de navigation intérieure est désormais traitée comme une famille distincte de la VHF marine.

Règles :

- toujours RX-only (`Duplex=off`, `Offset=0.000000`) ;
- aucune RF dupliquée si une fréquence fluviale est déjà présente via le bloc VHF marine ;
- la voie 10 est la première voie bateau-bateau en navigation intérieure française ;
- les affectations d'écluses, de ports et d'informations nautiques doivent être prouvées par une source officielle actuelle ;
- le canal maritime 16 n'est pas ajouté automatiquement aux packs intérieurs.

## Grand Est v0.4

La v0.3 publique reste immuable à **84 RX**.

Le scope fluvial Grand Est est fermé pour un candidat interne à **97 RX** :

- 84 mémoires v0.3 conservées ;
- +13 mémoires VHF navigation intérieure ;
- voies bateau-bateau : 6, 8, 10, 13, 72, 77 ;
- Strasbourg port : voie 11 ;
- Rhin/Moselle : voies 19, 20 et 22 en paired RX quand elles sont duplex ;
- pas de canal 16 ajouté ;
- voie 6 conservée en RX avec avertissement : usage interdit sur le Rhin entre PK 150 et 350.

Sources principales : ANFR Manuel CRR fluvial mai 2025 et Guide CCNR Rhin/Moselle édition 2026.

Le builder `tools/build_grand_est_v04_candidate.py` vérifie d'abord le SHA public immuable de Grand Est v0.3 (`45aef8547a701e7541e620fa9a2d8394595576921e793b75238146ff6e42e720`) avant d'ajouter le bloc fluvial.

## Audit national pass 1

Le fichier `research/sprint-103-inland-vhf-audit.json` couvre les 13 régions métropolitaines plus Annecy–Alpes–Léman.

### Packs intérieurs où des RF fluviales manquent clairement

- Grand Est → v0.4 en cours ;
- Île-de-France → futur v0.4 ;
- Bourgogne-Franche-Comté → futur v0.4 ;
- Auvergne-Rhône-Alpes → futur v0.3.

Centre-Val de Loire possède bien de la navigation intérieure, mais les affectations VHF locales actuelles doivent encore être fermées avant toute addition.

### Packs côtiers

Normandie, Bretagne, Hauts-de-France, Pays de la Loire, Nouvelle-Aquitaine, Occitanie, PACA et Corse disposent déjà d'un bloc VHF marine ou d'un périmètre côtier. Pour eux, les fréquences fluviales identiques ne doivent pas être ajoutées une seconde fois : il faut vérifier la couverture RF existante et ajouter seulement la provenance / le contexte fluvial si nécessaire.

Des usages fluviaux officiels sont déjà confirmés lors de ce pass pour Hauts-de-France, Pays de la Loire, Nouvelle-Aquitaine, Occitanie et PACA. Normandie doit faire l'objet d'un audit Seine détaillé ; Bretagne d'un audit des voies intérieures ; Corse n'a pas de scope fluvial séparé identifié.

Annecy–Alpes–Léman reste un cas lacustre séparé.

## État

Aucune version publique n'est modifiée dans ce sprint à ce stade. Le prochain jalon est de générer et figer le candidat Grand Est v0.4, puis de fermer la checklist avant toute publication.
