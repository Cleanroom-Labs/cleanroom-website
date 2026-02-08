# Blog Release Plan

Weekly cadence, starting after v1.0.0 software release. Each post is released on the same day of the week (recommend Tuesday or Wednesday — highest engagement on HN/Reddit).

## Strategy

Lead with standalone, discussion-generating content that provides value independent of the product. Build credibility and audience before introducing the tools. On HackerNews and Reddit, genuinely useful content with an organic connection to a product performs far better than overt advertising.

The sequence follows a narrative arc: **Problem → Philosophy → Strategy → Threats → Solution → Practice → Community → New Features**

## Release Schedule

### Phase 1: Establish the Problem (Weeks 1-2)

| Week | Post | Slug | Why This Order |
|------|------|------|----------------|
| 1 | **Wired for Surveillance** | `wired-for-surveillance` | The strongest standalone piece. CALEA, Salt Typhoon, documented misuse — this will generate organic discussion on HN/Reddit regardless of the product. Establishes credibility and signals that the team understands the problem space deeply. |
| 2 | **The Case for Privacy** | `the-case-for-privacy` | Companion to Week 1. Broadens the conversation from "surveillance is a problem" to "privacy is a right." The psychological research (chilling effects, self-fulfilling prophecy) and historical examples (COINTELPRO, Stasi) give people new frameworks to think with. |

**Social media angle:** Submit these as articles, not product announcements. The content stands on its own. Comments will naturally ask "so what do we do about it?" — which sets up Week 3.

### Phase 2: Introduce the Strategy (Week 3)

| Week | Post | Slug | Why This Order |
|------|------|------|----------------|
| 3 | **Why Air-Gapping?** | `why-air-gapping` | Now that the problem is established, introduce air-gapping as the architectural response. This post links back to the surveillance and quantum era posts, creating a natural connection for readers who discovered us through Weeks 1-2. The honest treatment of tradeoffs builds trust. |

**Social media angle:** "Show HN" style on HN, or a discussion post on r/netsec, r/privacy, r/selfhosted. Frame it as a thesis, not an ad.

### Phase 3: Deep Dives (Weeks 4-6)

| Week | Post | Slug | Why This Order |
|------|------|------|----------------|
| 4 | **Air-Gapping in the Quantum Era** | `air-gapping-in-the-quantum-era` | "Harvest now, decrypt later" is timely and attention-grabbing. Connects to the surveillance post (Week 1) — passive collection for future decryption is the other side of active surveillance. |
| 5 | **Air-Gapping Your Software Supply Chain** | `air-gapping-your-software-supply-chain` | Supply chain attacks (xz-utils, SolarWinds) are well-known on HN. This post maps CISA guidance to air-gapped workflows — practical and authoritative. |
| 6 | **USB Security for Airgap Data Transfers** | `usb-security-airgap-transfers` | The most practical/tactical post in the threat layer. Transitions from "why" to "how" — natural lead-in to the tools. |

**Social media angle:** Each targets a different subreddit/community. Quantum era → r/cybersecurity, r/privacy. Supply chain → r/programming, r/devops. USB security → r/netsec, r/homelab.

### Phase 4: The Tools (Week 7)

| Week | Post | Slug | Why This Order |
|------|------|------|----------------|
| 7 | **Privacy-First Tools for Air-Gapped Environments** | `introducing-airgap-tools` | Product announcement. By now, six weeks of content have established the problem, the philosophy, the strategy, and the threats. The tools are the payoff. Readers already understand *why* these exist. |

**Social media angle:** This is the "Show HN" / "Launch HN" post. Link to the product, mention it's open source, keep it factual. The six weeks of prior content serve as proof of domain expertise.

### Phase 5: Demos (Weeks 8-10)

| Week | Post | Slug | Why This Order |
|------|------|------|----------------|
| 8 | **Capturing Meeting Notes with Your Voice — No Cloud Required** | `demo-whisper-quick-capture` | Lead with the most relatable demo. Everyone takes meeting notes. The "no cloud" angle connects back to the privacy narrative. Lowest barrier to entry for new readers. |
| 9 | **Packaging Rust Applications for Air-Gapped Systems** | `demo-deploy-rust-app` | More technical audience. Appeals to Rust community (strong on HN) and DevOps/release engineering. |
| 10 | **Deploying Ollama and Large Models Across the Air Gap** | `demo-transfer-ollama` | AI/ML angle. Running local LLMs in air-gapped environments is timely and niche — exactly the kind of content that does well on HN. Good capstone because it showcases multiple tools working together. |

**Social media angle:** Each demo targets a specific community. Whisper → r/selfhosted, r/productivity. Rust deploy → r/rust, r/devops. Ollama → r/LocalLLaMA, r/selfhosted.

### Phase 6: Community (Week 11+)

| Week | Post | Slug | Why This Order |
|------|------|------|----------------|
| 11 | **Start a Sneakernet with Your Friends** | `start-a-sneakernet` | A lighter, fun post that reframes the tools for everyday social use. After 10 weeks of establishing the problem, the strategy, and the tools, this shows the human side — sharing files with friends, no cloud required. It's the most shareable post in the series and the best entry point for non-security audiences. |

**Social media angle:** This is the most broadly appealing post. Submit to r/selfhosted, r/datahoarder, r/homelab, and r/privacy. The tone is casual enough for general tech communities. On HN, this is the kind of "why not?" post that generates nostalgic discussion about sneakernets, BBS culture, and the joy of physical media.

### Phase 7: New Features (Week 12+)

| Week | Post | Slug | Why This Order |
|------|------|------|----------------|
| 12 | **Maintaining Air-Gapped Systems with Bills of Materials** | `maintaining-airgapped-systems-with-boms` | Introduces v1.1 features: SBOM/CBOM generation in Deploy and offline vulnerability scanning. After the initial tool launch and demos, this shows the long-term maintenance story — how to keep air-gapped systems secure and up-to-date using Bills of Materials and offline vulnerability databases. Positions the product as a complete lifecycle tool, not just a deployment tool. |

**Social media angle:** Technical and compliance-focused. Submit to r/netsec, r/cybersecurity, r/devops, and r/programming. The SBOM/CBOM angle is timely given U.S. regulatory requirements (2021 executive order, CISA guidance). On HN, the "offline vulnerability scanning" angle is novel and practical.

## Platform-Specific Notes

### HackerNews
- Submit the content-focused posts (Weeks 1-2) as articles, not "Show HN"
- Reserve "Show HN" for Week 7 (tool launch) or Week 3 (thesis)
- Don't submit more than one post per week — HN penalizes perceived self-promotion
- The surveillance and privacy posts are the most likely to reach the front page organically
- Engage genuinely in comments; don't just drop links

### Reddit
- Each post maps to different subreddits — spread across communities rather than hitting one repeatedly
- Key subreddits: r/privacy, r/netsec, r/cybersecurity, r/selfhosted, r/programming, r/rust, r/LocalLLaMA, r/homelab, r/devops
- Follow each subreddit's self-promotion rules (typically <10% of submissions should be your own content)
- The privacy and surveillance posts work well as discussion starters in r/privacy

### General
- Cross-post to Twitter/X, Mastodon, and LinkedIn on the same day
- Each post should have a 2-3 sentence summary optimized for the platform (HN title ≠ Reddit title ≠ tweet)
- Don't publish all platform posts simultaneously — stagger by a few hours to monitor engagement and adjust messaging

## Suggested HN Titles

Titles that work on HN are factual, specific, and avoid marketing language:

| Week | Suggested HN Title |
|------|-------------------|
| 1 | The Law That Wired America for Surveillance — And What Happened Next |
| 2 | The Psychological Case for Privacy: Chilling Effects, Self-Fulfilling Prophecy, and the Panopticon |
| 3 | Why Air-Gapping: Collapsing a Continuous Attack Surface into Discrete Events |
| 4 | Air-Gapping in the Quantum Era: Defending Against Harvest Now, Decrypt Later |
| 5 | Air-Gapping Your Software Supply Chain: Mapping CISA Guidance to Offline Workflows |
| 6 | USB Threat Models for Air-Gapped Data Transfers |
| 7 | Show HN: Privacy-First Tools for Air-Gapped Environments (open source, Rust) |
| 8 | Offline Voice Transcription with No Cloud — Quick Capture for Air-Gapped Systems |
| 9 | Packaging Rust Applications for Deployment to Systems Without Internet |
| 10 | Deploying Ollama and Large Models Across the Air Gap with Multi-USB Orchestration |
| 11 | Start a Sneakernet with Your Friends — File Sharing Without the Cloud |
| 12 | Maintaining Air-Gapped Systems with SBOMs, CBOMs, and Offline Vulnerability Scanning |
