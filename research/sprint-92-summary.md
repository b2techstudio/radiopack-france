# Sprint 92 — audit et durcissement sécurité

Date : 2026-08-15
État logique : **0.21.81**

## Résultat

- audit du frontend statique Astro, des dépendances, des workflows GitHub Actions, des secrets à signal fort, des redirections/downloads et du build de production ;
- alerte haute `nanoid 3.3.17` (`GHSA-2v37-7h3g-55p8`) corrigée vers `3.3.18` ;
- `npm audit --audit-level=low` et `pip-audit` verts ;
- 63 tests repository + build Astro verts ;
- CSP/HSTS/COOP et autres headers configurés ; JSON-LD échappé contre fermeture de script ;
- GitHub Actions épinglées par SHA, permissions réduites, checkout sans credentials persistants ;
- surveillance Dependabot hebdomadaire ajoutée ;
- domaine `radiopack.b2tech.studio` non résolvable depuis GitHub Actions lors du contrôle live, donc headers HTTP publics non certifiables à ce stade ;
- aucune mutation des CSV publics ni des fréquences RF.

Rapport complet : `research/security-audit-sprint92.md`.

## Réglages hors code restant à effectuer

- protéger la branche `main` ;
- activer Dependabot vulnerability alerts ;
- vérifier/activer Secret scanning, Push protection et Code scanning si disponibles.
