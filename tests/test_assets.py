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

