# RadioPack France - Sprint 4

Ce patch fait passer le pack Normandie a la version **0.3.1**.

## Nouveautes

- 2 canaux d'appel radioamateur en reception seule
- 15 relais ou voies de transpondeurs analogiques verifies
- 139 memoires organisees par plages fixes
- Guide PDF complet
- Export CSV separe des relais normands
- Generateur et tests compatibles avec les intervalles de memoires

## Installation

Copier **le contenu** de ce dossier a la racine :

```text
C:\Users\cross\Documents\CODE\PROJETS\RadioPack-France
```

Accepter la fusion et le remplacement des fichiers.

## Generer les CSV

```powershell
cd "C:\Users\cross\Documents\CODE\PROJETS\RadioPack-France"
python generator\generate_chirp_csv.py
python tests\test_generator.py
```

Resultat attendu :

```text
Tests RadioPack Sprint 4: OK
```

## Regenerer le PDF (facultatif)

Le PDF est deja inclus dans le patch. Pour le recreer :

```powershell
python -m pip install -r requirements-generator.txt
python generator\generate_pack_pdf.py
```

## Tester le site

```powershell
cd website
npm run dev
```

Verifier :

- http://localhost:4321/telechargements
- http://localhost:4321/regions/normandie

## Publier

```powershell
cd ..
git add .
git commit -m "Add Normandie v0.3.1 repeaters and PDF guide"
git push
```

## Correction Mont des Avaloirs

La mémoire 174 ajoute `53-F6ZCE` sur 145,700 MHz en NFM et réception seule.

Cette archive corrigée remplace l'archive Sprint 4 précédente.
