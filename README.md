# RadioPack France

Codeplugs CHIRP régionaux, documentés et générés à partir de données publiques vérifiables pour les radios Quansheng UV-K5.

Le projet privilégie une approche prudente : aucune fréquence n'est ajoutée uniquement pour remplir un pack, les sources doivent être identifiables et les exports sont configurés pour l'écoute.

## État actuel — Sprint 29

Deux packs régionaux restent publiés et immuables :

- **Normandie v0.3.1** — 139 mémoires RX ;
- **Annecy–Alpes–Léman v0.2** — 65 mémoires RX, avec variante **48 mémoires sans aviation**.

La Bretagne reste en recherche uniquement :

- **Bretagne v0.1 — recherche** — aucune mémoire publique, aucun nombre cible artificiel, aucune publication autorisée.

Le Sprint 29 approfondit la couverture réellement utile autour de **Mortain-Bocage / Sud-Manche**, la **VHF maritime publique Bretagne**, les relais analogiques régionaux et désormais la politique commune d'écoute des liaisons nativement duplex/split.

Le générateur public `/generateur` continue de proposer uniquement Annecy–Alpes–Léman v0.2 et Normandie v0.3.1.

## Principes permanents

- Réception seule : `Duplex=off`.
- `Offset=0.000000`.
- Noms de mémoires limités à 10 caractères.
- Maximum 200 mémoires par pack.
- Pas de remplissage artificiel.
- Une source identifiée n'est pas automatiquement une fréquence validée.
- Une même fréquence RF ne doit pas être dupliquée uniquement pour changer son étiquette géographique, son site ou sa fonction.
- Une version régionale publiée est immuable ; toute évolution crée une nouvelle version et une nouvelle revue.
- Un rôle ADRASEC n'est jamais déduit uniquement de l'implantation géographique d'un relais.
- Une infrastructure radio actuelle vérifiée ne vaut pas automatiquement validation d'un canal ou d'une fréquence précise.
- Une preuve de couverture VHF dans un secteur ne permet pas d'identifier automatiquement le site émetteur.
- Les réseaux professionnels privés de sécurité/secours restent hors des packs lorsqu'ils ne sont pas explicitement destinés à l'écoute publique ou au service amateur ouvert.

## Politique paired RX — écouter les deux sens

La règle commune est définie dans :

```text
research/paired-rx-policy.json
```

Lorsqu'une liaison publique est **nativement duplex ou split** et que ses deux fréquences distinctes sont vérifiées, RadioPack prévoit **deux fréquences RX** afin de pouvoir écouter les deux sens :

- VHF maritime duplex : navire → côte et côte → navire ;
- relais radioamateur : entrée du relais et sortie du relais ;
- transpondeur cross-band : les deux côtés publiés ;
- satellite split : montée sol → satellite et descente satellite → sol.

Cela ne signifie pas que le poste réalise une réception audio full-duplex simultanée. Les deux fréquences sont programmées comme mémoires d'écoute distinctes. Sur chaque mémoire, le TX reste bloqué par le contrat CHIRP : `Duplex=off` et `Offset=0.000000`.

Si plusieurs services partagent exactement la même fréquence RF, une seule mémoire suffit ; les différents rôles restent en métadonnées. Les tonalités CTCSS d'activation ou de montée restent documentaires et ne servent jamais à réactiver l'émission.

Le plan concret pour les prochaines versions est :

```text
research/paired-rx-next-version-plan.json
```

La **Normandie v0.3.1** publiée applique déjà cette logique à la VHF marine avec des paires comme `M01-S` / `M01-C`. Elle reste figée. La **Normandie v0.4**, **Annecy–Alpes–Léman v0.3** et **Bretagne v0.1** appliquent désormais cette règle à toute nouvelle liaison publique duplex/split retenue.

## Politique secours / ADRASEC

La politique commune est définie dans :

```text
research/emergency-radio-policy.json
```

Peuvent être étudiés pour une future intégration RX : relais et transpondeurs radioamateurs ADRASEC/FNRASEC documentés, relais radioamateurs analogiques régionaux réellement utiles, canaux maritimes publics et autres diffusions de sécurité explicitement destinées aux usagers.

Pour les relais analogiques retenus dans une prochaine version, entrée et sortie vérifiées seront toutes deux disponibles à l'écoute conformément à la politique paired RX.

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

- `F5ZHY` — Montabot / Percy-en-Normandie — sortie **145.6875 MHz**, entrée **145.0875 MHz**, FM ;
- `F6ZCE` — Mont des Avaloirs — sortie **145.700 MHz**, entrée **145.100 MHz**, FM, CTCSS 123 Hz ;
- `F1ZBX` — Paimpont / Brocéliande — sortie **145.675 MHz**, entrée **145.075 MHz**, FM, CTCSS 71.9 Hz ;
- `F5ZHA` — Laval — transpondeur analogique conservé en étude de couverture ;
- `F5ZIX` Tessy-sur-Vire et `F5ZPO` Gorron — APRS 144.800 MHz conservés comme métadonnées de maillage, sans dupliquer la mémoire APRS nationale ;
- `F1ZKC` Orne — C4FM, conservé comme métadonnée uniquement ;
- `F5ZTQ` Izé — arrêté, exclu des candidats.

Dans Normandie v0.4, les relais analogiques finalement sélectionnés conserveront **entrée et sortie** comme mémoires RX distinctes lorsque les deux fréquences sont vérifiées. Aucune de ces nouvelles recherches n'est encore promue.

## Annecy–Alpes–Léman v0.3 — recherche secours et paired RX

La v0.2 publique reste figée. La recherche suivante reste dans :

```text
research/annecy-alpes-leman-v0.3/
```

Premiers candidats déjà enregistrés :

- `F1ZJV` — Pointe des Brasses — sortie 145.7875 MHz / entrée 145.1875 MHz, priorité ADRASEC 74 ;
- `F1ZYT` — Semnoz — même paire : pas de doublon uniquement pour distinguer le site ;
- `F1ZHG` — Fort du Mont — 145.2875 / 432.5125 MHz ;
- `F5ZGT` — Cime Caron — 145.450 / 432.5125 MHz, pertinence de couverture Annecy à confirmer.

La v0.3 devra également migrer les satellites split vers la double écoute RX après recontrôle opérationnel :

- SO-50 : montée **145.850 MHz**, descente **436.795 MHz** ;
- AO-91 : montée **435.250 MHz**, descente **145.960 MHz** ;
- AO-123 : montée **145.850 MHz**, descente **435.400 MHz**.

La montée 145.850 MHz commune à SO-50 et AO-123 restera une seule mémoire RF, avec les deux rôles en métadonnées. Les tonalités de montée sont documentées mais ne rendent jamais le TX possible.

## Bretagne v0.1 — zonage Nord / Sud

Le zonage reste obligatoire :

- **Bretagne Nord / Manche Ouest** — contexte CROSS Corsen ;
- **Bretagne Sud / Atlantique** — contexte CROSS Etel ;
- **interface Penmarc'h / Finistère Sud** — raccordement de responsabilité SAR vérifié, recouvrements radio détaillés encore à documenter.

Les sources actuelles permettent maintenant de borner les deux côtés de l'interface :

- CROSS Corsen : **Baie du Mont-Saint-Michel** jusqu'à la pointe de Penmarc'h ;
- CROSS Étel : **Pointe de Penmarc'h** jusqu'à la frontière espagnole.

Penmarc'h est donc un point de raccordement de responsabilité SAR primaire-vérifié des deux côtés. Cette frontière ne permet toutefois **pas** de déduire les zones de couverture VHF, les sites émetteurs ou les recouvrements radio.

Le canal 16 reste une fréquence commune : il ne sera pas dupliqué uniquement pour écrire « Corsen » et « Etel ».

## Bretagne — VHF maritime publique Sprint 29

Le fichier de recherche est :

```text
research/bretagne-v0.1/public-maritime-radio.json
```

Pour une voie maritime nativement duplex, le futur pack Bretagne conservera désormais **les deux côtés en réception** : la fréquence émise par le navire et la fréquence émise par la station côtière. Chaque mémoire restera `Duplex=off`, `Offset=0.000000`.

| Canal | Type | Navire → côte RX | Côte → navire RX | Contexte |
|---|---|---:|---:|---|
| 16 | simplex | 156.800 MHz | 156.800 MHz | appel, détresse, sécurité ; une seule mémoire |
| 79 | duplex | 156.975 MHz | 161.575 MHz | usage Corsen historiquement primaire-vérifié en 2003, émetteur actuel encore à identifier |
| 80 | duplex | 157.025 MHz | 161.625 MHz | CROSS Étel : Penmarc'h, Groix et Belle-Ile vérifiés pour les bulletins météo côtiers |
| 63 | duplex | 156.175 MHz | 160.775 MHz | CROSS Étel : station d'Étel vérifiée en diffusion météo continue |
| 64 | duplex | 156.225 MHz | 160.825 MHz | mention ministérielle actuelle 63/64 Morbihan ; émetteur Bretagne 64 encore à réconcilier |

Les futurs noms proposés suivent le modèle déjà utilisé par la Normandie : par exemple `M79-S` pour le côté navire et `M79-C` pour le côté côte.

Le planning officiel du CROSS Étel identifie quatre émetteurs météo bretons exploitables comme métadonnées territoriales : **Penmarc'h**, **Groix**, **Belle-Ile** sur le canal 80 et **Étel** sur le canal 63 en continu.

Le ministère mentionne toujours une diffusion permanente sur les canaux 63/64 notamment dans le Morbihan. La page et le planning primaires du CROSS Étel exploités identifient explicitement Étel sur le canal 63 et aucun émetteur Bretagne sur 64. RadioPack conserve donc le canal 64 en recherche sans inventer de site, tout en gardant sa paire de fréquences RX comme donnée réglementaire.

### CROSS Corsen : SRR, infrastructures et couverture du Raz

La zone de recherche et sauvetage actuelle du CROSS Corsen est désormais enregistrée de la **Baie du Mont-Saint-Michel à la pointe de Penmarc'h**, pour environ 50 000 km². La géométrie offshore détaillée et les recouvrements radio restent à établir.

Le réseau radio actuel est documenté à **10 stations VHF et 2 stations MF**. Deux infrastructures sont primaire-vérifiées :

- **Cap Fréhel** : équipements CROSS Corsen de suivi et de liaison avec les navires, sans canal explicitement publié ;
- **Stiff / Ouessant** : équipements de radiocommunications du CROSS actuels, sans canal explicitement publié.

Cette revalidation du Stiff ne permet pas d'attribuer automatiquement le canal 79 au site. `radio_service_or_channel` reste `null`.

Une opération officielle du **21 septembre 2025** confirme également que le CROSS Corsen a établi un contact VHF avec un navire au nord de la **Pointe du Raz**. Cela valide une couverture VHF opérationnelle actuelle du secteur, mais pas le site émetteur ni le canal. L'ancienne installation VHF/MF de la Pointe du Raz documentée en 2003 reste `current_validation: false`.

Le centre principal actuel du CROSS Corsen à la **Pointe de Corsen / Plouarzel** reste séparé de l'inventaire des stations déportées. Sa présence ne suffit pas à revalider l'installation radio locale de secours multicanal documentée en 2003.

Le projet **CROSS Nouvelle génération** prévoit un regroupement fonctionnel Étel/Corsen avec un horizon opérationnel 2027. Cette réorganisation future ne modifie ni les fréquences actuelles ni les exigences de validation site par site.

Le décret primaire de 2003 reste utile pour l'historique : Stiff en VHF, Pointe du Raz en VHF/MF, Corsen en secours multicanal et diffusion régulière d'informations/météo sur le canal 79 après appel sur le canal 16. Le canal 79 reste sans émetteur actuel primaire-vérifié.

## Bretagne — ADRASEC et relais analogiques

L'inventaire reste :

```text
research/bretagne-v0.1/emergency-relays.json
```

Il couvre les organisations ADRASEC 22 / 29 / 35 / 56 et plusieurs relais analogiques régionaux :

- `F5ZIS` — Matignon — 145.2375 / 432.6500 MHz ;
- `F5ZIT` — Perros-Guirec — 145.2250 / 432.6500 MHz ;
- `F1ZBX` — Brocéliande — entrée 145.0750 / sortie 145.6750 MHz ;
- `F1ZGS` — Plouhinec — 145.2625 / 431.4250 MHz ;
- `F5ZDV` — Morlaix — 145.2625 / 438.7000 MHz ;
- `F5ZZL` — Cast — 145.2625 / 431.3750 MHz ;
- `F1ZBZ` — Lorient — sortie 431.200 MHz avec plusieurs voies publiées, direction exacte encore à revoir ;
- `F5ZPE` — Bignan — entrée 145.1375 / sortie 145.7375 MHz ;
- `F1ZBH`, `F1ZGQ` et `F1ZAJ` — APRS 144.800 MHz conservés comme métadonnées sans doublon mémoire.

Le plan paired RX conserve les deux côtés des relais/transpondeurs dont la paire est suffisamment explicite. Les fréquences partagées 145.2625 et 432.6500 resteront dédupliquées dans le futur pack.

### ADRASEC 35 : F1ZUG

L'ARA35 documente deux fonctions distinctes sur le site `F1ZUG` de Châtillon-en-Vendelais :

- `F1ZUG-4` est un digipeater APRS sur **144.800 MHz** ;
- le site héberge également un **transpondeur pour le réseau ADRASEC 35**.

La fréquence de ce transpondeur ADRASEC n'est pas publiée dans la source consultée. RadioPack la conserve à `null` et interdit de la déduire de la fréquence APRS.

### Rennes : F5ZEB R71, F5ZPV RU19 et F5ZZH R7X

- `F5ZEB` / **R71** — Rennes Est — entrée **431.075 MHz**, sortie **438.675 MHz**, CTCSS 71.9 Hz ; paire conservée dans le plan RX, mais sélection finale encore soumise à la couverture/redondance.
- `F5ZPV` / **RU19** — Rennes-Beaulieu — entrée **430.475 MHz**, sortie **439.875 MHz**, FM/C4FM ; toujours temporairement arrêté, donc hors candidats actifs.
- `F5ZZH` / **R7X** — Rennes-Beaulieu / Cesson-Sévigné — entrée **145.1875 MHz**, sortie **145.7875 MHz**, FM ; toujours temporairement arrêté et à la recherche d'un nouveau site, donc hors candidats actifs.

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

Le moteur impose actuellement `Duplex=off` et `Offset=0.000000` à chaque ligne générée. La double écoute est donc obtenue par deux mémoires RX lorsque les fréquences d'une paire diffèrent, jamais par une configuration TX split.

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
python tests\test_paired_rx_policy.py
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

1. intégrer la politique paired RX dans les assembleurs des prochaines versions lorsque leurs plans mémoire seront ouverts ;
2. identifier par source primaire actuelle les autres sites du réseau de **10 stations VHF et 2 stations MF** du CROSS Corsen ;
3. identifier le ou les émetteurs actuels du **canal 79** sans les déduire de la couverture du Raz ;
4. revalider l'installation VHF/MF historique de la **Pointe du Raz** et l'installation radio locale historique de **Corsen** ;
5. réconcilier l'émetteur actuel du canal 64 dans le Morbihan ;
6. trouver une seconde source actuelle pour F6ZES Sourdeval ;
7. retrouver la fréquence du transpondeur ADRASEC 35 de F1ZUG sans la déduire de l'APRS ;
8. poursuivre les inventaires ADRASEC 22/29/56 et Sud-Manche ;
9. revoir couverture et redondance des relais/transpondeurs avant toute sélection mémoire ;
10. revalider les redémarrages éventuels de F5ZPV RU19 et F5ZZH R7X ;
11. recontrôler les satellites avant Annecy v0.3 ;
12. ne publier aucune nouvelle mémoire avant revue explicite de la prochaine version.

## Maintenance

Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint. La CI doit évoluer avec le contrat du sprint.

Les caches Python (`__pycache__/` et `*.py[cod]`) sont ignorés par Git.

Le détail historique reste dans [CHANGELOG.md](CHANGELOG.md).

## Sécurité et usage

Les exports RadioPack sont destinés à l'écoute. Voir [NOTICE_LEGAL.md](NOTICE_LEGAL.md) pour les précautions et limites d'utilisation.
