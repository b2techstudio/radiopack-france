# Sprint 63 — revalidation des blocages externes

Date : **11 août 2026**  
État logique : **0.21.52**

## Objectif

Recontrôler les blocages qui peuvent évoluer par source externe sans fabriquer de preuve terrain et sans modifier les packs publics : F1ZOV, F5ZHA, F6ZES, puis la piste Guide Marine 2026 pour les canaux CROSS 64 et 79.

## Normandie v0.4

### F1ZOV — statut opérateur inchangé

Le Radio Club Nord Cotentin F6KFW publie toujours **F1ZOV — En Maintenance** et conserve la paire **430.375 / 431.975 MHz**. Le REF général le liste actif, mais la règle du projet donne priorité à l'exploitant local pour l'état opérationnel courant.

Décision : porte fermée, delta candidat **0**.

### F5ZHA — conflit secondaire mieux daté, mais porte toujours fermée

Le REF actuel conserve F5ZHA Laval actif comme transpondeur analogique transparent sur **145.4675 / 432.575 MHz**. RepeaterBook conserve la valeur conflictuelle **431.4125 MHz**.

La page de vérification par âge de RepeaterBook montre pour cette ligne une date de vérification **2017-02-17** et l'état affiché **Off-Air**. La valeur conflictuelle est donc désormais qualifiée comme **conflit secondaire stale/ancien**, et non comme une preuve actuelle de même poids que le REF.

Cette requalification ne ferme toutefois pas la porte. `promotion-gates.json` exige explicitement une **source locale actuelle ou une source autoritative équivalente**, en plus de la validation de pertinence/réception depuis Mortain. Aucune telle source de fréquence n'a été trouvée dans cette passe, et aucune observation terrain n'est disponible dans le dépôt.

Décision : conflit mieux qualifié mais réconciliation autoritative toujours incomplète ; couverture Mortain non validée ; delta candidat **0**.

### F6ZES Sourdeval — toujours aucune fréquence ni mode

Le REF actuel confirme encore :

- F6ZES ;
- Sourdeval ;
- responsable F1SMB ;
- locator `IN98MR93XV` ;
- altitude 230 m.

Les champs état, bande, émission, réception et mode restent vides. Des recherches ciblées sur `F6ZES F1SMB`, `F6ZES 145`, `F6ZES 430` et `F6ZES FM` n'ont pas fourni de seconde source actuelle suffisamment précise.

Une recherche infructueuse n'est pas une preuve d'arrêt ou d'absence.

Décision : fréquence et mode non résolus, aucune conjecture, delta candidat **0**.

### R3 / F1ZBX

Aucune nouvelle observation RX terrain n'est présente dans le dépôt. La porte exige toujours au moins deux sessions indépendantes valides depuis Mortain-Bocage.

Décision : porte terrain inchangée, delta candidat **0**.

## Bretagne v0.1 — Guide Marine 2026

La page Météo-France datée du **5 août 2026** confirme que le Guide Marine contient notamment les horaires et fréquences radio ainsi que le contenu des bulletins VHF.

Le lien PDF direct a été identifié :

`https://meteofrance.fr/sites/default/files/files/editorial/Guide%20MARINE%202026.pdf`

Le chargement du PDF a de nouveau été tenté dans le workflow web le 11 août 2026 mais a échoué sur un **cache miss**. Le contenu n'a donc pas été extrait et aucune capture de page PDF n'a pu être produite. Cette limitation ne devient ni preuve négative ni autorisation d'inférer un site.

Le ministère conserve par ailleurs l'indication générale selon laquelle le canal 16 annonce les diffusions sur 79/80 et que 63/64 assurent une diffusion permanente notamment dans le Morbihan. Cette page ne fournit pas de site émetteur précis pour Ch64 ou Ch79.

Décision :

- Étel Ch64 : site toujours non résolu ;
- Corsen Ch79 : site toujours non résolu ;
- delta RF Bretagne **0**.

## État final Sprint 63

- Normandie v0.4 candidat interne : **142 mémoires** ;
- preview : **142** ;
- plafond connu : **147** ;
- revue : **3/9** ;
- blocages : **6** ;
- ajouts éligibles : **0** ;
- aucune fréquence F6ZES inventée ;
- aucun changement Ch64/Ch79 depuis un PDF non lu ;
- aucun CSV public modifié ;
- aucun changement du registre public.

Le fichier machine de cette passe est `research/sprint-63-source-revalidation.json`.
