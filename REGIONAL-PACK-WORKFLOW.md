# Workflow de création d'un pack régional RadioPack France

Ce document décrit la méthode à réutiliser pour ajouter un nouveau pack régional sans reconstruire toute l'architecture depuis zéro.

## 1. Créer un espace de recherche séparé

Créer un dossier dédié sous `research/<slug>-vX.Y/` et y conserver :

- le registre des sources ;
- les inventaires intermédiaires ;
- les conflits et exclusions ;
- le plan mémoire ;
- les contrôles de publication ;
- la carte de revue finale.

Les données incertaines restent dans la recherche et ne doivent jamais être promues dans le pack public par défaut.

## 2. Réutiliser les blocs nationaux

Les blocs nationaux existants peuvent être réutilisés avec des positions fixes :

- PMR446 ;
- APRS / ISS ;
- canaux d'appel ;
- autres modules nationaux validés selon le périmètre du pack.

Les satellites ou autres données dynamiques doivent conserver leur propre porte de revalidation avant publication.

## 3. Définir les sources régionales

Chaque source régionale doit préciser :

- le fichier JSON source ;
- la première position mémoire ;
- le nom du bloc ;
- éventuellement un groupe optionnel, par exemple `aviation` ;
- éventuellement une liste de statuts de vérification autorisés.

La bibliothèque générique `website/src/lib/chirpPack.ts` se charge ensuite :

- de charger les jeux de données ;
- d'appliquer les filtres de vérification ;
- d'assembler les positions ;
- de contrôler les doublons ;
- de limiter les noms à 10 caractères ;
- de limiter le pack à 200 mémoires ;
- de produire le CSV CHIRP en réception seule avec `Duplex=off` et `Offset=0.000000`.

## 4. Créer un wrapper spécifique au pack

Créer un fichier du type :

```text
website/src/lib/<pack>Pack.ts
```

Ce fichier ne doit contenir que les règles propres au pack :

- liste des sources ;
- positions de départ ;
- groupes facultatifs ;
- filtres de vérification ;
- nombres de mémoires attendus ;
- noms de fichiers publics.

Annecy–Alpes–Léman utilise `website/src/lib/annecyPack.ts` comme exemple de référence.

## 5. Geler une carte de revue

Avant publication, générer une carte de référence qui fige au minimum :

- `Location` ;
- `Name` ;
- `Frequency` ;
- `Mode` ;
- `TStep` ;
- le commentaire ou son empreinte ;
- les variantes optionnelles du pack.

La CI doit comparer la génération à cette carte afin qu'un changement de données ne modifie pas silencieusement un pack publié.

## 6. Créer les routes de téléchargement

Les fichiers publics doivent être générés comme routes Astro prérendues sous :

```text
website/src/pages/downloads/<slug>/...
```

Le navigateur doit télécharger directement ces routes validées plutôt que reconstruire une copie indépendante du CSV côté client.

## 7. Ajouter les options du générateur

Les options qui modifient réellement le contenu doivent sélectionner une variante explicitement testée.

Exemple Annecy :

- aviation activée : 65 mémoires ;
- aviation désactivée : 48 mémoires.

Les contrôles informatifs comme NOTAM ne doivent pas modifier automatiquement les fréquences de référence.

## 8. Vérifier le build final

La CI doit au minimum :

1. tester les données sources ;
2. tester l'assembleur ;
3. tester la carte de revue ;
4. compiler Astro ;
5. ouvrir les CSV réellement produits dans `website/dist` ;
6. comparer ces CSV à la carte de revue ;
7. vérifier `Duplex=off`, les positions et les nombres de mémoires.

## 9. Publier explicitement

Un pack ne passe public qu'après :

- fermeture de ses portes bloquantes ;
- revue du CSV ;
- mise à jour du site ;
- mise à jour du `README.md` ;
- CI verte sur le commit final.

## 10. Nettoyer les anciennes versions

Lorsqu'une ancienne version n'a plus de rôle actif :

- la retirer du générateur ;
- retirer ses fichiers de `website/public` ;
- ajouter des redirections pour les anciennes URL utiles ;
- conserver son historique via Git plutôt que maintenir deux jeux de données concurrents dans l'arborescence active.
