# Grand Est v0.3 — Sprint 102

Statut : **candidat interne construit — aucune mutation publique**.

Base publique immuable : **Grand Est v0.2 / 59 mémoires RX**.
SHA-256 public v0.2 : `a50416bd8a88af249bb691daa657ffd4b578daf1324bd0ca4dd632a2f1a0e5c1`.

## État du candidat

Le périmètre radio analogique non exhaustif a été fermé après trois passes de recherche :

- **41 fréquences RF régionales uniques** ;
- déduplication explicite de `432.5375 MHz`, partagée par plusieurs crossbands ;
- F1ZAX différé car le REF courant le classe C4FM sans preuve locale actuelle de voix FM analogique ;
- F5ZBD exclu tant qu'il est signalé hors service / en mise à niveau ;
- F1ZBU exclu du périmètre analogique car son service courant est numérique ;
- les autres dossiers insuffisamment corroborés restent explicitement différés.

Un candidat déterministe interne est maintenant figé à **84 mémoires RX** :

- 43 mémoires non régionales héritées de la base v0.2 ;
- 19 mémoires aviation AIRAC 08/26 incluses dans ces 43 ;
- 41 mémoires radio régionales ;
- SHA-256 candidat : `45aef8547a701e7541e620fa9a2d8394595576921e793b75238146ff6e42e720`.

Le builder reconstruit d'abord la v0.2 et refuse de poursuivre si son SHA historique ne correspond pas. Le candidat reste `public_export_allowed=false` : aucune v0.3 publique n'existe encore.

## Prochaine gate

L'aviation doit être revalidée sur le cycle courant avant toute décision de publication. Le cycle AIRAC 08/26 reste applicable jusqu'au **2 septembre 2026 inclus**. Toute révision effectuée le **3 septembre 2026 ou après** doit repartir sur AIRAC 09/26.

Après l'aviation viennent la checklist de revue et les publication gates. Aucune mutation du registre ou du CSV public n'est autorisée avant leur fermeture.

## Règles

- réception uniquement ;
- `Duplex=off` ;
- `Offset=0.000000` ;
- paired RX pour chaque paire distincte vérifiée ;
- déduplication par fréquence RF ;
- maximum 200 mémoires ;
- pas d'inférence de fréquence ou de mode manquant ;
- pas de données opérationnelles privées / PPDR ;
- versions publiques déjà publiées immuables.

## Fichiers du Sprint 102

- `radio-validation-pass1-2026-08-22.json` : audit radio initial ;
- `radio-validation-pass2-2026-08-22.json` : seconde-source et déduplication ;
- `radio-validation-pass3-2026-08-22.json` : fermeture du scope radio ;
- `backlog.json` : différés et exclusions ;
- `release-scope.json` : état courant et gates ;
- `generated/release-candidate/` : candidat CSV + manifeste figés ;
- `tools/build_grand_est_v03_candidate.py` : reconstruction déterministe ;
- `tests/test_grand_est_v03_*.py` : garde-fous ;
- `.github/workflows/grand-est-v03-research.yml` : CI dédiée.
