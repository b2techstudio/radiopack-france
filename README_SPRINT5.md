# RadioPack France - Sprint 5

Ce patch publie le premier pack **Annecy & Haute-Savoie v0.1.0**.

## Contenu

- 36 memoires en reception seule
- 16 PMR446
- 6 APRS / ISS
- 2 canaux d'appel radioamateur
- 3 frequences aviation
- 9 sorties analogiques uniques
- CSV regional
- CSV separe des relais
- Guide PDF
- Pages du site mises a jour
- Generateur et tests mis a jour

## Installation

Decompresser l'archive, puis copier **tout son contenu** a la racine :

```text
C:\Users\cross\Documents\CODE\PROJETS\RadioPack-France
```

Accepter la fusion des dossiers et le remplacement des fichiers.

Tous les fichiers modifies sont fournis en version complete.

## Generation et tests

```powershell
cd "C:\Users\cross\Documents\CODE\PROJETS\RadioPack-France"

python generator\generate_chirp_csv.py
python tests\test_generator.py
```

Resultat attendu :

```text
Tests RadioPack Sprint 5: OK
```

## Regenerer le guide PDF

Le PDF est deja inclus. Pour le recreer :

```powershell
python -m pip install -r requirements-generator.txt
python generator\generate_annecy_pdf.py
```

## Tester le site

```powershell
cd website
npm run dev
```

Verifier :

- http://localhost:4321/
- http://localhost:4321/regions
- http://localhost:4321/regions/annecy-haute-savoie
- http://localhost:4321/telechargements

## Publier

```powershell
cd ..
git add .
git commit -m "Add Annecy Haute-Savoie receive-only pack"
git push
```
