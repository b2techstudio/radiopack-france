# Enrichissement métropolitain v0.2 — 19 août 2026

Les onze packs administratifs publiés en v0.1 le 19 août 2026 passent en **v0.2 enrichie**. Le principe est le même que pour les packs déjà matures : ajouter uniquement des blocs régionaux publics suffisamment documentés, garder une traçabilité explicite et conserver la réception seule sur chaque mémoire.

Les v0.1 restent des versions historiques immuables et leurs URL de téléchargement continuent d'être générées.

## Socle commun v0.2

Chaque pack conserve :

- 16 mémoires PMR446 RX ;
- 2 appels radioamateur RX ;
- 6 mémoires APRS / ISS RX ;
- une sélection régionale de relais FM 2 m analogiques recoupés, avec **paired RX** (sortie + entrée à -600 kHz lorsque la paire est retenue) ;
- `Duplex=off` et `Offset=0.000000` sur toutes les lignes.

La v0.2 ajoute une sélection aviation AM issue du contexte SIA **AIRAC 08/26**, recoupé avec les dernières pages eAIP publiques effectives des aérodromes sélectionnés. Le produit XML AIRAC courant est vérifié comme contexte de cycle, mais cette revue **ne prétend pas avoir extrait les champs du XML courant** : les fréquences publiées sont contrôlées sur les pages eAIP publiques accessibles.

Pour les six régions littorales concernées, le module national VHF marine RX de 90 mémoires est intégré au pack régional : Hauts-de-France, Pays de la Loire, Nouvelle-Aquitaine, Occitanie, Provence-Alpes-Côte d’Azur et Corse.

## Packs v0.2

| Région | v0.1 historique | Aviation | Relais 2 m | Marine | v0.2 |
|---|---:|---:|---:|---:|---:|
| Hauts-de-France | 36 | 14 | 8 | 90 | **144** |
| Île-de-France | 34 | 18 | 8 | 0 | **58** |
| Grand Est | 36 | 19 | 8 | 0 | **59** |
| Centre-Val de Loire | 32 | 6 | 6 | 0 | **42** |
| Pays de la Loire | 30 | 10 | 3 | 90 | **130** |
| Bourgogne-Franche-Comté | 30 | 7 | 3 | 0 | **37** |
| Nouvelle-Aquitaine | 42 | 13 | 12 | 90 | **151** |
| Auvergne-Rhône-Alpes | 38 | 18 | 10 | 0 | **62** |
| Occitanie | 44 | 20 | 11 | 90 | **156** |
| Provence-Alpes-Côte d’Azur | 42 | 25 | 10 | 90 | **159** |
| Corse | 28 | 19 | 2 | 90 | **137** |

Le total ne cherche jamais à remplir artificiellement les 200 mémoires du poste. Une fréquence ne rentre dans un pack que si elle apporte un usage d'écoute identifiable et une provenance publique exploitable.

## Sources et méthode

### Aviation

- SIA — Données aéronautiques XML AIRAC 08/26, corrigendum, cycle effectif du 6 août au 2 septembre 2026 ;
- SIA eAIP — pages AD 2.18 publiques des aérodromes retenus ;
- 121.500 MHz est conservée une seule fois comme mémoire d'urgence aviation RX.

Le détail des aérodromes, services, fréquences et garde-fous est enregistré dans `research/<region>-v0.2/pack-plan.json`.

### Radioamateur 2 m

Les paires sélectionnées sont recoupées à partir de RepeaterBook France et du roster français F5AIB/REF, avec le plan de bande REF comme garde-fou. La revue est datée du 19 août 2026. Les sorties et entrées retenues sont exportées comme deux mémoires **RX uniquement**.

### VHF marine

Le dataset national `data/national/marine-vhf-rx.json` est intégré tel quel aux régions littorales. Les canaux duplex y conservent les deux fréquences de réception lorsqu'elles sont distinctes, conformément à la politique `research/paired-rx-policy.json`.

## Ce qui reste volontairement hors v0.2

- UHF radioamateur : pas de promotion globale sans revalidation région par région de chaque relais et de son état actuel ;
- modes numériques et hotspots : incompatibilités et utilité variable selon le poste cible, donc pas d'ajout automatique ;
- fréquences privées, PPDR, secours opérationnel non public ou réseaux internes : exclues ;
- services aviation supplémentaires : ajoutés seulement lors d'une revue SIA dédiée et versionnée.

Chaque dossier `research/<region>-v0.2/` contient un `README.md` et un `pack-plan.json` machine-readable afin que la prochaine évolution reparte d'un état documenté plutôt que d'une liste opaque.

## Contrôle correctif SIA avant publication

Un second passage sur les pages primaires SIA eAIP AD 2.18 a été effectué avant publication. Il a corrigé les canaux de Lille dans Hauts-de-France, le rôle de 123.835 MHz au Bourget, et la sélection Grand Est. Le validateur de déduplication a notamment bloqué un doublon 121.805 MHz : la sélection Bâle-Mulhouse a été réalignée sur les valeurs SIA actuelles, dont 121.605 MHz pour le sol. Aucune désactivation du garde-fou n'a été utilisée.

