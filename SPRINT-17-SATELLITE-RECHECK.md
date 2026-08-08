# Sprint 17 — Recontrôle satellites et readiness verte

Date : 2026-08-08

## Objectif

Fermer la dernière porte réellement bloquante avant la génération de prépublication d'Annecy–Alpes–Léman v0.2.

## Sources officielles AMSAT revérifiées

- Live FM Satellites : https://www.amsat.org/live-fm-satellites/
- SO-50 satellite information : https://www.amsat.org/two-way-satellites/so-50-satellite-information/
- AO-91 Fox-1B : https://www.amsat.org/two-way-satellites/ao-91/
- Live OSCAR Satellite Status : https://www.amsat.org/status/
- Satellite Status API : https://www.amsat.org/status/api/

## Résultat

Les trois mémoires satellites du candidat restent cohérentes avec les publications AMSAT consultées le 2026-08-08 :

| Mémoire | Satellite | Descente mémorisée | Métadonnée de montée | Limite |
|---|---|---:|---|---|
| `SAT-SO50` | SO-50 | 436.795 MHz | 145.850 MHz, CTCSS 67 Hz, activation 74.4 Hz | — |
| `SAT-AO91` | AO-91 | 145.960 MHz | 435.250 MHz | passages éclairés uniquement à cause de la batterie |
| `SAT-AO123` | AO-123 | 435.400 MHz | 145.850 MHz, CTCSS 67 Hz | — |

Aucune liaison montante n'est exportée comme mémoire séparée.

## Portes de publication

La porte `dynamic_satellites` passe à `passed_official_amsat_recheck`.

Les quatre portes bloquantes sont désormais validées :

- `airac_fr`
- `airac_ch`
- `pending_airfields`
- `dynamic_satellites`

Les contrôles NOTAM France et Suisse restent facultatifs et non bloquants.

## Readiness

`tools/check_annecy_release_readiness.py` doit désormais répondre `READY` et retourner le code de sortie 0.

Le candidat reste à 65 mémoires et aucun CSV Annecy–Alpes–Léman v0.2 n'est encore exposé sous `website/public`.

## Étape suivante

Générer le candidat de prépublication v0.2, le contrôler comme export CHIRP final, puis préparer son intégration au générateur et au site. La publication effective reste une action séparée.
