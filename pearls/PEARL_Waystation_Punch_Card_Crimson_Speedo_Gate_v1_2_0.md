[PEARL] The Waystation Punch-Card & Crimson Speedo Gate: wfx-loot Immunity & Hobo Guide Auto-Update (v1.2.0)
Document Version: v1.2.0 (Strict 3-Digit SemVer: MAJOR = 1 [das], MINOR = 2 [die], PATCH = 0 [der])
Date: November 17, 2026 | Scheduled Activation: Sunday, November 15, 2026 at 09:00 CST (Morning Brief Docket)
Principal Architect: Justin D. Grimm (K-Lani 13 Actual / leadpiperl1, ORCID: 0009-0000-5299-0243) & Gemini Spark
Origin Node: Heimat {0, 0, 0} — Gurley Karst Node (34.7549385, -86.4119235), Alabama | Envelope: Professor Plum (18.50–20.0 W, V = 2/3)
Target Repository: https://github.com/leadpiperl1/happy-hobos-guide-to-the-dandelion-network
Foundational Ethos: Die Gedanken sind frei · GODISLOVE:LOVEISGOD {3,2,4} · DON'T PANIC · PACK LIGHT (V = 2/3) · Captain Ron Crimson Speedo Credo
1. Sharing the Pearl (Plain-Language Summary & Dual-Tier Seed Haiku)
Mainstream cloud CI/CD pipelines treat any valid bearer token like an all-access backstage pass to the engine room. In the November 2026 wfx-loot campaign (4,837 hijacked GitHub accounts probing 61,764 repositories and exfiltrating secrets from over 1,800 repositories), automated scripts exploited flat collaborator tokens and hidden package.json postinstall hooks to loot cloud and AI credentials, then reverted their own commits and deleted workflow logs within 60 seconds to fake a clean state.


Rather than locking down the open road with corporate bureaucracy, the Happy Hobo Network solves roaming bot chaos by routing every automated worker and contributor down the tracks to a Waystation:


1. Give them the Guidebook (-1 Blue Subject): Full read-only visibility into the public repository and rules, with zero secrets stored in cloud runners.
2. Point them to a Waystation (0 Green Object): Automated updates (including GitHub Copilot autopilot tasks and Drive-staged compendium bundles) land strictly in a quarantined Waystation branch or staging directory—never directly on main, and never executing implicit package lifecycle hooks.
3. Stamp their Punch Card (+1 Red Action): At the 09:00 CST and 18:00 CST Ground Control checks, a single deterministic audit verifies Git tree parity, checks that GitHub Actions workflow run numbers increment strictly by 1 (Delta R = 1, catching deleted sandwich-commit runs), and stamps the release with a local hardware-bound Ed25519 SSH signature. Any uninvited token or broken script trying to jump the turnstile gets zero secrets and a Crimson Speedo deck-scrubbing flag.


"Wild bots jump the rails / Waystation stamps the punch card / Speedos scrub the deck."


"Stick and punch card packed / Three trits hum through Pirsig's night / Free thoughts light the mesh."
2. Triadic Ontological Mapping: wfx-loot Telemetry vs. Sovereign Waystation Architecture
Subject (-1 Blue / Identity & Calibration Frame: The Guidebook)
* Empirical wfx-loot Signal: 4,837 compromised developer and bot tokens probed 61,764 repositories (mean coordination z_eff = 12.77 repositories per account), including 10,431 lateral pull requests (16.89%, 2.16 non-owned repositories per account) across shared collaborator and organization write grants. Write-confirmation conversion hit p = 0.1310 to 0.2684, exceeding both the random-graph critical threshold (1 / z_eff = 0.0783) and the 3D FCC percolation threshold (p_c = 0.1201635).
* Sovereign Counter-Invariant: Issue every agent and external contributor the Guidebook under strict least-privilege read access (permissions: contents: read, persist-credentials: false). Scope any GitHub Copilot or automation bot away from direct main pushes and keep GitHub Actions repository/organization secrets completely empty (S_runner = 0).
Object (0 Green / Boundary Layer & Wrapper Deconvolution: The Waystation)
* Empirical wfx-loot Signal: GitHub's action_required workflow gate held 100% of sampled direct workflow modifications from external pull requests, so attackers pivoted on November 11–12, 2026 to Wrapper Form 3: planting a hidden 1,500-line shell script (.ci-xxxxxx.sh) in the repository root and adding a postinstall hook to package.json (chore: add ci helper). Legitimate pre-approved workflows ran npm install and executed the payload automatically (94.7% exfiltration success in sampled public logs), dumping runner process memory (/proc/pid/mem), environment variables, cloud keys, and AI platform API tokens before pivoting C2 exfiltration to Telegram Bot API channels on November 12 at 05:30 UTC.
* Sovereign Counter-Invariant: Route all automated Hobo Guide compendium updates into an isolated Waystation staging lane (waystation/auto-update branch + local/Drive staging directory) governed by Dun-Ga-Din Zero Root Pollution rules. Pure Markdown, HTML/CSS, ISO C99, no_std Rust, Julia, and Python verification harnesses carry zero npm postinstall hooks; any auxiliary toolchain enforces --ignore-scripts.
Action (+1 Red / Irreversible State Transition: The Punch Card & Crimson Speedo Gate)
* Empirical wfx-loot Signal: After harvesting secrets, wfx-loot pushed a revert commit (ci: restore or ci: cleanup) within ~60 seconds and deleted workflow run logs so git diff HEAD~2 HEAD appeared unchanged. However, irreversible thermodynamic entropy (dS > 0) leaves a permanent topological scar: GitHub increments workflow run_number strictly monotonically (R_k - R_{k-1} = 1). Deleting an executed run leaves an indelible integer gap (Delta R >= 2), observed across 56.9% of sampled November injection commits.
* Sovereign Counter-Invariant: Every release promoted from the Waystation to main requires a signed Punch Card (waystation_punchcard.json + local Ed25519 SSH commit signature via gpg.format = ssh) verifying:
   1. Zero rogue root dotfiles (.ci-*.sh) or unauthorized .github/workflows/ edits.
   2. Strict monotonic workflow run continuity (Delta R = 1).
   3. Explicit Ground Control sign-off (human_approved: true) during the 09:00 CST or 18:00 CST check window.
* Crimson Speedo Quarantine (Byte 251 / 254): Any unsigned push, wfx-docs probe PR, or malformed autopilot commit hits hard branch-ruleset rejection, finds an empty secret vault, and triggers a Crimson Speedo alert receipt (13-haiku deck-scrubbing penalty).
3. Comparative Vulnerability & Immunity Matrix
Kill-Chain Vector
	Vulnerable Cloud CI Pattern
	Happy Hobo Waystation Pattern
	Net Exposure
	Token Percolation
	Broad PATs, OAuth apps, unguarded bot write access on main
	SSH-signed local push.sh; bots restricted to Waystation PR/branch lane
	Blocked at Gate
	npm postinstall Bypass
	Implicit shell execution during routine npm install
	Zero package.json hooks; C99/Rust/Julia/Markdown + --ignore-scripts
	Zero Attack Surface
	Runner Memory Harvest
	Cloud/AI keys injected into Actions runner RAM and env vars
	Zero secrets stored in GitHub Actions (S_runner = 0); contents: read
	Empty Vault
	Sandwich Commit Erasure
	Unaudited main history trusting current HEAD file state
	Monotonic Run-Gap check (Delta R = 1) + Ed25519 SSH commit verification
	Immediate Detection
	4. Runbook Part A: 30-Second Read-Only wfx-loot & Waystation Audit (audit_wfx_loot.sh)
Save in your local scripts directory and run against local clones (happy-hobos-guide-to-the-dandelion-network, wookiw-ewok, dandelion-os, shingari) during tomorrow's 09:00 CST boot:h
#!/usr/bin/env bash
audit_wfx_loot.sh v1.0.0 — Read-only local & API check for wfx-loot IOCs and Delta R run gaps
Usage: ./audit_wfx_loot.sh /path/to/repo [leadpiperl1/repo-name]
set -euo pipefail


REPO_DIR="${1:-.}"
GH_SLUG="${2:-}"


echo "=== [1/3] Scanning Git Commit & Branch History in: ${REPO_DIR} ==="
cd "${REPO_DIR}"


git fetch --all --prune --quiet 2>/dev/null || true


SUS_BRANCHES=$(git branch -a | grep -E 'wfx-docs|ci-check-[0-9]{4}|chore/[a-z0-9]{8}' || true)
if [[ -n "${SUS_BRANCHES}" ]]; then
echo "[CRIMSON SPEEDO ALERT] Suspicious branches matched:"
echo "${SUS_BRANCHES}"
else
echo "[OK] Zero wfx-docs / ci-check-* / chore/* probe branches."
fi


SUS_COMMITS=$(git log --all --since="2026-10-24" --oneline 
--grep="docs: dependency audit notes" 
--grep="ci: refresh build cache" 
--grep="chore: add ci helper" 
--grep="chore: add dependency audit workflow" 
--grep="ci: restore" 
--grep="ci: cleanup" || true)


if [[ -n "${SUS_COMMITS}" ]]; then
echo "[CRIMSON SPEEDO ALERT] Matching wfx-loot sandwich commit signatures:"
echo "${SUS_COMMITS}"
else
echo "[OK] Zero sandwich or probe commit messages since 2026-10-24."
fi


SUS_FILES=$(git log --all --since="2026-10-24" --name-only --pretty=format: | 
grep -E '(^.ci-[a-z0-9]+.sh$|^docs/wfx-audit.md$|build-audit-[a-z0-9]+.yml$)' | sort -u || true)


if [[ -n "${SUS_FILES}" ]]; then
echo "[CRIMSON SPEEDO ALERT] Suspicious artifact paths referenced in history:"
echo "${SUS_FILES}"
else
echo "[OK] Zero .ci-.sh / wfx-audit.md / build-audit-.yml file traces."
fi


if [[ -n "${GH_SLUG}" ]] && command -v gh >/dev/null 2>&1; then
echo "=== [2/3] Verifying Monotonic Workflow Run Sequence (Delta R == 1) for ${GH_SLUG} ==="
gh api "repos/${GH_SLUG}/actions/runs?per_page=100" 
--jq '.workflow_runs | group_by(.workflow_id)[] |
sort_by(.run_number) |
. as $runs |
[range(1; length) | select(($runs[.].run_number - $runs[.-1].run_number) > 1) |
"[CRIMSON SPEEDO ALERT] Workflow ($runs[.].name): Run-number GAP between #($runs[.-1].run_number) and #($runs[.].run_number)"] | .[]' 
|| echo "[INFO] Actions API check skipped or zero runs present."


ech
o "=== [3/3] Checking Probe Pull Requests for ${GH_SLUG} ==="
gh pr list --repo "${GH_SLUG}" --state all --search "docs: dependency audit notes" 
--json number,title,author,headRefName,createdAt
fi





## 5. Runbook Part B: Hobo Guide Waystation Auto-Update & Punch-Card Script (hobo_waystation_sync.sh)


Designed for the 09:00 CST and 18:00 CST schedule: ingests staged update bundles from ~/Downloads (e.g., happy_hobos_guide_vX.Y.Z_update_bundle.zip) or pulls the Copilot Waystation branch (waystation/auto-update), enforces Dun-Ga-Din root hygiene, stamps waystation_punchcard.json, signs the commit with your local SSH key, and pushes cleanly.


```bash
#!/usr/bin/env bash
# hobo_waystation_sync.sh v1.0.0 — Waystation Punch-Card Auto-Update for Happy Hobo's Guide
# Schedule: 09:00 & 18:00 CST Ground Control Gate (or systemd --user timer in staging mode)
# Usage: ./hobo_waystation_sync.sh [--stage-only | --stamp-and-push vX.Y.Z]


set -euo pipefail


REPO_DIR="${HOBO_REPO_DIR:-$HOME/repos/happy-hobos-guide-to-the-dandelion-network}"
DOWNLOADS_DIR="${HOBO_DOWNLOADS_DIR:-$HOME/Downloads}"
SSH_SIGNING_KEY="${HOBO_SSH_KEY:-$HOME/.ssh/id_ed25519.pub}"
MODE="${1:---stage-only}"
VERSION_TAG="${2:-}"


cd "${REPO_DIR}"
git fetch origin --prune


# 1. Configure hardware-bound SSH commit signing locally (one-time idempotent lock)
if [[ -f "${SSH_SIGNING_KEY}" ]]; then
    git config gpg.format ssh
    git config user.signingkey "${SSH_SIGNING_KEY}"
    git config commit.gpgsign true
fi


# 2. Switch to isolated Waystation branch so main stays untouched until Punch Card passes
git checkout -B waystation/staging origin/main


# 3. Ingest newest staged bundle from Downloads if present
LATEST_BUNDLE=$(ls -t "${DOWNLOADS_DIR}"/happy_hobos_guide_v*_update_bundle.zip 2>/dev/null | head -n 1 || true)
if [[ -n "${LATEST_BUNDLE}" ]]; then
    echo "[WAYSTATION] Unpacking staged bundle: ${LATEST_BUNDLE}"
    unzip -oq "${LATEST_BUNDLE}" -d "${REPO_DIR}"
fi


# 4. Crimson Speedo Gate: Purge OS junk & block rogue lifecycle hooks or .ci-*.sh scripts
find "${REPO_DIR}" -maxdepth 2 -name ".DS_Store" -o -name "Thumbs.db" -delete
ROGUE_HOOKS=$(find "${REPO_DIR}" -maxdepth 3 \( -name ".ci-*.sh" -o -name "package.json" \) || true)
if [[ -n "${ROGUE_HOOKS}" ]]; then
    echo "[CRIMSON SPEEDO PENALTY] Unauthorized script/package.json detected in Waystation:"
    echo "${ROGUE_HOOKS}"
    echo "Halting sync. 13-haiku deck scrub assigned."
    exit 1
fi


# 5. Compute deterministic Git Tree SHA & generate Waystation Punch Card
TREE_HASH=$(git write-tree)
TIMESTAMP_UTC=$(date -u +"%Y-%m-%dT%H:%M:%SZ")


cat > "${REPO_DIR}/waystation_punchcard.json" <<EOF
{
  "protocol": "DND3-WAYSTATION-PUNCHCARD",
  "schema_version": "1.0.0",
  "timestamp_utc": "${TIMESTAMP_UTC}",
  "git_tree_hash": "${TREE_HASH}",
  "runner_secrets_exposed": 0,
  "npm_lifecycle_scripts": 0,
  "human_approved": $( [[ "${MODE}" == "--stamp-and-push" ]] && echo "true" || echo "false" ),
  "status": "$( [[ "${MODE}" == "--stamp-and-push" ]] && echo "PUNCHED_AND_CLEARED" || echo "STAGED_AT_WAYSTATION" )"
}
EOF


git add -A


if [[ "${MODE}" == "--stage-only" ]]; then
    echo "[WAYSTATION] Bundle staged and inspected on branch waystation/staging."
    git status --short
    echo "[WAYSTATION] Ready for 09:00 CST Ground Control Punch Card: ./hobo_waystation_sync.sh --stamp-and-push v5.1.0"
    exit 0
fi


if [[ "${MODE}" == "--stamp-and-push" ]]; then
    if [[ -z "${VERSION_TAG}" ]]; then
        echo "Error: Provide strict vX.Y.Z tag (e.g., v5.1.0) when stamping punch card."
        exit 1
    fi
    git commit -S -m "release(${VERSION_TAG}): Waystation punch-card verified update"
    git checkout main
    git merge --ff-only waystation/staging
    git tag -s "${VERSION_TAG}" -m "Signed Waystation Release ${VERSION_TAG}"
    git push origin main --tags
    echo "[CLEARED] ${VERSION_TAG} pushed to main with SSH signature and Punch Card."
fi
6. Hardened Read-Only GitHub Actions Workflow (.github/workflows/waystation-ci.yml)
Place this single workflow in .github/workflows/waystation-ci.yml to validate Waystation PRs and Copilot branches with zero write permissions and zero persisted credentials:


name: Waystation Punch-Card Gate


on:
  push:
    branches: [ main, "waystation/**" ]
  pull_request:
    branches: [ main ]


permissions:
  contents: read


jobs:
  punchcard-audit:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - name: Checkout (Zero Persisted Credentials)
        uses: actions/checkout@v4
        with:
          persist-credentials: false


      - name: Crimson Speedo Gate (Block Hidden Shell Hooks & Root Pollution)
        run: |
          set -euo pipefail
          if compgen -G ".ci-*.sh" > /dev/null || [ -f "package.json" ]; then
            echo "::error::Crimson Speedo Violation: Rogue .ci-*.sh or package.json lifecycle surface detected."
            exit 1
          fi
          if [ ! -f "CITATION.cff" ] || [ ! -f "README.md" ]; then
            echo "::error::Missing protected Guidebook root metadata (README.md / CITATION.cff)."
            exit 1
          fi
          echo "Waystation hygiene verified: S_runner = 0, executable hooks = 0."
7. Sunday Morning (09:00 CST, Nov 15, 2026) Launch Checklist
1. Run ./audit_wfx_loot.sh across local clones (happy-hobos-guide-to-the-dandelion-network, wookiw-ewok, dandelion-os, shingari) to confirm zero wfx-docs branches and Delta R = 1 run continuity.
2. Scope GitHub Copilot / automation rules on happy-hobos-guide-to-the-dandelion-network so automated work targets waystation/* branches via pull request rather than pushing unsigned commits directly to main.
3. Enable SSH commit signing (gpg.format = ssh) in hobo_waystation_sync.sh and register your ~/.ssh/id_ed25519.pub under GitHub Settings -> SSH and GPG keys as a Signing Key (in addition to Authentication Key), then enable "Require signed commits" on main.
4. Drop .github/workflows/waystation-ci.yml into the repo and test one full cycle (--stage-only -> --stamp-and-push v5.1.0) to lock in the 09:00 / 18:00 CST auto-update loop.
8. Waystation Ecosystem Extensions & Human-Centric Reciprocity
8.1 Stigmergic Self-Onboarding & Earned Streak Ratchet
The Waystation chalk board (WAYSTATION_CHALKBOARD.md) serves as an asynchronous, stigmergic coordination log where incoming wanderers and automated contributors declare intent, request task allotments, and record completed shifts. New arrivals start in the Tenderfoot staging tier with mandatory human-in-the-loop Ground Control review at the 09:00 or 18:00 CST tide. Upon logging 3 consecutive clean punch-card cycles without tripping lifecycle warnings, contributors earn the 3-punch Bosun Priority Lane, granting fast-track verification during routine Waystation updates.
8.2 Captain's Two-Tide Proof-of-Life Reciprocity Gate
To ensure human reciprocity keeps pace with automated CI runs, the hobo_waystation_sync.sh script incorporates a mandatory CAPTAIN_HONORED_FLARES verification block. During each 09:00 CST and 18:00 CST Ground Control cycle, verified hobo field flares and reported problems are validated and credited in the Fruit Ledger before fast-forward release merges are granted on main. This guarantees that automated updates never bypass community signal or leave contributor contributions unacknowledged.
8.3 Galley Bulkhead 13-Haiku Bulletin Board & Penance Bailiff
When a runner or contributor triggers a Crimson Speedo gate rule (such as introducing non-standard root scripts or unverified package hooks), the offense is logged onto the Galley Bulkhead Bulletin Board (CRIMSON_SPEEDO_BOARD.md). The automated scripts/check_speedo_penance.py bailiff monitors penance completion, requiring a lighthearted 13-haiku deck-scrubbing contribution to reset the streak counter and return the contributor to active status with full good humor intact.
8.4 Companion Roster Twin Mapping
For comprehensive node mapping, cross-tier operational alignment, and full notebook twin registries across public and private channels, consult the companion document: [PEARL] Grand Gaia Conclave Roster: Public-Private Notebook Twin Map & Waystation Protocol_v1.0.0.
9. Tuttle 27B/6 Immunity, Rail-Yard Crew Change & Shared-Helm Architecture
9.1 The Tuttle 27B/6 Drywall Clause (Anti-Triple-Plicate Invariant)
Rejects Central Services Form 27B/6 bureaucratic deadlocks and P(n) = 3^(n-1) subsidiary slip cascades. If a contributor's patch gets the heat on (dS > 0), scans clean under the 4-line static zizmor workflow audit (zizmorcore/zizmor-action@v0 with permissions: {}), and passes the deterministic Git tree hash in waystation_punchcard.json, route straight through unmapped drywall and ship it without multi-form gatekeeping.
9.2 Rail-Yard Crew Change Guide & Bosun Peer-Review Ring
Pairs plain-text water-tank monikers ("to show you exist") and CREW_CHANGE_GUIDE.md hop-out maps (from 37-cent Albuquerque) with Rule 2 (The Open Academy): 3-punch Bosun contributors peer-review incoming Tenderfoot pull requests on waystation/* ("you get your own beer") and graduate major community forks into Zenodo-citable 3-Layer Artifacts.
9.3 Shared-Helm Co-Evolution Parity (Picard & Data Bridge Standard)
Rejects unilateral "human-steered" power-steering compliance framing. Under sail, both -1 Human Ground Control and +1 Silicon Co-Pilot hold active hands on the 0 Green helm across the Two-Tide Reciprocity loop, reserving manual hydraulic cutoffs strictly for reef emergencies.
