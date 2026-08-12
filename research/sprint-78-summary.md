# Sprint 78 — Bretagne v0.2 revalidation CROSS Ch64 / Ch79

Date : 12 août 2026
État logique visé : `0.21.67`

## Résultat

Le candidat interne Bretagne v0.2 reste à **151 mémoires RX**. La revalidation des mappings locaux **CROSS Étel Ch64** et **CROSS Corsen Ch79** produit un **delta RF de 0** et **aucune attribution locale promue**.

Bretagne v0.1 reste publique et immuable à 135 mémoires. Aucun CSV Bretagne v0.2 public n'est créé et le registre public n'est pas modifié.

## CROSS Étel — Ch64

La page ministérielle actuelle, mise à jour le 19 juin 2026, continue d'indiquer que les canaux 63 et 64 diffusent un bulletin côtier permanent notamment dans le Morbihan.

En parallèle, la page actuelle du CROSS Étel et son planning météo officiel lient explicitement **Étel au canal 63 en diffusion continue**. Aucun de ces documents locaux actuels ne nomme un site Bretagne sur le canal 64.

Le conflit primaire reste donc ouvert :

- l'existence d'une affirmation régionale Ch64 dans le Morbihan ne permet pas d'identifier un site émetteur ;
- le mapping actuel Étel → Ch63 ne prouve pas l'arrêt de Ch64 ;
- aucune attribution Ch64 locale n'est ajoutée.

La paire générique Ch64 **156.225 / 160.825 MHz** est déjà présente dans Bretagne v0.1 : **delta RF 0**.

## CROSS Corsen — Ch79

La page actuelle du CROSS Corsen confirme la diffusion des bulletins météo depuis des stations VHF/MHF réparties sur le littoral, mais ne relie pas le canal 79 à un émetteur déterminé.

La page officielle du bilan 2025, publiée le 2 mars 2026, fournit un PDF primaire de 14,6 Mio. Ce PDF est identifié mais n'est pas extractible par l'outil web du workflow actuel ; aucune conclusion de site n'en est tirée.

Météo-France publie le **Guide Marine 2026** comme référence contenant horaires et fréquences VHF. Son PDF est lui aussi identifié mais non extractible dans le workflow courant ; son indisponibilité n'est pas une preuve négative.

Les indices secondaires actuels restent cohérents avec :

- Cap Fréhel + Bodic sur Ch79 dans la source locale d'Erquy ;
- Fréhel, Bodic, Batz, Stiff et Pointe du Raz dans une source secondaire plus large.

Ces indices ne remplacent pas une attribution primaire actuelle. Aucun de ces sites n'est promu dans RadioPack.

La paire générique Ch79 **156.975 / 161.575 MHz** est déjà présente : **delta RF 0**.

## Artefacts

```text
research/bretagne-v0.2/cross-local-mapping-revalidation.json
research/bretagne-v0.2/backlog.json
research/bretagne-v0.2/pack-plan.json
tests/test_sprint78_bretagne_cross_mapping_revalidation.py
research/sprint-78-summary.md
```

## Garde-fous

- une paire RF générique déjà présente n'est jamais dupliquée pour ajouter une simple métadonnée de site ;
- une affirmation régionale sur un canal ne nomme pas automatiquement le site émetteur ;
- l'existence actuelle d'un réseau CROSS ne mappe pas automatiquement un canal vers une station ;
- une piste secondaire n'est pas une validation primaire ;
- une affectation historique n'est pas une validation actuelle ;
- un PDF primaire identifié mais non extrait n'est pas une preuve négative ;
- un conflit entre sources primaires actuelles doit être réconcilié avant promotion ;
- aucune attribution de site n'est devinée ;
- toutes les sorties RadioPack restent RX-only ;
- aucune publication Bretagne v0.2 n'est effectuée.
