# Normandie v0.4 — recherche

Cette branche de recherche prépare une future évolution du pack Normandie sans modifier l'artefact publié **v0.3.1**, qui reste figé.

## Politique paired RX

Normandie v0.4 applique la politique commune :

```text
research/paired-rx-policy.json
```

Lorsqu'une liaison analogique publique est nativement duplex/split et que ses deux fréquences sont vérifiées, **les deux côtés seront conservés pour l'écoute** sous forme de mémoires RX distinctes. Chaque mémoire restera `Duplex=off` et `Offset=0.000000`.

La Normandie v0.3.1 publique applique déjà ce modèle à la VHF marine avec ses paires `-S` / `-C`. La v0.4 étendra le même principe aux nouveaux relais/transpondeurs analogiques qui seront finalement sélectionnés, sans modifier la v0.3.1.

Une même fréquence RF partagée entre plusieurs rôles ou sites restera dédupliquée.

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

- `F5ZHY` — Montabot / Percy-en-Normandie — entrée **145.0875 MHz**, sortie **145.6875 MHz** ;
- `F6ZES` — Sourdeval — priorité de recherche locale, fréquence et mode actuels toujours à confirmer ;
- `F6ZCE` — Mont des Avaloirs — entrée **145.100 MHz**, sortie **145.700 MHz**, département 53 ;
- `F1ZBX` — Brocéliande / Paimpont — entrée **145.075 MHz**, sortie **145.675 MHz**, département 35 ;
- `F1ZOV` — Equeurdreville-Hainneville — entrée **430.375 MHz**, sortie **431.975 MHz**, faible priorité pour Mortain-Bocage ;
- `F1ZBL` — transpondeur Cherbourg — intérêt départemental mais direction de la paire encore à revoir avant modélisation paired RX ;
- relais numériques du département, conservés en métadonnées mais non retenus par défaut pour un profil RX analogique.

Le plan courant des paires est centralisé dans :

```text
research/paired-rx-next-version-plan.json
```

Aucune nouvelle version publique n'est créée dans ce dossier. Les paires ne deviendront des mémoires que lors de la construction et de la revue explicites de Normandie v0.4.
