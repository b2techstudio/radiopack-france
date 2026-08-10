# Normandie v0.4 — recherche

Cette branche de recherche prépare une future évolution du pack Normandie sans modifier l'artefact publié **v0.3.1**, qui reste figé à 139 mémoires.

## Politique paired RX

Normandie v0.4 applique la politique commune :

```text
research/paired-rx-policy.json
```

Lorsqu'une liaison analogique publique est nativement duplex/split et que ses deux fréquences sont vérifiées, **les deux côtés seront conservés pour l'écoute** sous forme de mémoires RX distinctes. Chaque mémoire restera `Duplex=off` et `Offset=0.000000`.

La Normandie v0.3.1 publique applique déjà ce modèle à la VHF marine avec ses paires `-S` / `-C`. La v0.4 étendra le même principe aux nouveaux relais/transpondeurs analogiques finalement sélectionnés, sans modifier la v0.3.1.

Une même fréquence RF partagée entre plusieurs rôles ou sites restera dédupliquée.

## Delta mémoire v0.4

Le premier plan mémoire concret est maintenant défini dans :

```text
research/normandie-v0.4/candidate-memory-delta.json
```

Il compare les **12 fréquences paired RX de recherche** avec les 139 mémoires de la v0.3.1 publiée. Quatre fréquences sont déjà présentes dans la base figée :

- `145.6875` — F5ZHY sortie ;
- `145.7000` — F6ZCE sortie ;
- `145.2500` — F1ZBL côté A ;
- `430.3750` — F1ZOV côté A.

Le delta paired RX maximal actuellement étudié est donc de **8 nouvelles fréquences**, sans positions mémoire attribuées :

### Prêtes au niveau recherche

- `145.0875` — F5ZHY entrée, paire actuelle explicitement publiée par l'ARA50 ;
- `145.1000` — F6ZCE entrée, déduite du décalage -600 kHz explicitement publié par l'ARAS72 avec sortie 145.700 MHz ;
- `431.2500` — F1ZBL côté B, paire bidirectionnelle 145.250 / 431.250 MHz confirmée par le Radio Club Nord Cotentin.

`ready_research_candidate` ne signifie pas publication autorisée : ces fréquences entrent seulement dans le candidat interne de travail.

### À valider depuis Mortain

- `145.0750` — F1ZBX / R3 entrée ;
- `145.6750` — F1ZBX / R3 sortie.

L'ARA35 publie un rayon d'usage de 150 km pour R3. La géométrie place Mortain à environ **119,3 km** du site, soit environ 30,7 km à l'intérieur de ce rayon, mais cela ne constitue pas une preuve de réception.

Le protocole RX-only dédié est :

```text
research/normandie-v0.4/r3-mortain-field-validation.json
```

La sortie `145.675 MHz` est la fréquence principale de validation de couverture. L'entrée `145.075 MHz` reste une écoute opportuniste : elle n'a pas besoin d'être reçue depuis Mortain pour conserver la logique paired RX si R3 est finalement sélectionné.

### Bloquées avant promotion

- `145.4675` / `432.5750` — F5ZHA Laval : le REF et une seconde liste actuelle concordent, mais l'ancien conflit RepeaterBook reste à fermer par une source locale actuelle et la couverture Mortain reste à vérifier ;
- `431.9750` — F1ZOV : la paire 430.375 / 431.975 MHz est recoupée par le Radio Club Nord Cotentin et l'ARA50, mais le club exploitant affiche actuellement **F1ZOV en maintenance**. Le nouveau côté reste donc bloqué jusqu'à revalidation du retour en service.

Le nombre final de mémoires v0.4 reste `null` et aucune position n'est assignée. Le delta ne constitue ni un objectif de remplissage ni une autorisation de publication.

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

## Candidats et blocages actuels

- `F5ZHY` — Montabot / Percy-en-Normandie — entrée **145.0875 MHz**, sortie **145.6875 MHz** ;
- `F6ZES` — Sourdeval — priorité locale, site/responsable/locator confirmés mais fréquence et mode toujours non résolus ;
- `F6ZCE` — Mont des Avaloirs — entrée **145.100 MHz**, sortie **145.700 MHz**, département 53 ;
- `F1ZBX` — Brocéliande / Paimpont — entrée **145.075 MHz**, sortie **145.675 MHz**, validation locale Mortain requise ;
- `F1ZOV` — Équeurdreville-Hainneville — paire **430.375 / 431.975 MHz** vérifiée mais station actuellement indiquée en maintenance par l'exploitant ;
- `F1ZBL` — transpondeur Équeurdreville-Hainneville — paire **145.250 / 431.250 MHz** résolue et recoupée ;
- `F5ZHA` — Laval — paire de recherche **145.4675 / 432.575 MHz**, encore bloquée par réconciliation locale et couverture ;
- relais numériques du département, conservés en métadonnées mais non retenus par défaut pour un profil RX analogique.

Le plan courant des paires reste centralisé dans :

```text
research/paired-rx-next-version-plan.json
```

Aucune nouvelle version publique n'est créée dans ce dossier. Les mémoires du delta ne pourront devenir publiques qu'après validation, allocation finale, revue explicite et création d'une nouvelle version Normandie.
