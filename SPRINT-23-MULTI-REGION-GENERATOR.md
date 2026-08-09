# Sprint 23 — Générateur public multi-régions

Date : 2026-08-09

## Objectif

Faire évoluer `/generateur` d'une interface dédiée uniquement à Annecy–Alpes–Léman vers un générateur public capable de sélectionner plusieurs packs régionaux publiés sans dupliquer la logique métier ni reconstruire de CSV côté navigateur.

## Registre public des packs

Nouveau fichier :

```text
website/src/lib/packRegistry.ts
```

Il devient la source de vérité du générateur pour les packs et variantes téléchargeables.

Packs enregistrés au Sprint 23 :

- Annecy–Alpes–Léman v0.2 : 65 mémoires avec aviation ou 48 sans aviation ;
- Normandie v0.3.1 : 139 mémoires dans sa variante publique fixe.

Le registre contient pour chaque variante :

- l'identifiant du pack ;
- le nom et la version ;
- le nombre de mémoires ;
- le nom du fichier ;
- l'URL publique ;
- les options réellement prises en charge.

## Générateur web

La page `/generateur` propose maintenant un sélecteur de pack.

### Annecy–Alpes–Léman

- option Aviation disponible ;
- 65 mémoires avec aviation ;
- 48 mémoires sans aviation ;
- contrôle NOTAM facultatif ;
- liens SOFIA-Briefing et Skybriefing ;
- téléchargement direct de la variante validée.

### Normandie

- variante fixe de 139 mémoires ;
- options Annecy masquées ;
- téléchargement direct du CSV v0.3.1 existant ;
- aucune modification des fréquences Normandie dans ce sprint.

## Règles conservées

- aucun Blob CSV généré dans le navigateur ;
- le bouton pointe uniquement vers une ressource publique validée ;
- toutes les mémoires restent RX-only avec `Duplex=off` ;
- les noms restent limités à 10 caractères ;
- aucun remplissage artificiel ;
- NOTAM reste informatif et non bloquant pour Annecy.

## Architecture réutilisable

Le flux est maintenant :

```text
chirpPack.ts
   ↓
<pack>Pack.ts
   ↓
route CSV / fichier public validé
   ↓
packRegistry.ts
   ↓
/generateur
```

L'ajout d'un futur pack ne doit plus nécessiter de recopier le code JavaScript du générateur.

## Tests ajoutés

### `tests/test_pack_registry.py`

Vérifie notamment :

- la présence d'Annecy et Normandie dans le registre ;
- les comptes 65 / 48 / 139 ;
- les URL publiques ;
- l'absence de v0.1 Annecy ;
- le contrat du sélecteur web ;
- le CSV Normandie en `Duplex=off`.

### `tests/test_built_public_pack_catalog.py`

Après `astro build`, vérifie les trois fichiers réellement déployés :

- Annecy 65 ;
- Annecy sans aviation 48 ;
- Normandie 139.

Le test contrôle également `Duplex=off`, `Offset=0.000000`, les noms et l'unicité des emplacements.

## Publication

Ce sprint ne change aucune fréquence et ne crée aucun nouveau pack régional.

Il prépare l'infrastructure nécessaire pour que le prochain pack puisse être intégré au générateur par configuration plutôt que par duplication de code.
