# Sprint 22 — Finition post-publication

Date : 2026-08-09

## Objectifs

- nettoyer les restes actifs d'Annecy v0.1 après la publication de la v0.2 ;
- conserver des redirections pour les anciennes URL ;
- simplifier le générateur web en sélectionnant directement les routes CSV publiques ;
- ajouter les liens officiels SOFIA-Briefing et Skybriefing dans le contrôle NOTAM ;
- extraire un moteur CHIRP générique réutilisable pour les prochains packs régionaux ;
- documenter le workflow de création d'un nouveau pack ;
- mettre à jour le README et les garde-fous CI.

## Nettoyage v0.1

Les fichiers actifs de l'ancienne version Annecy/Haute-Savoie v0.1 sont retirés du dépôt :

- ancien manifeste régional ;
- ancien inventaire aviation AIRAC 07/26 ;
- ancien inventaire de relais ;
- ancien CSV régional ;
- ancien CSV relais ;
- ancien guide PDF.

L'historique reste disponible dans Git. Les anciennes URL publiques utiles sont redirigées vers Annecy–Alpes–Léman v0.2 ou vers sa page régionale.

## Générateur web

Le générateur ne reconstruit plus un Blob CSV dans le navigateur. Il sélectionne directement l'une des deux routes prérendues et validées :

- 65 mémoires avec aviation ;
- 48 mémoires sans aviation.

Le bouton et le nom de fichier affiché suivent automatiquement la variante choisie.

Le contrôle NOTAM reste facultatif et non bloquant. Des liens directs vers les services officiels sont ajoutés :

- SOFIA-Briefing pour la France ;
- Skybriefing pour la Suisse.

## Architecture réutilisable

`website/src/lib/chirpPack.ts` contient désormais les règles génériques :

- chargement des jeux de données ;
- filtrage par statut de vérification ;
- assemblage des positions ;
- contrôle des doublons ;
- limite de 200 mémoires ;
- noms de 10 caractères maximum ;
- génération CHIRP RX avec `Duplex=off` et `Offset=0.000000`.

`website/src/lib/annecyPack.ts` devient un wrapper de configuration spécifique à Annecy–Alpes–Léman.

Le document `REGIONAL-PACK-WORKFLOW.md` décrit la procédure à réutiliser pour les prochaines régions.

## Politique de publication

Annecy–Alpes–Léman v0.2 reste le pack public courant. Le nettoyage de la v0.1 ne modifie aucune des 65 mémoires revues de la v0.2 ni sa variante 48 mémoires.
