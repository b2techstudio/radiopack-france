# Île-de-France v0.3 — release candidate interne

Travail ouvert le **21 août 2026** à partir de la **v0.2 publique immuable de 58 mémoires RX**.

Le dossier contient désormais un **release candidate interne déterministe de 57 mémoires RX**. Il n'est **pas encore publié** : la v0.2 publique reste inchangée, le publication record v0.3 n'est pas gelé et `publication_ready` reste à `false`.

## Radioamateur — scope final

Historique conservé dans :

- `radio-validation-2026-08-21.json` ;
- `radio-validation-pass2-2026-08-21.json` ;
- `radio-validation-pass3-2026-08-21.json`.

### Retenus dans le candidat

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
- **F1ZTC**, **F5ZDR**, **F5ZBK**, **F1ZDL** : exclus de cette v0.3 faute de preuve opérationnelle actuelle suffisante. Ils restent dans le backlog ; cette décision ne les déclare pas définitivement hors service.

Le bloc radio régional final contient **15 RF uniques**.

## Aviation — scope final AIRAC 08/26

Le candidat conserve les **18 mémoires aviation** déjà présentes dans la v0.2, sans expansion et avec un delta de **0**.

- **LFPG / Paris-CDG** : sous-ensemble retenu revalidé directement sur le SIA AIRAC 08/26 ;
- **LFPO / Paris-Orly** : catalogue COM SIA courant, matériel AD 2.18 officiel, SUP AIP **085/2026** et **147/2026** et revue NOTAM de la fenêtre courante utilisés pour valider le sous-ensemble retenu ;
- **LFPB / Paris-Le Bourget** : le NOTAM courant A2706/26 confirme les valeurs 8.33 kHz ATIS/GND/TWR/DEL retenues et le matériel SIA 2026 confirme **LE BOURGET INFO 123.835 MHz** ;
- aucune fréquence aviation supplémentaire n'est ajoutée dans cette v0.3.

Le détail final est dans `aviation-validation-pass4-2026-08-21.json`.

Cette validation est fraîche jusqu'au **2 septembre 2026 inclus**. Toute publication ou nouvelle validation effectuée à partir du **3 septembre 2026** doit être reprise sur **AIRAC 09/26**.

## Candidat déterministe

Fichiers :

- builder : `tools/build_idf_v03_candidate.py` ;
- CSV : `generated/release-candidate/radiopack-france-ile-de-france-v0.3-candidate.csv` ;
- manifeste : `generated/release-candidate/candidate-manifest.json`.

Le builder reconstruit d'abord la v0.2 à partir des sources du dépôt et exige son SHA-256 public figé :

`dbcadbcef403d7272dc374a7010def7276b06048a8e863277fcdb3558a8f624d`

Il construit ensuite la v0.3 en conservant les blocs nationaux et aviation et en remplaçant uniquement le bloc régional.

Résultat :

- **57 RX** au total ;
- **18 aviation** ;
- **15 radio régionales** ;
- SHA-256 candidat : `e04e6dbbf869661305068bac55cd8044abdcea7321d67e4c28111c9d057da125`.

## Gates

Fermés :

- conflits de sources radio ;
- comptage radio ;
- revalidation aviation pour le sous-ensemble retenu ;
- construction déterministe ;
- RX-only ;
- déduplication RF ;
- limite de 200 mémoires.

Encore ouvert :

- **gel du publication record v0.3** et revue finale de prépublication.

Tant que ce dernier gate n'est pas fermé, le candidat reste interne et aucun téléchargement public v0.3 n'est exposé.

## Règles permanentes

- RX uniquement : `Duplex=off`, `Offset=0.000000` ;
- maximum 200 mémoires ;
- paired RX pour les paires distinctes vérifiées ;
- déduplication RF ;
- aucun remplissage artificiel ;
- aucune fréquence ambiguë devinée ;
- une station insuffisamment corroborée peut être sortie du scope sans être déclarée définitivement inactive ;
- données privées, PPDR, chiffrées ou non publiquement vérifiables exclues ;
- v0.2 publique conservée immuable ;
- revalidation AIRAC obligatoire si la fenêtre de fraîcheur est franchie avant publication.
