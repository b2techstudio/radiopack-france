# RadioPack France — Sprint 9

Ce sprint prépare les blocs aviation et navigation lacustre d'Annecy–Alpes–Léman v0.2 sans publier prématurément de nouveau CSV régional.

## Aviation France

Le fichier `research/annecy-alpes-leman-v0.2/aviation-france-pre-airac-08.json` contient 11 fréquences uniques issues des publications officielles disponibles au 4 août 2026 :

- Annecy-Meythet : 118.200 MHz ;
- Annemasse : 125.875 MHz ;
- Chambéry : 123.700, 121.205, 118.300 et 127.100 MHz ;
- Grenoble-Le Versoud : 121.000 MHz ;
- Grenoble-Alpes-Isère : 121.930, 119.300 et 133.855 MHz ;
- Genève Information : 126.350 MHz.

Toutes les lignes sont :

- en mode `AM` ;
- au pas de 8.33 kHz ;
- en réception seule ;
- marquées `pre_airac_recheck` ;
- non utilisées par le générateur public.

L'AIRAC 07/26 reste en vigueur jusqu'au 5 août 2026 inclus. Le passage en production est interdit avant contrôle dans les publications AIRAC 08/26 effectives le 6 août 2026.

Albertville, Megève et Sallanches restent en attente d'extraction officielle.

## Navigation lacustre

Le fichier `research/annecy-alpes-leman-v0.2/navigation-lakes-findings.json` contient les conclusions suivantes :

- aucune fréquence lacustre n'est actuellement validée pour le pack public ;
- le plan VHF maritime de 57 canaux n'est pas transposé aux lacs suisses ;
- AIS 1 sur 161.975 MHz et AIS 2 sur 162.025 MHz sont exclus des lacs suisses ;
- le canal 16 sur 156.800 MHz est conservé uniquement comme cas conditionnel lié à une concession et à la navigation au radar ;
- les fréquences professionnelles ou événementielles concédées autour de 173 MHz sont exclues ;
- aucune fréquence publique générale n'a été identifiée dans les pages officielles consultées pour Annecy et le Bourget ;
- Aiguebelette reste en attente d'une source officielle spécifique.

Le résultat du bloc lacustre reste donc volontairement à zéro mémoire.

## Fichiers ajoutés

```text
research/annecy-alpes-leman-v0.2/aviation-france-pre-airac-08.json
research/annecy-alpes-leman-v0.2/navigation-lakes-findings.json
tests/test_annecy_aviation_lakes.py
SPRINT-9-AVIATION-LAKES-RESEARCH.md
```

## Fichiers remplacés

```text
.github/workflows/ci.yml
CHANGELOG.md
research/annecy-alpes-leman-v0.2/README.md
research/annecy-alpes-leman-v0.2/source-register.csv
tests/test_site_files.py
```

## Ce que ce sprint ne modifie pas

- le générateur CSV public ;
- les anciens fichiers Annecy v0.1 ;
- le pack Normandie ;
- les pages publiques ;
- les guides PDF ;
- le statut « En préparation » d'Annecy–Alpes–Léman v0.2.

## Synchronisation locale

```powershell
cd "C:\Users\cross\Documents\CODE\PROJETS\RadioPack-France"
git pull
git status
```

## Tests

```powershell
python generator\generate_chirp_csv.py
python tests\test_generator.py
python tests\test_site_files.py
python tests\test_annecy_research.py
python tests\test_annecy_aviation_lakes.py

cd website
npm run build
```

Résultats attendus :

```text
Tests RadioPack Sprint 5: OK
Tests RadioPack Sprint 9: OK
Tests Annecy–Alpes–Léman research: OK
Tests Annecy–Alpes–Léman aviation/lakes research: OK
```

Le build Astro doit se terminer sans erreur.

## Étape suivante

À partir du 6 août 2026 :

1. revalider les 11 fréquences du pré-inventaire dans l'AIRAC 08/26 ;
2. extraire Albertville, Megève et Sallanches ;
3. relever Genève, Lausanne et Sion depuis l'AIP suisse effectif ;
4. vérifier les NOTAM ;
5. assembler les premiers blocs de production uniquement avec les lignes confirmées.
