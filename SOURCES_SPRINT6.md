# Sources techniques - Sprint 6

Consultation : 4 août 2026.

## Astro

- Configuration de l'URL de production :
  https://docs.astro.build/fr/reference/configuration-reference/
- Création des URL canoniques avec `Astro.site` et `Astro.url` :
  https://docs.astro.build/fr/guides/configuring-astro/
- Recommandations de découverte du sitemap :
  https://docs.astro.build/fr/guides/integrations-guide/sitemap/

Le Sprint 6 génère directement `sitemap.xml` et `robots.txt` avec des routes Astro,
sans ajouter de dépendance au projet.

## Cloudflare Pages

- En-têtes personnalisés avec `public/_headers` :
  https://developers.cloudflare.com/pages/configuration/headers/
- Redirections avec `public/_redirects` :
  https://developers.cloudflare.com/pages/configuration/redirects/
- Page 404 personnalisée :
  https://developers.cloudflare.com/pages/configuration/serving-pages/

## GitHub Actions

- Checkout v6 :
  https://github.com/actions/checkout
- Setup Node v6 :
  https://github.com/actions/setup-node
- Setup Python v6 :
  https://github.com/actions/setup-python
