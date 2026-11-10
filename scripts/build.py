#!/usr/bin/env python3
"""
Odia Language Introduction Books - Pandoc Publishing Pipeline
Builds book source files into HTML and PDF distributions.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml
except ImportError:
    print("Error: pyyaml is not installed. Run 'uv sync' or 'pip install pyyaml'.", file=sys.stderr)
    sys.exit(1)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
BOOKS_DIR = PROJECT_ROOT / "books"
SHARED_DIR = PROJECT_ROOT / "shared"
DIST_DIR = PROJECT_ROOT / "dist"


def check_tool_installed(name: str) -> bool:
    """Check if a CLI tool is available in system PATH."""
    return shutil.which(name) is not None


def find_books(requested_book: str | None = None) -> List[Path]:
    """Discover books to build."""
    if not BOOKS_DIR.exists():
        print(f"Error: Books directory not found at {BOOKS_DIR}", file=sys.stderr)
        return []

    book_yaml_files = list(BOOKS_DIR.glob("*/book.yaml"))
    if requested_book:
        matched = [p for p in book_yaml_files if p.parent.name == requested_book]
        if not matched:
            print(f"Error: Book '{requested_book}' not found in {BOOKS_DIR}", file=sys.stderr)
            return []
        return matched

    return sorted(book_yaml_files, key=lambda p: p.parent.name)


def load_book_config(book_yaml_path: Path) -> Dict[str, Any]:
    """Parse book.yaml configuration."""
    with open(book_yaml_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    config.setdefault("slug", book_yaml_path.parent.name)
    config.setdefault("title_or", config.get("title", config["slug"]))
    config.setdefault("title_en", config.get("subtitle", ""))
    config.setdefault("author", "Odia Language Project")
    config.setdefault("language", "or")
    config.setdefault("version", "1.0.0")
    config.setdefault("date", time.strftime("%Y"))
    config.setdefault("chapters", [])
    return config


def get_chapter_paths(book_dir: Path, config: Dict[str, Any]) -> List[Path]:
    """Resolve ordered chapter markdown paths."""
    chapters_dir = book_dir / "chapters"
    if not chapters_dir.exists():
        raise FileNotFoundError(f"Chapters directory missing: {chapters_dir}")

    chapter_files = config.get("chapters", [])
    if not chapter_files:
        # Fall back to alphanumeric sorted .md files
        return sorted(chapters_dir.glob("*.md"))

    resolved = []
    for chapter_name in chapter_files:
        chapter_path = chapters_dir / chapter_name
        if not chapter_path.exists():
            raise FileNotFoundError(f"Chapter file declared in book.yaml not found: {chapter_path}")
        resolved.append(chapter_path)
    return resolved


def build_html(book_dir: Path, config: Dict[str, Any], chapter_paths: List[Path]) -> Path:
    """Compile book to HTML using Pandoc."""
    slug = config["slug"]
    out_dir = DIST_DIR / slug / "html"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{slug}.html"

    # Copy shared CSS to output directory
    shared_css = SHARED_DIR / "css" / "book.css"
    dest_css = out_dir / "book.css"
    if shared_css.exists():
        shutil.copy2(shared_css, dest_css)

    # Copy assets if present
    book_assets = book_dir / "assets"
    if book_assets.exists() and book_assets.is_dir():
        dest_assets = out_dir / "assets"
        if dest_assets.exists():
            shutil.rmtree(dest_assets)
        shutil.copytree(book_assets, dest_assets)

    template_file = SHARED_DIR / "templates" / "html" / "template.html"

    cmd = [
        "pandoc",
        *[str(p) for p in chapter_paths],
        "-o",
        str(out_file),
        "--standalone",
        "--toc",
        "--toc-depth=3",
        "--section-divs",
        "--css=book.css",
        f"-Mtitle={config['title_or']}",
        f"-Mtitle_or={config['title_or']}",
        f"-Mtitle_en={config.get('title_en', '')}",
        f"-Msubtitle={config.get('subtitle', '')}",
        f"-Mauthor={config.get('author', '')}",
        f"-Mversion={config.get('version', '')}",
        f"-Mdate={config.get('date', '')}",
        f"-Mlang={config.get('language', 'or')}",
    ]

    if template_file.exists():
        cmd.extend(["--template", str(template_file)])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Pandoc HTML build failed:\n{result.stderr}")

    return out_file


def build_pdf(book_dir: Path, config: Dict[str, Any], chapter_paths: List[Path]) -> Path:
    """Compile book to PDF using Pandoc with XeLaTeX."""
    if not check_tool_installed("xelatex"):
        raise RuntimeError(
            "xelatex is required to compile PDF books with Odia script fonts.\n"
            "Please ensure MacTeX / TeX Live is installed and available in PATH."
        )

    slug = config["slug"]
    out_dir = DIST_DIR / slug / "pdf"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{slug}.pdf"

    preamble_file = SHARED_DIR / "templates" / "latex" / "preamble.tex"

    cmd = [
        "pandoc",
        *[str(p) for p in chapter_paths],
        "-o",
        str(out_file),
        "--pdf-engine=xelatex",
        "--toc",
        "--toc-depth=2",
        "-V",
        "mainfont=Baloo Bhaina 2",
        "-V",
        "mainfontoptions=Script=Oriya",
        "-V",
        "geometry=a4paper,top=2.5cm,bottom=2.5cm,left=2.8cm,right=2.8cm",
        "-V",
        "colorlinks=true",
        "-V",
        "linkcolor=red!70!black",
        "-V",
        "urlcolor=blue!70!black",
        f"-Mtitle={config['title_or']}",
        f"-Mauthor={config.get('author', '')}",
        f"-Mdate={config.get('date', '')}",
        f"-Mlang={config.get('language', 'or')}",
    ]

    if preamble_file.exists():
        cmd.extend(["--include-in-header", str(preamble_file)])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Pandoc PDF build failed:\n{result.stderr}")

    return out_file


def build_book(book_yaml_path: Path, target_format: str = "all") -> Dict[str, Path]:
    """Build a single book in requested formats."""
    book_dir = book_yaml_path.parent
    config = load_book_config(book_yaml_path)
    chapter_paths = get_chapter_paths(book_dir, config)

    print(f"\n==================================================")
    print(f"📖 Building Book: {config['title_or']} ({config['slug']})")
    print(f"   Chapters count: {len(chapter_paths)}")
    print(f"==================================================")

    outputs = {}
    build_all = target_format.lower() in ("all", "both")

    # Build HTML
    if build_all or target_format.lower() == "html":
        t0 = time.time()
        print("  --> Generating HTML edition...")
        html_out = build_html(book_dir, config, chapter_paths)
        size_kb = html_out.stat().st_size / 1024
        print(f"  ✓ HTML generated: {html_out.relative_to(PROJECT_ROOT)} ({size_kb:.1f} KB in {time.time()-t0:.2f}s)")
        outputs["html"] = html_out

    # Build PDF
    if build_all or target_format.lower() == "pdf":
        t0 = time.time()
        print("  --> Generating PDF edition (XeLaTeX)...")
        pdf_out = build_pdf(book_dir, config, chapter_paths)
        size_kb = pdf_out.stat().st_size / 1024
        print(f"  ✓ PDF generated:  {pdf_out.relative_to(PROJECT_ROOT)} ({size_kb:.1f} KB in {time.time()-t0:.2f}s)")
        outputs["pdf"] = pdf_out

    return outputs


def clean() -> None:
    """Remove built output artifacts."""
    if DIST_DIR.exists():
        print(f"Removing build directory: {DIST_DIR}")
        shutil.rmtree(DIST_DIR)
        print("✓ Clean completed.")
    else:
        print("Already clean (no dist directory).")


def check_env() -> bool:
    """Verify system prerequisites."""
    print("Checking system prerequisites for Odia Book Publishing Pipeline:\n")
    tools = [
        ("Pandoc", "pandoc", True),
        ("XeLaTeX", "xelatex", True),
        ("Python 3", "python3", True),
        ("uv", "uv", False),
    ]

    all_ok = True
    for label, cmd, required in tools:
        found = check_tool_installed(cmd)
        version_str = ""
        if found:
            try:
                res = subprocess.run([cmd, "--version"], capture_output=True, text=True)
                version_str = res.stdout.splitlines()[0] if res.stdout else ""
            except Exception:
                version_str = "Available"
            print(f"  [✓] {label:10} : Found ({cmd}) -> {version_str}")
        else:
            status = "REQUIRED - MISSING" if required else "Optional - Missing"
            print(f"  [✗] {label:10} : {status}")
            if required:
                all_ok = False

    return all_ok


def main() -> None:
    parser = argparse.ArgumentParser(description="Odia Language Books Publisher")
    parser.add_argument("--book", "-b", help="Specific book slug to build (e.g. odia-words-and-sentences)")
    parser.add_argument(
        "--format",
        "-f",
        choices=["all", "html", "pdf"],
        default="all",
        help="Target output format (default: all)",
    )
    parser.add_argument("--clean", action="store_true", help="Clean dist/ build output directory")
    parser.add_argument("--check", action="store_true", help="Verify environment prerequisites")
    args = parser.parse_args()

    if args.clean:
        clean()
        return

    if args.check:
        ok = check_env()
        sys.exit(0 if ok else 1)

    if not check_tool_installed("pandoc"):
        print("Error: pandoc is not installed or not in PATH.", file=sys.stderr)
        sys.exit(1)

    books = find_books(args.book)
    if not books:
        print("No books found to build.", file=sys.stderr)
        sys.exit(1)

    overall_start = time.time()
    built_count = 0
    for book_yaml in books:
        try:
            build_book(book_yaml, target_format=args.format)
            built_count += 1
        except Exception as e:
            print(f"\n❌ Error building book at {book_yaml}:\n{e}", file=sys.stderr)
            sys.exit(1)

    print(f"\n✨ All done! Successfully built {built_count} book(s) in {time.time()-overall_start:.2f}s.")


if __name__ == "__main__":
    main()
