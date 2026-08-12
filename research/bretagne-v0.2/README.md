# Bretagne v0.2 — recherche

Bretagne v0.2 est publiée et immuable à **151 mémoires RX**, construite depuis Bretagne v0.1 historique et immuable (**135 mémoires RX**) + 16 mémoires aviation AIRAC 08/26.

## État Sprint 80 — publiée

Le candidat interne est désormais **figé à 151 mémoires RX** : base v0.1=135 + **16 mémoires aviation AIRAC 08/26**. Les revalidations radioamateur du Sprint 76, ADRASEC publique du Sprint 77 et CROSS Ch64/Ch79 du Sprint 78 produisent chacune un **delta RF de 0**. Le Sprint 79 clôt la revue de maturité à **10/10, 0 bloqueur, prépublication prête**. Le CSV public v0.2 et le registre sont désormais publiés ; Bretagne v0.1 reste conservée comme historique immuable.

### Publication Sprint 80

Le CSV public `website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv` est la copie exacte du candidat figé à 151 mémoires. Son SHA-256 est `73aa3d530ae9f6c572eb01794b0861ecba61df0faf7884ee766085d3de7601a4`.

`publication-record.json` enregistre l'empreinte, le cycle AIRAC 08/26, la fenêtre de validité jusqu'au 2 septembre 2026 inclus et les dossiers explicitement reportés après v0.2.

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

### ADRASEC — revalidation publique Sprint 77

`adrasec-public-revalidation.json` traite uniquement les informations publiquement vérifiables des ADRASEC 22, 29, 35 et 56 :

- les quatre associations sont confirmées dans l'agrément FNRASEC courant ; cette appartenance ne publie aucune fréquence ;
- ADRASEC 29 est recoupée publiquement avec F1ZBH-3 / F1ZGQ-3 sur APRS 144.800 MHz, déjà présent nationalement : **delta 0** ;
- F1ZUG conserve APRS 144.800 MHz, mais la fréquence de sa fonction transpondeur ADRASEC 35 reste non publiée et n'est pas inférée ;
- ADRASEC 56 publie son activité et des rôles APRS, sans fréquence de service ADRASEC actuelle distincte promue ;
- ADRASEC 22 ne reçoit aucune fréquence par simple géographie ou appartenance.

Les données opérationnelles privées PPDR restent hors périmètre.

### CROSS Étel Ch64 / Corsen Ch79 — Sprint 78

`cross-local-mapping-revalidation.json` confirme que les paires RF Ch64 et Ch79 restent génériques et déjà dédupliquées.

- Étel : le site est explicitement associé à Ch63 dans la documentation opérationnelle actuelle ; l'affirmation régionale Ch64 dans le Morbihan ne suffit pas à nommer un émetteur Ch64.
- Corsen : le réseau radio côtier actuel est confirmé mais Ch79 n'est toujours pas mappé par une source primaire actuelle vers Fréhel, Bodic, Batz, Stiff ou Pointe du Raz.
- Les indices secondaires ne sont pas promus et les PDF primaires identifiés mais non extraits ne produisent aucune conclusion négative.

Résultat : **151 mémoires RX, delta 0, 0 attribution locale promue**.

### Prépublication — Sprint 79

`maturity-review.json`, `release-scope.json`, `review-checklist.json` et `publication-gates.json` figent le périmètre à **151 mémoires RX**.

- revue : **10/10** ;
- bloqueurs : **0** ;
- audit reproductible : `tools/run_bretagne_v02_prepublication_audit.py --require-prepublication-ready` ;
- publication : **non effectuée**.

Le cycle AIRAC 08/26 est toujours courant au 12 août 2026. Les dossiers F1ZUG, mappings locaux CROSS et infrastructures amateur arrêtées/non résolues sont désormais explicitement reportés hors du scope figé et ne justifient aucun remplissage ou ajout RF.

## Dossiers reportés après le scope v0.2

Restent ouverts pour une version ou une revue future : fréquence de la fonction transpondeur F1ZUG / ADRASEC 35 non publiée, attribution locale CROSS Étel Ch64, attribution locale CROSS Corsen Ch79, ainsi que les futures revalidations de F5ZPV, F5ZZH et F5ZZC-4. Ils sont explicitement hors du périmètre v0.2 figé. La revalidation publique générale ADRASEC 22/29/35/56 est close à delta RF 0.

Règles permanentes : ne jamais modifier la v0.1 publiée, ne jamais déduire une donnée non publiée, ne jamais dupliquer une fréquence déjà présente pour ajouter une simple attribution locale, faire primer le statut opérateur local pour l'état opérationnel courant et conserver toutes les sorties RadioPack en écoute seule.
