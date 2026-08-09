# Sprint 24 — Tests de génération isolés

Date : 2026-08-09

## Objectif

Empêcher les tests locaux de modifier les CSV suivis par Git et empêcher une ancienne version régionale publiée d'être réécrite silencieusement à partir de jeux de données partagés devenus plus récents.

## Problème observé

`tests/test_generator.py` lançait directement :

```text
python generator/generate_chirp_csv.py --root <depot>
```

Le générateur écrivait alors dans `website/public/downloads/...`, y compris dans le fichier versionné :

```text
website/public/downloads/normandie/radiopack-france-normandie-v0.3.1.csv
```

Sous Windows, le test faisait donc apparaître ce fichier comme modifié dans `git status`.

Le Sprint 24 a également révélé que ce n'était pas seulement une différence de fins de ligne : les commentaires ISS du jeu national ont été enrichis après la publication de Normandie v0.3.1. Les fréquences et positions du pack publié restent inchangées, mais reconstruire v0.3.1 depuis les jeux partagés actuels ne reproduit plus exactement son contenu historique.

## Règle de version introduite

**Un pack régional publié et versionné est un artefact figé.**

Normandie v0.3.1 n'est donc plus planifiée dans les sorties du générateur générique. Une évolution des données Normandie doit produire une nouvelle version, avec revue et publication explicites, au lieu d'écraser v0.3.1.

Annecy–Alpes–Léman v0.2 reste généré par sa bibliothèque Astro dédiée et ses routes prérendues.

## Sortie isolée

`generator/generate_chirp_csv.py` accepte désormais :

```text
--output-root <dossier>
```

Les données sources continuent d'être lues depuis `--root`, mais les sorties génériques planifiées sont recréées sous `--output-root` en conservant leurs chemins relatifs.

Les sorties génériques actuellement concernées sont :

- PMR446 national ;
- VHF marine nationale ;
- APRS / ISS national ;
- canaux d'appel nationaux ;
- relais analogiques Normandie.

Le pack complet Normandie v0.3.1 est volontairement absent de cette liste.

## Nouveau comportement du test

`tests/test_generator.py` :

1. mémorise les octets des CSV suivis concernés, y compris Normandie v0.3.1 ;
2. crée un répertoire temporaire système ;
3. lance le générateur avec `--output-root` vers ce répertoire ;
4. compare les sorties temporaires génériques aux CSV publics correspondants ;
5. vérifie les nombres de mémoires et les règles RX-only ;
6. vérifie que Normandie v0.3.1 n'est pas reconstruite par le générateur générique ;
7. contrôle séparément le CSV Normandie publié de 139 mémoires ;
8. vérifie à la fin qu'aucun fichier suivi n'a changé d'un octet.

Les sorties temporaires sont automatiquement supprimées à la fin du test.

## Comportement manuel

Sans `--output-root`, le générateur générique écrit toujours ses **sorties génériques planifiées** dans leurs emplacements publics normaux.

Il ne réécrit plus le pack régional versionné Normandie v0.3.1. Cette version ne doit évoluer que via une nouvelle release régionale explicite.

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

Le workflow GitHub Actions exécute cette étape sous le nom :

```text
Test CSV generator in isolated output
```

Le test garantit donc à la fois l'isolation locale et l'immuabilité des packs régionaux déjà publiés.
