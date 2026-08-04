# RadioPack France — Sprint 10

Ce sprint transforme les recherches validées d'Annecy–Alpes–Léman v0.2 en un candidat interne strictement non publiable.

## Résultat

Le candidat interne contient 48 mémoires :

```text
000–015  PMR446                    16
020–025  APRS / ISS                 6
026–028  Satellites FM              3
030–031  Canaux d'appel             2
040–058  Radioamateur France       19
090–091  Radioamateur Suisse        2
Total                              48
```

Les plages aviation, navigation lacustre et réserves restent vides.

## Satellites retenus

### SO-50

- montée : 145.850 MHz ;
- CTCSS d'accès : 67 Hz ;
- activation : 74.4 Hz ;
- descente mémorisée : 436.795 MHz.

### AO-91

- montée : 435.250 MHz ;
- descente mémorisée : 145.960 MHz ;
- fonctionnement limité aux passages éclairés à cause de l'état de la batterie.

### AO-123

- montée : 145.850 MHz ;
- CTCSS : 67 Hz ;
- descente mémorisée : 435.400 MHz.

Dans tous les cas, la montée est une métadonnée. Seule la descente est écrite dans le CSV RX-only.

## Satellites reportés

- PO-101 : AMSAT le signale en déclin et activé selon calendrier ;
- CAS-3H : transpondeur sans calendrier fixe ;
- IO-86 : orbite limitée à environ ±30°, donc non adaptée à Annecy ;
- RS95S : phase de test ;
- TEVEL2 : état variable entre plusieurs satellites partageant la même fréquence.

## Assembleur interne

Le script suivant construit le candidat :

```powershell
python tools\build_annecy_internal_candidate.py
```

Sorties locales ignorées par Git :

```text
research/annecy-alpes-leman-v0.2/generated/annecy-alpes-leman-v0.2-internal.json
research/annecy-alpes-leman-v0.2/generated/annecy-alpes-leman-v0.2-internal.csv
```

Les sorties portent les garde-fous suivants :

- `status: internal_candidate_not_for_publication` ;
- `public_export_allowed: false` ;
- `Duplex=off` sur chaque mémoire ;
- aucune source aviation ;
- aucune source lacustre ;
- uniquement les relais suisses `verified_current` ;
- aucune montante ISS ou satellite exportée comme mémoire séparée.

## Tests

```powershell
python tests\test_annecy_internal_candidate.py
```

Résultat attendu :

```text
Tests Annecy–Alpes–Léman internal candidate: OK
```

La CI reconstruit le candidat dans un répertoire temporaire, vérifie son contenu, puis le supprime sans publier d'artefact interne. Elle exécute également ce test avec les autres contrôles du dépôt.

## Ce que ce sprint ne fait pas

- aucune publication Annecy v0.2 ;
- aucun lien de téléchargement public ;
- aucune modification du générateur public ;
- aucune intégration des fréquences aviation avant AIRAC 08/26 ;
- aucune fréquence lacustre ;
- aucun remplissage artificiel pour atteindre un nombre cible.

## Étape suivante

À partir du 6 août 2026, revalider l'aviation France et Suisse, puis reconstruire le candidat interne. Le passage vers un pack public ne sera possible qu'après validation complète, tests et revue du guide.
