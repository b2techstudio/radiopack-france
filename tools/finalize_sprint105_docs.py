#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

readme_path = ROOT / "README.md"
readme = readme_path.read_text(encoding="utf-8")
readme = readme.replace(
    "**État courant : Sprint 104 / 0.21.92 — Grand Est v0.4 est publiée et immuable à 97 RX, dont 19 aviation, 41 radio régionales et 13 VHF de navigation intérieure.**",
    "**État courant : Sprint 105 / 0.21.93 — Île-de-France v0.4 est publiée et immuable à 64 RX, dont 18 aviation, 15 radio régionales et 7 VHF de navigation intérieure.**",
)
readme = readme.replace(
    "- **Île-de-France v0.3** — 57 mémoires RX, dont 18 aviation ;\n- **Île-de-France v0.2** — 58 mémoires RX, historique immuable ;",
    "- **Île-de-France v0.4** — 64 mémoires RX, dont 18 aviation et 7 VHF navigation intérieure ;\n- **Île-de-France v0.3** — 57 mémoires RX, historique immuable ;\n- **Île-de-France v0.2** — 58 mémoires RX, historique immuable ;",
)
readme = readme.replace(
    "Les variantes par défaut représentent **1568 mémoires RX cumulées** dans le catalogue public.",
    "Les variantes par défaut représentent **1575 mémoires RX cumulées** dans le catalogue public.",
)
s105 = """## Sprint 105 — Île-de-France v0.4 publiée

Île-de-France v0.4 est publiée à **64 RX** à partir de la v0.3 immuable de 57 RX. Le delta est exclusivement constitué de **7 mémoires VHF de navigation intérieure** : canal 10 en simplex et canaux 18, 20 et 22 en paired RX. Aviation : **18, delta 0** ; radio régionale : **15, delta 0**.

Les affectations locales 2026 publiées par VNF pour le PCC de Vives-Eaux sont Varennes 22, Champagne 18, La Cave 22, Vives-Eaux 20 et Le Coudray 22. Le canal 69 n'est pas promu faute de base 2026 suffisante pour une mémoire permanente ; aucun canal 16 maritime n'est ajouté.

SHA public : `14e1d1d95b38ef44d01b9cccb989a3f1567153ac64875594cc24bd4b57a1cdc2`. Les v0.3/57 et v0.2/58 restent historiques et immuables. AIRAC 08/26 reste applicable jusqu'au 2 septembre 2026 inclus ; toute nouvelle révision aviation à partir du 3 septembre exige AIRAC 09/26.

"""
if "## Sprint 105 —" not in readme:
    readme = readme.replace("## Sprint 104 — Grand Est v0.4 publiée\n", s105 + "## Sprint 104 — Grand Est v0.4 publiée\n")
readme = readme.replace(
    "Après les publications BFC, Centre et Île-de-France v0.3, les autres régions métropolitaines encore en v0.2 seront traitées progressivement.",
    "Après les publications BFC, Centre, Île-de-France v0.4 et Grand Est v0.4, les autres régions métropolitaines encore en v0.2 seront traitées progressivement.",
)
readme = readme.replace(
    "python tests\\test_idf_v03_publication.py\n",
    "python tests\\test_idf_v03_publication.py\npython tests\\test_idf_v04_publication.py\npython tests\\test_sprint105_state_sync.py\n",
)
readme_path.write_text(readme, encoding="utf-8")

status_path = ROOT / "PROJECT_STATUS.md"
status = status_path.read_text(encoding="utf-8")
status = status.replace("Sprint courant : **104**", "Sprint courant : **105**")
status = status.replace("État logique : **0.21.92**", "État logique : **0.21.93**")
status = status.replace("Résumé courant : `research/sprint-104-summary.md`.", "Résumé courant : `research/sprint-105-summary.md`.")
status = status.replace(
    "- Île-de-France v0.3 : **57 mémoires RX**, dont **18 aviation**, publiée et immuable ; v0.2 **58 RX** historique immuable.",
    "- Île-de-France v0.4 : **64 mémoires RX**, dont **18 aviation**, **15 radio régionales** et **7 VHF navigation intérieure**, publiée et immuable ; v0.3 **57 RX** et v0.2 **58 RX** historiques immuables.",
)
s105_status = """## Sprint 105 — Île-de-France v0.4 publiée

Île-de-France v0.4 est publiée et figée à **64 RX** : **18 aviation**, **15 radio régionales** et **7 VHF navigation intérieure**. SHA public : `14e1d1d95b38ef44d01b9cccb989a3f1567153ac64875594cc24bd4b57a1cdc2`.

Le bloc fluvial retient les canaux **10, 18, 20 et 22** sur les emplacements **120–126**. Les canaux 18/20/22 sont représentés en paired RX sur leurs deux fréquences distinctes. Les affectations actuelles du PCC Vives-Eaux 2026 sont documentées par VNF. Le canal 69 n'est pas promu et aucun canal 16 maritime n'est ajouté.

L'aviation reste à **18 mémoires, delta 0**, héritée de v0.3. AIRAC 08/26 est applicable jusqu'au **2 septembre 2026 inclus** ; toute nouvelle révision aviation à partir du **3 septembre 2026** exige AIRAC 09/26.

Checklist : **12/12** ; publication gates : **0 blocker** ; candidat et CSV public byte-identiques. Les v0.3/57 et v0.2/58 restent historiques et immuables.

"""
if "## Sprint 105 —" not in status:
    status = status.replace("## Sprint 104 — Grand Est v0.4 publiée\n", s105_status + "## Sprint 104 — Grand Est v0.4 publiée\n")
status_path.write_text(status, encoding="utf-8")

changelog_path = ROOT / "CHANGELOG.md"
changelog = changelog_path.read_text(encoding="utf-8")
s105_change = """## 0.21.93 - 2026-08-22

**Sprint 105** — Île-de-France v0.4 publiée et figée à **64 mémoires RX**.

- base v0.3/57 vérifiée et conservée immuable ;
- +7 mémoires VHF de navigation intérieure : canal 10 et paired RX 18/20/22 ;
- 18 aviation inchangées, delta 0 ;
- 15 radio régionales inchangées, delta 0 ;
- canal 69 non promu ; aucun canal 16 maritime ajouté ;
- checklist **12/12**, publication gates **0 blocker** ;
- candidat/public byte-identiques ;
- SHA-256 : `14e1d1d95b38ef44d01b9cccb989a3f1567153ac64875594cc24bd4b57a1cdc2` ;
- v0.3/57 et v0.2/58 conservées historiques et immuables ;
- état projet synchronisé sur Sprint 105 / 0.21.93.

"""
if "## 0.21.93 - 2026-08-22" not in changelog:
    changelog = changelog.replace("# Changelog\n\n", "# Changelog\n\n" + s105_change)
changelog_path.write_text(changelog, encoding="utf-8")

print("Sprint 105 docs synchronized")
