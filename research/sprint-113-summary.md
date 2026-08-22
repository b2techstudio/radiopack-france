# Sprint 113 — Normandie v0.5 publiée sur couverture théorique

Date : **22 août 2026**

## Publication

Normandie v0.5 est publiée à **146 mémoires RX**, à partir de la v0.4 immuable de 142 mémoires.

- delta : **+4 RX** ;
- SHA candidat Sprint 112 : `1d7ce66c7a5faafe98e4ee59791bcd29af1fd1f432ee1bfc1cad7cba3bc5cf59` ;
- SHA CSV public v0.5 : `1d7ce66c7a5faafe98e4ee59791bcd29af1fd1f432ee1bfc1cad7cba3bc5cf59` ;
- identité byte-for-byte : **vérifiée** ;
- v0.4 / 142 RX : conservée comme version historique immuable.

## Quatre nouvelles mémoires

- 178 `35-R3-IN` — 145.075 MHz ;
- 179 `35-R3-OUT` — 145.675 MHz ;
- 180 `53-ZHA-V` — 145.4675 MHz ;
- 181 `53-ZHA-U` — 432.575 MHz.

Toutes restent `Duplex=off`, `Offset=0.000000`.

## Nature de la couverture

Ces quatre mémoires sont publiées sur une **couverture théorique documentée**. Elles ne sont pas présentées comme réception mesurée ou garantie.

La politique Sprint 112 utilise une plausibilité basée sur les paramètres publics, distance, géométrie simplifiée et FSPL. Les écoutes terrain deviennent un retour qualité facultatif et ne sont plus un gate de publication.

Les outils Sprint 84/85 ne sont pas supprimés : ils deviennent des **outils historiques facultatifs de contrôle qualité**. Leurs résultats ne peuvent ni retirer automatiquement une mémoire publiée, ni modifier automatiquement un candidat ou une publication.

## Toujours exclus

- F1ZOV : l'opérateur local le marque toujours en maintenance ;
- F6ZES : fréquence et mode publics non résolus ;
- l'ancienne fréquence secondaire F5ZHA 431.4125 MHz n'est pas promue.

## Publication web

- registre : Normandie v0.5 / 146 ;
- métadonnées région : v0.5 / 146 ;
- page région : mention explicite de la couverture théorique et de ses limites ;
- CSV public : `website/public/downloads/normandie/radiopack-france-normandie-v0.5.csv`.

## Références

- `research/normandie-v0.5/candidate-freeze.json`
- `research/normandie-v0.5/release-scope.json`
- `research/normandie-v0.5/publication-gates.json`
- `research/normandie-v0.5/publication-record.json`
- `tests/test_normandie_v05_public_release.py`
