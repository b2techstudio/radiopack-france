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

## Blocs à inventorier

1. socle national RX ;
2. radioamateur analogique France ;
3. radioamateur analogique Suisse ;
4. aviation France ;
5. aviation Suisse ;
6. lacs et navigation publique ;
7. satellites et balises analogiques utiles ;
8. usages locaux publics et vérifiables.

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

L'OFCOM indique que l'exploitation d'installations radio sur les lacs suisses, y compris le Léman, relève d'une concession de radiocommunication mobile terrestre ; une licence de station de navire n'y est pas valable. Cette règle interdit de recopier automatiquement le plan VHF maritime dans le pack. Toute mémoire lacustre doit être justifiée par une source publique spécifique.

## Conflits ouverts

- `F1ZJV` reste hors production : le REF national le classe en DMR/C4FM alors que le REF74 décrit encore un fonctionnement analogique.
- `F1ZYT` ne dispose pas d'une ligne technique complète et récente dans la base nationale ; il reste hors production.

Le détail est conservé dans `conflicts.csv`.

## Tests

Depuis la racine du dépôt :

```powershell
python tests\test_annecy_research.py
```

Résultat attendu :

```text
Tests Annecy–Alpes–Léman research: OK
```

La CI exécute également ce test à chaque push et publie le statut combiné `radiopack-ci/complete`.
