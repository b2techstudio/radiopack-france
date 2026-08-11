# RadioPack France — point de reprise

Dernière mise à jour : **11 août 2026**  
Sprint courant : **63**  
État logique : **0.21.52**

Ce fichier sert de point de reprise humain. L'état machine correspondant est dans `research/project-resume-state.json`. Le détail des Sprints 55 à 60 est dans `research/sprint-55-60-summary.md`, puis `research/sprint-61-summary.md`, `research/sprint-62-summary.md` et `research/sprint-63-summary.md`.

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

- **R3 / F1ZBX** : paramètres opérateur confirmés sur 145.075 / 145.675 MHz ; réception Mortain encore à démontrer par au moins deux sessions indépendantes.
- **F5ZHA Laval** : le REF courant conserve 145.4675 / 432.575 MHz. La valeur conflictuelle RepeaterBook 431.4125 MHz est maintenant mieux qualifiée : sa page de vérification par âge affiche **2017-02-17** et `Off-Air`. Ce conflit secondaire stale ne remplace cependant pas l'exigence d'une source locale actuelle ou autoritative équivalente, et la couverture utile Mortain reste non validée.
- **F1ZOV** : recontrôle du 11 août 2026, l'exploitant local F6KFW l'indique toujours **En Maintenance** sur 430.375 / 431.975 MHz ; le statut exploitant local reste prioritaire sur le REF général.
- **F6ZES Sourdeval** : recontrôle ciblé du 11 août 2026. Le REF confirme toujours site/responsable/locator/altitude mais laisse état, bande, émission, réception et mode vides. Les recherches ciblées n'ont pas fourni de seconde source actuelle de fréquence/mode. Fréquence/mode non résolus, delta candidat **0**, aucune conjecture autorisée.

### Revalidation des blocages — Sprint 63

`research/sprint-63-source-revalidation.json` conserve la passe datée sans modifier les critères des portes existantes.

- F1ZOV : maintenance opérateur confirmée à nouveau, delta **0**.
- F5ZHA : conflit RepeaterBook 431.4125 reclassé **secondaire stale** grâce à la date de vérification 2017-02-17 ; réconciliation autoritative toujours incomplète et terrain toujours requis, delta **0**.
- F6ZES : aucun champ fréquence/mode nouveau, delta **0**.
- R3 : aucune nouvelle observation terrain dans le dépôt, delta **0**.

Cette passe ne modifie ni `promotion-gates.json`, ni le candidat interne, ni les artefacts publics.

### Scan REF adjacent — Sprint 61

`research/normandie-v0.4/mortain-adjacent-ref-scan.json` recontrôle les départements **35, 50, 53 et 61**. Résultat : **0 nouveau relais analogique actif non déjà suivi**, donc delta candidat **0**.

- 35 : R3/F1ZBX reste le cas analogique actif pertinent ; R71/F5ZEB conserve le conflit REF/opérateur déjà documenté.
- 50 : F5ZHY, F1ZBL et F1ZOV sont déjà suivis ; F6ZES reste incomplet.
- 53 : F6ZCE et F5ZHA restent les cas analogiques pertinents ; F5ZTQ est arrêté.
- 61 : les lignes courantes F1ZKC et F1ZPR sont numériques C4FM/DMR et n'entrent pas dans le profil analogique.

Ce scan est une preuve d'inventaire, pas une preuve de réception. Il ne modifie ni candidat ni pack public.

## Bretagne — CROSS Corsen canal 79

`research/bretagne-v0.1/corsen-channel79-evidence.json` reste le dossier de vérité courant.

Le contexte primaire actuel confirme le réseau VHF/MF Corsen sans identifier le site actuel du canal 79. Une source locale actuelle du Club de Voile de la Baie d'Erquy associe le canal 79 à **Cap Fréhel** et **Bodic** avec des horaires de diffusion. Cette donnée reste une **piste secondaire**, pas une validation primaire : aucune attribution de site n'est promue.

Sprint 62 qualifie séparément deux infrastructures actuelles :

- **Cap Fréhel** : la DIRM confirme que le CROSS Corsen dispose au phare d'équipements de suivi et de liaison avec les navires ;
- **Stiff / Ouessant** : l'offre officielle 2026 et le marché DGAMPA de rénovation confirment des équipements de radiocommunications/radio actuellement nécessaires au CROSS Corsen.

Ces preuves d'infrastructure **n'attribuent aucun canal**. Une source primaire historique de 2003 documente l'usage du canal 79 par Ouessant Traffic / CROSS Corsen et l'architecture radio historique autour du Stiff/Pointe du Raz/Corsen ; elle reste historique et ne vaut pas validation 2026.

Le bilan officiel CROSS Corsen 2025, publié le 2 mars 2026, reste identifié mais son PDF de 14,6 Mio n'a pas pu être chargé par l'outil de lecture courant ; son contenu canal/site n'est donc pas utilisé. Cette impossibilité d'extraction n'est pas une preuve négative.

Météo-France présente depuis le **5 août 2026** son Guide Marine comme contenant notamment horaires, fréquences radio et contenu des bulletins VHF. Le lien direct du Guide Marine 2026 a été identifié, mais un nouveau chargement le 11 août 2026 a encore échoué dans le workflow web (`cache miss`). Le contenu n'a pas été extrait et aucune capture PDF n'a pu être obtenue : aucune attribution Ch79 n'en est déduite.

Les deux fréquences paired RX du canal 79, **156.975 / 161.575 MHz**, étaient déjà dans la recherche Bretagne : aucun delta mémoire RF.

## Bretagne — CROSS Étel canal 64

`research/bretagne-v0.1/etel-channel64-evidence.json` conserve le **conflit primaire actuel** :

- la page ministérielle actuelle affirme que les canaux **63 et 64** diffusent un bulletin côtier permanent notamment dans le Morbihan ;
- la page actuelle du CROSS Étel nomme Étel et Chassiron en diffusion continue sur **63** ;
- le planning météo actuellement lié par le CROSS liste les émetteurs/canaux et ne mentionne pas 64 ;
- le bilan officiel 2025 décrit **16 stations VHF + 2 MF**, nomme les émetteurs météo réguliers et les stations renforcées **Étel/Chassiron/Ferret sur 63**, sans mention de canal 64.

Sprint 62 formalise donc une **convergence opérationnelle locale sur Ch63** : trois sources opérationnelles locales actuelles exploitées mentionnent explicitement 63, aucune de ces trois ne mentionne 64. Cette convergence renforce le conflit avec la page ministérielle générique, mais **ne prouve ni que Ch64 fonctionne actuellement, ni qu'il est arrêté**. Aucun site Ch64 n'est attribué.

Le **Guide Marine 2026** reste une cible primaire prioritaire. Son URL PDF directe est maintenant connue mais le nouveau chargement du 11 août 2026 a échoué ; un PDF non lu ne produit aucune conclusion Ch64.

L'offre technique DIRM de juillet 2026 parle par ailleurs de **17 stations radio** maintenues de Penmarc'h à Biarritz. Ce nombre ne doit pas être réconcilié arithmétiquement avec « 16 VHF + 2 MF » sans définition commune des unités de comptage.

La paire RX 64 **156.225 / 160.825 MHz** était déjà dans la recherche Bretagne : delta RF **0**.

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
- une source secondaire actuelle peut prioriser une recherche mais ne remplace pas une validation primaire requise ;
- une source secondaire stale ne remplace pas la réconciliation autoritative explicitement exigée par une porte ;
- un conflit entre sources primaires actuelles doit être réconcilié avant promotion ;
- une convergence documentaire locale sur un canal ne réfute pas automatiquement un autre canal mentionné par une source primaire conflictuelle ;
- l'absence d'une donnée dans un document local courant n'est pas automatiquement une preuve d'arrêt ;
- une source primaire identifiée mais non extractible n'est pas une preuve négative ;
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
