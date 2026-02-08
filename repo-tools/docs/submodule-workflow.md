# Nested Submodules and Git Worktrees: A Developer's Guide

This project uses a three-level nested submodule architecture to manage documentation across multiple independent projects. This post explains why, what that means in practice, and how git worktrees make the workflow survivable.

## The Architecture

The full structure looks like this:

```
cleanroom-website/
├── cleanroom-technical-docs/
│   ├── cleanroom-whisper-docs/
│   │   └── source/cleanroom-theme/
│   ├── airgap-deploy-docs/
│   │   └── source/cleanroom-theme/
│   ├── airgap-transfer-docs/
│   │   └── source/cleanroom-theme/
│   └── source/cleanroom-theme/
└── cleanroom-theme/
```

Three levels of nesting, each serving a distinct purpose:

1. **Level 1: Website → Technical Docs.** The website repo pins a single submodule (`cleanroom-technical-docs`) that aggregates all project documentation into one Sphinx build.
2. **Level 2: Technical Docs → Project Docs.** The aggregator contains submodules for each project's documentation (`cleanroom-whisper-docs`, `airgap-deploy-docs`, `airgap-transfer-docs`), plus a copy of the shared theme.
3. **Level 3: Project Docs → Theme.** Each project doc repo embeds the shared theme (`cleanroom-theme`) so it can build independently without the aggregator.

The theme submodule appears at every level. This is intentional—it allows each project to build its own documentation in isolation while maintaining consistent styling. See [ARCHITECTURE.md](../../docs/ARCHITECTURE.md) for design rationale and alternatives considered.

## Complexities of Deeply Nested Submodules

Working with this setup day-to-day surfaces a few recurring realities.

### Detached HEAD is the Default State

Every submodule checks out a specific commit, not a branch. Running `git status` inside any submodule shows `HEAD detached at <sha>`. This is correct behavior, not an error. To make changes, you `git checkout main` first, do your work, commit, then update the parent repo to point to the new commit.

### Three-Commit Propagation

A change to project documentation requires three separate commits to reach the website:

1. Commit in the project docs repo (e.g., `airgap-deploy-docs`)
2. Commit in `cleanroom-technical-docs` to update the submodule pointer
3. Commit in `cleanroom-website` to update its submodule pointer

Each commit records a new SHA, and the parent must be updated to reference it. There's no shortcut. The `repo-tools push` command automates this, but the fundamental mechanics remain.

### Local-Only Submodule URLs

All submodules in this project point to local filesystem paths (e.g., `/Users/.../cleanroom-theme`), not remote URLs. The main website repo has no remote. This means `git submodule update --init --recursive` resolves against local directories, and cloning the repo on a new machine requires those paths to exist. This is a deliberate choice for an air-gapped development environment where network access is unavailable.

### Theme Duplication

The `cleanroom-theme` submodule is referenced six times across the tree—once at the website root, once inside the technical docs aggregator, and once inside each of the three project doc repos. They all point to the same source repo, but each is an independent checkout. Updating the theme means updating it in every location, which is handled by `repo-tools sync`.

### Submodule Drift

If you work in a project docs repo directly (outside the website tree), its commits advance independently. The parent repos still point to the old SHAs until you explicitly update them. `git status` in the parent will show `modified: <submodule> (new commits)`, which is easy to miss. The `repo-tools check` command helps catch this.

## Advantages

Despite the complexity, this architecture provides real benefits.

**Explicit version coupling.** Every level records exact SHAs. You always know which version of every project's docs a given website release includes. There's no ambiguity about what was deployed.

**Independent ownership.** Each project team owns their documentation repo. They can commit, review, and tag releases without coordinating with other teams or the website maintainer.

**Standalone builds.** Because each project embeds the theme, any project can build its own documentation in isolation. You don't need the full website tree to work on a single project's docs.

**Dual-homing.** Code repositories can include their documentation as a submodule. The same docs repo that lives inside the aggregator can also live inside the code repo, so documentation stays close to the code it describes.

## Disadvantages

**Steep learning curve.** Git submodules are already unfamiliar territory for many developers. Three levels of nesting compounds this. Detached HEADs, recursive updates, and multi-commit propagation are confusing until you've internalized the model.

**Multi-step propagation.** Every change requires touching multiple repos. Even with automation scripts, this is slower than editing files in a monorepo.

**Tooling assumptions.** Most git GUIs, IDE integrations, and CI systems assume a single-repo workflow. Nested submodules expose edge cases and gaps in tooling. Some operations that should be simple (like "show me what changed") require running commands at multiple levels of the tree.

**Slow clone and init.** `git clone --recursive` must descend through every level and initialize every submodule. With local URLs this is fast, but on a fresh machine you need all source repos present first.

## Git Worktrees to the Rescue

A common scenario: you're working on a documentation update and need to check something on a different branch—maybe to compare output or cherry-pick a fix. With submodules, switching branches is expensive. `git checkout other-branch` in the parent doesn't automatically update submodules, and `git submodule update --recursive` can take a while and clobber local changes.

Git worktrees solve this by letting you check out multiple branches simultaneously in separate directories. Each worktree shares the same `.git` object store, so it's lightweight. But there's a catch: `git worktree add` doesn't initialize submodules, and with local submodule URLs, `git submodule update --init --recursive` in a new worktree fails because the URLs resolve relative to the main worktree's checkout.

### The `add-worktree` Function

This zsh function handles both problems—creating the worktree and recursively initializing submodules with corrected URLs:

```zsh
_init_submodules_from_worktree() {
    local ref_worktree="$1"

    [[ -f .gitmodules ]] || return 0

    git submodule init || return 1

    # Override each submodule URL to point to the main worktree's checked-out copy
    local key subpath name
    while read key subpath; do
        name="${key#submodule.}"
        name="${name%.path}"
        git config "submodule.$name.url" "$ref_worktree/$subpath"
    done < <(git config --file .gitmodules --get-regexp '^submodule\..*\.path$')

    git submodule update || return 1

    # Recurse into each submodule
    while read key subpath; do
        (cd "$subpath" && _init_submodules_from_worktree "$ref_worktree/$subpath") || return 1
    done < <(git config --file .gitmodules --get-regexp '^submodule\..*\.path$')

    # Restore original remote URLs at all levels
    git submodule sync --recursive
}

add-worktree() {
    if [[ $# -ne 2 ]]; then
        echo "Usage: add-worktree <branch-name> <path>" >&2
        return 1
    fi

    local main_worktree
    main_worktree="$(git rev-parse --show-toplevel)" || return 1

    git worktree add -b "$1" "$2" || return 1
    cd "$2" || return 1

    _init_submodules_from_worktree "$main_worktree" || {
        echo "Warning: submodule update failed. Worktree created at $2 on branch $1." >&2
        return 1
    }
}
```

Here's what happens when you run `add-worktree my-feature ../cleanroom-website-my-feature`:

1. `git worktree add` creates a new worktree at the given path on a new branch.
2. `_init_submodules_from_worktree` runs in the new worktree. It reads `.gitmodules` and temporarily overrides each submodule's URL to point to the **main worktree's** checked-out copy of that submodule. This is the key insight—since submodule URLs are local paths, the new worktree needs to resolve them against an existing checkout rather than the original paths in `.gitmodules`.
3. After `git submodule update` succeeds, the function recurses into each submodule and repeats the process for nested submodules. This handles all three levels.
4. Finally, `git submodule sync --recursive` restores the original URLs from `.gitmodules` so that future operations (like pulling updates from the source repos) work correctly.

The result is a fully initialized worktree with all submodules at all levels checked out and ready to use.

## Propagating Changes Through the Repository

Once you've committed a change inside a nested submodule, it needs to bubble up through every parent. Manually, that means:

```bash
# 1. Commit inside the project docs repo
cd cleanroom-technical-docs/airgap-deploy-docs
git add -A && git commit -m "Update deployment guide"

# 2. Update the pointer in technical-docs
cd ..
git add airgap-deploy-docs
git commit -m "Update airgap-deploy-docs submodule"

# 3. Update the pointer in the website
cd ..
git add cleanroom-technical-docs
git commit -m "Update cleanroom-technical-docs submodule"
```

This gets tedious fast—especially when multiple submodules have changed. The `repo-tools push` command automates the push side of this workflow. It discovers every repo in the hierarchy, performs a topological sort (children before parents), validates that each repo is on a branch with no uncommitted changes, and pushes them in the correct order.

```bash
# Preview what would be pushed
repo-tools push --dry-run

# Push all repos with unpushed commits
repo-tools push

# Skip validation for recovery scenarios
repo-tools push --force
```

The topological ordering matters because pushing a parent before its children would create a state where the parent references commits that don't exist on the remote yet.

## Syncing the Theme

When the shared theme changes—a new color, an updated layout, a bug fix—it needs to be updated in every location it appears. The `repo-tools sync` command handles this end-to-end:

1. Resolves the target commit (defaults to the latest on `main` in the standalone theme repo, or accepts a specific SHA)
2. Discovers all theme submodule locations by parsing `.gitmodules` at every level
3. Validates that parent repos are in sync with their remotes
4. Updates each theme submodule to the target commit
5. Commits the changes bottom-up through the hierarchy
6. Pushes everything (unless `--no-push` is specified)

```bash
# Sync all theme instances to latest, commit, and push
repo-tools sync

# Sync to a specific commit
repo-tools sync abc1234

# Preview without making changes
repo-tools sync --dry-run

# Commit but don't push
repo-tools sync --no-push

# Also check for stale generated files (e.g., icons) after syncing
repo-tools sync --verify
repo-tools sync --rebuild  # auto-regenerate stale files
```

Without this script, you'd need to manually `cd` into six different directories, run `git checkout <sha>` in each, then commit your way back up the tree. The script reduces a fifteen-step process to one command.

## Merging Worktree Changes Back

After finishing work in a worktree, you need to integrate the changes into your main branch. The workflow is straightforward:

```bash
# From the main worktree
cd ~/Projects/cleanroom-website

# Merge the feature branch
git merge my-feature

# If the feature touched submodule pointers, update them
git submodule update --recursive

# Push everything through the hierarchy
repo-tools push
```

If you have multiple worktrees with changes to merge, do them sequentially. Each merge may update submodule pointers, and you want to resolve any conflicts at each step rather than accumulating them:

```bash
git merge feature-a
git submodule update --recursive
# verify, then continue

git merge feature-b
git submodule update --recursive
# resolve conflicts if feature-b touched the same submodules as feature-a

repo-tools push
```

## Managing Worktrees and Branches

Worktrees accumulate if you don't clean them up. A few commands to keep things tidy:

```bash
# See all worktrees
git worktree list

# Remove a worktree after you're done with it
git worktree remove ../cleanroom-website-my-feature

# Clean up stale entries (e.g., if you deleted the directory manually)
git worktree prune

# Delete the branch after merging
git branch -d my-feature
```

A naming convention helps keep things organized. Use the project directory name as a base and append the branch name as a suffix:

```
~/Projects/
├── cleanroom-website/                  # main worktree (main branch)
├── cleanroom-website-wt1/              # worktree 1 (feature branch)
├── cleanroom-website-wt2/              # worktree 2 (another feature)
└── cleanroom-website-hotfix/           # worktree for a quick fix
```

Sibling directories make it easy to `cd ../<other-worktree>` and keep everything visible in your file manager. The `-wt1`, `-wt2` pattern works well for short-lived worktrees; use descriptive names for longer-lived ones.

When you're done with a batch of work, clean up in one pass:

```bash
git worktree list                       # see what's active
git worktree remove ../cleanroom-website-wt1
git worktree remove ../cleanroom-website-wt2
git worktree prune
git branch -d feature-a feature-b      # delete merged branches
```

## Parallel Development with AI Coding Agents

Worktrees unlock a powerful workflow when combined with AI coding agents: true parallel development on a single repository.

The setup is simple. You have three independent tasks—say, updating the deploy docs, adding a new section to the whisper docs, and fixing a theme issue. Instead of working through them sequentially, you create a worktree for each:

```bash
cd ~/Projects/cleanroom-website
add-worktree update-deploy-docs   ../cleanroom-website-wt1
add-worktree expand-whisper-docs  ../cleanroom-website-wt2
add-worktree fix-theme-spacing    ../cleanroom-website-wt3
```

Each worktree has its own fully initialized checkout with all submodules at every level. Now you launch a coding agent in each one—three separate terminal sessions, three instances of Claude Code, each pointed at a different directory:

```bash
# Terminal 1
cd ../cleanroom-website-wt1 && claude

# Terminal 2
cd ../cleanroom-website-wt2 && claude

# Terminal 3
cd ../cleanroom-website-wt3 && claude
```

The agents work simultaneously without interfering with each other. Each operates in its own worktree with its own branch, its own working directory, and its own submodule state. There are no lock conflicts because git worktrees are designed for concurrent access to the same repository.

When the agents finish, you review each worktree's changes, then merge sequentially from the main worktree:

```bash
cd ~/Projects/cleanroom-website

git merge update-deploy-docs
git submodule update --recursive

git merge expand-whisper-docs
git submodule update --recursive

git merge fix-theme-spacing
git submodule update --recursive

# Push everything in one pass
repo-tools push
```

Then clean up:

```bash
git worktree remove ../cleanroom-website-wt1
git worktree remove ../cleanroom-website-wt2
git worktree remove ../cleanroom-website-wt3
git worktree prune
git branch -d update-deploy-docs expand-whisper-docs fix-theme-spacing
```

The key insight is that worktrees give each agent a complete, isolated environment while the shared `.git` object store means every branch and commit is immediately visible from the main worktree when it's time to merge. You get the parallelism of multiple clones without the disk cost or the hassle of syncing between them.

## Closing Thoughts

Nested submodules are a power tool. They solve real problems—version coupling, independent ownership, standalone builds—but they demand an understanding of git's object model that goes beyond typical usage. Git worktrees complement submodules well by removing the need to context-switch destructively. Together, they make it practical to maintain a multi-project documentation platform where each piece can evolve independently while the whole remains coherent.
