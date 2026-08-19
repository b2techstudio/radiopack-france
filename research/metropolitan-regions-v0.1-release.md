# Couverture métropolitaine v0.1 — 19 août 2026

RadioPack France publie les onze régions administratives métropolitaines qui ne disposaient pas encore d’un pack régional dédié. Avec Normandie et Bretagne, la couverture administrative métropolitaine atteint **13/13**. Annecy–Alpes–Léman reste un pack territorial spécialisé supplémentaire.

## Périmètre des nouvelles v0.1

- 16 mémoires PMR446 RX ;
- 2 appels radioamateur RX ;
- 6 mémoires APRS / ISS RX ;
- sélection régionale volontairement bornée de relais FM 2 m publics et recoupés ;
- politique **paired RX** : pour les paires retenues, deux mémoires de réception sont générées, sortie puis entrée à -600 kHz, dans la plage 2 m prévue par le plan de bande ;
- toutes les lignes publiques restent `Duplex=off` / `Offset=0.000000` ;
- aviation, UHF, numérique et extensions maritimes régionales restent hors de cette première v0.1 ;
- aucune donnée privée, de sécurité ou non publiquement vérifiable.

## Packs publiés

| Région | Version | Mémoires | Relais FM 2 m sélectionnés |
|---|---:|---:|---:|
| Hauts-de-France | v0.1 | 36 | 6 |
| Île-de-France | v0.1 | 34 | 5 |
| Grand Est | v0.1 | 36 | 6 |
| Centre-Val de Loire | v0.1 | 32 | 4 |
| Pays de la Loire | v0.1 | 30 | 3 |
| Bourgogne-Franche-Comté | v0.1 | 30 | 3 |
| Nouvelle-Aquitaine | v0.1 | 42 | 9 |
| Auvergne-Rhône-Alpes | v0.1 | 38 | 7 |
| Occitanie | v0.1 | 44 | 10 |
| Provence-Alpes-Côte d’Azur | v0.1 | 42 | 9 |
| Corse | v0.1 | 28 | 2 |

## Sources et revue

Les sélections 2 m ont été contrôlées le 19 août 2026 en croisant l’annuaire public RepeaterBook France avec le roster français F5AIB/REF. Le plan de bande REF sert de garde-fou pour les segments entrée/sortie 2 m et l’ANFR reste une source institutionnelle de contexte sur les installations radio.

Les références et la date de contrôle sont enregistrées directement dans `website/src/lib/metropolitanPack.ts`, qui constitue la source déterministe des onze nouvelles v0.1. Le registre public `website/src/lib/packRegistry.ts` expose ensuite les versions et les liens de téléchargement.

## Non-exhaustivité

Ces v0.1 constituent une base publique utile et traçable. Elles ne prétendent pas recenser tous les relais ou tous les services d’une région. Toute extension de contenu doit passer par une nouvelle revue et une nouvelle version publique.
