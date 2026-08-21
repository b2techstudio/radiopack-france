# Île-de-France v0.3 — checkpoint de recherche

Checkpoint ouvert le **21 août 2026** à partir de la **v0.2 publique immuable de 58 mémoires RX**.

Ce dossier ne constitue **pas** encore un candidat de publication. Aucun CSV public n'est modifié par ce checkpoint. La v0.3 doit d'abord fermer les conflits de sources radioamateur et terminer la revalidation aviation SIA/AIRAC.

## Radioamateur — première passe actuelle

La revue élargit le périmètre au 2 m, 70 cm et aux transpondeurs crossband analogiques, avec paired RX pour les paires distinctes et déduplication RF.

### Base v0.2 encore soutenue comme candidat de travail

- **F5ZNG Provins** — 145.625 / 145.025 MHz ;
- **F5ZNN Saint-Rémy-la-Vanne** — 145.650 / 145.050 MHz ;
- **F5ZMH Linas** — 145.7375 / 145.1375 MHz ;
- **F1ZHK Nangis** — 145.7625 / 145.1625 MHz, avec capture REF courante encore souhaitée avant promotion définitive.

### Nouveaux candidats fortement étayés

- **F5ZMR Provins** — 431.525 / 439.125 MHz ;
- **F5ZSY Issy-les-Moulineaux** — transpondeur analogique crossband 145.325 / 430.325 MHz.

### Candidats encore à recouper

- **F5ZBK Triel-sur-Seine** — 430.175 / 431.775 MHz : entrée REF courante active, seconde source opérationnelle actuelle encore recherchée ;
- **F1ZTC Paris 16** — 145.7875 / 145.1875 MHz : entrée REF courante active, seconde source opérationnelle actuelle encore recherchée.

### Non reconduits ou différés à ce stade

- **F5ZAD Clamart** : non reconduit ; REF le donne à l'arrêt et RepeaterBook le donne hors service ;
- **F1ZUX Achères** : non reconduit ; les éléments actuels indiquent un relais hors service/stale pour ce site francilien ;
- **F1ZSY Paris 16** : différé ; conflit entre des listes qui le donnent actif et RepeaterBook qui le donne inactif depuis plusieurs années ;
- **F5ZEQ Le Mesnil-le-Roi / Sartrouville** : différé ; conflit entre listes générales actives et page opérateur indiquant une maintenance / indisponibilité ;
- **F5ZDR Linas** : différé jusqu'à confirmation actuelle d'un fonctionnement UHF stable ;
- **F5ZNN crossband 145.650 / 430.650 MHz** : différé pour résoudre proprement le rôle et la déduplication de 145.650 MHz déjà présent dans la paire 2 m.

Le détail structuré est dans `radio-validation-2026-08-21.json`.

## Aviation — AIRAC 08/26

Le bloc public v0.2 contient **18 mémoires aviation AM**. La photographie AIRAC 08/26 reste courante jusqu'au **2 septembre 2026 inclus**.

La première passe du 21 août a identifié des SUP AIP actifs autour d'Orly, mais aucun changement de fréquence n'est promu sur cette seule base. La v0.3 conserve donc un **gate aviation ouvert** : revue complète des rubriques AD 2.18 utiles, puis contrôle NOTAM/SUP AIP applicable avant toute décision RF.

Toute publication ou nouvelle validation effectuée à partir du **3 septembre 2026** devra être reprise sur **AIRAC 09/26**.

Le détail est dans `aviation-airac08-2026-08-21.json`.

## Règles permanentes

- RX uniquement : `Duplex=off`, `Offset=0.000000` ;
- maximum 200 mémoires ;
- paired RX pour les paires distinctes vérifiées ;
- déduplication RF ;
- aucun remplissage artificiel ;
- aucun état, mode ou fréquence ambigu ne doit être deviné ;
- données privées, PPDR, chiffrées ou non publiquement vérifiables exclues ;
- v0.2 publique conservée immuable ;
- publication v0.3 interdite tant que les gates radio et aviation ne sont pas fermés.
