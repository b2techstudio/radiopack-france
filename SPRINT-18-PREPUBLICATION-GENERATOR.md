# Sprint 18 — Générateur de prépublication Annecy–Alpes–Léman v0.2

Date : 2026-08-08

## Objectif

Transformer le candidat interne validé en un véritable candidat de prépublication contrôlable, sans créer ni exposer le téléchargement public final.

## Résultat

Le script `tools/build_annecy_prepublication.py` est désormais le backend de prépublication Annecy–Alpes–Léman v0.2.

Il refuse de fonctionner si `tools/check_annecy_release_readiness.py` signale encore une porte bloquante.

Deux variantes sont prises en charge :

- aviation incluse : 65 mémoires ;
- aviation exclue : 48 mémoires.

Les numéros des autres mémoires ne sont pas compactés lorsque l'aviation est retirée.

## Option NOTAM

Le paramètre `--notam-check` accepte :

- `disabled` ;
- `requested_unconfirmed` ;
- `user_confirmed`.

Le choix est enregistré dans le manifeste JSON de génération. Il ne modifie jamais les lignes du CSV et ne bloque pas la génération.

## Emplacement des sorties

Par défaut :

`research/annecy-alpes-leman-v0.2/generated/prepublication/`

Ce chemin est couvert par le `.gitignore` existant et reste hors de `website/public`.

Le téléchargement public réservé reste :

`website/public/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv`

Il n'est pas créé pendant ce sprint.

## Sécurité

- toutes les lignes CSV utilisent `Duplex=off` ;
- aucun nom ne dépasse 10 caractères ;
- aucun doublon de mémoire, nom ou fréquence n'est accepté ;
- le candidat complet contient exactement 65 mémoires ;
- la variante sans aviation contient exactement 48 mémoires ;
- une revue finale explicite reste obligatoire avant toute copie vers `website/public`.

## Tests

`tests/test_annecy_prepublication.py` génère les variantes dans des répertoires temporaires et contrôle notamment :

- 65 mémoires avec aviation ;
- 48 mémoires sans aviation ;
- `Duplex=off` partout ;
- absence de doublons ;
- comportement NOTAM non bloquant ;
- absence persistante du CSV public v0.2.

La CI exécute ce test à chaque changement sur `main`.
