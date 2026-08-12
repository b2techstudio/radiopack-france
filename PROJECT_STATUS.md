# RadioPack France — point de reprise

Dernière mise à jour : **12 août 2026**
Sprint courant : **75**
État logique : **0.21.64**

Repères de compatibilité historique conservés pour les garde-fous antérieurs : Sprint courant : **73** ; État logique : **0.21.62**.

Ce fichier est le point de reprise humain. L'état machine correspondant est `research/project-resume-state.json`. Le résumé courant est `research/sprint-75-summary.md`.

## État public

- **Normandie v0.4** : **142 mémoires RX**, publiée et immuable.
- **Normandie v0.3.1** : 139 mémoires RX, historique immuable.
- **Annecy–Alpes–Léman v0.2** : 65 mémoires RX, variante 48 sans aviation, publiée et immuable.
- **Bretagne v0.1** : **135 mémoires RX**, publiée et immuable.
- Aucun CSV Bretagne v0.2 n'est public ; le registre public reste sur Bretagne v0.1.

## Sprint 75 — Bretagne v0.2 à 151 mémoires

Bretagne v0.2 est la version de recherche active. Elle repart toujours de la base publique immuable **v0.1 = 135 mémoires** et ajoute **16 mémoires aviation RX** aux positions 130 à 145. Le candidat interne atteint donc **151 mémoires RX**.

Les positions 146 à 149 restent libres : aucun remplissage artificiel. Le builder `tools/build_bretagne_v02_internal_candidate.py` reconstruit d'abord exactement la base v0.1 puis ajoute l'aviation, sans modifier aucun fichier public.

### Aviation AIRAC 08/26

Le produit SIA courant **AIRAC 08/26 - CORRIGENDUM** est en vigueur du **6 août au 2 septembre 2026 inclus**. La validation Sprint 75 suit le précédent déjà utilisé pour Annecy–Alpes–Léman : contexte AIRAC courant vérifié + dernière page AIP primaire publique effective pour le service.

Le dépôt ne prétend pas avoir extrait les octets du fichier XML courant et ne prétend pas avoir fait une correspondance champ par champ avec cet XML. Cette limite est explicite dans `research/bretagne-v0.2/aviation-airac-08.json`.

Périmètre retenu :

- Rennes Saint-Jacques : 7 fréquences uniques ;
- Brest Bretagne : 5 ;
- Dinard Pleurtuit Saint-Malo : 2 ;
- Quimper Pluguffan : 1 ;
- aviation urgence 121.500 MHz : 1.

Toutes sont AM, pas 8.33 kHz, RX-only. Les doublons de services sur la même RF sont dédupliqués.

Artefacts :

```text
research/bretagne-v0.2/aviation-airac-08.json
research/bretagne-v0.2/candidate-memory-delta.json
research/bretagne-v0.2/pack-plan.json
research/bretagne-v0.2/backlog.json
research/sprint-75-summary.md
tools/build_bretagne_v02_internal_candidate.py
tests/test_sprint75_bretagne_aviation.py
```

## Backlog Bretagne v0.2 restant

L'aviation est validée **pour le candidat interne uniquement**, pas pour une publication automatique. Restent ouverts :

- données ADRASEC publiquement vérifiables pour 22 / 29 / 35 / 56 ;
- cas F1ZUG / ADRASEC 35, sans jamais déduire une fréquence d'une entrée APRS ;
- attribution locale CROSS Étel Ch64 ;
- attribution locale CROSS Corsen Ch79 ;
- revalidation des infrastructures radioamateur F5ZPV, F5ZZH, F1ZBZ et F5ZZC-4.

Ch64 et Ch79 existent déjà génériquement dans la base publique v0.1 ; une attribution locale future ne crée pas de doublon RF.

## Historique Sprint 74

Bretagne v0.2 a été initialisée sur v0.1=135 avec candidat 135, delta 0 et six dossiers de recherche. Cette initialisation reste auditable dans `research/sprint-74-summary.md` même après le passage du candidat à 151.

## Historique Bretagne v0.1

Bretagne v0.1 a été publiée au Sprint 73 avec **135 mémoires RX**, après une revue 8/8 sans blocage du périmètre figé. Son CSV public reste identique au candidat revu et la version reste immuable.

Les données aviation, ADRASEC non publiées, mappings CROSS locaux et infrastructures amateur non résolues avaient été reportés à v0.2 sans validation implicite.

## Normandie v0.5 — état inchangé

Normandie v0.5 reste basée sur v0.4=142, avec **0 ajout éligible** et un plafond potentiel connu à **147 mémoires** hors F6ZES.

- **R3 / F1ZBX** : paire 145.075 / 145.675 MHz = **2 mémoires RX** si validation. Il faut toujours **2 sessions** RX indépendantes depuis Mortain ; les sessions sont des preuves, pas des mémoires.
- **F5ZHA** : le REF courant conserve 145.4675 / 432.575 MHz ; la donnée conflictuelle RepeaterBook reste associée à `2017-02-17` / `Off-Air`. La réconciliation autoritative et le terrain restent nécessaires.
- **F1ZOV** : toujours En Maintenance selon l'opérateur local au dernier contrôle.
- **F6ZES Sourdeval** : fréquence et mode toujours non résolus ; delta candidat **0** et aucune conjecture autorisée.

La revue v0.4 est **9/9** et les blocages de prépublication sont à **0** ; la publication enregistrée de v0.4 reste distincte des dossiers reportés à v0.5.

## Bretagne — frontières CROSS conservées

### CROSS Étel Ch64

Le **conflit primaire actuel** demeure : la source ministérielle maintient 63/64 dans le Morbihan, tandis que les sources locales CROSS Étel convergent sur Ch63. La **convergence opérationnelle locale sur Ch63** ne prouve ni fonctionnement ni arrêt de Ch64.

Le bilan 2025 parle de **16 stations VHF + 2 MF** et la maintenance 2026 de **17 stations radio** ; ces nombres ne sont pas réconciliés sans définition commune.

### CROSS Corsen Ch79

Les pistes secondaires incluent **Cap Fréhel**, **Bodic** et la chaîne jusqu'au **Stiff / Ouessant**. Elles ne remplacent toujours pas le mapping primaire actuel requis.

La page ministérielle de référence a été recontrôlée le **19 juin 2026**. Le **Guide Marine 2026** reste un élément de recherche documentaire distinct des mappings de sites.

## Sprint 66 — inventaires techniques historiques

Le Sprint 66 a confirmé des infrastructures et périmètres techniques sans transformer existence d'infrastructure en attribution de canal. Ce principe reste actif pour Bretagne v0.2 et Normandie v0.5.

## Commandes de reprise

```powershell
cd "C:\Users\cross\Documents\CODE\PROJETS\RadioPack-France"
git pull --ff-only

python tools\build_bretagne_v02_internal_candidate.py
python tests\test_sprint75_bretagne_aviation.py
python tests\test_sprint74_bretagne_v02_initialization.py
python tests\test_bretagne_public_release.py
python tests\test_pack_registry.py
python tests\test_site_files.py

python tools\run_normandie_v04_checks.py --extended
python tests\test_normandie_v04_review_handoff.py
python tests\test_sprint60_revalidation.py
python tests\test_sprint61_research.py
python tests\test_sprint62_primary_reference_boundaries.py
python tests\test_sprint63_blocker_revalidation.py
python tests\test_sprint64_dual_rx_contract.py
python tests\test_sprint65_primary_recheck.py
python tests\test_sprint66_technical_inventory_boundaries.py
python tests\test_sprint67_current_reference_synthesis.py

cd website
npm ci
npm run build
cd ..

python tests\test_built_annecy_public_csv.py
python tests\test_built_public_pack_catalog.py

git status
```

Terrain R3 :

```powershell
python tools\build_normandie_v04_r3_validation_pack.py
python tools\record_normandie_v04_r3_observation.py --help
```

Terrain F5ZHA :

```powershell
python tools\build_normandie_v04_f5zha_validation_pack.py
python tools\record_normandie_v04_f5zha_observation.py --help
```

## Règles de reprise

- ne jamais réécrire une version publiée ;
- toutes les mémoires restent RX-only avec `Duplex=off` et `Offset=0.000000` ;
- aucune fréquence non résolue n'est devinée ;
- aucune donnée opérationnelle privée PPDR n'est intégrée ;
- une source secondaire ne remplace pas une validation primaire exigée ;
- une infrastructure actuelle ne permet pas d'attribuer automatiquement un canal ;
- une déclaration régionale de canal ne permet pas d'identifier automatiquement son émetteur ;
- une observation terrain ne ferme pas un conflit de source ;
- le nombre de sessions terrain ne définit jamais le nombre de mémoires ;
- une paire vérifiée de deux fréquences distinctes conserve 2 mémoires RX ;
- une source primaire identifiée mais non lue n'est pas une preuve négative ;
- pour l'aviation, le contexte AIRAC courant et la dernière page AIP primaire effective peuvent valider un candidat interne selon le précédent du projet ;
- ne jamais revendiquer une correspondance de champs XML si les octets XML n'ont pas été réellement extraits ;
- une promotion vers le candidat interne n'est jamais une publication ;
- pas de remplissage artificiel ; maximum 200 mémoires ;
- revue finale et changement explicite du registre public restent obligatoires avant toute publication.
