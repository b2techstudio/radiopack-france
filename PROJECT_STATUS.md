# RadioPack France — point de reprise

Dernière mise à jour : **10 août 2026**  
Sprint courant : **54**  
État logique : **0.21.43**

Ce fichier sert de point de reprise humain. L'état machine correspondant est dans `research/project-resume-state.json`.

## État public

- **Normandie v0.3.1** : 139 mémoires RX, publiée et immuable.
- **Annecy–Alpes–Léman v0.2** : 65 mémoires RX, variante 48 sans aviation, publiée et immuable.
- **Bretagne v0.1** : recherche uniquement, aucune publication.

## Travail actif — Normandie v0.4

Candidat interne reproductible : **142 mémoires**, non public. Les trois portes connues représentent au maximum +5 mémoires, soit un plafond de travail connu à **147 mémoires**. Ce plafond n'est pas la taille publique finale et F6ZES reste hors calcul tant que fréquence et mode ne sont pas résolus.

Ajouts internes actuels : `50-ZHY-IN` 145.0875 MHz (175), `53-ZCE-IN` 145.1000 MHz (176), `50-ZBL-U` 431.2500 MHz (177).

État de revue actuel : **2/9 points complétés**, **7 blocages ouverts**, **0 ajout éligible**, preview **142 mémoires**. L'audit prépublication indique **intégrité OK** mais **release_ready=false**.

## État des dossiers bloqués

- **R3 / F1ZBX** : paramètres opérateur confirmés sur 145.075 / 145.675 MHz ; réception Mortain encore à démontrer par au moins deux sessions indépendantes.
- **F5ZHA Laval** : REF courant sur 145.4675 / 432.575 MHz ; conflit historique 431.4125 encore ouvert et couverture utile Mortain non validée.
- **F1ZOV** : le REF le liste actif, mais l'exploitant local F6KFW l'indique toujours **En Maintenance** ; le statut exploitant local reste prioritaire.
- **F6ZES Sourdeval** : site/responsable/locator connus, mais fréquence, mode et état opérationnel non résolus ; aucune fréquence ne doit être devinée.

## Pipeline Sprints 50–54

```text
research/normandie-v0.4/source-freshness-policy.json
tools/check_normandie_v04_source_freshness.py
tools/build_normandie_v04_review_checklist.py
tools/build_normandie_v04_candidate_diff.py
tools/run_normandie_v04_prepublication_audit.py
tests/test_normandie_v04_prepublication_audit.py
```

La politique de fraîcheur bloque la revue si un état opérateur ou une revalidation devient trop ancien, sans jamais transformer cette ancienneté en preuve d'arrêt. La checklist rend la revue mesurable. Le diff vérifie l'empilement exact **139 → 142 → preview** sans réécriture. L'audit distingue une chaîne techniquement cohérente d'une release réellement prête.

Au **10 août 2026**, les revalidations sont fraîches selon cette politique interne. Cela ne lève aucune porte de promotion.

## Commandes de reprise

```powershell
git pull --ff-only
python tools\run_normandie_v04_checks.py --extended
python tools\check_normandie_v04_source_consistency.py
python tools\check_normandie_v04_source_freshness.py
python tools\build_normandie_v04_review_checklist.py
python tools\build_normandie_v04_candidate_diff.py
python tools\run_normandie_v04_prepublication_audit.py
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
- une source périmée bloque la revue mais ne prouve jamais un arrêt ;
- une fréquence non résolue n'est jamais devinée ;
- géométrie et rayon annoncé ne sont pas des preuves de réception ;
- toutes les mémoires restent RX-only avec `Duplex=off` et `Offset=0.000000` ;
- une porte non franchie reste hors candidat ;
- preview, diff, checklist et audit sont non destructifs et non publics ;
- **integrity_ok** ne signifie jamais **release_ready** ;
- revue finale, plan mémoire final et changement explicite du registre public restent obligatoires avant publication.
