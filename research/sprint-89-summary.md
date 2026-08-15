# Sprint 89 — Annecy–Alpes–Léman v0.4 compatibility closure

Date : 2026-08-15
État : 0.21.78

Le gate qui maintenait F1ZTH 50.5375 MHz hors de la v0.3 est levé pour une future v0.4 : le manuel UV-K5 constructeur/FCC couvre la réception 50–600 MHz et le pilote CHIRP UV-K5 stock déclare la bande 50–76 MHz. Le REF courant publie F1ZTH actif en analogique FM.

Candidat déterministe non public : **77 RX / 60 sans aviation**, soit **+1 RF** depuis la v0.3 publique 76/59.

- ajout : `ZTH-6M` 50.537500 MHz, FM, RX-only ;
- v0.3 reste immuable ;
- aucune UHF ADRASEC non publiée n'est inférée ;
- SHA candidat complet : `2557076fcb198b830cd3b5ba64d7ff894c8e0d6e90eafc0fa40b691a3c6a5d98` ;
- SHA candidat sans aviation : `e31bfc6fce402af117b4f79caf6547b60a23c91ef36491e1351c74e96329aa6c`.

Preuve : `research/annecy-alpes-leman-v0.4/compatibility-and-source-review.json`. Builder : `tools/build_annecy_v04_candidate.py`.
