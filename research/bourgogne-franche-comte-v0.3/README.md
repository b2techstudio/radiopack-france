# Bourgogne-Franche-Comté v0.3 — publication

Publiée le **19 août 2026**.

La v0.3 est publiée et **immuable à 54 mémoires RX**, depuis la v0.2 historique immuable de 37 mémoires. Le CSV public est figé par SHA-256 : `b5af25a6766b1181e735d376d3f70ab47ffb9ed67b9e38e35bee15e8a86ae7a5`.

## Radioamateur

Deux passes de validation croisée ont ajouté **5 stations / 10 mémoires RX paired-RX** :

- **F5ZIQ — Besançon** : 145.450 / 432.550 MHz ;
- **F5ZVA — secteur Château-Chinon / Villapourçon** : 145.250 / 431.250 MHz ;
- **F5ZFQ — Ballon d’Alsace / Territoire de Belfort** : 145.2625 / 430.125 MHz ;
- **F1ZCA — Saint-Thiébaud / Mont Poupet** : 430.300 / 431.900 MHz ;
- **F5ZXZ — Cosne-Cours-sur-Loire** : 145.2125 / 431.100 MHz.

Cinq leads restent différés pour une version ultérieure : **F5ZNS, F5ZFE, F5ZKM, F5ZMS et F5ZTJ**. Ils n'ont pas été ajoutés sans confirmation opérateur suffisamment actuelle ou résolution des conflits documentaires. La publication est volontairement non exhaustive.

## Aviation — AIRAC 08/26

La v0.2 contenait déjà **7 mémoires aviation**. La v0.3 en ajoute **7**, portant le bloc aviation total à **14 mémoires** :

- **Besançon-La Vèze (LFQM)** : AFIS/A-A **122.205 MHz** ;
- **Saint-Yan (LFLN)** : APP **119.505 MHz** et **123.405 MHz** ;
- **Saint-Yan (LFLN)** : GND **121.805 MHz** ;
- **Saint-Yan (LFLN)** : TWR **122.300 MHz** ;
- **Saint-Yan (LFLN)** : ATIS **132.480 MHz** ;
- **Chalon-Champforgeuil (LFLH)** : CHALON Information AFIS/A-A **118.605 MHz**.

**Mâcon-Charnay (LFLM) 119.005 MHz** reste différé : une piste publique existe, mais la revue n'a pas capturé une confirmation primaire actuelle suffisamment nette pour l'intégrer sans réserve.

La photographie aviation est publiée dans le contexte **AIRAC 08/26**, en vigueur du 6 août au 2 septembre 2026 inclus. Toute révision du pack à partir du **3 septembre 2026** devra repasser par AIRAC 09/26 et une revue NOTAM/SUP AIP. RadioPack France reste un outil d'écoute RX et ne remplace pas l'information aéronautique opérationnelle.

## Contrat de publication

- **54 mémoires RX** : 37 de base +10 radioamateur +7 aviation ;
- RX-only : `Duplex=off`, `Offset=0.000000` ;
- fréquences, noms et emplacements CHIRP uniques ;
- aucun remplissage artificiel ;
- v0.2 historique conservée ;
- v0.3 servie par une route CSV dédiée et enregistrée dans le registre public.

Fichiers de publication : `publication-record.json`, `release-scope.json`, `review-checklist.json`, `publication-gates.json`, `pack-plan.json` et les trois fichiers de preuve radio/aviation. Le téléchargement public est `/downloads/bourgogne-franche-comte/radiopack-france-bourgogne-franche-comte-v0.3.csv`.
