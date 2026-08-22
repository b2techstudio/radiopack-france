# Sprint 110 — Normandie v0.5 : revalidation sources et handoff terrain

Date : 2026-08-22

## Objectif

Reprendre la priorité Normandie v0.5 après la publication Auvergne-Rhône-Alpes v0.3, revalider les quatre dossiers encore ouverts avec les sources publiques actuellement disponibles et confirmer si un changement du candidat 142 RX est justifié.

## Résultat

**Zéro promotion, zéro mutation publique, candidat maintenu à 142 RX.**

Le plafond potentiel connu reste **147 RX hors F6ZES**, mais aucune des additions potentielles ne franchit aujourd'hui ses gates.

## R3 / F1ZBX

La page publique ARA35 confirme toujours le relais F1ZBX de Brocéliande/Paimpont, sortie **145.675 MHz**, entrée **145.075 MHz** et fonctionnement annoncé. Cette confirmation source ne répond pas au critère territorial du projet : la promotion reste conditionnée à **deux sessions RX indépendantes et identifiées depuis Mortain-Bocage** sur 145.675 MHz.

Le web ne peut donc pas fermer ce gate.

## F5ZHA

Le répertoire public REF confirme actuellement F5ZHA à Laval comme actif avec la paire crossband analogique **145.4675 / 432.575 MHz**. Le conflit RF ancien n'est pas réactivé.

La paire source est stable, mais la promotion reste conditionnée à **deux sessions RX indépendantes et identifiées depuis Mortain-Bocage**, avec intelligibilité minimale **3/5** selon la politique existante.

## F1ZOV

Le Radio Club Nord Cotentin F6KFW affiche toujours explicitement **« En Maintenance »** pour F1ZOV, avec RX **430.375 MHz**, TX **431.975 MHz**, shift +1600 kHz.

La source locale opérateur reste prioritaire sur un annuaire général : **aucune promotion** tant que ce statut courant n'est pas levé.

## F6ZES

Le répertoire REF expose toujours F6ZES à **Sourdeval**, responsable F1SMB, locator **IN98MR93XV**, mais sans fréquence ni mode exploitables publiés.

Le projet conserve donc la règle : **aucune inférence de fréquence**, aucun ajout au candidat et aucun ajout au plafond connu tant qu'une RF et un mode publics utilisables ne sont pas disponibles.

## Handoff terrain

Le kit Sprint 84 et la politique d'évaluation Sprint 85 couvrent déjà entièrement les besoins actuels :

- R3/F1ZBX : 2 sessions indépendantes ;
- F5ZHA : 2 sessions indépendantes ;
- sondes RX-only déjà définies ;
- journal de sessions reproductible ;
- évaluateur automatique autorisé à produire un verdict de gate ;
- **aucune mutation automatique du candidat** ;
- **aucune publication automatique** ;
- revue humaine des sources encore obligatoire après un éventuel gate terrain satisfait.

Aucune nouvelle mémoire de diagnostic ni nouvel outil terrain n'est nécessaire dans ce sprint.

## Artefacts

- `research/normandie-v0.5/sprint110-source-field-refresh.json`
- `tests/test_sprint110_normandie_v05_refresh.py`
- `.github/workflows/sprint110-normandie-v05-refresh.yml`

## Suite

La prochaine action utile pour Normandie v0.5 est la collecte de vraies sessions terrain Mortain-Bocage via le kit existant. En parallèle, maintenir une veille source sur F1ZOV et F6ZES. Sans nouvelle preuve terrain ou source, le candidat reste **142 RX / delta 0** et la v0.4 publique reste immuable.
