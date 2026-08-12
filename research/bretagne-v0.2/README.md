# Bretagne v0.2 — recherche

Bretagne v0.2 est la version de recherche active basée sur Bretagne v0.1 publiée et immuable (**135 mémoires RX**).

## État Sprint 75

Le candidat interne contient désormais **151 mémoires RX**, soit **+16 mémoires aviation** validées dans le contexte AIRAC 08/26. Aucun export public v0.2 n'existe et le registre public reste sur Bretagne v0.1.

L'aviation occupe les positions **130 à 145** : Rennes Saint-Jacques, Brest Bretagne, Dinard Pleurtuit Saint-Malo, Quimper Pluguffan et la fréquence générique aviation d'urgence 121.500 MHz. Les positions 146 à 149 restent libres ; aucun remplissage artificiel.

Sources et méthode : `aviation-airac-08.json`. Le produit SIA AIRAC 08/26 courant est vérifié et les dernières pages AIP primaires publiques effectives sont utilisées selon le précédent déjà appliqué à Annecy–Alpes–Léman. Le dépôt ne prétend pas avoir extrait les octets de l'export XML courant ni avoir comparé directement chaque champ à cet XML.

Le builder non public `tools/build_bretagne_v02_internal_candidate.py` reconstruit d'abord la base v0.1 à 135 puis injecte les 16 mémoires aviation aux positions réservées, en vérifiant les collisions de positions, noms et fréquences.

## Backlog restant

Restent ouverts : données ADRASEC publiquement vérifiables, cas F1ZUG / ADRASEC 35, attribution locale CROSS Étel Ch64, attribution locale CROSS Corsen Ch79 et infrastructures radioamateur nécessitant une revalidation actuelle.

Règles permanentes : ne jamais modifier la v0.1 publiée, ne jamais déduire une donnée non publiée, ne jamais dupliquer une fréquence déjà présente pour ajouter une simple attribution locale, et conserver toutes les sorties RadioPack en écoute seule.
