# RadioPack France — Sprints 30 à 34

Date : **10 août 2026**

Cette passe prolonge le Sprint 29 sans modifier aucun pack public. Normandie v0.3.1 reste figée à 139 mémoires ; le candidat interne Normandie v0.4 reste à 142 mémoires et n'est pas une prépublication.

## Sprint 30 — 0.21.19 — revalidation des portes externes

Ajout de `research/normandie-v0.4/blocked-station-revalidation.json`.

Recontrôle courant :

- **R3 / F1ZBX** : l'ARA35 confirme le relais opérationnel et la paire 145.075 / 145.675 MHz ; aucune preuve de réception réelle depuis Mortain-Bocage n'est déduite de la page opérateur ;
- **F5ZHA Laval** : REF et `manuel.la-radio.eu` concordent sur 145.4675 / 432.575 MHz, RepeaterBook conserve 431.4125 MHz ; aucune source locale actuelle trouvée ne ferme encore le conflit ;
- **F1ZOV** : le Radio Club Nord Cotentin marque toujours le relais **En Maintenance** et confirme 430.375 / 431.975 MHz ;
- **F6ZES Sourdeval** : le REF confirme le site, F1SMB, IN98MR93XV et 230 m, mais toujours aucune fréquence ou mode exploitable.

Aucune fréquence bloquée n'est promue.

## Sprint 31 — 0.21.20 — enregistreur terrain R3

Ajout de `tools/record_normandie_v04_r3_observation.py`.

L'outil :

- enregistre une observation directement dans `r3-mortain-field-validation.json` ;
- n'accepte que les fréquences du mini-pack de validation ;
- contrôle l'intelligibilité 0–5 et le niveau de confiance d'identification ;
- impose cohérence `no-signal => intelligibilité 0 + confidence none` ;
- effectue une écriture atomique ;
- ne modifie aucune donnée publique et ne promeut automatiquement aucune fréquence.

## Sprint 32 — 0.21.21 — rapport local des portes

Ajout de `tools/build_normandie_v04_gate_report.py`.

Le générateur combine le checker existant et l'instantané de revalidation pour produire localement, dans le dossier `generated/` ignoré par Git :

- un rapport JSON ;
- un rapport Markdown lisible ;
- le nombre de sessions R3 valides ;
- l'état de F5ZHA et F1ZOV ;
- la priorité F6ZES ;
- la prochaine action associée à chaque blocage.

Le rapport reste explicitement non public.

## Sprint 33 — 0.21.22 — reprise autonome du projet

Ajout de :

- `research/project-resume-state.json` — état machine du projet ;
- `PROJECT_STATUS.md` — état humain et commandes de reprise.

Ils figent le point de reprise à partir des données du dépôt : versions publiques, candidat interne 142 mémoires, cinq fréquences bloquées, F6ZES non résolu, sources de vérité et commandes locales.

L'objectif est qu'une perte de conversation ne bloque plus la reprise : le dépôt contient désormais son propre état de travail explicite.

## Sprint 34 — 0.21.23 — contrôle local et CI

Ajout de :

- `tools/run_normandie_v04_checks.py` — commande unique pour les contrôles Normandie v0.4 ;
- `tests/test_normandie_v04_field_tools.py` — tests de l'instantané externe, de l'enregistreur, du rapport et du mécanisme de reprise ;
- une étape GitHub Actions dédiée aux outils terrain/reprise ;
- extension rétrocompatible de `research/normandie-v0.4/pack-plan.json` en conservant le schéma 1.1, avec liens vers les nouveaux outils ;
- renforcement de `tests/test_normandie_v04_candidate_delta.py` afin de garder ces liens cohérents ;
- conservation explicite du contrat de schéma 1.1 déjà contrôlé par `tests/test_site_files.py`.

Commande locale principale :

```powershell
python tools\run_normandie_v04_checks.py
```

Contrôles étendus :

```powershell
python tools\run_normandie_v04_checks.py --extended
```

## État à la fin de la passe

- Normandie v0.3.1 publique : **139 mémoires**, inchangée ;
- Normandie v0.4 candidat interne : **142 mémoires**, inchangé ;
- ajouts internes actuels : **3** ;
- fréquences encore bloquées : **5** ;
- R3 : test terrain Mortain toujours requis ;
- F5ZHA : conflit source + pertinence/couverture toujours ouverts ;
- F1ZOV : maintenance toujours bloquante ;
- F6ZES : fréquence toujours non résolue ;
- publication Normandie v0.4 : **interdite**.
