# Sprint 83 — revalidation ciblée Normandie v0.5

État logique cible : **0.21.72**.

Le Sprint 83 reprend les quatre dossiers différés de Normandie v0.5 à partir de sources publiques actuelles. **Aucune mémoire n'est promue** : le candidat interne reste à **142 mémoires RX**, delta **0**. Le plafond potentiel connu reste **147 mémoires** hors F6ZES, dont la fréquence et le mode restent non résolus.

## Résultat

- base publique immuable : Normandie v0.4 = **142 RX** ;
- candidat v0.5 avant : **142 RX** ;
- candidat v0.5 après : **142 RX** ;
- delta RF : **0** ;
- promotions : **0** ;
- plafond potentiel connu hors F6ZES : **147 RX** ;
- aucun CSV public v0.5 ;
- aucun changement du registre public.

## R3 F1ZBX / Brocéliande

La page actuelle de l'ARA35 confirme le relais R3 F1ZBX opérationnel avec la paire **145.075 / 145.675 MHz** et un CTCSS temporaire de **71.9 Hz**. L'ARA35 documente encore des opérations d'entretien du site en 2025.

Décision : les paramètres opérateur sont solides, mais le gate du projet reste la **réception réelle depuis Mortain-Bocage**. Deux sessions RX indépendantes et identifiées restent nécessaires. Une source web ou une géométrie théorique ne peut pas fermer ce gate. **Delta 0**.

## F5ZHA Laval

Le répertoire REF courant donne F5ZHA **actif** à Laval comme transpondeur analogique transparent bidirectionnel sur **145.4675 / 432.575 MHz**. Une seconde liste actuelle indépendante reprend la même paire.

RepeaterBook conserve cependant **431.4125 MHz**, avec une entrée dont la date de vérification affichée est **2017-02-17**. Cette valeur est donc conservée comme conflit secondaire ancien pour diagnostic, mais elle ne remplace pas la paire courante du REF.

Décision : la paire REF **145.4675 / 432.575 MHz** reste la paire de diagnostic actuelle. La couverture utile depuis Mortain n'a toujours pas été démontrée par deux sessions identifiées ; aucune promotion. **Delta 0**.

## F1ZOV Equeurdreville-Hainneville

Le Radio Club Nord Cotentin F6KFW marque toujours **F1ZOV « En Maintenance »** et publie la paire **430.375 / 431.975 MHz**. Le répertoire REF le liste parallèlement actif.

Décision : pour l'état opérationnel courant, le statut de l'opérateur local reste prioritaire sur l'annuaire général. Le dossier reste bloqué jusqu'à disparition explicite du statut maintenance. **Delta 0**.

## F6ZES Sourdeval

Le REF continue de lister F6ZES à Sourdeval, responsable F1SMB, locator IN98MR93XV, altitude 230 m. La fiche publique exploitée ne fournit toujours ni fréquence utilisable, ni mode, ni état opérationnel.

Décision : aucune fréquence ni aucun mode ne sont devinés. **Delta 0**.

## Reproductibilité

Le nouveau builder `tools/build_normandie_v05_internal_candidate.py` reconstruit le candidat v0.5 comme copie exacte de la v0.4 publique immuable et vérifie son SHA-256, le contrat RX-only, l'unicité des positions/noms/RF et l'absence de remplissage artificiel.

Preuve : `research/normandie-v0.5/current-blocker-revalidation.json`.

Garde-fou : `tests/test_sprint83_normandie_v05_revalidation.py`.
