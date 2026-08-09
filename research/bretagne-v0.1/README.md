# Bretagne — espace de recherche v0.1

Cet espace initialise le troisième pack régional RadioPack France à partir du starter `tools/create_regional_pack.py`.

## État actuel

- statut : `research_scaffold_not_public` ;
- aucune fréquence n'est encore retenue ;
- aucun nombre cible de mémoires n'est imposé ;
- aucun fichier public n'est créé ;
- aucune entrée n'est ajoutée à `website/src/lib/packRegistry.ts` ;
- aucune entrée n'est ajoutée à `website/src/data/regions.json`.

## Règle de zonage Bretagne

La Bretagne ne doit **pas** être traitée comme une seule zone radio uniforme.

La recherche doit distinguer au minimum :

- **Bretagne Nord / Manche Ouest** — contexte opérationnel CROSS Corsen ;
- **Bretagne Sud / Atlantique** — contexte opérationnel CROSS Etel ;
- **zone de transition du Finistère Sud** — frontière opérationnelle exacte à confirmer sur la cartographie officielle actuelle avant toute publication.

Cette séparation s'applique particulièrement à la VHF maritime, mais également à l'étude des relais radioamateurs et de toute infrastructure dont la couverture dépend réellement du territoire.

Le détail est conservé dans :

```text
research/bretagne-v0.1/maritime-zones.json
```

### Canal 16

Le canal 16 reste un canal maritime commun : le futur pack ne devra donc pas créer deux mémoires identiques uniquement pour écrire « Corsen » et « Etel ».

En revanche, les métadonnées de recherche doivent indiquer :

- le CROSS responsable selon la zone ;
- les stations VHF déportées / relais qui assurent la couverture ;
- les éventuelles zones de recouvrement ;
- les canaux météo et de sécurité utilisés localement.

Avant toute promotion d'une mémoire maritime, la limite opérationnelle actuelle Corsen / Etel devra être précisément confirmée.

### Premiers constats officiels

Les sources institutionnelles recensées montrent notamment :

- des opérations récentes à Audierne, l'île de Sein et la pointe de Pen Hir coordonnées par CROSS Corsen ;
- des opérations récentes à Concarneau / Trévignon et Belle-Île coordonnées par CROSS Etel ;
- des opérations au large de Penmarc'h coordonnées par CROSS Etel ;
- le ministère indique que le canal 16 met en relation avec le CROSS de la zone ;
- les annonces météo sont diffusées via le canal 16 vers 79/80, avec une diffusion permanente sur 63/64 notamment dans le Morbihan.

Ces éléments servent au **cadrage**, pas encore à créer des mémoires.

## Sources de départ

Le registre comprend notamment :

- SIA / eAIP pour Brest-Bretagne `LFRB` ;
- SIA / eAIP pour Rennes-Saint-Jacques `LFRN` ;
- portail Open Data de l'ANFR ;
- services ANFR liés aux radioamateurs et stations répétitrices ;
- documentation officielle du ministère chargé de la mer sur le canal 16 et la météo VHF ;
- documentation de la Préfecture maritime de l'Atlantique sur le partage des zones CROSS et des opérations récentes.

Ces références sont des **sources de départ**, pas des fréquences déjà validées pour le pack.

## Relais à étudier

Deux inventaires différents devront être constitués :

1. **stations VHF maritimes déportées / relais de couverture CROSS**, séparées Bretagne Nord et Bretagne Sud ;
2. **relais radioamateurs**, eux aussi rattachés à une sous-zone Bretagne Nord, Bretagne Sud ou transition lorsque cela est pertinent.

On ne déduira pas une zone uniquement du département : l'implantation, la couverture réelle et l'usage opérationnel devront être documentés.

## Suite

1. confirmer la limite SRR actuelle entre CROSS Corsen et CROSS Etel ;
2. inventorier les stations VHF déportées et leurs zones de couverture ;
3. établir les canaux météo / sécurité pertinents par sous-zone ;
4. établir les relais radioamateurs Bretagne Nord et Bretagne Sud ;
5. poursuivre séparément aviation et autres domaines ;
6. construire ensuite un plan mémoire sans objectif artificiel de remplissage ;
7. créer une carte de revue avant toute publication ;
8. publier uniquement après fermeture des portes, revue explicite et CI verte.

Voir `REGIONAL-PACK-WORKFLOW.md` pour le processus complet.
