# Sambalpuri Pasapalli Cover Background Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a subtle, culturally authentic Sambalpuri *Pasapalli* (Ikat / Bandha) geometric SVG pattern and integrate it as the cover hero background for Odia language books.

**Architecture:** A standalone vector SVG tile (`shared/assets/patterns/sambalpuri-ikat.svg`) provides a seamless 2D repeating *Pasapalli* stepped-diamond lattice. The Python build engine (`scripts/build.py`) is updated to bundle shared assets into distribution directories, and the reader stylesheet (`shared/css/book.css`) layers this SVG over the warm terracotta gradient with low opacity for optimal typographic contrast.

**Tech Stack:** SVG (Scalable Vector Graphics), CSS3 (multi-layer backgrounds, responsive & print media queries), Python 3.14 (Pathlib, shutil, subprocess), Pandoc, Pytest.

**Spec:** `docs/superpowers/specs/2026-11-11-cover-sambalpuri-geometric-pattern-design.md`

## Global Constraints

- SVG file must be clean, lightweight (< 4 KB), and tile seamlessly along both X and Y axes.
- Text legibility on `.book-hero` must remain high (WCAG AA compliant contrast between text and background).
- The pattern must be subtle (monochrome `#8b2500` terracotta at 4–6% opacity).
- Print styles must keep the background clean (avoid printing decorative background tiles).
- All tests in `tests/` must pass.

## Review Focus

1. Asset copy in `build.py` must support when `shared/assets` exists without breaking if book-specific `book/assets` also exists.
2. SVG pattern must tile seamlessly without visible seam artifacts or clipped boundary strokes.
3. CSS background path must resolve properly relative to `book.css` in `dist/<slug>/html/`.
4. High-contrast reader readability: hero title and metadata text must not suffer readability degradation.
5. Clean command (`make clean`) must remove generated output assets without errors.

---

### Task 1: Create the Sambalpuri Pasapalli Stepped-Diamond SVG Pattern

**Files:**
- Create: `shared/assets/patterns/sambalpuri-ikat.svg`
- Test: `tests/test_assets.py`

**Interfaces:**
- Consumes: Design spec geometry requirements (stepped diamond, nested lozenge, central star/dot accent, terracotta `#8b2500` at ~0.05 opacity).
- Produces: `shared/assets/patterns/sambalpuri-ikat.svg` usable as a CSS background tile.

- [ ] **Step 1: Write unit test validating SVG existence, valid XML structure, viewBox, and seamless pattern geometry**

Create `tests/test_assets.py`:
```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_assets.py -v` (with bypass if needed)
Expected: FAIL ("SVG pattern file must exist")

- [ ] **Step 3: Implement `shared/assets/patterns/sambalpuri-ikat.svg`**

Create a clean 80x80 viewBox SVG representing the Sambalpuri *Pasapalli* bandha:
- Stepped diamond outlines formed by geometric stepped paths (`M... L...`).
- Concentric nested diamond center with a small 4-point star/cross accent.
- Repeating corner half-diamonds at (0,0), (80,0), (0,80), (80,80) to ensure perfect 2D tiling without seams.
- Fill/stroke color `#8b2500` at opacity `0.05` to `0.07`.

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_assets.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add shared/assets/patterns/sambalpuri-ikat.svg tests/test_assets.py
git commit -m "feat: add Sambalpuri Pasapalli ikat geometric pattern SVG"
```

---

### Task 2: Update Build Engine to Copy Shared Assets to Distribution

**Files:**
- Modify: `scripts/build.py:147-155`
- Test: `tests/test_build.py`

**Interfaces:**
- Consumes: `SHARED_DIR / "assets"` and `book_dir / "assets"`.
- Produces: `dist/<slug>/html/assets/` containing both shared assets (like patterns) and book-specific assets.

- [ ] **Step 1: Write test in `tests/test_build.py` asserting shared assets are copied to HTML dist**

Add `test_build_html_copies_shared_assets()`:
```python
def test_build_html_copies_shared_assets():
    book_yaml = BOOKS_DIR / "odia-words-and-sentences" / "book.yaml"
    config = load_book_config(book_yaml)
    chapters = get_chapter_paths(book_yaml.parent, config)
    html_out = build_html(book_yaml.parent, config, chapters)
    
    pattern_dest = html_out.parent / "assets" / "patterns" / "sambalpuri-ikat.svg"
    assert pattern_dest.exists(), f"Expected shared pattern asset at {pattern_dest}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_build.py::test_build_html_copies_shared_assets -v`
Expected: FAIL (pattern_dest does not exist)

- [ ] **Step 3: Implement shared asset copying in `scripts/build.py`**

In `build_html()`:
```python
    # Copy shared assets if present
    shared_assets = SHARED_DIR / "assets"
    dest_assets = out_dir / "assets"
    if shared_assets.exists() and shared_assets.is_dir():
        dest_assets.mkdir(parents=True, exist_ok=True)
        shutil.copytree(shared_assets, dest_assets, dirs_exist_ok=True)

    # Copy book-specific assets if present (can override or supplement shared assets)
    book_assets = book_dir / "assets"
    if book_assets.exists() and book_assets.is_dir():
        dest_assets.mkdir(parents=True, exist_ok=True)
        shutil.copytree(book_assets, dest_assets, dirs_exist_ok=True)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_build.py -v`
Expected: ALL PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/build.py tests/test_build.py
git commit -m "feat(build): copy shared assets to HTML distribution directory"
```

---

### Task 3: Update CSS to Apply the Geometric SVG Background to the Book Hero

**Files:**
- Modify: `shared/css/book.css:159-170, 414-420`
- Test: Browser / Pandoc build verification

**Interfaces:**
- Consumes: `assets/patterns/sambalpuri-ikat.svg` relative to `book.css` in `dist/<slug>/html/`.
- Produces: Styled `.book-hero` in `shared/css/book.css` with layered SVG pattern and linear gradient.

- [ ] **Step 1: Update `.book-hero` styling in `shared/css/book.css`**

Update `.book-hero`:
```css
.book-hero {
  background-color: var(--color-surface);
  background-image:
    url('assets/patterns/sambalpuri-ikat.svg'),
    linear-gradient(135deg, #fdf8f4 0%, #ffffff 100%);
  background-repeat: repeat, no-repeat;
  background-size: 80px 80px, auto;
  border: 1px solid var(--color-border);
  border-left: 6px solid var(--color-primary);
  border-radius: var(--radius-md);
  padding: 2.5rem;
  margin-bottom: 3.5rem;
  box-shadow: var(--shadow-sm);
  position: relative;
}
```

- [ ] **Step 2: Update `@media print` rules in `shared/css/book.css`**

Ensure print output remains clean:
```css
  .book-hero {
    border: none;
    background: none !important;
    padding: 0;
    margin-bottom: 2rem;
    box-shadow: none;
  }
```

- [ ] **Step 3: Verify build and inspect output HTML**

Run: `uv run python scripts/build.py --book odia-words-and-sentences --format html`
Expected: Build succeeds, `dist/odia-words-and-sentences/html/book.css` contains pattern background rules.

- [ ] **Step 4: Commit**

```bash
git add shared/css/book.css
git commit -m "style: apply Sambalpuri geometric pattern SVG background to book-hero"
```

---

### Task 4: End-to-End Verification and Clean Check

**Files:**
- All modified files

**Interfaces:**
- Consumes: Entire pipeline and test suite.
- Produces: Verified build and clean outputs.

- [ ] **Step 1: Run the full test suite**

Run: `uv run pytest -v`
Expected: All tests pass.

- [ ] **Step 2: Run full build of all books**

Run: `uv run python scripts/build.py --format html`
Expected: Clean compilation with assets copied.

- [ ] **Step 3: Verify clean command**

Run: `uv run python scripts/build.py --clean`
Expected: `dist/` cleaned cleanly without error.
Re-run build: `uv run python scripts/build.py --format html`

- [ ] **Step 4: Commit final changes or tag**
