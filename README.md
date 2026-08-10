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
- Pour l'état courant d'un relais géré par une association locale, la page opérationnelle de l'exploitant est prioritaire sur un annuaire général lorsqu'ils divergent ; le conflit reste toutefois documenté.
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

La carte des fréquences uniques après déduplication est désormais séparée dans :

```text
research/paired-rx-deduplicated-memory-plan.json
```

Elle matérialise uniquement les paires déjà documentées et encore actives au niveau recherche : **12 fréquences uniques pour Normandie v0.4**, **10 pour Annecy–Alpes–Léman v0.3** et **29 pour Bretagne v0.1**. Ces nombres ne sont **pas** des tailles finales de packs ni des objectifs de remplissage. Les fréquences partagées sont fusionnées par région et les liaisons arrêtées ou non résolues restent hors de cette liste active.

La **Normandie v0.3.1** publiée applique déjà cette logique à la VHF marine avec des paires comme `M01-S` / `M01-C`. Elle reste figée. La **Normandie v0.4**, **Annecy–Alpes–Léman v0.3** et **Bretagne v0.1** appliquent désormais cette règle à toute nouvelle liaison publique duplex/split retenue.

## Politique secours / ADRASEC

La politique commune est définie dans :

```text
research/emergency-radio-policy.json
```

Peuvent être étudiés pour une future intégration RX : relais et transpondeurs radioamateurs ADRASEC/FNRASEC documentés, relais radioamateurs analogiques régionaux réellement utiles, canaux maritimes publics et autres diffusions de sécurité explicitement destinées aux usagers.

Pour les relais analogiques retenus dans une prochaine version, entrée et sortie vérifiées seront toutes deux disponibles à l'écoute conformément à la politique paired RX.

Pour les **statuts opérationnels**, RadioPack distingue désormais explicitement l'annuaire technique de la source exploitante : lorsqu'une association responsable publie qu'un relais est arrêté ou opérationnel et que le REF affiche l'inverse, l'état de l'exploitant local est retenu pour la recherche courante, le désaccord est conservé et aucune couverture n'est déduite de ce seul statut.

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

Le rafraîchissement paired RX courant est séparé dans :

```text
research/normandie-v0.4/paired-rx-refresh.json
```

Le périmètre vérifié couvre volontairement **50, 35, 53 et 61**, parce que la couverture radio utile autour de Mortain-Bocage ne suit pas les frontières départementales.

### Sourdeval F6ZES

Le répertoire courant confirme `F6ZES` à **Sourdeval**, responsable `F1SMB`, locator `IN98MR93XV`, altitude 230 m.

En revanche, aucune fréquence ni aucun mode exploitable ne sont actuellement fournis dans la fiche vérifiée. Un nouveau recontrôle ciblé le **10 août 2026** n'a pas fourni de seconde source publique actuelle suffisamment précise. RadioPack applique donc une règle stricte :

```text
sourdeval_must_not_be_guessed: true
```

`F6ZES` reste prioritaire mais **sans fréquence candidate** tant qu'une seconde source actuelle ne permet pas de la recouper.

### Relais documentés autour du secteur

- `F5ZHY` — Montabot / Percy-en-Normandie — sortie **145.6875 MHz**, entrée **145.0875 MHz**, FM ;
- `F6ZCE` — Mont des Avaloirs — sortie **145.700 MHz**, entrée **145.100 MHz**, FM, CTCSS 123 Hz ;
- `F1ZBX` — Paimpont / Brocéliande — sortie **145.675 MHz**, entrée **145.075 MHz**, FM, CTCSS 71.9 Hz ;
- `F5ZHA` — Laval — le REF actuel et `manuel.la-radio.eu` concordent sur **145.4675 / 432.5750 MHz**. RepeaterBook affiche toutefois encore **431.4125 MHz** sur une donnée ancienne : la paire REF est renforcée et reste dans la recherche paired RX, mais elle demeure **bloquée avant publication** tant qu'une source locale actuelle ne ferme pas définitivement le conflit ;
- `F1ZBL` — Équeurdreville-Hainneville — paire cross-band **145.2500 / 431.2500 MHz** confirmée à la fois par le REF et le Radio Club Nord Cotentin. La liste `manuel.la-radio.eu` concorde également ; la valeur secondaire `431.2250 MHz` vue dans RepeaterBook n'est donc pas retenue ;
- `F5ZIX` Tessy-sur-Vire et `F5ZPO` Gorron — APRS 144.800 MHz conservés comme métadonnées de maillage, sans dupliquer la mémoire APRS nationale ;
- `F1ZKC` Orne — C4FM, conservé comme métadonnée uniquement ;
- `F5ZTQ` Izé — arrêté, exclu des candidats.

Dans Normandie v0.4, les relais analogiques finalement sélectionnés conserveront **entrée et sortie** comme mémoires RX distinctes lorsque les deux fréquences sont vérifiées. La carte paired RX Normandie reste à **12 fréquences RF uniques de recherche** ; ce compte inclut F5ZHA comme paire de recherche, mais son conflit secondaire doit être réconcilié localement avant toute publication. F6ZES reste le principal blocage immédiat. Aucune de ces nouvelles recherches n'est encore promue.

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

Un inventaire technique séparé est désormais conservé dans :

```text
research/bretagne-v0.1/etel-network.json
```

Une offre officielle DIRM NAMO de juillet 2026 indique que le service technique du CROSS Étel assure la maintenance de **17 stations radio littorales de la Pointe de Penmarc'h à Biarritz**. Ce chiffre confirme que les quatre émetteurs météo bretons nommés ne constituent qu'un inventaire partiel du réseau. La page actuelle du CROSS Étel confirme aussi Chassiron et Étel sur le canal 63 en diffusion continue ; Chassiron reste une métadonnée hors Bretagne.

Le nombre de stations ne permet pas d'en déduire les noms ni les canaux. Le ministère mentionne toujours une diffusion permanente sur les canaux 63/64 notamment dans le Morbihan, mais les sources locales exploitées n'identifient explicitement aucun site Bretagne sur le canal 64. Les recherches ciblées du 10 août 2026 n'ont pas fermé cette attribution. RadioPack conserve donc le canal 64 en recherche sans inventer de site, tout en gardant sa paire de fréquences RX comme donnée réglementaire.

### CROSS Corsen : SRR, infrastructures et couverture du Raz

La zone de recherche et sauvetage actuelle du CROSS Corsen est désormais enregistrée de la **Baie du Mont-Saint-Michel à la pointe de Penmarc'h**, pour environ 50 000 km². La géométrie offshore détaillée et les recouvrements radio restent à établir.

Le réseau radio actuel est documenté à **10 stations VHF et 2 stations MF**. Deux infrastructures sont primaire-vérifiées :

- **Cap Fréhel** : équipements CROSS Corsen de suivi et de liaison avec les navires, sans canal explicitement publié ;
- **Stiff / Ouessant** : équipements de radiocommunications du CROSS actuels, sans canal explicitement publié.

Cette revalidation du Stiff ne permet pas d'attribuer automatiquement le canal 79 au site. `radio_service_or_channel` reste `null`.

Une opération officielle du **21 septembre 2025** confirme également que le CROSS Corsen a établi un contact VHF avec un navire au nord de la **Pointe du Raz**. Cela valide une couverture VHF opérationnelle actuelle du secteur, mais pas le site émetteur ni le canal. L'ancienne installation VHF/MF de la Pointe du Raz documentée en 2003 reste `current_validation: false`.

Le centre principal actuel du CROSS Corsen à la **Pointe de Corsen / Plouarzel** reste séparé de l'inventaire des stations déportées. Sa présence ne suffit pas à revalider l'installation radio locale de secours multicanal documentée en 2003.

Le projet **CROSS Nouvelle génération** prévoit un regroupement fonctionnel Étel/Corsen avec un horizon opérationnel 2027. Cette réorganisation future ne modifie ni les fréquences actuelles ni les exigences de validation site par site.

Le décret primaire de 2003 reste utile pour l'historique : Stiff en VHF, Pointe du Raz en VHF/MF, Corsen en secours multicanal et diffusion régulière d'informations/météo sur le canal 79 après appel sur le canal 16. Un nouveau recontrôle ciblé le 10 août 2026 n'a toujours pas identifié l'émetteur actuel du canal 79 ; aucune attribution au Stiff, à la Pointe du Raz ou à Corsen n'est déduite.

## Bretagne — ADRASEC et relais analogiques

L'inventaire principal reste :

```text
research/bretagne-v0.1/emergency-relays.json
```

L'extension REF actuelle est conservée séparément dans :

```text
research/bretagne-v0.1/ref-analog-expansion.json
```

La revue géométrie/redondance est conservée dans :

```text
research/bretagne-v0.1/analog-coverage-redundancy-review.json
```

Elle permet de compléter les candidats analogiques actuels sans confondre leurs métadonnées techniques avec une couverture mesurée.

### Côtes-d'Armor — cluster 432.650 MHz

Le répertoire REF actuel documente cinq transpondeurs analogiques actifs partageant le côté **432.650 MHz** :

- `F5ZIS` — Matignon — 145.2375 / 432.6500 MHz ;
- `F5ZIT` — Perros-Guirec — 145.2250 / 432.6500 MHz ;
- `F5ZIU` — La Harmoye — **145.4625 / 432.6500 MHz** ;
- `F5ZIV` — Saint-Brieuc — **145.4875 / 432.6500 MHz** ;
- `F5ZJR` — Plessala — **145.2875 / 432.6500 MHz**.

La fréquence 432.650 MHz reste donc **une seule mémoire RX** avec cinq rôles de site. Les centres des locators REF placent les deux extrêmes Matignon / Perros-Guirec à environ **90,6 km** l'un de l'autre : c'est un indicateur de diversité géographique, **pas une mesure de couverture radio**. Les altitudes, puissances et gains d'antenne publiés servent uniquement à prioriser la prochaine revue ; RadioPack n'en déduit aucune portée réelle.

Une cartographie radioamateur actuelle indépendante retrouve également les cinq sites séparément. Elle corrobore donc la **présence actuelle du groupe de cinq**, mais ne documente aucune liaison entre eux. Une ancienne fiche RepeaterBook de F5ZIT, revue en 2016, indiquait explicitement un lien avec F5ZIV, F5ZIU, F5ZIS et F5ZJR ; cette information reste un **indice historique secondaire**. Le REF actuel confirme les cinq sites actifs, le même responsable F6HRP, le même côté 432.650 MHz et le même CTCSS 71.9 Hz, mais aucune source actuelle exploitée ne publie explicitement leur interconnexion. RadioPack conserve donc `current_primary_linkage_verified: false` et `current_association_linkage_verified: false`.

Au niveau de la recherche mémoire, 432.650 MHz reçoit une priorité élevée d'**efficacité mémoire** : une seule fréquence RF représente cinq sites actifs, même si ces sites n'étaient finalement pas interconnectés. Les cinq côtés VHF restent en revanche distincts et sont tous conservés dans la carte paired RX.

### Finistère

- `F1ZGS` — Plouhinec — 145.2625 / 431.4250 MHz ;
- `F5ZDV` — Morlaix — 145.2625 / 438.7000 MHz ;
- `F5ZZL` — Cast — 145.2625 / 431.3750 MHz.

Le côté 145.2625 MHz reste une seule mémoire RF partagée entre ces trois transpondeurs.

### Morbihan — F1ZMU, F1ZBZ et F5ZPE

- `F1ZMU` — Saint-Nolff — relais FM actif, **sortie 430.3250 MHz / entrée 439.7250 MHz**, 50 W selon le REF ;
- `F5ZPE` — Bignan — entrée **145.1375 MHz** / sortie **145.7375 MHz** ;
- `F1ZBZ` — Lorient — cas multi-chemins désormais explicite dans le REF autour du côté commun **431.2000 MHz**.

Les centres de locators placent F1ZMU à environ **19 km** de F5ZPE. Cette proximité n'en fait pas un doublon : F1ZMU apporte une paire UHF entièrement distincte et reste un candidat de recherche prioritaire à vérifier sur le terrain ou par étude de propagation. Les autres services pouvant partager l'indicatif de base F1ZMU ne sont pas utilisés pour attribuer automatiquement un rôle au relais phonie.

Pour `F1ZBZ`, les lignes REF documentent notamment 431.200→/←145.6250, 145.0250→/←431.2000, 431.200→/←145.7375 et 145.1375→/←431.2000 selon les colonnes émission/réception du répertoire. RadioPack conserve donc cinq fréquences RX uniques pour ce transpondeur : **431.2000, 145.6250, 145.0250, 145.7375 et 145.1375 MHz**. Les deux dernières sont déjà présentes via F5ZPE et restent dédupliquées ; F1ZBZ ajoute donc **trois fréquences RF nouvelles** au plan après déduplication. Sa sélection reste conditionnée à une revue de couverture locale.

Les infrastructures APRS `F1ZBH`, `F1ZGQ` et `F1ZAJ` restent des métadonnées sans doublon 144.800 MHz.

### ADRASEC 35 : F1ZUG

L'ARA35 documente deux fonctions distinctes sur le site `F1ZUG` de Châtillon-en-Vendelais :

- `F1ZUG-4` est un digipeater APRS sur **144.800 MHz** ;
- le site héberge également un **transpondeur pour le réseau ADRASEC 35**.

La fréquence de ce transpondeur ADRASEC n'est pas publiée dans la source consultée. RadioPack la conserve à `null` et interdit de la déduire de la fréquence APRS.

### Rennes : F5ZEB R71, F5ZPV RU19 et F5ZZH R7X

Le recontrôle du 10 août 2026 met en évidence une divergence de statut entre le REF et les pages de l'**ARA35**, qui exploite ces équipements. RadioPack retient donc la source locale pour l'état opérationnel courant tout en conservant le désaccord :

- `F5ZEB` / **R71** — Rennes Est — entrée **431.075 MHz**, sortie **438.675 MHz**, CTCSS 71.9 Hz. L'ARA35 l'indique **opérationnel depuis le 25 septembre 2025** sur un site temporaire, alors que le REF l'affiche arrêté. Pour la recherche courante, R71 est donc considéré opérationnel, mais reste hors sélection publique tant que couverture/redondance ne sont pas validées ;
- `F5ZPV` / **RU19** — Rennes-Beaulieu — entrée **430.475 MHz**, sortie **439.875 MHz**, FM/C4FM. L'ARA35 l'indique **temporairement arrêté** sans confirmation actuelle de redémarrage, alors que le REF l'affiche actif : il reste donc hors candidats actifs ;
- `F5ZZH` / **R7X** — Rennes-Beaulieu / Cesson-Sévigné — entrée **145.1875 MHz**, sortie **145.7875 MHz**, FM. L'ARA35 indique un arrêt temporaire et la recherche d'un nouveau site ; le REF l'affiche également arrêté. Il reste hors candidats actifs.

Cette hiérarchie ne change aucune fréquence et ne transforme jamais un statut « opérationnel » en preuve de couverture. Les recherches ADRASEC 22, 29 et 56 restent ouvertes : un relais radioamateur ne reçoit jamais un rôle ADRASEC sur la seule base de sa localisation.

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
python tests\test_paired_rx_memory_plan.py
python tests\test_etel_network_research.py
python tests\test_bretagne_ref_analog_expansion.py
python tests\test_analog_coverage_redundancy_review.py
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

1. revalider par source associative actuelle l'interconnexion éventuelle du cluster Côtes-d'Armor **432.650 MHz** ; la présence des cinq sites est désormais recoupée indépendamment mais l'interconnexion reste non prouvée ;
2. trouver une source locale actuelle supplémentaire pour **F5ZHA Laval** afin de fermer définitivement le conflit 432.5750 / 431.4125, même si deux listes actuelles concordent déjà sur 432.5750 ;
3. suivre les statuts **F5ZEB R71 / F5ZPV RU19 / F5ZZH R7X** sur les pages ARA35 et ne réactiver RU19/R7X qu'après annonce explicite de redémarrage ;
4. vérifier la couverture utile de F1ZMU, F1ZBZ, F5ZHA et F5ZEB sans la déduire des seules puissances, altitudes ou états opérationnels ;
5. faire évoluer la carte RX dédupliquée au fil des validations, puis l'intégrer aux assembleurs des prochaines versions seulement lorsque leurs plans mémoire seront ouverts ;
6. identifier progressivement les **17 stations radio du CROSS Étel** et le site actuel du canal 64 sans déduction à partir du seul nombre de stations ;
7. identifier par source primaire actuelle les autres sites du réseau de **10 stations VHF et 2 stations MF** du CROSS Corsen ;
8. identifier le ou les émetteurs actuels du **canal 79** sans les déduire de la couverture du Raz ;
9. revalider l'installation VHF/MF historique de la **Pointe du Raz** et l'installation radio locale historique de **Corsen** ;
10. trouver une seconde source actuelle pour F6ZES Sourdeval ;
11. retrouver la fréquence du transpondeur ADRASEC 35 de F1ZUG sans la déduire de l'APRS ;
12. poursuivre les inventaires ADRASEC 22/29/56 et Sud-Manche ;
13. recontrôler les satellites avant Annecy v0.3 ;
14. ne publier aucune nouvelle mémoire avant revue explicite de la prochaine version.

## Maintenance

Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint. La CI doit évoluer avec le contrat du sprint.

Les caches Python (`__pycache__/` et `*.py[cod]`) sont ignorés par Git.

Le détail historique reste dans [CHANGELOG.md](CHANGELOG.md).

## Sécurité et usage

Les exports RadioPack sont destinés à l'écoute. Voir [NOTICE_LEGAL.md](NOTICE_LEGAL.md) pour les précautions et limites d'utilisation.