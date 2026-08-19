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

Les dix leads analogiques FM du backlog ont été recherchés une seconde fois avec une règle plus stricte que l'annuaire seul : la promotion interne exige une confirmation actuelle indépendante, de préférence issue de l'opérateur, d'une association locale ou d'une télémétrie publique attribuable à la station.

Trois stations passent ce filtre :

- **F5ZIQ — Besançon** : 145.450 / 432.550 MHz ;
- **F5ZVA — secteur Château-Chinon / Villapourçon** : 145.250 / 431.250 MHz ;
- **F5ZFQ — Ballon d’Alsace / Territoire de Belfort** : 145.2625 / 430.125 MHz.

La politique paired RX ajoute donc **6 mémoires** au candidat interne : **43 RX au total**. Ce candidat n'est **pas public** et ne remplace pas la v0.2 de 37 mémoires.

Les sept leads restants restent bloqués ou différés : F1ZCA, F5ZNS, F5ZXZ, F5ZFE, F5ZKM, F5ZMS et F5ZTJ. Les causes sont tracées individuellement dans `second-source-validation-2026-08-19.json` et `backlog.json` : absence de confirmation actuelle opérateur, source trop ancienne ou conflit de site/fréquence.

## Périmètre

La priorité est donnée aux relais et transpondeurs **analogiques FM** réellement utiles en réception sur UV-K5. Les infrastructures uniquement numériques restent différées. Les réseaux privés, PPDR ou non publiquement vérifiables restent exclus.

La v0.3 conserve les règles suivantes : RX-only, `Duplex=off`, `Offset=0.000000`, paired RX pour une paire distincte vérifiée, déduplication RF et aucun remplissage artificiel.

Fichiers de travail :

- `pack-plan.json` — contrat courant de la v0.3 ;
- `backlog.json` — état des 10 leads analogiques ;
- `current-ref-audit.json` — photographie de l'audit REF initial ;
- `second-source-validation-2026-08-19.json` — décisions de validation croisée ;
- `internal-candidate-v0.3.json` — candidat interne de 43 RX, non publiable en l'état.
