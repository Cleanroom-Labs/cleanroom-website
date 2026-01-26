"""
PDF assembly and styling with WeasyPrint.

Generates a single-document PDF with working internal links and page numbers.
"""

from pathlib import Path
from typing import Optional

try:
    from weasyprint import HTML
    from weasyprint.text.fonts import FontConfiguration
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

try:
    from pypdf import PdfReader, PdfWriter
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False

from config import Config, config as default_config
from extractors.base import ContentSection


class PDFBuilder:
    """Build PDF from extracted content using single-document approach."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or default_config

        if not WEASYPRINT_AVAILABLE:
            raise ImportError(
                "WeasyPrint is required for PDF generation. "
                "Install with: pip install weasyprint"
            )

        if not PYPDF_AVAILABLE:
            raise ImportError(
                "pypdf is required for PDF bookmarks. "
                "Install with: pip install pypdf"
            )

        self.font_config = FontConfiguration()

    def build(
        self,
        blog_sections: list[ContentSection],
        docs_sections: list[ContentSection],
        screenshots: dict[str, Path],
        output_path: Optional[Path] = None,
    ) -> Path:
        """Build the complete PDF as a single document."""
        output_path = output_path or self.config.paths.output_path

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if self.config.verbose:
            print("\nBuilding PDF as single document...")

        # Build complete HTML document
        html_content = self._build_complete_document(
            blog_sections, docs_sections, screenshots
        )

        # Generate PDF from single HTML
        temp_path = self.config.paths.output_dir / "temp_combined.pdf"
        document = HTML(string=html_content)
        document.write_pdf(str(temp_path), font_config=self.font_config)

        if self.config.verbose:
            print("  Generated combined PDF")

        # Add bookmarks using pypdf
        self._add_bookmarks(temp_path, output_path, blog_sections, docs_sections)

        # Clean up temp file
        if temp_path.exists():
            temp_path.unlink()

        if self.config.verbose:
            print(f"\nPDF generated: {output_path}")

        return output_path

    def _build_complete_document(
        self,
        blog_sections: list[ContentSection],
        docs_sections: list[ContentSection],
        screenshots: dict[str, Path],
    ) -> str:
        """Build complete HTML document with all content."""
        # Build cover page HTML
        cover_html = self._build_cover_html(screenshots)

        # Build TOC HTML
        toc_html = self._build_toc_html(blog_sections, docs_sections)

        # Build screenshots section (after TOC)
        screenshots_html = self._build_screenshots_html(screenshots)

        # Build intro sections (About and Our Tools)
        intro_html = self._build_intro_html()

        # Build content sections HTML
        blog_html = self._build_content_html("Blog Posts", blog_sections) if blog_sections else ""
        docs_html = self._build_content_html("Technical Documentation", docs_sections) if docs_sections else ""

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                {self._get_base_css()}
                {self._get_cover_css()}
                {self._get_toc_css()}
            </style>
        </head>
        <body>
            {cover_html}
            {toc_html}
            {screenshots_html}
            {intro_html}
            {blog_html}
            {docs_html}
        </body>
        </html>
        """

    def _get_base_css(self) -> str:
        """Generate base CSS for all pages with reduced whitespace."""
        colors = self.config.colors
        fonts = self.config.fonts
        layout = self.config.page_layout

        return f"""
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        @page {{
            size: {layout.size};
            margin: {layout.margin_top} {layout.margin_right} {layout.margin_bottom} {layout.margin_left};

            @bottom-center {{
                content: counter(page);
                font-family: {fonts.sans};
                font-size: 10pt;
                color: {colors.docs_text_muted};
            }}
        }}

        @page cover {{
            margin: 0;
            @bottom-center {{
                content: none;
            }}
        }}

        @page toc {{
            @bottom-center {{
                content: counter(page, lower-roman);
            }}
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            font-family: {fonts.sans};
            font-size: 11pt;
            line-height: 1.5;
            color: {colors.docs_text_secondary};
            background: {colors.docs_content_bg};
            margin: 0;
            padding: 0;
            text-align: justify;
        }}

        h1 {{
            font-size: 24pt;
            font-weight: 700;
            color: {colors.docs_text_primary};
            margin: 1.2em 0 0.4em 0;
            page-break-after: avoid;
            text-align: left;
        }}

        h2 {{
            font-size: 18pt;
            font-weight: 600;
            color: {colors.docs_text_primary};
            margin: 1.4em 0 0.4em 0;
            page-break-after: avoid;
            border-bottom: 1px solid {colors.docs_border};
            padding-bottom: 0.2em;
            text-align: left;
        }}

        h3 {{
            font-size: 14pt;
            font-weight: 600;
            color: {colors.docs_text_primary};
            margin: 1.0em 0 0.3em 0;
            page-break-after: avoid;
            text-align: left;
        }}

        h4, h5, h6 {{
            font-size: 12pt;
            font-weight: 600;
            color: {colors.docs_text_primary};
            margin: 0.8em 0 0.2em 0;
            page-break-after: avoid;
            text-align: left;
        }}

        p {{
            margin: 0.8em 0;
            orphans: 3;
            widows: 3;
            text-align: justify;
            hyphens: auto;
        }}

        a {{
            color: {colors.emerald};
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        ul, ol {{
            margin: 0.4em 0;
            padding-left: 1.5em;
        }}

        li {{
            margin: 0.15em 0;
        }}

        code {{
            font-family: {fonts.mono};
            font-size: 0.9em;
            background: {colors.docs_code_bg};
            color: {colors.docs_code_text};
            padding: 0.15em 0.3em;
            border-radius: 3px;
        }}

        pre {{
            font-family: {fonts.mono};
            font-size: 9pt;
            background: {colors.docs_code_bg};
            color: {colors.docs_code_text};
            padding: 0.75em;
            border-radius: 6px;
            overflow-x: auto;
            page-break-inside: avoid;
            border: 1px solid {colors.docs_border};
            margin: 0.5em 0;
        }}

        pre code {{
            background: none;
            padding: 0;
            font-size: inherit;
        }}

        blockquote {{
            border-left: 4px solid {colors.emerald};
            margin: 0.5em 0;
            padding: 0.3em 0.75em;
            background: {colors.docs_code_bg};
            font-style: italic;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 0.5em 0;
            font-size: 10pt;
            page-break-inside: avoid;
        }}

        th, td {{
            border: 1px solid {colors.docs_border};
            padding: 0.35em 0.5em;
            text-align: left;
        }}

        th {{
            background: {colors.docs_code_bg};
            font-weight: 600;
            color: {colors.docs_text_primary};
        }}

        hr {{
            border: none;
            border-top: 1px solid {colors.docs_border};
            margin: 1em 0;
        }}

        img {{
            max-width: 100%;
            height: auto;
        }}

        .section-break {{
            page-break-before: always;
        }}

        /* Blog-specific styles */
        .blog-title {{
            margin-top: 0;
        }}

        .blog-meta {{
            color: {colors.docs_text_muted};
            font-size: 10pt;
            margin: 0.3em 0 0.5em 0;
        }}

        .blog-tags {{
            display: inline;
        }}

        .blog-tag {{
            display: inline-block;
            background: {colors.emerald};
            color: white;
            font-size: 8pt;
            padding: 0.1em 0.4em;
            border-radius: 3px;
            margin-right: 0.3em;
        }}

        .blog-excerpt {{
            font-style: italic;
            color: {colors.docs_text_muted};
            border-left: 3px solid {colors.emerald};
            padding-left: 0.75em;
            margin: 0.5em 0;
        }}

        /* Sphinx-needs styles */
        .need {{
            border: 1px solid {colors.docs_border};
            border-radius: 6px;
            padding: 0.75em;
            margin: 0.5em 0;
            page-break-inside: avoid;
        }}

        .need-title {{
            font-weight: 600;
            color: {colors.docs_text_primary};
        }}

        /* Admonition styles */
        .admonition {{
            border-radius: 6px;
            padding: 0.75em;
            margin: 0.5em 0;
            page-break-inside: avoid;
        }}

        .admonition.note {{
            background: #eff6ff;
            border-left: 4px solid #3b82f6;
        }}

        .admonition.warning {{
            background: #fefce8;
            border-left: 4px solid #f59e0b;
        }}

        .admonition.danger {{
            background: #fef2f2;
            border-left: 4px solid #ef4444;
        }}

        .admonition-title {{
            font-weight: 600;
            margin-bottom: 0.3em;
        }}

        /* Content section spacing */
        .content-section {{
            margin-bottom: 1em;
        }}

        .main-section-title {{
            text-align: center;
            page-break-after: avoid;
        }}
        """

    def _get_cover_css(self) -> str:
        """Generate CSS for print-friendly cover page."""
        colors = self.config.colors

        return f"""
        /* Cover page styles - print-friendly with white background */
        .cover-page {{
            page: cover;
            page-break-after: always;
            min-height: 297mm;
            padding: 25mm 20mm;
            background: {colors.docs_content_bg};
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}

        .cover-title-section {{
            text-align: center;
            max-width: 400px;
        }}

        .cover-subtitle {{
            font-size: 12pt;
            color: {colors.emerald};
            text-transform: uppercase;
            letter-spacing: 3px;
            margin: 0 0 12mm 0;
            font-weight: 500;
        }}

        .cover-main-title {{
            font-size: 42pt;
            font-weight: 700;
            color: {colors.docs_text_primary};
            margin: 0;
            line-height: 1.1;
        }}

        .cover-tagline {{
            font-size: 12pt;
            color: {colors.docs_text_secondary};
            margin: 8mm auto 0 auto;
            max-width: 350px;
            line-height: 1.5;
        }}

        .cover-hero-section {{
            text-align: center;
            margin: 10mm 0;
        }}

        .cover-hero-image {{
            max-width: 100%;
            border-radius: 6px;
            border: 1px solid {colors.docs_border};
        }}

        .cover-products-section {{
            text-align: center;
            margin-top: auto;
        }}

        .cover-products-image {{
            max-width: 100%;
            border-radius: 6px;
            border: 1px solid {colors.docs_border};
        }}

        /* Screenshots page styles */
        .screenshots-page {{
            page: cover;
            page-break-after: always;
            min-height: 297mm;
            padding: 20mm;
            background: {colors.docs_content_bg};
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 15mm;
        }}

        .screenshot-hero {{
            max-width: 100%;
            max-height: 120mm;
            border-radius: 6px;
            border: 1px solid {colors.docs_border};
        }}

        .screenshot-products {{
            max-width: 100%;
            max-height: 100mm;
            border-radius: 6px;
            border: 1px solid {colors.docs_border};
        }}
        """

    def _build_cover_html(self, screenshots: dict[str, Path]) -> str:
        """Build HTML for print-friendly cover page."""
        return """
        <div class="cover-page">
            <div class="cover-title-section">
                <p class="cover-subtitle">Privacy-First Development Tools</p>
                <h1 class="cover-main-title">Cleanroom Labs</h1>
                <p class="cover-tagline">
                    Build software that respects privacy. Free and open source tools
                    that work without network dependency.
                </p>
            </div>
        </div>
        """

    def _build_screenshots_html(self, screenshots: dict[str, Path]) -> str:
        """Build HTML for screenshots section after TOC."""
        # Build hero image reference
        hero_img = ""
        if "hero" in screenshots and screenshots["hero"].exists():
            hero_img = f'<img src="file://{screenshots["hero"]}" class="screenshot-hero" />'

        # Build products image reference
        products_img = ""
        if "products" in screenshots and screenshots["products"].exists():
            products_img = f'<img src="file://{screenshots["products"]}" class="screenshot-products" />'

        if not hero_img and not products_img:
            return ""

        return f"""
        <div class="screenshots-page">
            {hero_img}
            {products_img}
        </div>
        """

    def _build_intro_html(self) -> str:
        """Build HTML for introduction sections (About and Our Tools)."""
        return """
        <div class="main-content-section section-break">
            <h1 id="intro-about" class="main-section-title">About Cleanroom Labs</h1>

            <p>Cleanroom Labs builds free, open-source tools for air-gapped development. Our mission is to make privacy-preserving software accessible to everyone, not just security experts.</p>

            <h2 id="intro-principles">Core Principles</h2>

            <h3 id="intro-privacy">Privacy by Default</h3>
            <p>Every tool we build works without network connectivity. Your data stays on your machine, under your control. We don't collect telemetry, require accounts, or phone home.</p>

            <h3 id="intro-accessibility">Accessibility over Expertise</h3>
            <p>Security shouldn't require a PhD. Our tools are designed for developers who want privacy without becoming security experts. Simple interfaces, sensible defaults, comprehensive documentation.</p>

            <h3 id="intro-minimalism">Minimalism</h3>
            <p>We build focused tools that do one thing well. No feature bloat, no unnecessary complexity. Each tool solves a specific problem in the air-gapped development workflow.</p>

            <h3 id="intro-transparency">Transparency</h3>
            <p>All our code is open source under permissive licenses. You can audit every line, build from source, and verify that our tools do exactly what they claim.</p>

            <h2 id="intro-tools">Our Tools</h2>

            <h3 id="intro-airgap-transfer">AirGap Transfer</h3>
            <p>Secure data transfer for air-gapped systems. Move files between isolated networks using QR codes, with cryptographic verification ensuring data integrity. No USB drives, no network bridges, no compromises.</p>

            <h3 id="intro-airgap-deploy">AirGap Deploy</h3>
            <p>Universal deployment framework for isolated environments. Package applications with all dependencies, deploy to air-gapped systems, and manage updates without network access.</p>

            <h3 id="intro-cleanroom-whisper">Cleanroom Whisper</h3>
            <p>Private voice transcription powered by local AI. Convert speech to text using OpenAI's Whisper model running entirely on your hardware. No cloud uploads, no API calls, no recordings leaving your machine.</p>

            <h2 id="intro-philosophy">Technical Philosophy</h2>

            <h3 id="intro-rust">Rust-First Approach</h3>
            <p>We build our core tools in Rust for memory safety, performance, and standalone binaries. No runtime dependencies, no garbage collection pauses, no security vulnerabilities from memory corruption.</p>

            <h3 id="intro-offline">Offline-First Architecture</h3>
            <p>Every feature works without network connectivity. We design for the air-gapped case first, then add optional network features. If it requires internet, it's not a core feature.</p>

            <h3 id="intro-local-ai">Local AI Models</h3>
            <p>Our AI-powered tools run entirely on user hardware. We package optimized models, handle hardware detection, and provide the same quality as cloud services without the privacy tradeoffs.</p>
        </div>
        """

    def _get_toc_css(self) -> str:
        """Generate CSS for table of contents with page numbers."""
        colors = self.config.colors

        return f"""
        /* Table of contents styles */
        .toc-page {{
            page: toc;
            page-break-after: always;
        }}

        .toc-container {{
            padding: 10mm 0;
        }}

        .toc-title {{
            text-align: center;
            color: {colors.docs_text_primary};
            margin-bottom: 1.5em;
            font-size: 28pt;
        }}

        .toc-section-heading {{
            font-size: 14pt;
            font-weight: 600;
            color: {colors.docs_text_primary};
            margin: 1.2em 0 0.5em 0;
            padding-bottom: 0.3em;
            border-bottom: 1px solid {colors.docs_border};
        }}

        .toc-list {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}

        .toc-entry {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin: 0.3em 0;
            font-size: 9pt;
        }}

        .toc-entry-title {{
            color: {colors.docs_text_secondary};
            text-decoration: none;
            flex: 1;
            padding-right: 1em;
        }}

        .toc-entry-title:hover {{
            color: {colors.emerald};
        }}

        .toc-leader {{
            flex-shrink: 0;
            width: 1em;
        }}

        .toc-page-num {{
            color: {colors.docs_text_muted};
            font-size: 8pt;
            flex-shrink: 0;
            text-align: right;
            min-width: 2em;
        }}

        /* Use CSS target-counter for page numbers */
        .toc-entry-title::after {{
            content: target-counter(attr(href), page);
            position: absolute;
            right: 0;
        }}

        .toc-project-group {{
            margin-left: 1em;
        }}

        .toc-project-title {{
            font-weight: 600;
            color: {colors.docs_text_primary};
            font-size: 10pt;
            margin: 0.8em 0 0.3em 0;
        }}

        .toc-project-entries {{
            margin-left: 1em;
        }}
        """

    def _build_toc_html(
        self,
        blog_sections: list[ContentSection],
        docs_sections: list[ContentSection],
    ) -> str:
        """Build HTML for table of contents with working links."""
        toc_items = []

        # Introduction sections
        toc_items.append('<h2 class="toc-section-heading">About Cleanroom Labs</h2>')
        toc_items.append('<ul class="toc-list">')
        intro_entries = [
            ("intro-about", "About Cleanroom Labs"),
            ("intro-principles", "Core Principles"),
            ("intro-tools", "Our Tools"),
            ("intro-philosophy", "Technical Philosophy"),
        ]
        for anchor_id, title in intro_entries:
            toc_items.append(f'''
                <li class="toc-entry">
                    <a href="#{anchor_id}" class="toc-entry-title">{title}</a>
                    <span class="toc-leader"></span>
                    <span class="toc-page-num"></span>
                </li>
            ''')
        toc_items.append('</ul>')

        # Blog section
        if blog_sections:
            toc_items.append('<h2 class="toc-section-heading">Blog Posts</h2>')
            toc_items.append('<ul class="toc-list">')
            for section in blog_sections:
                toc_items.append(f'''
                    <li class="toc-entry">
                        <a href="#{section.anchor_id}" class="toc-entry-title">{section.title}</a>
                        <span class="toc-leader"></span>
                        <span class="toc-page-num"></span>
                    </li>
                ''')
            toc_items.append('</ul>')

        # Documentation section
        if docs_sections:
            toc_items.append('<h2 class="toc-section-heading">Technical Documentation</h2>')
            toc_items.append('<ul class="toc-list">')

            current_project = None
            for section in docs_sections:
                # Detect project from ID
                project = self._extract_project_from_id(section.id)

                if project != current_project:
                    if current_project is not None:
                        toc_items.append('</ul></div>')
                    project_title = self._get_project_title(project)
                    toc_items.append(f'''
                        <div class="toc-project-group">
                            <div class="toc-project-title">{project_title}</div>
                            <ul class="toc-list toc-project-entries">
                    ''')
                    current_project = project

                toc_items.append(f'''
                    <li class="toc-entry">
                        <a href="#{section.anchor_id}" class="toc-entry-title">{section.title}</a>
                        <span class="toc-leader"></span>
                        <span class="toc-page-num"></span>
                    </li>
                ''')

            if current_project is not None:
                toc_items.append('</ul></div>')
            toc_items.append('</ul>')

        toc_html = "\n".join(toc_items)

        return f"""
        <div class="toc-page">
            <div class="toc-container">
                <h1 class="toc-title">Table of Contents</h1>
                {toc_html}
            </div>
        </div>
        """

    def _get_project_title(self, project: str) -> str:
        """Get display title for a project."""
        titles = {
            "meta": "Cross-Project Documentation",
            "airgap-transfer": "AirGap Transfer",
            "airgap-deploy": "AirGap Deploy",
            "cleanroom-whisper": "Cleanroom Whisper",
        }
        return titles.get(project, project.replace("-", " ").title())

    def _extract_project_from_id(self, section_id: str) -> str:
        """Extract project name from section ID."""
        # Known two-part project prefixes
        two_part_prefixes = ["airgap-transfer", "airgap-deploy", "cleanroom-whisper"]

        for prefix in two_part_prefixes:
            if section_id.startswith(prefix):
                return prefix

        # Fall back to first segment or "meta"
        if "-" in section_id:
            return section_id.split("-")[0]
        return "meta"

    def _build_content_html(
        self,
        section_title: str,
        sections: list[ContentSection],
    ) -> str:
        """Build HTML for a content section (blog or docs)."""
        content_parts = []

        for i, section in enumerate(sections):
            # Add section break for all but first
            section_class = "section-break" if i > 0 else ""

            content_parts.append(f'''
                <div id="{section.anchor_id}" class="content-section {section_class}">
                    {section.html_content}
                </div>
            ''')

        content_html = "\n".join(content_parts)

        return f"""
        <div class="main-content-section section-break">
            <h1 class="main-section-title">{section_title}</h1>
            {content_html}
        </div>
        """

    def _add_bookmarks(
        self,
        input_path: Path,
        output_path: Path,
        blog_sections: list[ContentSection],
        docs_sections: list[ContentSection],
    ) -> None:
        """Add bookmarks to the generated PDF using named destinations."""
        reader = PdfReader(str(input_path))
        writer = PdfWriter()

        # Copy all pages
        for page in reader.pages:
            writer.add_page(page)

        # Get named destinations from PDF (WeasyPrint creates these from HTML id attributes)
        destinations = reader.named_destinations

        def get_page_for_anchor(anchor_id: str) -> int | None:
            """Find page number for a named destination."""
            dest = destinations.get(anchor_id)
            if dest:
                return reader.get_destination_page_number(dest)
            return None

        # Add top-level bookmarks
        writer.add_outline_item("Cover", 0)
        writer.add_outline_item("Table of Contents", 1)

        # Add intro section bookmarks
        intro_page = get_page_for_anchor("intro-about") or 2
        intro_parent = writer.add_outline_item("About Cleanroom Labs", intro_page)
        intro_subsections = [
            ("intro-principles", "Core Principles"),
            ("intro-tools", "Our Tools"),
            ("intro-philosophy", "Technical Philosophy"),
        ]
        for anchor_id, title in intro_subsections:
            page = get_page_for_anchor(anchor_id)
            if page is not None:
                writer.add_outline_item(title, page, parent=intro_parent)

        if blog_sections:
            # Find first blog page from actual anchor
            first_blog_page = get_page_for_anchor(blog_sections[0].anchor_id) or 2
            blog_parent = writer.add_outline_item("Blog Posts", first_blog_page)

            # Add each blog post as child bookmark
            for section in blog_sections:
                page = get_page_for_anchor(section.anchor_id)
                if page is not None:
                    writer.add_outline_item(section.title, page, parent=blog_parent)

        if docs_sections:
            # Find first docs page
            first_docs_page = get_page_for_anchor(docs_sections[0].anchor_id)
            if first_docs_page is None:
                # Fallback: estimate based on last blog section
                if blog_sections:
                    last_blog_page = get_page_for_anchor(blog_sections[-1].anchor_id) or 2
                    first_docs_page = last_blog_page + 1
                else:
                    first_docs_page = 2
            docs_parent = writer.add_outline_item("Technical Documentation", first_docs_page)

            # Group by project with nested hierarchy
            current_project = None
            project_parent = None
            for section in docs_sections:
                project = self._extract_project_from_id(section.id)
                page = get_page_for_anchor(section.anchor_id)

                if project != current_project:
                    project_title = self._get_project_title(project)
                    project_page = page if page is not None else first_docs_page
                    project_parent = writer.add_outline_item(
                        project_title, project_page, parent=docs_parent
                    )
                    current_project = project

                if page is not None and project_parent:
                    writer.add_outline_item(section.title, page, parent=project_parent)

        # Write final PDF
        with open(output_path, "wb") as f:
            writer.write(f)

        if self.config.verbose:
            print(f"  Added bookmarks to PDF")


def build_pdf(
    blog_sections: list[ContentSection],
    docs_sections: list[ContentSection],
    screenshots: dict[str, Path],
    config: Optional[Config] = None,
    output_path: Optional[Path] = None,
) -> Path:
    """Convenience function to build PDF."""
    builder = PDFBuilder(config)
    return builder.build(blog_sections, docs_sections, screenshots, output_path)
