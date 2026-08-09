# Bretagne — espace de recherche v0.1

Cet espace initialise le troisième pack régional RadioPack France à partir du starter `tools/create_regional_pack.py`.

## État actuel

- statut : `research_scaffold_not_public` ;
- aucune fréquence n'est encore retenue publiquement ;
- aucun nombre cible de mémoires n'est imposé ;
- aucun fichier public n'est créé ;
- aucune entrée n'est ajoutée à `website/src/lib/packRegistry.ts` ;
- aucune entrée n'est ajoutée à `website/src/data/regions.json`.

## Règle paired RX

Bretagne v0.1 applique la politique globale :

```text
research/paired-rx-policy.json
```

Une liaison publique nativement duplex/split dont les deux fréquences sont vérifiées devra conserver **les deux côtés pour l'écoute**. Si les fréquences diffèrent, deux mémoires RX sont prévues ; chacune reste `Duplex=off` et `Offset=0.000000`.

Pour la VHF maritime :

- `-S` = côté navire, navire → côte ;
- `-C` = côté station côtière, côte → navire.

Exemples déjà modélisés dans `public-maritime-radio.json` :

- canal 63 : 156.175 / 160.775 MHz ;
- canal 64 : 156.225 / 160.825 MHz ;
- canal 79 : 156.975 / 161.575 MHz ;
- canal 80 : 157.025 / 161.625 MHz.

Le canal 16 simplex reste une seule mémoire sur 156.800 MHz. Une même fréquence RF partagée par plusieurs sites ou fonctions ne devra pas être dupliquée inutilement.

## Règle de zonage Bretagne

La Bretagne ne doit **pas** être traitée comme une seule zone radio uniforme.

La recherche doit distinguer au minimum :

- **Bretagne Nord / Manche Ouest** — contexte opérationnel CROSS Corsen ;
- **Bretagne Sud / Atlantique** — contexte opérationnel CROSS Etel ;
- **zone de transition du Finistère Sud** — interface autour de la Pointe de Penmarc'h, avec recouvrements radio encore à documenter avant toute publication.

La responsabilité SAR est désormais primaire-vérifiée des deux côtés de Penmarc'h : CROSS Corsen de la **Baie du Mont-Saint-Michel** à la Pointe de Penmarc'h, et CROSS Étel à partir de la Pointe de Penmarc'h jusqu'à la frontière espagnole. Cela ne permet pas de déduire la couverture radio réelle ou les sites émetteurs.

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

### Réseau technique CROSS Étel — 17 stations actuelles

Le nouveau fichier :

```text
research/bretagne-v0.1/etel-network.json
```

enregistre une information actuelle supplémentaire provenant d'une offre officielle DIRM NAMO publiée en juillet 2026 : le service technique du CROSS Étel assure la maintenance de **17 stations radio réparties sur le littoral, de la Pointe de Penmarc'h à Biarritz**.

Cette information donne le **dimensionnement actuel du réseau**, pas la liste nominative de ses 17 stations ni leurs canaux. Les quatre émetteurs météo bretons déjà vérifiés restent donc un inventaire partiel. La page actuelle du CROSS Étel confirme en plus Chassiron et Étel sur le canal 63 en diffusion continue ; Chassiron est conservé comme contexte hors Bretagne.

Le canal 64 reste non attribué : le fait que le réseau compte 17 stations ne permet pas de choisir arbitrairement Étel, Groix, Belle-Ile, Penmarc'h ou un autre site. La règle `channel_64_site_must_not_be_guessed` est testée explicitement.

### CROSS Corsen

Le réseau actuel est documenté à 10 stations VHF et 2 stations MF. Cap Fréhel et Stiff/Ouessant sont primaire-vérifiés comme infrastructures radio actuelles sans canal publié. Une opération officielle confirme une couverture VHF actuelle au nord de la Pointe du Raz, sans identifier l'émetteur ni le canal.

Le canal 79 reste donc sans émetteur actuel primaire-vérifié. La frontière SAR à Penmarc'h, la couverture VHF du Raz et l'existence d'une infrastructure radio ne doivent jamais être utilisés pour inventer une affectation de canal.

### Premiers constats officiels

Les sources institutionnelles recensées montrent notamment :

- des opérations récentes à Audierne, l'île de Sein, la pointe de Pen Hir et la Pointe du Raz coordonnées par CROSS Corsen ;
- des opérations récentes à Concarneau / Trévignon et Belle-Île coordonnées par CROSS Etel ;
- l'interface de responsabilité SAR des deux CROSS à Penmarc'h ;
- le réseau technique actuel du CROSS Étel compte 17 stations radio entre Penmarc'h et Biarritz ;
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

Les nouvelles sources DIRM NAMO utilisées pour l'interface Penmarc'h, les réseaux CROSS et les émetteurs météo sont tracées dans `public-maritime-radio.json`, `maritime-zones.json` et `etel-network.json`.

Ces références sont des **sources de départ ou de validation de recherche**, pas des fréquences déjà publiées pour le pack.

## Relais à étudier

Deux inventaires différents devront être constitués :

1. **stations VHF maritimes déportées / relais de couverture CROSS**, séparées Bretagne Nord et Bretagne Sud ;
2. **relais radioamateurs**, eux aussi rattachés à une sous-zone Bretagne Nord, Bretagne Sud ou transition lorsque cela est pertinent.

Pour les relais/transpondeurs analogiques finalement sélectionnés, les deux côtés publiquement vérifiés seront conservés en RX conformément à la politique paired RX. On ne déduira pas une zone ou un rôle ADRASEC uniquement du département.

## Suite

1. inventorier depuis une source primaire les stations VHF déportées de CROSS Corsen et leurs zones de couverture ;
2. identifier progressivement les **17 stations radio du CROSS Étel** sans déduire leurs noms du seul dimensionnement du réseau ;
3. réconcilier l'usage actuel du canal 64 dans le Morbihan avec une source primaire locale ;
4. documenter les éventuels recouvrements radio autour de l'interface Penmarc'h ;
5. poursuivre les relais radioamateurs et ADRASEC Bretagne Nord / Bretagne Sud ;
6. construire le futur plan mémoire en conservant les deux côtés des liaisons duplex/split vérifiées ;
7. poursuivre séparément aviation et autres domaines ;
8. construire ensuite un plan mémoire sans objectif artificiel de remplissage ;
9. créer une carte de revue avant toute publication ;
10. publier uniquement après fermeture des portes, revue explicite et CI verte.

Voir `REGIONAL-PACK-WORKFLOW.md` pour le processus complet.
