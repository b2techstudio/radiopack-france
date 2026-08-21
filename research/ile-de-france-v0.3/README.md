# Île-de-France v0.3 — prépublication prête

Travail ouvert le **21 août 2026** à partir de la **v0.2 publique immuable de 58 mémoires RX**.

Le dossier contient un **release candidate interne déterministe de 57 mémoires RX** et son bundle de prépublication complet. La v0.3 est **prête à publier mais pas encore publiée** : la v0.2 reste l'unique version publique.

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

Non reconduits dans ce scope : F5ZAD, F1ZUX, ancienne attribution F1ZSY, F5ZEQ, F1ZTC, F5ZDR, F5ZBK et F1ZDL. Les dossiers insuffisamment corroborés restent réévaluables ultérieurement.

Bloc radio régional final : **15 RF uniques**.

## Aviation — scope final AIRAC 08/26

Le candidat conserve **18 mémoires aviation, delta 0**, sans expansion :

- **LFPG** : sous-ensemble retenu revalidé directement sur AIRAC 08/26 ;
- **LFPO** : catalogue COM SIA courant, AD 2.18 officiel, SUP AIP 085/2026 et 147/2026 et revue NOTAM courante ;
- **LFPB** : NOTAM A2706/26 pour ATIS/GND/TWR/DEL et matériel SIA 2026 pour INFO 123.835 MHz.

Aucune fréquence aviation supplémentaire n'est ajoutée. La validation est fraîche jusqu'au **2 septembre 2026 inclus** ; AIRAC 09/26 est obligatoire à partir du **3 septembre 2026** avant publication ou nouvelle validation aviation.

## Candidat déterministe

- total : **57 RX** ;
- aviation : **18** ;
- radio régionales : **15** ;
- SHA-256 : `e04e6dbbf869661305068bac55cd8044abdcea7321d67e4c28111c9d057da125` ;
- builder : `tools/build_idf_v03_candidate.py` ;
- CSV candidat : `generated/release-candidate/radiopack-france-ile-de-france-v0.3-candidate.csv` ;
- manifeste : `generated/release-candidate/candidate-manifest.json`.

Avant de construire la v0.3, le builder reconstruit obligatoirement la v0.2 et vérifie son SHA public figé : `dbcadbcef403d7272dc374a7010def7276b06048a8e863277fcdb3558a8f624d`.

## Prépublication

- `review-checklist.json` : **12/12** ;
- `publication-gates.json` : **0 blocker** ;
- `publication-record.json` : figé avec statut `prepublication_frozen_not_published` ;
- `release-scope.json` : `publication_ready=true`, `published=false` ;
- aucune route CSV publique v0.3 créée ;
- aucun registre public modifié.

Tous les gates internes sont donc fermés. La seule étape restante est la publication atomique : le futur CSV public devra être strictement identique au candidat et conserver le SHA `e04e6dbbf869661305068bac55cd8044abdcea7321d67e4c28111c9d057da125` avant que le record soit marqué `published_immutable`.

## Règles permanentes

- RX uniquement : `Duplex=off`, `Offset=0.000000` ;
- maximum 200 mémoires ;
- paired RX pour les paires distinctes vérifiées ;
- déduplication RF ;
- aucun remplissage artificiel ;
- aucune fréquence ambiguë devinée ;
- données privées, PPDR, chiffrées ou non publiquement vérifiables exclues ;
- versions publiées immuables ;
- revalidation AIRAC obligatoire si la fenêtre de fraîcheur est franchie avant publication.
