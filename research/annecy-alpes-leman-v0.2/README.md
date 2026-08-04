# Annecy–Alpes–Léman v0.2 — base de recherche

Cette arborescence démarre la reconstruction sans publier de fréquence non recoupée.

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

Les blocs français et suisses doivent rester séparés dans les noms, la documentation et le futur plan mémoire.

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

## Conflit déjà ouvert

F1ZJV reste hors production tant que son statut analogique ou numérique n'est pas recoupé entre la base nationale et la source locale.
