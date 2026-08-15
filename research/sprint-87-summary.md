# Sprint 87 — prépublication Annecy–Alpes–Léman v0.3

État logique : **0.21.76**.

Le périmètre v0.3 est figé à **76 mémoires RX / 59 sans aviation**, soit **+11 RF uniques** par rapport à la v0.2. La revalidation des sources courantes, le cycle AIRAC, les satellites, la déduplication et les exclusions ont été revus avant publication.

Checklist : **12/12**, bloqueurs : **0**. F1ZTH 50.5375 MHz est une exclusion de scope documentée, pas une fréquence devinée ni un bloqueur. La liaison UHF ADRASEC non publiée n'est pas inférée.

Le builder `tools/build_annecy_v03_release_candidate.py` reproduit les deux variantes et le plan de revue ligne par ligne avant toute copie publique.
