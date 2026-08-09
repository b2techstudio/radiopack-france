# Sprint 27 — Zonage radio maritime Bretagne

Date : 2026-08-09

## Objectif

Éviter de traiter la Bretagne comme une seule zone radio uniforme.

Le futur pack Bretagne doit tenir compte du fait que le contexte opérationnel VHF change selon la façade maritime, notamment pour le CROSS responsable, la couverture des stations VHF déportées et certaines diffusions météo.

## Découpage de recherche retenu

Le fichier :

```text
research/bretagne-v0.1/maritime-zones.json
```

impose désormais trois sous-zones de recherche :

1. **Bretagne Nord / Manche Ouest** — contexte CROSS Corsen ;
2. **Bretagne Sud / Atlantique** — contexte CROSS Etel ;
3. **transition Finistère Sud** — limite opérationnelle exacte à confirmer sur la cartographie officielle actuelle avant toute publication.

## Canal 16

Le canal 16 est un canal commun. Le futur pack RX ne doit donc pas créer deux mémoires identiques uniquement pour afficher deux noms de CROSS.

En revanche, les métadonnées doivent conserver :

- le CROSS responsable selon la zone ;
- les stations VHF déportées assurant la couverture ;
- les éventuelles zones de recouvrement ;
- les canaux météo et de sécurité utilisés localement.

Aucune fréquence n'est promue pendant ce sprint.

## Constat opérationnel utilisé pour le cadrage

Les sources officielles récentes permettent de distinguer clairement les contextes suivants :

- Audierne, l'île de Sein et la pointe de Pen Hir relèvent d'opérations coordonnées par CROSS Corsen ;
- Concarneau / Trévignon et Belle-Île relèvent d'opérations coordonnées par CROSS Etel ;
- des opérations récentes au large de Penmarc'h ont été coordonnées par CROSS Etel.

Ces exemples ne servent pas à fixer à eux seuls la frontière SAR exacte. La cartographie officielle actuelle de partage de la SRR Corsen / Etel reste la référence à exploiter avant publication.

## Météo VHF

La documentation officielle du ministère indique notamment :

- annonce des bulletins météo via le canal 16 avant diffusion sur 79/80 ;
- diffusion permanente sur 63/64 notamment dans le Morbihan.

Ces éléments sont enregistrés comme contexte de recherche uniquement.

## Relais et stations

Deux inventaires séparés seront nécessaires :

- stations VHF maritimes déportées / relais de couverture des CROSS ;
- relais radioamateurs, rattachés à une sous-zone Bretagne Nord, Bretagne Sud ou transition lorsque cela est pertinent.

## Porte de publication

Une nouvelle porte `maritime_zoning` bloque explicitement toute publication tant que :

- la limite actuelle Corsen / Etel n'est pas confirmée ;
- les stations VHF déportées ne sont pas inventoriées ;
- les canaux météo / sécurité utiles ne sont pas cadrés par zone ;
- les relais radioamateurs ne sont pas organisés territorialement.

## État public

Aucun changement :

- Bretagne reste absente de `packRegistry.ts` ;
- Bretagne reste absente de `regions.json` ;
- aucune page publique Bretagne ;
- aucun CSV Bretagne ;
- aucune fréquence Bretagne promue.

Annecy–Alpes–Léman v0.2 reste à 65 / 48 mémoires et Normandie v0.3.1 reste figée à 139 mémoires.
