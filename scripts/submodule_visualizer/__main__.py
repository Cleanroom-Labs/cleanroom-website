#!/usr/bin/env python3
"""
Entry point for the git submodule visualizer.

Usage:
    python -m scripts.submodule_visualizer [path]

Args:
    path: Path to the git repository (default: current directory)
"""

import argparse
import sys
from pathlib import Path


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Visualize git repositories and their submodules"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to the git repository (default: current directory)",
    )
    args = parser.parse_args()

    repo_path = Path(args.path).resolve()

    if not repo_path.exists():
        print(f"Error: Path does not exist: {repo_path}", file=sys.stderr)
        return 1

    if not (repo_path / ".git").exists():
        print(f"Error: Not a git repository: {repo_path}", file=sys.stderr)
        return 1

    # Import here to avoid tkinter import on --help
    from .app import SubmoduleVisualizerApp

    app = SubmoduleVisualizerApp(repo_path)
    app.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
