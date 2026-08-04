# RadioPack France — Sprint 8

Ce sprint construit le premier inventaire structuré d'Annecy–Alpes–Léman v0.2 sans publier prématurément un nouveau pack régional.

## Contenu

- 19 fréquences radioamateur analogiques françaises uniques ;
- départements couverts : Ain, Isère, Savoie et Haute-Savoie ;
- quatre regroupements de fréquences partagées ;
- huit candidats suisses séparés par niveau de confiance ;
- HB9G 145.725 MHz et 439.100 MHz recoupés avec les pages du club ;
- HB9MM et HB9Y maintenus en attente de vérification récente ;
- F1ZJV et F1ZYT maintenus hors production ;
- registre des sources complété ;
- test de recherche automatisé ;
- exécution du nouveau test dans GitHub Actions.

## Ce que ce sprint ne fait pas

- il ne remplace pas le pack Annecy v0.1 ;
- il ne crée pas encore le CSV Annecy–Alpes–Léman v0.2 ;
- il ne rend aucun téléchargement Annecy disponible ;
- il ne modifie pas le générateur public ;
- il ne fige pas les fréquences aviation avant l'AIRAC du 6 août 2026 ;
- il ne publie aucune fréquence suisse non recoupée.

## Fichiers principaux

```text
research/annecy-alpes-leman-v0.2/radioamateur-france-inventory.json
research/annecy-alpes-leman-v0.2/radioamateur-switzerland-candidates.json
research/annecy-alpes-leman-v0.2/source-register.csv
research/annecy-alpes-leman-v0.2/conflicts.csv
research/annecy-alpes-leman-v0.2/README.md
tests/test_annecy_research.py
tests/test_site_files.py
.github/workflows/ci.yml
CHANGELOG.md
```

## Synchronisation locale

```powershell
cd "C:\Users\cross\Documents\CODE\PROJETS\RadioPack-France"
git pull
```

## Tests

```powershell
python generator\generate_chirp_csv.py
python tests\test_generator.py
python tests\test_site_files.py
python tests\test_annecy_research.py

cd website
npm run build
```

Résultats attendus :

```text
Tests RadioPack Sprint 5: OK
Tests RadioPack Sprint 8: OK
Tests Annecy–Alpes–Léman research: OK
```

Le build Astro doit se terminer sans erreur.

## Publication

Les fichiers de ce sprint sont déjà versionnés sur la branche `main`. Le statut GitHub Actions attendu est :

```text
radiopack-ci/complete — success
```

Cloudflare Pages peut se redéployer après les commits, mais la présentation publique d'Annecy reste volontairement sur « En préparation ».

## Étape suivante

Après prise d'effet de l'AIRAC du 6 août 2026 :

1. relever l'aviation française depuis l'eAIP SIA effectif ;
2. relever l'aviation suisse depuis l'AIP Skyguide effectif ;
3. recouper HB9MM et HB9Y avec les exploitants ou leurs publications récentes ;
4. étudier les fréquences publiques spécifiques aux lacs sans recopier le plan maritime ;
5. assembler un premier plan mémoire v0.2 sans dépasser les données réellement validées.
