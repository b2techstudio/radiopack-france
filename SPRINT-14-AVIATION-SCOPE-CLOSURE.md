# RadioPack France — Sprint 14

## Clôture conservatrice du périmètre aviation v0.2

Ce sprint ne cherche pas à augmenter artificiellement le nombre de mémoires. Il clôt le dernier bloc de recherche aviation lorsque les sources primaires ne sont pas suffisamment extractibles dans le workflow actuel.

## Résultat

Le candidat interne reste à **65 mémoires**.

```text
000–015  PMR446                              16
020–025  APRS / ISS                           6
026–028  Satellites FM                        3
030–031  Canaux d'appel                       2
040–058  Radioamateur France                 19
090–091  Radioamateur Suisse                  2
125–135  Aviation France / bassin genevois   11
155–160  Aviation Suisse                      6
Total                                        65
```

Toutes les mémoires restent en réception seule avec `Duplex=off`.

## Terrains volontairement omis

### LFKA — Albertville

La VAC primaire `AD-2.LFKA.pdf` est bien référencée dans le catalogue officiel SIA. Son bloc radio n'a cependant pas pu être extrait de façon suffisamment fiable dans ce workflow. Des valeurs existent sur des sources secondaires, mais elles ne sont pas utilisées.

Statut : `excluded_scope_unverified_primary`.

### LFHM — Megève

Même règle : la VAC primaire `AD-2.LFHM.pdf` est identifiée dans le catalogue officiel SIA, mais le bloc radio primaire n'est pas exploitable ici avec un niveau de confiance suffisant. Aucune fréquence secondaire n'est promue.

Statut : `excluded_scope_unverified_primary`.

### LSGG — Genève-aéroport

L'OFAC confirme LSGG et l'exploitant, et le cycle AIP courant est connu via Skyguide/Skybriefing. Plusieurs listes secondaires donnent des fréquences de Genève, mais le tableau radio opérationnel primaire courant n'est pas publiquement extractible de façon assez fiable dans ce workflow.

Statut : `excluded_scope_unverified_primary`.

`GENEV-INFO` 126.350 MHz reste présente dans le bloc transfrontalier car cette fréquence dispose déjà d'un recoupement officiel distinct.

### LFHZ — Sallanches-Mont-Blanc

Reste `excluded_closed_aerodrome`, fermeture effective depuis le 1er septembre 2020.

## Porte de recherche aviation

La porte `pending_airfields` passe de :

```text
pending_research_completion
```

à :

```text
passed_scope_closed
```

Elle ne contient plus d'élément en attente. Cette validation signifie uniquement que le **périmètre v0.2 est explicitement décidé** ; elle ne prétend pas que LFKA, LFHM ou LSGG n'ont pas de fréquences actives.

## Ce qui bloque encore une publication

`public_release_allowed` reste `false`.

Les contrôles dynamiques suivants restent obligatoires juste avant publication :

1. NOTAM France via SOFIA-Briefing ;
2. NOTAM Suisse via Skybriefing ;
3. statut opérationnel des satellites FM via AMSAT.

Ces vérifications ne doivent pas être déclarées valides plusieurs jours à l'avance.

## Sources secondaires

Les fréquences repérées sur des bases communautaires ou privées ont uniquement servi à orienter les recherches. Elles ne sont pas enregistrées comme mémoires, ni comme données de production, et ne remplacent pas les sources primaires manquantes.

## Aucun changement public

- aucun CSV Annecy v0.2 publié ;
- aucun PDF Annecy v0.2 publié ;
- aucun lien de téléchargement Annecy v0.2 ;
- statut public toujours « En préparation » ;
- générateur public toujours déconnecté des fichiers de recherche v0.2.

## Synchronisation locale

```powershell
cd "C:\Users\cross\Documents\CODE\PROJETS\RadioPack-France"
git pull --ff-only
python tools\build_annecy_internal_candidate.py
python tests\test_annecy_airac08.py
python tests\test_annecy_internal_candidate.py
git status
```

Résultat attendu : candidat interne de 65 mémoires et tests OK.
