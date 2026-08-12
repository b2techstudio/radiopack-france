# Bretagne v0.2 — recherche

Bretagne v0.2 est la version de recherche active basée sur Bretagne v0.1 publiée et immuable (**135 mémoires RX**).

## État Sprint 76

Le candidat interne reste à **151 mémoires RX** : base v0.1=135 + **16 mémoires aviation AIRAC 08/26**. La revalidation des infrastructures radioamateur du Sprint 76 produit un **delta RF de 0**. Aucun export public v0.2 n'existe et le registre public reste sur Bretagne v0.1.

### Aviation

L'aviation occupe les positions **130 à 145** : Rennes Saint-Jacques, Brest Bretagne, Dinard Pleurtuit Saint-Malo, Quimper Pluguffan et la fréquence générique aviation d'urgence 121.500 MHz. Les 16 mémoires sont en AM, **avec un pas de 8,33 kHz**, RX-only. Les positions 146 à 149 restent libres ; aucun remplissage artificiel.

Sources et méthode : `aviation-airac-08.json`. Le produit SIA AIRAC 08/26 courant est vérifié et les dernières pages AIP primaires publiques effectives sont utilisées selon le précédent déjà appliqué à Annecy–Alpes–Léman. Le dépôt ne prétend pas avoir extrait les octets de l'export XML courant ni avoir comparé directement chaque champ à cet XML.

Le builder non public `tools/build_bretagne_v02_internal_candidate.py` reconstruit d'abord la base v0.1 à 135 puis injecte les 16 mémoires aviation aux positions réservées, en vérifiant les collisions de positions, noms et fréquences.

### Infrastructures radioamateur

`amateur-infrastructure-revalidation.json` revalide F5ZPV, F5ZZH, F1ZBZ et F5ZZC-4 :

- F1ZBZ est résolu à **delta 0** car ses valeurs RF actuelles sont déjà toutes représentées dans le plan Bretagne dédupliqué ;
- F5ZPV reste exclu tant que l'ARA35 le donne temporairement arrêté, même si un annuaire général le présente actif ;
- F5ZZH reste arrêté ;
- F5ZZC-4 conserve un rôle APRS/ADRASEC35 documenté mais sans fréquence actuelle validée, et n'est pas assimilé à l'entrée distincte F5ZZC analogique.

## Backlog restant

Restent ouverts : données ADRASEC publiquement vérifiables, cas F1ZUG / ADRASEC 35, attribution locale CROSS Étel Ch64, attribution locale CROSS Corsen Ch79, ainsi que les futures revalidations de F5ZPV, F5ZZH et F5ZZC-4.

Règles permanentes : ne jamais modifier la v0.1 publiée, ne jamais déduire une donnée non publiée, ne jamais dupliquer une fréquence déjà présente pour ajouter une simple attribution locale, faire primer le statut opérateur local pour l'état opérationnel courant et conserver toutes les sorties RadioPack en écoute seule.
