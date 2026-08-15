# Sprint 82 — revalidation publique ciblée Bretagne v0.3

État logique cible : **0.21.71**.

Le Sprint 82 revalide les six dossiers non-AIRAC encore ouverts de Bretagne v0.3 à partir de sources publiques actuelles ou explicitement historiques. **Aucune nouvelle RF n'est promue** : le candidat reste à **151 mémoires RX**, delta **0**, et Bretagne v0.2 reste la version publique immuable.

## Résultat

- candidat avant : **151 RX** ;
- candidat après : **151 RX** ;
- delta RF : **0** ;
- promotions : **0** ;
- aucun CSV public v0.3 ;
- aucun changement du registre public.

## F1ZUG / ADRASEC35

L'ARA35 publie toujours F1ZUG-4 comme digipeater APRS sur **144.800 MHz**. Le site est également décrit comme hébergeant un transpondeur pour le réseau ADRASEC35, mais **aucune fréquence publique du transpondeur n'est fournie**. Un index APRS public montre par ailleurs une activité récente de F1ZUG-4 dans le snapshot consulté.

Décision : APRS 144.800 MHz est déjà présent dans le bloc national ; **delta 0**. La fréquence du transpondeur ADRASEC35 reste `null` et n'est jamais déduite de l'APRS.

## F5ZZC-4

La page ARA35 disponible associe historiquement F5ZZC-4 à un digipeater APRS ADRASEC35 sur le campus de Ker Lann, mais son texte est ancré sur l'état de 2015. Aucune source publique actuelle assez forte n'a été trouvée pour valider une fréquence de service actuelle F5ZZC-4.

Décision : **delta 0**, pas de promotion. L'absence de trace récente dans un index public ne prouve pas un arrêt. F5ZZC-4 ne doit pas être confondu avec le relais analogique distinct F5ZZC, que l'annuaire REF donne arrêté.

## F5ZPV et F5ZZH

- **F5ZPV / RU19** : l'ARA35 le maintient explicitement « temporairement arrêté », même si l'annuaire général REF le liste actif. Le statut opérateur local reste prioritaire.
- **F5ZZH / R7X** : l'ARA35 le maintient temporairement arrêté et indique qu'un nouveau site est recherché.

Décision : aucune preuve de redémarrage, donc **delta 0** pour les deux.

## CROSS Étel Ch64

La page ministérielle 2026 maintient une diffusion météo permanente sur les canaux **63 et 64 dans le Morbihan**, sans nommer le site du canal 64. La page opérationnelle actuelle du CROSS Étel associe explicitement la station d'Étel au **canal 63**.

Décision : le conflit primaire reste ouvert ; aucune attribution locale Ch64 n'est promue. La paire générique `156.225 / 160.825 MHz` existe déjà, donc **delta RF 0**.

## CROSS Corsen Ch79

La page actuelle du CROSS Corsen confirme son réseau VHF/MHF côtier et la diffusion de bulletins météo depuis les stations du littoral, mais ne fournit pas de mapping primaire actuel **canal 79 → site émetteur précis**.

Décision : aucune attribution locale Ch79. La paire générique `156.975 / 161.575 MHz` existe déjà, donc **delta RF 0**.

## Frontières conservées

- donnée non publiée = non inférée ;
- APRS ≠ fréquence d'un autre service ;
- absence dans un index public ≠ preuve d'arrêt ;
- rôle historique ≠ fréquence actuelle validée ;
- opérateur local > annuaire général pour l'état courant ;
- infrastructure CROSS actuelle ≠ mapping canal → station ;
- métadonnée locale ≠ nouvelle mémoire si la RF générique existe déjà ;
- données opérationnelles privées PPDR/ADRASEC exclues.

Fichier de preuve : `research/bretagne-v0.3/public-service-revalidation.json`.

Garde-fou : `tests/test_sprint82_bretagne_v03_public_revalidation.py`.

## Clôture

Le dépôt nettoyé a passé la CI complète avant la clôture de référence : garde-fou Sprint 82, contrôles historiques, générateur public et build Astro sont verts. Le commit de clôture ne modifie aucune donnée radio ni le candidat ; il sert uniquement à produire l'archive exacte du HEAD de référence.
