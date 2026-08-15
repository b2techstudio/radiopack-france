# Annecy–Alpes–Léman v0.3 — recherche

État : **Sprint 86 / 0.21.75 — premier candidat interne à 76 mémoires RX, 59 sans aviation, +11 RF uniques, aucune publication**.

La base publique **v0.2 reste immuable à 65 mémoires / 48 sans aviation**. Le candidat v0.3 applique désormais la politique paired RX aux liaisons split/duplex déjà sélectionnées et aux nouveaux cas publics validés.

## Candidat Sprint 86

- base v0.2 complète : **65 RX** ;
- base v0.2 sans aviation : **48 RX** ;
- candidat v0.3 complet : **76 RX** ;
- candidat v0.3 sans aviation : **59 RX** ;
- delta : **+11 RF uniques** ;
- plafond conditionnel : **77** si F1ZTH 50.5375 MHz franchit le gate de compatibilité UV-K5/firmware ;
- `Duplex=off`, `Offset=0.000000`, aucune émission ;
- aucune route ni entrée de registre v0.3.

Preuve structurée : `paired-rx-expansion.json`. Builder : `tools/build_annecy_v03_internal_candidate.py`.

## Satellites paired RX

La v0.2 publique conserve les descentes historiques. La v0.3 ajoute **145.850 MHz** comme montée RX partagée SO-50/AO-123 et **435.250 MHz** comme montée RX AO-91. La fréquence 145.850 n’est mémorisée qu’une fois. Les descentes restent déjà présentes : SO-50 436.795, AO-91 145.960, AO-123 435.400 MHz.

Le statut opérationnel AMSAT doit être recontrôlé avant toute publication v0.3.

## Relais France

Nouvelles entrées RX de relais dont les sorties étaient déjà sélectionnées :

- F1ZOH Crozet : **439.625 MHz** ;
- F6ZJD Nurieux : **145.0375 MHz** ;
- F1ZCQ Échirolles : **145.050 MHz** ;
- F1ZCR Chamrousse : **430.325 MHz** ;
- F1ZDC Échirolles : **431.425 MHz**.

F1ZPY/F1ZWY et les transpondeurs F5ZDT, F1ZFX, F1ZIC, F1ZHE, F1ZHG, F5ZGT et F5ZLV n’ajoutent aucune RF après déduplication : leurs deux côtés sont déjà représentés dans la base.

## Haute-Savoie / ADRASEC public

F1ZJV Pointe des Brasses et F1ZYT Semnoz partagent la paire analogique VHF publique **145.1875 / 145.7875 MHz**. Deux mémoires RF suffisent aux deux sites.

La source locale mentionne un lien/transpondeur UHF ADRASEC mais n’en publie pas la fréquence : aucune fréquence UHF n’est inférée, recherchée dans des données privées ou ajoutée au candidat.

## Suisse HB9G

Les sorties HB9G 145.725 et 439.100 MHz étant déjà présentes, le paired RX ajoute leurs entrées **145.125 MHz** et **431.500 MHz**.

## F1ZTH 50 MHz différé

Le REF publie **50.5375 MHz** comme côté analogique supplémentaire de F1ZTH. Les deux autres côtés, 431.275 et 145.2125 MHz, sont déjà présents. La RF 50.5375 représente donc un potentiel +1, mais reste hors candidat tant que RadioPack n’a pas défini et vérifié une base de compatibilité récepteur/firmware UV-K5 permettant de la garantir aux utilisateurs. Aucun firmware tiers n’est supposé.

## Génération

```bash
python tools/build_annecy_v03_internal_candidate.py --output-dir annecy-v03
python tools/build_annecy_v03_internal_candidate.py --no-aviation --output-dir annecy-v03-no-air
```

Le builder repart du candidat v0.2 validé, conserve ses lignes à l’identique et ajoute uniquement les 11 RF de `paired-rx-expansion.json`.

Règles permanentes : v0.2 immuable, RX-only, fréquence identique dédupliquée, données non publiées jamais inférées, réseaux professionnels privés/PPDR exclus, revue humaine obligatoire avant publication.
