# RadioPack France — Sprints 55 à 60

Date : **10 août 2026**

Cette passe prolonge la chaîne de revue non publique de Normandie v0.4 puis reprend la recherche externe prioritaire. Aucun pack public n'est modifié. Normandie v0.3.1 reste figée à 139 mémoires et le candidat interne v0.4 reste à 142 mémoires.

## Sprint 55 — 0.21.44 — snapshot de revue

- Ajout de `tools/build_normandie_v04_review_snapshot.py`.
- Capture déterministe de l'état de revue : audit, checklist, diff candidat et décisions stations.
- Identifiant SHA-256 du snapshot.
- Le snapshot est une preuve de revue interne : il ne complète pas la revue, ne mute pas le candidat et ne publie rien.

## Sprint 56 — 0.21.45 — manifeste d'empreintes

- Ajout de `tools/build_normandie_v04_review_manifest.py`.
- Empreintes SHA-256 des onze entrées de revue, du candidat interne et du preview gardé.
- Le CSV public Normandie v0.3.1 et `website/src/lib/packRegistry.ts` font partie des entrées surveillées.
- Toute future activation publique doit rester un changement explicite séparé.

## Sprint 57 — 0.21.46 — détection de dérive

- Ajout de `tools/check_normandie_v04_review_drift.py`.
- Comparaison d'un manifeste de revue capturé avec l'état courant du dépôt.
- Toute modification d'une entrée revue, du candidat, du preview ou du snapshot force une nouvelle revue.
- Un contrôle sans dérive n'est jamais une autorisation de publication.

## Sprint 58 — 0.21.47 — dry-run de publication

- Suppression de la dépendance circulaire imposant un registre public déjà modifié pour terminer la prépublication.
- Séparation entre **prépublication prête** et **activation publique**.
- Ajout de `tools/run_normandie_v04_publication_dry_run.py` : baseline de revue obligatoire, dérive nulle obligatoire, aucun fichier public écrit.
- `activation_ready=true`, lorsqu'il sera atteint, restera une condition de simulation et non une publication automatique.

## Sprint 59 — 0.21.48 — handoff de revue

- Ajout de `tests/test_normandie_v04_review_handoff.py`.
- Intégration du snapshot, manifeste, drift checker et dry-run au runner local et à GitHub Actions.
- État courant vérifié par le test : **3/9 points de revue complétés**, **6 blocages ouverts**, candidat/preview **142/142**, `release_ready=false`.
- La baseline propre reste propre ; une dérive synthétique impose bien une nouvelle revue.

## Sprint 60 — 0.21.49 — reprise de recherche prioritaire

### F6ZES Sourdeval

- Ajout de `research/normandie-v0.4/f6zes-revalidation.json`.
- Le REF courant confirme `F6ZES`, Sourdeval, F1SMB, `IN98MR93XV` et 230 m.
- Les champs état, bande, émission, réception et mode restent absents : fréquence et mode ne sont donc toujours pas résolus.
- Aucune page publique ARA50 spécifique à F6ZES n'a été retrouvée pendant cette passe ; cette absence de résultat n'est pas une preuve négative.
- Delta candidat : **0**. `sourdeval_must_not_be_guessed=true` reste impératif.

### CROSS Corsen — canal 79

- Ajout de `research/bretagne-v0.1/corsen-channel79-evidence.json`.
- Le contexte primaire actuel confirme le réseau VHF/MF Corsen mais ne rattache toujours pas le canal 79 à un site précis.
- Une page locale actuelle du Club de Voile de la Baie d'Erquy donne le canal 79 pour **Cap Fréhel** et **Bodic**, avec leurs horaires de diffusion.
- Cette source est enregistrée comme **indice secondaire local actuel** uniquement : elle renforce la priorité de revalidation primaire de Cap Fréhel/Bodic mais ne ferme pas le dossier.
- Les deux fréquences paired RX du canal 79, 156.975 et 161.575 MHz, étaient déjà dans le plan Bretagne : delta RF **0**.

### Garde-fous

- Ajout de `tests/test_sprint60_revalidation.py` et de son étape CI.
- Aucune fréquence F6ZES n'est créée.
- Aucune attribution Corsen Ch79 n'est promue depuis la seule source secondaire.
- Aucun CSV public, aucune route publique et aucune entrée de registre public ne sont modifiés.

## État fin de passe

- Normandie v0.3.1 publique : **139 mémoires**, inchangée.
- Annecy–Alpes–Léman v0.2 publique : **65 / 48 mémoires**, inchangée.
- Bretagne : toujours **non publique**.
- Normandie v0.4 candidat interne : **142 mémoires**, inchangé.
- Preview courant : **142 mémoires**.
- Ajouts futurs actuellement éligibles : **0**.
- Checklist de revue : **3/9**.
- Blocages ouverts : **6**.
- F6ZES : fréquence/mode non résolus, delta 0.
- Corsen Ch79 : Cap Fréhel/Bodic deviennent des pistes secondaires prioritaires, attribution primaire toujours ouverte.
- Publication v0.4 : **interdite**.
