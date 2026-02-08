# Blog Content Guide

This document describes the layered architecture of the blog content and how posts relate to each other.

## Content Layers

| Layer | Purpose | Tone | Posts |
|-------|---------|------|-------|
| **Why privacy matters** | The human, societal, and legal case for privacy | Evidence-based, measured, values-oriented | `wired-for-surveillance.mdx`, `the-case-for-privacy.mdx` |
| **Why air-gap?** | Foundational thesis for air-gapping as a strategy | Technical but accessible, honest about tradeoffs | `why-air-gapping.mdx` |
| **Specific threats** | Deep dives into individual threat vectors | Technical, well-sourced, practical | `air-gapping-in-the-quantum-era.mdx`, `air-gapping-your-software-supply-chain.mdx`, `usb-security-airgap-transfers.mdx` |
| **Tools** | What we built and how they work together | Practical, feature-focused | `introducing-airgap-tools.mdx` |
| **Demos** | Step-by-step walkthroughs of specific workflows | Tutorial-style, hands-on | `demo-deploy-rust-app.mdx`, `demo-transfer-ollama.mdx`, `demo-whisper-quick-capture.mdx` |

## Cross-Referencing Conventions

- **`why-air-gapping.mdx` is the hub.** It links out to threat-specific posts and serves as the entry point for the "why" narrative. Most other posts link back to it.
- **Threat-specific posts** can cross-reference each other where the content is complementary (e.g., quantum era ↔ surveillance).
- **Tool and demo posts** link back to the foundational layers (`why-air-gapping`, `introducing-airgap-tools`) for context.
- **Privacy-layer posts** (`wired-for-surveillance`, `the-case-for-privacy`) are designed to stand alone and be shareable independently. They don't need to reference the tools directly — `why-air-gapping` handles the bridge.

## The `drafts/` Subdirectory

Posts in `content/blog/drafts/` are work-in-progress and not yet published. When a draft is ready for publication, move it to `content/blog/` proper. Links to draft posts from published posts will not resolve until the draft is moved.

## Adding New Content

When writing a new post, consider which layer it belongs to:

1. **Is it about why privacy or security matters in general?** → "Why privacy matters" layer
2. **Is it about why air-gapping specifically is a good strategy?** → "Why air-gap?" layer (rare — this is mostly covered by the hub post)
3. **Is it a deep dive into a specific threat?** → "Specific threats" layer
4. **Is it introducing a tool or capability?** → "Tools" layer
5. **Is it a walkthrough of how to do something?** → "Demos" layer

Each layer builds on the ones above it. A demo post can assume the reader has access to the "why" if they want it, but should be self-contained enough to follow without it.
