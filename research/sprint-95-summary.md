# Sprint 95 — Annecy–Alpes–Léman v0.4 publiée

- Date : 2026-08-15
- Statut : **publiée et immuable**.
- Version complète : **77 RX** ; SHA-256 `2557076fcb198b830cd3b5ba64d7ff894c8e0d6e90eafc0fa40b691a3c6a5d98`.
- Sans aviation : **60 RX** ; SHA-256 `e31bfc6fce402af117b4f79caf6547b60a23c91ef36491e1351c74e96329aa6c`.
- Aviation : 17 ; delta depuis v0.3 : **+1 RF** (`ZTH-6M`, 50.5375 MHz).
- v0.3 reste immuable : 76 / 59 et ses empreintes historiques sont contrôlées par les tests.
- RX-only, Duplex=off, Offset=0.000000, déduplication RF, aucun remplissage artificiel, aucune RF privée/PPDR/ADRASEC non publiée.
- Registre, page régionale, générateur et métadonnées publiques pointent vers v0.4.
- Travail actif suivant : Bretagne v0.3, en attente de la revalidation AIRAC 09/26 à partir du 3 septembre 2026 ; Normandie v0.5 reste dépendante des validations terrain.

## Clôture

- SHA de publication propre avant clôture : `f9cc9e3cee59c3131782d78df4d095d4148cfa89`.
- RadioPack CI run 1012 (`31894796351`) : succès complet.
- Security Audit run 43 (`31894796228`) : succès complet, y compris la vérification HTTPS live de l'origine Cloudflare Pages déployée.
- Annecy v0.4 Guards run 23 (`31894796237`) : succès.
- Annecy v0.3 Release Guards run 76 (`31894796249`) : succès ; historique v0.3 préservé.
- Sprints 89-91 Guards run 49 (`31894796222`) : succès.
- Ce commit de clôture ajoute uniquement la traçabilité et déclenche l'archive de référence ; les CSV publics et leurs empreintes restent inchangés.
- Le SHA final, le run CI final et l'artefact de référence sont ceux produits par GitHub Actions après ce commit de clôture.
