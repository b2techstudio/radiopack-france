# Sprint 29 — Mortain-Bocage et Bretagne : couverture radio locale

Date : 2026-08-09

## Objectif

Approfondir la recherche radio autour de Mortain-Bocage / Sud-Manche et la VHF publique de Bretagne sans modifier les versions déjà publiées.

Les sorties publiques restent donc inchangées :

- Normandie v0.3.1 : 139 mémoires ;
- Annecy–Alpes–Léman v0.2 : 65 mémoires, 48 sans aviation ;
- Bretagne : toujours non publiée.

## Mortain-Bocage / Sud-Manche

Le nouveau fichier :

```text
research/normandie-v0.4/mortain-bocage-coverage.json
```

classe les infrastructures selon leur pertinence potentielle pour Mortain-Bocage plutôt que selon les seules limites administratives.

Départements étudiés : Manche 50, Ille-et-Vilaine 35, Mayenne 53 et Orne 61.

### Sourdeval F6ZES

Le répertoire REF courant confirme :

- indicatif `F6ZES` ;
- site : Sourdeval ;
- responsable : `F1SMB` ;
- locator : `IN98MR93XV` ;
- altitude : 230 m.

En revanche, la fiche courante exploitée ne fournit actuellement ni fréquence ni mode utilisable pour une validation.

La recherche Web complémentaire du Sprint 29 n'a pas fourni de seconde source actuelle suffisamment précise pour lever ce blocage.

La règle reste donc explicite : **ne jamais deviner la fréquence de F6ZES**. Une seconde source actuelle est requise avant de transformer Sourdeval en mémoire candidate.

### Relais prioritaires déjà documentés

- `F5ZHY` Montabot / Percy-en-Normandie : 145.6875 MHz en sortie, 145.0875 MHz en entrée, FM ;
- `F6ZCE` Mont des Avaloirs : 145.700 MHz en sortie, 145.100 MHz en entrée, FM, CTCSS 123 Hz ;
- `F1ZBX` Paimpont / Brocéliande : 145.675 MHz en sortie, 145.075 MHz en entrée, FM, CTCSS 71.9 Hz ;
- `F5ZHA` Laval : transpondeur analogique à conserver en étude de couverture avant toute sélection.

Les digipeaters APRS locaux sur 144.800 MHz restent des métadonnées de couverture : le futur pack ne dupliquera pas la mémoire APRS nationale pour chaque site.

Les relais numériques uniquement, comme le candidat C4FM de l'Orne étudié ici, ne consomment pas de mémoire dans le profil RX analogique.

## Bretagne — VHF maritime publique

Le fichier :

```text
research/bretagne-v0.1/public-maritime-radio.json
```

sépare correctement les fréquences navire et station côtière pour les voies duplex.

Pour un pack **RX-only**, la fréquence mémorisable d'une voie duplex est la fréquence émise par la station côtière et reçue par le navire.

Fréquences officielles étudiées :

| Canal | Type | Fréquence RX utile au pack | Usage étudié |
|---|---|---:|---|
| 16 | simplex | 156.800 MHz | appel, détresse, sécurité |
| 79 | duplex | 161.575 MHz | CROSS / météo annoncée sur 16 |
| 80 | duplex | 161.625 MHz | CROSS / météo annoncée sur 16 |
| 63 | duplex | 160.775 MHz | météo côtière permanente selon zone |
| 64 | duplex | 160.825 MHz | affectation CROSS / autorités portuaires, usage Bretagne à réconcilier |

Aucune de ces fréquences n'est encore promue dans Bretagne v0.1.

Le canal 16 reste une mémoire unique : il ne sera pas dupliqué pour produire artificiellement une mémoire `CORSEN` et une mémoire `ETEL`.

### Validation primaire CROSS Étel — complément Sprint 29

Une nouvelle vérification primaire DIRM NAMO permet de préciser le zonage et les émetteurs météo :

- le **CROSS Étel est officiellement compétent à partir de la Pointe de Penmarc'h (Finistère) jusqu'à la frontière espagnole** ;
- le planning officiel du CROSS Étel liste **Penmarc'h — canal 80** ;
- **Groix — canal 80** ;
- **Belle-Ile — canal 80** ;
- **Étel — canal 63 en diffusion continue**.

Ces quatre sites sont désormais enregistrés comme **métadonnées de recherche primaires vérifiées**, pas comme mémoires publiques.

Le ministère chargé de la mer mentionne par ailleurs une diffusion permanente sur les canaux 63 et 64 notamment dans le Morbihan. Le planning local primaire CROSS Étel exploité n'identifie cependant aucun émetteur Bretagne sur le canal 64. Le Sprint 29 conserve donc 160.825 MHz comme donnée réglementaire de recherche sans inventer de site ni promouvoir la fréquence.

La page actuelle du **CROSS Corsen** confirme un réseau VHF/MHF veillé et des diffusions météo depuis des stations littorales, mais ne fournit pas la liste détaillée de ces stations et de leurs canaux. L'inventaire Corsen reste donc `official_inventory_pending`.

L'ancienne formulation « frontière Finistère Sud entièrement inconnue » est remplacée par une position plus précise : **le point de départ de compétence Étel à Penmarc'h est vérifié**, mais la ligne cartographique détaillée, les éventuels recouvrements VHF et les sites Corsen restent à documenter.

## Bretagne — relais analogiques régionaux

L'inventaire `research/bretagne-v0.1/emergency-relays.json` contient des candidats analogiques actuels :

- `F5ZIS` Matignon : 145.2375 MHz, transpondeur vers 432.6500 MHz, CTCSS 71.9 Hz ;
- `F5ZIT` Perros-Guirec : 145.2250 MHz, transpondeur vers 432.6500 MHz, CTCSS 71.9 Hz ;
- `F1ZBX` Brocéliande : 145.675 MHz ;
- `F1ZBZ` Lorient : sortie 431.200 MHz avec plusieurs entrées publiées ; direction exacte à revoir avant sélection RX ;
- `F5ZPE` Bignan : 145.7375 MHz en sortie, 145.1375 MHz en entrée, CTCSS 71.9 Hz.

Le fait qu'un relais soit situé dans une zone où une ADRASEC est active ne suffit jamais à lui attribuer un rôle ADRASEC. Ce rôle doit être documenté par une source dédiée.

## Sécurité et réseaux professionnels

Le Sprint 29 conserve la politique du Sprint 28 :

- relais radioamateurs publics et infrastructures ADRASEC documentées : recherche autorisée ;
- canaux maritimes publics : recherche autorisée ;
- canaux opérationnels internes PPDR/PMR de police, gendarmerie, SDIS, SAMU ou associations de secours : hors publication sauf diffusion explicitement publique.

## Garde-fous

Le test :

```text
tests/test_mortain_bretagne_radio_research.py
```

vérifie notamment :

- que F6ZES reste sans fréquence tant qu'elle n'est pas recoupée ;
- les valeurs des relais Mortain/Sud-Manche déjà documentés ;
- l'exclusion des doublons APRS et des relais numériques incompatibles ;
- les fréquences RX exactes des canaux maritimes 16/63/64/79/80 ;
- le point de départ de compétence Étel à Penmarc'h ;
- les émetteurs météo primaires Penmarc'h, Groix, Belle-Ile et Étel ;
- le maintien de CROSS Corsen et du site Bretagne du canal 64 en recherche lorsqu'ils ne sont pas suffisamment documentés ;
- les relais Bretagne ;
- l'absence de Bretagne, Normandie v0.4 et Annecy v0.3 dans le registre public.

Le test Bretagne et le garde-fou global ont également été alignés sur ce nouvel état.

La CI exécute ce test dans l'étape `Test Mortain and Bretagne public radio research`.

## Étape suivante

Priorités :

1. trouver une seconde source actuelle pour la fréquence et le mode de F6ZES Sourdeval ;
2. identifier depuis une source primaire la liste détaillée des stations VHF déportées de CROSS Corsen ;
3. documenter les recouvrements VHF autour de Penmarc'h ;
4. réconcilier l'usage actuel du canal 64 dans le Morbihan avec une source primaire locale ;
5. poursuivre les inventaires ADRASEC 22/29/35/56 et Sud-Manche ;
6. ne publier aucune nouvelle mémoire avant revue de couverture et nouvelle version explicite.
