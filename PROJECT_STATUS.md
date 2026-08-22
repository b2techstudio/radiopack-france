# RadioPack France — point de reprise

Dernière mise à jour : **22 août 2026**
Sprint courant : **109**
État logique : **0.21.97**

L'état machine officiel est `research/project-resume-state.json`. Résumé courant : `research/sprint-109-summary.md`.

## État public

- Normandie v0.4 : **142 mémoires RX**, publiée et immuable.
- Annecy–Alpes–Léman v0.4 : **77 mémoires RX**, variante **60 sans aviation**, publiée et immuable.
- Bretagne v0.2 : **151 mémoires RX**, publiée et immuable.
- Hauts-de-France v0.2 : **144 mémoires RX**, publiée et immuable.
- Île-de-France v0.4 : **64 mémoires RX**, dont **18 aviation**, **15 radio régionales** et **7 VHF navigation intérieure**, publiée et immuable ; v0.3 **57 RX** et v0.2 **58 RX** historiques immuables.
- Grand Est v0.4 : **97 mémoires RX**, dont **19 aviation** et **13 VHF navigation intérieure**, publiée et immuable ; v0.3 **84 RX** et v0.2 **59 RX** historiques immuables.
- Centre-Val de Loire v0.3 : **51 mémoires RX**, dont **7 aviation**, publiée et immuable.
- Pays de la Loire v0.2 : **130 mémoires RX**, publiée et immuable.
- Bourgogne-Franche-Comté v0.4 : **61 mémoires RX**, dont **14 aviation** et **7 VHF navigation intérieure**, publiée et immuable ; v0.3 **54 RX** et v0.2 **37 RX** historiques immuables.
- Nouvelle-Aquitaine v0.2 : **151 mémoires RX**, publiée et immuable.
- Auvergne-Rhône-Alpes v0.3 : **71 mémoires RX**, dont **18 aviation** et **9 VHF navigation intérieure**, publiée et immuable ; v0.2 **62 RX** historique immuable.
- Occitanie v0.2 : **156 mémoires RX**, publiée et immuable.
- Provence-Alpes-Côte d’Azur v0.2 : **159 mémoires RX**, publiée et immuable.
- Corse v0.2 : **137 mémoires RX**, publiée et immuable.

Couverture : **13/13 régions administratives métropolitaines**. Annecy–Alpes–Léman est un pack territorial supplémentaire. Les cinq régions d'outre-mer ne sont pas encore couvertes.

## Sprint 109 — Auvergne-Rhône-Alpes v0.3 publiée

Auvergne-Rhône-Alpes v0.3 est publiée et figée à **71 RX**. Elle conserve les **62 lignes** de v0.2 et ajoute **9 mémoires VHF navigation intérieure** aux emplacements **120–128** : voies **10, 12, 18, 19, 20 et 22**, avec paired RX pour 19, 20 et 22.

La voie 18 est retenue côté bateau uniquement à **156.900 MHz** : **161.500 MHz n'est pas ajoutée**. Le canal maritime 16 / 156.800 MHz reste exclu.

SHA public et candidat : `b44a95486af5fd89fa72246ed7c8f0ab79e3084f6b0429df5215fba9918d691e`.

La route Astro publique v0.3 a été vérifiée byte-identique au candidat Sprint 108 figé. Publication gates : **0 blocker**. La v0.2 de 62 RX reste historique et immuable.

Les **18 mémoires aviation** sont héritées sans modification de v0.2. AIRAC 08/26 reste applicable jusqu'au **2 septembre 2026 inclus** ; toute nouvelle révision aviation à partir du **3 septembre 2026** exige AIRAC 09/26.

## Sprint 108 — candidat ARA v0.3 figé

Le Sprint 108 a fermé le minimum vérifié Auvergne-Rhône-Alpes à **+9 RF fluviales**, construit le candidat déterministe 71 RX et figé le SHA avant toute mutation publique.

## Sprint 107 — Bourgogne-Franche-Comté v0.4 publiée

Bourgogne-Franche-Comté v0.4 est publiée et figée à **61 RX**. Elle conserve les **54 lignes** de v0.3 et ajoute **7 mémoires VHF navigation intérieure** sur les emplacements **120–126** : voies **10, 12, 20, 22 et 69**, avec paired RX pour 20 et 22.

SHA public et candidat : `02dcba7e14a0cce331b63126ea4e552d41013ebd51aecec19907009f40236a72`.

La route Astro publique v0.4 a été vérifiée byte-identique au candidat figé. Publication gates : **0 blocker**. La v0.3 de 54 RX reste historique et immuable.

## Sprints 106–103 — VHF navigation intérieure

- Sprint 106 : candidat BFC v0.4 figé à 61 RX avant publication.
- Sprint 105 : Île-de-France v0.4 publiée à **64 RX**, +7 VHF navigation intérieure.
- Sprint 104 : Grand Est v0.4 publiée à **97 RX**, +13 VHF navigation intérieure.
- Sprint 103 : audit national VHF navigation intérieure ; les quatre deltas non côtiers vérifiés Grand Est, IDF, BFC et ARA sont maintenant publiés.

## Historique récent

- Sprint 102 : Grand Est v0.3 publiée à 84 RX.
- Sprint 101 : Île-de-France v0.3 publiée à 57 RX.
- Sprint 100 : Centre-Val de Loire v0.3 publiée à 51 RX.
- Sprint 99 : Bourgogne-Franche-Comté v0.3 publiée à 54 RX.
- Sprint 98 : consolidation officielle des onze publications métropolitaines v0.2.
- Sprint 97 : consolidation de l'état UI/catalogue post-Sprint 96.

## Travaux ouverts

### Normandie v0.5

**Priorité actionnable actuelle.** Candidat **142 RX, delta 0**. Les promotions restent bloquées par les gates terrain/source : validation terrain requise pour **R3/F1ZBX** et **F5ZHA**, veille source sur **F1ZOV** et **F6ZES**. Le plafond potentiel connu reste 147 RX hors F6ZES si tous les gates identifiés se ferment.

### Bretagne v0.3

Candidat **151 RX, delta 0**. Publication bloquée jusqu'à la revalidation AIRAC 09/26 à partir du **3 septembre 2026** ; avant cette date, AIRAC 08/26 reste la référence applicable.

## Contrat permanent

- RX-only : `Duplex=off`, `Offset=0.000000` ;
- maximum 200 mémoires ;
- paired RX pour les paires distinctes vérifiées ;
- déduplication RF ;
- aucun remplissage artificiel ;
- aucune fréquence ambiguë devinée ;
- données privées/PPDR non publiées ;
- versions publiées immuables ;
- aviation revalidée sur le cycle AIRAC applicable avant toute nouvelle publication.