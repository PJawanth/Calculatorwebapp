"""Render dashboard HTML from template."""

import os
import shutil
from pathlib import Path


def render_dashboard() -> None:
    """Copy template to site directory."""
    # Ensure site directory exists
    os.makedirs("site", exist_ok=True)

    # Get paths
    script_dir = Path(__file__).parent
    template_path = script_dir / "templates" / "index.html"
    output_path = Path("site") / "index.html"

    # Copy template to site
    shutil.copy(template_path, output_path)
    print(f"Dashboard rendered to {output_path}")  # noqa: T201


def main() -> None:
    """Main entry point."""
    render_dashboard()


if __name__ == "__main__":
    main()
