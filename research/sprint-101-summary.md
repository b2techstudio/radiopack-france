# Sprint 101 — Île-de-France v0.3, prépublication prête

État logique : **0.21.90**

Le Sprint 101 dispose désormais d'un **release candidate interne déterministe Île-de-France v0.3 de 57 RX** et d'un bundle de prépublication complet. La **v0.2 publique de 58 RX reste immuable** et aucune mutation publique v0.3 n'est encore effectuée.

## Candidat figé

Le candidat contient :

- **24 mémoires nationales** reprises depuis les datasets source du dépôt ;
- **18 mémoires aviation** conservées sans expansion ;
- **15 mémoires radio régionales** ;
- total : **57 RX**.

SHA-256 candidat : `e04e6dbbf869661305068bac55cd8044abdcea7321d67e4c28111c9d057da125`.

Le builder `tools/build_idf_v03_candidate.py` reconstruit d'abord la v0.2 et exige le SHA public figé `dbcadbcef403d7272dc374a7010def7276b06048a8e863277fcdb3558a8f624d`, puis reconstruit la v0.3 et la compare byte-à-byte au candidat gelé.

## Radioamateur

Le scope radio est final pour cette v0.3 : F5ZNG, F5ZNN, F5ZMH, F1ZHK, F6ZEE, F5ZMR, F5ZSY et l'extension crossband dédupliquée F5ZNN constituent le bloc retenu. F5ZEQ reste non reconduit pendant sa maintenance ; F1ZTC, F5ZDR, F5ZBK et F1ZDL restent hors scope faute de preuve opérationnelle actuelle suffisante, sans déclaration de fermeture définitive.

Le bloc régional final compte **15 RF uniques**. Les conflits radio et le comptage sont fermés pour le scope courant.

## Aviation — AIRAC 08/26

Le sous-ensemble aviation retenu est finalisé à **18 mémoires, delta 0**, sans expansion :

- **LFPG** revalidé directement sur le SIA AIRAC 08/26 ;
- **LFPO** revalidé pour le sous-ensemble retenu avec le catalogue COM SIA courant, le matériel AD 2.18 officiel, les SUP AIP 085/2026 et 147/2026 et la revue NOTAM courante ;
- **LFPB** revalidé avec le NOTAM courant A2706/26 pour les valeurs ATIS/GND/TWR/DEL et le matériel SIA 2026 pour INFO 123.835 MHz.

Cette validation est utilisable jusqu'au **2 septembre 2026 inclus**. À partir du **3 septembre 2026**, une revalidation AIRAC 09/26 est obligatoire avant publication ou nouvelle validation aviation.

## Bundle de prépublication

Trois éléments sont maintenant figés :

- `review-checklist.json` : **12/12** éléments revus ;
- `publication-gates.json` : **0 blocker** ;
- `publication-record.json` : record v0.3 figé en statut **`prepublication_frozen_not_published`** avec le SHA candidat.

Le release scope confirme que tous les gates techniques et de revue sont fermés : radio, aviation, construction déterministe, RX-only, déduplication, limite mémoire, checklist, zéro blocker et publication record.

## État de publication

- `release_candidate_memory_count` : **57** ;
- `publication_record_frozen` : **true** ;
- `publication_ready` : **true** ;
- `published` : **false** ;
- CSV public v0.3 créé : **non** ;
- registre public mis à jour : **non** ;
- v0.2 publique : **58 RX, toujours immuable**.

La prochaine étape est donc exclusivement la **mutation publique atomique** : exposer un CSV strictement identique au candidat, mettre le registre/site à v0.3, vérifier le SHA du build public, puis transformer le record prépublication en record `published_immutable`.

Références :

- `research/ile-de-france-v0.3/radio-validation-pass3-2026-08-21.json` ;
- `research/ile-de-france-v0.3/aviation-validation-pass4-2026-08-21.json` ;
- `research/ile-de-france-v0.3/generated/release-candidate/candidate-manifest.json` ;
- `research/ile-de-france-v0.3/review-checklist.json` ;
- `research/ile-de-france-v0.3/publication-gates.json` ;
- `research/ile-de-france-v0.3/publication-record.json` ;
- `research/ile-de-france-v0.3/release-scope.json` ;
- `tools/build_idf_v03_candidate.py` ;
- `tests/test_idf_v03_candidate.py` ;
- `tests/test_sprint101_state_sync.py`.
