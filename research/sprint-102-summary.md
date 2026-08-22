# Sprint 102 — Grand Est v0.3 radio scope + internal candidate

Date : 2026-08-22

## Base figée

- Grand Est v0.2 : **59 RX** ;
- aviation : **19** mémoires AIRAC 08/26 ;
- radio régionale historique : 16 mémoires / 8 relais paired-RX ;
- SHA-256 public v0.2 : `a50416bd8a88af249bb691daa657ffd4b578daf1324bd0ca4dd632a2f1a0e5c1` ;
- version publique immuable.

## Recherche radio

Trois passes ont fermé un scope analogique non exhaustif sans mutation publique.

La v0.2 n'est pas reconduite aveuglément : F1ZAX est différé car l'inventaire REF courant le classe C4FM ; F5ZBD est exclu tant que les sources locales le signalent hors service / en mise à niveau ; F1ZBU est exclu du scope analogique car le service courant est numérique.

Le scope retenu ajoute notamment F5ZUD, F1ZUV, F5ZAW, F5ZYS, les crossbands Ardennes/Meuse validés, F5ZDJ, F1ZDA, F1ZBV et les relais Moselle F1ZFL/F5ZCC/F1ZJS.

La fréquence `432.5375 MHz`, commune à F1ZEK, F5ZFT, F1ZGN et F1ZGP, est stockée une seule fois. F1ZCV partage exactement la paire RF de F5ZAU et ne crée donc aucun delta RF.

Scope radio final pour cette version : **41 RF régionales uniques**.

## Candidat déterministe

Le builder `tools/build_grand_est_v03_candidate.py` reconstruit d'abord la v0.2 et exige son SHA historique exact avant de créer le candidat.

Candidat interne figé :

- **84 RX** au total ;
- **19 aviation** ;
- **41 radio régionales** ;
- SHA-256 : `45aef8547a701e7541e620fa9a2d8394595576921e793b75238146ff6e42e720` ;
- RX-only, RF/noms/locations uniques, limite 200 respectée ;
- `public_export_allowed=false` ;
- aucune v0.3 publique créée.

## Prochaine gate

Revalidation aviation du cycle applicable. AIRAC 08/26 est valable jusqu'au **2 septembre 2026 inclus** ; à partir du **3 septembre 2026**, toute révision doit utiliser AIRAC 09/26.

Ensuite : checklist de revue, publication gates, puis seulement une éventuelle publication immuable v0.3.
