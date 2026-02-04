"""
Configuration and design tokens for PDF generation.

Design tokens sourced from common/tokens/colors.js
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class Paths:
    """Path configuration for PDF generation."""
    # Input paths (relative to repo root)
    docs_dir: Path = field(default_factory=lambda: Path("public/docs"))
    blog_dir: Path = field(default_factory=lambda: Path("content/blog"))

    # Output paths
    output_dir: Path = field(default_factory=lambda: Path("output"))
    screenshots_dir: Path = field(default_factory=lambda: Path("output/screenshots"))

    # Default output filename
    output_filename: str = "cleanroom-labs.pdf"

    @property
    def output_path(self) -> Path:
        return self.output_dir / self.output_filename


@dataclass
class Colors:
    """Design tokens from common/tokens/colors.js"""

    # Backgrounds
    slate_950: str = "#030712"  # Deepest background (hero, cards)
    slate_900: str = "#111827"  # Primary dark / sidebar search
    slate_800: str = "#1f2937"  # Sidebar / nav / footer
    slate_700: str = "#374151"  # Borders, dividers
    slate_600: str = "#4b5563"  # Muted elements

    # Documentation content (light theme)
    docs_content_bg: str = "#ffffff"
    docs_code_bg: str = "#f8fafc"  # slate-50
    docs_text_primary: str = "#1e293b"  # slate-800
    docs_text_secondary: str = "#334155"  # slate-700
    docs_text_muted: str = "#64748b"  # slate-500
    docs_code_text: str = "#1e293b"  # slate-800
    docs_border: str = "#e2e8f0"  # slate-200

    # Text colors
    text_primary: str = "#f9fafb"  # gray-50
    text_secondary: str = "#d1d5db"  # gray-300
    text_muted: str = "#9ca3af"  # gray-400
    code_text: str = "#e2e8f0"  # slate-200

    # Accent colors - Emerald
    emerald: str = "#10b981"  # emerald-500
    emerald_light: str = "#34d399"  # emerald-400
    emerald_dark: str = "#059669"  # emerald-600

    # Syntax highlighting
    syntax_comment: str = "#6b7280"
    syntax_keyword: str = "#c084fc"
    syntax_string: str = "#34d399"
    syntax_function: str = "#60a5fa"
    syntax_number: str = "#fbbf24"


@dataclass
class Fonts:
    """Font configuration."""
    sans: str = "Inter, system-ui, -apple-system, sans-serif"
    mono: str = "Monaco, Menlo, 'Ubuntu Mono', Consolas, monospace"


@dataclass
class PageLayout:
    """PDF page layout configuration."""
    size: str = "A4"
    margin_top: str = "20mm"
    margin_bottom: str = "20mm"
    margin_left: str = "20mm"
    margin_right: str = "20mm"


@dataclass
class Selectors:
    """CSS selectors to strip from extracted content."""
    # Navigation elements to remove
    strip: tuple = (
        ".wy-nav-side",
        ".wy-nav-top",
        ".wy-breadcrumbs",
        ".wy-breadcrumbs-aside",
        "a.headerlink",
        ".rst-footer-buttons",
        "footer",
        ".site-nav-bar",
        ".sidebar-toggle",
        "nav",
        "script",
        "style",
        "#quality-bar",  # Remove Quality Bar section from PDF
    )

    # Main content selectors
    content: str = '[role="main"]'
    fallback_content: str = ".rst-content"


@dataclass
class DocOrder:
    """Documentation section ordering."""
    # Order for project documentation sections
    projects: tuple = (
        "meta",
        "airgap-transfer",
        "airgap-deploy",
        "cleanroom-whisper",
    )


@dataclass
class ScreenshotConfig:
    """Screenshot capture configuration."""
    viewport_width: int = 1440
    viewport_height: int = 900

    # CSS selectors for screenshot targets
    hero_selector: str = "section"  # First section is hero
    products_selector: str = "#products"  # Products section

    # Default server URL
    server_url: str = "http://localhost:3000"


@dataclass
class Config:
    """Main configuration container."""
    paths: Paths = field(default_factory=Paths)
    colors: Colors = field(default_factory=Colors)
    fonts: Fonts = field(default_factory=Fonts)
    page_layout: PageLayout = field(default_factory=PageLayout)
    selectors: Selectors = field(default_factory=Selectors)
    doc_order: DocOrder = field(default_factory=DocOrder)
    screenshot: ScreenshotConfig = field(default_factory=ScreenshotConfig)

    # Verbose output
    verbose: bool = False

    def __post_init__(self):
        """Resolve paths relative to repo root."""
        self.repo_root = self._find_repo_root()
        self.paths.docs_dir = self.repo_root / self.paths.docs_dir
        self.paths.blog_dir = self.repo_root / self.paths.blog_dir
        self.paths.output_dir = self.repo_root / self.paths.output_dir
        self.paths.screenshots_dir = self.repo_root / self.paths.screenshots_dir

    def _find_repo_root(self) -> Path:
        """Find the repository root by looking for CLAUDE.md or .git."""
        current = Path(__file__).resolve().parent
        while current != current.parent:
            if (current / "CLAUDE.md").exists() or (current / ".git").exists():
                return current
            current = current.parent
        raise RuntimeError("Could not find repository root")


# Default configuration instance
config = Config()
