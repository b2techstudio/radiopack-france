# Sprint 20 — aperçu web du générateur

Date : 2026-08-08

## Objectif

Brancher les options Annecy–Alpes–Léman v0.2 dans une véritable interface Astro sans publier le CSV final.

## Réalisé

- création de la page `/generateur` ;
- ajout du lien Générateur dans la navigation principale ;
- ajout de la route au sitemap ;
- option **Inclure les fréquences aviation** active dans l'aperçu :
  - 65 mémoires avec aviation ;
  - 48 mémoires sans aviation ;
- option **Contrôle NOTAM avant génération** active dans l'aperçu ;
- confirmation facultative « J'ai vérifié les NOTAM applicables » ;
- résumé dynamique du nombre de mémoires et de l'état NOTAM ;
- maintien du bouton de génération CSV Annecy en état désactivé ;
- maintien de l'absence du fichier public `radiopack-france-annecy-alpes-leman-v0.2.csv` ;
- ajout de `tests/test_web_generator.py` et branchement dans la CI.

## Règles conservées

- aucune fréquence n'est ajoutée par l'interface ;
- le contrôle NOTAM n'altère jamais les fréquences ;
- toutes les mémoires restent RX-only avec `Duplex=off` ;
- le candidat complet reste celui de 65 mémoires validé au Sprint 19 ;
- l'interface web visible ne vaut pas publication du pack ;
- le téléchargement v0.2 nécessite encore une action explicite séparée.

## État de sortie

- aperçu web : **câblé** ;
- backend de prépublication : **câblé** ;
- CSV public Annecy v0.2 : **absent** ;
- téléchargement web Annecy v0.2 : **verrouillé**.
