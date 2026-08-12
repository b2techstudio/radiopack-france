# Sprint 76 — Bretagne v0.2 revalidation des infrastructures radioamateur

Date : 12 août 2026
État logique visé : `0.21.65`

## Résultat

Le candidat interne Bretagne v0.2 reste à **151 mémoires RX**. La passe de revalidation sur F5ZPV, F5ZZH, F1ZBZ et F5ZZC-4 produit un **delta RF de 0**.

Aucun fichier public Bretagne v0.2 n'est créé et Bretagne v0.1 reste immuable à 135 mémoires.

## F1ZBZ Lorient — dossier RF résolu sans nouvel ajout

Le répertoire REF courant expose plusieurs chemins actifs autour de F1ZBZ. Après déduplication, les cinq valeurs RF utiles sont déjà toutes représentées dans `research/paired-rx-deduplicated-memory-plan.json` : 145.025, 145.1375, 145.625, 145.7375 et 431.200 MHz.

Les deux valeurs 145.1375 et 145.7375 sont déjà fusionnées avec les rôles F5ZPE correspondants. La revue de direction des chemins F1ZBZ n'impose donc aucune nouvelle mémoire : **delta 0**.

## F5ZPV — conflit de statut, opérateur local prioritaire

Le REF général affiche F5ZPV actif, tandis que l'ARA35, exploitant local, indique toujours le RU19 temporairement arrêté. La règle permanente du projet s'applique : le statut opérateur local prime pour l'état opérationnel courant.

F5ZPV reste donc hors candidat. La paire documentée 430.475 / 439.875 MHz n'est pas promue dans Bretagne v0.2 tant qu'un redémarrage n'est pas confirmé par l'opérateur local.

## F5ZZH — toujours arrêté

L'ARA35 indique toujours le relais VHF de Rennes temporairement arrêté et à la recherche d'un nouveau site. Le répertoire général le donne également arrêté. La paire 145.1875 / 145.7875 MHz reste hors candidat jusqu'à une confirmation locale de remise en service.

## F5ZZC-4 — rôle APRS conservé, fréquence actuelle non validée

La page ARA35 identifie F5ZZC-4 à Ker Lann / Bruz comme digipeater APRS géré par l'ADRASEC 35, mais le texte de la page décrit le réseau « fin 2015 ». Cette preuve de rôle est donc conservée comme contexte, pas comme validation actuelle de fréquence.

Le répertoire REF contient par ailleurs une entrée distincte F5ZZC analogique arrêtée sur 432.975 MHz. Aucun élément ne prouve qu'il s'agit du même service que F5ZZC-4 APRS. Les deux identifiants ne sont pas fusionnés et aucune fréquence n'est attribuée à F5ZZC-4.

## Artefacts

```text
research/bretagne-v0.2/amateur-infrastructure-revalidation.json
tests/test_sprint76_bretagne_amateur_revalidation.py
research/sprint-76-summary.md
```

Le backlog v0.2 marque désormais F1ZBZ comme résolu à delta 0. Les priorités restantes de ce dossier sont F5ZPV, F5ZZH et F5ZZC-4.

## Garde-fous

- le statut opérateur local prime sur un annuaire général pour l'état courant ;
- une infrastructure arrêtée n'est pas promue ;
- une simple revue de direction ne crée pas de doublon RF ;
- des indicatifs proches ne prouvent pas qu'il s'agit du même service ;
- une preuve de rôle ancienne ne valide pas une fréquence actuelle ;
- toutes les mémoires restent RX-only ;
- aucune publication v0.2 n'est effectuée.

## Rappel Sprint 75

Le candidat reste composé de la base v0.1 à 135 mémoires plus 16 mémoires aviation AIRAC 08/26. Ces mémoires aviation sont toutes en AM, **avec un pas de 8,33 kHz**, aux positions 130 à 145 ; les positions 146 à 149 restent libres.
