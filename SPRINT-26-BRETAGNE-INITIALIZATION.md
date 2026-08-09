# Sprint 26 — Initialisation Bretagne

Date : 2026-08-09

## Décision

La Bretagne devient la troisième région de travail de RadioPack France.

Ce sprint initialise uniquement la recherche. Il ne publie aucune fréquence et ne modifie pas les deux packs régionaux déjà disponibles.

## Raisons du choix

- continuité géographique avec la Normandie ;
- intérêt d'un futur pack combinant usages terrestres, radioamateurs, aviation et contexte côtier ;
- présence de sources officielles françaises accessibles pour démarrer la recherche ;
- architecture multi-régions et starter désormais suffisamment sûrs pour ouvrir un troisième chantier sans impact public.

## Espace créé

```text
research/bretagne-v0.1/
```

Il contient :

- `README.md` ;
- `pack-plan.json` ;
- `source-registry.json` ;
- `publication-gates.json` ;
- `memory-plan.json`.

## État de départ

- statut : `research_scaffold_not_public` ;
- fréquence retenue : 0 ;
- nombre cible de mémoires : aucun ;
- blocs mémoire : aucun ;
- export public : interdit ;
- ajout au registre public : interdit ;
- création de routes publiques : interdite ;
- revue finale : obligatoire et non réalisée.

## Premières sources officielles recensées

Le registre initial contient uniquement des points d'entrée institutionnels, sans extraction de fréquence :

- SIA / AIP France — Brest Bretagne `LFRB` ;
- SIA / AIP France — Rennes Saint-Jacques `LFRN` ;
- portail Open Data de l'ANFR ;
- page ANFR des missions radioamateurs ;
- annuaire officiel ANFR des radioamateurs autorisés.

Chaque entrée est marquée `frequency_data_promoted: false`.

Une source identifiée n'est donc jamais assimilée à une fréquence validée.

## Garde-fous

`tests/test_bretagne_research_scaffold.py` vérifie notamment :

- les cinq fichiers de recherche ;
- zéro bloc et zéro cible mémoire ;
- tous les drapeaux de publication à `false` ;
- les cinq sources initiales ;
- l'absence de fréquence promue ;
- l'absence de Bretagne dans `packRegistry.ts` ;
- l'absence de Bretagne dans `regions.json` ;
- l'absence de page régionale et de route de téléchargement.

## Packs publics inchangés

- Annecy–Alpes–Léman v0.2 : 65 mémoires, 48 sans aviation ;
- Normandie v0.3.1 : 139 mémoires, version publiée figée.

## Étape suivante

Le prochain travail Bretagne devra d'abord préciser le périmètre et enrichir le registre de sources avant toute création d'inventaire fréquentiel.

Aucune fréquence ne doit être ajoutée uniquement pour atteindre un nombre cible de mémoires.
