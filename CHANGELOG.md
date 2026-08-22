# Changelog

## 0.21.92 - 2026-08-22

**Sprint 104** — Grand Est v0.4 publiée et figée à **97 mémoires RX** après le Sprint 103 d'audit VHF navigation intérieure.

- +13 mémoires VHF fluviales validées ;
- 19 aviation inchangées, delta 0 ;
- 41 radio régionales inchangées, delta 0 ;
- candidat/public byte-identiques ;
- SHA-256 : `ba34604b11b75ae7f0e7aa17e3734053ff37bbe7910218af1ab66e59f3428a5d` ;
- v0.3/84 et v0.2/59 conservées immuables ;
- audit national : aucune duplication des RF fluviales déjà présentes dans les blocs VHF maritimes côtiers.

## 0.21.91 - 2026-08-22

**Sprint 102** — Grand Est v0.3 publiée et figée à **84 mémoires RX**, dont 19 aviation et 41 radio régionales. SHA-256 : `45aef8547a701e7541e620fa9a2d8394595576921e793b75238146ff6e42e720`.

## 0.21.90 - 2026-08-22

**Sprint 101** — Île-de-France v0.3 publiée et figée à **57 mémoires RX**.

- base historique **Île-de-France v0.2 / 58 RX / 18 aviation** conservée immuable ;
- v0.3 : **57 RX**, dont **18 aviation** et **15 radio régionales** ;
- scope radio finalisé avec F5ZNG, F5ZNN, F5ZMH, F1ZHK, F6ZEE, F5ZMR, F5ZSY et extension crossband F5ZNN dédupliquée ;
- F5ZEQ non reconduit pendant sa maintenance ; F1ZTC, F5ZDR, F5ZBK et F1ZDL différés faute de corroboration actuelle suffisante ;
- aviation AIRAC 08/26 conservée à 18 mémoires, delta 0, avec revue LFPG/LFPO/LFPB et NOTAM/SUP du sous-ensemble retenu ;
- AIRAC 09/26 obligatoire pour toute nouvelle révision aviation à partir du 3 septembre 2026 ;
- checklist **12/12**, publication gates **0 blocker** ;
- CSV public strictement byte-identique au candidat déterministe ;
- SHA-256 public : `e04e6dbbf869661305068bac55cd8044abdcea7321d67e4c28111c9d057da125` ;
- publication record : `published_immutable` ;
- RX-only, paired RX, déduplication et aucun remplissage artificiel.

## 0.21.89 - 2026-08-20

**Sprint 100** — Centre-Val de Loire v0.3 publiée et figée à **51 mémoires RX**.

- 20 mémoires radioamateur analogiques sur 10 infrastructures ;
- 7 mémoires aviation AM ;
- Châteauroux-Déols corrigé de 125.875 à **125.880 MHz** ;
- Saint-Denis-de-l'Hôtel **122.405 MHz** ajouté ;
- F5ZQY non reconduit, F5ZNX et autres dossiers ambigus différés ;
- SHA-256 public : `0882c84133576fae7f6b3cba64efc32e915355c254e533ed9850eb0edf2ebaae` ;
- v0.2 de 42 RX conservée immuable ;
- RX-only, paired RX, déduplication et aucun remplissage artificiel.

## 0.21.88 - 2026-08-19

**Sprint 99** — Bourgogne-Franche-Comté v0.3 publiée et figée à **54 mémoires RX**.

- +10 mémoires radioamateur analogiques validées ;
- 14 mémoires aviation au total ;
- SHA-256 public : `b5af25a6766b1181e735d376d3f70ab47ffb9ed67b9e38e35bee15e8a86ae7a5` ;
- v0.2 de 37 RX conservée immuable ;
- dossiers insuffisamment prouvés différés.

## 0.21.87 - 2026-08-19

**Sprint 98** — consolidation officielle des onze packs métropolitains v0.2.

- couverture administrative métropolitaine 13/13 ;
- publication records, scopes, checklists 10/10 et gates satisfaits ;
- SHA-256 calculés sur build Astro frais ;
- aucune mutation RF ni réécriture des v0.1 historiques.

## 0.21.86 - 2026-08-17

**Sprint 97** — consolidation de l'état post-Sprint 96.

- détails de canaux régionaux depuis les CSV publics ;
- raccourcis du générateur accessibles au clavier ;
- registre public utilisé comme source de vérité ;
- aucune mutation RF ou CSV public.

## 0.21.85 - 2026-08-15

**Sprint 96** — thème Midnight Blue Soft et synchronisation du site public.

## Repères historiques conservés

Les versions publiées précédentes restent immuables. Les dossiers historiques détaillés et leurs preuves restent conservés sous `research/`, et les garde-fous de compatibilité des anciens sprints restent exécutés en CI.
