# Sprint 16 — prépublication et contrôle de readiness

Date : 2026-08-08

## Objectif

Préparer la transition d'Annecy–Alpes–Léman v0.2 vers la prépublication sans créer de CSV public tant que le dernier contrôle dynamique obligatoire n'est pas terminé.

## État actuel

- candidat interne : 65 mémoires ;
- AIRAC France : validé ;
- AIRAC Suisse : validé ;
- périmètre aviation : clos ;
- NOTAM France : contrôle facultatif, non bloquant ;
- NOTAM Suisse : contrôle facultatif, non bloquant ;
- satellites FM : recontrôle officiel AMSAT encore requis ;
- publication publique : interdite tant que cette dernière porte reste ouverte.

## Nouveaux garde-fous

Le script `tools/check_annecy_release_readiness.py` lit les portes opérationnelles et distingue :

- les portes réellement bloquantes (`required_for_public_release: true`) ;
- les contrôles seulement informatifs ou conseillés (`required_for_public_release: false`).

Au 8 août 2026, le seul bloqueur attendu est `dynamic_satellites`.

Le fichier `research/annecy-alpes-leman-v0.2/prepublication-plan.json` réserve le futur chemin de téléchargement mais impose `public_file_created: false` et `public_export_allowed: false`.

## NOTAM

Les options prévues par `generator/options.json` restent indépendantes :

- `include_aviation` modifie le contenu CSV ;
- `notam_check` ne modifie pas les fréquences et ne bloque pas la génération.

## Réseau AMSAT

Le contrôle en direct n'a pas été validé pendant ce sprint car l'accès web aux pages AMSAT n'était pas disponible de façon fiable dans le workflow courant. Aucun statut satellite n'a donc été promu artificiellement.

La prochaine action est de refaire le contrôle officiel de SO-50, AO-91 et AO-123. Si les trois entrées restent compatibles avec le candidat, la porte `dynamic_satellites` pourra passer à un statut `passed_*`, puis le candidat de prépublication pourra être généré.

## Aucun changement public

Ce sprint ne crée aucun fichier Annecy–Alpes–Léman v0.2 dans `website/public` et ne modifie pas le statut public « En préparation ».
