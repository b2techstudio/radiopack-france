# Sprint 101 — Île-de-France v0.3, candidat déterministe

État logique : **0.21.90**

Le Sprint 101 a désormais construit le premier **release candidate interne déterministe Île-de-France v0.3** à partir de la **v0.2 publique immuable de 58 mémoires RX**. La v0.2 publique n'est pas modifiée et la v0.3 n'est pas encore publiée.

## Candidat

Le candidat contient **57 mémoires RX** :

- **24 mémoires nationales** reprises à l'identique depuis les datasets source du dépôt ;
- **18 mémoires aviation** conservées sans expansion ;
- **15 mémoires radio régionales** issues du scope radio finalisé au Sprint 101.

SHA-256 du candidat : `e04e6dbbf869661305068bac55cd8044abdcea7321d67e4c28111c9d057da125`.

Le builder `tools/build_idf_v03_candidate.py` reconstruit d'abord la v0.2 depuis les sources du dépôt et refuse de poursuivre si le résultat ne correspond pas au SHA public figé `dbcadbcef403d7272dc374a7010def7276b06048a8e863277fcdb3558a8f624d`. Il construit ensuite la v0.3 en conservant les blocs nationaux et aviation et en remplaçant uniquement le bloc régional.

## Radioamateur

Le scope radio est final pour ce candidat :

- F5ZNG, F5ZNN, F5ZMH et F1ZHK sont conservés ;
- F6ZEE reprend le jeu RF 145.100 / 145.700 MHz de l'ancienne attribution F1ZSY ;
- F5ZMR et F5ZSY sont ajoutés ;
- le crossband F5ZNN ajoute uniquement 430.650 MHz après déduplication ;
- F5ZEQ n'est pas reconduit tant que l'opérateur le donne en maintenance ;
- F1ZTC, F5ZDR, F5ZBK et F1ZDL restent hors du scope de ce candidat faute de preuve opérationnelle actuelle suffisante, sans être déclarés définitivement hors service.

Le bloc régional final compte **15 RF uniques**. `radio_source_conflicts_closed = true` et `radio_memory_accounting_final = true` pour le scope courant.

## Aviation — AIRAC 08/26

La revalidation aviation est fermée **pour le sous-ensemble de publication retenu de 18 mémoires**, sans prétendre constituer un catalogue aviation exhaustif et sans ajouter de nouvelles fréquences.

- **LFPG / Paris-CDG** : le sous-ensemble retenu a été directement revalidé sur le SIA AIRAC 08/26 ;
- **LFPO / Paris-Orly** : le catalogue COM SIA courant, le matériel AD 2.18 officiel, les SUP AIP 085/2026 et 147/2026 et la revue NOTAM de la fenêtre courante convergent sans faire apparaître de changement affectant le sous-ensemble retenu ;
- **LFPB / Paris-Le Bourget** : le NOTAM courant A2706/26 confirme les valeurs 8.33 kHz ATIS/GND/TWR/DEL retenues, et le matériel SIA 2026 confirme LE BOURGET INFO 123.835 MHz.

La décision finale de ce scope aviation est donc **18 mémoires, delta 0**. Le gate aviation est fermé pour une publication effectuée au plus tard le **2 septembre 2026 inclus**. Toute publication ou nouvelle validation à partir du **3 septembre 2026** exige une revalidation AIRAC 09/26.

## Garde-fous du candidat

Les tests vérifient :

- reconstruction exacte de la v0.2 et concordance avec son SHA public figé ;
- reconstruction byte-à-byte du CSV candidat et concordance avec son manifeste ;
- 57 mémoires exactement ;
- 18 aviation et 15 radio régionales ;
- RX-only : `Duplex=off`, `Offset=0.000000` ;
- fréquences, noms et emplacements CHIRP uniques ;
- déduplication RF ;
- limite de 200 mémoires respectée.

## État de publication

- candidat déterministe construit : **oui** ;
- radio finalisée : **oui** ;
- aviation finalisée pour AIRAC 08/26 et le sous-ensemble retenu : **oui** ;
- `release_candidate_memory_count` : **57** ;
- publication record gelé : **non** ;
- CSV public v0.3 publié : **non** ;
- `publication_ready` : **false**.

La prochaine étape est la prépublication : revue finale, gel du publication record et vérification que le SHA du futur CSV public correspond exactement au candidat avant toute mutation du registre ou du téléchargement public.

Références :

- `research/ile-de-france-v0.3/radio-validation-pass3-2026-08-21.json` ;
- `research/ile-de-france-v0.3/aviation-validation-pass4-2026-08-21.json` ;
- `research/ile-de-france-v0.3/release-scope.json` ;
- `research/ile-de-france-v0.3/generated/release-candidate/candidate-manifest.json` ;
- `research/ile-de-france-v0.3/generated/release-candidate/radiopack-france-ile-de-france-v0.3-candidate.csv` ;
- `tools/build_idf_v03_candidate.py` ;
- `tests/test_idf_v03_candidate.py` ;
- `tests/test_sprint101_state_sync.py`.
