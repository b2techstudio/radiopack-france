# Sprint 24 — Tests de génération isolés

Date : 2026-08-09

## Objectif

Empêcher les tests locaux de modifier les CSV suivis par Git, en particulier sous Windows où une simple régénération peut faire apparaître un fichier comme modifié à cause de différences de fins de ligne.

## Problème observé

`tests/test_generator.py` lançait directement :

```text
python generator/generate_chirp_csv.py --root <depot>
```

Le générateur écrivait alors dans `website/public/downloads/...`. Même lorsque le contenu logique restait identique, le fichier Normandie v0.3.1 pouvait apparaître comme modifié dans `git status`.

## Correction

`generator/generate_chirp_csv.py` accepte désormais :

```text
--output-root <dossier>
```

Les données sources continuent d'être lues depuis `--root`, mais tous les chemins de sortie sont recréés sous `--output-root`.

Le comportement manuel historique reste disponible : si `--output-root` n'est pas fourni, le générateur écrit toujours vers les emplacements publics normaux du dépôt.

## Nouveau comportement du test

`tests/test_generator.py` :

1. mémorise les octets des CSV publics suivis ;
2. crée un répertoire temporaire système ;
3. lance le générateur avec `--output-root` vers ce répertoire ;
4. ouvre chaque CSV temporaire ;
5. compare ses lignes au CSV public suivi correspondant ;
6. vérifie les nombres de mémoires et les règles RX-only ;
7. vérifie à la fin que les fichiers suivis n'ont changé d'aucun octet.

Les sorties temporaires sont automatiquement supprimées à la fin du test.

## Résultat attendu sous Windows

La commande :

```powershell
python tests\test_generator.py
git status
```

doit laisser le dépôt propre :

```text
nothing to commit, working tree clean
```

## CI

Le workflow GitHub Actions exécute désormais cette étape sous le nom :

```text
Test CSV generator in isolated output
```

La génération manuelle des fichiers publics reste une action explicite et distincte des tests.
