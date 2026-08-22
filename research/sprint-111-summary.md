# Sprint 111 — Bretagne v0.3 AIRAC 09/26 readiness

Date : **22 août 2026**  
État logique prévu : **0.21.99**

## Résultat

Le Sprint 111 prépare la revalidation aviation de Bretagne v0.3 sans modifier le pack public ni présumer le contenu opérationnel du prochain cycle.

- Bretagne v0.2 publique : **151 RX**, immuable ;
- candidat v0.3 interne : **151 RX**, delta **0** ;
- bloc aviation à revalider : **16 mémoires**, positions **130–145** ;
- AIRAC 08/26 reste courant jusqu'au **2 septembre 2026 inclus** ;
- AIRAC 09/26 est déjà disponible sur le site SIA mais n'entre en vigueur que le **3 septembre 2026** ;
- aucun CSV public v0.3 n'est créé ;
- aucune mutation RF n'est effectuée.

## Préparation ajoutée

`research/bretagne-v0.3/airac09-readiness.json` enregistre la disponibilité anticipée du produit SIA AIRAC 09/26 tout en le marquant explicitement comme **non courant au 22 août**.

`research/bretagne-v0.3/airac09-revalidation-template.json` fournit une matrice vide de 16 lignes correspondant exactement à la baseline aviation AIRAC 08/26. Chaque mémoire devra être décidée explicitement `unchanged`, `changed` ou `removed` avec source et note de preuve.

`tools/check_bretagne_v03_airac09_revalidation.py` impose les gates suivants :

1. date d'évaluation dans la fenêtre AIRAC 09/26 ;
2. vérification d'une source primaire courante ;
3. décision explicite sur les 16 mémoires ;
4. source AIRAC 09/26 pour chaque décision ;
5. revue humaine datée ;
6. aucune revendication XML champ par champ sans extraction des octets XML.

Le validateur ne peut jamais publier ni modifier automatiquement le candidat. Un verdict positif autorise uniquement la reconstruction d'un **candidat interne**, suivie d'une prépublication séparée.

## Protection temporelle

Le test Sprint 111 vérifie explicitement qu'une matrice complète, même synthétique, **ne peut pas franchir le gate au 22 août 2026**. Le 3 septembre, le template vierge reste également bloqué tant que les 16 décisions et la revue primaire/humaine ne sont pas présentes.

## Sources de cycle

- SIA France — Données aéronautiques XML AIRAC 09/26, annoncées en vigueur du 03/09/2026 au 30/09/2026 inclus ;
- EUROCONTROL Network Manager — AIRAC 2609, du 03/09/2026 au 30/09/2026.

La disponibilité anticipée de ces sources ne vaut pas validation courante avant leur date d'effet.

## Suite

Avant le 3 septembre : aucune revalidation AIRAC 09/26 ne peut être clôturée.

À partir du 3 septembre : copier le template, revalider les 16 mémoires à partir des sources alors courantes, faire la revue humaine, exécuter le validateur avec `--require-candidate-rebuild-ready`, puis seulement reconstruire le candidat interne v0.3. Toute publication restera une étape séparée.
