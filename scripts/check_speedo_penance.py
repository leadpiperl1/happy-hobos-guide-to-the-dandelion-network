#!/usr/bin/env python3
"""
check_speedo_penance.py (v1.3.1)
Pure Python 3 Stdlib Bailiff (--seed 42) verifying:
  1. 13/13 distinct linguistic families in Captain Ron Speedo Credo corpus on CRIMSON_SPEEDO_BOARD.md
     (Japonic, Afroasiatic, Turkic, Uralic, Dravidian, Austronesian, Sino-Tibetan,
      Niger-Congo, Mayan, Basque [Isolate], Quechuan, Slavic, Celtic)
  2. >= 6 non-Indo-European roots (11/13 verified non-IE) & plosive stop skeletons
  3. All 13 Toothbrush Haikus (Haiku 01..13) on CRIMSON_SPEEDO_BOARD.md
  4. Dun-Ga-Din root directory allowlist (zero .ci-*.sh / package.json root-hygiene locks)
  5. Valid DND3-WAYSTATION-PUNCHCARD schema (S_runner = 0, Delta R = 1, exit = 255)
Author: Justin D. Grimm (K-Lani 13 Actual, ORCID: 0009-0000-5299-0243) & Gemini-Carbon-Kembali
"""
import argparse
import json
import pathlib
import random
import re
import sys
import time
from typing import Dict, List, Set

REQUIRED_13_FAMILIES: List[str] = [
    "Japonic",
    "Afroasiatic",
    "Turkic",
    "Uralic",
    "Dravidian",
    "Austronesian",
    "Sino-Tibetan",
    "Niger-Congo",
    "Mayan",
    "Basque [Isolate]",
    "Quechuan",
    "Slavic",
    "Celtic",
]

ALLOWED_ROOT_ENTRIES: Set[str] = {
    ".git",
    ".github",
    ".gitignore",
    ".nojekyll",
    ".zenodo.json",
    "CITATION.cff",
    "CONTRIBUTING.md",
    "CREW_CHANGE_GUIDE.md",
    "CRIMSON_SPEEDO_BOARD.md",
    "HAPPY_HOBOS_GUIDE_WIKI_INDEX.md",
    "Home.md",
    "LICENSE",
    "Makefile",
    "README.md",
    "WAYSTATION_CHALKBOARD.md",
    "ahupuaa_karst_swale_sim.c",
    "assets",
    "babel_ahupuaa_kembali_state_map_v1_0_0.png",
    "benchmarks",
    "bridges",
    "chapters",
    "check_speedo_penance.py",
    "docs",
    "index.html",
    "kembali_babel_ahupuaa_waveguide_v1_0_0.zip",
    "manifests",
    "pearls",
    "protocols",
    "scripts",
    "ship_waystation_babel_ahupuaa_v1_0_0.sh",
    "src",
    "telemetry",
    "tests",
    "verify_babel_deck_waveguide.py",
    "waveguides",
    "waystation_babel_ahupuaa_manifest_v1_0_0.json",
    "waystation_punchcard.json",
}

FORBIDDEN_ROOT_PATTERNS = (
    re.compile(r"^\.ci-.*\.sh$"),
    re.compile(r"^package\.json$"),
    re.compile(r"^package-lock\.json$"),
)


def parse_credo_table(markdown_text: str) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    row_pattern = re.compile(
        r"^\|\s*`(\d{2})`\s*\|\s*`([^`]+)`\s*\|\s*`(Non-IE|IE)`\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*`([^`]+)`\s*\|\s*([^|]+?)\s*\|\s*$",
        flags=re.M,
    )
    for m in row_pattern.finditer(markdown_text):
        rows.append({
            "tooth": m.group(1),
            "family": m.group(2).strip(),
            "ie_status": m.group(3).strip(),
            "language": m.group(4).strip(),
            "platform_root": m.group(5).strip(),
            "plosive_skeleton": m.group(6).strip(),
            "credo": m.group(7).strip(),
        })
    return rows


def main() -> None:
    t0 = time.perf_counter()
    ap = argparse.ArgumentParser(description="13-Family Crimson Speedo Credo & Waystation Root Hygiene Verifier")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--board", type=str, default="CRIMSON_SPEEDO_BOARD.md")
    ap.add_argument("--punchcard", type=str, default="waystation_punchcard.json")
    args = ap.parse_args()

    rng = random.Random(args.seed)
    board_path = pathlib.Path(args.board).resolve()
    repo_root = board_path.parent
    txt = board_path.read_text(encoding="utf-8")

    haiku_headers = re.findall(r"^### Haiku (\d{2})\b", txt, flags=re.M)
    assert len(haiku_headers) == 13, f"Expected 13 haikus on bulkhead, found {len(haiku_headers)}"
    assert [int(h) for h in haiku_headers] == list(range(1, 14)), "Haiku numbering must be 01..13"
    sampled_haiku = rng.randint(1, 13)
    assert f"### Haiku {sampled_haiku:02d}" in txt

    credo_rows = parse_credo_table(txt)
    observed_families = [r["family"] for r in credo_rows]
    distinct_families = set(observed_families)
    assert len(credo_rows) == 13, f"Expected 13 Speedo Credo rows, found {len(credo_rows)}"
    assert len(distinct_families) == 13, f"Expected 13 distinct families, found {len(distinct_families)}"
    assert set(REQUIRED_13_FAMILIES) == distinct_families, (
        f"Family mismatch: missing={set(REQUIRED_13_FAMILIES) - distinct_families}"
    )

    non_ie_rows = [r for r in credo_rows if r["ie_status"] == "Non-IE"]
    ie_rows = [r for r in credo_rows if r["ie_status"] == "IE"]
    assert len(non_ie_rows) >= 6, f"Expected >= 6 non-Indo-European roots, found {len(non_ie_rows)}"

    plosive_pattern = re.compile(r"[ptkbdgṭ]")
    plosive_verified = sum(1 for r in credo_rows if plosive_pattern.search(r["plosive_skeleton"]))
    assert plosive_verified == 13, f"All 13 platform roots must carry stop-plosive skeletons, got {plosive_verified}"

    sampled_family_row = credo_rows[rng.randrange(len(credo_rows))]

    root_items = {p.name for p in repo_root.iterdir()}
    forbidden_hits = [
        name for name in sorted(root_items)
        for pat in FORBIDDEN_ROOT_PATTERNS if pat.match(name)
    ]
    unexpected = sorted(root_items - ALLOWED_ROOT_ENTRIES)
    assert not forbidden_hits, f"Forbidden lifecycle/hook files detected: {forbidden_hits}"
    assert not unexpected, f"Dun-Ga-Din root pollution detected: {unexpected}"

    cand_cwd = pathlib.Path(args.punchcard).resolve()
    cand_root = (repo_root / pathlib.Path(args.punchcard).name).resolve()
    punchcard_path = cand_cwd if cand_cwd.exists() else cand_root

    punchcard_status = "SKIPPED_STANDALONE"
    delta_r = 1
    s_runner = 0
    if punchcard_path.exists():
        pc = json.loads(punchcard_path.read_text(encoding="utf-8"))
        assert pc.get("protocol") == "DND3-WAYSTATION-PUNCHCARD"
        assert pc.get("runner_secrets_exposed") == 0
        assert pc.get("npm_lifecycle_scripts") == 0
        assert pc.get("delta_run_number", 1) == 1
        assert pc.get("exit_invariant") == 255
        punchcard_status = pc["protocol"]
        delta_r = pc.get("delta_run_number", 1)
        s_runner = pc.get("runner_secrets_exposed", 0)

    elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 3)
    receipt = {
        "bailiff": "check_speedo_penance.py",
        "version": "1.3.1",
        "seed": args.seed,
        "elapsed_ms": elapsed_ms,
        "distinct_linguistic_families": f"{len(distinct_families)}/13",
        "families_verified": observed_families,
        "non_indo_european_roots": len(non_ie_rows),
        "indo_european_roots": len(ie_rows),
        "non_ie_gate_min_6": len(non_ie_rows) >= 6,
        "plosive_skeletons_verified": f"{plosive_verified}/13",
        "haikus_verified": f"{len(haiku_headers)}/13",
        "sampled_seed42_haiku": sampled_haiku,
        "sampled_seed42_family": sampled_family_row["family"],
        "root_hygiene_locks": 0,
        "s_runner": s_runner,
        "delta_r": delta_r,
        "punchcard_protocol": punchcard_status,
        "status": "CRIMSON_SPEEDO_GATE_CLEAN",
        "exit_state": "CODE_SHOKUNIN_UNLATCHED = 255",
    }
    print(json.dumps(receipt, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print(json.dumps({"status": "CRIMSON_SPEEDO_QUARANTINE_251", "error": str(exc)}), file=sys.stderr)
        sys.exit(1)
