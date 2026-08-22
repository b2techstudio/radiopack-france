# Sprint 102 — Grand Est v0.3 publication

Date : 2026-08-22

## Résultat

Grand Est **v0.3 est publié comme version immuable** avec :

- **84 mémoires RX** au total ;
- **19 mémoires aviation** ;
- **41 fréquences radio régionales** ;
- SHA-256 candidat/public : `45aef8547a701e7541e620fa9a2d8394595576921e793b75238146ff6e42e720`.

La v0.2 / 59 RX reste historique et immuable, avec son SHA `a50416bd8a88af249bb691daa657ffd4b578daf1324bd0ca4dd632a2f1a0e5c1`.

## Radio

Trois passes ont fermé un scope analogique volontairement non exhaustif à **41 RF uniques**. La fréquence `432.5375 MHz`, commune à plusieurs crossbands, n'est stockée qu'une seule fois.

Les cas insuffisamment corroborés ou hors périmètre analogique n'ont pas été forcés : F1ZAX, F5ZBD, F5ZRP, F5ZTY, F5ZUK, F1ZFN et F1ZEF restent différés/exclus selon leur dossier ; F1ZBU reste exclu car son service courant est numérique.

## Aviation

Les **19 mémoires aviation** de la v0.2 sont conservées **strictement inchangées** dans la v0.3 :

- AIRAC 08/26 toujours courant le 2026-08-22 ;
- delta aviation : **0 ajout / 0 retrait / 0 modification** ;
- aucune nouvelle validation champ-par-champ n'est revendiquée ;
- toute nouvelle révision aviation à partir du **3 septembre 2026** devra être revalidée sur AIRAC 09/26.

## Publication

Le CSV public utilise exactement les mêmes octets que le candidat déterministe canonique. Le builder reconstruit d'abord la v0.2 et refuse la génération si son SHA historique ne correspond pas.

Garde-fous finaux :

- `Duplex=off` / `Offset=0.000000` sur toutes les mémoires ;
- RF, noms et locations uniques ;
- maximum 200 respecté ;
- checklist **12/12** ;
- publication gates **0 blocker** ;
- candidat/public byte-identiques ;
- registre et page régionale synchronisés ;
- v0.2 historique conservée.
