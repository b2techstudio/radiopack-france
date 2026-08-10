# RadioPack France — point de reprise

Dernière mise à jour : **10 août 2026**  
Sprint courant : **39**  
État logique : **0.21.28**

Ce fichier sert de point de reprise humain. L'état machine correspondant est dans `research/project-resume-state.json`.

## État public

- **Normandie v0.3.1** : 139 mémoires RX, publiée et immuable.
- **Annecy–Alpes–Léman v0.2** : 65 mémoires RX, variante 48 sans aviation, publiée et immuable.
- **Bretagne v0.1** : recherche uniquement, aucune publication.

Le générateur public ne doit proposer que les versions effectivement publiées.

## Travail actif — Normandie v0.4

Normandie v0.4 reste **non publique**. Le candidat interne reproductible contient **142 mémoires** :

- les 139 mémoires de Normandie v0.3.1 conservées comme base immuable ;
- `50-ZHY-IN` — 145.0875 MHz — location interne provisoire 175 ;
- `53-ZCE-IN` — 145.1000 MHz — location interne provisoire 176 ;
- `50-ZBL-U` — 431.2500 MHz — location interne provisoire 177.

Les locations 175–177 ne définissent pas la numérotation publique finale.

Les trois portes connues peuvent ajouter au maximum **5 mémoires supplémentaires** si elles sont toutes réellement levées, soit un plafond de travail connu de **147 mémoires**. Ce nombre n'est pas une taille publique finale et n'inclut pas F6ZES tant qu'aucune fréquence exploitable n'est vérifiée.

## Portes encore bloquées

### R3 / F1ZBX Brocéliande

- 145.075 MHz : entrée RX opportuniste ;
- 145.675 MHz : sortie RX, sonde principale de couverture ;
- paramètres opérateur ARA35 confirmés ;
- réception réelle depuis Mortain-Bocage non encore démontrée ;
- au moins deux sessions RX indépendantes, identifiées et suffisamment intelligibles sont nécessaires ;
- delta connu si la porte passe : **+2 mémoires**.

### F5ZHA Laval

- paire REF actuelle : 145.4675 / 432.575 MHz ;
- RepeaterBook conserve l'ancienne valeur conflictuelle 431.4125 MHz ;
- le centre du locator `IN98OB86BQ` est à environ **65,6 km** de la référence Mortain ;
- cette géométrie ne vaut jamais preuve de réception ;
- un mini-pack RX-only de diagnostic est disponible avec `ZHA-VHF`, `ZHA-UHF` et `ZHA-OLD` ;
- `ZHA-OLD` est une sonde diagnostique uniquement et ne remplace jamais la paire REF actuelle ;
- le conflit de source et la pertinence/couverture locale restent à fermer avant promotion ;
- delta connu si la porte passe : **+2 mémoires**.

### F1ZOV Équeurdreville-Hainneville

- paire vérifiée : 430.375 / 431.975 MHz ;
- le Radio Club Nord Cotentin marque encore F1ZOV **En Maintenance** ;
- 431.975 MHz reste bloquée tant que l'exploitant local ne confirme pas le retour en service ;
- delta connu si la porte passe : **+1 mémoire**.

### F6ZES Sourdeval

Le REF confirme le site de Sourdeval, F1SMB, le locator IN98MR93XV et l'altitude 230 m, mais aucune fréquence ou mode exploitable n'est fourni. Aucune fréquence ne doit être devinée.

F6ZES reste donc **hors du plafond 147** : tant que sa fréquence n'est pas résolue, son éventuel delta mémoire n'est pas chiffrable.

## Nouveaux outils Sprints 35–39

```text
research/normandie-v0.4/f5zha-mortain-validation.json
tools/build_normandie_v04_f5zha_validation_pack.py
tools/build_normandie_v04_readiness_report.py
tools/build_normandie_v04_promotion_scenarios.py
tests/test_normandie_v04_readiness.py
```

Le readiness report combine les portes connues, les revalidations externes et le candidat interne. La matrice de scénarios calcule les **8 combinaisons** possibles des trois portes connues, de 142 à 147 mémoires, sans jamais produire d'autorisation de publication.

## Fichiers de vérité

```text
research/project-resume-state.json
research/normandie-v0.4/pack-plan.json
research/normandie-v0.4/candidate-memory-delta.json
research/normandie-v0.4/internal-candidate-map.json
research/normandie-v0.4/promotion-gates.json
research/normandie-v0.4/blocked-station-revalidation.json
research/normandie-v0.4/r3-mortain-field-validation.json
research/normandie-v0.4/r3-validation-pack.json
research/normandie-v0.4/f5zha-mortain-validation.json
```

## Reprendre le projet en local

Mettre le dépôt à jour :

```powershell
git pull --ff-only
```

Lancer la passe de contrôles Normandie v0.4 :

```powershell
python tools\run_normandie_v04_checks.py
```

Contrôle étendu :

```powershell
python tools\run_normandie_v04_checks.py --extended
```

Générer le mini-pack R3 :

```powershell
python tools\build_normandie_v04_r3_validation_pack.py
```

Générer le mini-pack diagnostic F5ZHA :

```powershell
python tools\build_normandie_v04_f5zha_validation_pack.py
```

Afficher l'état des portes :

```powershell
python tools\check_normandie_v04_promotion_gates.py
```

Générer le rapport local des portes :

```powershell
python tools\build_normandie_v04_gate_report.py
```

Générer le readiness report :

```powershell
python tools\build_normandie_v04_readiness_report.py
```

Générer les scénarios de promotion connus :

```powershell
python tools\build_normandie_v04_promotion_scenarios.py
```

Aide pour enregistrer une observation terrain R3 :

```powershell
python tools\record_normandie_v04_r3_observation.py --help
```

## Règles de reprise

- ne jamais réécrire une version publiée ;
- ne jamais promouvoir une fréquence uniquement pour remplir un pack ;
- une recherche infructueuse n'est pas une preuve d'arrêt ou d'absence ;
- la géométrie et un rayon annoncé ne sont pas une preuve de réception ;
- pour un statut opérationnel courant, l'exploitant local prime sur un annuaire général ;
- une fréquence historique conflictuelle peut servir de sonde de diagnostic RX mais ne remplace pas une source courante autoritative ;
- toutes les mémoires exportées restent RX-only avec TX bloqué ;
- une porte non franchie reste hors candidat/publication ;
- un scénario calculé n'est ni une promotion ni une publication ;
- la taille publique finale reste indéfinie tant que la revue finale n'est pas explicitement terminée.
