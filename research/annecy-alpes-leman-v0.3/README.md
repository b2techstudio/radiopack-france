# Annecy–Alpes–Léman v0.3 — publiée

État : **Sprint 88 / 0.21.77 — v0.3 publiée et immuable à 76 mémoires RX, 59 sans aviation**.

La v0.3 part de la v0.2 publique immuable (65 / 48) et ajoute **11 fréquences RF uniques** selon la politique paired RX. Les deux CSV publics sont générés par `tools/build_annecy_v03_release_candidate.py`, contrôlés par la CI puis figés par SHA-256 dans `publication-record.json`.

## Résultat

- version complète : **76 RX** ;
- sans aviation : **59 RX** ;
- aviation : **17 RX** ;
- delta v0.2 → v0.3 : **+11 RF uniques** ;
- émission désactivée : `Duplex=off`, `Offset=0.000000` ;
- aucune fréquence privée, PPDR ou ADRASEC opérationnelle non publiée ;
- aucune duplication d'une RF uniquement pour multiplier les sites ou rôles.

## Ajouts v0.3

- satellites split : 145.850 MHz (SO-50/AO-123, une seule mémoire) et 435.250 MHz (AO-91) ;
- relais France : 439.625, 145.0375, 145.050, 430.325, 431.425 MHz ;
- Haute-Savoie : 145.1875 / 145.7875 MHz pour la paire analogique publique F1ZJV/F1ZYT ;
- HB9G : 145.125 et 431.500 MHz en complément des sorties déjà présentes.

## Exclusions fermées pour cette version

- F1ZTH **50.5375 MHz** : fréquence publique mais hors v0.3 tant qu'une baseline UV-K5/firmware commune ne garantit pas le 50 MHz ;
- liaison UHF ADRASEC F1ZJV/F1ZYT : fréquence non publique, donc non recherchée dans des données privées et non inférée ;
- omissions aviation antérieures : pas de remplissage par source secondaire non vérifiée.

Sources de vérité : `paired-rx-expansion.json`, `current-source-revalidation.json`, `release-scope.json`, `review-checklist.json`, `prepublication-reviewed-memory-map.json` et `publication-record.json`.
