# Sprint 97 — consolidation de l’état post-Sprint 96

Date : **17 août 2026**  
État logique : **0.21.86**

## Résultat

Le Sprint 97 formalise comme état officiel les raffinements UX déjà présents au-dessus du Sprint 96, sans modifier les packs radio publiés ni les recherches RF en cours.

- Les pages régionales Normandie, Bretagne et Annecy–Alpes–Léman affichent des groupes de canaux repliables construits directement depuis les **CSV publics**, afin de conserver une seule source de vérité pour le contenu affiché.
- Bretagne conserve ses groupes aviation contrôlés pour Rennes, Brest, Dinard et Quimper ; Brest reste gardé à cinq mémoires exactes dans `tests/test_pack_registry.py`.
- Le générateur multi-régions propose des raccourcis de sélection cliquables et accessibles au clavier pour Annecy–Alpes–Léman, Normandie et Bretagne.
- Les nombres du générateur sont explicitement définis comme les nombres de mémoires des CSV publiés : **77 / 60** pour Annecy, **142** pour Normandie et **151** pour Bretagne.
- `publicPacks` reste la source de vérité des versions, variantes, compteurs et URLs des packs publics.

## Synchronisation de l’état

La clôture du Sprint 97 synchronise désormais le même état **97 / 0.21.86** dans :

- `README.md` ;
- `PROJECT_STATUS.md` ;
- `CHANGELOG.md` ;
- `research/project-resume-state.json` ;
- `research/sprint-97-post96-ui-state.json` ;
- ce résumé.

Un garde-fou dédié, `tests/test_sprint97_state_sync.py`, vérifie cette cohérence ainsi que les invariants publics et est exécuté par `RadioPack CI`.

## Invariants préservés

- Normandie publique : **v0.4 / 142 RX**, immuable.
- Annecy–Alpes–Léman publique : **v0.4 / 77 RX**, variante **60 RX sans aviation**, immuable.
- Bretagne publique : **v0.2 / 151 RX**, immuable.
- Aucun CSV public, aucune fréquence, aucune mémoire RF et aucune règle d’émission ne sont modifiés par ce sprint.
- Bretagne v0.3 reste à **151 RX, delta 0**, avec revalidation AIRAC 09/26 obligatoire à partir du **3 septembre 2026** avant toute publication.
- Normandie v0.5 reste à **142 RX, delta 0** ; R3/F1ZBX et F5ZHA restent dépendants du terrain, F1ZOV reste en veille de statut opérateur et F6ZES reste sans RF/mode public exploitable.

## Reprise machine

L’état officiel complet est `research/project-resume-state.json` au niveau **Sprint 97 / 0.21.86**. `research/sprint-97-post96-ui-state.json` conserve le détail structuré des changements UX consolidés par ce sprint ; il complète l’état principal sans le remplacer.

Ordre de reprise recommandé :

1. `PROJECT_STATUS.md` ;
2. `research/project-resume-state.json` ;
3. `research/sprint-97-summary.md` ;
4. `research/sprint-97-post96-ui-state.json`.

## Validation de clôture

La fusion reste conditionnée à une CI verte. Les contrôles attendus comprennent notamment :

- `tests/test_sprint97_state_sync.py` ;
- `tests/test_pack_registry.py` ;
- `tests/test_web_generator.py` ;
- `tests/test_sprints89_91_integrity.py` ;
- le build Astro ;
- les audits et gardes de release existants.
