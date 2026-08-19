# Sprint 98 — consolidation métropolitaine v0.2

Date : **2026-08-19**  
État logique : **0.21.87**

Le Sprint 98 transforme la publication post-Sprint 97 des onze régions métropolitaines en état officiel auditable. **Aucune fréquence, aucune mémoire RF et aucun CSV public ne sont modifiés par ce sprint.**

## Résultat

- **11** packs v0.2 consolidés ;
- **1135 mémoires RX** sur ces onze packs ;
- un `publication-record.json`, un `release-scope.json`, un `review-checklist.json` **10/10** et un `publication-gates.json` par région ;
- SHA-256 figé sur un build Astro frais pour chaque CSV généré ;
- v0.1 historiques conservées et générables ;
- contrat `Duplex=off` / `Offset=0.000000` inchangé ;
- état officiel porté à **Sprint 98 / 0.21.87**.

| Région | Mémoires | SHA-256 |
|---|---:|---|
| Hauts-de-France | 144 | `881f830ed81a0c55506830f1c767bc2a2a0a674e0677fc971c8f40f6646ca96c` |
| Île-de-France | 58 | `dbcadbcef403d7272dc374a7010def7276b06048a8e863277fcdb3558a8f624d` |
| Grand Est | 59 | `a50416bd8a88af249bb691daa657ffd4b578daf1324bd0ca4dd632a2f1a0e5c1` |
| Centre-Val de Loire | 42 | `68e164763834e69dcd85dd9b1b67777e42922134be33d5e25738f4df71f2bb29` |
| Pays de la Loire | 130 | `b737a2e2849c73ed4dd97a4288d6ad862433948e0d4d7eaaa580648547b7d501` |
| Bourgogne-Franche-Comté | 37 | `828af205aa07fe6685e3ad395ec2f0f56222fcfb5bb2f7b8f6a0bd4082714c0a` |
| Nouvelle-Aquitaine | 151 | `619f13f7c8b6cb2529f4f0320268a055c95edc3e7333acefa795010c6e50a8e2` |
| Auvergne-Rhône-Alpes | 62 | `60b4f96467419db40e9f3f33076057f4e093853c81d9e3315b8fe7f0459daa53` |
| Occitanie | 156 | `30f08222923cf49525d0d5f8c0f4d169cb5cd80ecc2713eee1dc5ac4d2e3b8f4` |
| Provence-Alpes-Côte d’Azur | 159 | `0b4deb7acb334c6aa5f4d8c6127a670c84709c79619176754b3a813491bcb273` |
| Corse | 137 | `0cf92ac1ed0e39793d7257d7c71f43d4e6019d79806456f0aee961b4cc333a70` |

Manifeste : `research/sprint-98-metropolitan-publication-manifest.json`. Audit primaire commun : `research/metropolitan-v0.2-primary-source-audit.md`.

## Travaux actifs conservés

- **Bretagne v0.3** : 151 RX, delta 0, revalidation AIRAC 09/26 requise à partir du 3 septembre 2026 ;
- **Normandie v0.5** : 142 RX, delta 0, gates terrain/source inchangés.

Toute évolution RF ultérieure d'un des onze packs devra créer une nouvelle version ; les v0.2 consolidées ici sont immuables.
