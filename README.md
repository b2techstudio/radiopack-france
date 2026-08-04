# RadioPack France

Codeplugs CHIRP régionaux, documentés et générés à partir de données publiques vérifiables pour les radios Quansheng UV-K5.

## Sprint 2

Cette version ajoute :

- une architecture de données JSON évolutive ;
- un générateur CSV CHIRP sans dépendance externe ;
- le jeu national PMR446 analogique 16 canaux ;
- un premier aperçu Normandie ;
- des exports configurés en réception seule ;
- les premières pages de téléchargement réellement fonctionnelles.

## Générer les CSV

Depuis la racine du dépôt :

```powershell
python generator/generate_chirp_csv.py
```

Tester le générateur :

```powershell
python tests/test_generator.py
```

## Lancer le site

```powershell
cd website
npm install
npm run dev
```

## Déploiement

Le dépôt est connecté à Cloudflare Pages. Un `git push` sur `main` déclenche automatiquement un nouveau déploiement.

## Sécurité

Les premiers exports sont volontairement en réception seule. Voir [NOTICE_LEGAL.md](NOTICE_LEGAL.md).
