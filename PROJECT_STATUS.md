# RadioPack France — point de reprise

Dernière mise à jour : **12 août 2026**
Sprint courant : **81**
État logique : **0.21.70**

Repères de compatibilité historique conservés pour les garde-fous antérieurs : Sprint courant : **73** ; État logique : **0.21.62**.

Compatibilité historique Normandie : revue v0.4 est **9/9** ; blocages de prépublication sont à **0** ; publication enregistrée.

L'état machine correspondant est `research/project-resume-state.json`. Résumé courant : `research/sprint-81-summary.md`.

## État public

- Normandie v0.4 : **142 mémoires RX**, publiée et immuable.
- Annecy–Alpes–Léman v0.2 : 65 mémoires RX, variante 48 sans aviation.
- Bretagne v0.2 : **151 mémoires RX**, publiée et immuable.
- Bretagne v0.1 : **135 mémoires RX**, publication historique immuable.

## Sprint 81 — Bretagne v0.3 initialisée à 151

La prochaine version Bretagne démarre depuis la v0.2 publique immuable, sans ajout automatique : **151 mémoires RX, delta 0**. Le builder v0.3 recopie exactement la v0.2 et vérifie son SHA-256.

- aucune v0.3 publique ni bascule de registre ;
- AIRAC 08/26 reste courant jusqu’au 2 septembre 2026 inclus ; AIRAC 09/26 commence le 3 septembre ;
- toute future publication v0.3 après cette transition doit revalider l’aviation ;
- seuls F1ZUG public, CROSS Ch64/Ch79, F5ZPV, F5ZZH et F5ZZC-4 restent reportés, plus la transition AIRAC ;
- les revues ADRASEC générales à delta 0 et F1ZBZ ne sont pas rouvertes sans nouvelle preuve.

Test : `tests/test_sprint81_bretagne_v03_initialization.py`.

## Sprint 80 — Bretagne v0.2 publiée à 151

La publication explicite est terminée : le candidat gelé au Sprint 79 est devenu le CSV public Bretagne v0.2, **octet pour octet identique** au builder.

- **151 mémoires RX**, dont 16 aviation AIRAC 08/26 ;
- SHA-256 public : `73aa3d530ae9f6c572eb01794b0861ecba61df0faf7884ee766085d3de7601a4` ;
- AIRAC 08/26 recontrôlé courant le 12 août 2026, valable jusqu'au 2 septembre 2026 inclus ;
- registre et page Bretagne basculés sur v0.2 ;
- v0.1 conservée comme historique immuable ;
- dossiers F1ZUG, mappings CROSS et relais amateur arrêtés/non résolus restent reportés hors scope sans être inventés.

Tests : `tests/test_bretagne_v02_public_release.py` et `tests/test_sprint80_bretagne_v02_publication.py`.

## Sprint 79 — scope v0.2 figé, prépublication prête

Bretagne v0.2 est figée à **151 mémoires RX**. La revue de maturité est à **10/10**, avec **0 bloqueur** pour le périmètre explicitement retenu.

- AIRAC 08/26 reste courant au 12 août 2026 et les 16 mémoires aviation sont maintenues dans le scope ;
- F1ZUG/ADRASEC35, les mappings locaux Ch64/Ch79 et les infrastructures amateur arrêtées/non résolues sont reportés explicitement hors scope ;
- aucun de ces reports ne crée une RF manquante dans les 151 mémoires figées ;
- l'audit de prépublication reconstruit le candidat et interdit toute mutation publique prématurée.

État : `prepublication_ready=true`, **publication toujours false**. Un sprint séparé reste obligatoire pour créer/figer le CSV public, son empreinte et la bascule du registre.

Test : `tests/test_sprint79_bretagne_v02_maturity.py`. Audit : `tools/run_bretagne_v02_prepublication_audit.py --require-prepublication-ready`.

## Sprint 78 — CROSS Ch64 / Ch79, candidat toujours 151

La revalidation primaire des mappings locaux CROSS produit un **delta candidat 0** et aucune attribution de site.

- Étel Ch64 : l'affirmation ministérielle régionale 63/64 dans le Morbihan ne nomme pas de site ; la documentation opérationnelle actuelle mappe Étel sur Ch63. Le conflit primaire reste ouvert et Ch64 n'est ni déclaré arrêté ni attribué à un site précis.
- Corsen Ch79 : le réseau côtier actuel est confirmé, mais aucun mapping primaire actuel Ch79 → émetteur précis n'est exploitable. Fréhel/Bodic/Batz/Stiff/Raz restent des pistes secondaires ou historiques, pas des attributions promues.
- Le Guide Marine 2026 est identifié mais son PDF n'est pas extrait dans le workflow courant ; son indisponibilité ne vaut pas preuve négative.
- Les deux paires RF sont déjà présentes génériquement : aucune duplication mémoire.

Test : `tests/test_sprint78_bretagne_cross_mapping_revalidation.py`.

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

## Dossiers reportés après le scope Bretagne v0.2

Ces dossiers restent ouverts en recherche mais **ne bloquent plus le scope v0.2 figé** : F1ZUG / ADRASEC 35 sans fréquence de transpondeur publiée, F5ZPV/F5ZZH/F5ZZC-4 arrêtés ou non résolus, et mappings locaux CROSS Étel Ch64 / Corsen Ch79. ADRASEC 29 et F1ZBZ sont déjà résolus à delta RF 0.

Ch64 et Ch79 existent déjà génériquement dans la base v0.1 : une attribution locale future restera une métadonnée et ne devra pas créer de doublon RF.

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
python tests\test_sprint78_bretagne_cross_mapping_revalidation.py
python tools\run_bretagne_v02_prepublication_audit.py --require-prepublication-ready
python tests\test_sprint79_bretagne_v02_maturity.py
python tests\test_bretagne_v02_public_release.py
python tests\test_sprint80_bretagne_v02_publication.py
python tools\build_bretagne_v03_internal_candidate.py
python tests\test_sprint81_bretagne_v03_initialization.py
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
- `prepublication_ready=true` n'autorise jamais à lui seul une publication ;
- pas de remplissage artificiel ; maximum 200 mémoires ;
- revue finale et changement explicite du registre public restent obligatoires avant publication.
