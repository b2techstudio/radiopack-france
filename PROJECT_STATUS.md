# RadioPack France — point de reprise

Dernière mise à jour : **21 août 2026**
Sprint courant : **100**
État logique : **0.21.89**

L'état machine officiel est `research/project-resume-state.json`. Résumé courant : `research/sprint-100-summary.md`.

## État public

- Normandie v0.4 : **142 mémoires RX**, publiée et immuable.
- Annecy–Alpes–Léman v0.4 : **77 mémoires RX**, variante **60 sans aviation**, publiée et immuable.
- Annecy–Alpes–Léman v0.3 : **76 / 59**, historique immuable.
- Bretagne v0.2 : **151 mémoires RX**, publiée et immuable.
- Hauts-de-France v0.2 : **144 mémoires RX**, publiée et immuable.
- Île-de-France v0.2 : **58 mémoires RX**, publiée et immuable.
- Grand Est v0.2 : **59 mémoires RX**, publiée et immuable.
- Centre-Val de Loire v0.3 : **51 mémoires RX**, dont **7 aviation**, publiée et immuable.
- Pays de la Loire v0.2 : **130 mémoires RX**, publiée et immuable.
- Bourgogne-Franche-Comté v0.3 : **54 mémoires RX**, dont **14 aviation**, publiée et immuable.
- Nouvelle-Aquitaine v0.2 : **151 mémoires RX**, publiée et immuable.
- Auvergne-Rhône-Alpes v0.2 : **62 mémoires RX**, publiée et immuable.
- Occitanie v0.2 : **156 mémoires RX**, publiée et immuable.
- Provence-Alpes-Côte d’Azur v0.2 : **159 mémoires RX**, publiée et immuable.
- Corse v0.2 : **137 mémoires RX**, publiée et immuable.

Couverture : **13/13 régions administratives métropolitaines**. Annecy–Alpes–Léman est un pack territorial supplémentaire. Les cinq régions d'outre-mer ne sont pas encore couvertes.

## Sprint 100 — Centre-Val de Loire v0.3

Le Sprint **100 / 0.21.89** officialise Centre-Val de Loire v0.3 à **51 RX**. La v0.2 de 42 RX reste historique et immuable. La v0.3 comprend 20 mémoires radioamateur analogiques et 7 aviation ; Châteauroux-Déols est corrigé à **125.880 MHz** et Saint-Denis-de-l'Hôtel **122.405 MHz** est ajouté. SHA public : `0882c84133576fae7f6b3cba64efc32e915355c254e533ed9850eb0edf2ebaae`.

Références : `research/centre-val-de-loire-v0.3/publication-record.json` et `research/sprint-100-summary.md`.

## Sprint 99 — Bourgogne-Franche-Comté v0.3

Le Sprint **99 / 0.21.88** officialise Bourgogne-Franche-Comté v0.3 à **54 RX**, dont 14 aviation. La v0.2 de 37 RX reste historique et immuable. SHA public : `b5af25a6766b1181e735d376d3f70ab47ffb9ed67b9e38e35bee15e8a86ae7a5`.

Références : `research/bourgogne-franche-comte-v0.3/publication-record.json` et `research/sprint-99-summary.md`.

## Sprint 98 — consolidation officielle de l'enrichissement métropolitain v0.2

Le Sprint **98 / 0.21.87** a consolidé les onze v0.2 avec scopes figés, checklists 10/10, gates satisfaits, publication records et SHA-256 issus d'un build Astro frais. Les v0.1 associées restent historiques et immuables.

Références : `research/sprint-98-summary.md` et `research/sprint-98-metropolitan-publication-manifest.json`.

## Sprint 97 — consolidation de l'état post-Sprint 96

Le Sprint **97 / 0.21.86** a consolidé les détails de canaux régionaux alimentés depuis les CSV publics, les raccourcis du générateur accessibles au clavier et la synchronisation du registre public, sans mutation RF ni CSV.

Références : `research/sprint-97-summary.md` et `research/sprint-97-post96-ui-state.json`.

## Sprint 91 — Bretagne v0.3 AIRAC09 handoff

Le candidat reste à **151 RX, delta 0**. AIRAC 08/26 est courant jusqu'au 2 septembre 2026 inclus ; AIRAC 09/26 doit être revalidé à partir du 3 septembre avant toute publication v0.3.

## Sprint 90 — Normandie v0.5 source refresh

Le candidat reste à **142 RX, delta 0**. R3/F1ZBX et F5ZHA exigent du terrain ; F1ZOV reste sous surveillance d'état opérateur et F6ZES reste sans fréquence/mode public suffisamment établi.

## Sprint 89 — Annecy v0.4 candidat

État historique avant publication : **77 RX / 60 sans aviation**, +1 RF 50.5375 MHz. Ce candidat est ensuite devenu la v0.4 publique immuable.

## Travaux ouverts

### Île-de-France v0.3

Prochaine région métropolitaine à enrichir. La base publique reste **v0.2 / 58 RX / 18 aviation**, immuable.

Un premier checkpoint de recherche a été ouvert le **21 août 2026** dans `research/ile-de-france-v0.3/`. La revue actuelle ne constitue pas encore un candidat de publication : **F5ZAD** et **F1ZUX** ne sont plus reconduits automatiquement ; **F1ZSY** et **F5ZEQ** restent bloqués par des conflits de sources/état ; **F5ZMR Provins** et le crossband **F5ZSY Issy-les-Moulineaux** sont les nouveaux candidats les mieux étayés ; **F5ZBK** et **F1ZTC** demandent encore une seconde corroboration actuelle. Le cas crossband **F5ZNN** doit être résolu avec la déduplication RF avant comptage final.

L'aviation reste sur la photographie **AIRAC 08/26** jusqu'au 2 septembre 2026 inclus. La revue AD 2.18 et NOTAM/SUP AIP reste ouverte ; aucune modification RF aviation n'est promue dans ce checkpoint. Toute publication à partir du **3 septembre 2026** exigera AIRAC 09/26.

Aucun CSV public ni registre de version n'est modifié tant que les gates radio et aviation ne sont pas fermés.

### Bretagne v0.3

Candidat **151 RX, delta 0**. Publication bloquée jusqu'à la revalidation AIRAC 09/26 à partir du **3 septembre 2026**.

### Normandie v0.5

Candidat **142 RX, delta 0** avec les gates terrain/source historiques toujours ouverts.

## Contrat permanent

- RX-only : `Duplex=off`, `Offset=0.000000` ;
- maximum 200 mémoires ;
- paired RX pour les paires distinctes vérifiées ;
- déduplication RF ;
- aucun remplissage artificiel ;
- aucune fréquence ambiguë devinée ;
- données privées/PPDR non publiées ;
- versions publiées immuables ;
- aviation revalidée sur le cycle AIRAC applicable avant toute nouvelle publication.
