"""
PDF assembly and styling with WeasyPrint.
"""

from pathlib import Path
from typing import Optional

try:
    from weasyprint import HTML, CSS
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
    """Build PDF from extracted content."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or default_config

        if not WEASYPRINT_AVAILABLE:
            raise ImportError(
                "WeasyPrint is required for PDF generation. "
                "Install with: pip install weasyprint"
            )

        if not PYPDF_AVAILABLE:
            raise ImportError(
                "pypdf is required for PDF merging. "
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
        """Build the complete PDF."""
        output_path = output_path or self.config.paths.output_path

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if self.config.verbose:
            print("\nBuilding PDF...")

        # Build individual sections
        temp_dir = self.config.paths.output_dir / "temp_pdf"
        temp_dir.mkdir(parents=True, exist_ok=True)

        pdf_paths = []

        # 1. Cover page
        cover_path = temp_dir / "01_cover.pdf"
        self._build_cover_page(screenshots, cover_path)
        pdf_paths.append(cover_path)

        # 2. Table of contents
        toc_path = temp_dir / "02_toc.pdf"
        self._build_toc(blog_sections, docs_sections, toc_path)
        pdf_paths.append(toc_path)

        # 3. Blog posts
        if blog_sections:
            blog_path = temp_dir / "03_blog.pdf"
            self._build_content_section("Blog Posts", blog_sections, blog_path)
            pdf_paths.append(blog_path)

        # 4. Technical documentation
        if docs_sections:
            docs_path = temp_dir / "04_docs.pdf"
            self._build_content_section("Technical Documentation", docs_sections, docs_path)
            pdf_paths.append(docs_path)

        # Merge all PDFs
        self._merge_pdfs(pdf_paths, output_path, blog_sections, docs_sections)

        # Clean up temp files
        for pdf_path in pdf_paths:
            if pdf_path.exists():
                pdf_path.unlink()
        if temp_dir.exists():
            try:
                temp_dir.rmdir()
            except OSError:
                pass  # Directory not empty, leave it

        if self.config.verbose:
            print(f"\nPDF generated: {output_path}")

        return output_path

    def _get_base_css(self) -> str:
        """Generate base CSS for all pages."""
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

        @page :first {{
            @bottom-center {{
                content: none;
            }}
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            font-family: {fonts.sans};
            font-size: 11pt;
            line-height: 1.6;
            color: {colors.docs_text_secondary};
            background: {colors.docs_content_bg};
            margin: 0;
            padding: 0;
        }}

        h1 {{
            font-size: 24pt;
            font-weight: 700;
            color: {colors.docs_text_primary};
            margin: 1em 0 0.5em 0;
            page-break-after: avoid;
        }}

        h2 {{
            font-size: 18pt;
            font-weight: 600;
            color: {colors.docs_text_primary};
            margin: 1.5em 0 0.5em 0;
            page-break-after: avoid;
            border-bottom: 1px solid {colors.docs_border};
            padding-bottom: 0.3em;
        }}

        h3 {{
            font-size: 14pt;
            font-weight: 600;
            color: {colors.docs_text_primary};
            margin: 1.2em 0 0.4em 0;
            page-break-after: avoid;
        }}

        h4, h5, h6 {{
            font-size: 12pt;
            font-weight: 600;
            color: {colors.docs_text_primary};
            margin: 1em 0 0.3em 0;
            page-break-after: avoid;
        }}

        p {{
            margin: 0.8em 0;
            orphans: 3;
            widows: 3;
        }}

        a {{
            color: {colors.emerald};
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        ul, ol {{
            margin: 0.8em 0;
            padding-left: 1.5em;
        }}

        li {{
            margin: 0.3em 0;
        }}

        code {{
            font-family: {fonts.mono};
            font-size: 0.9em;
            background: {colors.docs_code_bg};
            color: {colors.docs_code_text};
            padding: 0.2em 0.4em;
            border-radius: 3px;
        }}

        pre {{
            font-family: {fonts.mono};
            font-size: 9pt;
            background: {colors.docs_code_bg};
            color: {colors.docs_code_text};
            padding: 1em;
            border-radius: 6px;
            overflow-x: auto;
            page-break-inside: avoid;
            border: 1px solid {colors.docs_border};
        }}

        pre code {{
            background: none;
            padding: 0;
            font-size: inherit;
        }}

        blockquote {{
            border-left: 4px solid {colors.emerald};
            margin: 1em 0;
            padding: 0.5em 1em;
            background: {colors.docs_code_bg};
            font-style: italic;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1em 0;
            font-size: 10pt;
            page-break-inside: avoid;
        }}

        th, td {{
            border: 1px solid {colors.docs_border};
            padding: 0.5em 0.75em;
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
            margin: 2em 0;
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
            margin: 0.5em 0;
        }}

        .blog-tags {{
            margin: 0.5em 0 1em 0;
        }}

        .blog-tag {{
            display: inline-block;
            background: {colors.emerald};
            color: white;
            font-size: 9pt;
            padding: 0.2em 0.6em;
            border-radius: 3px;
            margin-right: 0.5em;
        }}

        .blog-excerpt {{
            font-style: italic;
            color: {colors.docs_text_muted};
            border-left: 3px solid {colors.emerald};
            padding-left: 1em;
            margin: 1em 0;
        }}

        /* Sphinx-needs styles */
        .need {{
            border: 1px solid {colors.docs_border};
            border-radius: 6px;
            padding: 1em;
            margin: 1em 0;
            page-break-inside: avoid;
        }}

        .need-title {{
            font-weight: 600;
            color: {colors.docs_text_primary};
        }}

        /* Admonition styles */
        .admonition {{
            border-radius: 6px;
            padding: 1em;
            margin: 1em 0;
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
            margin-bottom: 0.5em;
        }}
        """

    def _build_cover_page(self, screenshots: dict[str, Path], output_path: Path) -> None:
        """Build the cover page with screenshots."""
        colors = self.config.colors
        fonts = self.config.fonts

        # Build hero image reference
        hero_img = ""
        if "hero" in screenshots and screenshots["hero"].exists():
            hero_img = f'<img src="file://{screenshots["hero"]}" class="hero-image" />'

        # Build products image reference
        products_img = ""
        if "products" in screenshots and screenshots["products"].exists():
            products_img = f'<img src="file://{screenshots["products"]}" class="products-image" />'

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @page {{
                    size: A4;
                    margin: 0;
                }}

                body {{
                    font-family: {fonts.sans};
                    margin: 0;
                    padding: 0;
                    background: {colors.slate_950};
                    color: {colors.text_primary};
                    min-height: 100vh;
                }}

                .cover {{
                    display: flex;
                    flex-direction: column;
                    min-height: 297mm;
                    padding: 20mm;
                }}

                .hero-section {{
                    text-align: center;
                    margin-bottom: 30mm;
                }}

                .hero-image {{
                    max-width: 100%;
                    border-radius: 8px;
                    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
                }}

                .title-section {{
                    text-align: center;
                    margin: 20mm 0;
                }}

                .main-title {{
                    font-size: 36pt;
                    font-weight: 700;
                    color: {colors.text_primary};
                    margin: 0 0 10mm 0;
                }}

                .subtitle {{
                    font-size: 14pt;
                    color: {colors.emerald};
                    text-transform: uppercase;
                    letter-spacing: 2px;
                    margin: 0;
                }}

                .tagline {{
                    font-size: 12pt;
                    color: {colors.text_secondary};
                    margin: 10mm 0 0 0;
                    max-width: 400px;
                    margin-left: auto;
                    margin-right: auto;
                }}

                .products-section {{
                    margin-top: auto;
                    text-align: center;
                }}

                .products-image {{
                    max-width: 100%;
                    border-radius: 8px;
                }}

                .footer {{
                    text-align: center;
                    margin-top: 20mm;
                    font-size: 10pt;
                    color: {colors.text_muted};
                }}
            </style>
        </head>
        <body>
            <div class="cover">
                <div class="title-section">
                    <p class="subtitle">Privacy-First Development Tools</p>
                    <h1 class="main-title">Cleanroom Labs</h1>
                    <p class="tagline">
                        Build software that respects privacy. Free and open source tools
                        that work without network dependency.
                    </p>
                </div>

                {f'<div class="hero-section">{hero_img}</div>' if hero_img else ''}

                {f'<div class="products-section">{products_img}</div>' if products_img else ''}

                <div class="footer">
                    <p>Generated from cleanroomlabs.dev</p>
                </div>
            </div>
        </body>
        </html>
        """

        document = HTML(string=html)
        document.write_pdf(str(output_path), font_config=self.font_config)

        if self.config.verbose:
            print(f"  Built cover page: {output_path}")

    def _build_toc(
        self,
        blog_sections: list[ContentSection],
        docs_sections: list[ContentSection],
        output_path: Path,
    ) -> None:
        """Build the table of contents page."""
        colors = self.config.colors

        toc_items = []

        # Blog section
        if blog_sections:
            toc_items.append('<h2>Blog Posts</h2>')
            toc_items.append('<ul class="toc-list">')
            for section in blog_sections:
                toc_items.append(
                    f'<li><a href="#{section.anchor_id}">{section.title}</a></li>'
                )
            toc_items.append('</ul>')

        # Documentation section
        if docs_sections:
            toc_items.append('<h2>Technical Documentation</h2>')
            toc_items.append('<ul class="toc-list">')

            current_project = None
            for section in docs_sections:
                # Detect project from ID
                project = section.id.split("-")[0] if "-" in section.id else "meta"

                if project != current_project:
                    if current_project is not None:
                        toc_items.append('</ul></li>')
                    project_title = self._get_project_title(project)
                    toc_items.append(f'<li><strong>{project_title}</strong><ul>')
                    current_project = project

                toc_items.append(
                    f'<li><a href="#{section.anchor_id}">{section.title}</a></li>'
                )

            if current_project is not None:
                toc_items.append('</ul></li>')
            toc_items.append('</ul>')

        toc_html = "\n".join(toc_items)

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                {self._get_base_css()}

                .toc-container {{
                    padding: 20mm 0;
                }}

                .toc-title {{
                    text-align: center;
                    color: {colors.docs_text_primary};
                    margin-bottom: 2em;
                }}

                .toc-list {{
                    list-style: none;
                    padding: 0;
                }}

                .toc-list li {{
                    margin: 0.5em 0;
                }}

                .toc-list ul {{
                    list-style: none;
                    padding-left: 1.5em;
                    margin: 0.5em 0;
                }}

                .toc-list a {{
                    color: {colors.docs_text_secondary};
                    text-decoration: none;
                }}

                .toc-list a:hover {{
                    color: {colors.emerald};
                }}
            </style>
        </head>
        <body>
            <div class="toc-container">
                <h1 class="toc-title">Table of Contents</h1>
                {toc_html}
            </div>
        </body>
        </html>
        """

        document = HTML(string=html)
        document.write_pdf(str(output_path), font_config=self.font_config)

        if self.config.verbose:
            print(f"  Built table of contents: {output_path}")

    def _get_project_title(self, project: str) -> str:
        """Get display title for a project."""
        titles = {
            "meta": "Cross-Project Documentation",
            "airgap-transfer": "AirGap Transfer",
            "airgap-deploy": "AirGap Deploy",
            "cleanroom-whisper": "Cleanroom Whisper",
        }
        return titles.get(project, project.replace("-", " ").title())

    def _build_content_section(
        self,
        section_title: str,
        sections: list[ContentSection],
        output_path: Path,
    ) -> None:
        """Build a content section (blog or docs)."""
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

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                {self._get_base_css()}

                .main-section-title {{
                    text-align: center;
                    page-break-after: avoid;
                }}

                .content-section {{
                    margin-bottom: 2em;
                }}
            </style>
        </head>
        <body>
            <h1 class="main-section-title">{section_title}</h1>
            {content_html}
        </body>
        </html>
        """

        document = HTML(string=html)
        document.write_pdf(str(output_path), font_config=self.font_config)

        if self.config.verbose:
            print(f"  Built section: {section_title} ({len(sections)} items)")

    def _merge_pdfs(
        self,
        pdf_paths: list[Path],
        output_path: Path,
        blog_sections: list[ContentSection],
        docs_sections: list[ContentSection],
    ) -> None:
        """Merge all PDFs and add bookmarks."""
        writer = PdfWriter()

        page_offset = 0
        bookmarks = []

        for pdf_path in pdf_paths:
            if not pdf_path.exists():
                continue

            reader = PdfReader(str(pdf_path))
            num_pages = len(reader.pages)

            # Add pages
            for page in reader.pages:
                writer.add_page(page)

            # Track bookmarks based on section
            if "cover" in pdf_path.name:
                bookmarks.append(("Cover", page_offset))
            elif "toc" in pdf_path.name:
                bookmarks.append(("Table of Contents", page_offset))
            elif "blog" in pdf_path.name:
                bookmarks.append(("Blog Posts", page_offset))
            elif "docs" in pdf_path.name:
                bookmarks.append(("Technical Documentation", page_offset))

            page_offset += num_pages

        # Add bookmarks to PDF
        for title, page_num in bookmarks:
            writer.add_outline_item(title, page_num)

        # Write final PDF
        with open(output_path, "wb") as f:
            writer.write(f)

        if self.config.verbose:
            print(f"  Merged {len(pdf_paths)} sections into final PDF")


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
