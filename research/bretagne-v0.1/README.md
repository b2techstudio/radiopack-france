# Bretagne — espace de recherche v0.1

Cet espace initialise le troisième pack régional RadioPack France à partir du starter `tools/create_regional_pack.py`.

## État initial

- statut : `research_scaffold_not_public` ;
- aucune fréquence n'est encore retenue ;
- aucun nombre cible de mémoires n'est imposé ;
- aucun fichier public n'est créé ;
- aucune entrée n'est ajoutée à `website/src/lib/packRegistry.ts` ;
- aucune entrée n'est ajoutée à `website/src/data/regions.json`.

## Périmètre de départ

La Bretagne est retenue comme troisième région de recherche. Le premier travail consiste uniquement à identifier et documenter les sources officielles utiles avant toute extraction de fréquences.

Les premiers points d'entrée recensés sont :

- SIA / eAIP pour Brest-Bretagne `LFRB` ;
- SIA / eAIP pour Rennes-Saint-Jacques `LFRN` ;
- portail Open Data de l'ANFR ;
- services ANFR liés aux radioamateurs et stations répétitrices.

Ces références sont des **sources de départ**, pas des fréquences déjà validées pour le pack.

## Suite

1. définir précisément le périmètre géographique et fonctionnel ;
2. compléter le registre de sources ;
3. rechercher séparément aviation, radioamateur et éventuels blocs régionaux pertinents ;
4. réutiliser les blocs nationaux uniquement lorsqu'ils sont appropriés au futur pack ;
5. construire un plan mémoire sans objectif artificiel de remplissage ;
6. créer une carte de revue avant toute publication ;
7. publier uniquement après fermeture des portes, revue explicite et CI verte.

Voir `REGIONAL-PACK-WORKFLOW.md` pour le processus complet.
