# Bourgogne-Franche-Comté v0.3 — recherche

Initialisation : **19 août 2026**.

La v0.3 démarre depuis la **v0.2 publique immuable de 37 mémoires RX**. Aucun CSV public et aucune fréquence publiée ne sont modifiés pendant la phase de recherche.

## Relais radioamateurs — audit et validation

La liste publique des relais du REF a été revue pour les départements 21, 25, 39, 58, 70, 71, 89 et 90. Les trois paires VHF déjà présentes dans la v0.2 restent conservées : F1ZDK, F5ZBP et F1ZCT.

Deux passes de validation croisée ont ensuite permis de promouvoir **5 stations / 10 mémoires RX** dans le candidat interne :

- **F5ZIQ — Besançon** : 145.450 / 432.550 MHz ;
- **F5ZVA — secteur Château-Chinon / Villapourçon** : 145.250 / 431.250 MHz ;
- **F5ZFQ — Ballon d’Alsace / Territoire de Belfort** : 145.2625 / 430.125 MHz ;
- **F1ZCA — Saint-Thiébaud / Mont Poupet** : 430.300 / 431.900 MHz ;
- **F5ZXZ — Cosne-Cours-sur-Loire** : 145.2125 / 431.100 MHz.

Cinq leads restent volontairement bloqués : **F5ZNS, F5ZFE, F5ZKM, F5ZMS et F5ZTJ**. Ils ne seront pas promus sans confirmation opérateur suffisamment actuelle ou résolution des conflits documentaires.

## Aviation — passe AIRAC 08/26

La v0.2 contient déjà **7 mémoires aviation** : 121.500 MHz, Dole-Tavaux, Dijon-Longvic, Nevers-Fourchambault, Auxerre-Branches et Montbéliard-Courcelles.

Une nouvelle passe aviation a été effectuée dans le contexte **AIRAC 08/26**, en vigueur du 6 août au 2 septembre 2026 inclus. Elle ajoute au candidat interne **6 mémoires AM** suffisamment étayées :

- **Besançon-La Vèze (LFQM)** : AFIS/A-A **122.205 MHz** ;
- **Saint-Yan (LFLN)** : APP **119.505 MHz** et **123.405 MHz** ;
- **Saint-Yan (LFLN)** : GND **121.805 MHz** ;
- **Saint-Yan (LFLN)** : TWR **122.300 MHz** ;
- **Saint-Yan (LFLN)** : ATIS **132.480 MHz**.

Deux autres pistes aviation sont conservées sans promotion : **Chalon-Champforgeuil (LFLH) 118.605 MHz** et **Mâcon-Charnay (LFLM) 119.005 MHz**. Les fréquences apparaissent dans des jeux de données publics, mais cette passe n'a pas capturé une confirmation primaire actuelle assez nette de la fréquence exacte ; elles restent donc en backlog plutôt que d'être ajoutées artificiellement.

Aucune extraction directe des champs XML AIRAC 08/26 n'est revendiquée. Le contexte du cycle est vérifié sur le produit SIA courant, puis les fréquences promues sont recoupées avec les pages AIP accessibles ou une source locale actuelle de l'aérodrome.

Si la v0.3 est publiée **à partir du 3 septembre 2026**, une revalidation **AIRAC 09/26** sera obligatoire, avec contrôle des NOTAM et SUP AIP applicables au moment de la publication.

## Candidat interne courant

Le candidat interne passe de **47 à 53 mémoires RX** :

- base publique v0.2 : 37 ;
- enrichissement radioamateur : +10 ;
- enrichissement aviation : +6 ;
- total candidat : **53 RX**.

Il reste **non publiable en l'état** : aucune route de téléchargement, aucun CSV public et aucune entrée de registre ne sont modifiés. Les règles restent RX-only, `Duplex=off`, `Offset=0.000000`, déduplication RF et aucun remplissage artificiel.

Fichiers de travail :

- `pack-plan.json` — contrat courant de la v0.3 ;
- `backlog.json` — état des leads et ventilation du delta ;
- `current-ref-audit.json` — audit REF initial ;
- `second-source-validation-2026-08-19.json` — validation radio passe 1 ;
- `second-source-validation-pass2-2026-08-19.json` — validation radio passe 2 ;
- `aviation-airac08-2026-08-19.json` — audit et promotion aviation ;
- `internal-candidate-v0.3.json` — candidat interne courant de 53 RX.
