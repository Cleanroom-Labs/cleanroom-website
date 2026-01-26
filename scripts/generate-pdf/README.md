# PDF Generation Tool

Generate a comprehensive PDF report from the Cleanroom Labs website content, including blog posts, technical documentation, and visual screenshots.

## Features

- **Screenshot-based cover page** from hero section
- **Product cards graphic** from "Our Tools" section
- **Table of contents** with clickable navigation
- **All blog posts** sorted by date (newest first)
- **Complete technical documentation** with preserved structure
- **Professional styling** matching brand colors

## Prerequisites

- Python 3.9+
- Built documentation (`npm run build-docs`)
- Running dev server (`npm run dev`) for screenshots

## Installation

```bash
# Install Python dependencies
pip install -r scripts/generate-pdf/requirements.txt

# Install Playwright browser for screenshots (optional)
playwright install chromium
```

## Usage

```bash
# Basic usage (requires dev server running)
python -m scripts.generate-pdf

# With custom output path
python -m scripts.generate-pdf --output custom-output.pdf

# Skip screenshots (use cached or no screenshots)
python -m scripts.generate-pdf --skip-screenshots

# Verbose output
python -m scripts.generate-pdf --verbose

# Show help
python -m scripts.generate-pdf --help
```

## Complete Workflow

```bash
# 1. Build the documentation
npm run build-docs

# 2. Start the dev server (in a separate terminal)
npm run dev

# 3. Generate the PDF
python -m scripts.generate-pdf

# Output: output/cleanroom-labs.pdf
```

## CLI Options

| Option | Description |
|--------|-------------|
| `--output PATH` | Output PDF location (default: `output/cleanroom-labs.pdf`) |
| `--server-url URL` | Dev server URL for screenshots (default: `http://localhost:3000`) |
| `--skip-screenshots` | Use existing screenshots or skip screenshot capture |
| `--verbose, -v` | Enable verbose output |
| `--help` | Show help message |

## Architecture

```
scripts/generate-pdf/
├── __init__.py          # Package initialization
├── __main__.py          # Entry point for python -m
├── main.py              # CLI implementation
├── config.py            # Configuration and design tokens
├── screenshot.py        # Playwright screenshot capture
├── pdf_builder.py       # WeasyPrint PDF assembly
├── extractors/
│   ├── __init__.py
│   ├── base.py          # Base extractor with link handling
│   ├── blog.py          # MDX blog post extraction
│   └── sphinx.py        # Sphinx documentation extraction
└── requirements.txt     # Python dependencies
```

## Dependencies

| Library | Purpose |
|---------|---------|
| **beautifulsoup4** | HTML parsing and content extraction |
| **weasyprint** | HTML-to-PDF conversion with CSS support |
| **pypdf** | PDF merging and bookmark generation |
| **python-frontmatter** | MDX blog post frontmatter parsing |
| **markdown** | Markdown-to-HTML rendering |
| **playwright** | Screenshot capture (optional) |

## Customization

### Colors

Colors are sourced from `cleanroom-theme/tokens/colors.js` and defined in `config.py`:

- **Cover page**: Dark background (`#030712`), emerald accents (`#10b981`)
- **Content pages**: Light background (`#ffffff`), dark text (`#1e293b`)
- **Code blocks**: Light gray background (`#f8fafc`)

### Page Layout

Configurable in `config.py`:

- **Size**: A4
- **Margins**: 20mm all sides
- **Page numbers**: Centered in footer (except cover)

### Content Order

Documentation sections are processed in this order:

1. Cross-project documentation (meta)
2. AirGap Transfer
3. AirGap Deploy
4. Cleanroom Whisper

## Troubleshooting

### "Failed to connect to localhost:3000"

The dev server is not running. Start it in a separate terminal:

```bash
npm run dev
```

### "Playwright not installed"

Install Playwright and the Chromium browser:

```bash
pip install playwright
playwright install chromium
```

### "WeasyPrint not found" or "cannot load library"

WeasyPrint requires system dependencies. On macOS:

```bash
brew install pango glib
pip install weasyprint

# If you get library loading errors, set the library path:
export DYLD_LIBRARY_PATH=/opt/homebrew/lib
python -m scripts.generate-pdf
```

On Ubuntu/Debian:

```bash
apt-get install libpango-1.0-0 libpangocairo-1.0-0 libglib2.0-0
pip install weasyprint
```

### Images not appearing

Ensure the docs are built before generating the PDF:

```bash
npm run build-docs
```

### Large PDF file size

Screenshots significantly increase file size. Use `--skip-screenshots` for a smaller PDF without cover images.

## Output

The generated PDF includes:

1. **Cover page** - Hero screenshot, branding, tagline
2. **Table of contents** - Clickable links to all sections
3. **Blog posts** - All MDX posts with metadata, sorted by date
4. **Technical documentation** - Complete Sphinx docs with code blocks

PDF bookmarks are added for major sections for easy navigation.
