# Bourgogne-Franche-Comté v0.3 — recherche

Initialisation : **19 août 2026**.

La v0.3 démarre depuis la **v0.2 publique immuable de 37 mémoires RX**. Aucun CSV public et aucune fréquence publiée ne sont modifiés à cette étape.

## Premier audit public

La liste publique des relais du REF, indiquée comme mise à jour le **13 mai 2026**, a été revue pour les départements 21, 25, 39, 58, 70, 71, 89 et 90.

Les trois paires VHF déjà présentes dans la v0.2 sont toujours visibles comme actives dans cette source :

- F1ZDK — Mont-Saint-Vincent — 145.750 / 145.150 MHz ;
- F5ZBP — Saint-Thiébaud — 145.775 / 145.175 MHz ;
- F1ZCT — Chitry — 145.7875 / 145.1875 MHz.

Le libellé public historique de F5ZBP reste volontairement inchangé dans la v0.2 ; la différence de nom de site relevée dans l'annuaire courant est seulement tracée pour la prochaine version.

## Leads analogiques v0.3

Dix stations analogiques FM actives constituent le premier backlog : F5ZIQ, F1ZCA, F5ZNS, F5ZVA, F5ZXZ, F5ZFE, F5ZKM, F5ZMS, F5ZTJ et F5ZFQ.

En appliquant la politique paired RX à chaque paire distincte, leur plafond théorique est de **20 mémoires supplémentaires avant déduplication**. Ce nombre n'est pas un candidat publié : la v0.3 reste actuellement à **37 RX, delta 0**.

Chaque lead doit encore recevoir une confirmation publique indépendante et actuelle, idéalement par l'association ou l'opérateur local, avant toute promotion dans un candidat interne. Un statut temporaire, arrêté ou ambigu ne compte pas comme validation.

## Périmètre

La priorité est donnée aux relais et transpondeurs **analogiques FM** réellement utiles en réception sur UV-K5. Les infrastructures uniquement numériques restent différées. Les réseaux privés, PPDR ou non publiquement vérifiables restent exclus.

Fichiers de travail :

- `pack-plan.json` — contrat de la v0.3 ;
- `backlog.json` — leads analogiques non promus ;
- `current-ref-audit.json` — photographie de l'audit REF courant.

Source de départ : `https://www.r-e-f.org/index.php?Itemid=492&id=1279&option=com_content&view=article`.
