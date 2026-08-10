# RadioPack France — Sprint 61

Date : **10 août 2026**  
État logique : **0.21.50**

Cette passe poursuit la recherche sans modifier aucun pack public. Normandie v0.3.1 reste figée à 139 mémoires, Annecy–Alpes–Léman v0.2 à 65/48 mémoires et Bretagne reste non publique.

## CROSS Étel — canal 64

Ajout de `research/bretagne-v0.1/etel-channel64-evidence.json` et passage de `etel-network.json` au schéma 1.1.

La situation du canal 64 est maintenant classée comme **conflit entre sources primaires actuelles** :

- la page ministérielle actuelle, mise à jour le 19 juin 2026, maintient l'affirmation que les canaux 63 et 64 diffusent un bulletin côtier permanent notamment dans le Morbihan ;
- la page actuelle du CROSS Étel nomme Étel et Chassiron en diffusion continue sur le canal 63 ;
- le planning météo actuellement lié par cette page liste les émetteurs et canaux utilisés sans mentionner 64 ;
- le bilan d'activité CROSS-A Étel 2025, publié le 13 mars 2026, décrit 16 stations VHF et 2 stations MF, liste les émetteurs météo réguliers et indique les stations renforcées Étel, Chassiron et Ferret sur le canal 63, sans mention de 64.

Cette divergence ne permet ni d'identifier le site breton du canal 64, ni de conclure à son arrêt. La paire RX 156.225 / 160.825 MHz était déjà connue : **delta RF 0**.

Le nombre de 17 stations radio mentionné dans une offre technique DIRM de juillet 2026 est conservé séparément du bilan 16 VHF + 2 MF : les unités de comptage ne sont pas définies de façon identique et ne sont pas réconciliées par simple calcul.

## CROSS Corsen — canal 79

Passage de `research/bretagne-v0.1/corsen-channel79-evidence.json` au schéma 1.1.

- La page actuelle CROSS Corsen confirme toujours le réseau VHF/MF littoral sans attribuer le canal 79 à un site précis.
- Le bilan officiel Corsen 2025 publié le 2 mars 2026 a été identifié ; son PDF de 14,6 Mio n'a pas pu être chargé dans le workflow de lecture courant et n'est donc pas utilisé pour inférer un canal ou un site.
- Une recherche primaire ciblée Cap Fréhel / Bodic / Batz n'a fourni aucune attribution Ch79 exploitable.
- Les indices secondaires actuels Cap Fréhel / Bodic restent des priorités de recherche mais ne sont pas promus.
- La paire 156.975 / 161.575 MHz était déjà connue : **delta RF 0**.

## Mortain-Bocage — scan REF adjacent

Ajout de `research/normandie-v0.4/mortain-adjacent-ref-scan.json`.

Le répertoire REF courant a été relu sur les départements 35, 50, 53 et 61 :

- Ille-et-Vilaine : R3/F1ZBX reste le cas analogique actif pertinent ; R71/F5ZEB conserve son conflit de statut REF/opérateur ; F5ZZC est arrêté.
- Manche : F5ZHY, F1ZBL et F1ZOV sont déjà suivis ; F6ZES reste incomplet.
- Mayenne : F6ZCE et F5ZHA restent les cas analogiques pertinents ; F5ZTQ est arrêté.
- Orne : les deux relais courants listés sont numériques C4FM/DMR.

Résultat : **0 nouveau relais analogique actif non déjà suivi**, **delta candidat 0**. Le scan est une preuve d'inventaire, pas une preuve de réception.

## Tests et garde-fous

- Mise à jour de `tests/test_etel_network_research.py` pour figer le conflit primaire Ch64 et distinguer les dimensions de comptage du réseau Étel.
- Ajout de `tests/test_sprint61_research.py` pour contrôler Ch64, Ch79, le scan REF adjacent, l'absence de mutation du candidat et l'absence de publication Bretagne.
- L'état machine passe à Sprint 61 / 0.21.50 sans changement du candidat Normandie v0.4 : **142 mémoires**, **3/9**, **6 blocages**, **0 ajout éligible**.

## État fin de passe

- Normandie v0.3.1 publique : **139 mémoires**, inchangée.
- Annecy–Alpes–Léman v0.2 publique : **65/48 mémoires**, inchangée.
- Normandie v0.4 candidat interne : **142 mémoires**, inchangé.
- Plafond connu si les portes actuelles sont franchies : **147 mémoires**.
- Nouveaux candidats analogiques issus du scan 35/50/53/61 : **0**.
- Canal 64 Étel : conflit primaire ouvert, site non identifié.
- Canal 79 Corsen : attribution primaire de site non résolue.
- Publication : **interdite**.
