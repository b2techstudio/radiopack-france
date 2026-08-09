# RadioPack France

Codeplugs CHIRP régionaux, documentés et générés à partir de données publiques vérifiables pour les radios Quansheng UV-K5.

Le projet privilégie une approche prudente : aucune fréquence n'est ajoutée uniquement pour remplir un pack, les sources doivent être identifiables et les exports publics sont configurés en réception seule.

## État actuel — Sprint 29

Deux packs régionaux restent publiés et immuables :

- **Normandie v0.3.1** — 139 mémoires RX ;
- **Annecy–Alpes–Léman v0.2** — 65 mémoires RX, avec variante **48 mémoires sans aviation**.

La Bretagne reste en recherche uniquement :

- **Bretagne v0.1 — recherche** — aucune mémoire publique, aucun nombre cible artificiel, aucune publication autorisée.

Le Sprint 29 approfondit deux axes :

- la couverture réellement utile autour de **Mortain-Bocage / Sud-Manche**, au-delà des frontières administratives 50/35/53/61 ;
- la **VHF maritime publique Bretagne** et les relais analogiques régionaux, toujours avec le découpage Bretagne Nord / CROSS Corsen et Bretagne Sud / CROSS Etel.

Le générateur public `/generateur` continue de proposer uniquement Annecy–Alpes–Léman v0.2 et Normandie v0.3.1.

## Principes permanents

- Réception seule : `Duplex=off`.
- `Offset=0.000000`.
- Noms de mémoires limités à 10 caractères.
- Maximum 200 mémoires par pack.
- Pas de remplissage artificiel.
- Une source identifiée n'est pas automatiquement une fréquence validée.
- Une même fréquence ne doit pas être dupliquée uniquement pour changer son étiquette géographique ou son nom de site.
- Une version régionale publiée est immuable ; toute évolution crée une nouvelle version et une nouvelle revue.
- Un rôle ADRASEC n'est jamais déduit uniquement de l'implantation géographique d'un relais.
- Les réseaux professionnels privés de sécurité/secours ne sont pas transformés en canaux d'écoute simplement parce qu'ils existent.

## Politique secours / ADRASEC

La politique commune est définie dans :

```text
research/emergency-radio-policy.json
```

Peuvent être étudiés pour une future intégration RX : relais et transpondeurs radioamateurs ADRASEC/FNRASEC documentés, relais radioamateurs analogiques régionaux réellement utiles, canaux maritimes publics et autres diffusions de sécurité explicitement destinées aux usagers.

Restent hors publication par défaut les canaux opérationnels internes PPDR/PMR de police, gendarmerie, SDIS, SAMU, Protection Civile, Croix-Rouge ou autres réseaux professionnels privés lorsqu'ils ne sont pas explicitement destinés à l'écoute publique ou au service amateur ouvert.

## Normandie v0.4 — recherche Mortain-Bocage / Sud-Manche

La v0.3.1 publique reste figée. La prochaine évolution est préparée dans :

```text
research/normandie-v0.4/
```

Le fichier de couverture Sprint 29 est :

```text
research/normandie-v0.4/mortain-bocage-coverage.json
```

Le périmètre vérifié couvre volontairement **50, 35, 53 et 61**, parce que la couverture radio utile autour de Mortain-Bocage ne suit pas les frontières départementales.

### Sourdeval F6ZES

Le répertoire courant confirme `F6ZES` à **Sourdeval**, responsable `F1SMB`, locator `IN98MR93XV`, altitude 230 m.

En revanche, aucune fréquence ni aucun mode exploitable ne sont actuellement fournis dans la fiche vérifiée. RadioPack applique donc une règle stricte :

```text
sourdeval_must_not_be_guessed: true
```

`F6ZES` reste prioritaire mais **sans fréquence candidate** tant qu'une seconde source actuelle ne permet pas de la recouper.

### Relais documentés autour du secteur

- `F5ZHY` — Montabot / Percy-en-Normandie — sortie **145.6875 MHz**, entrée 145.0875 MHz, FM ;
- `F6ZCE` — Mont des Avaloirs — sortie **145.700 MHz**, entrée 145.100 MHz, FM, CTCSS 123 Hz ;
- `F1ZBX` — Paimpont / Brocéliande — sortie **145.675 MHz**, entrée 145.075 MHz, FM, CTCSS 71.9 Hz ;
- `F5ZHA` — Laval — transpondeur analogique conservé en étude de couverture ;
- `F5ZIX` Tessy-sur-Vire et `F5ZPO` Gorron — APRS 144.800 MHz conservés comme métadonnées de maillage, sans dupliquer la mémoire APRS nationale ;
- `F1ZKC` Orne — C4FM, conservé comme métadonnée uniquement ;
- `F5ZTQ` Izé — arrêté, exclu des candidats.

Aucune de ces nouvelles recherches n'est encore promue dans Normandie v0.4.

## Annecy–Alpes–Léman v0.3 — recherche secours

La v0.2 publique reste figée. La recherche suivante reste dans :

```text
research/annecy-alpes-leman-v0.3/
```

Premiers candidats déjà enregistrés :

- `F1ZJV` — Pointe des Brasses — 145.7875 MHz FM, priorité ADRASEC 74 ;
- `F1ZYT` — Semnoz — même sortie 145.7875 MHz : pas de doublon mémoire uniquement pour distinguer le site ;
- `F1ZHG` — Fort du Mont — 145.2875 MHz ;
- `F5ZGT` — Cime Caron — 145.450 MHz, pertinence de couverture Annecy à confirmer.

## Bretagne v0.1 — zonage Nord / Sud

Le zonage reste obligatoire :

- **Bretagne Nord / Manche Ouest** — contexte CROSS Corsen ;
- **Bretagne Sud / Atlantique** — contexte CROSS Etel ;
- **interface Penmarc'h / Finistère Sud** — début de compétence du CROSS Étel vérifié, recouvrements radio détaillés encore à documenter.

La DIRM NAMO indique explicitement que le **CROSS Étel est compétent à partir de la Pointe de Penmarc'h (Finistère) jusqu'à la frontière espagnole**. Ce point d'interface n'est donc plus laissé à une simple déduction opérationnelle. En revanche, l'inventaire détaillé des stations VHF de CROSS Corsen et les éventuels recouvrements radio autour de Penmarc'h restent bloquants pour une publication.

Le canal 16 reste une fréquence commune : il ne sera pas dupliqué uniquement pour écrire « Corsen » et « Etel ».

## Bretagne — VHF maritime publique Sprint 29

Le fichier de recherche est :

```text
research/bretagne-v0.1/public-maritime-radio.json
```

Pour une voie maritime duplex, le pack RX doit mémoriser la **fréquence émise par la station côtière et reçue par le navire**, pas la fréquence d'émission du navire.

| Canal | Type | Fréquence RX étudiée | Contexte |
|---|---|---:|---|
| 16 | simplex | 156.800 MHz | appel, détresse, sécurité |
| 79 | duplex | 161.575 MHz | CROSS / météo annoncée sur 16 ; usage Corsen historiquement primaire-vérifié en 2003 mais émetteur actuel à revalider |
| 80 | duplex | 161.625 MHz | CROSS Étel : Penmarc'h, Groix et Belle-Ile vérifiés pour les bulletins météo côtiers |
| 63 | duplex | 160.775 MHz | CROSS Étel : station d'Étel vérifiée en diffusion météo continue |
| 64 | duplex | 160.825 MHz | mention ministérielle actuelle 63/64 Morbihan recontrôlée ; émetteur Bretagne 64 toujours non identifié dans la source locale Étel |

Le planning officiel du CROSS Étel identifie quatre émetteurs météo bretons exploitables comme métadonnées territoriales : **Penmarc'h**, **Groix**, **Belle-Ile** sur le canal 80 et **Étel** sur le canal 63 en continu.

Le ministère mentionne toujours une diffusion permanente sur les canaux 63/64 notamment dans le Morbihan. Cette mention a été recontrôlée en 2026, mais la page et le planning primaires du CROSS Étel exploités identifient explicitement Étel sur le canal 63 et aucun émetteur Bretagne sur 64. RadioPack conserve donc le canal 64 en recherche sans inventer de site.

### CROSS Corsen : réseau actuel dimensionné, sites actuels encore à inventorier

La page actuelle du CROSS Corsen confirme un réseau radio VHF/MF veillé en permanence et des stations littorales utilisées pour les diffusions météorologiques. Une communication officielle récente de la DGAMPA précise désormais sa taille : **10 stations radio VHF et 2 stations MF**. Les noms et canaux de ces stations ne sont toutefois pas fournis dans la source exploitée.

Une source primaire DIRM NAMO confirme par ailleurs que le **phare du Cap Fréhel** héberge des équipements du CROSS Corsen de **suivi et de liaison avec les navires** pour la surveillance du trafic et la coordination des secours. RadioPack enregistre donc Cap Fréhel comme infrastructure radio Corsen actuelle vérifiée, mais ne le classe pas automatiquement comme station VHF météo et ne lui attribue aucun canal.

Un décret primaire de **2003** fournit une piste historique beaucoup plus détaillée : il documente alors des équipements radio au **Stiff / Ouessant**, à la **Pointe du Raz** et sur le site de **Corsen**, ainsi qu'une diffusion régulière d'informations et de météo sur le **canal 79** après appel sur le canal 16. Ces éléments sont conservés comme **architecture historique à revalider**, et non comme inventaire 2026. Ils ne deviennent ni sites actuels ni mémoires publiques tant qu'une source actuelle ne les recoupe.

Ces fréquences, émetteurs, infrastructures et pistes historiques sont documentés dans la recherche mais **pas encore promus dans Bretagne v0.1**.

## Bretagne — ADRASEC et relais analogiques

L'inventaire reste :

```text
research/bretagne-v0.1/emergency-relays.json
```

Il couvre les organisations ADRASEC 22 / 29 / 35 / 56 et plusieurs relais analogiques régionaux :

- `F5ZIS` — Matignon — 145.2375 MHz, transpondeur vers 432.6500 MHz, CTCSS 71.9 Hz ;
- `F5ZIT` — Perros-Guirec — 145.2250 MHz, transpondeur vers 432.6500 MHz, CTCSS 71.9 Hz ;
- `F1ZBX` — Brocéliande — 145.675 MHz ;
- `F1ZGS` — Plouhinec — sortie **431.425 MHz**, entrée 145.2625 MHz, CTCSS 71.9 Hz ;
- `F5ZDV` — Morlaix — sortie **438.700 MHz**, entrée 145.2625 MHz, CTCSS 71.9 Hz ;
- `F5ZZL` — Cast — sortie **431.375 MHz**, entrée 145.2625 MHz, CTCSS 71.9 Hz ;
- `F1ZBZ` — Lorient — sortie 431.200 MHz avec plusieurs entrées publiées, direction exacte à revoir avant sélection RX ;
- `F5ZPE` — Bignan — sortie 145.7375 MHz, entrée 145.1375 MHz, CTCSS 71.9 Hz ;
- `F1ZBH`, `F1ZGQ` et `F1ZAJ` — infrastructures APRS 144.800 MHz conservées comme métadonnées et non comme mémoires dupliquées.

Les nouveaux transpondeurs Finistère `F1ZGS`, `F5ZDV` et `F5ZZL` sont des candidats analogiques de recherche, pas encore des mémoires retenues. Leur couverture et leur redondance doivent être étudiées avant toute sélection.

### ADRASEC 35 : F1ZUG mieux qualifié

L'ARA35 documente deux fonctions distinctes sur le site `F1ZUG` de Châtillon-en-Vendelais :

- `F1ZUG-4` est un digipeater APRS sur **144.800 MHz** ;
- une publication d'entretien du site datée de juin 2024 indique également un **transpondeur pour le réseau ADRASEC 35**.

La fréquence de ce transpondeur ADRASEC n'est pas publiée dans la source consultée. RadioPack la conserve donc à `null` et interdit explicitement de la déduire de la fréquence APRS 144.800 MHz.

### Rennes : F5ZEB R71 et F5ZPV RU19

- `F5ZEB` / **R71** — Rennes Est — de nouveau opérationnel depuis le 25 septembre 2025 selon l'ARA35 ; entrée **431.075 MHz**, sortie **438.675 MHz**, CTCSS 71.9 Hz, liaison vers le R3 `F1ZBX` de Brocéliande. Il reste `rx_pack_candidate: false` tant que couverture et redondance ne sont pas revues ; aucun rôle ADRASEC ne lui est attribué.
- `F5ZPV` / **RU19** — Rennes-Beaulieu — sortie **439.875 MHz**, entrée **430.475 MHz**, CTCSS 71.9 Hz, FM/C4FM. La page ARA35 actuelle le donne encore comme temporairement arrêté ; il reste donc hors candidats actifs jusqu'à confirmation d'un redémarrage effectif.

Les recherches ADRASEC 22, 29 et 56 restent ouvertes : un relais radioamateur ne reçoit jamais un rôle ADRASEC sur la seule base de sa localisation.

## Packs publics actuels

Téléchargements Annecy :

```text
/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv
/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2-sans-aviation.csv
```

Téléchargement Normandie :

```text
/downloads/normandie/radiopack-france-normandie-v0.3.1.csv
```

Le catalogue public reste :

```text
Annecy 65 / 48 + Normandie 139
```

Bretagne v0.1, Normandie v0.4 et Annecy–Alpes–Léman v0.3 restent volontairement hors de `website/src/lib/packRegistry.ts`.

## Architecture

Moteur CHIRP générique :

```text
website/src/lib/chirpPack.ts
```

Configuration Annecy publique :

```text
website/src/lib/annecyPack.ts
```

Registre des packs effectivement téléchargeables :

```text
website/src/lib/packRegistry.ts
```

Voir aussi :

- [REGIONAL-PACK-WORKFLOW.md](REGIONAL-PACK-WORKFLOW.md)
- [SPRINT-27-BRETAGNE-MARITIME-ZONING.md](SPRINT-27-BRETAGNE-MARITIME-ZONING.md)
- [SPRINT-28-EMERGENCY-ADRASEC-RESEARCH.md](SPRINT-28-EMERGENCY-ADRASEC-RESEARCH.md)
- [SPRINT-29-MORTAIN-BRETAGNE-RADIO-RESEARCH.md](SPRINT-29-MORTAIN-BRETAGNE-RADIO-RESEARCH.md)

## Tests principaux

```powershell
python tests\test_generator.py
python tests\test_site_files.py
python tests\test_pack_registry.py
python tests\test_regional_pack_starter.py
python tests\test_bretagne_research_scaffold.py
python tests\test_emergency_relay_research.py
python tests\test_mortain_bretagne_radio_research.py
python tests\test_web_generator.py
python tests\test_annecy_research.py
python tests\test_annecy_aviation_lakes.py
python tests\test_annecy_airac08.py
python tests\test_annecy_internal_candidate.py
python tests\test_annecy_release_readiness.py
python tests\test_annecy_prepublication.py
python tests\test_annecy_prepublication_review.py
```

Après les tests locaux :

```powershell
git status
```

Résultat attendu :

```text
nothing to commit, working tree clean
```

Après un build Astro :

```powershell
cd website
npm run build
cd ..
python tests\test_built_annecy_public_csv.py
python tests\test_built_public_pack_catalog.py
```

## Synchroniser le dépôt local

```powershell
cd "C:\Users\cross\Documents\CODE\PROJETS\RadioPack-France"
git pull --ff-only
git status
```

Les archives de sprint sont des sauvegardes de référence uniquement : ne pas les décompresser dans le dépôt local lorsque GitHub contient déjà les changements.

## Prochaines priorités

1. identifier par source primaire actuelle les noms des **10 stations VHF et 2 stations MF** du réseau CROSS Corsen ;
2. revalider en source actuelle les pistes historiques **Stiff / Ouessant, Pointe du Raz et Corsen**, ainsi que l'usage actuel du canal 79 ;
3. réconcilier l'émetteur actuel du canal 64 dans le Morbihan ;
4. trouver une seconde source actuelle pour F6ZES Sourdeval ;
5. retrouver la fréquence du transpondeur ADRASEC 35 de F1ZUG sans la déduire de l'APRS ;
6. poursuivre les inventaires ADRASEC 22/29/56 et Sud-Manche ;
7. revoir couverture et redondance de F1ZGS, F5ZDV, F5ZZL et F5ZEB avant toute sélection mémoire ;
8. revalider le redémarrage éventuel de F5ZPV RU19 ;
9. ne publier aucune nouvelle mémoire avant revue explicite de la prochaine version.

## Maintenance

Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint. La CI doit évoluer avec le contrat du sprint.

Les caches Python (`__pycache__/` et `*.py[cod]`) sont ignorés par Git.

Le détail historique reste dans [CHANGELOG.md](CHANGELOG.md).

## Sécurité et usage

Les exports RadioPack sont destinés à l'écoute. Voir [NOTICE_LEGAL.md](NOTICE_LEGAL.md) pour les précautions et limites d'utilisation.
