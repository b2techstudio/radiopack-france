# Sprint 29 — Mortain-Bocage et Bretagne : couverture radio locale

Date : 2026-08-09

## Objectif

Approfondir la recherche radio autour de Mortain-Bocage / Sud-Manche et la VHF publique de Bretagne sans modifier les versions déjà publiées.

Les sorties publiques restent donc inchangées :

- Normandie v0.3.1 : 139 mémoires ;
- Annecy–Alpes–Léman v0.2 : 65 mémoires, 48 sans aviation ;
- Bretagne : toujours non publiée.

## Mortain-Bocage / Sud-Manche

Le fichier :

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

Les recherches complémentaires du Sprint 29 n'ont toujours pas fourni de seconde source actuelle suffisamment précise pour lever ce blocage.

La règle reste donc explicite : **ne jamais deviner la fréquence de F6ZES**. Une seconde source actuelle est requise avant de transformer Sourdeval en mémoire candidate.

### Relais prioritaires déjà documentés

- `F5ZHY` Montabot / Percy-en-Normandie : 145.6875 MHz en sortie, 145.0875 MHz en entrée, FM ;
- `F6ZCE` Mont des Avaloirs : 145.700 MHz en sortie, 145.100 MHz en entrée, FM, CTCSS 123 Hz ;
- `F1ZBX` Paimpont / Brocéliande : 145.675 MHz en sortie, 145.075 MHz en entrée, FM, CTCSS 71.9 Hz ;
- `F5ZHA` Laval : transpondeur analogique à conserver en étude de couverture avant toute sélection.

Les digipeaters APRS locaux sur 144.800 MHz restent des métadonnées de couverture : le futur pack ne dupliquera pas la mémoire APRS nationale pour chaque site.

Les relais numériques uniquement ne consomment pas de mémoire dans le profil RX analogique cible.

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
| 79 | duplex | 161.575 MHz | CROSS / météo annoncée sur 16 ; usage Corsen historiquement primaire-vérifié en 2003, émetteur actuel non identifié |
| 80 | duplex | 161.625 MHz | CROSS / météo annoncée sur 16 |
| 63 | duplex | 160.775 MHz | météo côtière permanente selon zone |
| 64 | duplex | 160.825 MHz | mention ministérielle actuelle 63/64 Morbihan, émetteur Bretagne 64 à réconcilier |

Aucune de ces fréquences n'est encore promue dans Bretagne v0.1.

Le canal 16 reste une mémoire unique : il ne sera pas dupliqué pour produire artificiellement une mémoire `CORSEN` et une mémoire `ETEL`.

### CROSS Étel — validation primaire

La DIRM NAMO permet de préciser le zonage et les émetteurs météo :

- le **CROSS Étel est officiellement compétent à partir de la Pointe de Penmarc'h (Finistère) jusqu'à la frontière espagnole** ;
- **Penmarc'h — canal 80** ;
- **Groix — canal 80** ;
- **Belle-Ile — canal 80** ;
- **Étel — canal 63 en diffusion continue**.

Ces quatre sites restent des **métadonnées de recherche primaires vérifiées**, pas des mémoires publiques.

La page actuelle du ministère chargé de la mer mentionne toujours une diffusion permanente sur les canaux 63 et 64 notamment dans le Morbihan. Cette mention a été recontrôlée en 2026. En parallèle, les sources primaires locales du CROSS Étel exploitées identifient explicitement Étel sur le canal 63 et aucun émetteur Bretagne sur le canal 64. Le Sprint 29 conserve donc 160.825 MHz comme donnée de recherche sans inventer de site ni promouvoir la fréquence.

### CROSS Corsen — infrastructures actuelles et couverture sectorielle du Raz

La page actuelle du CROSS Corsen confirme un réseau VHF/MF veillé en permanence et des diffusions météo depuis des stations littorales. Une communication officielle récente de la DGAMPA apporte une information structurante : le réseau Corsen s'appuie sur **10 stations radio VHF et 2 stations MF**.

La liste complète et les canaux de ces stations restent à établir. Deux infrastructures actuelles sont désormais primaire-vérifiées :

- **Cap Fréhel** : équipements de suivi et de liaison avec les navires, sans canal publié dans la source exploitée ;
- **Stiff / Ouessant** : sources officielles 2026 confirmant des équipements de radiocommunications du CROSS dans la tour, sans canal publié.

La revalidation actuelle du Stiff ne permet pas d'attribuer le canal 79 au site. Le canal reste en recherche tant qu'une source primaire actuelle n'identifie pas son émetteur.

Une opération officielle du **21 septembre 2025** apporte une nouvelle preuve autour de la **Pointe du Raz** : le CROSS Corsen a établi un contact VHF avec un navire au nord de la pointe. Cette donnée valide une **couverture VHF opérationnelle actuelle du secteur**, mais le communiqué ne précise ni l'émetteur utilisé ni son canal. L'installation VHF/MF historique de la Pointe du Raz reste donc `current_validation: false` et ne devient pas une station actuelle par déduction.

Le centre opérationnel principal du CROSS Corsen à la **Pointe de Corsen / Plouarzel** est également documenté comme actuel, mais il reste séparé de l'inventaire des stations radio déportées. Sa présence ne suffit pas à revalider l'installation radio locale de secours multicanal décrite en 2003.

### CROSS Nouvelle génération — contexte futur uniquement

Une offre officielle de préfiguration publiée en 2026 décrit un projet **CROSS Nouvelle génération** prévoyant un regroupement fonctionnel Étel/Corsen, avec un horizon opérationnel **2027**.

RadioPack conserve cette information comme contexte de transition uniquement. Elle ne permet pas de modifier les affectations, sites ou fréquences actuels avant publication de sources opérationnelles nouvelles.

### Corsen — historique primaire de 2003

Le décret Légifrance de 2003 reste utile pour documenter l'architecture de l'époque :

- équipements VHF au **Stiff / Ouessant** ;
- installation **VHF et MF à la Pointe du Raz** ;
- installation radio de secours multicanal sur le site de **Corsen** ;
- diffusion régulière d'informations et de météo sur le **canal 79**, après appel sur le canal 16.

Le Stiff est aujourd'hui revalidé comme infrastructure radio actuelle. La Pointe du Raz dispose désormais d'une preuve actuelle de couverture VHF du secteur, mais pas d'une revalidation de son émetteur historique. Le centre de Corsen/Plouarzel est actuel, mais son ancienne installation locale reste elle aussi à revalider. Le canal 79 reste sans émetteur actuel primaire-vérifié.

L'interface Penmarc'h reste également à documenter du point de vue des recouvrements radio réels : la frontière de responsabilité ne suffit pas à déduire une couverture VHF.

## Bretagne — relais analogiques régionaux et ADRASEC

L'inventaire `research/bretagne-v0.1/emergency-relays.json` contient des candidats analogiques actuels et des métadonnées ADRASEC.

### Côtes-d'Armor / Bretagne Nord

- `F5ZIS` Matignon : 145.2375 MHz, transpondeur vers 432.6500 MHz, CTCSS 71.9 Hz ;
- `F5ZIT` Perros-Guirec : 145.2250 MHz, transpondeur vers 432.6500 MHz, CTCSS 71.9 Hz.

### Ille-et-Vilaine / ADRASEC 35

- `F1ZBX` Brocéliande : 145.675 MHz ;
- `F5ZEB` R71 Rennes Est : sortie 438.675 MHz, entrée 431.075 MHz, CTCSS 71.9 Hz, remis en service le 25 septembre 2025 ;
- `F5ZPV` RU19 Rennes-Beaulieu : sortie 439.875 MHz, entrée 430.475 MHz, FM/C4FM, toujours conservé comme temporairement arrêté dans la source actuelle ;
- `F5ZZH` R7X Rennes-Beaulieu / Cesson-Sévigné : sortie **145.7875 MHz**, entrée **145.1875 MHz**, FM, actuellement documenté par l'ARA35 comme **temporairement arrêté et à la recherche d'un nouveau site** ; il reste `rx_pack_candidate: false`.

Le site `F1ZUG` de Châtillon-en-Vendelais reste qualifié avec deux fonctions distinctes :

- digipeater APRS `F1ZUG-4` sur 144.800 MHz ;
- site hébergeant également un **transpondeur pour le réseau ADRASEC 35**, information publiée lors d'une opération d'entretien en juin 2024.

La fréquence de ce transpondeur ADRASEC n'est pas publiée. Le fichier conserve donc :

```text
adrasec_transponder_frequency_mhz: null
```

et interdit de la déduire à partir de 144.800 MHz.

### Finistère — candidats analogiques REF

Le répertoire REF actuel permet de conserver trois transpondeurs analogiques actifs au travail Bretagne, tous sans leur attribuer de rôle ADRASEC :

- `F1ZGS` — Plouhinec — sortie **431.425 MHz**, entrée **145.2625 MHz**, FM, CTCSS 71.9 Hz ;
- `F5ZDV` — Morlaix — sortie **438.700 MHz**, entrée **145.2625 MHz**, FM, CTCSS 71.9 Hz ;
- `F5ZZL` — Cast — sortie **431.375 MHz**, entrée **145.2625 MHz**, FM, CTCSS 71.9 Hz.

Ils sont `rx_pack_candidate: true` uniquement au niveau de la recherche. Leur couverture, leur redondance et leur intérêt pour le futur plan mémoire doivent encore être revus avant toute sélection.

### Morbihan — APRS et analogique

- `F1ZBZ` Lorient : sortie 431.200 MHz avec plusieurs voies publiées ; direction exacte à revoir avant sélection RX ;
- `F5ZPE` Bignan : sortie 145.7375 MHz, entrée 145.1375 MHz, CTCSS 71.9 Hz ;
- `F1ZAJ` Plouray : APRS **144.800 MHz**, conservé uniquement comme métadonnée de maillage puisque la fréquence APRS nationale existe déjà dans le bloc commun.

Les recherches ADRASEC 22, 29 et 56 restent ouvertes : l'existence des organisations est documentée, mais aucun rôle de relais ne sera déduit de la seule implantation géographique ou d'un indicatif radioamateur.

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
- le réseau Corsen actuel dimensionné à **10 stations VHF et 2 stations MF** ;
- Cap Fréhel et Stiff/Ouessant comme infrastructures radio actuelles sans leur attribuer de canal non publié ;
- la **couverture VHF actuelle du secteur de la Pointe du Raz** sans en déduire le site émetteur ni le canal ;
- le centre actuel de Plouarzel sans l'assimiler à une station radio déportée ;
- le projet CROSS-NG 2027 comme contexte futur sans mutation des fréquences actuelles ;
- le canal 79 toujours sans émetteur actuel revalidé ;
- la mention ministérielle actuelle du canal 64 tout en maintenant l'émetteur Bretagne non résolu ;
- la séparation stricte entre l'APRS F1ZUG-4 et la fréquence encore inconnue du transpondeur ADRASEC 35 ;
- F5ZEB R71 comme donnée régionale actuelle mais non promue ;
- F5ZPV RU19 et F5ZZH R7X comme relais temporairement arrêtés, donc non candidats actifs ;
- F1ZGS, F5ZDV et F5ZZL comme candidats analogiques Finistère non publiés ;
- F1ZAJ Plouray comme métadonnée APRS sans doublon mémoire ;
- l'absence de Bretagne, Normandie v0.4 et Annecy v0.3 dans le registre public.

Les garde-fous globaux et Bretagne sont alignés sur ces distinctions entre infrastructure, couverture, émetteur et canal.

## Étape suivante

Priorités :

1. identifier par source primaire actuelle les autres sites des **10 stations VHF et 2 stations MF** du réseau CROSS Corsen ;
2. identifier l'émetteur actuel derrière la couverture VHF de la **Pointe du Raz** et l'usage actuel du canal 79 ;
3. revalider l'installation radio historique de la Pointe du Raz et l'installation locale historique de Corsen ;
4. suivre CROSS Nouvelle génération sans projeter son organisation 2027 sur les données actuelles ;
5. réconcilier l'usage actuel du canal 64 dans le Morbihan avec une source primaire locale ;
6. trouver une seconde source actuelle pour la fréquence et le mode de F6ZES Sourdeval ;
7. retrouver la fréquence actuelle du transpondeur ADRASEC 35 de F1ZUG sans la déduire de l'APRS ;
8. poursuivre les inventaires ADRASEC 22/29/56 et Sud-Manche ;
9. revoir la couverture et la redondance de F1ZGS, F5ZDV, F5ZZL et F5ZEB avant toute sélection mémoire ;
10. revalider les retours éventuels de F5ZPV RU19 et F5ZZH R7X ;
11. ne publier aucune nouvelle mémoire avant revue de couverture et nouvelle version explicite.
