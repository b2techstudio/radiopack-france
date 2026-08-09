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
- **zone de transition du Finistère Sud** — interface autour de la Pointe de Penmarc'h, avec recouvrements radio encore à documenter avant toute publication.

La DIRM NAMO indique désormais explicitement que le **CROSS Étel est compétent à partir de la Pointe de Penmarc'h (Finistère) jusqu'à la frontière espagnole**. Ce point d'interface est donc considéré comme vérifié pour la recherche. Il reste néanmoins nécessaire de documenter la ligne cartographique détaillée, les éventuels recouvrements radio et les stations VHF de CROSS Corsen avant publication.

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

### Validation primaire CROSS Étel

Le planning officiel de diffusion météo du CROSS Étel permet maintenant d'identifier plusieurs émetteurs bretons :

- **Penmarc'h — canal 80** ;
- **Groix — canal 80** ;
- **Belle-Ile — canal 80** ;
- **Étel — canal 63 en diffusion continue**.

Le ministère indique par ailleurs que le canal 16 annonce les bulletins sur 79/80 et mentionne une diffusion permanente sur 63/64 notamment dans le Morbihan. Le planning primaire CROSS Étel exploité n'identifie toutefois pas d'émetteur Bretagne sur le canal 64. RadioPack conserve donc le canal 64 comme donnée réglementaire de recherche, sans lui attribuer de site breton tant que ce point n'est pas réconcilié par une source primaire locale actuelle.

Pour CROSS Corsen, la page DIRM actuelle confirme un réseau VHF/MHF et des diffusions météo depuis des stations littorales, mais la liste détaillée des sites et canaux n'est pas fournie dans la source exploitée. Aucun site Corsen n'est donc inventé.

### Premiers constats officiels

Les sources institutionnelles recensées montrent notamment :

- des opérations récentes à Audierne, l'île de Sein et la pointe de Pen Hir coordonnées par CROSS Corsen ;
- des opérations récentes à Concarneau / Trévignon et Belle-Île coordonnées par CROSS Etel ;
- la compétence officielle de CROSS Étel à partir de la Pointe de Penmarc'h vers le sud ;
- le ministère indique que le canal 16 met en relation avec le CROSS de la zone ;
- le planning CROSS Étel identifie Penmarc'h, Groix et Belle-Ile sur le canal 80 et Étel sur le canal 63 en continu.

Ces éléments servent au **cadrage et à la validation de recherche**, pas encore à créer des mémoires publiques.

## Sources de départ

Le registre comprend notamment :

- SIA / eAIP pour Brest-Bretagne `LFRB` ;
- SIA / eAIP pour Rennes-Saint-Jacques `LFRN` ;
- portail Open Data de l'ANFR ;
- services ANFR liés aux radioamateurs et stations répétitrices ;
- documentation officielle du ministère chargé de la mer sur le canal 16 et la météo VHF ;
- documentation de la Préfecture maritime de l'Atlantique sur le partage des zones CROSS et des opérations récentes.

Les nouvelles sources DIRM NAMO utilisées pour l'interface Penmarc'h et les émetteurs météo sont tracées directement dans `public-maritime-radio.json` et `maritime-zones.json`.

Ces références sont des **sources de départ ou de validation de recherche**, pas des fréquences déjà publiées pour le pack.

## Relais à étudier

Deux inventaires différents devront être constitués :

1. **stations VHF maritimes déportées / relais de couverture CROSS**, séparées Bretagne Nord et Bretagne Sud ;
2. **relais radioamateurs**, eux aussi rattachés à une sous-zone Bretagne Nord, Bretagne Sud ou transition lorsque cela est pertinent.

On ne déduira pas une zone uniquement du département : l'implantation, la couverture réelle et l'usage opérationnel devront être documentés.

## Suite

1. inventorier depuis une source primaire les stations VHF déportées de CROSS Corsen et leurs zones de couverture ;
2. documenter les éventuels recouvrements radio autour de l'interface Penmarc'h ;
3. réconcilier l'usage actuel du canal 64 dans le Morbihan avec une source primaire locale ;
4. poursuivre les relais radioamateurs et ADRASEC Bretagne Nord / Bretagne Sud ;
5. poursuivre séparément aviation et autres domaines ;
6. construire ensuite un plan mémoire sans objectif artificiel de remplissage ;
7. créer une carte de revue avant toute publication ;
8. publier uniquement après fermeture des portes, revue explicite et CI verte.

Voir `REGIONAL-PACK-WORKFLOW.md` pour le processus complet.
