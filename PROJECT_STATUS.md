# RadioPack France — point de reprise

Dernière mise à jour : **22 août 2026**
Sprint courant : **113**
État logique : **0.22.01**

L'état machine officiel est `research/project-resume-state.json`. Résumé courant : `research/sprint-113-summary.md`.

## État public

- Normandie v0.5 : **146 mémoires RX**, publiée et immuable ; 4 mémoires sont retenues sur couverture théorique documentée. Normandie v0.4 / 142 RX reste historique et immuable.
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

Couverture : **13/13 régions administratives métropolitaines**. Annecy–Alpes–Léman est un pack territorial supplémentaire. Les cinq régions d'outre-mer ne sont pas encore couvertes. Les variantes par défaut totalisent **1595 mémoires RX** dans le catalogue public.

## Sprint 113 — Normandie v0.5 publiée

Normandie v0.5 est publiée et figée à **146 RX** à partir de la v0.4 immuable de 142 RX. Le delta de **+4 RX** est :

- 178 `35-R3-IN` — 145.075 MHz ;
- 179 `35-R3-OUT` — 145.675 MHz ;
- 180 `53-ZHA-V` — 145.4675 MHz ;
- 181 `53-ZHA-U` — 432.575 MHz.

Ces quatre mémoires reposent sur une **couverture théorique documentée**. Elles ne sont pas présentées comme réception mesurée ou garantie. Les écoutes terrain deviennent du contrôle qualité facultatif et ne bloquent plus la publication.

SHA candidat/public : `1d7ce66c7a5faafe98e4ee59791bcd29af1fd1f432ee1bfc1cad7cba3bc5cf59`. Identité byte-for-byte vérifiée. Publication gates : **0 blocker**.

Toujours différés :
- F1ZOV : statut opérateur local toujours en maintenance ;
- F6ZES : fréquence et mode publics toujours non résolus ;
- ancienne valeur secondaire F5ZHA 431.4125 MHz : non promue.

## Sprint 112 — Normandie v0.5 : politique théorique et candidat figé

Le Sprint 112 a remplacé le caractère bloquant de l'écoute terrain par une politique de couverture théorique documentée. Le candidat est passé de **142 à 146 RX**, puis a été figé au même SHA que la publication Sprint 113.

La théorie peut fermer un gate de couverture uniquement lorsque fréquence, mode et statut courant sont suffisamment documentés. Elle ne peut ni inventer une donnée manquante ni contourner un statut de maintenance, et elle ne doit jamais être assimilée à une réception réelle.

## Sprint 111 — Bretagne v0.3 AIRAC 09/26 prête pour revalidation

Le produit SIA AIRAC 09/26 est disponible en avance mais n'est **pas courant avant le 3 septembre 2026**. Sprint 111 prépare une matrice de **16 mémoires aviation** (positions 130–145) et un validateur qui exige une décision explicite pour chaque mémoire, une source primaire courante et une revue humaine.

Bretagne v0.2 reste publique et immuable à **151 RX** ; le candidat v0.3 reste **151 RX / delta 0**. Aucun CSV v0.3 n'est créé. Un verdict AIRAC positif autorisera seulement une reconstruction interne, jamais une publication automatique.

## Sprint 110 — historique Normandie v0.5, ancien handoff terrain

Au Sprint 110, Normandie v0.5 était encore **interne à 142 RX / delta 0** et R3/F1ZBX ainsi que F5ZHA étaient soumis à des sessions terrain. Ce cadre est conservé comme photographie historique mais a été **supplanté par la politique théorique du Sprint 112**.

Le kit Sprint 84 et l'évaluateur Sprint 85 restent disponibles comme outils facultatifs de contrôle qualité. Ils ne sont plus des gates de promotion ou de publication.

## Sprint 109 — Auvergne-Rhône-Alpes v0.3 publiée

Auvergne-Rhône-Alpes v0.3 est publiée et figée à **71 RX**. Elle conserve les **62 lignes** de v0.2 et ajoute **9 mémoires VHF navigation intérieure** aux emplacements **120–128** : voies **10, 12, 18, 19, 20 et 22**, avec paired RX pour 19, 20 et 22.

La voie 18 est retenue côté bateau uniquement à **156.900 MHz** : **161.500 MHz n'est pas ajoutée**. Le canal maritime 16 / 156.800 MHz reste exclu.

SHA public et candidat : `b44a95486af5fd89fa72246ed7c8f0ab79e3084f6b0429df5215fba9918d691e`.

Les **18 mémoires aviation** sont héritées sans modification de v0.2. AIRAC 08/26 reste applicable jusqu'au **2 septembre 2026 inclus** ; toute nouvelle révision aviation à partir du **3 septembre 2026** exige AIRAC 09/26.

## Sprint 108 — candidat ARA v0.3 figé

Le Sprint 108 a fermé le minimum vérifié Auvergne-Rhône-Alpes à **+9 RF fluviales**, construit le candidat déterministe 71 RX et figé le SHA avant toute mutation publique.

## Sprint 107 — Bourgogne-Franche-Comté v0.4 publiée

Bourgogne-Franche-Comté v0.4 est publiée et figée à **61 RX**. Elle conserve les **54 lignes** de v0.3 et ajoute **7 mémoires VHF navigation intérieure** sur les emplacements **120–126** : voies **10, 12, 20, 22 et 69**, avec paired RX pour 20 et 22.

SHA public et candidat : `02dcba7e14a0cce331b63126ea4e552d41013ebd51aecec19907009f40236a72`.

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

### Normandie après v0.5

Normandie v0.5 est **publiée à 146 RX**. Il n'y a plus de gate terrain bloquant. La veille source reste ouverte sur **F1ZOV** et **F6ZES**. Toute écoute terrain éventuelle sert uniquement de retour qualité et ne doit pas être confondue avec le fondement théorique de la publication actuelle.

### Bretagne v0.3

Candidat **151 RX, delta 0**. Sprint 111 a préparé la matrice de 16 mémoires et le validateur. AIRAC 09/26 est disponible comme source future mais ne devient courant qu'à partir du **3 septembre 2026** ; avant cette date, AIRAC 08/26 reste la référence applicable.

En attendant cette échéance, les nouveaux travaux de couverture peuvent utiliser la **théorie documentée** selon la politique Sprint 112, tout en conservant les exigences de source, statut opérationnel, déduplication et absence d'inférence.

## Contrat permanent

- RX-only : `Duplex=off`, `Offset=0.000000` ;
- maximum 200 mémoires ;
- paired RX pour les paires distinctes vérifiées ;
- déduplication RF ;
- aucun remplissage artificiel ;
- aucune fréquence ou mode ambigu/non résolu deviné ;
- couverture théorique documentée autorisée comme gate de couverture ;
- théorie jamais présentée comme réception mesurée ou garantie ;
- écoutes terrain facultatives comme contrôle qualité ;
- statut maintenance jamais contourné par la théorie ;
- données privées/PPDR non publiées ;
- versions publiées immuables ;
- aviation revalidée sur le cycle AIRAC applicable avant toute nouvelle publication.
