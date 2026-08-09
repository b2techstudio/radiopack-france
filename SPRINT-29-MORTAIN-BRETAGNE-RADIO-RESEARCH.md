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
| 79 | duplex | 161.575 MHz | CROSS / météo annoncée sur 16 |
| 80 | duplex | 161.625 MHz | CROSS / météo annoncée sur 16 |
| 63 | duplex | 160.775 MHz | météo côtière permanente selon zone |
| 64 | duplex | 160.825 MHz | affectation CROSS / autorités portuaires, usage Bretagne à réconcilier |

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

Le ministère chargé de la mer mentionne par ailleurs une diffusion permanente sur les canaux 63 et 64 notamment dans le Morbihan. Le planning local primaire CROSS Étel exploité n'identifie cependant aucun émetteur Bretagne sur le canal 64. Le Sprint 29 conserve donc 160.825 MHz comme donnée réglementaire de recherche sans inventer de site ni promouvoir la fréquence.

### CROSS Corsen — Cap Fréhel confirmé, canal non attribué

La page actuelle du CROSS Corsen confirme toujours un réseau VHF/MHF veillé et des diffusions météo depuis des stations littorales, sans publier la liste détaillée de ces stations et de leurs canaux.

Une source primaire DIRM NAMO distincte apporte néanmoins une avancée : le **phare du Cap Fréhel héberge des équipements du CROSS Corsen de suivi et de liaison avec les navires**, utilisés pour la surveillance du trafic maritime et la coordination des secours.

Cette preuve est enregistrée comme **infrastructure radio Corsen primaire-vérifiée**. Elle n'est volontairement pas classée comme station VHF météo et aucun canal, notamment le 79, ne lui est attribué sans source primaire supplémentaire. L'inventaire `remote_vhf_sites` de Corsen reste donc ouvert.

L'interface Penmarc'h reste également à documenter du point de vue des recouvrements radio réels : la frontière de responsabilité ne suffit pas à déduire une couverture VHF.

## Bretagne — relais analogiques régionaux et ADRASEC

L'inventaire `research/bretagne-v0.1/emergency-relays.json` contient des candidats analogiques actuels et des métadonnées ADRASEC.

### Côtes-d'Armor / Bretagne Nord

- `F5ZIS` Matignon : 145.2375 MHz, transpondeur vers 432.6500 MHz, CTCSS 71.9 Hz ;
- `F5ZIT` Perros-Guirec : 145.2250 MHz, transpondeur vers 432.6500 MHz, CTCSS 71.9 Hz.

### Ille-et-Vilaine / ADRASEC 35

- `F1ZBX` Brocéliande : 145.675 MHz ;
- `F5ZEB` R71 Rennes Est : sortie 438.675 MHz, entrée 431.075 MHz, CTCSS 71.9 Hz, remis en service le 25 septembre 2025 ;
- `F5ZPV` RU19 Rennes-Beaulieu : sortie 439.875 MHz, entrée 430.475 MHz, FM/C4FM, toujours conservé comme temporairement arrêté dans la source actuelle.

Le site `F1ZUG` de Châtillon-en-Vendelais reste qualifié avec deux fonctions distinctes :

- digipeater APRS `F1ZUG-4` sur 144.800 MHz ;
- site hébergeant également un **transpondeur pour le réseau ADRASEC 35**, information publiée lors d'une opération d'entretien en juin 2024.

La fréquence de ce transpondeur ADRASEC n'est pas publiée. Le fichier conserve donc :

```text
adrasec_transponder_frequency_mhz: null
```

et interdit de la déduire à partir de 144.800 MHz.

### Finistère — nouveaux candidats analogiques REF

Le répertoire REF actuel permet d'ajouter trois transpondeurs analogiques actifs au travail Bretagne, tous sans leur attribuer de rôle ADRASEC :

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
- Cap Fréhel comme infrastructure radio Corsen primaire-vérifiée **sans lui attribuer de service VHF ni de canal** ;
- le maintien de l'inventaire VHF Corsen et du site Bretagne du canal 64 en recherche ;
- la séparation stricte entre l'APRS F1ZUG-4 et la fréquence encore inconnue du transpondeur ADRASEC 35 ;
- F5ZEB R71 comme donnée régionale actuelle mais non promue ;
- F5ZPV RU19 comme relais temporairement arrêté, donc non candidat actif ;
- F1ZGS, F5ZDV et F5ZZL comme candidats analogiques Finistère non publiés ;
- F1ZAJ Plouray comme métadonnée APRS sans doublon mémoire ;
- l'absence de Bretagne, Normandie v0.4 et Annecy v0.3 dans le registre public.

Le test secours/ADRASEC et le test de scaffold Bretagne sont alignés sur ces constats.

## Étape suivante

Priorités :

1. trouver une seconde source actuelle pour la fréquence et le mode de F6ZES Sourdeval ;
2. compléter par sources primaires la liste détaillée des stations VHF/MHF de CROSS Corsen et leurs canaux ;
3. documenter les recouvrements VHF autour de Penmarc'h ;
4. réconcilier l'usage actuel du canal 64 dans le Morbihan avec une source primaire locale ;
5. retrouver la fréquence actuelle du transpondeur ADRASEC 35 de F1ZUG sans la déduire de l'APRS ;
6. poursuivre les inventaires ADRASEC 22/29/56 et Sud-Manche ;
7. revoir la couverture et la redondance de F1ZGS, F5ZDV, F5ZZL et F5ZEB avant toute sélection mémoire ;
8. revalider le retour éventuel de F5ZPV RU19 ;
9. ne publier aucune nouvelle mémoire avant revue de couverture et nouvelle version explicite.
