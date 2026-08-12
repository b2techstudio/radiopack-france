# Sprint 79 — Bretagne v0.2 revue de maturité et prépublication

Date : 12 août 2026  
État logique visé : `0.21.68`

## Résultat

Le candidat interne Bretagne v0.2 est **figé à 151 mémoires RX** : Bretagne v0.1 publique et immuable à 135 + 16 mémoires aviation AIRAC 08/26.

La revue de maturité classe les dossiers restants et conclut à **10/10 contrôles passés, 0 bloqueur, prépublication prête**, sans publier la v0.2. Aucun CSV public v0.2 ni changement du registre public n'est effectué.

## Aviation incluse

Le produit SIA **AIRAC 08/26 - CORRIGENDUM** reste le cycle courant au 12 août 2026, en vigueur du **6 août au 2 septembre 2026 inclus**. Les 16 mémoires déjà intégrées restent donc dans le périmètre figé.

La frontière méthodologique reste explicite : les octets de l'export XML courant n'ont pas été extraits dans le workflow du dépôt. RadioPack France utilise le contexte AIRAC courant et les dernières pages AIP primaires publiques effectives déjà validées, mais ne revendique aucune comparaison XML champ par champ non effectuée.

## Dossiers résolus ou reportables

- **ADRASEC public 22/29/35/56** : revue close à delta RF 0 ; les fréquences opérationnelles non publiées restent exclues.
- **F1ZUG / ADRASEC 35** : APRS 144.800 MHz est déjà couvert ; la fréquence du transpondeur ADRASEC non publiée est reportée et jamais inférée.
- **CROSS Étel Ch64 / Corsen Ch79** : les paires RF génériques sont déjà valides ; les mappings locaux non prouvés deviennent des métadonnées optionnelles reportables, pas des bloqueurs.
- **F1ZBZ** : résolu à delta RF 0.
- **F5ZPV / F5ZZH / F5ZZC-4** : restent hors périmètre v0.2 tant qu'ils sont arrêtés ou non résolus.

## Prépublication

Nouveaux artefacts :

```text
research/bretagne-v0.2/maturity-review.json
research/bretagne-v0.2/release-scope.json
research/bretagne-v0.2/review-checklist.json
research/bretagne-v0.2/publication-gates.json
tools/run_bretagne_v02_prepublication_audit.py
tests/test_sprint79_bretagne_v02_maturity.py
```

Le scope est figé à **151**, la checklist est à **10/10**, le nombre de bloqueurs est **0**, et l'audit doit reconstruire exactement le candidat tout en vérifiant que v0.2 reste absente des téléchargements et du registre publics.

## Frontière de publication

`prepublication_ready=true` ne signifie jamais `public_release_allowed=true`.

La publication doit rester un sprint séparé et explicite qui devra :

- reconstruire et figer le CSV revu ;
- enregistrer son empreinte ;
- basculer explicitement le registre et le téléchargement publics ;
- préserver Bretagne v0.1 comme version historique immuable ;
- recontrôler la fraîcheur aviation si la publication intervient hors de la fenêtre AIRAC 08/26 actuelle.

## Décision

- candidat : **151 RX** ;
- delta Sprint 79 : **0** ;
- revue : **10/10** ;
- bloqueurs : **0** ;
- prépublication : **prête** ;
- publication : **non effectuée**.
