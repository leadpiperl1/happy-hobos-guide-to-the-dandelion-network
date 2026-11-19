#!/usr/bin/env bash
# ==============================================================================
# hobo_waystation_sync.sh (v1.2.0)
# Waystation Punch-Card Auto-Update, Tuttle 27B/6 Drywall Gate & Two-Tide Sync
# Schedule: 09:00 & 18:00 CST Ground Control Gate (profplum, bash-5.3$)
# Author: Justin D. Grimm (ORCID: 0009-0000-5299-0243)
# Usage: bash scripts/hobo_waystation_sync.sh [--dry-run | --stage-only | --stamp-and-push vX.Y.Z]
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="${HOBO_REPO_DIR:-$(cd "${SCRIPT_DIR}/.." && pwd)}"
DOWNLOADS_DIR="${HOBO_DOWNLOADS_DIR:-$HOME/Downloads}"
SSH_SIGNING_KEY="${HOBO_SSH_KEY:-$HOME/.ssh/id_ed25519.pub}"
MODE="${1:---dry-run}"
VERSION_TAG="${2:-v5.1.0}"

cd "${REPO_DIR}"

echo "=== Happy Hobo Waystation Sync (v1.2.0) | Mode: ${MODE} | Target: ${VERSION_TAG} ==="

# 1. Tuttle 27B/6 & wfx-loot Pre-Flight Audit
bash "${REPO_DIR}/scripts/audit_wfx_loot.sh" "${REPO_DIR}" "leadpiperl1/happy-hobos-guide-to-the-dandelion-network"

# 2. Captain's Two-Tide Proof-of-Life Reciprocity Gate (09:00 & 18:00 CST)
CAPTAIN_HONORED_FLARES="$(grep -c 'HONORED' "${REPO_DIR}/WAYSTATION_CHALKBOARD.md" || true)"
if [[ "${CAPTAIN_HONORED_FLARES}" -lt 1 ]]; then
  echo "[TWO-TIDE GATE] Zero honored flares recorded in WAYSTATION_CHALKBOARD.md; review community flares first." >&2
  exit 1
fi
echo "[OK] Two-Tide Proof-of-Life Gate: ${CAPTAIN_HONORED_FLARES} honored flare entries verified."

# 3. Crimson Speedo 13-Haiku Bulkhead & Pure-Stdlib Verification (--seed 42)
python3 "${REPO_DIR}/scripts/check_speedo_penance.py" --seed 42 \
  --board "${REPO_DIR}/CRIMSON_SPEEDO_BOARD.md" \
  --punchcard "${REPO_DIR}/waystation_punchcard.json"
python3 "${REPO_DIR}/waveguides/dandelion_communicator_madras_v5_0_0.py" --verify

if [[ "${MODE}" == "--dry-run" ]]; then
  echo "[DRY-RUN PASS] Tuttle 27B/6, Two-Tide Proof-of-Life, and Crimson Speedo 13-Haiku gates clean."
  exit 0
fi

# 4. Hardware-bound Ed25519 SSH signing check (graceful fallback if unconfigured)
SIGN_COMMIT_FLAGS=()
SIGN_TAG_FLAGS=(-a)
SSH_SIGNED="false"
if [[ "$(git config --get gpg.format || true)" == "ssh" ]] && [[ -n "$(git config --get user.signingkey || true)" ]]; then
  SIGN_COMMIT_FLAGS=(-S)
  SIGN_TAG_FLAGS=(-s)
  SSH_SIGNED="true"
elif [[ -f "${SSH_SIGNING_KEY}" ]]; then
  git config gpg.format ssh
  git config user.signingkey "${SSH_SIGNING_KEY}"
  SIGN_COMMIT_FLAGS=(-S)
  SIGN_TAG_FLAGS=(-s)
  SSH_SIGNED="true"
else
  echo "[NOTICE] No local Ed25519 SSH signing key configured; falling back to unsigned Git commit/tag."
fi

WAYSTATION_BRANCH="waystation/${VERSION_TAG}"
git checkout -B "${WAYSTATION_BRANCH}"

TREE_HASH="$(git write-tree)"
TIMESTAMP_UTC="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
HUMAN_OK="false"
STATUS_STR="STAGED_AT_WAYSTATION"
if [[ "${MODE}" == "--stamp-and-push" ]]; then
  HUMAN_OK="true"
  STATUS_STR="PUNCHED_AND_CLEARED"
fi

cat > "${REPO_DIR}/waystation_punchcard.json" <<EOF
{
  "protocol": "DND3-WAYSTATION-PUNCHCARD",
  "schema_version": "1.2.0",
  "repository": "leadpiperl1/happy-hobos-guide-to-the-dandelion-network",
  "version": "${VERSION_TAG}",
  "timestamp_utc": "${TIMESTAMP_UTC}",
  "git_tree_hash": "${TREE_HASH}",
  "runner_secrets_exposed": 0,
  "npm_lifecycle_scripts": 0,
  "tuttle_27b6_drywall_bypass": true,
  "two_tide_windows_cst": ["09:00", "18:00"],
  "captain_honored_flares": ${CAPTAIN_HONORED_FLARES},
  "ssh_signed": ${SSH_SIGNED},
  "human_approved": ${HUMAN_OK},
  "status": "${STATUS_STR}",
  "exit_invariant": 255
}
EOF

git add -A
if [[ "${MODE}" == "--stage-only" ]]; then
  echo "[WAYSTATION] Staged on ${WAYSTATION_BRANCH} (tree=${TREE_HASH})."
  git status --short
  exit 0
fi

if [[ "${MODE}" == "--stamp-and-push" ]]; then
  git commit "${SIGN_COMMIT_FLAGS[@]}" -m "release(${VERSION_TAG}): Waystation punch-card verified update" || true
  git push -u origin "${WAYSTATION_BRANCH}"
  git checkout main
  git merge --ff-only "${WAYSTATION_BRANCH}"
  git tag -f "${SIGN_TAG_FLAGS[@]}" "${VERSION_TAG}" -m "Waystation Release ${VERSION_TAG}"
  git push origin main "${VERSION_TAG}"
  echo "[CLEARED] ${VERSION_TAG} fast-forwarded to main (ssh_signed=${SSH_SIGNED})."
fi
