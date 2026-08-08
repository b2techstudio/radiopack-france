# Changelog

## 0.10.0 - 2026-08-08

- Ajout de quatre fréquences aviation Sion recoupées sur le site officiel de l'aéroport : GND 121,705 MHz, TWR 118,275 MHz, ATIS 130,630 MHz et APP 126,825 MHz.
- Maintien hors candidat des fréquences de handling Sion 131,475 / 131,670 / 131,955 MHz et des aides de radionavigation 110,7 / 112,15 MHz.
- Passage du bloc aviation Suisse de 2 à 6 mémoires et du candidat interne de 57 à 61 mémoires.
- Reclassement de Sallanches-Mont-Blanc LFHZ en `excluded_closed_aerodrome` : fermeture officielle à toute circulation aérienne effective depuis le 1er septembre 2020.
- Réduction de la liste aviation encore à recouper à Chambéry LFLB, Albertville LFKA, Megève LFHM et Genève LSGG.
- Ajout d'un fichier `aviation-operational-gates.json` séparant validation des fréquences et contrôles dynamiques de pré-publication.
- Maintien des portes NOTAM France (SOFIA-Briefing), NOTAM Suisse (Skybriefing) et statut satellites en attente d'un contrôle daté au moment de la publication.
- Extension des tests AIRAC et du candidat interne pour interdire la réintroduction de Sallanches, des fréquences Sion exclues et de toute donnée non validée.
- Aucun changement des téléchargements publics Annecy, du générateur public ou du statut « En préparation ».

## 0.9.0 - 2026-08-08

- Revalidation partielle du bloc aviation Annecy–Alpes–Léman sur le cycle AIRAC 08/26 effectif depuis le 6 août 2026.
- Ajout de sept mémoires aviation France / bassin genevois recoupées publiquement : Annecy-Meythet, Annemasse, Grenoble-Le Versoud, Grenoble-Alpes-Isère et Genève Information.
- Ajout de deux mémoires Lausanne-La Blécherette recoupées sur le site officiel de l'exploitant : 123,205 MHz et 118,830 MHz.
- Conservation du pré-inventaire AIRAC 07/26 comme historique, avec interdiction explicite de l'utiliser dans l'assembleur.
- Maintien hors candidat de Chambéry, Albertville, Megève, Sallanches, Genève-aéroport et Sion tant que les données courantes ne sont pas suffisamment recoupées publiquement.
- Passage du candidat interne de 48 à 57 mémoires, toutes en réception seule avec `Duplex=off`.
- Ajout du test `tests/test_annecy_airac08.py` et extension des tests du candidat interne aux blocs aviation.
- Aucun changement des téléchargements publics Annecy, du générateur public ou du statut « En préparation ».

## 0.8.0 - 2026-08-04

- Ajout de SO-50, AO-91 et AO-123 dans un inventaire satellite FM de recherche.
- Conservation exclusive des liaisons descendantes comme mémoires RX ; les montantes restent des métadonnées.
- Exclusion prudente de PO-101, CAS-3H, IO-86, RS95S et TEVEL2 du candidat interne.
- Finalisation d'un plan mémoire provisoire de 48 mémoires validées.
- Ajout d'un assembleur interne qui refuse l'aviation non revalidée, les lacs et les lignes suisses non confirmées.
- Génération locale d'un JSON et d'un CSV internes marqués `public_export_allowed: false` dans un dossier ignoré par Git.
- Ajout du test `tests/test_annecy_internal_candidate.py` et de son exécution dans GitHub Actions.
- Aucun changement du générateur public, des téléchargements Annecy ou du statut « En préparation ».

## 0.7.1 - 2026-08-04

- Correction de la modélisation des fréquences ISS en distinguant explicitement liaison montante et liaison descendante.
- Voix équipage en Région 1 : montée 145,200 MHz et descente mondiale 145,800 MHz.
- Répéteur vocal croisé : montée 145,990 MHz avec CTCSS 67 Hz et descente 437,800 MHz.
- Packet/APRS VHF sur 145,825 MHz dans les deux sens et UHF sur 437,825 MHz dans les deux sens lorsque ces modes sont actifs.
- Confirmation de 437,550 MHz comme fréquence descendante SSTV utilisée lors de campagnes ARISS 2026 ; certaines autres campagnes peuvent utiliser 145,800 MHz.
- Conservation exclusive des fréquences descendantes dans les mémoires RX publiques ; les montantes restent des métadonnées documentaires.
- Ajout de tests empêchant l'export de 145,200 MHz et 145,990 MHz comme mémoires de réception séparées.
- Régénération du CSV national APRS/ISS sans changement du nombre de mémoires.

## 0.7.0 - 2026-08-04

- Ajout d'un pré-inventaire aviation France de 11 fréquences uniques pour Annecy–Alpes–Léman v0.2.
- Organisation des fréquences d'Annecy, Annemasse, Chambéry, Grenoble-Le Versoud, Grenoble-Alpes-Isère et Genève Information.
- Marquage obligatoire de toutes les lignes aviation pour revalidation à partir de l'AIRAC 08/26 du 6 août 2026.
- Maintien d'Albertville, Megève et Sallanches en attente d'extraction officielle.
- Ajout des conclusions officielles sur la navigation des lacs d'Annecy, du Bourget et du Léman.
- Exclusion du plan maritime de 57 canaux, de l'AIS suisse et des réseaux professionnels concédés autour de 173 MHz.
- Conservation du canal 16 suisse comme cas conditionnel de recherche, sans intégration au pack public.
- Ajout du test `tests/test_annecy_aviation_lakes.py` et de son exécution dans GitHub Actions.
- Aucun changement du générateur public, des CSV, du PDF ou du statut « En préparation » de la v0.2.

## 0.6.0 - 2026-08-04

- Ajout de l'inventaire de recherche radioamateur France pour Annecy–Alpes–Léman v0.2.
- Recensement de 19 fréquences analogiques uniques dans l'Ain, l'Isère, la Savoie et la Haute-Savoie.
- Fusion de quatre fréquences partagées afin d'éviter les doublons dans le futur plan mémoire.
- Ajout d'un inventaire séparé de huit candidats suisses pour Genève, Vaud et Valais.
- Validation actuelle de HB9G 145,725 MHz et 439,100 MHz ; les autres candidats suisses restent en attente de recoupement.
- Confirmation des conflits F1ZJV et F1ZYT, maintenus hors production.
- Ajout du test `tests/test_annecy_research.py` et de son exécution dans GitHub Actions.
- Aucun changement du générateur public, des CSV ou du statut « En préparation » de la v0.2.

## 0.5.1 - 2026-08-04

- Reclassification publique d'Annecy & Haute-Savoie v0.1 comme aperçu historique incomplet.
- Retrait des liens directs vers les CSV et PDF Annecy v0.1 des pages publiques.
- Renommage de la prochaine zone en Annecy–Alpes–Léman.
- Passage du statut public à « En préparation » pour la future v0.2.
- Mise à jour de l'accueil, de la liste des régions, des téléchargements et de la page des versions.
- Adaptation du composant de carte régionale aux packs non disponibles.
- Ajout de contrôles empêchant la republication accidentelle des liens Annecy v0.1.
- Ajout d'une base de recherche structurée pour Annecy–Alpes–Léman v0.2.

## 0.5.0 - 2026-08-04

- Ajout des URL canoniques et des metadonnees Open Graph / Twitter.
- Ajout des donnees structurees WebSite en JSON-LD.
- Ajout du manifeste web et du lien de sitemap.
- Ajout des routes dynamiques `robots.txt` et `sitemap.xml`.
- Ajout d'une page 404 personnalisee compatible Cloudflare Pages.
- Ajout de la page publique "Etat des packs".
- Mise a jour du bouton principal du menu pour les deux regions disponibles.
- Ajout d'un menu mobile accessible.
- Ajout des en-tetes de securite et de cache Cloudflare Pages.
- Ajout de redirections permanentes pour les anciens téléchargements Normandie.
- Ajout d'une integration continue GitHub Actions pour tester les CSV et compiler Astro.
- Ajout d'un test automatique des fichiers de production.

## 0.4.0 - 2026-08-04

- Publication du premier pack Annecy & Haute-Savoie v0.1.0.
- Ajout de 36 memoires en reception seule.
- Ajout de l'aviation d'Annecy-Meythet et d'Annemasse.
- Ajout de neuf sorties analogiques uniques en Haute-Savoie, dans l'Ain et en Savoie.
- Regroupement des frequences de transpondeurs partagees afin d'eviter les doublons.
- Ajout du CSV regional, du CSV des relais et du guide PDF.
- Mise a jour de l'accueil, des regions, des telechargements, du generateur et des tests.

## 0.3.1 - 2026-08-04

- Ajout du relais F6ZCE de Pré-en-Pail / Mont des Avaloirs.
- Fréquence de sortie : 145,700 MHz, réception seule.
- Pack Normandie porté à 139 mémoires.
- Liste des relais portée à 15 mémoires.
- Mise à jour du site, des tests et du guide PDF.

## 0.3.0 - 2026-08-04

- Ajout des canaux d'appel FM 145,500 MHz et 433,500 MHz en reception seule.
- Ajout de 14 sorties de relais ou voies de transpondeurs analogiques verifies en Normandie.
- Organisation du pack par plages fixes de memoires.
- Pack Normandie porte a 138 memoires.
- Ajout d'un guide PDF telechargeable.
- Ajout d'un export CSV specifique aux relais analogiques normands.
- Mise a jour du generateur et des tests pour gerer les intervalles de memoires.

## 0.2.0 - 2026-08-04

- Ajout de la VHF marine, APRS/ISS et de l'aviation normande.
- Pack Normandie porte a 122 memoires.

## 0.1.0 - 2026-08-04

- Premiere base PMR446 et generateur CSV CHIRP.
