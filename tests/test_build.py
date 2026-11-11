"""
Tests for the Odia Language Books Pandoc Publishing Pipeline.
"""

from __future__ import annotations

import shutil
from pathlib import Path
import pytest
import yaml

from scripts.build import (
    PROJECT_ROOT,
    BOOKS_DIR,
    DIST_DIR,
    check_tool_installed,
    find_books,
    load_book_config,
    get_chapter_paths,
    build_html,
    build_pdf,
    clean,
    get_best_odia_font,
)


def test_system_prerequisites():
    """Verify that pandoc is installed and accessible."""
    assert check_tool_installed("pandoc"), "pandoc must be installed"


def test_discover_books():
    """Verify that books are discovered correctly."""
    books = find_books()
    assert len(books) >= 1, "At least one book should be discovered"
    slugs = [b.parent.name for b in books]
    assert "odia-words-and-sentences" in slugs


def test_book_yaml_schema():
    """Validate structure and chapter presence for every book."""
    books = find_books()
    for book_yaml in books:
        with open(book_yaml, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        assert "title_or" in data or "title" in data, f"Missing title in {book_yaml}"
        assert "chapters" in data and isinstance(data["chapters"], list), (
            f"Missing chapters list in {book_yaml}"
        )
        assert len(data["chapters"]) > 0, f"No chapters declared in {book_yaml}"

        book_dir = book_yaml.parent
        config = load_book_config(book_yaml)
        chapter_paths = get_chapter_paths(book_dir, config)
        assert len(chapter_paths) == len(data["chapters"])
        for ch in chapter_paths:
            assert ch.exists(), f"Chapter file not found: {ch}"


def test_build_starter_book_html(tmp_path):
    """Test HTML compilation for 'odia-words-and-sentences'."""
    book_yaml = BOOKS_DIR / "odia-words-and-sentences" / "book.yaml"
    assert book_yaml.exists()

    config = load_book_config(book_yaml)
    chapters = get_chapter_paths(book_yaml.parent, config)
    html_out = build_html(book_yaml.parent, config, chapters)

    assert html_out.exists(), "HTML output must exist"
    assert html_out.stat().st_size > 5000, "HTML output should not be empty"

    content = html_out.read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in content
    assert "ଓଡ଼ିଆ ଶବ୍ଦ ଓ ବାକ୍ୟ" in content
    assert "book.css" in content


def test_build_html_copies_shared_assets():
    """Verify that shared assets like pattern SVGs are copied into dist/<slug>/html/assets/."""
    book_yaml = BOOKS_DIR / "odia-words-and-sentences" / "book.yaml"
    config = load_book_config(book_yaml)
    chapters = get_chapter_paths(book_yaml.parent, config)
    html_out = build_html(book_yaml.parent, config, chapters)

    pattern_dest = html_out.parent / "assets" / "patterns" / "sambalpuri-ikat.svg"
    assert pattern_dest.exists(), f"Expected shared pattern asset at {pattern_dest}"


def test_build_html_asset_overlay_and_cleanup(tmp_path):
    """Verify stale output asset cleanup and two-tier asset merging (shared + book-specific)."""
    # Create test book structure
    test_slug = "test-overlay-book"
    book_dir = tmp_path / test_slug
    chapters_dir = book_dir / "chapters"
    assets_dir = book_dir / "assets"
    chapters_dir.mkdir(parents=True)
    assets_dir.mkdir(parents=True)

    (chapters_dir / "01-test.md").write_text("# Test\nContent", encoding="utf-8")
    (assets_dir / "custom.txt").write_text("book-specific", encoding="utf-8")

    # Override a shared pattern with book-specific version
    patterns_dir = assets_dir / "patterns"
    patterns_dir.mkdir(parents=True)
    (patterns_dir / "sambalpuri-ikat.svg").write_text("<svg>override</svg>", encoding="utf-8")

    config = {
        "slug": test_slug,
        "title_or": "ଟେଷ୍ଟ",
        "chapters": ["01-test.md"],
    }
    chapters = [chapters_dir / "01-test.md"]

    # Pre-populate dist with an orphaned stale asset
    out_dir = DIST_DIR / test_slug / "html"
    dist_assets = out_dir / "assets"
    dist_assets.mkdir(parents=True, exist_ok=True)
    stale_file = dist_assets / "stale_orphan.txt"
    stale_file.write_text("should be deleted on rebuild", encoding="utf-8")

    # Run build
    html_out = build_html(book_dir, config, chapters)

    # 1. Stale orphan must have been wiped
    assert not stale_file.exists(), "Stale assets from prior builds must be cleaned"

    # 2. Book-specific asset is present
    assert (dist_assets / "custom.txt").read_text(encoding="utf-8") == "book-specific"

    # 3. Book-specific asset overrode the shared asset
    assert (dist_assets / "patterns" / "sambalpuri-ikat.svg").read_text(encoding="utf-8") == "<svg>override</svg>"

    # Clean up test output from dist
    if out_dir.parent.exists():
        shutil.rmtree(out_dir.parent)


@pytest.mark.skipif(not check_tool_installed("xelatex"), reason="xelatex not available")
def test_build_starter_book_pdf():
    """Test PDF compilation with XeLaTeX for 'odia-words-and-sentences'."""
    book_yaml = BOOKS_DIR / "odia-words-and-sentences" / "book.yaml"
    assert book_yaml.exists()

    config = load_book_config(book_yaml)
    chapters = get_chapter_paths(book_yaml.parent, config)
    pdf_out = build_pdf(book_yaml.parent, config, chapters)

    assert pdf_out.exists(), "PDF output must exist"
    assert pdf_out.stat().st_size > 20000, "PDF output should be larger than 20KB"

    # Verify that cover background XObject/graphic was embedded
    content = pdf_out.read_bytes()
    assert b"/XObject" in content, "Cover background graphic XObject must be embedded in PDF"


def test_font_selection():
    """Verify font detection and fallback mechanism."""
    font = get_best_odia_font()
    assert isinstance(font, str) and len(font) > 0
    # Custom font preference is honored
    assert get_best_odia_font("CustomPreferredFont") == "CustomPreferredFont"


def test_clean_command():
    """Test that clean removes dist directory."""
    test_file = DIST_DIR / "temp_test_artifact.txt"
    test_file.parent.mkdir(parents=True, exist_ok=True)
    test_file.write_text("temp")
    assert test_file.exists()

    clean()
    assert not DIST_DIR.exists()
