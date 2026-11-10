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
        assert "chapters" in data and isinstance(data["chapters"], list), f"Missing chapters list in {book_yaml}"
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
