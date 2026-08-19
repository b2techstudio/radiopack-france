# Bourgogne-Franche-Comté v0.3 — recherche

Initialisation : **19 août 2026**.

La v0.3 démarre depuis la **v0.2 publique immuable de 37 mémoires RX**. Aucun CSV public et aucune fréquence publiée ne sont modifiés pendant la phase de recherche.

## Premier audit public

La liste publique des relais du REF, indiquée comme mise à jour le **13 mai 2026**, a été revue pour les départements 21, 25, 39, 58, 70, 71, 89 et 90.

Les trois paires VHF déjà présentes dans la v0.2 restent visibles comme actives dans cette source :

- F1ZDK — Mont-Saint-Vincent — 145.750 / 145.150 MHz ;
- F5ZBP — Saint-Thiébaud — 145.775 / 145.175 MHz ;
- F1ZCT — Chitry — 145.7875 / 145.1875 MHz.

Le libellé public historique de F5ZBP reste volontairement inchangé dans la v0.2 ; la différence de nom de site relevée dans l'annuaire courant est seulement tracée pour la prochaine version.

## Validation croisée — passe 1

Trois stations ont été validées pour le candidat interne :

- **F5ZIQ — Besançon** : 145.450 / 432.550 MHz ;
- **F5ZVA — secteur Château-Chinon / Villapourçon** : 145.250 / 431.250 MHz ;
- **F5ZFQ — Ballon d’Alsace / Territoire de Belfort** : 145.2625 / 430.125 MHz.

La politique paired RX a ajouté **6 mémoires**, portant alors le candidat interne à **43 RX**.

## Validation croisée — passe 2

Deux leads supplémentaires passent le filtre après vérification indépendante :

- **F1ZCA — Saint-Thiébaud / Mont Poupet** : 430.300 / 431.900 MHz. La paire actuelle du REF est corroborée directement par la page locale REF-39 du relais RU12, qui documente la même configuration et son retour en service ;
- **F5ZXZ — Cosne-Cours-sur-Loire** : 145.2125 / 431.100 MHz. Le conflit avec un ancien listing est levé pour le candidat interne par une télémétrie APRS publique actuelle attribuée à F5ZXZ et annonçant exactement cette paire à Cosne-sur-Loire.

Cela ajoute **4 mémoires RX** supplémentaires. Le candidat interne atteint donc **47 RX**, soit **+10** par rapport à la v0.2 publique.

Cinq leads restent volontairement bloqués : **F5ZNS, F5ZFE, F5ZKM, F5ZMS et F5ZTJ**. Les raisons sont conservées dans `second-source-validation-pass2-2026-08-19.json` : absence de confirmation opérateur suffisamment actuelle, documentation indépendante trop ancienne, ou conflit historique de site/indicatif/configuration.

## Périmètre

La priorité est donnée aux relais et transpondeurs **analogiques FM** réellement utiles en réception sur UV-K5. Les infrastructures uniquement numériques restent différées. Les réseaux privés, PPDR ou non publiquement vérifiables restent exclus.

La v0.3 conserve les règles suivantes : RX-only, `Duplex=off`, `Offset=0.000000`, paired RX pour une paire distincte vérifiée, déduplication RF et aucun remplissage artificiel.

Le candidat **47 RX reste interne** : il n'est pas publié, n'est pas ajouté au registre public et ne remplace pas la v0.2 de 37 mémoires.

Fichiers de travail :

- `pack-plan.json` — contrat courant de la v0.3 ;
- `backlog.json` — état des 10 leads analogiques ;
- `current-ref-audit.json` — photographie de l'audit REF initial ;
- `second-source-validation-2026-08-19.json` — passe 1 ;
- `second-source-validation-pass2-2026-08-19.json` — passe 2 ;
- `internal-candidate-v0.3.json` — candidat interne courant de 47 RX.
