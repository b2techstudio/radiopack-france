# Sprint 62 — frontières de preuve primaire CROSS Étel / Corsen

Date : **11 août 2026**  
État logique : **0.21.51**  
Statut : **recherche uniquement, aucun changement public**

## Objectif

Approfondir les deux dossiers maritimes encore ouverts sans transformer une convergence documentaire, une infrastructure radio ou une source historique en preuve opérationnelle actuelle non démontrée.

## CROSS Étel — canal 64

La page ministérielle actuelle conserve l'affirmation que les canaux **63 et 64** diffusent un bulletin météo côtier permanent notamment dans le Morbihan.

En parallèle, trois sources opérationnelles locales actuelles exploitées convergent explicitement vers le **canal 63** :

- la page actuelle du CROSS Étel nomme Étel et Chassiron en diffusion continue sur 63 ;
- le planning météo actuellement lié par le CROSS liste Étel et Chassiron sur 63 et les autres émetteurs sur 79/80, sans mentionner 64 ;
- le bilan d'activité 2025 liste les stations renforcées Étel, Chassiron et Ferret sur 63, sans mentionner 64.

Cette convergence ne permet toujours pas de conclure que le canal 64 est arrêté ou absent. Le dossier reste un **conflit entre sources primaires actuelles** : l'opération actuelle de Ch64 n'est pas prouvée, son arrêt n'est pas prouvé et aucun site n'est attribué.

Météo-France a publié le 5 août 2026 une page présentant son **Guide Marine 2026** comme une référence contenant notamment horaires, fréquences radio et contenu des bulletins VHF. Le PDF a été identifié mais n'a pas pu être exploité dans le workflow courant ; il devient une cible primaire de réconciliation sans produire aucune conclusion par défaut.

Paire RX Ch64 déjà présente dans la recherche Bretagne : **156.225 / 160.825 MHz**. Delta RF : **0**.

## CROSS Corsen — canal 79

Deux infrastructures actuelles sont désormais séparément qualifiées comme preuves d'infrastructure, sans affectation de canal :

- **Cap Fréhel** : la DIRM confirme que le CROSS Corsen dispose au phare d'équipements de suivi et de liaison avec les navires ;
- **Stiff / Ouessant** : une offre officielle 2026 et le marché public DGAMPA de rénovation indiquent que la tour/vigie abrite aujourd'hui des équipements de radiocommunications ou des équipements radio nécessaires au CROSS Corsen.

Une source primaire historique de 2003 documente l'utilisation du canal 79 par Ouessant Traffic / CROSS Corsen après appel sur 16 et l'architecture radio historique autour du Stiff, de la Pointe du Raz et de Corsen. Elle reste **historique** : elle explique les cibles de revalidation mais ne prouve aucune affectation 2026.

La source locale actuelle du Club de Voile de la Baie d'Erquy continue d'associer Ch79 à **Cap Fréhel** et **Bodic**. C'est un indice secondaire actuel, pas une validation primaire.

Le Guide Marine 2026 de Météo-France est également enregistré comme cible primaire pertinente, mais son PDF non extrait ne peut pas être utilisé pour attribuer un site.

Conclusion : Cap Fréhel et Stiff/Ouessant sont des infrastructures actuelles vérifiées ; l'affectation actuelle du **canal 79** à un site précis reste non résolue. Paire RX déjà connue **156.975 / 161.575 MHz**, delta RF **0**.

## Normandie v0.4

Aucun changement de candidat :

- base publique immuable : **139 mémoires** ;
- candidat interne : **142 mémoires** ;
- preview : **142 mémoires** ;
- plafond de travail connu si les portes actuelles passent : **147 mémoires** ;
- revue : **3/9** ;
- blocages ouverts : **6** ;
- ajouts éligibles actuels : **0**.

Le scan REF adjacent du Sprint 61 reste valide et n'ajoute aucun nouveau candidat analogique.

## Garde-fous ajoutés

- une convergence locale sur Ch63 ne réfute pas à elle seule Ch64 ;
- l'absence de Ch64 dans les documents opérationnels locaux actuels n'est pas une preuve d'arrêt ;
- une référence primaire identifiée mais non extractible n'est pas une preuve négative ;
- une infrastructure radio actuelle ne permet pas d'attribuer un canal précis ;
- une affectation historique primaire ne vaut pas validation actuelle ;
- une source secondaire actuelle peut prioriser une cible mais ne permet pas la promotion ;
- aucune nouvelle mémoire RF et aucune mutation publique ne résultent de cette passe.

## Fichiers principaux

```text
research/bretagne-v0.1/etel-channel64-evidence.json
research/bretagne-v0.1/corsen-channel79-evidence.json
tests/test_sprint62_primary_reference_boundaries.py
research/project-resume-state.json
PROJECT_STATUS.md
README.md
```

## Suite prioritaire

1. Extraire une version exploitable du **Guide Marine 2026 Météo-France** pour vérifier directement les tableaux VHF actuels.
2. Chercher un inventaire technique nominatif actuel des stations CROSS Étel afin de réconcilier définitivement Ch64.
3. Chercher une source primaire actuelle associant explicitement Ch79 à Cap Fréhel, Bodic, Batz, Stiff/Ouessant ou Pointe du Raz.
4. À défaut de nouvelle preuve documentaire maritime, reprendre les validations terrain Normandie R3/F5ZHA sans utiliser le terrain pour fermer les conflits de sources.
