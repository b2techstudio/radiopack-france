# Sprint 67 — synthèse des références courantes

Date : 11 août 2026  
État logique visé : `0.21.56`

## Objectif

Le Sprint 67 ne cherche pas à multiplier les recherches générales déjà épuisées. Il consolide trois frontières de preuve encore susceptibles d'être mal interprétées :

1. une source primaire actuelle peut confirmer qu'un **canal** est utilisé sans identifier son **site émetteur** ;
2. plusieurs sources secondaires cohérentes ne deviennent pas automatiquement une validation primaire actuelle ;
3. un badge d'état courant affiché par un annuaire ne doit pas écraser une provenance de vérification explicitement datée et ancienne.

Aucune porte de publication n'est abaissée et aucun pack public n'est modifié.

## Guide ministériel 2026

Le `Guide des loisirs nautiques en mer — Sécurité et environnement — Édition 2026`, lié par la page officielle du ministère mise à jour le 19 juin 2026, a pu être chargé et inspecté dans ce sprint.

La page pertinente indique :

- le canal 16 annonce l'émission imminente par le CROSS d'un bulletin météo sur les canaux **79 et 80** ;
- les canaux **63 et 64** diffusent un bulletin météo côtier permanent ;
- le document renvoie ensuite vers le Guide Marine de Météo-France.

Le guide ministériel **ne nomme aucun émetteur pour Ch64 ou Ch79**. Il constitue donc une confirmation primaire actuelle au niveau du canal, mais pas une attribution `canal ↔ site`.

Conséquences :

- Ch64 reste sans site Morbihan primaire-vérifié ;
- Ch79 reste sans émetteur Corsen primaire-vérifié ;
- aucune nouvelle mémoire RF n'est créée : les paires étaient déjà présentes dans la recherche Bretagne.

## CROSS Étel — Ch64

La paire reste :

- 156.225 MHz navire → côte ;
- 160.825 MHz côte → navire ;
- **2 mémoires RX** si Ch64 devient publiable.

Le nouveau guide ministériel renforce la fraîcheur de l'affirmation régionale 63/64, mais n'identifie toujours aucun site. En parallèle, les sources opérationnelles locales déjà exploitées du CROSS Étel convergent toujours vers Ch63 pour Étel/Chassiron.

Le conflit primaire reste donc ouvert :

- fonctionnement actuel de Ch64 sur un site nommé : non prouvé ;
- arrêt de Ch64 : non prouvé ;
- site Ch64 : non confirmé ;
- promotion : interdite.

## CROSS Corsen — Ch79

La paire reste :

- 156.975 MHz navire → côte ;
- 161.575 MHz côte → navire ;
- **2 mémoires RX** si Ch79 devient publiable.

Les indices secondaires sont désormais suffisamment cohérents pour améliorer la priorité de recherche, sans promotion :

- Club de Voile de la Baie d'Erquy : Ch79 à Cap Fréhel et Bodic ;
- une autre table secondaire restitue Fréhel, Bodic, Batz, Stiff et Raz sur Ch79 ;
- une publication secondaire récente mentionne le Stiff / Ouessant pour une diffusion Ch79.

En parallèle, les sources primaires actuelles confirment déjà l'existence d'infrastructures radio CROSS à **Cap Fréhel** et **Stiff / Ouessant**, mais sans mapping Ch79.

La convergence `infrastructure primaire actuelle + indice secondaire Ch79` ne devient pas une attribution primaire actuelle. La priorité de revalidation est désormais :

1. Stiff / Ouessant ;
2. Cap Fréhel ;
3. Bodic ;
4. Batz ;
5. Pointe du Raz.

## F5ZHA Laval

La paire de travail reste 145.4675 / 432.575 MHz selon les sources déjà privilégiées dans la recherche.

RepeaterBook présente toutefois deux signaux incompatibles :

- la fiche de recherche courante pour 431.4125 MHz affiche visuellement un statut vert ;
- la page de provenance / âge de vérification associe F5ZHA 431.4125 MHz à la date **2017-02-17** et à l'état **Off-Air**.

Le Sprint 67 interdit donc explicitement d'utiliser un badge d'affichage courant pour masquer la provenance datée. Cette incohérence ne ferme pas la porte : une source locale actuelle ou autoritative équivalente reste requise, puis la pertinence/réception depuis Mortain doit encore être validée.

Delta candidat : **0**.

## F6ZES et R3

F6ZES Sourdeval reste sans fréquence, mode ou état opérationnel exploitable : aucune conjecture, delta 0.

R3 / F1ZBX reste inchangé :

- 145.075 + 145.675 MHz = exactement **2 mémoires RX** si la porte est franchie ;
- **2 sessions terrain indépendantes** restent nécessaires ;
- les sessions sont des preuves, pas des mémoires.

## État final du sprint

Normandie v0.4 :

- candidat interne : **142** ;
- preview : **142** ;
- plafond connu : **147** ;
- revue : **3/9** ;
- blocages : **6** ;
- ajouts éligibles : **0**.

État public inchangé :

- Normandie v0.3.1 : **139 mémoires**, immuable ;
- Annecy–Alpes–Léman v0.2 : **65 / 48 mémoires**, immuable ;
- Bretagne v0.1 : recherche uniquement.

## Nouveau garde-fou

`tests/test_sprint67_current_reference_synthesis.py` verrouille notamment :

- confirmation primaire du canal ≠ attribution du site ;
- convergence secondaire ≠ validation primaire ;
- infrastructure primaire + indice secondaire ≠ mapping primaire `canal ↔ site` ;
- badge d'annuaire courant ≠ remplacement d'une provenance datée ;
- maintien des paires à 2 mémoires RX ;
- absence de toute mutation publique.

Finalisation : garde-fou Sprint 67 intégré à la CI ; aucun fichier public n'est modifié. Le workflow CI principal porte la finalisation atomique du changelog et de l'archive.
