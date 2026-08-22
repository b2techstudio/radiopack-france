# Sprint 102 — Grand Est v0.3 initialization

Date : 2026-08-22

## But

Démarrer la recherche Grand Est v0.3 sans modifier le pack public v0.2.

## Base figée

- Grand Est v0.2 : 59 RX ;
- aviation : 19 mémoires AIRAC 08/26 ;
- radio régionale : 16 mémoires issues de 8 relais 2 m paired-RX ;
- SHA-256 public v0.2 : `a50416bd8a88af249bb691daa657ffd4b578daf1324bd0ca4dd632a2f1a0e5c1` ;
- version publique immuable.

## Pass radio 1

Le premier audit courant confirme sept des huit relais v0.2 comme base analogique exploitable au premier passage : F5ZAU, F1ZDG, F5ZDL, F1ZAE, F5ZEC, F5ZCQ et F1ZPJ.

F1ZAX n'est pas reconduit automatiquement : l'inventaire REF courant le classe C4FM alors que des annuaires secondaires conservent une présentation FM/Fusion. Une corroboration opérateur/local actuelle est requise avant inclusion dans un pack analogique.

Quatre nouveaux liens disposent déjà de deux sources publiques actuelles ou suffisamment convergentes pour former le noyau de la passe suivante :

- F5ZUD — Nancy/Vandoeuvre — 145.7125 / 145.1125 MHz ;
- F1ZUV — Strasbourg — 144.750 / 439.750 MHz ;
- F5ZAW — Bellefosse/Champ du Feu — 145.2125 / 433.425 MHz ;
- F5ZYS — Dogneville — 439.775 / 430.375 MHz.

Le plan de travail contient également des candidats non promus en Ardennes, Aube, Meuse, Moselle, Haut-Rhin et Vosges. La fréquence 432.5375 MHz apparaît sur plusieurs transpondeurs : la future construction devra dédupliquer la RF au lieu de créer plusieurs mémoires identiques.

## État

- recherche pass 1 : terminée ;
- pass 2 / seconde source : requise ;
- aviation v0.3 : non démarrée ;
- candidat déterministe : non construit ;
- compteur final : non figé ;
- publication : interdite à ce stade ;
- mutation CSV/site public : aucune.

Toute révision aviation effectuée à partir du 3 septembre 2026 devra utiliser AIRAC 09/26.
