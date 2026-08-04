# RadioPack France — Sprint 1

Ce pack contient la première version du site Astro : page d'accueil, régions, Normandie, Annecy / Haute-Savoie, téléchargements, documentation et à propos.

## Installation dans le projet Astro déjà créé

1. Fermer le serveur Astro s'il tourne (`Ctrl+C`).
2. Décompresser ce ZIP.
3. Copier les dossiers `src` et `public` dans le dossier `website` créé avec Astro.
4. Accepter le remplacement des fichiers existants.
5. Dans PowerShell :

```powershell
cd C:\Users\cross\Documents\CODE\PROJETS\RadioPack-France\website
npm run dev
```

6. Ouvrir `http://localhost:4321`.

## Git

Depuis le dossier racine `RadioPack-France` :

```powershell
git init
git add .
git commit -m "feat: initial RadioPack France website"
git branch -M main
git remote add origin https://github.com/b2techstudio/radiopack-france.git
git push -u origin main
```

Si `origin` existe déjà, ne pas relancer la commande `git remote add origin`.

## Design

La première version utilise du CSS Astro natif, sans dépendance UI supplémentaire. Le fond est volontairement clair / gris bleuté, avec les couleurs B2Tech Studio (violet, bleu, orange) en accents.
