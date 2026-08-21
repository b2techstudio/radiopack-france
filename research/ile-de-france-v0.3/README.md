# Île-de-France v0.3 — checkpoint de recherche

Checkpoint ouvert le **21 août 2026** à partir de la **v0.2 publique immuable de 58 mémoires RX**.

Ce dossier ne constitue **pas encore** un candidat de publication. Aucun CSV public n'est modifié. Après trois passes, le **scope radio est finalisé pour cette reprise** ; l'aviation reste le seul gate de release.

## Radioamateur — troisième passe

Historique conservé dans :

- `radio-validation-2026-08-21.json` ;
- `radio-validation-pass2-2026-08-21.json` ;
- `radio-validation-pass3-2026-08-21.json`.

### Retenus dans le scope courant

- **F5ZNG Provins** — 145.625 / 145.025 MHz ;
- **F5ZNN Saint-Rémy-la-Vanne** — 145.650 / 145.050 MHz ;
- **F5ZMH Linas** — 145.7375 / 145.1375 MHz ;
- **F1ZHK Nangis** — 145.7625 / 145.1625 MHz ;
- **F6ZEE Pontault-Combault** — 145.100 / 145.700 MHz, même jeu RF que l'ancienne attribution F1ZSY ;
- **F5ZMR Provins** — 431.525 / 439.125 MHz ;
- **F5ZSY Issy-les-Moulineaux** — crossband 145.325 / 430.325 MHz ;
- **F5ZNN crossband** — 145.650 / 430.650 MHz, avec déduplication : seule **430.650 MHz** ajoute une mémoire.

### Non reconduits dans ce scope

- **F5ZAD**, **F1ZUX** : non reconduits depuis les passes précédentes ;
- **F1ZSY** : ancienne attribution remplacée par F6ZEE sur le même jeu RF ;
- **F5ZEQ** : non reconduit tant que l'opérateur le signale hors service pour maintenance ;
- **F1ZTC**, **F5ZDR**, **F5ZBK**, **F1ZDL** : exclus de cette v0.3 faute de preuve opérationnelle actuelle suffisante. Ils restent dans le backlog et pourront être réévalués plus tard ; cette décision ne prétend pas qu'ils sont définitivement hors service.

### Comptage radio final du scope

Si les **18 mémoires aviation** restent inchangées :

`58 - 8 + 2 + 4 + 1 = 57`

Le **57** est désormais le compteur de travail radio final pour ce scope, mais **pas encore un release candidate** car l'aviation n'est pas fermée.

## Aviation — troisième passe AIRAC 08/26

AIRAC **08/26** est courant du **6 août au 2 septembre 2026 inclus**. Le bloc aviation reste provisoirement à **18 mémoires, delta 0**.

- **LFPG / Paris-CDG** : les quatre APP v0.2 118.155, 119.855, 121.155 et 124.355 MHz sont revalidées directement sur le SIA du cycle courant ;
- **LFPO / Paris-Orly** : le matériel COM SIA officiel récent contient les huit fréquences v0.2. Les SUP AIP **085/2026** et **147/2026** sont actifs et concernent les procédures temporaires ainsi que les travaux de la piste 06/24 ;
- **LFPB / Paris-Le Bourget** : le matériel SIA officiel de juin/juillet 2026 confirme les cinq fréquences v0.2 ;
- la preuve directe AIRAC 08/26 LFPO/LFPB et la revue NOTAM/SUP complète restent nécessaires avant de figer un delta RF aviation à zéro.

Le détail est dans `aviation-validation-pass3-2026-08-21.json`.

Toute publication ou nouvelle validation effectuée à partir du **3 septembre 2026** devra être reprise sur **AIRAC 09/26**.

## Gates de publication restant ouverts

- revalidation autoritative de cycle courant LFPO ;
- revalidation autoritative de cycle courant LFPB ;
- revue NOTAM LFPG/LFPO/LFPB ;
- revue SUP AIP suffisante, notamment l'activation des phases du SUP 147/2026 ;
- construction et validation du candidat déterministe après fermeture du gate aviation.

## Règles permanentes

- RX uniquement : `Duplex=off`, `Offset=0.000000` ;
- maximum 200 mémoires ;
- paired RX pour les paires distinctes vérifiées ;
- déduplication RF ;
- aucun remplissage artificiel ;
- aucun état, mode ou fréquence ambigu ne doit être deviné ;
- une station insuffisamment corroborée peut être sortie du scope sans être déclarée définitivement inactive ;
- données privées, PPDR, chiffrées ou non publiquement vérifiables exclues ;
- v0.2 publique conservée immuable ;
- publication v0.3 interdite tant que le gate aviation n'est pas fermé.
