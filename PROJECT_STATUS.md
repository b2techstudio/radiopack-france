# RadioPack France — point de reprise

Dernière mise à jour : **11 août 2026**  
Sprint courant : **66**  
État logique : **0.21.55**

Ce fichier sert de point de reprise humain. L'état machine correspondant est dans `research/project-resume-state.json`. Le détail des Sprints 55 à 60 est dans `research/sprint-55-60-summary.md`, puis `research/sprint-61-summary.md`, `research/sprint-62-summary.md`, `research/sprint-63-summary.md`, `research/sprint-64-summary.md`, `research/sprint-65-summary.md` et `research/sprint-66-summary.md`.

## État public

- **Normandie v0.3.1** : 139 mémoires RX, publiée et immuable.
- **Annecy–Alpes–Léman v0.2** : 65 mémoires RX, variante 48 sans aviation, publiée et immuable.
- **Bretagne v0.1** : recherche uniquement, aucune publication.

## Travail actif — Normandie v0.4

Candidat interne reproductible : **142 mémoires**, non public. Les trois portes de fréquence connues représentent au maximum +5 mémoires, soit un plafond de travail connu à **147 mémoires**. Ce plafond n'est pas la taille publique finale et F6ZES reste hors calcul tant que fréquence et mode ne sont pas résolus.

Ajouts internes actuels : `50-ZHY-IN` 145.0875 MHz (175), `53-ZCE-IN` 145.1000 MHz (176), `50-ZBL-U` 431.2500 MHz (177).

État de revue actuel vérifié par `tests/test_normandie_v04_review_handoff.py` : **3/9 points complétés**, **6 blocages ouverts**, **0 ajout éligible**, preview **142 mémoires**. L'audit reste non prêt pour publication.

## Chaîne de revue — Sprints 55 à 59

```text
tools/build_normandie_v04_review_snapshot.py
tools/build_normandie_v04_review_manifest.py
tools/check_normandie_v04_review_drift.py
tools/run_normandie_v04_publication_dry_run.py
tests/test_normandie_v04_review_handoff.py
```

Le snapshot capture l'état logique de revue. Le manifeste enregistre les SHA-256 des entrées, du candidat et du preview. Le drift checker impose une nouvelle revue dès qu'une entrée suivie change. Le dry-run sépare la prépublication de l'activation publique et n'écrit jamais de fichier public.

## Dossiers Normandie encore bloqués

- **R3 / F1ZBX** : paramètres opérateur confirmés sur 145.075 / 145.675 MHz. Si la porte est franchie, la paire représente exactement **2 mémoires RX**. La réception Mortain reste à démontrer par **2 sessions** indépendantes sur la sortie identifiée 145.675 MHz ; ces sessions sont des preuves et ne changent pas le nombre de mémoires.
- **F5ZHA Laval** : recontrôle Sprint 65, le REF courant affiche toujours F5ZHA actif sur **145.4675 / 432.575 MHz**. La valeur conflictuelle RepeaterBook 431.4125 MHz reste secondaire stale avec vérification affichée **2017-02-17** et `Off-Air`. Une source locale actuelle ou autoritative équivalente et la couverture utile Mortain restent requises.
- **F1ZOV** : recontrôle du 11 août 2026, l'exploitant local F6KFW l'indique toujours **En Maintenance** sur 430.375 / 431.975 MHz ; le statut exploitant local reste prioritaire.
- **F6ZES Sourdeval** : recontrôle Sprint 65, le REF confirme site/responsable/locator/altitude mais laisse toujours état, bande, émission, réception et mode vides. Fréquence/mode non résolus, delta candidat **0**, aucune conjecture autorisée.

### Inventaires techniques courants — Sprint 66

`research/sprint-66-technical-inventory-boundaries.json` enregistre la nouvelle passe sans toucher au candidat.

- F5ZHA : ARAM53 est identifiable comme association active, mais aucune publication technique locale actuelle exploitée ne valide la paire ; existence associative ≠ validation de fréquence.
- F6ZES : fréquence/mode/état toujours absents ; delta candidat **0**.
- CROSS Étel : l'offre DIRM `2026-2341297` confirme **17 stations radio** de Penmarc'h à Biarritz et un contexte MHF/VHF, mais aucun nom de station ni canal : Ch64 reste sans site.
- CROSS Corsen : Stiff est revalidé comme infrastructure radio 2026 ; le marché `DGAMPA-SNC1-2025-03_STIFF` confirme le projet de rénovation mais aucun Ch79. Une source secondaire non datée restitue Fréhel/Bodic/Batz/Stiff/Raz sur Ch79, uniquement comme cible de recherche.
- Guide Marine 2026 : nouvelle tentative `cache miss`, donc aucune inférence.

État inchangé : **142**, plafond **147**, revue **3/9**, **6 blocages ouverts**, **0 ajout éligible**, non prêt pour publication.

### Recontrôle primaire courant — Sprint 65

`research/sprint-65-primary-recheck.json` enregistre la passe actuelle sans toucher au candidat.

- F5ZHA : paire REF 145.4675 / 432.575 MHz maintenue comme paire de travail ; réconciliation locale/autoritative toujours incomplète et terrain toujours requis.
- F6ZES : F1SMB, `IN98MR93XV` et 230 m restent présents, mais fréquence/mode/état opérationnel restent absents.
- Résultat : **0 porte franchie, 0 ajout éligible, candidat/preview 142/142, plafond 147, revue 3/9, 6 blocages**.

### Contrat deux mémoires RX — Sprint 64

`research/sprint-64-dual-rx-contract.json` sépare explicitement le nombre de mémoires du nombre de preuves terrain.

- **R3** : `R3-OUT` 145.675 et `R3-IN` 145.075 sont les deux membres de paire. `CTRL-ZHY` 145.6875 est seulement un contrôle facultatif hors paire. Deux sessions de terrain sont toujours nécessaires, mais si la porte passe le delta reste **+2 mémoires**, pas +4.
- **CROSS Étel Ch64** : 156.225 + 160.825 MHz = **2 mémoires RX** si le canal devient publiable ; conflit primaire/site toujours non résolu, delta actuel 0.
- **CROSS Corsen Ch79** : 156.975 + 161.575 MHz = **2 mémoires RX** si le canal devient publiable ; attribution primaire actuelle de l'émetteur toujours non résolue, delta actuel 0.

Le contrat ne modifie ni candidat, ni `promotion-gates.json`, ni pack public.

### Revalidation des blocages — Sprint 63

`research/sprint-63-source-revalidation.json` conserve la passe datée sans modifier les critères des portes existantes.

- F1ZOV : maintenance opérateur confirmée à nouveau, delta **0**.
- F5ZHA : conflit RepeaterBook 431.4125 reclassé **secondaire stale** grâce à la date de vérification 2017-02-17 ; réconciliation autoritative toujours incomplète et terrain toujours requis, delta **0**.
- F6ZES : aucun champ fréquence/mode nouveau, delta **0**.
- R3 : aucune nouvelle observation terrain dans le dépôt, delta **0**.

### Scan REF adjacent — Sprint 61

`research/normandie-v0.4/mortain-adjacent-ref-scan.json` recontrôle les départements **35, 50, 53 et 61**. Résultat : **0 nouveau relais analogique actif non déjà suivi**, donc delta candidat **0**.

Ce scan est une preuve d'inventaire, pas une preuve de réception. Il ne modifie ni candidat ni pack public.

## Bretagne — inventaires techniques Sprint 66

La maintenance 2026 du CROSS Étel confirme 17 stations radio et le domaine MHF/VHF sans fournir l'inventaire nominatif ou les canaux. Le Stiff / Ouessant reste une infrastructure radio Corsen actuelle, mais ni le poste 2026 ni le marché de rénovation ne l'associent à Ch79. La chaîne secondaire Fréhel/Bodic/Batz/Stiff/Raz ne devient pas une preuve primaire actuelle.

Les paires restent **Ch64 156.225 / 160.825 MHz = 2 mémoires RX** et **Ch79 156.975 / 161.575 MHz = 2 mémoires RX** si leurs portes sont un jour franchies ; delta RF actuel **0**.

## Bretagne — recontrôle primaire Sprint 65

Trois frontières sont désormais rafraîchies avec leurs dates courantes :

- la page du ministère chargée de la mer, mise à jour le **19 juin 2026**, maintient que le canal 16 annonce les diffusions météo CROSS sur **79 et 80**, et que les canaux **63 et 64** diffusent un bulletin côtier permanent notamment dans le Morbihan ; elle ne nomme aucun site Ch64 ;
- la page du CROSS Étel, mise à jour le **24 novembre 2025**, maintient les vacations annoncées sur 16 puis diffusées sur 79/80 et la diffusion continue **Étel + Chassiron sur Ch63**, sans site Ch64 ;
- la page du CROSS Corsen, mise à jour le **24 mars 2026**, confirme le réseau VHF/MHF permanent et les bulletins météo diffusés depuis des stations littorales, sans mapping **Ch79 ↔ station**.

Règles renforcées : une déclaration régionale de canal ne nomme pas automatiquement son émetteur et la confirmation d'un réseau CROSS ne mappe pas automatiquement un canal vers une station.

## Bretagne — CROSS Corsen canal 79

`research/bretagne-v0.1/corsen-channel79-evidence.json` reste le dossier de vérité courant.

Le contexte primaire actuel confirme le réseau VHF/MF Corsen sans identifier le site actuel du canal 79. Une source locale actuelle du Club de Voile de la Baie d'Erquy associe le canal 79 à **Cap Fréhel** et **Bodic** avec des horaires de diffusion. Cette donnée reste une **piste secondaire**, pas une validation primaire.

- **Cap Fréhel** : infrastructure CROSS actuelle vérifiée ;
- **Stiff / Ouessant** : équipements radio actuels vérifiés ;
- ces infrastructures **n'attribuent aucun canal**.

Le bilan officiel CROSS Corsen 2025 et le Guide Marine 2026 restent identifiés mais non exploitables dans le workflow courant. Une source non lue n'est pas une preuve négative.

La paire Ch79 **156.975 / 161.575 MHz** est verrouillée comme **2 mémoires RX distinctes** si Ch79 devient publiable. Les deux fréquences étaient déjà dans la recherche Bretagne : aucun delta mémoire RF actuel.

## Bretagne — CROSS Étel canal 64

`research/bretagne-v0.1/etel-channel64-evidence.json` conserve le **conflit primaire actuel** :

- la page ministérielle actuelle affirme que les canaux **63 et 64** diffusent un bulletin côtier permanent notamment dans le Morbihan ;
- la page actuelle du CROSS Étel nomme Étel et Chassiron en diffusion continue sur **63** ;
- le planning météo actuellement lié par le CROSS liste les émetteurs/canaux et ne mentionne pas 64 ;
- le bilan officiel 2025 décrit **16 stations VHF + 2 MF**, nomme les émetteurs météo réguliers et les stations renforcées **Étel/Chassiron/Ferret sur 63**, sans mention de canal 64.

La **convergence opérationnelle locale sur Ch63** ne prouve ni que Ch64 fonctionne actuellement, ni qu'il est arrêté. Aucun site Ch64 n'est attribué.

L'offre technique DIRM de juillet 2026 parle de **17 stations radio** maintenues ; ce nombre ne doit pas être réconcilié arithmétiquement avec « 16 VHF + 2 MF » sans définition commune.

La paire Ch64 **156.225 / 160.825 MHz** est verrouillée comme **2 mémoires RX distinctes** si Ch64 devient publiable. Elle était déjà dans la recherche Bretagne : delta RF actuel **0**.

## Guide Marine 2026

La page Météo-France datée du 5 août 2026 indique toujours que le Guide Marine contient les horaires, fréquences radio et contenus des bulletins VHF. Le lien direct du PDF 2026 a été retenté le 11 août 2026 ; le workflow retourne toujours `cache miss`.

Conséquence : contenu non extrait, aucune capture PDF disponible, aucune inférence Ch64 et aucune attribution Ch79.

## Commandes de reprise

```powershell
cd "C:\Users\cross\Documents\CODE\PROJETS\RadioPack-France"
git pull --ff-only

python tools\run_normandie_v04_checks.py --extended
python tools\check_normandie_v04_source_consistency.py
python tools\check_normandie_v04_source_freshness.py
python tools\build_normandie_v04_review_snapshot.py
python tools\build_normandie_v04_review_manifest.py
python tools\run_normandie_v04_prepublication_audit.py
python tests\test_normandie_v04_review_handoff.py
python tests\test_sprint60_revalidation.py
python tests\test_sprint61_research.py
python tests\test_sprint62_primary_reference_boundaries.py
python tests\test_sprint63_blocker_revalidation.py
python tests\test_sprint64_dual_rx_contract.py
python tests\test_sprint65_primary_recheck.py
python tests\test_sprint66_technical_inventory_boundaries.py
python tests\test_etel_network_research.py

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
- le statut opérateur local prime pour l'état opérationnel courant ;
- une observation radio ne ferme pas un conflit de source ;
- **le nombre de sessions terrain ne définit jamais le nombre de mémoires** ;
- une paire vérifiée de deux fréquences distinctes conserve **2 mémoires RX** après franchissement des portes ;
- une mémoire de contrôle facultative n'est pas membre de la paire ;
- une source secondaire actuelle peut prioriser une recherche mais ne remplace pas une validation primaire requise ;
- une source secondaire stale ne remplace pas la réconciliation autoritative explicitement exigée par une porte ;
- un conflit entre sources primaires actuelles doit être réconcilié avant promotion ;
- une convergence documentaire locale sur un canal ne réfute pas automatiquement un autre canal mentionné par une source primaire conflictuelle ;
- l'absence d'une donnée dans un document local courant n'est pas automatiquement une preuve d'arrêt ;
- une source primaire identifiée mais non extractible n'est pas une preuve négative ;
- une déclaration régionale actuelle sur un canal ne permet pas d'identifier automatiquement son site émetteur ;
- la confirmation d'un réseau CROSS courant ne permet pas de mapper automatiquement un canal vers une station ;
- une infrastructure radio actuelle ne permet pas d'attribuer un canal précis ;
- une affectation historique primaire ne vaut pas validation opérationnelle actuelle ;
- une source périmée bloque une revue mais ne prouve jamais un arrêt ;
- une recherche infructueuse n'est pas une preuve négative ;
- une fréquence non résolue n'est jamais devinée ;
- des nombres de stations issus de définitions différentes ne sont pas réconciliés sans définition commune ;
- géométrie et rayon annoncé ne sont pas des preuves de réception ;
- toutes les mémoires restent RX-only avec `Duplex=off` et `Offset=0.000000` ;
- une porte non franchie reste hors candidat ;
- snapshot, manifeste, drift check, preview, diff, audit et dry-run sont non destructifs et non publics ;
- **integrity_ok** ou un drift propre ne signifie jamais **release_ready** ;
- revue finale, plan mémoire final et changement explicite du registre public restent obligatoires avant publication.
