# Sprint 81 — initialisation Bretagne v0.3

État logique : **0.21.70**.

Bretagne v0.3 est initialisée en recherche depuis la **v0.2 publique immuable à 151 mémoires RX**. Le candidat interne initial reste à **151**, avec **delta 0** : il reproduit exactement le CSV public v0.2 et n'effectue aucune publication v0.3.

## Base immuable

- Bretagne v0.2 : **151 RX**, toujours version publique courante ;
- SHA-256 : `73aa3d530ae9f6c572eb01794b0861ecba61df0faf7884ee766085d3de7601a4` ;
- builder v0.3 : `tools/build_bretagne_v03_internal_candidate.py` ;
- aucun CSV public v0.3 ;
- aucun changement du registre public.

## Transition AIRAC

Le contrôle du 12 août 2026 conserve AIRAC 08/26 comme cycle courant jusqu'au **2 septembre 2026 inclus**. EUROCONTROL place AIRAC 2609 du **3 au 30 septembre 2026**.

`research/bretagne-v0.3/airac-transition-policy.json` impose donc :

- v0.2 reste immuable après expiration d'AIRAC 08/26 ;
- toute publication v0.3 avec aviation à partir du 3 septembre doit revalider le bloc aviation sur le cycle courant ;
- un remplacement/corrigendum SIA antérieur impose également un nouveau contrôle de fraîcheur ;
- aucune égalité champ par champ avec l'XML courant n'est revendiquée sans extraction directe de ses octets.

## Backlog v0.3

Les dossiers ouverts sont limités à :

- transition AIRAC 09/26 ;
- F1ZUG / fréquence de transpondeur ADRASEC35, source publique uniquement ;
- CROSS Étel Ch64 ;
- CROSS Corsen Ch79 ;
- F5ZPV après éventuelle preuve de redémarrage ;
- F5ZZH après éventuelle preuve de redémarrage/site ;
- F5ZZC-4, fréquence de service actuelle non résolue.

Les revues ADRASEC générales déjà résolues à delta RF 0 et F1ZBZ déjà entièrement représenté ne sont pas rouverts sans nouvelle preuve.

## Garde-fou

`tests/test_sprint81_bretagne_v03_initialization.py` vérifie l'identité exacte avec le CSV v0.2, le SHA-256, 151 mémoires RX uniques, l'absence de v0.3 publique, le maintien du registre v0.2 et les frontières du backlog/AIRAC.

## Validation finale

- HEAD de pré-clôture propre : `0248000c1152b83ee15cb512b24e9876b14402e2` ;
- CI complète de pré-clôture : **succès** (run 845) ;
- garde-fou Sprint 81 : **succès** ;
- build Astro de production : **succès** ;
- générateur web et catalogue des packs publics : **succès** ;
- helper, trigger et workflow temporaires de finalisation : **supprimés du dépôt**.

Le commit de clôture porte le marqueur `[reference-archive]` afin de générer l'archive source exacte du HEAD final après validation complète de la CI.
