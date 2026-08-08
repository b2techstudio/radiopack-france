# Annecy–Alpes–Léman v0.2 — base de recherche

Cette arborescence prépare la reconstruction sans publier de fréquence non recoupée.

## Périmètre

France : Haute-Savoie (74), Savoie (73), Ain (01), Isère (38), avec zones voisines uniquement lorsque l'intérêt régional est documenté.

Suisse : Genève, Vaud et Valais.

Les blocs français et suisses restent séparés dans le plan mémoire et la documentation.

## État au 8 août 2026

### Radioamateur

Le candidat contient 19 fréquences analogiques françaises vérifiées et 2 sorties suisses HB9G `verified_current`. Les candidats suisses non recoupés et les conflits F1ZJV/F1ZYT restent hors assemblage.

### Aviation France — AIRAC 08/26

Onze mémoires sont recoupées sur les publications officielles :

- Annecy-Meythet : 118.200 MHz ;
- Annemasse : 125.875 MHz ;
- Chambéry Aix-les-Bains : 123.700, 121.205, 118.300 et 127.100 MHz ;
- Grenoble-Le Versoud : 121.000 MHz ;
- Grenoble-Alpes-Isère : 121.930, 119.300 et 133.855 MHz ;
- Genève Information : 126.350 MHz.

Toutes sont en `AM`, pas `8.33`, `rx_only`, et statut `verified_airac08_public`.

Le pré-inventaire AIRAC 07/26 reste historique et interdit à l'assembleur.

#### Périmètre explicitement exclu

- **LFKA Albertville** : la VAC primaire courante est identifiée au catalogue SIA, mais son bloc radio n'est pas extractible de façon suffisamment fiable dans ce workflow. Les fréquences trouvées sur des sources secondaires ne sont pas utilisées.
- **LFHM Megève** : même règle ; VAC primaire identifiée, aucune fréquence secondaire promue sans extraction primaire fiable.
- **LFHZ Sallanches-Mont-Blanc** : `excluded_closed_aerodrome`, fermé à toute circulation aérienne depuis le 1er septembre 2020.

LFKA et LFHM portent le statut `excluded_scope_unverified_primary`. Cette exclusion est volontaire pour la v0.2 et ne prétend pas que ces terrains n'ont pas de fréquence active.

### Aviation Suisse

Six mémoires sont recoupées publiquement :

- Lausanne LSGL AD : 123.205 MHz ;
- Lausanne APCH INFO : 118.830 MHz ;
- Sion Ground : 121.705 MHz ;
- Sion Tower : 118.275 MHz ;
- Sion ATIS : 130.630 MHz ;
- Sion Approach : 126.825 MHz.

Les fréquences de handling Sion 131.475 / 131.670 / 131.955 MHz et les aides de radionavigation 110.7 / 112.15 MHz restent exclues.

**LSGG Genève-aéroport** est maintenant `excluded_scope_unverified_primary` pour la v0.2 : l'aéroport et le cycle courant sont documentés sur des sources officielles, mais le tableau radio opérationnel primaire n'est pas publiquement extractible avec un niveau de confiance suffisant dans ce workflow. Les fréquences trouvées sur des sources secondaires ne sont donc pas importées. Genève Information 126.350 MHz reste couverte une seule fois dans le bloc transfrontalier.

### Lacs et navigation

Le bloc reste à zéro mémoire. Aucun plan maritime général n'est transposé au Léman, l'AIS suisse reste exclu et aucune fréquence publique générale suffisamment vérifiée n'a été retenue pour Annecy, Bourget ou Aiguebelette.

### Satellites FM

Trois descendantes sont conservées :

- SO-50 : 436.795 MHz ;
- AO-91 : 145.960 MHz, utilisation limitée aux passages éclairés ;
- AO-123 : 435.400 MHz.

Les montantes restent des métadonnées et ne deviennent jamais des mémoires séparées. Le statut opérationnel des satellites doit être recontrôlé juste avant publication.

## Candidat interne

`tools/build_annecy_internal_candidate.py` assemble **65 mémoires** :

- 16 PMR446 ;
- 6 APRS/ISS ;
- 3 satellites FM ;
- 2 canaux d'appel ;
- 19 radioamateur France ;
- 2 radioamateur Suisse ;
- 11 aviation France / bassin genevois ;
- 6 aviation Suisse.

Le résultat reste sous `research/annecy-alpes-leman-v0.2/generated/`, dossier ignoré par Git, avec `public_export_allowed: false` et `Duplex=off` partout.

## Clôture du périmètre aviation v0.2

La recherche de fréquences fixes est désormais considérée comme **close pour la v0.2**. LFKA, LFHM et LSGG sont des omissions documentées plutôt que des lignes remplies à partir de données secondaires. Le pack pourra les intégrer dans une version future si une source primaire exploitable devient disponible.

La porte `pending_airfields` est donc `passed_scope_closed` et ne contient plus d'élément en attente.

## Portes encore bloquantes avant publication

`aviation-operational-gates.json` maintient `public_release_allowed: false`. Restent à effectuer au moment de la publication :

1. briefing NOTAM France via SOFIA-Briefing ;
2. briefing NOTAM Suisse via Skybriefing ;
3. recontrôle du statut opérationnel des satellites FM.

Ces contrôles sont dynamiques et ne doivent pas être déclarés définitivement valides plusieurs jours à l'avance.

## Tests

Depuis la racine :

```powershell
python tests\test_annecy_research.py
python tests\test_annecy_aviation_lakes.py
python tests\test_annecy_airac08.py
python tests\test_annecy_internal_candidate.py
```

Le candidat public Annecy v0.2 n'est toujours pas généré ni publié.
