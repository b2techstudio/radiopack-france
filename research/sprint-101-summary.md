# Sprint 101 — ouverture Île-de-France v0.3

État logique : **0.21.90**

Le Sprint 101 ouvre officiellement la reprise **Île-de-France v0.3** à partir de la **v0.2 publique immuable de 58 mémoires RX**, dont 18 aviation. Ce sprint est un checkpoint de recherche : **aucun CSV public, aucune version publiée et aucun SHA de publication ne sont modifiés**.

La première revue radioamateur conserve F5ZNG, F5ZNN, F5ZMH et F1ZHK comme base de travail, promeut F5ZMR Provins et le transpondeur crossband F5ZSY Issy-les-Moulineaux comme nouveaux candidats fortement étayés, ne reconduit pas automatiquement F5ZAD et F1ZUX, et maintient les dossiers conflictuels ou incomplets dans les gates documentés.

L'aviation reste sur **AIRAC 08/26 jusqu'au 2 septembre 2026 inclus**. La revue complète AD 2.18 et NOTAM/SUP AIP n'est pas encore fermée et aucune modification RF aviation n'est promue. Toute publication ou nouvelle validation à partir du **3 septembre 2026** devra être reprise sur **AIRAC 09/26**.

Le contrat public reste RX-only : `Duplex=off`, `Offset=0.000000`, paired RX pour les paires distinctes vérifiées, déduplication RF, aucun remplissage artificiel et aucune fréquence ambiguë devinée.

Références :

- `research/ile-de-france-v0.3/README.md` ;
- `research/ile-de-france-v0.3/radio-validation-2026-08-21.json` ;
- `research/ile-de-france-v0.3/aviation-airac08-2026-08-21.json` ;
- `research/ile-de-france-v0.3/release-scope.json` ;
- `tests/test_idf_v03_research.py`.
