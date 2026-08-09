# Sprint 29 — Mortain-Bocage et Bretagne : couverture radio locale

Date : 2026-08-09

## Objectif

Approfondir la recherche radio autour de Mortain-Bocage / Sud-Manche et la VHF publique de Bretagne sans modifier les versions déjà publiées, puis intégrer une nouvelle règle commune : **toute liaison publique nativement duplex/split dont les deux fréquences sont vérifiées doit permettre l'écoute des deux sens**.

Les sorties publiques restent inchangées :

- Normandie v0.3.1 : 139 mémoires ;
- Annecy–Alpes–Léman v0.2 : 65 mémoires, 48 sans aviation ;
- Bretagne : toujours non publiée.

## Politique paired RX

La politique globale est enregistrée dans :

```text
research/paired-rx-policy.json
```

Le plan concret des prochaines versions est :

```text
research/paired-rx-next-version-plan.json
```

Règle :

- liaison duplex/split avec deux fréquences distinctes vérifiées → deux mémoires RX ;
- chaque mémoire reste `Duplex=off` et `Offset=0.000000` ;
- aucune configuration TX split n'est créée ;
- une fréquence RF identique partagée par plusieurs rôles reste une seule mémoire ;
- tonalités d'activation ou de montée conservées comme métadonnées uniquement ;
- les versions déjà publiées restent immuables.

La Normandie v0.3.1 est déjà conforme pour la VHF marine avec des paires `-S` / `-C`. La règle s'applique désormais aux prochaines versions Normandie v0.4, Annecy–Alpes–Léman v0.3 et Bretagne v0.1.

### Satellites Annecy v0.3

La v0.2 publiée reste figée avec les descentes seules. La v0.3 devra, après recontrôle opérationnel, permettre l'écoute des deux côtés :

- SO-50 : 145.850 MHz montée / 436.795 MHz descente ;
- AO-91 : 435.250 MHz montée / 145.960 MHz descente ;
- AO-123 : 145.850 MHz montée / 435.400 MHz descente.

La montée 145.850 MHz commune à SO-50 et AO-123 reste dédupliquée.

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

La fiche courante exploitée ne fournit toujours ni fréquence ni mode utilisable pour une validation. La règle reste : **ne jamais deviner la fréquence de F6ZES**.

### Relais prioritaires documentés

- `F5ZHY` Montabot / Percy-en-Normandie : 145.0875 / 145.6875 MHz ;
- `F6ZCE` Mont des Avaloirs : 145.100 / 145.700 MHz, CTCSS 123 Hz ;
- `F1ZBX` Paimpont / Brocéliande : 145.075 / 145.675 MHz, CTCSS 71.9 Hz ;
- `F1ZOV` Equeurdreville : 430.375 / 431.975 MHz, faible priorité Mortain.

Si ces relais sont finalement sélectionnés pour Normandie v0.4, leurs deux côtés vérifiés devront être écoutables conformément à la politique paired RX.

## Bretagne — VHF maritime publique

Le fichier :

```text
research/bretagne-v0.1/public-maritime-radio.json
```

modélise maintenant les deux côtés RX des voies nativement duplex :

| Canal | Navire → côte | Côte → navire | État |
|---|---:|---:|---|
| 16 | 156.800 MHz | 156.800 MHz | simplex, une seule mémoire |
| 63 | 156.175 MHz | 160.775 MHz | paire vérifiée, Étel sur 63 côté côte |
| 64 | 156.225 MHz | 160.825 MHz | paire vérifiée, site Bretagne 64 encore à réconcilier |
| 79 | 156.975 MHz | 161.575 MHz | paire vérifiée, émetteur Corsen actuel encore inconnu |
| 80 | 157.025 MHz | 161.625 MHz | paire vérifiée, Penmarc'h/Groix/Belle-Ile côté côte |

Aucune de ces nouvelles mémoires n'est encore promue dans Bretagne v0.1.

Le canal 16 reste une mémoire unique : il ne sera pas dupliqué pour produire artificiellement une mémoire `CORSEN` et une mémoire `ETEL`.

## Interface CROSS Corsen / CROSS Étel à Penmarc'h

La responsabilité SAR est maintenant documentée des deux côtés :

- CROSS Corsen : **Baie du Mont-Saint-Michel à la pointe de Penmarc'h** ;
- CROSS Étel : **Pointe de Penmarc'h à la frontière espagnole**.

Penmarc'h est donc primaire-vérifié comme interface de responsabilité. Cette donnée ne permet pas de déduire la couverture VHF réelle, la géométrie offshore détaillée ni les recouvrements des stations radio.

## CROSS Corsen — infrastructures et couverture

Le réseau actuel est documenté à **10 stations VHF et 2 stations MF**.

Infrastructures actuelles primaire-vérifiées :

- **Cap Fréhel** : suivi et liaison avec les navires, canal non publié ;
- **Stiff / Ouessant** : équipements de radiocommunications actuels, canal non publié.

Une opération officielle du **21 septembre 2025** confirme une communication VHF entre le CROSS Corsen et un navire au nord de la **Pointe du Raz**. Cette donnée prouve une couverture VHF actuelle du secteur, mais pas le site émetteur ni le canal.

L'installation VHF/MF historique de la Pointe du Raz reste `current_validation: false`. Le centre principal de Pointe de Corsen / Plouarzel reste séparé de l'inventaire des stations déportées.

Le canal 79, bien que documenté historiquement en 2003 pour des informations/météo Corsen/Ouessant, reste sans émetteur actuel primaire-vérifié.

Le projet **CROSS Nouvelle génération** à horizon 2027 reste un contexte futur qui ne modifie aucune affectation actuelle.

## Bretagne — relais analogiques régionaux et ADRASEC

L'inventaire reste :

```text
research/bretagne-v0.1/emergency-relays.json
```

Le plan paired RX inclut notamment, sous réserve de sélection finale :

- `F1ZBX` : 145.075 / 145.675 MHz ;
- `F5ZEB` : 431.075 / 438.675 MHz ;
- `F5ZIS` : 145.2375 / 432.6500 MHz ;
- `F5ZIT` : 145.2250 / 432.6500 MHz ;
- `F1ZGS` : 145.2625 / 431.4250 MHz ;
- `F5ZDV` : 145.2625 / 438.7000 MHz ;
- `F5ZZL` : 145.2625 / 431.3750 MHz ;
- `F5ZPE` : 145.1375 / 145.7375 MHz.

Les fréquences partagées 145.2625 et 432.6500 MHz devront rester dédupliquées.

`F5ZPV` RU19 et `F5ZZH` R7X conservent leurs paires comme métadonnées mais restent hors candidats actifs tant que leur redémarrage n'est pas confirmé.

La fréquence du transpondeur ADRASEC 35 de `F1ZUG` reste inconnue et ne doit pas être déduite de l'APRS 144.800 MHz.

Les recherches ADRASEC 22, 29 et 56 restent ouvertes : aucun rôle ADRASEC n'est attribué par simple proximité géographique.

## Garde-fous

Nouveau test :

```text
tests/test_paired_rx_policy.py
```

Il vérifie notamment :

- la politique globale de double écoute RX ;
- `Duplex=off` et `Offset=0.000000` ;
- les paires maritimes Bretagne 63/64/79/80 ;
- les montées/descentes satellites prévues pour Annecy v0.3 ;
- la déduplication des fréquences RF partagées ;
- la conformité historique de la Normandie v0.3.1 pour la VHF marine ;
- l'immutabilité des packs publics.

Les tests existants `test_mortain_bretagne_radio_research.py`, `test_bretagne_research_scaffold.py` et `test_site_files.py` restent les garde-fous de zonage, sources, absence de publication et état des relais.

## Étape suivante

1. faire passer toute la CI avec la nouvelle politique paired RX ;
2. intégrer la politique dans les futurs assembleurs de Normandie v0.4, Annecy v0.3 et Bretagne v0.1 lorsque leurs plans mémoire seront ouverts ;
3. poursuivre l'inventaire primaire des stations CROSS Corsen et l'émetteur actuel du canal 79 ;
4. réconcilier le canal 64 dans le Morbihan ;
5. poursuivre F6ZES Sourdeval et les ADRASEC 22/29/56 ;
6. recontrôler les satellites avant toute publication Annecy v0.3 ;
7. ne publier aucune nouvelle mémoire avant revue explicite.
