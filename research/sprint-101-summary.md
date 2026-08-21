# Sprint 101 — Île-de-France v0.3, deuxième passe

État logique : **0.21.90**

Le Sprint 101 poursuit officiellement la reprise **Île-de-France v0.3** à partir de la **v0.2 publique immuable de 58 mémoires RX**, dont 18 aviation. Le travail reste un checkpoint de recherche : **aucun CSV public, aucune version publiée et aucun SHA de publication ne sont modifiés**.

## Radioamateur

La deuxième passe porte le calcul de travail provisoire à **57 mémoires RX** si les blocs nationaux et aviation restent inchangés. Ce compteur n'est pas un release candidate.

Décisions désormais étayées :

- F5ZNG, F5ZNN, F5ZMH et F1ZHK restent dans la base de travail ;
- F5ZMR Provins et le crossband F5ZSY Issy-les-Moulineaux restent les nouveaux ajouts directs de la première passe ;
- F6ZEE Pontault-Combault reprend le même jeu RF 145.100 / 145.700 MHz que l'ancienne attribution F1ZSY, donc sans nouvelle mémoire RF nette ;
- le crossband F5ZNN 145.650 / 430.650 MHz est validé avec déduplication : seule 430.650 MHz ajoute une mémoire ;
- F5ZEQ n'est pas reconduit tant que son opérateur le signale hors service pour maintenance ;
- F5ZBK et F1ZDL restent en attente d'une seconde corroboration opérationnelle actuelle ;
- F1ZTC et F5ZDR restent différés.

## Aviation

AIRAC **08/26** reste applicable du **6 août au 2 septembre 2026 inclus**. Le sous-ensemble v0.2 de **18 mémoires aviation** reste inchangé dans le calcul provisoire, delta 0.

La page SIA eAIP AD 2.18 directement courante de **LFPG / Paris Charles-de-Gaulle** a permis de revalider les quatre fréquences APP déjà présentes en v0.2 : 118.155, 119.855, 121.155 et 124.355 MHz. Des fréquences APP supplémentaires actuelles ont été observées mais ne sont pas promues sans décision de périmètre et fermeture complète des gates.

Les validations directes AIRAC 08/26 de **LFPO / Paris-Orly** et **LFPB / Paris-Le Bourget**, ainsi que la revue NOTAM/SUP AIP applicable, restent ouvertes. Toute publication ou nouvelle validation à partir du **3 septembre 2026** devra être reprise sur **AIRAC 09/26**.

## État de publication

- compteur de travail provisoire : **57 RX** ;
- aviation provisoire : **18 RX**, delta 0 ;
- `release_candidate_memory_count` : **null** ;
- conflits radio entièrement fermés : **non** ;
- revalidation aviation complète : **non** ;
- publication v0.3 autorisée : **non**.

Le contrat public reste RX-only : `Duplex=off`, `Offset=0.000000`, paired RX pour les paires distinctes vérifiées, déduplication RF, aucun remplissage artificiel et aucune fréquence ambiguë devinée.

Références :

- `research/ile-de-france-v0.3/README.md` ;
- `research/ile-de-france-v0.3/radio-validation-2026-08-21.json` ;
- `research/ile-de-france-v0.3/radio-validation-pass2-2026-08-21.json` ;
- `research/ile-de-france-v0.3/aviation-airac08-2026-08-21.json` ;
- `research/ile-de-france-v0.3/aviation-validation-pass2-2026-08-21.json` ;
- `research/ile-de-france-v0.3/release-scope.json` ;
- `tests/test_idf_v03_research.py` ;
- `tests/test_sprint101_state_sync.py`.
