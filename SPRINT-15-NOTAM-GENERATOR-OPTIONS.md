# RadioPack France — Sprint 15

Ce sprint transforme le contrôle NOTAM en option facultative du futur générateur, sans modifier les CSV publics actuels.

## Décision fonctionnelle

RadioPack France reste un pack d'écoute RX et non un outil de préparation ou de conduite d'un vol.

Les fréquences aviation de référence restent validées sur les publications AIP/AIRAC et autres sources officielles retenues par le projet.

Les NOTAM deviennent un contrôle opérationnel facultatif :

- ils ne bloquent plus la publication d'un pack d'écoute RX ;
- ils ne modifient jamais automatiquement une fréquence du CSV ;
- ils peuvent être demandés ou non par l'utilisateur du futur générateur ;
- le générateur doit simplement indiquer clairement si le contrôle a été demandé et confirmé.

## Contrat du futur générateur

Le fichier `generator/options.json` définit deux options indépendantes :

- `include_aviation` : ajoute ou retire le bloc aviation du CSV ;
- `notam_check` : ajoute un contrôle NOTAM facultatif avant génération.

États prévus pour `notam_check` :

```text
disabled
requested_unconfirmed
user_confirmed
```

L'état `automatic_verified` est réservé pour une éventuelle intégration future si une source officielle automatisable est disponible.

## Interface prévue

Le futur générateur pourra présenter :

```text
☑ Inclure les fréquences aviation
☐ Contrôle NOTAM avant génération
```

Lorsque le contrôle NOTAM est demandé :

```text
France : SOFIA-Briefing
Suisse : Skybriefing

☐ J'ai vérifié les NOTAM applicables
```

La génération reste possible même sans confirmation NOTAM, avec un avertissement explicite.

## Portes de publication

Les portes AIRAC France, AIRAC Suisse et périmètre aérodromes restent des contrôles bloquants.

Les portes NOTAM France et Suisse passent à :

```text
required_for_public_release: false
status: advisory_optional_pre_generation
```

Le contrôle dynamique des satellites FM reste pour l'instant la seule porte dynamique bloquante avant préparation de la publication v0.2.

## Ce qui ne change pas

- le candidat interne reste à 65 mémoires ;
- `public_release_allowed` reste à `false` ;
- aucune fréquence Annecy v0.2 n'est publiée ;
- le générateur public historique n'est pas encore relié à Annecy–Alpes–Léman v0.2 ;
- tous les exports restent en réception seule avec `Duplex=off`.
