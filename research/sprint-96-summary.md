# Sprint 96 — Midnight Blue Soft production rollout

Date : **15 août 2026**  
État logique : **0.21.85**

## Résultat

- **Midnight Blue Soft** devient la direction visuelle de production de RadioPack France.
- Palette officielle : fond `#182538`, surface `#223249`, carte `#2B3D56`, texte `#F4F7FB`, bleu `#4EA8FF`, violet `#9185FF`, vert RX `#65D7B1`, jaune signal `#F4C95D`.
- La page d’accueil reprend une identité radioamateur épurée : double VFO, S-mètre, repères 6 m / 2 m / 70 cm et banques mémoire régionales.
- Header, footer et socle CSS public sont harmonisés avec la même direction.
- `telechargements.astro` et `versions.astro` utilisent désormais `publicPacks` comme source de vérité pour les versions, variantes, compteurs et URLs des packs régionaux.
- `tests/test_pack_registry.py` bloque le retour des anciennes références Bretagne v0.1 / Annecy v0.2 sur ces pages.

## Invariants préservés

- Normandie publique : **v0.4 / 142 RX**, immuable.
- Annecy–Alpes–Léman publique : **v0.4 / 77 RX**, variante **60 RX sans aviation**, immuable.
- Bretagne publique : **v0.2 / 151 RX**, immuable.
- Aucun CSV public, aucune fréquence, aucune mémoire RF et aucune règle d’émission n’ont été modifiés par ce sprint.
- Bretagne v0.3 reste à **151 RX, delta 0**, en attente de la revalidation AIRAC 09/26 à partir du 3 septembre 2026.
- Le domaine personnalisé `radiopack.b2tech.studio` reste séparé de l’origine Cloudflare Pages tant que sa configuration DNS n’est pas finalisée.

## Validation

Le sprint est conçu pour être clôturé uniquement après passage du build Astro, des tests dépôt/radio, de l’audit sécurité et des gardes permanentes sur le SHA final de documentation.
