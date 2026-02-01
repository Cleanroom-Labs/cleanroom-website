#!/usr/bin/env python3
"""
CLI entry point for PDF generation.

Usage:
    python -m scripts.generate-pdf [options]

Options:
    --output PATH       Output PDF location (default: output/cleanroom-labs.pdf)
    --server-url URL    Dev server for screenshots (default: http://localhost:3000)
    --skip-screenshots  Use existing screenshots if available
    --verbose          Enable verbose output
    --help             Show this help message
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from extractors.blog import BlogExtractor
from extractors.sphinx import SphinxExtractor
from screenshot import capture_screenshots, PLAYWRIGHT_AVAILABLE
from pdf_builder import build_pdf


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate a comprehensive PDF from the Cleanroom Labs website.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python -m scripts.generate-pdf
    python -m scripts.generate-pdf --output custom-output.pdf
    python -m scripts.generate-pdf --skip-screenshots
    python -m scripts.generate-pdf --verbose

Prerequisites:
    1. Build the docs: npm run build-docs
    2. Start dev server: npm run dev (in separate terminal)
    3. Install dependencies: pip install -r scripts/generate-pdf/requirements.txt
        """,
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="Output PDF location (default: output/cleanroom-labs.pdf)",
    )

    parser.add_argument(
        "--server-url",
        default="http://localhost:3000",
        help="Dev server URL for screenshots (default: http://localhost:3000)",
    )

    parser.add_argument(
        "--skip-screenshots",
        action="store_true",
        help="Skip screenshot capture and use existing screenshots",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output",
    )

    parser.add_argument(
        "--draft",
        action="store_true",
        help="Add a diagonal DRAFT watermark to every page",
    )

    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()

    # Create configuration
    config = Config()
    config.verbose = args.verbose

    print("Cleanroom Labs PDF Generator")
    print("=" * 40)

    # Step 1: Capture screenshots
    screenshots = {}
    if not args.skip_screenshots:
        print("\n1. Capturing screenshots...")

        if not PLAYWRIGHT_AVAILABLE:
            print("   Warning: Playwright not installed. Skipping screenshots.")
            print("   Install with: pip install playwright && playwright install chromium")
        else:
            try:
                screenshots = capture_screenshots(config, args.server_url)
                print(f"   Captured {len(screenshots)} screenshot(s)")
            except RuntimeError as e:
                print(f"   Error: {e}")
                print("   Continuing without screenshots...")
    else:
        print("\n1. Skipping screenshot capture (--skip-screenshots)")
        # Check for existing screenshots
        hero_path = config.paths.screenshots_dir / "hero.png"
        products_path = config.paths.screenshots_dir / "products.png"
        if hero_path.exists():
            screenshots["hero"] = hero_path
        if products_path.exists():
            screenshots["products"] = products_path
        if screenshots:
            print(f"   Found {len(screenshots)} existing screenshot(s)")

    # Step 2: Extract blog posts
    print("\n2. Extracting blog posts...")
    blog_extractor = BlogExtractor(config)
    blog_sections = blog_extractor.extract()
    print(f"   Extracted {len(blog_sections)} blog post(s)")

    # Step 3: Extract Sphinx documentation
    print("\n3. Extracting technical documentation...")
    sphinx_extractor = SphinxExtractor(config)
    docs_sections = sphinx_extractor.extract()
    print(f"   Extracted {len(docs_sections)} documentation page(s)")

    # Step 4: Build PDF
    print("\n4. Building PDF...")
    output_path = args.output or config.paths.output_path

    try:
        result_path = build_pdf(
            blog_sections=blog_sections,
            docs_sections=docs_sections,
            screenshots=screenshots,
            config=config,
            output_path=output_path,
            draft=args.draft,
        )
        print(f"\nSuccess! PDF generated at: {result_path}")
        return 0

    except Exception as e:
        print(f"\nError building PDF: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
