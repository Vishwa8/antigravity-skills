---
name: github-skills-sync
description: Syncs skills and files from a GitHub repository into the local .agent/skills/ directory using the GitHub MCP server. Use when the user asks to pull, sync, update, install, or fetch skills from GitHub, or references a GitHub repo URL containing skills. Handles full skill directory trees — SKILL.md, scripts/, references/, and any nested files — without git clone.
---

# GitHub Skills Sync

Pulls any skill (or any file/folder) from a GitHub repository into the local workspace using the **GitHub MCP server** (`mcp_github_get_file_contents`). No `git clone` required — works purely through the API.

---

## When to Use This Skill

- User pastes a GitHub URL pointing to a skill or folder
- User says "pull from GitHub", "sync my skills", "install skill from repo"
- User wants to update locally installed skills from the source repo
- User wants to copy any file or directory from a GitHub repo locally

---

## Workflow

### Step 1 — Parse the Target

Extract from the user's request:

| Field | Example |
| --- | --- |
| GitHub owner | `Vishwa8` |
| Repo name | `antigravity-skills` |
| Branch | `master` (default) |
| Remote path | `.agent/skills/nano-banana-2-image-generation` |
| Local destination | `.agent/skills/` (default) |

If the user provides a GitHub URL, parse it directly:
```
https://github.com/{owner}/{repo}/tree/{branch}/{path}
https://github.com/{owner}/{repo}/blob/{branch}/{path}
```

If destination is not specified, mirror the remote path structure locally.

---

### Step 2 — Discover the Tree

Use `mcp_github_get_file_contents` on the target path. This returns either:
- A **file** (single object with `content` field) → write directly
- A **directory** (array of objects with `type: "file"` or `type: "dir"`) → recurse

**Recursion rule:** For each `type: "dir"` item in the listing, call `mcp_github_get_file_contents` on its `path`. Continue until all leaves are files.

> Parallelize sibling calls where possible for speed.

---

### Step 3 — Write Files Locally

For each file discovered:
1. Extract the `content` field (it is the **decoded text content**, not base64 — the MCP server decodes it for you)
2. Determine the local path by replacing the remote base path with the local destination
3. Use `write_to_file` with `Overwrite: true` to write each file

**Path mapping example:**
```
Remote: .agent/skills/nano-banana-2-image-generation/scripts/generate_image.py
Local dest: d:\Dev\Image-Gen\.agent\skills\
-> Local: d:\Dev\Image-Gen\.agent\skills\nano-banana-2-image-generation\scripts\generate_image.py
```

---

### Step 4 — Confirm

After all files are written, report to the user:
- ✅ List of all files synced with their local paths
- 📁 The local root where the skill was installed
- Any files that were skipped or failed

---

## Full Repo Sync

To sync **all skills** from a repo:
1. Call `mcp_github_get_file_contents` on the root skills path (e.g., `.agent/skills`)
2. For each directory returned (each is one skill), recurse using Step 2
3. Write all files using Step 3

---

## Key Rules

- **Never use `git clone`** — it hangs on Windows due to credential prompts. Always use the GitHub MCP.
- **Always use absolute paths** when writing files locally.
- **`content` is already decoded** — write it as-is (it is a plain string, not base64).
- **Preserve directory structure** exactly as it exists in the remote repo.
- **Overwrite existing files** — local copies are always replaced by the latest from GitHub.

---

## Default Repo

The user's primary skills repo is:
- **Owner:** `Vishwa8`
- **Repo:** `antigravity-skills`
- **Branch:** `master`
- **Skills path:** `.agent/skills`
- **Default local destination:** current workspace `.agent/skills/`

If the user says "sync my skills" without specifying a repo, use these defaults.

---

## Checklist

- [ ] Owner, repo, branch, and remote path identified
- [ ] Root listing fetched via `mcp_github_get_file_contents`
- [ ] All subdirectories recursed
- [ ] All files written locally with `write_to_file`
- [ ] Summary of synced files delivered to user
