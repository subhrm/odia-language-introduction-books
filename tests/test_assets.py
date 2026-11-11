"""
Tests for shared visual assets and SVG pattern integrity.
"""

from pathlib import Path
import xml.etree.ElementTree as ET


def test_sambalpuri_ikat_svg_validity():
    svg_path = Path("shared/assets/patterns/sambalpuri-ikat.svg")
    assert svg_path.exists(), "SVG pattern file must exist"
    assert svg_path.stat().st_size < 4096, "SVG pattern should be lightweight (< 4KB)"

    tree = ET.parse(svg_path)
    root = tree.getroot()
    assert root.tag.endswith("svg"), "Root element must be <svg>"
    assert root.attrib.get("viewBox") == "0 0 80 80", "SVG must have 0 0 80 80 viewBox"
    assert root.attrib.get("width") == "80" and root.attrib.get("height") == "80"


def test_cover_bg_assets_validity():
    """Verify that full-page A4 cover background SVG and vector PDF assets exist and are valid."""
    svg_path = Path("shared/assets/patterns/cover-bg.svg")
    pdf_path = Path("shared/assets/patterns/cover-bg.pdf")

    assert svg_path.exists(), "A4 cover background SVG must exist"
    tree = ET.parse(svg_path)
    root = tree.getroot()
    assert root.tag.endswith("svg")
    assert "210" in root.attrib.get("viewBox", "") and "297" in root.attrib.get("viewBox", "")

    assert pdf_path.exists(), "Vector cover-bg.pdf must exist"
    assert pdf_path.stat().st_size > 1000, "cover-bg.pdf must be valid non-empty PDF"
    with open(pdf_path, "rb") as f:
        header = f.read(5)
    assert header.startswith(b"%PDF"), "Must have valid %PDF magic header"

