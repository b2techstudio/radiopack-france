# Sprint 105 — Île-de-France v0.4 publiée

Date : **22 août 2026**  
État logique : **0.21.93**

## Résultat

Île-de-France v0.4 est publiée et figée à **64 mémoires RX** à partir de la v0.3 immuable de **57 RX**.

- aviation : **18 mémoires**, delta **0** ;
- radio régionale : **15 mémoires**, delta **0** ;
- **+7 mémoires VHF de navigation intérieure** ;
- candidat et CSV public byte-identiques ;
- SHA-256 candidat/public : `14e1d1d95b38ef44d01b9cccb989a3f1567153ac64875594cc24bd4b57a1cdc2`.

## VHF navigation intérieure

Le scope permanent retenu utilise uniquement des affectations suffisamment documentées par VNF et le plan de fréquences ANFR :

- canal 10 : **156.500 MHz** ;
- canal 18 : **156.900 / 161.500 MHz** en paired RX ;
- canal 20 : **157.000 / 161.600 MHz** en paired RX ;
- canal 22 : **157.100 / 161.700 MHz** en paired RX.

Le flyer VNF du PCC de Vives-Eaux de mai 2026 documente les affectations actuelles des cinq écluses : Varennes 22, Champagne 18, La Cave 22, Vives-Eaux 20 et Le Coudray 22.

Les sept mémoires occupent les emplacements **120 à 126**, en `NFM`, pas de 25 kHz, `Duplex=off`, `Offset=0.000000`.

Le **canal 69 n'est pas promu** : la documentation actuelle 2026 consultée ne justifie pas une mémoire permanente dans ce scope. Aucun canal 16 maritime n'est ajouté.

## Aviation

Les **18 mémoires aviation** de la v0.3 sont héritées sans modification. Aucune nouvelle revalidation champ par champ n'est revendiquée pour Sprint 105.

AIRAC 08/26 reste applicable jusqu'au **2 septembre 2026 inclus**. Toute nouvelle révision aviation à partir du **3 septembre 2026** exige une revalidation AIRAC 09/26.

## Intégrité

- base publique v0.3 vérifiée par SHA-256 : `e04e6dbbf869661305068bac55cd8044abdcea7321d67e4c28111c9d057da125` ;
- builder déterministe : `tools/build_idf_v04_candidate.py` ;
- RF, noms et locations uniques ;
- aucune duplication avec la base v0.3 ;
- checklist **12/12** ;
- publication gates : **0 blocker** ;
- versions v0.3/57 et v0.2/58 conservées historiques et immuables.

Référence principale : `research/ile-de-france-v0.4/publication-record.json`.
