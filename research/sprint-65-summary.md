# Sprint 65 — recontrôle primaire courant sans promotion

Date : 11 août 2026  
État logique : `0.21.54`

## Objectif

Rafraîchir les sources primaires encore utiles aux blocages Normandie v0.4 et Bretagne v0.1, sans modifier un pack public et sans transformer une information régionale ou d'infrastructure en attribution de site/canal.

## Normandie v0.4

### F5ZHA Laval

Le répertoire courant du REF continue d'afficher F5ZHA actif à Laval avec la paire analogique FM :

- 145.4675 MHz ;
- 432.575 MHz.

Cette revalidation maintient la paire de travail mais **ne ferme pas** la porte de publication : le contrat du dépôt exige toujours une source locale actuelle ou une source autoritative équivalente pour réconcilier définitivement le conflit historique, plus une validation de pertinence/réception depuis Mortain.

Résultat :

- source gate : fermé ;
- terrain Mortain : fermé ;
- delta candidat : 0.

### F6ZES Sourdeval

Le REF courant continue de confirmer :

- F6ZES ;
- Sourdeval ;
- responsable F1SMB ;
- locator `IN98MR93XV` ;
- altitude 230 m.

La ligne ne fournit toujours ni fréquence, ni mode, ni état opérationnel exploitable.

Résultat :

- fréquence/mode : non résolus ;
- delta candidat : 0 ;
- règle `must_not_guess_frequency` maintenue.

### État Normandie

Aucune porte n'est franchie :

- candidat interne : 142 ;
- preview : 142 ;
- plafond de travail connu : 147 ;
- revue : 3/9 ;
- blocages : 6 ;
- ajouts éligibles : 0.

R3 reste dépendant de deux sessions terrain indépendantes ; Sprint 64 continue de verrouiller que la paire R3 représente deux mémoires RX, indépendamment du nombre de sessions de preuve.

## Bretagne v0.1

### Ministère — déclaration VHF actuelle

La page ministérielle `Règles de sécurité pour les loisirs nautiques en mer`, mise à jour le 19 juin 2026, indique actuellement :

- le canal 16 annonce les diffusions météo CROSS sur 79 et 80 ;
- les canaux 63 et 64 diffusent un bulletin météo côtier permanent dans le Morbihan, entre autres zones.

Cette déclaration est primaire et actuelle mais **régionale** : elle ne nomme aucun émetteur Ch64.

Règle conservée : `current_regional_channel_statement_does_not_identify_transmitter_site`.

### CROSS Étel — source locale actuelle

La page DIRM du CROSS Étel, mise à jour le 24 novembre 2025, indique :

- annonces sur le canal 16 puis écoute sur 79 ou 80 pour les vacations ;
- diffusion continue sur Ch63 depuis les stations d'Étel et de Chassiron.

Elle ne nomme aucun site Ch64. Son absence de Ch64 ne prouve ni fonctionnement ni arrêt du canal 64.

Le conflit primaire reste donc ouvert :

- ministère : Ch63 + Ch64 permanent dans le Morbihan ;
- source locale CROSS : Étel/Chassiron sur Ch63 ;
- site Ch64 : non identifié.

La paire Ch64 reste 156.225 / 160.825 MHz, soit deux mémoires RX si le canal devient publiable, avec delta RF actuel 0.

### CROSS Corsen — source locale actuelle

La page DIRM du CROSS Corsen, mise à jour le 24 mars 2026, confirme :

- un réseau radio VHF/MHF veillé en permanence ;
- des bulletins météo diffusés plusieurs fois par jour depuis des stations VHF/MHF déployées sur le littoral.

Elle ne fournit aucun mapping Ch79 ↔ station.

Cap Fréhel reste une infrastructure CROSS actuelle vérifiée pour le suivi et la liaison avec les navires, mais cette infrastructure ne permet toujours pas d'y attribuer Ch79.

La paire Ch79 reste 156.975 / 161.575 MHz, soit deux mémoires RX si le canal devient publiable, avec delta RF actuel 0.

### Guide Marine 2026

La page Météo-France du 5 août 2026 continue d'indiquer que le Guide Marine contient notamment horaires et fréquences radio des bulletins VHF.

Le lien direct du PDF 2026 a été retenté le 11 août 2026. Le workflow web retourne toujours `cache miss` :

- contenu PDF non extrait ;
- aucune capture PDF disponible ;
- aucune inférence Ch64 ;
- aucune attribution Ch79.

Un document primaire identifié mais non lu reste une cible de recherche, pas une preuve.

## Nouveaux garde-fous Sprint 65

- une déclaration régionale courante sur un canal ne nomme pas automatiquement un site émetteur ;
- la confirmation courante d'un réseau de stations CROSS ne mappe pas automatiquement un canal vers une station ;
- l'infrastructure radio courante ne vaut pas affectation de canal ;
- une absence locale ne vaut pas preuve d'arrêt ;
- un PDF primaire non lu ne produit aucune inférence ;
- une fréquence non résolue n'est jamais inventée.

## Tests

Nouveau test :

```powershell
python tests\test_sprint65_primary_recheck.py
```

Il vérifie les limites F5ZHA/F6ZES, les déclarations primaires ministère/Étel/Corsen, le maintien des deux mémoires RX Ch64/Ch79, l'absence de site promu et l'immutabilité des packs publics.

## État public

Aucun changement :

- Normandie v0.3.1 : 139 mémoires ;
- Annecy–Alpes–Léman v0.2 : 65 mémoires, variante 48 sans aviation ;
- Bretagne : non publique ;
- Normandie v0.4 : non publique.
