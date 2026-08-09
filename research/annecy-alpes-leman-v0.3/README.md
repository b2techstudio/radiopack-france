# Annecy–Alpes–Léman v0.3 — recherche

Cette branche prépare une future évolution du pack Annecy–Alpes–Léman sans modifier la version publiée **v0.2**, qui reste figée à 65 mémoires / 48 sans aviation.

## Politique paired RX

Annecy–Alpes–Léman v0.3 applique :

```text
research/paired-rx-policy.json
```

Toute liaison publique nativement duplex/split retenue devra permettre l'écoute de ses **deux fréquences vérifiées**. Les deux côtés seront des mémoires RX distinctes avec `Duplex=off` et `Offset=0.000000` ; aucune montée ne sera configurée comme fréquence TX.

Cela concerne les relais analogiques, les transpondeurs cross-band et les satellites split. Les fréquences RF identiques partagées par plusieurs fonctions restent dédupliquées.

## Satellites — changement par rapport à v0.2

La v0.2 publiée reste immuable et conserve son modèle historique « descente en mémoire, montée en métadonnée ».

Pour la **v0.3**, après recontrôle du statut opérationnel des satellites avant publication, le plan paired RX prévoit :

- `SO-50` — montée **145.850 MHz**, descente **436.795 MHz** ;
- `AO-91` — montée **435.250 MHz**, descente **145.960 MHz** ;
- `AO-123` — montée **145.850 MHz**, descente **435.400 MHz**.

SO-50 et AO-123 partageant 145.850 MHz en montée, cette fréquence restera une seule mémoire RX avec les deux rôles en métadonnées. Les CTCSS d'activation/montée restent documentaires et ne réactivent jamais le TX.

## Objectif du chantier secours / ADRASEC

Le chantier réexamine les relais et transpondeurs radioamateurs utilisés ou prioritaires pour les ADRASEC dans les départements 74, 73, 38 et 01.

Premiers cas :

- `F1ZJV` — Pointe des Brasses — entrée **145.1875 MHz**, sortie **145.7875 MHz**, relais VHF analogique ADRASEC 74 ;
- `F1ZYT` — Semnoz — même paire 145.1875 / 145.7875 MHz que F1ZJV ; une seule paire RF sera nécessaire pour les deux sites ;
- `F1ZHG` — Fort du Mont — paire **145.2875 / 432.5125 MHz**, transpondeur ADRASEC 73 ;
- `F5ZGT` — Cime Caron — paire **145.450 / 432.5125 MHz**, couverture Annecy–Léman encore à vérifier ;
- autres relais ADRASEC 73/38/01 uniquement si leur couverture est réellement pertinente pour le bassin Annecy–Léman.

Une même fréquence RF ne sera pas dupliquée uniquement pour représenter deux sites ou fonctions différents. Les sites et rôles ADRASEC restent en métadonnées lorsque nécessaire.

Le plan de travail détaillé est centralisé dans :

```text
research/paired-rx-next-version-plan.json
```

Les réseaux professionnels privés de secours restent exclus. Aucune mémoire v0.3 n'est encore publiée : la sélection finale, la déduplication, les statuts opérationnels et la revue du futur CSV restent obligatoires.
