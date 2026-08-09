# Sprint 25 — Starter de pack régional

Date : 2026-08-09

## Objectif

Préparer un moyen sûr et reproductible d'initialiser la recherche d'un futur pack régional sans créer de contenu public par accident.

## Nouvel outil

Le script :

```text
tools/create_regional_pack.py
```

crée uniquement un espace de recherche sous :

```text
research/<slug>-v<version>/
```

Il ne crée aucune page Astro, aucune route CSV et aucune entrée dans `website/src/lib/packRegistry.ts`.

## Fichiers créés

Le starter génère :

- `README.md` ;
- `pack-plan.json` ;
- `source-registry.json` ;
- `publication-gates.json` ;
- `memory-plan.json`.

L'état initial est volontairement vide : aucune fréquence, aucun bloc mémoire et aucun nombre cible de mémoires ne sont imposés.

## Garde-fous par défaut

Le starter fixe dès le départ :

- réception seule ;
- `Duplex=off` ;
- `Offset=0.000000` ;
- noms limités à 10 caractères ;
- maximum 200 mémoires ;
- aucun remplissage artificiel ;
- préférence pour les sources primaires ;
- interdiction de publier des données non vérifiées ;
- revue obligatoire avant publication ;
- versions publiées considérées comme immuables.

Tous les drapeaux de publication commencent à `false`.

## Exemple

```powershell
python tools\create_regional_pack.py --name "Bretagne" --slug bretagne --version 0.1
```

La commande crée alors :

```text
research/bretagne-v0.1/
```

sans modifier le générateur public.

## Sécurité contre les écrasements

Si le dossier cible existe déjà, le script s'arrête avec une erreur. Il n'écrase jamais un espace de recherche existant.

Les slugs sont limités aux caractères `a-z`, `0-9` et aux tirets simples. Les versions acceptées utilisent `X.Y` ou `X.Y.Z`.

## Tests

`tests/test_regional_pack_starter.py` exécute le starter dans un répertoire temporaire et vérifie notamment :

- la présence exacte des cinq fichiers attendus ;
- l'absence de répertoire `website` dans la sortie ;
- l'absence de fréquence ou de nombre cible initial ;
- les drapeaux de publication à `false` ;
- les règles RX-only permanentes ;
- le refus d'écraser un dossier existant ;
- le refus d'un slug invalide ;
- l'absence de modification de `packRegistry.ts` et `regions.json`.

## Publication

Créer un starter n'est que le début du travail de recherche. Pour rendre le pack public, il faut ensuite suivre `REGIONAL-PACK-WORKFLOW.md`, fermer toutes les portes, créer une carte de revue, ajouter explicitement le pack au registre public, mettre le site et le README à jour, puis obtenir une CI verte.
