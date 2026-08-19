# Hauts-de-France v0.2

Cette version enrichit la v0.1 sans la modifier. Le pack public courant contient **144 mémoires RX**.

## Blocs

- 16 PMR446 ;
- 2 appels radioamateur ;
- 6 APRS / ISS ;
- 14 mémoires aviation AM revues dans le contexte SIA AIRAC 08/26 ;
- 8 relais FM 2 m sélectionnés, soit 16 mémoires paired RX ;
- 90 mémoires VHF marine issues du module national.

Toutes les lignes CHIRP restent `Duplex=off` / `Offset=0.000000`.

## Méthode

L'aviation s'appuie sur le produit SIA AIRAC 08/26 courant comme contexte et sur les pages eAIP AD 2.18 publiques effectives des aérodromes retenus. Aucun rapprochement champ par champ avec l'export XML courant n'est revendiqué sans extraction du fichier XML.

Les relais 2 m sont recoupés avec RepeaterBook France et le roster F5AIB/REF, sous le garde-fou du plan de bande REF. Les fréquences UHF et numériques restent dans le backlog tant qu'une revue dédiée n'a pas validé leur état actuel et leur utilité pour le profil d'écoute visé.

Le détail machine-readable est dans `pack-plan.json`. La v0.1 historique reste générable et immuable.
