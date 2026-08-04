# Installation du Sprint 2

Le ZIP est conçu pour être fusionné avec la racine locale du dépôt `RadioPack-France`.

## 1. Copier les fichiers

1. Arrêter le serveur Astro avec `Ctrl+C`.
2. Décompresser le ZIP.
3. Copier tout le contenu du dossier `radiopack-france-sprint2` dans :

```text
C:\Users\cross\Documents\CODE\PROJETS\RadioPack-France
```

4. Accepter la fusion et le remplacement des fichiers.

## 2. Générer et vérifier les CSV

Depuis la racine du dépôt :

```powershell
python generator/generate_chirp_csv.py
python tests/test_generator.py
```

Le résultat attendu se termine par :

```text
Tests RadioPack Sprint 2: OK
```

## 3. Vérifier le site localement

```powershell
cd website
npm run dev
```

Ouvrir `http://localhost:4321/telechargements` et tester les deux boutons CSV.

## 4. Publier

Depuis la racine :

```powershell
git add .
git commit -m "Add RadioPack data and CSV generator"
git push
```

Cloudflare Pages redéploiera automatiquement le site.
