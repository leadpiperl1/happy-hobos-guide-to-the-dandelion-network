/**
 * ============================================================================
 * dandelion_quad_repo_bridge_v5_0_2.gs — 4-Repo Chromatic Porch & Git->Zenodo Bridge
 * ============================================================================
 * Version:     v5.0.2 (Armistice Day Campfire Porch + Zero-Form Zenodo Release Engine)
 * Architects:  Justin D. Grimm (K-Lani 13 Actual / Mr. Monkey Hand) & Gemini-Carbon
 * Ethos:       Warm Myspace-Tom Porch Light · Linus's Law · Zero Manual Data Entry
 *
 * MANAGES ALL FOUR OPEN-COMMONS REPOSITORIES VIA GIT API:
 *   1. leadpiperl1/dandelion-os                                  (v5.0.2)
 *   2. leadpiperl1/happy-hobos-guide-to-the-dandelion-network    (v5.0.2)
 *   3. leadpiperl1/wookiw-ewok                                   (v5.0.2)
 *   4. leadpiperl1/epigenetic-state-dispatch                     (v1.0.0 Preprint + PDF + Code)
 *
 * ZERO-MANUAL-ENTRY GIT -> ZENODO WORKFLOW (3 CLICKS TOTAL):
 *   STEP 1: Paste this file into Google Apps Script (Code.gs), press Ctrl+S,
 *           select `pushAllFourCampfireRepos_v5_0_2` in the top dropdown, and click Run.
 *           (This pushes all colorful SVG banners, READMEs, code, PDFs, and .zenodo.json
 *            files, and automatically creates `epigenetic-state-dispatch` on GitHub!)
 *   STEP 2: Open https://zenodo.org/account/settings/github/ , click "Sync now",
 *           and make sure the toggle switches next to ALL 4 repositories are flipped ON.
 *   STEP 3: Come back here, select `cutZenodoReleasesAllFour_v5_0_2` in the dropdown,
 *           and click Run! GitHub will publish formal releases on all 4 repos, and
 *           Zenodo's webhook will automatically read `.zenodo.json` and mint permanent
 *           DOIs for you with ZERO manual typing!
 * ============================================================================
 */

const GITHUB_OWNER_V502 = "leadpiperl1";
const DEFAULT_BRANCH_V502 = "main";
const MAX_LINUS_LAW_BLOB_BYTES_V502 = 2097152; // 2 MB per-file audit guard

const QUAD_REPO_TARGETS = {
  OS_KERNEL: {
    repo: "dandelion-os",
    payloadFile: "dandelion_github_payload_v5.0.2.json",
    releaseTag: "v5.0.2",
    releaseTitle: "Dandelion Successor Architecture v5.0.2 — Campfire Porch & 577B C99/Julia Substrate",
    description: "Dandelion Successor Architecture: Warm, Local-First Balanced Ternary OS (≤ 18.50 W), Bite-10 Coma-Bridge & Star Trek Communicator Substrate"
  },
  HAPPY_HOBO: {
    repo: "happy-hobos-guide-to-the-dandelion-network",
    payloadFile: "happy_hobo_github_payload_v5.0.2.json",
    releaseTag: "v5.0.2",
    releaseTitle: "The Happy Hobo's Guide to the Dandelion Network v5.0.2 — Don't Panic, Pack Light (V=2/3)",
    description: "DON'T PANIC · PACK LIGHT (V=2/3): Open-Source Ecotone Fist-Bump Waveguide Commons & Madras Sanctuary Guide"
  },
  WOOKIW_EWOK: {
    repo: "wookiw-ewok",
    payloadFile: "wookiw_ewok_github_payload_v5.0.2.json",
    releaseTag: "v5.0.2",
    releaseTitle: "Wookiw-Ewok (WikiWeWalk) v5.0.2 — Na-Dene & Bergson Waveguide + Open Commons Wiki",
    description: "Wookiw-Ewok (WikiWeWalk): Decentralized Open-Source Knowledge Wiki, Na-Dene & Bergson Waveguides, and Madras Slate Pearls"
  },
  EPIGENETIC_PREPRINT: {
    repo: "epigenetic-state-dispatch",
    payloadFile: "epigenetic_dispatch_github_payload_v1.0.0.json",
    releaseTag: "v1.0.0",
    releaseTitle: "Hysteretic Ternary State Tagging & Matrix-Free Lanczos Saddle Escape (v1.0.0 Preprint & Suite)",
    description: "Reproducible nonlinear optimization preprint & NumPy benchmark suite: Dual-rail RC hysteresis, L-BFGS & 10-step HVP Lanczos (1,1) saddle escape"
  }
};

/**
 * STEP 1 FUNCTION: Pushes all 4 colorful repos (including binary PDFs & SVG banners)!
 */
function pushAllFourCampfireRepos_v5_0_2() {
  const summary = [];
  [
    QUAD_REPO_TARGETS.OS_KERNEL,
    QUAD_REPO_TARGETS.HAPPY_HOBO,
    QUAD_REPO_TARGETS.WOOKIW_EWOK,
    QUAD_REPO_TARGETS.EPIGENETIC_PREPRINT
  ].forEach(function(cfg) {
    summary.push(executeAtomicPushV502_(cfg));
  });
  Logger.log("[ALL 4 CAMPFIRE REPOS PUSHED] " + JSON.stringify(summary, null, 2));
  return summary;
}

/**
 * STEP 3 FUNCTION: Run AFTER flipping the 4 repo switches ON at zenodo.org/account/settings/github/
 * Cuts formal GitHub Releases so Zenodo auto-ingests .zenodo.json with zero manual typing!
 */
function cutZenodoReleasesAllFour_v5_0_2() {
  const props = PropertiesService.getScriptProperties();
  const token = props.getProperty("GITHUB_TOKEN");
  if (!token) throw new Error("Missing GITHUB_TOKEN in Script Properties.");
  const owner = props.getProperty("GITHUB_OWNER") || GITHUB_OWNER_V502;

  const releases = [];
  [
    QUAD_REPO_TARGETS.OS_KERNEL,
    QUAD_REPO_TARGETS.HAPPY_HOBO,
    QUAD_REPO_TARGETS.WOOKIW_EWOK,
    QUAD_REPO_TARGETS.EPIGENETIC_PREPRINT
  ].forEach(function(cfg) {
    const repoInfo = ghRequestV502_(token, "GET", "/repos/" + owner + "/" + cfg.repo);
    const activeBranch = repoInfo.default_branch || DEFAULT_BRANCH_V502;
    const refData = ghRequestV502_(token, "GET", "/repos/" + owner + "/" + cfg.repo + "/git/ref/heads/" + activeBranch);
    const headSha = refData.object.sha;
    let tagToUse = cfg.releaseTag;
    try {
      const rel = ghRequestV502_(token, "POST", "/repos/" + owner + "/" + cfg.repo + "/releases", {
        tag_name: tagToUse,
        target_commitish: headSha,
        name: cfg.releaseTitle,
        body: cfg.description + "\n\nAutomated DataCite archival metadata provided in `.zenodo.json` and `CITATION.cff`.",
        draft: false,
        prerelease: false
      });
      releases.push({ repo: cfg.repo, tag: tagToUse, release_url: rel.html_url });
    } catch (e) {
      // If tag already existed before Zenodo toggle was flipped, mint clean `.1` Zenodo hook tag
      const bumpTag = tagToUse + "-zenodo";
      const rel2 = ghRequestV502_(token, "POST", "/repos/" + owner + "/" + cfg.repo + "/releases", {
        tag_name: bumpTag,
        target_commitish: headSha,
        name: cfg.releaseTitle + " (Zenodo Archive)",
        body: cfg.description + "\n\nAutomated DataCite archival metadata provided in `.zenodo.json` and `CITATION.cff`.",
        draft: false,
        prerelease: false
      });
      releases.push({ repo: cfg.repo, tag: bumpTag, release_url: rel2.html_url });
    }
  });
  Logger.log("[ALL 4 ZENODO RELEASES PUBLISHED] " + JSON.stringify(releases, null, 2));
  return releases;
}

function executeAtomicPushV502_(targetCfg) {
  const props = PropertiesService.getScriptProperties();
  const token = props.getProperty("GITHUB_TOKEN");
  if (!token) throw new Error("Missing GITHUB_TOKEN in Project Settings -> Script Properties.");

  const owner = props.getProperty("GITHUB_OWNER") || GITHUB_OWNER_V502;
  const iter = DriveApp.getFilesByName(targetCfg.payloadFile);
  if (!iter.hasNext()) {
    throw new Error("Payload file not found in Google Drive: " + targetCfg.payloadFile);
  }

  const payload = JSON.parse(iter.next().getBlob().getDataAsString());
  if (payload.human_approved === false) {
    Logger.log("[HOLD] " + targetCfg.payloadFile + " has human_approved=false.");
    return { repo: targetCfg.repo, status: "HELD" };
  }

  ensureGitHubRepoExistsV502_(token, owner, targetCfg.repo, targetCfg.description);

  const repoInfo = ghRequestV502_(token, "GET", "/repos/" + owner + "/" + targetCfg.repo);
  const branch = repoInfo.default_branch || payload.branch || DEFAULT_BRANCH_V502;
  const refData = ghRequestV502_(token, "GET", "/repos/" + owner + "/" + targetCfg.repo + "/git/ref/heads/" + branch);
  const headSha = refData.object.sha;
  const commitData = ghRequestV502_(token, "GET", "/repos/" + owner + "/" + targetCfg.repo + "/git/commits/" + headSha);
  const baseTreeSha = commitData.tree.sha;

  const treeEntries = [];
  (payload.files || []).forEach(function(item) {
    let b64Content = "";
    if (item.encoding === "base64") {
      b64Content = item.content;
      if (b64Content.length * 0.75 > MAX_LINUS_LAW_BLOB_BYTES_V502) {
        throw new Error("[BLOB GUARD] Base64 file exceeds 2 MB ceiling: " + item.path);
      }
    } else {
      const rawBytes = Utilities.newBlob(item.content || "").getBytes();
      if (rawBytes.length > MAX_LINUS_LAW_BLOB_BYTES_V502) {
        throw new Error("[BLOB GUARD] UTF-8 file exceeds 2 MB ceiling: " + item.path);
      }
      b64Content = Utilities.base64Encode(rawBytes);
    }

    const blobResp = ghRequestV502_(token, "POST", "/repos/" + owner + "/" + targetCfg.repo + "/git/blobs", {
      content: b64Content,
      encoding: "base64"
    });
    treeEntries.push({
      path: item.path,
      mode: item.path.slice(-3) === ".sh" ? "100755" : "100644",
      type: "blob",
      sha: blobResp.sha
    });
  });

  const newTree = ghRequestV502_(token, "POST", "/repos/" + owner + "/" + targetCfg.repo + "/git/trees", {
    base_tree: baseTreeSha,
    tree: treeEntries
  });

  const newCommit = ghRequestV502_(token, "POST", "/repos/" + owner + "/" + targetCfg.repo + "/git/commits", {
    message: payload.commit_message || ("Release " + targetCfg.repo + " " + targetCfg.releaseTag),
    tree: newTree.sha,
    parents: [headSha]
  });

  ghRequestV502_(token, "PATCH", "/repos/" + owner + "/" + targetCfg.repo + "/git/refs/heads/" + branch, {
    sha: newCommit.sha,
    force: false
  });

  const receipt = {
    status: "SYNC_COMPLETE",
    repository: owner + "/" + targetCfg.repo,
    version: payload.version || targetCfg.releaseTag,
    commit_sha: newCommit.sha,
    synced_at_utc: new Date().toISOString(),
    files_pushed: treeEntries.length
  };
  DriveApp.createFile(
    "github_sync_receipt_" + targetCfg.repo + "_" + (payload.version || targetCfg.releaseTag) + ".json",
    JSON.stringify(receipt, null, 2),
    MimeType.PLAIN_TEXT
  );
  Logger.log("[SYNC COMPLETE] " + JSON.stringify(receipt));
  return receipt;
}

function ensureGitHubRepoExistsV502_(token, owner, repo, description) {
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
    ghRequestV502_(token, "POST", "/user/repos", {
      name: repo,
      description: description,
      private: false,
      auto_init: true
    });
    Utilities.sleep(2000);
  }
}

function ghRequestV502_(token, method, endpoint, bodyObj) {
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
