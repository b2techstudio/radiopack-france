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

## Avancement au 8 août 2026

### Radioamateur France

Le fichier `radioamateur-france-inventory.json` contient :

- 19 fréquences analogiques uniques ;
- des sorties actives en 2 m et 70 cm pour les départements 01, 38, 73 et 74 ;
- quatre regroupements de fréquences partagées afin d'éviter les doublons ;
- les deux sorties analogiques des transpondeurs transparents lorsque les deux sont utiles à l'écoute ;
- uniquement des lignes `NFM` et `rx_only`.

Ce fichier reste un inventaire de recherche et n'est pas lu par le générateur public.

### Radioamateur Suisse

Le fichier `radioamateur-switzerland-candidates.json` sépare les niveaux de confiance :

- Genève : HB9G 145.725 MHz et 439.100 MHz sont recoupés avec les pages du club ;
- Vaud : HB9MM 145.600 MHz et 438.850 MHz demandent encore une confirmation récente de l'exploitant ;
- Valais : les quatre fréquences historiques HB9Y restent en attente de recoupement actuel.

Aucune candidate suisse non recoupée ne passe dans le candidat interne.

### Aviation France — AIRAC 08/26

Le cycle AIRAC 08/26 est effectif depuis le 6 août 2026. Le fichier `aviation-france-airac-08.json` contient sept mémoires actuellement recoupées sur les publications officielles publiques :

- Annecy-Meythet : 118.200 MHz ;
- Annemasse : 125.875 MHz ;
- Grenoble-Le Versoud : 121.000 MHz ;
- Grenoble-Alpes-Isère : 121.930, 119.300 et 133.855 MHz ;
- Genève Information : 126.350 MHz pour le bassin transfrontalier.

Toutes ces lignes sont en `AM`, au pas de 8.33 kHz, en `rx_only` et portent le statut `verified_airac08_public`.

Le pré-inventaire `aviation-france-pre-airac-08.json` est conservé pour l'historique mais reste explicitement interdit à l'assembleur.

Restent en attente :

- Chambéry Aix-les-Bains : les quatre fréquences du pré-inventaire ne sont pas réutilisées automatiquement ;
- Albertville ;
- Megève.

Sallanches-Mont-Blanc n'est plus une ligne en attente : l'aérodrome est classé `excluded_closed_aerodrome`, car sa fermeture à toute circulation aérienne est effective depuis le 1er septembre 2020. Aucune fréquence active ne doit être recherchée ou réintroduite pour LFHZ.

### Aviation Suisse

Le fichier `aviation-switzerland-airac-08.json` contient désormais six fréquences recoupées publiquement :

- Lausanne LSGL AD : 123.205 MHz ;
- Lausanne APCH INFO : 118.830 MHz ;
- Sion Ground : 121.705 MHz ;
- Sion Tower : 118.275 MHz ;
- Sion ATIS : 130.630 MHz ;
- Sion Approach : 126.825 MHz.

Les quatre fréquences Sion proviennent de la page officielle « Infos pilotes » de l'Aéroport de Sion. Les fréquences de handling 131.475, 131.670 et 131.955 MHz ainsi que les aides de radionavigation ILS 110.7 MHz et VOR SION 112.15 MHz sont explicitement exclues du bloc ATS/ATIS.

L'OFAC documente l'espacement de canaux VHF 8.33 kHz applicable à l'aviation suisse ; les six lignes sont donc modélisées en `AM`, pas `8.33`, et `rx_only`.

Genève-aéroport reste hors candidat tant que ses tableaux fréquentiels courants ne sont pas recoupables publiquement avec un niveau de confiance suffisant. Genève Information 126.350 MHz n'est mémorisée qu'une seule fois, dans le bloc France / bassin genevois, afin d'éviter un doublon.

### Lacs et navigation

Le fichier `navigation-lakes-findings.json` aboutit toujours à zéro mémoire publique :

- aucun plan VHF maritime général n'est copié pour le Léman ;
- AIS 1 sur 161.975 MHz et AIS 2 sur 162.025 MHz sont exclus des lacs suisses ;
- le canal 16 sur 156.800 MHz reste un cas conditionnel lié à une concession et à la navigation au radar, pas une mémoire du pack public général ;
- les réseaux professionnels concédés autour de 173 MHz sont exclus ;
- les pages officielles des lacs d'Annecy et du Bourget sont référencées, sans fréquence publique générale identifiée dans les pages consultées ;
- Aiguebelette reste en attente d'une source officielle spécifique à la radio de navigation.

### Satellites FM et candidat interne

Le fichier `satellites-fm-inventory.json` conserve trois descendantes analogiques documentées par AMSAT :

- SO-50 : 436.795 MHz, avec montée 145.850 MHz et CTCSS 67 Hz ;
- AO-91 : 145.960 MHz, avec montée 435.250 MHz, utilisable seulement lorsque le satellite est éclairé ;
- AO-123 : 435.400 MHz, avec montée 145.850 MHz et CTCSS 67 Hz.

Comme pour l'ISS, seule la liaison descendante devient une mémoire d'écoute. Les montantes restent des métadonnées.

Le script `tools/build_annecy_internal_candidate.py` assemble désormais un candidat interne de 61 mémoires :

- 16 PMR446 ;
- 6 APRS/ISS ;
- 3 satellites FM ;
- 2 canaux d'appel ;
- 19 fréquences radioamateur françaises ;
- 2 relais radioamateur suisses `verified_current` ;
- 7 fréquences aviation France / bassin genevois ;
- 6 fréquences aviation Suisse : 2 Lausanne et 4 Sion.

Le résultat est généré localement sous `research/annecy-alpes-leman-v0.2/generated/`, avec `public_export_allowed: false`. Ce dossier est ignoré par Git. Les lacs et toutes les lignes en attente, exclues ou en conflit restent hors candidat.

## Blocs restant à inventorier ou recouper

1. Chambéry, Albertville et Megève ;
2. Genève-aéroport ;
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

## Aviation — règle après AIRAC 08/26

Le gel global du 4 août est levé uniquement pour les lignes qui ont franchi les portes de validation. Une fréquence du pré-inventaire AIRAC 07/26 n'est jamais promue automatiquement parce que le cycle a changé : elle doit disposer d'un recoupement courant et d'un statut explicitement autorisé par l'assembleur.

Le contrôle NOTAM reste une porte séparée de pré-publication. Les pages officielles consultées renvoient vers les services NOTAM/Skybriefing, mais aucun état « aucun NOTAM impactant » n'est enregistré automatiquement dans le dépôt. Tant que ce contrôle opérationnel n'est pas explicitement effectué et daté, le candidat reste non publiable.

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
python tests\test_annecy_airac08.py
python tests\test_annecy_internal_candidate.py
```

Résultats attendus :

```text
Tests Annecy–Alpes–Léman research: OK
Tests Annecy–Alpes–Léman aviation/lakes research: OK
Tests Annecy–Alpes–Léman AIRAC 08 aviation: OK
Tests Annecy–Alpes–Léman internal candidate: OK
```

La CI exécute ces tests à chaque push et publie le statut combiné `radiopack-ci/complete`.
