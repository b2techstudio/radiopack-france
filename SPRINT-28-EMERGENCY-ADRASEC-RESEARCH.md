# Sprint 28 — Relais secours / ADRASEC multi-régions

Date : 2026-08-09

## Objectif

Étendre la recherche RadioPack France aux relais radioamateurs utilisés pour les communications de secours et de sécurité civile, tout en séparant clairement :

- les relais radioamateurs publics / ADRASEC ;
- les infrastructures radioamateurs régionales utiles à la couverture locale ;
- les services maritimes publics ;
- les réseaux professionnels PPDR/PMR privés, qui ne doivent pas être publiés comme canaux opérationnels internes.

## Politique commune

Le fichier :

```text
research/emergency-radio-policy.json
```

définit les règles communes.

Sont éligibles à la recherche pour une future mémoire RX :

- relais et transpondeurs radioamateurs ADRASEC/FNRASEC publiquement documentés ;
- relais radioamateurs analogiques régionaux pertinents ;
- canaux maritimes et diffusions de sécurité explicitement publics ;
- autres diffusions de sécurité officiellement destinées à la réception des usagers.

Ne sont pas intégrés par défaut :

- canaux opérationnels internes de police, gendarmerie, pompiers, SAMU et autres réseaux PPDR ;
- canaux PMR privés d'associations de secours ou de Protection Civile lorsqu'ils ne sont pas explicitement destinés à l'écoute publique ;
- relais uniquement numériques incompatibles avec le profil RX analogique cible.

## Normandie v0.4 — priorité Mortain-Bocage

La version publiée Normandie v0.3.1 reste immuable.

Une nouvelle branche de recherche est ouverte :

```text
research/normandie-v0.4/
```

Le futur pack ne doit pas être borné au département 50 : depuis Mortain-Bocage, la couverture utile doit également être étudiée dans les départements 35, 53 et 61.

Premiers candidats :

- `F5ZHY` — Montabot / Percy-en-Normandie — sortie 145.6875 MHz FM ;
- `F6ZES` — Sourdeval — indicatif et site identifiés, fréquence actuelle encore à confirmer ;
- `F6ZCE` — Mont des Avaloirs / département 53 — sortie 145.700 MHz FM ;
- `F1ZBX` — Brocéliande / Paimpont — sortie 145.675 MHz FM, couverture depuis le Sud-Manche à vérifier ;
- `F1ZBL` — Cherbourg — transpondeur cross-band, intérêt surtout départemental nord ;
- `F1ZOV` — Equeurdreville — relais analogique nord Manche ;
- `F5ZTE` — Percy-en-Normandie — réseau numérique, conservé comme métadonnée mais non retenu par défaut pour le profil analogique.

L'ADRASEC 14-50 est enregistrée comme organisation actuelle membre de la FNRASEC, mais aucune fréquence n'est déduite de cette seule appartenance.

## Annecy–Alpes–Léman v0.3

La version publiée v0.2 reste immuable.

Nouvelle branche de recherche :

```text
research/annecy-alpes-leman-v0.3/
```

Premiers candidats :

- `F1ZJV` — Pointe des Brasses — sortie 145.7875 MHz FM, relais ADRASEC 74 ;
- `F1ZYT` — Semnoz — même sortie 145.7875 MHz : ne pas dupliquer une mémoire uniquement pour le site ;
- `F1ZHG` — Fort du Mont — sortie 145.2875 MHz, transpondeur ADRASEC 73 ;
- `F5ZGT` — Cime Caron — sortie 145.450 MHz, pertinence réelle pour Annecy à vérifier.

## Bretagne v0.1

Le zonage Nord/Sud du Sprint 27 reste obligatoire.

Le nouvel inventaire :

```text
research/bretagne-v0.1/emergency-relays.json
```

ouvre la recherche ADRASEC 22 / 29 / 35 / 56 et ajoute notamment :

- `F1ZUG-4` — APRS 144.800 MHz, site ARA35 avec rôle dans le réseau ADRASEC 35 ;
- `F5ZZC-4` — digipeater APRS ADRASEC 35, fréquence actuelle à revalider ;
- `F1ZBX` — Brocéliande — 145.675 MHz FM ;
- `F1ZBH` et `F1ZGQ` — digipeaters APRS Finistère, utiles à la cartographie du maillage local mais sans duplication du 144.800 national.

Une nouvelle porte `emergency_relay_inventory` interdit la publication Bretagne tant que les infrastructures ADRASEC 22/29/35/56 et les relais régionaux pertinents n'ont pas été inventoriés et zonés.

## Garde-fous

`tests/test_emergency_relay_research.py` vérifie notamment :

- l'absence de mutation des versions publiées ;
- le caractère non public des futurs v0.4 Normandie et v0.3 Annecy ;
- les priorités Mortain-Bocage / Sud-Manche ;
- les premiers candidats ADRASEC/analogiques ;
- l'exclusion des réseaux privés PPDR/PMR ;
- l'absence de nouvelle route de téléchargement ;
- l'absence des futures versions dans `packRegistry.ts`.

## État public inchangé

- Normandie v0.3.1 : 139 mémoires ;
- Annecy–Alpes–Léman v0.2 : 65 mémoires / 48 sans aviation ;
- Bretagne : toujours non publique.
