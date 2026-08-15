# Bretagne v0.3 — recherche

État : **Sprint 82 / 0.21.71 — six dossiers non-AIRAC revalidés, candidat toujours 151 mémoires RX, delta RF 0**.

La v0.3 démarre sans nouvelle mémoire : le candidat interne initial reproduit exactement le CSV public v0.2. La v0.2 reste immuable et demeure la version publique courante.

## Sprint 82 — revalidation publique ciblée

`public-service-revalidation.json` recontrôle F1ZUG, F5ZZC-4, F5ZPV, F5ZZH et les mappings CROSS Étel Ch64 / Corsen Ch79. Aucun dossier ne produit de nouvelle RF : **delta 0**.

- F1ZUG APRS 144.800 MHz reste déjà couvert nationalement ; le transpondeur ADRASEC35 reste sans fréquence publique ;
- F5ZZC-4 reste non résolu faute de source actuelle de fréquence ;
- F5ZPV et F5ZZH restent arrêtés selon l’opérateur local ;
- Ch64 et Ch79 restent des paires génériques sans attribution locale non prouvée.

## Base

- version publiée de départ : **Bretagne v0.2** ;
- mémoires : **151 RX** ;
- SHA-256 : `73aa3d530ae9f6c572eb01794b0861ecba61df0faf7884ee766085d3de7601a4` ;
- delta initial v0.3 : **0** ;
- aucun CSV public v0.3 ;
- aucune bascule du registre public.

Le builder `tools/build_bretagne_v03_internal_candidate.py` vérifie le record de publication v0.2, son SHA-256, le contrat RX-only et l'unicité des positions, noms et fréquences, puis copie exactement le CSV v0.2 vers une sortie interne v0.3.

## Transition AIRAC

Au 12 août 2026, le SIA maintient AIRAC 08/26 en vigueur du 6 août au 2 septembre 2026 inclus. EUROCONTROL donne AIRAC 2609 du 3 au 30 septembre 2026.

Conséquence : la v0.2 publiée ne change jamais à l'expiration du cycle. En revanche, toute future publication v0.3 contenant le bloc aviation après le 2 septembre doit revalider ce bloc sur le cycle courant avant publication. L'absence d'extraction XML directe interdit toujours de revendiquer une égalité champ par champ avec l'XML courant.

Voir `research/bretagne-v0.3/airac-transition-policy.json`.

## Dossiers reportés

Seuls les dossiers encore ouverts sont repris :

- F1ZUG / fréquence de transpondeur ADRASEC35 : veille sur source publique uniquement ;
- CROSS Étel Ch64 : attribution locale non résolue, delta RF attendu 0 si la paire générique reste inchangée ;
- CROSS Corsen Ch79 : attribution locale non résolue, même règle de non-duplication ;
- F5ZPV : revalidation seulement après preuve de redémarrage ;
- F5ZZH : revalidation seulement après preuve de redémarrage et de site ;
- F5ZZC-4 : fréquence APRS actuelle encore non validée, sans confusion avec F5ZZC analogique ;
- AIRAC 09/26 : transition de fraîcheur planifiée, sans delta mémoire présumé.

Les revues ADRASEC générales déjà résolues à delta RF nul et F1ZBZ déjà entièrement représenté ne sont pas rouverts sans nouvelle preuve.

## Règles

- RX uniquement : `Duplex=off`, `Offset=0.000000` ;
- base v0.2 immuable ;
- une RF déjà présente n'est jamais dupliquée pour de la métadonnée locale ;
- aucune donnée opérationnelle privée PPDR/ADRASEC n'est recherchée ou déduite ;
- une infrastructure arrêtée n'est pas promue ;
- une transition AIRAC déclenche une revue de fraîcheur, pas un ajout automatique ;
- une promotion interne éventuelle reste distincte d'une publication.
