# Normandie v0.5 — recherche

État : **Sprint 112 — candidat interne 146 mémoires RX, delta +4 fondé sur une couverture théorique documentée ; aucune publication dans ce sprint**.

Base publique immuable : **Normandie v0.4, 142 mémoires RX**.

## Politique de couverture actuelle

Les écoutes terrain ne sont plus un prérequis de promotion. Pour une station dont la fréquence, le mode et l'état courant sont déjà vérifiés publiquement, une **couverture théorique plausible** peut fermer le gate de couverture. Cette décision doit rester explicitement étiquetée comme théorique : elle ne signifie ni réception mesurée ni réception garantie.

Source de vérité : `theoretical-coverage-policy.json` et `sprint112-theoretical-coverage.json`.

Les anciens outils terrain Sprint 84/85 restent disponibles comme **retour qualité facultatif** ; ils ne bloquent plus le candidat ni une future publication.

## Promotions Sprint 112

### R3 / F1ZBX — +2 RX

- paire publique actuelle : **145.075 / 145.675 MHz** ;
- opérateur : ARA35, relais opérationnel ;
- site publié à Paimpont/Brocéliande, antenne ~262 m ASL ;
- distance théorique vers le point de référence Mortain : **~118.32 km** ;
- rayon d'usage publié par l'opérateur : **150 km** ;
- enveloppe géométrique 4/3 Terre basée sur les altitudes d'extrémité : **~129.44 km** ;
- décision : paire intégrée au candidat, **couverture théorique**.

Mémoires : `35-R3-IN` et `35-R3-OUT`, emplacements 178–179.

### F5ZHA Laval — +2 RX

- paire actuelle REF : **145.4675 / 432.575 MHz** ;
- statut REF : actif, transpondeur analogique transparent ;
- locator : `IN98OB86BQ`, altitude publiée 55 m ;
- distance théorique vers Mortain : **~65.66 km** ;
- enveloppe géométrique 4/3 Terre d'extrémité : **~93.31 km** ;
- l'ancienne valeur secondaire 431.4125 MHz reste exclue ;
- décision : paire intégrée au candidat, **couverture théorique**.

Mémoires : `53-ZHA-V` et `53-ZHA-U`, emplacements 180–181.

## Dossiers toujours exclus

- **F1ZOV** : l'opérateur local le marque toujours en maintenance. La théorie de propagation ne remplace pas un statut opérationnel courant.
- **F6ZES Sourdeval** : fréquence et mode publics toujours non résolus. Aucune fréquence n'est inférée.

Le plafond potentiel connu hors F6ZES reste donc **147 RX** si F1ZOV sort ultérieurement de maintenance.

## Limites de la théorie

Le calcul documente une plausibilité de trajet radio, pas une mesure de terrain. Il ne modélise pas complètement le relief intermédiaire, les bâtiments, la végétation, les diagrammes d'antenne, la sensibilité du récepteur ou le fading. Les commentaires des mémoires et la documentation publique doivent conserver la mention **couverture théorique**.

## Règles permanentes

RX-only, `Duplex=off`, `Offset=0.000000`, paires RF distinctes = deux mémoires RX, aucune fréquence devinée, pas de remplissage artificiel, v0.4 publique immuable, statut opérateur courant prioritaire, données privées/PPDR exclues.
