# RadioPack France — Sprint 7

Ce correctif retire l'aperçu Annecy v0.1 du catalogue public et prépare la reconstruction Annecy–Alpes–Léman v0.2.

## État vérifié avant correction

- Branche par défaut : `main`
- Dernier commit observé : `7585d0274b3609f5723d19f27a1c22c0be355bbc`
- Message : `Add production SEO and CI checks`
- Le Sprint 6 est donc bien présent sur GitHub.
- Le connecteur GitHub utilisé pour la vérification dispose d'un accès en lecture, sans droit de push ; ce correctif est livré sous forme d'archive à fusionner localement.

## Effet public du correctif

- Normandie v0.3.1 reste le seul pack régional téléchargeable.
- Annecy v0.1 n'est plus qualifié de bêta disponible.
- Les liens directs Annecy v0.1 sont retirés de l'accueil, de la fiche région, des téléchargements et de la page des versions.
- La route historique `/regions/annecy-haute-savoie` reste stable, mais sa page présente désormais Annecy–Alpes–Léman v0.2 comme en préparation.
- Les anciens fichiers v0.1 ne sont pas supprimés du dépôt : ils restent historiques, sans promotion publique.

## Installation

Décompresser l'archive puis copier tout son contenu à la racine du projet :

```text
C:\Users\cross\Documents\CODE\PROJETS\RadioPack-France
```

Accepter la fusion des dossiers et le remplacement des fichiers.

## Tests

Depuis la racine :

```powershell
python generator\generate_chirp_csv.py
python tests\test_generator.py
python tests\test_site_files.py
```

Résultats attendus :

```text
Tests RadioPack Sprint 5: OK
Tests RadioPack Sprint 7: OK
```

Puis :

```powershell
cd website
npm run build
npm run dev
```

Contrôler :

```text
http://localhost:4321/
http://localhost:4321/regions
http://localhost:4321/regions/annecy-haute-savoie
http://localhost:4321/telechargements
http://localhost:4321/versions
```

Vérifications visuelles :

- l'accueil indique 1 pack disponible et 1 pack en reconstruction ;
- Annecy–Alpes–Léman porte le statut « En préparation » ;
- aucun bouton ne télécharge directement Annecy v0.1 ;
- Normandie reste téléchargeable ;
- le menu mobile et les éléments SEO du Sprint 6 restent présents.

## Git

```powershell
cd "C:\Users\cross\Documents\CODE\PROJETS\RadioPack-France"
git status
git add .
git commit -m "Reclassify Annecy v0.1 and prepare Alps Leman v0.2"
git push
```

Après le `git push`, GitHub Actions et Cloudflare Pages doivent se redéployer automatiquement.
