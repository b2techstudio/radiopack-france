# Sprint 101 — Île-de-France v0.3, troisième passe

État logique : **0.21.90**

Le Sprint 101 poursuit officiellement la reprise **Île-de-France v0.3** à partir de la **v0.2 publique immuable de 58 mémoires RX**, dont 18 aviation. Aucun CSV public, aucune version publiée et aucun SHA de publication ne sont modifiés.

## Radioamateur — scope final de cette reprise

Le calcul radio est désormais figé pour le scope courant : **57 mémoires RX si le bloc aviation reste à 18**.

Les décisions validées des passes précédentes sont conservées : F5ZNG, F5ZNN, F5ZMH et F1ZHK ; F6ZEE reprend le jeu RF 145.100 / 145.700 MHz de l'ancienne attribution F1ZSY ; F5ZMR et F5ZSY sont ajoutés ; le crossband F5ZNN ajoute uniquement 430.650 MHz après déduplication ; F5ZEQ reste non reconduit tant que l'opérateur le donne en maintenance.

Les quatre derniers dossiers ne bloquent plus cette publication : **F1ZTC, F5ZDR, F5ZBK et F1ZDL sont exclus du scope v0.3 courant faute de preuve opérationnelle actuelle suffisante**, sans affirmation de fermeture définitive. Ils restent dans le backlog pour une future revalidation.

Conséquence : `radio_source_conflicts_closed = true` et `radio_memory_accounting_final = true` pour le scope de release courant.

## Aviation — seul verrou restant

AIRAC **08/26** reste applicable du **6 août au 2 septembre 2026 inclus**. Le bloc aviation de travail reste à **18 mémoires, delta 0**.

- **LFPG / Paris-CDG** : le sous-ensemble v0.2 est directement revalidé sur le SIA courant ;
- **LFPO / Paris-Orly** : le matériel COM SIA officiel récent contient toutes les fréquences v0.2. Les SUP AIP 085/2026 et 147/2026 sont actifs et concernent les procédures temporaires / travaux de la piste 06/24 ;
- **LFPB / Paris-Le Bourget** : le matériel SIA officiel de juin/juillet 2026 confirme les cinq fréquences du sous-ensemble v0.2.

La publication reste néanmoins bloquée : la preuve statique directe AIRAC 08/26 de LFPO/LFPB et surtout la revue **NOTAM/SUP applicable**, dont l'activation des phases du SUP 147/2026, ne sont pas encore suffisamment closes pour geler un delta RF à zéro.

Toute publication ou nouvelle validation à partir du **3 septembre 2026** devra être reprise sur **AIRAC 09/26**.

## État de publication

- compteur de travail : **57 RX** si aviation inchangée ;
- radio : **scope final / comptage final** ;
- aviation : **18 RX provisoires, delta 0** ;
- `release_candidate_memory_count` : **null** ;
- revalidation aviation complète : **non** ;
- candidat déterministe construit : **non** ;
- publication v0.3 autorisée : **non**.

Le contrat public reste RX-only : `Duplex=off`, `Offset=0.000000`, paired RX pour les paires distinctes vérifiées, déduplication RF, aucun remplissage artificiel et aucune fréquence ambiguë devinée.

Références :

- `research/ile-de-france-v0.3/radio-validation-pass3-2026-08-21.json` ;
- `research/ile-de-france-v0.3/aviation-validation-pass3-2026-08-21.json` ;
- `research/ile-de-france-v0.3/release-scope.json` ;
- `tests/test_idf_v03_research.py` ;
- `tests/test_sprint101_state_sync.py`.
