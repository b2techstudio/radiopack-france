# Sprint 75 — Bretagne v0.2 aviation AIRAC 08/26

Date : 12 août 2026
État logique visé : `0.21.64`

## Résultat

Le candidat interne Bretagne v0.2 passe de **135 à 151 mémoires RX**, soit **+16 mémoires aviation** aux positions 130 à 145. Bretagne v0.1 reste publique, immuable et inchangée à 135 mémoires.

Aucun CSV Bretagne v0.2 public n'est créé et le registre public reste sur v0.1.

## Méthode de validation aviation

Le SIA publie le produit courant **AIRAC 08/26 - CORRIGENDUM**, en vigueur du 6 août au 2 septembre 2026 inclus.

RadioPack France applique à la Bretagne la méthode déjà utilisée dans le projet pour Annecy–Alpes–Léman : contexte AIRAC courant vérifié + dernière page AIP primaire publique effective pour le service. Une page AIP dont la date d'effet précède le début du cycle peut donc être utilisée lorsqu'elle demeure la dernière page effective publique retrouvée pour ce service.

Le dépôt **ne prétend pas** avoir extrait les octets de l'export XML courant et ne prétend pas avoir vérifié chaque champ directement dans cet XML. Cette limite est enregistrée explicitement dans `research/bretagne-v0.2/aviation-airac-08.json`.

## Périmètre Sprint 75

Le périmètre reste celui déjà examiné avant la publication v0.1 :

- Rennes Saint-Jacques (LFRN) : 7 fréquences uniques ;
- Brest Bretagne (LFRB) : 5 fréquences uniques ;
- Dinard Pleurtuit Saint-Malo (LFRD) : 2 fréquences uniques ;
- Quimper Pluguffan (LFRQ) : 1 fréquence unique ;
- aviation urgence 121.500 MHz : 1 mémoire générique.

Total : **16 mémoires**, toutes en AM, pas 8.33 kHz, réception seule. Les doublons de service partageant la même fréquence sont fusionnés en une seule mémoire RF.

Les positions 146 à 149 restent libres : aucun remplissage artificiel.

## Artefacts

```text
research/bretagne-v0.2/aviation-airac-08.json
research/bretagne-v0.2/candidate-memory-delta.json
tools/build_bretagne_v02_internal_candidate.py
tests/test_sprint75_bretagne_aviation.py
```

`research/bretagne-v0.2/pack-plan.json` est avancé à 151 mémoires et le backlog aviation est marqué comme validé **pour le candidat interne uniquement**. Les autres dossiers ADRASEC, CROSS et infrastructures radioamateur restent ouverts.

## Garde-fous

- Bretagne v0.1 reste immuable à 135 mémoires ;
- aucune mémoire v0.2 n'est publiée ;
- toutes les mémoires restent RX-only avec `Duplex=off` et `Offset=0.000000` ;
- noms CHIRP limités à 10 caractères ;
- fréquences, noms et positions mémoire uniques ;
- aucune donnée secondaire seule n'est promotable ;
- aucune correspondance XML courante n'est revendiquée sans extraction réelle ;
- la frontière de validité AIRAC 08/26 reste obligatoire avant toute revue publique ;
- les aérodromes supplémentaires et fréquences militaires spécifiques restent hors périmètre de ce sprint.
