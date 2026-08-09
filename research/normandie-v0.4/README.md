# Normandie v0.4 — recherche

Cette branche de recherche prépare une future évolution du pack Normandie sans modifier l'artefact publié **v0.3.1**, qui reste figé.

## Priorité géographique

Le travail v0.4 donne une priorité explicite à **Mortain-Bocage / Sud-Manche**. La sélection radio ne doit pas s'arrêter à la frontière administrative de la Manche : les relais réellement utiles depuis ce secteur peuvent se trouver dans les départements voisins.

Départements adjacents à contrôler :

- Ille-et-Vilaine `35` ;
- Mayenne `53` ;
- Orne `61`.

## Secours et ADRASEC

Le futur inventaire doit distinguer :

- relais radioamateurs analogiques avec usage ou priorité ADRASEC ;
- relais radioamateurs régionaux utiles à la couverture locale ;
- transpondeurs et digipeaters ;
- réseaux professionnels de sécurité/secours, documentés seulement comme contexte lorsqu'ils ne sont pas destinés à l'écoute publique.

Les réseaux opérationnels privés PPDR/PMR de police, gendarmerie, SDIS, SAMU ou associations de secours ne sont pas ajoutés comme fréquences simplement parce qu'ils existent.

## Premiers candidats

Le fichier `emergency-relays.json` ouvre notamment la revue de :

- `F5ZHY` — Montabot / Percy-en-Normandie — sortie analogique 145.6875 MHz ;
- `F6ZES` — Sourdeval — priorité de recherche locale, fréquence actuelle à confirmer ;
- `F6ZCE` — Mont des Avaloirs — 145.700 MHz, département 53 ;
- `F1ZBX` — Brocéliande / Paimpont — 145.675 MHz, département 35 ;
- `F1ZBL` — transpondeur Cherbourg — intérêt départemental mais moins prioritaire pour Mortain-Bocage ;
- relais numériques du département, conservés en métadonnées mais non retenus par défaut pour un profil RX analogique.

Aucune nouvelle version publique n'est créée dans ce dossier.
