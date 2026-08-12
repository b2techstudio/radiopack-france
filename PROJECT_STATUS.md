# RadioPack France — point de reprise

Dernière mise à jour : **12 août 2026**
Sprint courant : **77**
État logique : **0.21.66**

Repères de compatibilité historique conservés pour les garde-fous antérieurs : Sprint courant : **73** ; État logique : **0.21.62**.

Compatibilité historique Normandie : revue v0.4 est **9/9** ; blocages de prépublication sont à **0** ; publication enregistrée.

L'état machine correspondant est `research/project-resume-state.json`. Résumé courant : `research/sprint-77-summary.md`.

## État public

- Normandie v0.4 : **142 mémoires RX**, publiée et immuable.
- Annecy–Alpes–Léman v0.2 : 65 mémoires RX, variante 48 sans aviation.
- Bretagne v0.1 : **135 mémoires RX**, publiée et immuable.
- Bretagne v0.2 : aucune publication ; le registre public reste sur v0.1.

## Sprint 77 — ADRASEC public, candidat toujours 151

La revalidation publique des ADRASEC 22, 29, 35 et 56 produit un **delta candidat 0**. Le candidat Bretagne v0.2 reste à **151 mémoires RX**.

- ADRASEC 29 : F1ZBH-3 et F1ZGQ-3 sont recoupés publiquement sur APRS 144.800 MHz, déjà présent nationalement ;
- ADRASEC 35 : F1ZUG APRS 144.800 MHz reste distinct de la fonction transpondeur ADRASEC 35 dont la fréquence n'est pas publiée ;
- ADRASEC 56 : activité publique confirmée, aucune fréquence de service ADRASEC actuelle distincte promue ;
- ADRASEC 22 : appartenance confirmée, aucune fréquence actuelle explicitement attribuée dans le périmètre public retenu ;
- aucune fréquence opérationnelle privée ni donnée PPDR n'est recherchée ou inférée.

Test : `tests/test_sprint77_bretagne_adrasec_public_revalidation.py`.

## Sprint 76 — Bretagne v0.2 reste à 151

La revalidation radioamateur de F5ZPV, F5ZZH, F1ZBZ et F5ZZC-4 produit un **delta candidat 0**. Le candidat interne reste à **151 mémoires RX** : base v0.1=135 + 16 aviation AIRAC 08/26.

`research/bretagne-v0.2/amateur-infrastructure-revalidation.json` enregistre les décisions :

- F1ZBZ : les cinq RF publiées dans le répertoire courant sont déjà représentées dans le plan dédupliqué Bretagne ; dossier de direction résolu à delta RF 0 ;
- F5ZPV : l'annuaire général le présente actif mais l'ARA35, opérateur local, le maintient temporairement arrêté ; le statut local prime, donc aucune promotion ;
- F5ZZH : toujours arrêté et en recherche de nouveau site ;
- F5ZZC-4 : rôle APRS/ADRASEC35 documenté par une page ancienne, sans fréquence actuelle validée ; l'entrée distincte F5ZZC analogique arrêtée ne doit pas être assimilée à F5ZZC-4.

Test : `tests/test_sprint76_bretagne_amateur_revalidation.py`.

## Sprint 75 — aviation AIRAC 08/26

Le candidat est passé de 135 à **151 mémoires RX** avec 16 mémoires aviation aux positions 130 à 145. Les positions 146 à 149 restent libres.

AIRAC 08/26 est traité dans `research/bretagne-v0.2/aviation-airac-08.json`. Les 16 mémoires sont en AM, **avec un pas de 8,33 kHz**, RX-only. Le dépôt ne revendique aucune correspondance champ par champ avec le XML courant tant que ses octets ne sont pas extraits.

## Backlog Bretagne v0.2 restant

- F1ZUG / ADRASEC 35 reste sans fréquence de transpondeur publiée ;
- ADRASEC 29 est résolu à delta RF 0 sur APRS 144.800 MHz déjà national ;
- F5ZPV, F5ZZH et F5ZZC-4 à revalider ultérieurement ;
- mapping local CROSS Étel Ch64 ;
- mapping local CROSS Corsen Ch79.

Ch64 et Ch79 existent déjà génériquement dans la base v0.1 : une attribution locale ne doit pas créer de doublon RF.

## Normandie v0.5 — état conservé

Normandie v0.5 reste à 142 mémoires avec **0 ajout éligible** et un plafond de travail connu à **147 mémoires** hors F6ZES.

- R3 / F1ZBX : une paire représente **2 mémoires RX** si validée ; **2 sessions** terrain indépendantes restent des preuves, pas des mémoires.
- F5ZHA : conflit de source historique ; la provenance RepeaterBook conserve `2017-02-17` / Off-Air.
- F1ZOV : statut opérateur local prioritaire.
- F6ZES Sourdeval : fréquence/mode non résolus ; delta candidat **0** et aucune conjecture.

Commande historique :

```powershell
python tools\run_normandie_v04_checks.py --extended
```

## Frontières CROSS Bretagne conservées

### CROSS Étel Ch64

Le **conflit primaire actuel** demeure. La source ministérielle maintient 63/64 dans le Morbihan tandis que la **convergence opérationnelle locale sur Ch63** ne prouve ni fonctionnement ni arrêt de Ch64.

Le bilan 2025 parle de **16 stations VHF + 2 MF** et la maintenance 2026 de **17 stations radio**. Ces nombres ne sont pas réconciliés sans définition commune.

### CROSS Corsen Ch79

Les pistes secondaires restent **Cap Fréhel**, **Bodic** et **Stiff / Ouessant**. Elles ne deviennent pas automatiquement une attribution primaire de site.

Le contrôle ministériel du **19 juin 2026** et le **Guide Marine 2026** restent des références de recherche. Le **Sprint 66** conserve les frontières d'inventaire technique qui empêchent de transformer une infrastructure en attribution automatique de canal.

## Mortain-Bocage / Sud-Manche — garde-fous historiques

Stations suivies : F5ZHY, F6ZES, F6ZCE, F1ZBX, F5ZHA et F1ZOV. Le statut opérateur local prime ; géométrie et portée théorique ne prouvent pas la réception.

## Commandes de reprise

```powershell
cd "C:\Users\cross\Documents\CODE\PROJETS\RadioPack-France"
git pull --ff-only

python tools\build_bretagne_v02_internal_candidate.py
python tests\test_sprint75_bretagne_aviation.py
python tests\test_sprint76_bretagne_amateur_revalidation.py
python tests\test_sprint77_bretagne_adrasec_public_revalidation.py
python tests\test_sprint74_bretagne_v02_initialization.py
python tests\test_bretagne_public_release.py
python tests\test_site_files.py
python tests\test_pack_registry.py

python tools\run_normandie_v04_checks.py --extended

cd website
npm ci
npm run build
cd ..

git status
```

## Règles de reprise

- versions publiées immuables ;
- toutes les mémoires RX-only avec `Duplex=off` et `Offset=0.000000` ;
- aucune fréquence non résolue n'est devinée ;
- aucune donnée privée PPDR n'est intégrée ;
- le statut opérateur local prime sur un annuaire général pour l'état courant ;
- une infrastructure arrêtée n'est pas promue ;
- des indicatifs proches ne prouvent pas le même service ;
- une preuve de rôle ancienne ne valide pas une fréquence actuelle ;
- une revue de direction ne crée pas de doublon RF ;
- une promotion dans un candidat interne n'est jamais une publication ;
- pas de remplissage artificiel ; maximum 200 mémoires ;
- revue finale et changement explicite du registre public restent obligatoires avant publication.
