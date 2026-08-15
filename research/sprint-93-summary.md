# Sprint 93 — clôture sécurité live

- Date : 2026-08-15
- L'origine Cloudflare Pages déployée `https://radiopack-france.pages.dev/` est auditée en HTTPS par la CI.
- CSP, HSTS, X-Frame-Options, X-Content-Type-Options, COOP, Referrer-Policy et Permissions-Policy sont vérifiés.
- `radiopack.b2tech.studio` reste contrôlé séparément ; son absence de DNS n'empêche plus de certifier l'origine Pages réellement déployée.
- Les audits npm/Python, secrets, DOM-XSS, redirections, source maps et permissions Actions restent actifs.
- La protection de branche `main` reste un réglage GitHub externe non activé dans l'état observé.
