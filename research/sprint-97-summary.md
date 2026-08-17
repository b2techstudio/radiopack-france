# Sprint 97 — consolidation de l’état post-Sprint 96

Date : **17 août 2026**  
État logique : **0.21.86**

## Objectif

Formaliser le véritable point de reprise du dépôt après les derniers raffinements UX ajoutés au-dessus du Sprint 96, sans modifier les packs radio publiés ni les recherches RF en cours.

Le HEAD de référence de départ est `28ec3844ad0bd48aef74e4eafee5a1f59ee93390`.

## État UI désormais pris en compte

- Les pages régionales Normandie, Bretagne et Annecy–Alpes–Léman affichent des groupes de canaux repliables construits à partir des **CSV publics eux-mêmes**, afin d’éviter une seconde source de vérité.
- Bretagne conserve un regroupement aviation spécifique pour Rennes, Brest, Dinard et Quimper ; Brest reste contrôlé à cinq mémoires exactes dans `tests/test_pack_registry.py`.
- Le générateur multi-régions expose des raccourcis cliquables et accessibles au clavier pour Annecy–Alpes–Léman, Normandie et Bretagne.
- Les nombres affichés dans le générateur sont explicitement définis comme le nombre de mémoires présentes dans le CSV publié : **77 / 60** pour Annecy, **142** pour Normandie et **151** pour Bretagne.
- `publicPacks` reste la source de vérité des versions, variantes, compteurs et URLs des packs publics.

## Invariants préservés

- Normandie publique : **v0.4 / 142 RX**, immuable.
- Annecy–Alpes–Léman publique : **v0.4 / 77 RX**, variante **60 RX sans aviation**, immuable.
- Bretagne publique : **v0.2 / 151 RX**, immuable.
- Aucun CSV public, aucune fréquence, aucune mémoire RF et aucune règle d’émission ne sont modifiés par ce sprint.
- Bretagne v0.3 reste à **151 RX, delta 0**, avec revalidation AIRAC 09/26 obligatoire à partir du **3 septembre 2026** avant toute publication.
- Normandie v0.5 reste à **142 RX, delta 0** ; R3/F1ZBX et F5ZHA restent dépendants du terrain, F1ZOV reste en veille de statut opérateur et F6ZES reste sans RF/mode public exploitable.

## Reprise machine

L’état historique complet reste conservé dans `research/project-resume-state.json` au niveau Sprint 96 / 0.21.85. Le delta correspondant à ce Sprint 97 est enregistré dans `research/sprint-97-post96-ui-state.json` afin de ne pas réécrire ou réduire le gros état machine historique.

Pour reprendre le projet, lire dans cet ordre :

1. `PROJECT_STATUS.md` ;
2. `research/project-resume-state.json` ;
3. `research/sprint-97-post96-ui-state.json` ;
4. `research/sprint-97-summary.md`.

## Validation attendue

Les garde-fous existants restent la référence :

- `tests/test_pack_registry.py` pour le registre public, les détails de canaux CSV-backed et les libellés du générateur ;
- `tests/test_web_generator.py` pour la logique du générateur multi-régions ;
- build Astro et CI complète avant fusion.

Le Sprint 97 est volontairement un sprint de **consolidation documentaire et d’état** : il formalise le HEAD réel sans ouvrir de nouveau chantier RF avant que les gates externes soient franchis.
