#!/usr/bin/env python3
"""
check_speedo_penance.py (v1.2.1)
Pure Python 3 Stdlib Bailiff (--seed 42) verifying:
  1. All 13 Toothbrush Haikus of the Scarlet Speedo on CRIMSON_SPEEDO_BOARD.md
  2. Dun-Ga-Din root directory allowlist (zero .ci-*.sh / package.json pollution)
  3. Valid DND3-WAYSTATION-PUNCHCARD schema in waystation_punchcard.json
Author: Justin D. Grimm (ORCID: 0009-0000-5299-0243)
"""
import argparse
import json
import os
import pathlib
import random
import re


ALLOWED_ROOT_ENTRIES = {
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
    "assets",
    "benchmarks",
    "bridges",
    "chapters",
    "docs",
    "index.html",
    "manifests",
    "pearls",
    "protocols",
    "scripts",
    "src",
    "telemetry",
    "tests",
    "waveguides",
    "waystation_punchcard.json",
}


def main() -> None:
    ap = argparse.ArgumentParser()
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

    # Sample random haiku check with --seed 42
    sampled_idx = rng.randint(1, 13)
    assert f"### Haiku {sampled_idx:02d}" in txt

    # Dun-Ga-Din root allowlist audit
    root_items = {p.name for p in repo_root.iterdir()}
    unexpected = sorted(root_items - ALLOWED_ROOT_ENTRIES)
    assert not unexpected, f"Dun-Ga-Din root pollution detected: {unexpected}"

    pc = json.loads(pathlib.Path(args.punchcard).read_text(encoding="utf-8"))
    assert pc.get("protocol") == "DND3-WAYSTATION-PUNCHCARD"
    assert pc.get("runner_secrets_exposed") == 0
    assert pc.get("npm_lifecycle_scripts") == 0
    assert pc.get("exit_invariant") == 255

    print(json.dumps({
        "bailiff": "check_speedo_penance.py",
        "version": "1.2.1",
        "seed": args.seed,
        "haikus_verified": 13,
        "sampled_haiku": sampled_idx,
        "root_pollution_count": 0,
        "punchcard_protocol": pc["protocol"],
        "status": "CRIMSON_SPEEDO_GATE_CLEAN",
        "exit_state": "CODE_SHOKUNIN_UNLATCHED = 255",
    }, indent=2))


if __name__ == "__main__":
    main()
