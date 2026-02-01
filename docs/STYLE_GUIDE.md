# Style Guide

Writing conventions and terminology standards for the Cleanroom website, blog posts, and technical documentation.

## Air-Gap Terminology

| Context | Form | Example |
|---------|------|---------|
| General noun | "air gap" (two words) | "data crosses the air gap" |
| General adjective | "air-gapped" (hyphenated) | "an air-gapped system" |
| General verb/gerund | "air-gapping" (hyphenated) | "why air-gapping matters" |
| Product names | "AirGap" (CamelCase) | "AirGap Transfer", "AirGap Deploy" |
| CLI commands/paths | lowercase hyphenated | `airgap-transfer pack`, `/docs/deploy/` |

**Never use** "airgapped" or "airgap" (single word) when referring to the general concept. The single-word form is reserved for product identifiers, slugs, and CLI commands.

## Tone

Tone varies by context:

- **Technical documentation** (`technical-docs`): Technical and direct. Avoid marketing language.
- **Blog posts**: Less formal tone is fine. Conversational writing is encouraged.
- **Top-level pages**: Marketing language is acceptable where appropriate, but keep it grounded.

## Formatting Conventions

### Headings

- Use **sentence case** for section headings (`## What you need to know`)
- Use **title case** in blog post `title` frontmatter (`title: "Packaging Rust Applications for Air-Gapped Systems"`)

### Product references

- Use the full product name on first mention: "AirGap Transfer", "AirGap Deploy", "Cleanroom Whisper"
- After context is established, shorter references are acceptable

### Lists

- Use **bold lead-in** for list items when each item is a distinct concept:
  ```markdown
  - **Buy from reputable sources.** Purchase directly from manufacturers...
  ```

### Links

- Cross-link to related blog posts where relevant
- Use relative paths: `/blog/slug`, `/docs/project/page.html`

### Code references

- Use backticks for commands, file paths, and config values: `airgap-deploy prep`, `conf.py`
