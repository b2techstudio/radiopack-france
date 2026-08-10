# RadioPack France — point de reprise

Dernière mise à jour : **10 août 2026**  
Sprint courant : **44**  
État logique : **0.21.33**

Ce fichier sert de point de reprise humain. L'état machine correspondant est dans `research/project-resume-state.json`.

## État public

- **Normandie v0.3.1** : 139 mémoires RX, publiée et immuable.
- **Annecy–Alpes–Léman v0.2** : 65 mémoires RX, variante 48 sans aviation, publiée et immuable.
- **Bretagne v0.1** : recherche uniquement, aucune publication.

## Travail actif — Normandie v0.4

Candidat interne reproductible : **142 mémoires**, non public.

Ajouts internes actuels :

- `50-ZHY-IN` — 145.0875 MHz — location provisoire 175 ;
- `53-ZCE-IN` — 145.1000 MHz — location provisoire 176 ;
- `50-ZBL-U` — 431.2500 MHz — location provisoire 177.

Les trois portes connues peuvent ajouter au maximum 5 mémoires, soit un plafond de travail connu à **147 mémoires**. Ce plafond n'est pas la taille publique finale et F6ZES reste hors calcul tant qu'aucune fréquence exploitable n'est résolue.

## Portes encore fermées

- **R3 / F1ZBX** : 145.075 / 145.675 MHz ; au moins deux sessions RX Mortain identifiées et intelligibles sont requises.
- **F5ZHA Laval** : 145.4675 / 432.575 MHz ; couverture locale utile + réconciliation autoritative du conflit de source requises. Les observations terrain ne peuvent jamais fermer le conflit.
- **F1ZOV** : 431.975 MHz ; l'exploitant local marque toujours le relais En Maintenance.
- **F6ZES Sourdeval** : site connu, fréquence et mode toujours non résolus ; aucune valeur ne doit être devinée.

## Pipeline Sprints 40–44

```text
research/normandie-v0.4/f5zha-mortain-validation.json
research/normandie-v0.4/external-evidence-matrix.json
tools/record_normandie_v04_f5zha_observation.py
tools/build_normandie_v04_evidence_report.py
tools/build_normandie_v04_internal_promotion_plan.py
tests/test_normandie_v04_evidence_pipeline.py
```

Le plan de promotion interne est **non destructif** : il ne propose que les ajouts d'une porte réellement franchie, n'applique jamais le plan automatiquement et ne publie rien. À l'état Sprint 44 : **0 ajout éligible**, candidat inchangé à 142 mémoires.

## Commandes de reprise

```powershell
git pull --ff-only
python tools\run_normandie_v04_checks.py --extended
python tools\build_normandie_v04_evidence_report.py
python tools\build_normandie_v04_internal_promotion_plan.py
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
- ne jamais promouvoir une fréquence pour remplir un pack ;
- une recherche infructueuse n'est pas une preuve d'arrêt ;
- la géométrie n'est pas une preuve de réception ;
- le statut opérateur local prime pour l'état opérationnel courant ;
- une observation radio ne ferme pas un conflit de source ;
- une fréquence non résolue n'est jamais devinée ;
- toutes les mémoires restent RX-only ;
- une porte non franchie reste hors candidat ;
- un plan ou scénario généré n'est ni une promotion ni une publication.
