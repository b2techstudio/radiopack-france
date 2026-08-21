# Île-de-France v0.3 — checkpoint de recherche

Checkpoint ouvert le **21 août 2026** à partir de la **v0.2 publique immuable de 58 mémoires RX**.

Ce dossier ne constitue **pas** encore un candidat de publication. Aucun CSV public n'est modifié par ce checkpoint. La v0.3 doit encore fermer les conflits de sources radioamateur et terminer la revalidation aviation SIA/AIRAC.

## Radioamateur — deuxième passe du 21 août

La revue couvre le 2 m, 70 cm et les transpondeurs crossband analogiques, avec paired RX pour les paires distinctes et déduplication RF.

La deuxième passe affine la première sans réécrire son historique. Le détail initial reste dans `radio-validation-2026-08-21.json` et les nouvelles décisions sont figées dans `radio-validation-pass2-2026-08-21.json`.

### Base v0.2 encore soutenue

- **F5ZNG Provins** — 145.625 / 145.025 MHz ;
- **F5ZNN Saint-Rémy-la-Vanne** — 145.650 / 145.050 MHz ;
- **F5ZMH Linas** — 145.7375 / 145.1375 MHz ;
- **F1ZHK Nangis** — 145.7625 / 145.1625 MHz. La capture REF courante a été retrouvée et converge avec la liste RepeaterBook actuelle : le gate de conservation est fermé.

### Nouveaux ajouts directement étayés depuis la première passe

- **F5ZMR Provins** — 431.525 / 439.125 MHz, soit deux mémoires RX ;
- **F5ZSY Issy-les-Moulineaux** — transpondeur analogique crossband 145.325 / 430.325 MHz, soit deux mémoires RX.

### Décisions fermées par la deuxième passe

- **F6ZEE Pontault-Combault** — 145.100 / 145.700 MHz : REF le donne actif et RepeaterBook le donne en service avec une entrée ajoutée le 21 janvier 2026. Ces deux RF sont exactement celles de l'ancienne attribution **F1ZSY Paris** de la v0.2. En RX-only, la paire reste donc représentée sous l'attribution courante F6ZEE, avec **zéro nouvelle mémoire RF nette** ;
- **F5ZNN crossband** — 145.650 / 430.650 MHz : REF et la liste opérationnelle RI49 convergent. Comme 145.650 MHz existe déjà dans la paire 2 m F5ZNN, la déduplication RF ajoute uniquement **430.650 MHz**, soit **une seule nouvelle mémoire** ;
- **F5ZEQ Le Mesnil-le-Roi** — 145.750 / 145.150 MHz : non reconduit dans le candidat de travail courant, car la page de son opérateur F5KCK indique explicitement que le relais est hors service pour maintenance. Il pourra être réévalué lorsque l'opérateur annoncera son retour en service ;
- **F1ZSY Paris** : l'ancienne attribution n'est plus retenue, mais son jeu RF 145.100 / 145.700 MHz n'est pas supprimé puisqu'il est repris par F6ZEE.

### Gates radio encore ouverts

- **F5ZBK Triel-sur-Seine** — 430.175 / 431.775 MHz : REF courant actif, seconde corroboration opérationnelle actuelle encore recherchée ;
- **F1ZDL Saint-Mard** — 430.075 / 439.475 MHz : nouveau candidat repéré dans le REF courant, seconde corroboration opérationnelle actuelle requise ;
- **F1ZTC Paris** : différé. RepeaterBook le marque hors service sur 145.775 / 145.175 MHz avec une revue du 17 février 2026, tandis que d'autres listes publiques ne convergent pas complètement sur l'état et les fréquences ;
- **F5ZDR Linas** : différé. Les éléments locaux décrivent encore une chaîne UHF dégradée tandis que les annuaires exposent aussi des rôles multimodes/numériques différents ; aucun état analogique stable n'est promu.

### Comptage de travail provisoire

Si les blocs nationaux et les **18 mémoires aviation** de la v0.2 restent inchangés, les décisions radio actuellement validées donnent un **compteur de travail provisoire de 57 mémoires** :

`58 - 8 + 2 + 4 + 1 = 57`

- `-8` : retrait de quatre anciennes paires v0.2 (F5ZAD, F1ZUX, F1ZSY, F5ZEQ) ;
- `+2` : réintégration du même jeu RF 145.100 / 145.700 sous F6ZEE ;
- `+4` : F5ZMR et F5ZSY ;
- `+1` : 430.650 MHz pour le crossband F5ZNN après déduplication.

**57 n'est pas le compteur d'un release candidate.** F5ZBK, F1ZDL, F1ZTC, F5ZDR et l'aviation restent derrière des gates ouverts.

## Aviation — deuxième passe AIRAC 08/26

Le bloc public v0.2 contient **18 mémoires aviation AM**. AIRAC 08/26 reste le cycle courant du **6 août au 2 septembre 2026 inclus**.

La deuxième passe est enregistrée dans `aviation-validation-pass2-2026-08-21.json` et avance la revue sans fermer prématurément le gate aviation :

- **LFPG / Paris Charles-de-Gaulle** : la page SIA eAIP AD 2.18 directement courante depuis le 6 août 2026 a été contrôlée. Les quatre fréquences APP déjà présentes en v0.2 — **118.155, 119.855, 121.155 et 124.355 MHz** — sont toujours publiées et sont donc revalidées pour le calcul de travail ;
- le même AD 2.18 LFPG publie aussi d'autres fréquences APP actuelles, notamment **125.830, 126.430, 126.580, 131.205, 133.380 et 136.280 MHz**. Elles sont uniquement consignées comme observations : aucune n'est ajoutée tant que le périmètre utile et la revue complète aviation ne sont pas fermés ;
- **LFPO / Paris-Orly** : les huit mémoires v0.2 restent inchangées dans le calcul provisoire, mais la capture directe AD 2.18 AIRAC 08/26 et la revue NOTAM/SUP applicables restent ouvertes. Les SUP AIP 147/2026 et 085/2026 précédemment identifiés restent à examiner dans cette fermeture ;
- **LFPB / Paris-Le Bourget** : les cinq mémoires v0.2 restent elles aussi inchangées dans le calcul provisoire ; la capture directe AD 2.18 AIRAC 08/26 et la revue NOTAM/SUP restent à fermer.

La décision aviation provisoire reste donc **18 mémoires, delta 0**. Elle n'est pas finale et ne transforme pas le total de travail **57** en release candidate.

Toute publication ou nouvelle validation effectuée à partir du **3 septembre 2026** devra être reprise sur **AIRAC 09/26**.

## Règles permanentes

- RX uniquement : `Duplex=off`, `Offset=0.000000` ;
- maximum 200 mémoires ;
- paired RX pour les paires distinctes vérifiées ;
- déduplication RF ;
- aucun remplissage artificiel ;
- aucun état, mode ou fréquence ambigu ne doit être deviné ;
- l'état courant publié par l'opérateur local prévaut sur un annuaire général pour une décision de publication ;
- toute fréquence aviation supplémentaire exige validation de source et décision explicite de périmètre ;
- données privées, PPDR, chiffrées ou non publiquement vérifiables exclues ;
- v0.2 publique conservée immuable ;
- publication v0.3 interdite tant que les gates radio et aviation ne sont pas fermés.
