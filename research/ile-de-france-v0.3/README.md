# Île-de-France v0.3 — publiée et immuable

Travail ouvert le **21 août 2026** à partir de la **v0.2 publique immuable de 58 mémoires RX** et publication finalisée le **22 août 2026**.

La v0.3 publique contient **57 mémoires RX** et est désormais figée. La v0.2 reste historique et immuable.

## Radioamateur — scope final

Retenus :

- **F5ZNG Provins** — 145.625 / 145.025 MHz ;
- **F5ZNN Saint-Rémy-la-Vanne** — 145.650 / 145.050 MHz ;
- **F5ZMH Linas** — 145.7375 / 145.1375 MHz ;
- **F1ZHK Nangis** — 145.7625 / 145.1625 MHz ;
- **F6ZEE Pontault-Combault** — 145.100 / 145.700 MHz ;
- **F5ZMR Provins** — 431.525 / 439.125 MHz ;
- **F5ZSY Issy-les-Moulineaux** — 145.325 / 430.325 MHz ;
- **F5ZNN crossband** — seule RF nouvelle **430.650 MHz** après déduplication avec 145.650 MHz.

Non reconduits dans ce scope : **F5ZAD, F1ZUX, ancienne attribution F1ZSY, F5ZEQ, F1ZTC, F5ZDR, F5ZBK et F1ZDL**. Les dossiers insuffisamment corroborés restent réévaluables ultérieurement ; leur exclusion ne constitue pas une déclaration de fermeture définitive.

Bloc radio régional final : **15 RF uniques**.

## Aviation — AIRAC 08/26

Le pack conserve **18 mémoires aviation, delta 0**, sans expansion :

- **LFPG** : sous-ensemble retenu revalidé directement sur AIRAC 08/26 ;
- **LFPO** : catalogue COM SIA courant, AD 2.18 officiel, SUP AIP 085/2026 et 147/2026 et revue NOTAM courante ;
- **LFPB** : NOTAM A2706/26 pour ATIS/GND/TWR/DEL et matériel SIA 2026 pour INFO 123.835 MHz.

Aucune fréquence aviation supplémentaire n'est ajoutée. La validation est fraîche jusqu'au **2 septembre 2026 inclus** ; AIRAC 09/26 est obligatoire à partir du **3 septembre 2026** avant toute nouvelle révision aviation.

## Publication déterministe

- total : **57 RX** ;
- aviation : **18** ;
- radio régionales : **15** ;
- SHA-256 public : `e04e6dbbf869661305068bac55cd8044abdcea7321d67e4c28111c9d057da125` ;
- SHA-256 v0.2 historique : `dbcadbcef403d7272dc374a7010def7276b06048a8e863277fcdb3558a8f624d` ;
- builder : `tools/build_idf_v03_candidate.py` ;
- CSV candidat : `generated/release-candidate/radiopack-france-ile-de-france-v0.3-candidate.csv` ;
- CSV public : `website/public/downloads/ile-de-france/radiopack-france-ile-de-france-v0.3.csv`.

Le CSV public réutilise **exactement le même blob Git** que le candidat figé ; la CI vérifie en plus l'identité byte-à-byte et le SHA-256.

## Gates finaux

- checklist : **12/12** ;
- blockers : **0** ;
- RX-only : validé ;
- déduplication RF : validée ;
- limite 200 : validée ;
- publication record : **`published_immutable`** ;
- `published = true` ;
- v0.2 historique conservée immuable.

## Règles permanentes

- RX uniquement : `Duplex=off`, `Offset=0.000000` ;
- maximum 200 mémoires ;
- paired RX pour les paires distinctes vérifiées ;
- déduplication RF ;
- aucun remplissage artificiel ;
- aucune fréquence ambiguë devinée ;
- données privées, PPDR, chiffrées ou non publiquement vérifiables exclues ;
- toute nouvelle version publique devra recevoir un nouveau numéro et préserver cette v0.3 immuable.
