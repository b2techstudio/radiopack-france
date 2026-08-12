# Sprint 77 — Bretagne v0.2 revalidation publique ADRASEC

Date : 12 août 2026
État logique visé : `0.21.66`

## Résultat

Le candidat interne Bretagne v0.2 reste à **151 mémoires RX**. La revalidation publique ADRASEC des départements **22, 29, 35 et 56** produit un **delta RF de 0**.

Bretagne v0.1 reste publique et immuable à 135 mémoires. Aucun CSV Bretagne v0.2 public n'est créé et le registre public n'est pas modifié.

## Agrément national

L'arrêté du 9 janvier 2025 renouvelant l'agrément national de sécurité civile de la FNRASEC confirme dans sa liste de membres les ADRASEC 22, 29, 35 et 56.

Cette preuve confirme l'existence et l'appartenance organisationnelle ; elle ne publie aucune fréquence. Le projet interdit donc de déduire une fréquence depuis la seule appartenance à la FNRASEC.

## ADRASEC 29 — preuve publique actuelle, delta 0

Le répertoire REF courant publie **F1ZBH Dinéault** et **F1ZGQ Saint-Éloy** actifs en APRS sur **144.800 MHz**. L'inventaire public APRS.fi expose actuellement les commentaires `APRS DIGI F1ZBH-3 ADRASEC-29` et `DIGI F1ZGQ-3 ***ADRASEC-29***`.

La fonction publique ADRASEC-29 et la fréquence APRS sont donc recoupées sans inférence. Mais 144.800 MHz existe déjà dans le bloc national APRS de RadioPack France : **aucune nouvelle mémoire RF**.

## ADRASEC 35 — fonctions séparées

Le REF courant confirme **F1ZUG** actif en APRS sur **144.800 MHz**. L'ARA35 documente aussi le site F1ZUG comme relais APRS et, lors d'un entretien publié en juin 2024, comme transpondeur du réseau ADRASEC 35.

La fréquence du transpondeur ADRASEC 35 n'est toutefois pas publiée dans cette source. RadioPack France conserve donc strictement deux fonctions distinctes :

- APRS F1ZUG : 144.800 MHz, déjà couvert nationalement ;
- transpondeur ADRASEC 35 : fréquence non publiée, aucune mémoire créée.

La page F5ZZC-4 décrit un état du réseau APRS datant de fin 2015 ; elle reste une preuve historique de rôle, pas une validation actuelle de fréquence.

## ADRASEC 56 — activité publique, pas de fréquence ADRASEC promue

Le site public ADRASEC 56 confirme son activité dans le Morbihan et son rattachement à la préfecture de Vannes, sans publier de fréquence opérationnelle.

APRS.fi montre publiquement des rôles ADRASEC 56, notamment F1ZMU-3 à Saint-Nolff, mais cette métadonnée de rôle ne suffit pas à attribuer une fréquence sans source RF correspondante.

Le REF courant publie par ailleurs F1ZKU Languidic actif sur 430.450 / 439.850 MHz en C4FM. Une source de 2017 relie historiquement F1ZKU à une intervention de membres de l'ADRASEC 56, mais cette preuve est trop ancienne pour attribuer aujourd'hui un rôle ADRASEC courant à ce relais. Aucune mémoire n'est créée à partir de cette association historique.

## ADRASEC 22 — appartenance confirmée, aucune fréquence attribuée

L'appartenance actuelle à la FNRASEC est confirmée. Les sources publiques consultées montrent des infrastructures radioamateur dans les Côtes-d'Armor, mais aucune preuve actuelle suffisamment explicite ne relie une fréquence donnée à l'ADRASEC 22.

La géographie seule ne constitue jamais une preuve de rôle ADRASEC.

## Frontière de sécurité documentaire

Le Sprint 77 ne recherche pas de fréquence opérationnelle privée et exclut explicitement toute donnée PPDR privée. Une donnée non publiée n'est ni devinée, ni reconstruite depuis un indicatif, un chemin APRS, une implantation ou une appartenance associative.

## Artefacts

```text
research/bretagne-v0.2/adrasec-public-revalidation.json
research/bretagne-v0.2/backlog.json
research/bretagne-v0.2/pack-plan.json
tests/test_sprint77_bretagne_adrasec_public_revalidation.py
research/sprint-77-summary.md
```

Le garde-fou Sprint 74 est rendu compatible avec la résolution ultérieure du dossier ADRASEC à delta zéro.

## Garde-fous

- appartenance associative != fréquence publiée ;
- géographie != rôle ADRASEC ;
- APRS != fréquence d'un autre service ;
- rôle historique != rôle courant ;
- même RF déjà présente = aucune duplication ;
- aucune fréquence opérationnelle non publiée n'est inférée ;
- les données PPDR privées restent hors périmètre ;
- toutes les sorties RadioPack restent RX-only ;
- aucune publication Bretagne v0.2 n'est effectuée.
