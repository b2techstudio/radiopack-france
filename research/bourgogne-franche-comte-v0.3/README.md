# Bourgogne-Franche-Comté v0.3 — prépublication

Date de revue : **19 août 2026**.

La v0.3 est construite depuis la **v0.2 publique immuable de 37 mémoires RX**. La portée est désormais fermée à **54 mémoires RX** pour la prépublication, sans remplissage artificiel et sans abaisser le seuil de preuve des fréquences ajoutées.

## Relais radioamateurs — audit et validation

La liste publique des relais du REF a été revue pour les départements 21, 25, 39, 58, 70, 71, 89 et 90. Les trois paires VHF déjà présentes dans la v0.2 restent conservées : F1ZDK, F5ZBP et F1ZCT.

Deux passes de validation croisée ont permis d'ajouter **5 stations / 10 mémoires RX** :

- **F5ZIQ — Besançon** : 145.450 / 432.550 MHz ;
- **F5ZVA — secteur Château-Chinon / Villapourçon** : 145.250 / 431.250 MHz ;
- **F5ZFQ — Ballon d’Alsace / Territoire de Belfort** : 145.2625 / 430.125 MHz ;
- **F1ZCA — Saint-Thiébaud / Mont Poupet** : 430.300 / 431.900 MHz ;
- **F5ZXZ — Cosne-Cours-sur-Loire** : 145.2125 / 431.100 MHz.

Cinq leads restent volontairement différés : **F5ZNS, F5ZFE, F5ZKM, F5ZMS et F5ZTJ**. Ils pourront être repris dans une version ultérieure si une confirmation opérateur suffisamment actuelle ou une clarification des configurations conflictuelles devient disponible. Leur absence ne bloque pas cette publication, volontairement non exhaustive.

## Aviation — AIRAC 08/26

La v0.2 contient déjà **7 mémoires aviation** : 121.500 MHz, Dole-Tavaux, Dijon-Longvic, Nevers-Fourchambault, Auxerre-Branches et Montbéliard-Courcelles.

La passe v0.3 ajoute **7 mémoires AM** supplémentaires dans le contexte **AIRAC 08/26**, en vigueur du 6 août au 2 septembre 2026 inclus :

- **Besançon-La Vèze (LFQM)** : AFIS/A-A **122.205 MHz** ;
- **Saint-Yan (LFLN)** : APP **119.505 MHz** et **123.405 MHz** ;
- **Saint-Yan (LFLN)** : GND **121.805 MHz** ;
- **Saint-Yan (LFLN)** : TWR **122.300 MHz** ;
- **Saint-Yan (LFLN)** : ATIS **132.480 MHz** ;
- **Chalon-Champforgeuil (LFLH)** : CHALON Information AFIS/A-A **118.605 MHz**.

La fréquence **Mâcon-Charnay (LFLM) 119.005 MHz** reste différée : elle est corroborée par des données publiques secondaires, mais la revue n'a pas capturé une confirmation primaire actuelle suffisamment nette pour l'intégrer sans réserve.

Aucune extraction directe des champs XML AIRAC 08/26 n'est revendiquée. Le contexte du cycle est vérifié sur le produit SIA courant, puis les fréquences promues sont recoupées avec les pages AIP accessibles ou une source locale actuelle de l'aérodrome. Le pack reste un outil d'écoute RX et ne remplace pas l'information aéronautique opérationnelle.

Si une publication intervient **à partir du 3 septembre 2026**, une revalidation **AIRAC 09/26** sera obligatoire, avec revue des NOTAM et SUP AIP applicables.

## Release candidate

La portée fermée est de **54 mémoires RX** :

- base publique v0.2 : 37 ;
- enrichissement radioamateur : +10 ;
- enrichissement aviation : +7 ;
- total : **54 RX** ;
- aviation totale dans la v0.3 : **14 mémoires**.

Le CSV v0.3 possède une route dédiée afin de préserver la v0.2 historique. Les règles restent RX-only, `Duplex=off`, `Offset=0.000000`, fréquences/noms/emplacements uniques, et aucun remplissage artificiel.

Fichiers de revue :

- `pack-plan.json` — contrat et portée v0.3 ;
- `backlog.json` — leads validés ou différés ;
- `current-ref-audit.json` — audit REF initial ;
- `second-source-validation-2026-08-19.json` — validation radio passe 1 ;
- `second-source-validation-pass2-2026-08-19.json` — validation radio passe 2 ;
- `aviation-airac08-2026-08-19.json` — audit aviation ;
- `internal-candidate-v0.3.json` — release candidate 54 RX ;
- `release-scope.json`, `review-checklist.json`, `publication-gates.json` — contrôles de prépublication.
