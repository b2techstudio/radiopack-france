# Sprint 86 — Annecy–Alpes–Léman v0.3 paired RX

État logique cible : **0.21.75**.

Le Sprint 86 transforme le plan de recherche Annecy–Alpes–Léman v0.3 en un premier candidat interne exact, sans modifier la v0.2 publique immuable.

## Résultat

- base publique v0.2 : **65 mémoires RX**, ou **48 sans aviation** ;
- candidat interne v0.3 : **76 mémoires RX**, ou **59 sans aviation** ;
- delta : **+11 fréquences RF uniques** ;
- plafond conditionnel : **77** si la compatibilité RX 50 MHz de la cible UV-K5/firmware du projet est définie et validée pour F1ZTH 50.5375 MHz ;
- aucun CSV public v0.3 ;
- aucun changement du registre public ;
- aucune fréquence ADRASEC non publiée n'est inférée.

## Ajouts paired RX

### Satellites

La v0.2 conserve son modèle historique où les montées restent en métadonnées. La v0.3 applique la politique paired RX et ajoute les montées comme mémoires d'écoute distinctes :

- `SAT-UP145` — **145.850 MHz**, montée partagée SO-50 / AO-123 ;
- `SAT-UP435` — **435.250 MHz**, montée AO-91.

La fréquence 145.850 MHz n'est ajoutée qu'une fois malgré ses deux rôles. Les descentes 436.795, 145.960 et 435.400 MHz restent celles déjà présentes en v0.2. Le statut opérationnel des satellites devra être recontrôlé avant toute publication v0.3.

### France — relais déjà sélectionnés

Les entrées suivantes deviennent de nouvelles mémoires RX parce que leur sortie correspondante est déjà sélectionnée dans la v0.2 :

- F1ZOH Crozet — **439.625 MHz** ;
- F6ZJD Nurieux — **145.0375 MHz** ;
- F1ZCQ Échirolles — **145.050 MHz** ;
- F1ZCR Chamrousse — **430.325 MHz** ;
- F1ZDC Échirolles — **431.425 MHz**.

F1ZPY et F1ZWY ne créent aucune nouvelle mémoire : leurs entrées respectives sont déjà représentées par la sortie de l'autre relais. Les transpondeurs F5ZDT, F1ZFX, F1ZIC, F1ZHE, F1ZHG, F5ZGT et F5ZLV sont également déjà couverts des deux côtés après déduplication RF.

### Haute-Savoie / ADRASEC public

Le couple F1ZJV Pointe des Brasses / F1ZYT Semnoz partage la paire VHF analogique publique :

- `74-R7X-IN` — **145.1875 MHz** ;
- `74-R7X-OUT` — **145.7875 MHz**.

Les deux sites partagent donc deux mémoires RF, et non quatre. La source locale mentionne une liaison/transpondeur UHF lié à l'ADRASEC, mais aucune fréquence publique n'est utilisée ni déduite : ce volet reste différé.

### Suisse — HB9G

Les deux relais HB9G déjà présents par leur sortie reçoivent maintenant leur entrée RX :

- `CH-HG-VIN` — **145.125 MHz** pour la sortie 145.725 MHz ;
- `CH-HG-UIN` — **431.500 MHz** pour la sortie 439.100 MHz.

## F1ZTH 50 MHz différé

Le REF publie actuellement **50.5375 MHz** comme troisième côté analogique du transpondeur F1ZTH, tandis que 431.275 et 145.2125 MHz sont déjà dans la v0.2. Cette RF représente donc un potentiel **+1**.

Elle n'est pas intégrée au Sprint 86 car RadioPack ne définit pas encore une base de compatibilité firmware/récepteur UV-K5 garantissant le stockage et la réception 50 MHz pour les utilisateurs. Le projet ne doit pas supposer qu'un firmware tiers est installé. Le plafond est donc 77, mais le candidat reste 76.

## Builder et garde-fous

Le builder `tools/build_annecy_v03_internal_candidate.py` repart du builder v0.2 validé, conserve toutes les lignes de base à l'identique puis ajoute uniquement les 11 RF approuvées dans `research/annecy-alpes-leman-v0.3/paired-rx-expansion.json`.

Il vérifie :

- déduplication des fréquences ;
- absence de collision de numéros mémoire et de noms ;
- noms CHIRP de 10 caractères maximum ;
- RX-only avec `Duplex=off`, `Offset=0.000000` ;
- exclusion explicite de 50.5375 MHz tant que le gate matériel/firmware reste ouvert ;
- candidat **76 / 59**, jamais public.

Garde-fou : `tests/test_sprint86_annecy_v03_paired_rx_expansion.py`.

## Clôture

Le HEAD nettoyé `287408c5c6a40b99d1e81650e3c5499475a7b565` a passé la CI complète au run **915** : tests dépôt, garde-fou Sprint 86, build Astro et statut combiné sont tous en succès. Aucun fichier temporaire de finalisation ne reste dans le dépôt.

Le présent commit de clôture porte le marqueur `[reference-archive]` et ne modifie que cette note de traçabilité. Il ne change ni le candidat 76/59, ni les fréquences, ni le registre, ni les packs publics. La CI de ce commit doit produire l'archive exacte du HEAD final.
