# Versioning & Branching Guide

How documentation and code are versioned, branched, and deployed across Cleanroom Labs projects.

## Standards Alignment

This workflow is designed to satisfy the configuration management requirements of:

- **ISO/IEC/IEEE 12207:2017** (Software Life Cycle Processes) — requires configuration identification, baseline management, change control, and status accounting
- **ISO/IEC/IEEE 29148:2018** (Requirements Engineering) — defines how requirements documents (SRS, use cases) should be managed and versioned
- **IEEE 828** (Configuration Management Plans) — requires unique identification of configuration items, controlled baselines, and audit trails
- **ISO/IEC/IEEE 29119** (Software Testing) — defines test documentation standards including versioned test plans

These standards prescribe *what* is needed (identifiable baselines, change control, traceability) but not *how* to implement it. The approach below uses Semantic Versioning and git tags to satisfy these requirements.

### How this workflow satisfies IEEE/ISO requirements

| Requirement | How it's satisfied |
|---|---|
| **Configuration identification** | SemVer tags uniquely identify every baseline (`v1.0.0`, `v1.0.0-rc.1`) |
| **Baseline management** | Git tags are immutable snapshots of code + documentation together |
| **Change control** | Pull requests with review required before merging to `main` |
| **Status accounting** | Tag history + `versions.json` manifest track all released versions |
| **Traceability** | Submodule pointers in each tag link exact documentation to exact code |
| **Audit trail** | Git history provides complete change history with author attribution |

## Version Lifecycle

Use standard [Semantic Versioning](https://semver.org/) with pre-release identifiers.

### Stages

| Stage | Tag format | What it means |
|-------|-----------|---------------|
| **dev** | No tag (tracks `main`) | Active development. Documentation and code are in flux. Use cases and requirements are being written. |
| **beta** | `v1.0.0-beta.1` | Requirements mostly locked. Code is being written. Design documents and test specifications are in progress. Suitable for review. |
| **rc** | `v1.0.0-rc.1` | Feature-complete. All documentation, code, and tests are believed ready. Only critical fixes from this point. |
| **release** | `v1.0.0` | Shipped. Documentation matches released code exactly. This is a controlled baseline. |

The `.1` suffix is the iteration counter within a pre-release stage (per SemVer 2.0.0, section 9). It allows multiple iterations: `v1.0.0-beta.1` → `v1.0.0-beta.2` → `v1.0.0-rc.1` → `v1.0.0-rc.2` → `v1.0.0`. SemVer-aware tools sort these in the correct order automatically.

### Typical progression

```
Requirements & use cases drafted
        │
        ▼
v1.0.0-beta.1  ← "Here's what we're building and why"
        │
    Code development, design docs, test specs
    (iterate — adjust requirements if needed)
        │
        ▼
v1.0.0-beta.2  ← "Updated after design review"  (optional)
        │
    Feature freeze, final documentation polish
        │
        ▼
v1.0.0-rc.1    ← "We believe this is ready"
        │
    Final review, only critical fixes
        │
        ▼
v1.0.0         ← RELEASE (controlled baseline)
```

### What each stage means for documentation

| Document type | beta | rc | release |
|---|---|---|---|
| Use cases | Mostly complete | Frozen | Frozen |
| Requirements (SRS) | Mostly complete | Frozen | Frozen |
| Design (SDD) | In progress | Complete | Frozen |
| Test specifications | In progress | Complete | Frozen |
| User guides | Drafts | Complete | Frozen |

"Frozen" means changes require a new version bump (e.g., `rc.1` → `rc.2`).

### When to bump versions

- **Patch** (`1.0.0` → `1.0.1`): Bug fixes, documentation corrections, no feature changes
- **Minor** (`1.0.0` → `1.1.0`): New features, new use cases, backwards-compatible
- **Major** (`1.0.0` → `2.0.0`): Breaking changes, major architectural shifts

## Branching Strategy

### Trunk-based development

All repos (documentation and future code repos) use the same strategy:

```
main ─────●─────●─────●─────●─────●─────●──── (continuous)
           \         /       │           │
            feature-1       tag          tag
                          v1.0.0-beta.1  v1.0.0
```

- **`main`** is the single long-lived branch. All work integrates here.
- **Feature branches** are short-lived (days, not weeks). Created from `main`, merged back via pull request.
- **Tags** mark baselines. Tags are the version system — not branches.

### Why not Git Flow (main + develop)?

Git Flow uses a separate `develop` branch for integration and reserves `main` for releases. This adds overhead:

- Every change requires an extra merge (`develop` → `main` at release time)
- Two branches to keep in sync
- Merge conflicts between long-lived branches
- Release process is more complex

For a small team, trunk-based development is simpler and equally rigorous. Tags provide the same "controlled release point" that a release branch would, without the overhead.

If the team grows or you need concurrent maintenance of old versions, you can add release branches later (e.g., `release/1.x`) without changing the day-to-day workflow.

### Branch protection

Configure on `main`:
- Require pull request reviews before merging
- Require status checks to pass (CI builds, docs build)
- No force-push

This satisfies the IEEE 828 change control requirement.

### How tags work with submodules

When a project code repo is tagged:

```
whisper/                          ← tagged v1.0.0
├── src/                          ← code at that point
├── docs/                         ← submodule pointer → cleanroom-whisper-docs @ abc123
│   └── (cleanroom-whisper-docs @ abc123)
│       ├── source/
│       │   ├── requirements/     ← requirements at that point
│       │   ├── design/           ← design docs at that point
│       │   └── testing/          ← test specs at that point
│       └── common/ → def456     ← shared config at that point
└── Cargo.toml
```

The tag captures:
1. The exact code
2. The exact documentation (via submodule pointer)
3. The exact shared configuration (via nested submodule pointer)

This is a complete, auditable baseline — one tag, one truth.

## Multi-Version Documentation Hosting

### Build-and-archive (not sphinx-multiversion)

Each tagged version is built once by CI and stored permanently as static files. Old versions are never rebuilt.

```
public/docs/
├── whisper/
│   ├── latest/           → symlink to newest stable (e.g., 1.0.0)
│   ├── dev/              → rebuilt on every push to main
│   ├── 1.0.0/            → built once from v1.0.0 tag
│   ├── 1.0.0-rc.1/       → built once from v1.0.0-rc.1 tag
│   └── 1.0.0-beta.1/     → built once from v1.0.0-beta.1 tag
├── deploy/
│   └── (same structure)
└── transfer/
    └── (same structure)
```

### How CI handles each trigger

| Trigger | Action |
|---------|--------|
| Push to `main` | Build docs → deploy to `<project>/dev/` |
| Tag `v*-beta.*` | Build docs → deploy to `<project>/<version>/` with beta banner |
| Tag `v*-rc.*` | Build docs → deploy to `<project>/<version>/` with RC banner |
| Tag `v*` (stable) | Build docs → deploy to `<project>/<version>/`, update `latest` pointer |

### Version switcher

A `versions.json` file is updated by CI on each tagged deploy:

```json
[
  {"version": "1.0.0", "url": "/docs/whisper/1.0.0/", "stable": true},
  {"version": "1.0.0-rc.1", "url": "/docs/whisper/1.0.0-rc.1/"},
  {"version": "dev", "url": "/docs/whisper/dev/"}
]
```

The Sphinx theme reads this file to render a version dropdown.

### Banners

- **dev**: "This is development documentation and may change at any time."
- **beta**: "This is pre-release documentation for version X.Y.Z-beta.N."
- **rc**: "This is a release candidate. Report issues before final release."
- **stable**: No banner.

## References

- [Semantic Versioning 2.0.0](https://semver.org/)
- [ISO/IEC/IEEE 12207:2017](https://www.iso.org/standard/63712.html) — Software Life Cycle Processes
- [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html) — Requirements Engineering
- [IEEE 828](https://standards.ieee.org/ieee/828/6163/) — Configuration Management in Systems and Software Engineering
- [ISO/IEC/IEEE 29119](https://www.iso.org/standard/81291.html) — Software and Systems Engineering — Software Testing
- [Trunk-Based Development](https://trunkbaseddevelopment.com/)
