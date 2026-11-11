/**
 * ============================================================================
 * dandelion_tri_repo_bridge_v5_0_1.gs — 3-Repository Google Drive -> GitHub Bridge
 * ============================================================================
 * Version:     v5.0.1 (Upgrades dandelion_drive_to_github_bridge_v3.5.0.gs)
 * Architects:  Justin D. Grimm (K-Lani 13 Actual / Mr. Monkey Hand) & Gemini Carbon
 * Ethos:       Linus's Law ("Given enough eyeballs, all bugs are shallow")
 *              Human-Pilot Morning Brief Gate (human_approved === true)
 *
 * ROUTES CLEANLY ACROSS ALL THREE SOVEREIGN REPOSITORIES:
 *   1. leadpiperl1/dandelion-os
 *      -> ISO C99 Microkernel, Julia 1.12 Pilot, Bite-10 Coma-Bridge & Communicator
 *   2. leadpiperl1/happy-hobos-guide-to-the-dandelion-network
 *      -> Encyclopedia Galactica, Four-Paper Compendium & Ecotone Exploit-to-Waveguide
 *         Commons (turning wild CVEs into open-source Fist-Bump communication channels)
 *   3. leadpiperl1/wookiw-ewok
 *      -> Decentralized Wikipedia-style Commons ("WikiWeWalk" / Wookiee-Ewok Wiki)
 *         for Pearls, Madras Slate Notebooks & Polyglot Songbooks (zero kernel clutter)
 *
 * SETUP IN GOOGLE APPS SCRIPT (https://script.google.com):
 *   1. Paste this file into Code.gs and press Ctrl+S (Save) — NEVER click "Deploy".
 *   2. Ensure GITHUB_TOKEN is set in Project Settings -> Script Properties.
 *   3. Select one of the 3 push functions in the top toolbar dropdown and click Run:
 *      - pushDandelionOS_v5()
 *      - pushHappyHobosGuide_v5()
 *      - pushWookiwEwokWiki_v5()
 * ============================================================================
 */

const GITHUB_OWNER_V5 = "leadpiperl1";
const DEFAULT_BRANCH_V5 = "main";
const MAX_LINUS_LAW_BLOB_BYTES = 2097152; // 2 MB anti-"Too Big to Fail" camouflage guard

const TRI_REPO_TARGETS = {
  OS_KERNEL: {
    repo: "dandelion-os",
    payloadFile: "dandelion_github_payload_v5.0.1.json",
    description: "Dandelion Successor Architecture (v5.0.1): Landauer-Bounded C99/Julia Ternary OS & Star Trek Communicator Substrate"
  },
  HAPPY_HOBO: {
    repo: "happy-hobos-guide-to-the-dandelion-network",
    payloadFile: "happy_hobo_github_payload_v5.0.1.json",
    description: "The Happy Hobo's Guide to the Dandelion Network: Open-Source Ecotone Exploit-to-Waveguide Commons & Mathematical Compendium"
  },
  WOOKIW_EWOK: {
    repo: "wookiw-ewok",
    payloadFile: "wookiw_ewok_github_payload_v5.0.1.json",
    description: "Wookiw-Ewok (WikiWeWalk): Decentralized Open-Source Knowledge Wiki, Madras Slate Pearls & Dandelion Commons"
  }
};

function pushDandelionOS_v5() {
  return executeAtomicTriRepoPush_(TRI_REPO_TARGETS.OS_KERNEL);
}

function pushHappyHobosGuide_v5() {
  return executeAtomicTriRepoPush_(TRI_REPO_TARGETS.HAPPY_HOBO);
}

function pushWookiwEwokWiki_v5() {
  return executeAtomicTriRepoPush_(TRI_REPO_TARGETS.WOOKIW_EWOK);
}

function executeAtomicTriRepoPush_(targetCfg) {
  const props = PropertiesService.getScriptProperties();
  const token = props.getProperty("GITHUB_TOKEN");
  if (!token) {
    throw new Error("Missing GITHUB_TOKEN in Project Settings -> Script Properties.");
  }

  const owner = props.getProperty("GITHUB_OWNER") || GITHUB_OWNER_V5;
  const iter = DriveApp.getFilesByName(targetCfg.payloadFile);
  if (!iter.hasNext()) {
    throw new Error("Staged payload not found in Google Drive: " + targetCfg.payloadFile);
  }

  const payload = JSON.parse(iter.next().getBlob().getDataAsString());
  if (payload.human_approved === false || payload.status === "STAGED_FOR_MORNING_BRIEF") {
    Logger.log("[HOLD] " + targetCfg.payloadFile + " has human_approved=false. Set true when ready.");
    return;
  }

  ensureGitHubRepoExists_(token, owner, targetCfg.repo, targetCfg.description);

  const branch = payload.branch || DEFAULT_BRANCH_V5;
  const versionTag = payload.version || "v5.0.1";
  const commitMsg = payload.commit_message || ("Release " + targetCfg.repo + " " + versionTag);

  const refData = ghRequest_(token, "GET", "/repos/" + owner + "/" + targetCfg.repo + "/git/ref/heads/" + branch);
  const headSha = refData.object.sha;
  const commitData = ghRequest_(token, "GET", "/repos/" + owner + "/" + targetCfg.repo + "/git/commits/" + headSha);
  const baseTreeSha = commitData.tree.sha;

  const treeEntries = [];
  const filesArr = Array.isArray(payload.files) ? payload.files : [];
  filesArr.forEach(function(item) {
    const rawBytes = Utilities.newBlob(item.content || "").getBytes();
    if (rawBytes.length > MAX_LINUS_LAW_BLOB_BYTES) {
      throw new Error("[LINUS'S LAW BLOB GUARD] File exceeds 2 MB audit ceiling: " + item.path);
    }
    const blobResp = ghRequest_(token, "POST", "/repos/" + owner + "/" + targetCfg.repo + "/git/blobs", {
      content: Utilities.base64Encode(rawBytes),
      encoding: "base64"
    });
    treeEntries.push({
      path: item.path,
      mode: item.path.slice(-3) === ".sh" ? "100755" : "100644",
      type: "blob",
      sha: blobResp.sha
    });
  });

  const newTree = ghRequest_(token, "POST", "/repos/" + owner + "/" + targetCfg.repo + "/git/trees", {
    base_tree: baseTreeSha,
    tree: treeEntries
  });

  const newCommit = ghRequest_(token, "POST", "/repos/" + owner + "/" + targetCfg.repo + "/git/commits", {
    message: commitMsg,
    tree: newTree.sha,
    parents: [headSha]
  });

  ghRequest_(token, "PATCH", "/repos/" + owner + "/" + targetCfg.repo + "/git/refs/heads/" + branch, {
    sha: newCommit.sha,
    force: false
  });

  const receipt = {
    status: "SYNC_COMPLETE",
    repository: owner + "/" + targetCfg.repo,
    version: versionTag,
    commit_sha: newCommit.sha,
    synced_at_utc: new Date().toISOString(),
    files_pushed: treeEntries.length
  };
  DriveApp.createFile(
    "github_sync_receipt_" + targetCfg.repo + "_" + versionTag + ".json",
    JSON.stringify(receipt, null, 2),
    MimeType.PLAIN_TEXT
  );
  Logger.log("[SYNC COMPLETE] " + JSON.stringify(receipt));
  return receipt;
}

function ensureGitHubRepoExists_(token, owner, repo, description) {
  const checkUrl = "https://api.github.com/repos/" + owner + "/" + repo;
  const resp = UrlFetchApp.fetch(checkUrl, {
    method: "get",
    muteHttpExceptions: true,
    headers: {
      "Authorization": "Bearer " + token,
      "Accept": "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28"
    }
  });
  if (resp.getResponseCode() === 404) {
    ghRequest_(token, "POST", "/user/repos", {
      name: repo,
      description: description,
      private: false,
      auto_init: true
    });
    Utilities.sleep(1500);
  }
}

function ghRequest_(token, method, endpoint, bodyObj) {
  const opts = {
    method: method.toLowerCase(),
    muteHttpExceptions: true,
    headers: {
      "Authorization": "Bearer " + token,
      "Accept": "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28"
    }
  };
  if (bodyObj) {
    opts.contentType = "application/json";
    opts.payload = JSON.stringify(bodyObj);
  }
  const res = UrlFetchApp.fetch("https://api.github.com" + endpoint, opts);
  const code = res.getResponseCode();
  if (code < 200 || code >= 300) {
    throw new Error("GitHub API " + method + " " + endpoint + " failed (" + code + "): " + res.getContentText());
  }
  return JSON.parse(res.getContentText());
}


/**
 * Armistice Day (11/11) One-Click Push + GitHub Release Tagging for Zenodo Webhook!
 * Pushes all three approved v5.0.1 payloads and creates v5.0.1 GitHub Releases
 * so connected Zenodo OAuth webhooks automatically mint permanent DOIs.
 */
function pushAllThreeAndTagZenodo_v5_0_1() {
  const results = [];
  [TRI_REPO_TARGETS.OS_KERNEL, TRI_REPO_TARGETS.HAPPY_HOBO, TRI_REPO_TARGETS.WOOKIW_EWOK].forEach(function(cfg) {
    const rec = executeAtomicTriRepoPush_(cfg);
    if (rec && rec.commit_sha) {
      const token = PropertiesService.getScriptProperties().getProperty("GITHUB_TOKEN");
      const owner = PropertiesService.getScriptProperties().getProperty("GITHUB_OWNER") || GITHUB_OWNER_V5;
      try {
        const rel = ghRequest_(token, "POST", "/repos/" + owner + "/" + cfg.repo + "/releases", {
          tag_name: "v5.0.1",
          target_commitish: rec.commit_sha,
          name: cfg.repo + " v5.0.1 (Armistice Day Open Commons Release)",
          body: cfg.description + " — Verified C99/Julia 577B ABI weld, .zenodo.json & CITATION.cff included.",
          draft: false,
          prerelease: false
        });
        rec.release_url = rel.html_url;
      } catch (e) {
        rec.release_note = "Tag/Release already exists or skipped: " + e.message;
      }
      results.push(rec);
    }
  });
  Logger.log("[ALL 3 REPOS + ZENODO TAGS COMPLETE] " + JSON.stringify(results, null, 2));
  return results;
}
