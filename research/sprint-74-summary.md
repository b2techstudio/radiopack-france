# Sprint 74 — initialisation Bretagne v0.2

Date : 12 août 2026
État logique : `0.21.63`

## Nouvelle version de recherche

Bretagne v0.2 est initialisée sur la base publique immuable **Bretagne v0.1 = 135 mémoires RX**.

Aucun ajout n'est promu au démarrage : candidat courant **135**, delta **0**. Aucun fichier public v0.2 n'est créé et le registre public reste sur v0.1.

## Backlog repris

`research/bretagne-v0.2/backlog.json` reprend six dossiers explicitement différés ou non résolus :

- extraction exacte de la source aviation courante avant toute promotion ;
- revalidation des données ADRASEC publiquement vérifiables en Bretagne, sans inférence d'une donnée non publiée ;
- cas F1ZUG / ADRASEC 35, dont le rôle est documenté mais dont la donnée spécifique ne doit pas être déduite de l'APRS ;
- attribution locale CROSS Étel Ch64, sans dupliquer la mémoire générique déjà publiée ;
- attribution locale CROSS Corsen Ch79, sans dupliquer la mémoire générique déjà publiée ;
- infrastructures radioamateur arrêtées, ambiguës ou nécessitant une revalidation actuelle.

## Garde-fous

La v0.1 reste immuable. Un report ne vaut jamais validation. Une simple attribution locale ne crée pas une nouvelle mémoire lorsque la même valeur RF existe déjà dans le pack de base. Les données privées PPDR restent exclues et les données non publiées ne sont jamais déduites.
