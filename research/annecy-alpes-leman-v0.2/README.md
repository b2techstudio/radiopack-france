# Annecy–Alpes–Léman v0.2 — base de recherche

Cette arborescence prépare la reconstruction sans publier de fréquence non recoupée.

## Périmètre

### France

- Haute-Savoie (74)
- Savoie (73)
- Ain (01)
- Isère (38)
- zones voisines uniquement si l'audibilité et l'intérêt régional sont documentés

### Suisse

- Genève
- Vaud
- Valais

Les blocs français et suisses restent séparés dans les noms, la documentation et le futur plan mémoire.

## Avancement au 4 août 2026

### Radioamateur France

Le fichier `radioamateur-france-inventory.json` contient désormais :

- 19 fréquences analogiques uniques ;
- des sorties actives en 2 m et 70 cm pour les départements 01, 38, 73 et 74 ;
- quatre regroupements de fréquences partagées afin d'éviter les doublons ;
- les deux sorties analogiques des transpondeurs transparents lorsque les deux sont utiles à l'écoute ;
- uniquement des lignes `NFM` et `rx_only`.

Ce fichier reste un inventaire de recherche et n'est pas encore lu par le générateur public.

### Radioamateur Suisse

Le fichier `radioamateur-switzerland-candidates.json` sépare les niveaux de confiance :

- Genève : HB9G 145.725 MHz et 439.100 MHz sont recoupés avec les pages du club ;
- Vaud : HB9MM 145.600 MHz et 438.850 MHz demandent encore une confirmation récente de l'exploitant ;
- Valais : les quatre fréquences historiques HB9Y restent en attente de recoupement actuel.

Aucune candidate suisse non recoupée ne doit passer dans un JSON de production.

### Aviation France — pré-inventaire

Le fichier `aviation-france-pre-airac-08.json` contient 11 fréquences uniques du cycle AIRAC 07/26 :

- Annecy-Meythet ;
- Annemasse ;
- Chambéry Aix-les-Bains ;
- Grenoble Le Versoud ;
- Grenoble Alpes Isère ;
- Genève Information pour le bassin frontalier.

Toutes les lignes sont en `AM`, en `rx_only` et portent le statut `pre_airac_recheck`.

Le cycle AIRAC 07/26 reste valable jusqu'au 5 août 2026 inclus. Aucune de ces fréquences ne peut passer en production avant contrôle dans l'AIRAC 08/26 effectif à partir du 6 août 2026. Albertville, Megève et Sallanches restent à extraire depuis les publications officielles.

### Lacs et navigation

Le fichier `navigation-lakes-findings.json` aboutit actuellement à zéro mémoire publique :

- aucun plan VHF maritime général n'est copié pour le Léman ;
- AIS 1 sur 161.975 MHz et AIS 2 sur 162.025 MHz sont exclus des lacs suisses ;
- le canal 16 sur 156.800 MHz reste un cas conditionnel lié à une concession et à la navigation au radar, pas une mémoire du pack public général ;
- les réseaux professionnels concédés autour de 173 MHz sont exclus ;
- les pages officielles des lacs d'Annecy et du Bourget sont référencées, sans fréquence publique générale identifiée dans les pages consultées ;
- Aiguebelette reste en attente d'une source officielle spécifique à la radio de navigation.

### Satellites FM et candidat interne

Le fichier `satellites-fm-inventory.json` ajoute trois descendantes analogiques documentées par AMSAT :

- SO-50 : 436.795 MHz, avec montée 145.850 MHz et CTCSS 67 Hz ;
- AO-91 : 145.960 MHz, avec montée 435.250 MHz, utilisable seulement lorsque le satellite est éclairé ;
- AO-123 : 435.400 MHz, avec montée 145.850 MHz et CTCSS 67 Hz.

Comme pour l'ISS, seule la liaison descendante devient une mémoire d'écoute. Les montantes restent des métadonnées.

Le script `tools/build_annecy_internal_candidate.py` assemble un candidat interne de 48 mémoires :

- 16 PMR446 ;
- 6 APRS/ISS ;
- 3 satellites FM ;
- 2 canaux d'appel ;
- 19 fréquences radioamateur françaises ;
- 2 relais suisses `verified_current`.

Le résultat est généré localement sous `research/annecy-alpes-leman-v0.2/generated/`, avec `public_export_allowed: false`. Ce dossier est ignoré par Git. L'aviation, les lacs et toutes les lignes en attente ou en conflit restent exclus.

## Blocs restant à inventorier

1. aviation France après AIRAC 08/26 ;
2. aviation Suisse après AIRAC du 6 août 2026 ;
3. balises analogiques réellement utiles ;
4. usages locaux publics et vérifiables ;
5. recoupements radioamateurs suisses encore ouverts.

## Portes de validation

Une ligne ne passe dans le futur JSON de production que si :

- la source est identifiable et datée ;
- le service est public et non sensible ;
- le mode est analogique et recevable par l'UV-K5 ;
- la fréquence n'est pas contradictoire avec une source de même niveau ou plus récente ;
- les fréquences identiques sont fusionnées lorsqu'elles représentent le même usage d'écoute ;
- le commentaire conserve les indicatifs et sites utiles ;
- l'export public reste en `Duplex=off`.

## Aviation — règle de gel

Au 4 août 2026, l'eAIP France AIRAC 07/26 reste en vigueur jusqu'au 5 août inclus et les données AIRAC 08/26 prennent effet le 6 août. La Suisse annonce également une AIRAC AMDT au 6 août 2026. L'extraction aéronautique de production doit donc être gelée sur les publications effectives à partir du 6 août, puis contrôlée avec les NOTAM avant publication.

## Navigation sur les lacs suisses

L'OFCOM indique que l'exploitation d'installations radio sur les lacs suisses, y compris le Léman, relève d'une concession de radiocommunication mobile terrestre ; une licence de station de navire n'y est pas valable. Les équipements maritimes de 57 canaux et l'AIS ne doivent donc pas être transposés dans le pack. Le canal 16 n'est conservé que comme cas de recherche conditionnel.

## Conflits ouverts

- `F1ZJV` reste hors production : le REF national le classe en DMR/C4FM alors que le REF74 décrit encore un fonctionnement analogique.
- `F1ZYT` ne dispose pas d'une ligne technique complète et récente dans la base nationale ; il reste hors production.

Le détail est conservé dans `conflicts.csv`.

## Tests

Depuis la racine du dépôt :

```powershell
python tests\test_annecy_research.py
python tests\test_annecy_aviation_lakes.py
python tests\test_annecy_internal_candidate.py
```

Résultats attendus :

```text
Tests Annecy–Alpes–Léman research: OK
Tests Annecy–Alpes–Léman aviation/lakes research: OK
Tests Annecy–Alpes–Léman internal candidate: OK
```

La CI exécute ces tests à chaque push et publie le statut combiné `radiopack-ci/complete`.
