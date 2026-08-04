# Sources ajoutees au Sprint 5

Verification effectuee le 4 aout 2026.

## Aviation - Annecy et Haute-Savoie

- SIA eAIP AIRAC 07/26, en vigueur du 09/07/2026 au 05/08/2026 :
  https://www.sia.aviation-civile.gouv.fr/produits-numeriques-en-libre-disposition/eaip.html
- Annecy-Meythet LFLP, TWR / AFIS / A-A 118,200 MHz :
  https://www.sia.aviation-civile.gouv.fr/media/dvd/eAIP_09_JUL_2026/FRANCE/AIRAC-2026-07-09/html/eAIP/FR-AD-2.LFLP-fr-FR.html
- Annemasse A-A 125,875 MHz, reference dans ENR 5.5 :
  https://www.sia.aviation-civile.gouv.fr/media/dvd/eAIP_09_JUL_2026/FRANCE/AIRAC-2026-07-09/html/eAIP/FR-ENR-5.5-fr-FR.html

## Relais et transpondeurs analogiques

- REF - liste des relais :
  https://www.r-e-f.org/index.php?Itemid=492&id=1279&option=com_content&view=article
- Derniere mise a jour indiquee par le REF : 13 mai 2026.

Stations ou groupes de sorties inclus :

- F5ZLV - Viuz-la-Chiesaz
- F5ZDT - Leyssard
- F1ZOH - Crozet
- F1ZPY - Apremont
- F6ZJD - Nurieux
- F1ZHE - Montvalezan
- F1ZHG - Albertville
- F5ZGT - Saint-Martin-de-Belleville

Les sorties 432,6500 MHz et 432,5125 MHz sont partagees par plusieurs installations.
RadioPack France les conserve une seule fois dans le CSV afin d'eviter des doublons de scan.

## Regle de publication

Toutes les nouvelles memoires sont configurees en reception seule avec `Duplex=off`.
Les modes numeriques non decodables par le Quansheng UV-K5 ne sont pas inclus.
