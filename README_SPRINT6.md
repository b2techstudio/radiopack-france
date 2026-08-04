# RadioPack France - Sprint 6

Ce patch prépare le site pour une exploitation publique plus propre sur Cloudflare Pages.

## Contenu

- URL canonique `https://radiopack.b2tech.studio`
- métadonnées Open Graph et Twitter
- données structurées JSON-LD
- manifeste web
- sitemap XML
- robots.txt
- page 404
- page `État des packs`
- menu mobile accessible
- bouton principal `Télécharger`
- en-têtes de sécurité Cloudflare
- redirections des anciens téléchargements Normandie
- GitHub Actions pour les tests Python et le build Astro

## Installation

Décompresser l'archive puis copier **tout son contenu** à la racine :

```text
C:\Users\cross\Documents\CODE\PROJETS\RadioPack-France
```

Accepter la fusion des dossiers et le remplacement des fichiers.

Tous les fichiers modifiés sont fournis en version complète.

## Tests locaux

Depuis la racine du projet :

```powershell
python tests\test_generator.py
python tests\test_site_files.py
```

Résultat attendu :

```text
Tests RadioPack Sprint 5: OK
Tests RadioPack Sprint 6: OK
```

Puis compiler le site :

```powershell
cd website
npm run build
npm run dev
```

Pages et fichiers à contrôler :

```text
http://localhost:4321/
http://localhost:4321/versions
http://localhost:4321/robots.txt
http://localhost:4321/sitemap.xml
http://localhost:4321/une-page-inexistante
```

## Publication

```powershell
cd ..
git add .
git commit -m "Add production SEO and CI checks"
git push
```

Le `git push` déclenche :

1. le workflow GitHub Actions ;
2. le déploiement automatique Cloudflare Pages.

Dans GitHub, l'onglet **Actions** doit afficher deux tâches vertes :

- `CSV and repository tests`
- `Astro production build`

Dans Cloudflare Pages, le nouveau déploiement doit utiliser le même commit.
