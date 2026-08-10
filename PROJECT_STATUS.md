# RadioPack France — point de reprise

Dernière mise à jour : **10 août 2026**  
Sprint courant : **34**  
État logique : **0.21.23**

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

## Portes encore bloquées

### R3 / F1ZBX Brocéliande

- 145.075 MHz : entrée RX opportuniste ;
- 145.675 MHz : sortie RX, sonde principale de couverture ;
- paramètres opérateur ARA35 confirmés ;
- réception réelle depuis Mortain-Bocage non encore démontrée ;
- au moins deux sessions RX indépendantes, identifiées et suffisamment intelligibles sont nécessaires.

### F5ZHA Laval

- paire de recherche : 145.4675 / 432.575 MHz ;
- REF et `manuel.la-radio.eu` concordent ;
- RepeaterBook conserve 431.4125 MHz ;
- aucune source locale actuelle n'a encore fermé le conflit ;
- pertinence/couverture utile depuis Mortain encore non validée.

### F1ZOV Équeurdreville-Hainneville

- paire vérifiée : 430.375 / 431.975 MHz ;
- le Radio Club Nord Cotentin marque encore F1ZOV **En Maintenance** ;
- 431.975 MHz reste bloquée tant que l'exploitant local ne confirme pas le retour en service.

### F6ZES Sourdeval

Le REF confirme le site de Sourdeval, F1SMB, le locator IN98MR93XV et l'altitude 230 m, mais aucune fréquence ou mode exploitable n'est fourni. Aucune fréquence ne doit être devinée.

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
```

## Reprendre le projet en local

Mettre le dépôt à jour :

```powershell
git pull origin main
```

Lancer la passe de contrôles Normandie v0.4 :

```powershell
python tools\run_normandie_v04_checks.py
```

Générer le mini-pack R3 :

```powershell
python tools\build_normandie_v04_r3_validation_pack.py
```

Afficher l'état des portes :

```powershell
python tools\check_normandie_v04_promotion_gates.py
```

Générer le rapport local lisible :

```powershell
python tools\build_normandie_v04_gate_report.py
```

Aide pour enregistrer une observation terrain :

```powershell
python tools\record_normandie_v04_r3_observation.py --help
```

## Règles de reprise

- ne jamais réécrire une version publiée ;
- ne jamais promouvoir une fréquence uniquement pour remplir un pack ;
- une recherche infructueuse n'est pas une preuve d'arrêt ou d'absence ;
- la géométrie et un rayon annoncé ne sont pas une preuve de réception ;
- pour un statut opérationnel courant, l'exploitant local prime sur un annuaire général ;
- toutes les mémoires exportées restent RX-only avec TX bloqué ;
- une porte non franchie reste hors candidat/publication.
