# RadioPack France

Codeplugs CHIRP régionaux, documentés et générés à partir de données publiques vérifiables pour les radios Quansheng UV-K5.

Le projet privilégie une approche prudente : aucune fréquence n'est ajoutée uniquement pour remplir un pack, les sources doivent être identifiables et les exports publics sont configurés en réception seule.

## État actuel — Sprint 28

Deux packs régionaux restent publiés et immuables :

- **Normandie v0.3.1** — 139 mémoires RX ;
- **Annecy–Alpes–Léman v0.2** — 65 mémoires RX, avec variante **48 mémoires sans aviation**.

La Bretagne reste en recherche uniquement :

- **Bretagne v0.1 — recherche** — 0 fréquence promue, aucun nombre cible artificiel, aucune publication autorisée.

Le Sprint 28 étend la recherche aux **relais radioamateurs de secours / ADRASEC**, aux relais régionaux utiles et aux infrastructures côtières publiques. Les versions déjà publiées ne sont pas modifiées : les évolutions passent par **Normandie v0.4** et **Annecy–Alpes–Léman v0.3** en recherche.

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
- Les réseaux professionnels privés de sécurité/secours ne sont pas transformés en canaux d'écoute simplement parce qu'ils existent.

## Politique secours / ADRASEC — Sprint 28

La politique commune est définie dans :

```text
research/emergency-radio-policy.json
```

Peuvent être étudiés pour une future intégration RX :

- relais et transpondeurs radioamateurs ADRASEC/FNRASEC publiquement documentés ;
- relais radioamateurs analogiques régionaux réellement utiles à la couverture locale ;
- canaux maritimes et diffusions météo/sécurité explicitement publics ;
- autres diffusions de sécurité officiellement destinées à la réception des usagers.

Restent hors publication par défaut :

- canaux opérationnels internes PPDR/PMR de police, gendarmerie, SDIS, SAMU ou autres réseaux professionnels ;
- canaux privés de Protection Civile, Croix-Rouge ou associations de secours lorsqu'ils ne sont pas explicitement destinés à l'écoute publique ou au service amateur ouvert ;
- relais uniquement numériques incompatibles avec le profil RX analogique cible.

L'ANFR distingue les réseaux radioamateurs des réseaux professionnels PMR/PPDR. RadioPack ne doit donc pas mélanger un relais amateur ADRASEC public avec un canal professionnel opérationnel privé.

## Normandie v0.4 — recherche Mortain-Bocage / Sud-Manche

La v0.3.1 publique reste figée. La prochaine évolution est préparée dans :

```text
research/normandie-v0.4/
```

Le périmètre prioritaire est **Mortain-Bocage / Sud-Manche**. La couverture utile ne s'arrête pas à la frontière du département 50 : la recherche regarde aussi les départements voisins **35, 53 et 61**.

Premiers candidats enregistrés :

- `F5ZHY` — Montabot / Percy-en-Normandie — **145.6875 MHz FM** ;
- `F6ZES` — Sourdeval — indicatif et site identifiés, fréquence actuelle encore à confirmer ;
- `F6ZCE` — Mont des Avaloirs / département 53 — **145.700 MHz FM** ;
- `F1ZBX` — Brocéliande / Paimpont / département 35 — **145.675 MHz FM**, couverture depuis Mortain à vérifier ;
- `F1ZBL` — transpondeur Cherbourg, intérêt surtout Nord-Manche ;
- `F1ZOV` — Equeurdreville, relais analogique Nord-Manche ;
- `F5ZTE` — Percy-en-Normandie, réseau numérique conservé en métadonnée mais non retenu par défaut pour l'écoute analogique.

L'**ADRASEC 14-50** est enregistrée comme organisation actuelle membre de la FNRASEC. Cette appartenance ne suffit jamais à déduire une fréquence : chaque relais doit être validé séparément.

## Annecy–Alpes–Léman v0.3 — recherche secours

La v0.2 publique reste figée. La prochaine recherche est dans :

```text
research/annecy-alpes-leman-v0.3/
```

Premiers candidats :

- `F1ZJV` — Pointe des Brasses — **145.7875 MHz FM**, relais ADRASEC 74 ;
- `F1ZYT` — Semnoz — même sortie 145.7875 MHz : pas de doublon mémoire uniquement pour distinguer le site ;
- `F1ZHG` — Fort du Mont — **145.2875 MHz**, transpondeur ADRASEC 73 ;
- `F5ZGT` — Cime Caron — **145.450 MHz**, pertinence de couverture Annecy à confirmer.

Le rôle des relais ADRASEC 73/38/01 sera étudié uniquement s'ils apportent une couverture réellement pertinente au bassin Annecy–Alpes–Léman.

## Bretagne v0.1 — recherche Nord / Sud + ADRASEC

Le zonage du Sprint 27 reste obligatoire :

- **Bretagne Nord / Manche Ouest** — contexte CROSS Corsen ;
- **Bretagne Sud / Atlantique** — contexte CROSS Etel ;
- **transition Finistère Sud** — limite opérationnelle exacte encore à confirmer.

Le canal 16 reste une fréquence commune : il ne sera pas dupliqué uniquement pour écrire « Corsen » et « Etel ». Le CROSS responsable, les stations VHF déportées et les zones de couverture restent des métadonnées territoriales.

Le nouvel inventaire :

```text
research/bretagne-v0.1/emergency-relays.json
```

ouvre maintenant la recherche sur **ADRASEC 22 / 29 / 35 / 56** et les relais régionaux associés.

Premiers éléments :

- `F1ZUG-4` — APRS **144.800 MHz**, site ARA35 avec rôle documenté dans le réseau ADRASEC 35 ;
- `F5ZZC-4` — digipeater APRS ADRASEC 35, fréquence actuelle à revalider avant toute promotion ;
- `F1ZBX` — Brocéliande — **145.675 MHz FM** ;
- `F1ZBH` et `F1ZGQ` — APRS Finistère **144.800 MHz**, conservés comme métadonnées de maillage et non comme doublons du canal APRS national.

Une porte de publication `emergency_relay_inventory` bloque Bretagne tant que les infrastructures ADRASEC 22/29/35/56 et les relais régionaux pertinents ne sont pas correctement inventoriés et zonés.

## Packs publics actuels

### Annecy–Alpes–Léman v0.2

Téléchargements :

```text
/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv
/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2-sans-aviation.csv
```

### Normandie v0.3.1

Téléchargement :

```text
/downloads/normandie/radiopack-france-normandie-v0.3.1.csv
```

Le catalogue public reste donc :

```text
Annecy 65 / 48 + Normandie 139
```

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

Bretagne v0.1, Normandie v0.4 et Annecy–Alpes–Léman v0.3 restent volontairement hors de ce registre.

Voir aussi :

- [REGIONAL-PACK-WORKFLOW.md](REGIONAL-PACK-WORKFLOW.md)
- [SPRINT-27-BRETAGNE-MARITIME-ZONING.md](SPRINT-27-BRETAGNE-MARITIME-ZONING.md)
- [SPRINT-28-EMERGENCY-ADRASEC-RESEARCH.md](SPRINT-28-EMERGENCY-ADRASEC-RESEARCH.md)

## Tests principaux

```powershell
python tests\test_generator.py
python tests\test_site_files.py
python tests\test_pack_registry.py
python tests\test_regional_pack_starter.py
python tests\test_bretagne_research_scaffold.py
python tests\test_emergency_relay_research.py
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

## Maintenance

Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint. La CI doit évoluer avec le contrat du sprint.

Les caches Python (`__pycache__/` et `*.py[cod]`) sont ignorés par Git.

Le détail historique reste dans [CHANGELOG.md](CHANGELOG.md).

## Sécurité et usage

Les exports RadioPack sont destinés à l'écoute. Voir [NOTICE_LEGAL.md](NOTICE_LEGAL.md) pour les précautions et limites d'utilisation.
