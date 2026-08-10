# RadioPack France — point de reprise

Dernière mise à jour : **10 août 2026**  
Sprint courant : **61**  
État logique : **0.21.50**

Ce fichier sert de point de reprise humain. L'état machine correspondant est dans `research/project-resume-state.json`. Le détail des Sprints 55 à 60 est dans `research/sprint-55-60-summary.md` et la passe actuelle dans `research/sprint-61-summary.md`.

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
- **F5ZHA Laval** : REF courant sur 145.4675 / 432.575 MHz ; conflit historique 431.4125 encore ouvert et couverture utile Mortain non validée.
- **F1ZOV** : le REF le liste actif, mais l'exploitant local F6KFW l'indique toujours **En Maintenance** ; le statut exploitant local reste prioritaire.
- **F6ZES Sourdeval** : revalidation du 10 août 2026 dans `research/normandie-v0.4/f6zes-revalidation.json`. Le REF confirme site/responsable/locator/altitude mais laisse état, bande, émission, réception et mode vides. Fréquence/mode non résolus, delta candidat **0**, aucune conjecture autorisée.

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

Le bilan officiel CROSS Corsen 2025, publié le 2 mars 2026, a été identifié pendant le Sprint 61. Son PDF de 14,6 Mio n'a pas pu être chargé par l'outil de lecture courant ; son contenu canal/site n'est donc pas utilisé. Cette impossibilité d'extraction n'est pas une preuve négative.

Les deux fréquences paired RX du canal 79, **156.975 / 161.575 MHz**, étaient déjà dans la recherche Bretagne : aucun delta mémoire RF.

## Bretagne — CROSS Étel canal 64

Nouveau dossier : `research/bretagne-v0.1/etel-channel64-evidence.json`.

Le canal 64 est désormais classé **conflit primaire actuel**, pas simplement « site inconnu » :

- la page ministérielle actuelle, mise à jour le **19 juin 2026**, affirme que les canaux **63 et 64** diffusent un bulletin côtier permanent notamment dans le Morbihan ;
- la page actuelle du CROSS Étel nomme Étel en diffusion continue sur **63** ;
- le planning météo actuellement lié par le CROSS liste les émetteurs/canaux et ne mentionne pas 64 ;
- le bilan officiel 2025, publié en mars 2026, décrit **16 stations VHF + 2 MF**, nomme les émetteurs météo réguliers et les stations renforcées **Étel/Chassiron/Ferret sur 63**, sans mention de canal 64.

Cette divergence entre sources primaires actuelles doit être réconciliée. L'absence de 64 dans les documents locaux actuels **ne prouve pas son arrêt** et ne permet pas d'attribuer le canal à Étel, Groix, Belle-Ile, Penmarc'h ou un autre site.

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
- un conflit entre sources primaires actuelles doit être réconcilié avant promotion ;
- l'absence d'une donnée dans un document local courant n'est pas automatiquement une preuve d'arrêt ;
- une source primaire identifiée mais non extractible n'est pas une preuve négative ;
- une source périmée bloque la revue mais ne prouve jamais un arrêt ;
- une recherche infructueuse n'est pas une preuve négative ;
- une fréquence non résolue n'est jamais devinée ;
- des nombres de stations issus de définitions différentes ne sont pas réconciliés sans définition commune ;
- géométrie et rayon annoncé ne sont pas des preuves de réception ;
- toutes les mémoires restent RX-only avec `Duplex=off` et `Offset=0.000000` ;
- une porte non franchie reste hors candidat ;
- snapshot, manifeste, drift check, preview, diff, audit et dry-run sont non destructifs et non publics ;
- **integrity_ok** ou un drift propre ne signifie jamais **release_ready** ;
- revue finale, plan mémoire final et changement explicite du registre public restent obligatoires avant publication.
