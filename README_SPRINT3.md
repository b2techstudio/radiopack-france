# RadioPack France — Sprint 3

Ce patch fait passer le pack Normandie à la version **0.2.0**.

## Contenu

- 16 canaux PMR446 RX
- 90 mémoires VHF marine RX
- 6 mémoires APRS / ISS RX
- 10 mémoires aviation normande RX
- 122 mémoires dans le pack Normandie
- Générateur et tests mis à jour
- Pages Téléchargements et Normandie mises à jour

## Installation

Copier **le contenu** de ce dossier à la racine du dépôt :

```text
C:\Users\cross\Documents\CODE\PROJETS\RadioPack-France
```

Accepter la fusion et le remplacement des fichiers.

Le fichier existant `data/national/pmr446.json` n'est pas inclus dans le patch : il reste celui du Sprint 2.

## Génération et tests

```powershell
cd "C:\Users\cross\Documents\CODE\PROJETS\RadioPack-France"
python generator\generate_chirp_csv.py
python tests\test_generator.py
```

Résultat attendu :

```text
Tests RadioPack Sprint 3: OK
```

## Test du site

```powershell
cd website
npm run dev
```

Pages à vérifier :

- http://localhost:4321/telechargements
- http://localhost:4321/regions/normandie

## Git

```powershell
cd ..
git add .
git commit -m "Add Normandie v0.2 receive-only datasets"
git push
```
