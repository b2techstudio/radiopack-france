#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"Missing replacement anchor: {label}")
    return text.replace(old, new, 1)

with tempfile.TemporaryDirectory(prefix="annecy-v04-finalize-") as td:
    subprocess.run([sys.executable, str(ROOT / "tools/build_annecy_v04_candidate.py"), "--output-dir", td], cwd=ROOT, check=True)
    manifest = json.loads((Path(td) / "annecy-v0.4-manifest.json").read_text(encoding="utf-8"))

# Machine state
state_path = ROOT / "research/project-resume-state.json"
state = json.loads(state_path.read_text(encoding="utf-8"))
state["updated"] = "2026-08-15"
state["current_sprint"] = 91
state["state_version"] = "0.21.80"
state["active_work"] = {
    "pack": "Bretagne",
    "target_version": "0.3",
    "status": "airac09_future_handoff_prepared_waiting_effective_date",
    "public_base_version": "0.2",
    "public_base_memory_count": 151,
    "candidate_memory_count": 151,
    "candidate_memory_delta": 0,
    "airac_current": "08/26",
    "airac_current_until_inclusive": "2026-09-02",
    "airac_next_required": "09/26",
    "airac_next_effective_from": "2026-09-03",
    "publication_allowed_before_airac09_revalidation": False,
    "handoff": "research/bretagne-v0.3/airac09-handoff.json"
}
state["annecy_v0_4_research"] = {
    "status": "deterministic_candidate_ready_not_public",
    "based_on_public_version": "0.3",
    "public_version_remains": "0.3",
    "candidate_memory_count": manifest["full_memory_count"],
    "candidate_without_aviation_memory_count": manifest["without_aviation_memory_count"],
    "candidate_memory_delta": 1,
    "added_frequency_mhz": 50.5375,
    "added_memory_name": "ZTH-6M",
    "full_candidate_sha256": manifest["full_sha256"],
    "without_aviation_candidate_sha256": manifest["without_aviation_sha256"],
    "compatibility_review": "research/annecy-alpes-leman-v0.4/compatibility-and-source-review.json",
    "builder": "tools/build_annecy_v04_candidate.py",
    "published": False
}
state["normandie_v0_5_latest_refresh"] = {
    "status": "current_sources_refreshed_zero_delta_field_blocked",
    "candidate_memory_count": 142,
    "candidate_memory_delta": 0,
    "known_potential_ceiling_excluding_f6zes": 147,
    "field_required": ["R3_F1ZBX", "F5ZHA"],
    "source_watch": ["F1ZOV", "F6ZES"],
    "evidence": "research/normandie-v0.5/sprint90-source-refresh.json"
}
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Summaries
write("research/sprint-89-summary.md", f"""# Sprint 89 — Annecy–Alpes–Léman v0.4 compatibility closure\n\nDate : 2026-08-15\nÉtat : 0.21.78\n\nLe gate qui maintenait F1ZTH 50.5375 MHz hors de la v0.3 est levé pour une future v0.4 : le manuel UV-K5 constructeur/FCC couvre la réception 50–600 MHz et le pilote CHIRP UV-K5 stock déclare la bande 50–76 MHz. Le REF courant publie F1ZTH actif en analogique FM.\n\nCandidat déterministe non public : **77 RX / 60 sans aviation**, soit **+1 RF** depuis la v0.3 publique 76/59.\n\n- ajout : `ZTH-6M` 50.537500 MHz, FM, RX-only ;\n- v0.3 reste immuable ;\n- aucune UHF ADRASEC non publiée n'est inférée ;\n- SHA candidat complet : `{manifest['full_sha256']}` ;\n- SHA candidat sans aviation : `{manifest['without_aviation_sha256']}`.\n\nPreuve : `research/annecy-alpes-leman-v0.4/compatibility-and-source-review.json`. Builder : `tools/build_annecy_v04_candidate.py`.\n""")
write("research/sprint-90-summary.md", """# Sprint 90 — Normandie v0.5 source refresh\n\nDate : 2026-08-15\nÉtat : 0.21.79\n\nRecontrôle des dossiers encore ouverts : **candidat 142 RX, delta 0, zéro promotion**.\n\n- R3/F1ZBX et F5ZHA sont désormais explicitement classés `field_validation_required` : aucun travail web supplémentaire ne peut fermer ces gates ;\n- F1ZOV reste `En Maintenance` chez l'opérateur local F6KFW malgré le REF général actif ;\n- F6ZES reste identifié à Sourdeval sans fréquence ni mode exploitables publiquement ;\n- plafond potentiel conservé à 147 hors F6ZES ;\n- aucune v0.5 publique.\n\nPreuve : `research/normandie-v0.5/sprint90-source-refresh.json`.\n""")
write("research/sprint-91-summary.md", """# Sprint 91 — Bretagne v0.3 AIRAC 09/26 handoff\n\nDate : 2026-08-15\nÉtat : 0.21.80\n\nLe SIA maintient AIRAC 08/26 courant jusqu'au **2 septembre 2026 inclus**. AIRAC 09/26 ne peut donc pas être utilisé comme preuve actuelle avant le **3 septembre 2026**.\n\n- candidat Bretagne v0.3 : **151 RX, delta 0** ;\n- publication v0.3 interdite avant revalidation AIRAC 09/26 si elle intervient à partir du 3 septembre ;\n- runbook AIRAC09 préparé ;\n- les six dossiers non-AIRAC ouverts restent inchangés ;\n- v0.2 publique reste immuable.\n\nHandoff : `research/bretagne-v0.3/airac09-handoff.json`.\n""")

# PROJECT_STATUS
p = read("PROJECT_STATUS.md")
p = replace_once(p, "Sprint courant : **88**", "Sprint courant : **91**", "PROJECT sprint")
p = replace_once(p, "État logique : **0.21.77**", "État logique : **0.21.80**", "PROJECT state")
p = replace_once(p, "Résumé courant : `research/sprint-88-summary.md`.", "Résumé courant : `research/sprint-91-summary.md`.", "PROJECT summary")
p = replace_once(p, "- Annecy–Alpes–Léman v0.2 : 65 mémoires RX, variante 48 sans aviation.", "- Annecy–Alpes–Léman v0.3 : **76 mémoires RX**, variante **59 sans aviation**, publiée et immuable.", "PROJECT stale Annecy public line")
insert = f"""## Sprint 91 — Bretagne v0.3 AIRAC09 handoff\n\nAIRAC 08/26 reste courant jusqu'au 2 septembre 2026 inclus. Le handoff 09/26 est préparé pour le 3 septembre ; candidat **151 RX, delta 0**, aucune publication anticipée.\n\n## Sprint 90 — Normandie v0.5 source refresh\n\nCandidat **142 RX, delta 0**. R3/F1ZBX et F5ZHA exigent du terrain ; F1ZOV reste en maintenance locale ; F6ZES reste sans RF/mode public exploitable.\n\n## Sprint 89 — Annecy v0.4 candidat\n\nLe gate de compatibilité 50 MHz est levé. Candidat déterministe non public **77 RX / 60 sans aviation**, avec `ZTH-6M` 50.5375 MHz. La v0.3 publique reste immuable.\n\n"""
p = replace_once(p, "## Sprint 88 — Annecy v0.3 publiée\n", insert + "## Sprint 88 — Annecy v0.3 publiée\n", "PROJECT insert")
write("PROJECT_STATUS.md", p)

# README
r = read("README.md")
r = replace_once(r, "**État courant : Sprint 88 / 0.21.77 — Annecy–Alpes–Léman v0.3 est publiée et immuable à 76 mémoires RX (59 sans aviation), +11 RF uniques par rapport à v0.2.**", "**État courant : Sprint 91 / 0.21.80 — Annecy v0.4 candidat 77/60 non public ; Normandie v0.5 142/delta 0 bloquée terrain ; Bretagne v0.3 151/delta 0 en attente AIRAC 09/26.**", "README status")
r = replace_once(r, "## État actuel — Sprint 88 / 0.21.77", "## État actuel — Sprint 91 / 0.21.80", "README heading")
r = replace_once(r, "Recherche : **Annecy–Alpes–Léman v0.3 = 76 mémoires RX / 59 sans aviation, +11 RF uniques**, premier candidat interne paired RX non public ; plafond conditionnel 77 si F1ZTH 50.5375 MHz franchit le gate de compatibilité UV-K5/firmware. Normandie v0.5 reste à **142 RX**, delta 0, en attente de terrain R3/F5ZHA et de nouvelles sources F1ZOV/F6ZES. Bretagne v0.3 reste à **151 RX**, delta 0 ; sa prochaine transition aviation reste AIRAC 09/26 au 3 septembre 2026.", "Recherche : **Annecy v0.4 = 77 RX / 60 sans aviation, +1 RF**, candidat déterministe non public après validation du 50 MHz stock UV-K5/CHIRP. Normandie v0.5 reste à **142 RX**, delta 0 : R3/F5ZHA exigent du terrain, F1ZOV/F6ZES restent en veille source. Bretagne v0.3 reste à **151 RX**, delta 0, avec handoff AIRAC 09/26 préparé pour le 3 septembre 2026.", "README research")
r = replace_once(r, "`research/sprint-85-summary.md` et `research/sprint-86-summary.md`.", "`research/sprint-85-summary.md`, `research/sprint-86-summary.md`, `research/sprint-89-summary.md`, `research/sprint-90-summary.md` et `research/sprint-91-summary.md`.", "README resume list")
ri = """## Sprint 91 — Bretagne AIRAC 09/26 handoff\n\nHandoff reproductible prêt pour le 3 septembre 2026 ; v0.3 reste à **151 RX, delta 0**, sans publication anticipée.\n\n## Sprint 90 — Normandie v0.5 refresh\n\nCandidat **142 RX, delta 0**. R3/F1ZBX et F5ZHA sont des gates terrain ; F1ZOV reste en maintenance locale et F6ZES sans RF/mode public exploitable.\n\n## Sprint 89 — Annecy v0.4 candidat\n\nLe manuel UV-K5 constructeur/FCC et le pilote CHIRP stock couvrent 50.5375 MHz. Le candidat non public passe à **77 RX / 60 sans aviation** avec `ZTH-6M`, tandis que la v0.3 reste immuable.\n\n"""
r = replace_once(r, "## Sprint 88 — publication Annecy–Alpes–Léman v0.3\n", ri + "## Sprint 88 — publication Annecy–Alpes–Léman v0.3\n", "README insert")
write("README.md", r)

# CHANGELOG
c = read("CHANGELOG.md")
entry = f"""# Changelog\n\n## 0.21.80 - 2026-08-15\n\n- **Sprint 91** : handoff Bretagne v0.3 AIRAC 09/26 préparé ; candidat **151 RX, delta 0**, aucune anticipation avant le 3 septembre.\n\n## 0.21.79 - 2026-08-15\n\n- **Sprint 90** : refresh Normandie v0.5 ; candidat **142 RX, delta 0**, R3/F5ZHA terrain uniquement, F1ZOV maintenance locale, F6ZES RF/mode non résolus.\n\n## 0.21.78 - 2026-08-15\n\n- **Sprint 89** : compatibilité stock UV-K5/CHIRP 50 MHz validée ; candidat Annecy v0.4 non public **77 RX / 60 sans aviation**, +1 RF `ZTH-6M` 50.5375 MHz.\n- SHA candidats : `{manifest['full_sha256']}` / `{manifest['without_aviation_sha256']}`.\n\n"""
if not c.startswith("# Changelog\n\n"):
    raise RuntimeError("Unexpected changelog header")
c = entry + c[len("# Changelog\n\n"):]
write("CHANGELOG.md", c)

print("Sprints 89-91 finalizer complete")
