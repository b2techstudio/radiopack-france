# Audit primaire métropolitain v0.2 — 19 août 2026

Dernier contrôle avant fusion des onze enrichissements v0.2.

## Aviation SIA

La sélection aviation est revue sur les pages publiques SIA eAIP AD 2.18, dans le contexte du cycle AIRAC 08/26. Le produit AIRAC courant sert de contexte de cycle ; aucune extraction XML champ par champ n'est revendiquée sans lecture directe de l'export XML.

Un second passage primaire a corrigé trois points avant publication :

- **Hauts-de-France / LFQQ Lille** : réalignement des canaux publiés sur l'eAIP courant, avec 126.480 / 129.360 MHz retenues pour l'information, 120.275 MHz approche, 121.855 MHz sol, 118.555 MHz tour et 119.330 MHz ATIS. La fréquence FIS 132.540 MHz est documentée dans l'eAIP mais reste volontairement hors de la sélection bornée afin de conserver les 14 mémoires aviation prévues ;
- **Île-de-France / LFPB Le Bourget** : 123.835 MHz est libellée FIS et non APP ;
- **Grand Est** : la sélection a été reconstruite depuis LFST, LFSB, LFJL et LFSN. Bâle-Mulhouse sol est 121.605 MHz ; le doublon 121.805 MHz détecté par le validateur a donc été supprimé par correction de la donnée, jamais par affaiblissement du garde-fou.

## Radioamateur et VHF marine

Les relais FM 2 m restent des sélections publiques recoupées RepeaterBook France + F5AIB/REF, avec le plan de bande REF comme garde-fou et la politique paired RX active. Les régions littorales réutilisent le dataset national VHF marine, sans réinterprétation locale non prouvée.

## Garde-fous de publication

- RX uniquement : `Duplex=off`, `Offset=0.000000` ;
- déduplication RF active ;
- maximum 200 mémoires par pack ;
- v0.1 historiques conservées et générables ;
- aucune fréquence privée, PPDR ou opérationnelle non publiquement vérifiable ;
- UHF et numérique différés à une revue dédiée ;
- aucun remplissage artificiel des mémoires restantes.

La CI et le build Astro doivent reconstruire les onze v0.2 sans fréquence dupliquée avant fusion.
