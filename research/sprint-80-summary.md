# Sprint 80 — publication Bretagne v0.2

État logique : **0.21.69**.

Bretagne v0.2 est publiée et immuable à **151 mémoires RX**. Le fichier public est la copie exacte du candidat gelé au Sprint 79 : base v0.1 de 135 mémoires + 16 mémoires aviation AIRAC 08/26.

## Contrôles de publication

- revue prépublication : **10/10**, **0 bloqueur** ;
- contrôle SIA le 12 août 2026 : AIRAC 08/26 CORRIGENDUM toujours courant, valable du 6 août au 2 septembre 2026 inclus ;
- aucune comparaison XML champ par champ n'est revendiquée sans extraction directe de l'XML ;
- toutes les lignes restent RX-only (`Duplex=off`, `Offset=0.000000`) ;
- aucune RF dupliquée ;
- Ch64/Ch79 restent génériques sans site CROSS local non prouvé ;
- aucune fréquence ADRASEC opérationnelle non publiée n'est intégrée.

## Publication

- CSV : `website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv` ;
- mémoires : **151** ;
- SHA-256 : `73aa3d530ae9f6c572eb01794b0861ecba61df0faf7884ee766085d3de7601a4` ;
- record : `research/bretagne-v0.2/publication-record.json` ;
- Bretagne v0.1 reste conservée comme publication historique immuable.

La bascule du registre, de la page Bretagne, du générateur et de `website/src/data/regions.json` pointe maintenant vers v0.2 / 151 mémoires.

## Compatibilité historique

Les garde-fous Bretagne des Sprints 71 à 79 restent exécutables après publication. Les tests qui devaient historiquement prouver l'absence d'une v0.2 publique ont été rendus forward-compatible : ils continuent de valider leur état historique, puis reconnaissent la publication explicite du Sprint 80 sans affaiblir les contrôles de source, de déduplication ou d'immutabilité.

La v0.1 reste vérifiée octet pour octet contre son candidat historique et demeure présente dans l'arbre public comme archive immuable. La v0.2 possède ses propres garde-fous `tests/test_bretagne_v02_public_release.py` et `tests/test_sprint80_bretagne_v02_publication.py`, tous deux branchés dans la CI principale.

Le test générique du générateur web valide désormais Bretagne v0.2 / 151, y compris son aviation fixe incluse, tandis que le sélecteur aviation optionnel reste limité à Annecy–Alpes–Léman.

## Validation de clôture

Avant le commit d'archive final, la suite CI complète a été rejouée avec succès : tous les tests dépôt jusqu'au générateur web, les garde-fous Sprints 71–80 et le build Astro passent ensemble. Le commit de clôture demande en plus l'archive de référence exacte du HEAD final.
