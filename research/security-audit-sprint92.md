# Sprint 92 — audit de sécurité RadioPack France

Date : 2026-08-15  
Cible : dépôt `b2techstudio/radiopack-france`, site statique Astro / Cloudflare Pages  
État : audit technique pré-fusion terminé ; contrôle HTTP réel prévu automatiquement après fusion sur `main`.

## Conclusion

Aucune compromission active ni vulnérabilité applicative critique n'a été identifiée dans le code audité. Une vulnérabilité **haute** de chaîne de dépendances a en revanche été détectée par le nouvel audit npm : `nanoid 3.3.17` était affecté par `GHSA-2v37-7h3g-55p8`. Le lockfile a été régénéré avec la version corrigée `3.3.18`, puis `npm audit --audit-level=low` a été rejoué avec succès.

Le site reste un site **statique** : ce dépôt ne contient ni API serveur publique, ni base de données, ni authentification, ni session applicative. Cela supprime de la surface d'attaque plusieurs familles classiques côté serveur, mais ne dispense pas de protéger le navigateur, la chaîne de build, GitHub Actions et le déploiement Cloudflare.

## Surface analysée

- code Astro, TypeScript et JavaScript côté navigateur ;
- construction du générateur de téléchargement et URLs de CSV ;
- redirections Cloudflare Pages ;
- en-têtes HTTP de sécurité ;
- production JSON-LD et usages `set:html` ;
- dépendances npm et Python ;
- lockfile npm et intégrité des dépendances ;
- GitHub Actions, permissions du `GITHUB_TOKEN`, actions tierces et checkout ;
- recherche à signal fort de clés privées, tokens GitHub, clés AWS et fichiers `.env` ;
- présence éventuelle de source maps dans le build public ;
- conservation des 63 tests fonctionnels historiques et du build Astro ;
- contrôle HTTP réel de `https://radiopack.b2tech.studio/` après intégration sur `main`.

## Résultats par sévérité

### Haute — corrigée : dépendance npm `nanoid`

Le premier `npm audit` a détecté `nanoid 3.3.17`, vulnérable selon `GHSA-2v37-7h3g-55p8` (plage affectée terminant à 3.3.17). La remédiation a été appliquée au seul lockfile, qui résout maintenant `nanoid 3.3.18` avec une nouvelle empreinte d'intégrité. Le nouvel audit npm complet passe au niveau `low`, donc sans alerte connue remontée par npm dans le graphe verrouillé au moment de l'audit.

### Moyenne — corrigée : chaîne GitHub Actions

Avant Sprint 92 :

- les actions `checkout`, `setup-python`, `setup-node` et `upload-artifact` étaient appelées par tags de version ;
- le workflow principal accordait `statuses: write` globalement ;
- les checkouts conservaient les credentials Git par défaut.

Après Sprint 92 :

- toutes les actions utilisées par les workflows permanents sont épinglées sur un SHA Git complet ;
- les jobs ordinaires restent à `contents: read` ;
- `statuses: write` est limité au seul job qui publie le statut combiné ;
- `persist-credentials: false` est imposé à tous les checkouts permanents ;
- `pull_request_target` et les permissions générales d'écriture sont interdits par test.

### Moyenne — corrigée : protection navigateur / injection

Les réponses Cloudflare sont désormais préparées avec :

- `Content-Security-Policy` ;
- `Strict-Transport-Security` ;
- `X-Frame-Options: DENY` ;
- `X-Content-Type-Options: nosniff` ;
- `Referrer-Policy` ;
- `Permissions-Policy` ;
- `Cross-Origin-Opener-Policy: same-origin` ;
- `X-Permitted-Cross-Domain-Policies: none`.

La CSP limite par défaut les ressources à la même origine, refuse les objets et l'intégration en frame, limite les formulaires à la même origine et demande la mise à niveau HTTPS. Les styles/scripts inline restent autorisés pour compatibilité avec le build Astro actuel ; ce point est documenté dans les risques résiduels.

Le seul `set:html` attendu est le JSON-LD du layout principal. Sa sérialisation échappe désormais explicitement le caractère `<` avant injection dans le bloc `application/ld+json`, empêchant une future valeur contrôlée par le projet de fermer le tag `script`.

### Faible à moyenne — corrigée : garde-fous frontend et navigation

Un test déterministe rejette désormais :

- `innerHTML =` ;
- `outerHTML =` ;
- `insertAdjacentHTML()` ;
- `document.write()` ;
- `eval()` ;
- `new Function()` ;
- les URLs `javascript:` ;
- les liens `target=_blank` sans `noopener` ou `noreferrer` ;
- les destinations de redirection externes / de type open redirect ;
- les URLs de téléchargement publiques qui ne sont pas sous `/downloads/` sur la même origine.

Aucun de ces sinks interdits n'est présent dans le frontend actuel.

### Faible à moyenne — corrigée : détection accidentelle de secrets

Le garde-fou rejette les fichiers sensibles suivis par Git tels que `.env`, clés privées/certificats et quelques formats de credentials usuels. Il recherche également les signatures de clés privées, tokens GitHub classiques / fine-grained et clés d'accès AWS dans les sources texte suivies. Aucun résultat correspondant à ces signatures n'a été trouvé pendant l'audit.

Cette vérification locale ne remplace pas le secret scanning de l'hébergeur sur l'historique Git complet.

## Tests exécutés sur la PR d'audit

Sur le HEAD de la branche après remédiation de `nanoid` et suppression du workflow temporaire :

- `Repository security invariants` : **SUCCESS** ;
- compilation Python `generator/`, `tools/`, `tests/` : **SUCCESS** ;
- `pip-audit` sur `requirements-generator.txt` : **SUCCESS** ;
- `npm audit --audit-level=low` : **SUCCESS** ;
- build Astro production : **SUCCESS** ;
- absence de fichiers `*.map` dans `dist` : **SUCCESS** ;
- présence de `_headers`, `_redirects`, CSP et HSTS dans `dist` : **SUCCESS** ;
- CI fonctionnelle : **63/63 contrôles de données/dépôt + build Astro SUCCESS** ;
- garde Annecy v0.3 : **SUCCESS** ;
- garde Sprints 89–91 : **SUCCESS**.

Le workflow `Security Audit` reste permanent et s'exécute sur push/PR, manuellement et chaque lundi. Le contrôle du site réellement servi est ignoré sur les PR et exécuté sur `main`/manuel/planifié afin de vérifier que Cloudflare expose réellement les en-têtes attendus.

## Surveillance des dépendances

`.github/dependabot.yml` a été ajouté pour proposer chaque semaine les mises à jour npm, pip et GitHub Actions. Il s'agit d'une surveillance de versions ; le réglage GitHub **Dependabot vulnerability alerts** reste une option de dépôt distincte.

## Risques résiduels / réglages hors code

### 1. Branche `main` non protégée — à corriger dans les réglages GitHub

Au moment de l'audit, l'API du dépôt signale `main` comme non protégée. Une personne ou un token disposant d'un droit de push pourrait donc contourner une PR et pousser directement. Le code de Sprint 92 ne peut pas imposer ce réglage avec les capacités actuellement disponibles.

Recommandation : protéger `main`, exiger les checks CI et Security Audit, empêcher les force-push et suppressions, et préférer les PR pour toute modification.

### 2. Dependabot vulnerability alerts désactivé — à activer dans les réglages GitHub

L'endpoint GitHub des alertes Dependabot a répondu explicitement que les alertes étaient désactivées pour ce dépôt. Le fichier `dependabot.yml` n'active pas ce réglage de sécurité à lui seul.

Recommandation : activer les **Dependabot alerts** (et les security updates si souhaité) dans les réglages Security du dépôt.

### 3. Secret scanning / code scanning — état non vérifiable avec l'intégration actuelle

Les endpoints correspondants ne sont pas accessibles au connecteur utilisé pendant cet audit. Leur état est donc **non confirmé** ; aucune conclusion « activé » ou « désactivé » n'est tirée.

Recommandation : vérifier dans GitHub > Settings > Security que Secret scanning / Push protection et Code scanning sont activés lorsqu'ils sont disponibles pour le dépôt.

### 4. CSP encore compatible avec les scripts/styles inline

La CSP contient `script-src 'self' 'unsafe-inline'` et `style-src 'self' 'unsafe-inline'` parce que le build Astro actuel émet du code inline. Cette politique reste nettement plus restrictive que l'absence de CSP, mais une CSP basée sur hashes/nonces serait plus forte contre certaines injections HTML futures.

Recommandation future : supprimer progressivement `unsafe-inline` si la chaîne de build permet des hashes/nonces stables sans casser les pages.

## Ce que cet audit ne promet pas

Aucun audit ne peut garantir qu'un site est « impossible à hacker ». Cet audit établit qu'au 15 août 2026 :

- aucune faille critique exploitable n'a été trouvée dans la surface examinée ;
- la vulnérabilité haute détectée dans les dépendances a été corrigée ;
- les contrôles préventifs les plus importants pour ce site statique sont automatisés ;
- les régressions fonctionnelles existantes restent vertes ;
- les risques résiduels connus sont explicitement documentés plutôt que masqués.

## Fichiers de contrôle permanents

- `.github/workflows/security-audit.yml`
- `.github/dependabot.yml`
- `tests/test_security_hardening.py`
- `website/public/_headers`
- `website/src/layouts/BaseLayout.astro`
- `.github/workflows/ci.yml`
- `.github/workflows/annecy-v03-guards.yml`
- `.github/workflows/sprints89-91-guards.yml`
- `research/security-audit-sprint92.md`
