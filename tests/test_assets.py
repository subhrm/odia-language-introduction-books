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
    assert "viewBox" in root.attrib or ("width" in root.attrib and "height" in root.attrib)
