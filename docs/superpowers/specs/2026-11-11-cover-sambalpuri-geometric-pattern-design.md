# Design Specification: Sambalpuri Pasapalli Geometric Pattern Background for Book Cover

## 1. Intent & Why
The cover section (`.book-hero`) of each generated book currently uses a simple linear gradient. To celebrate Odia cultural identity and elevate the visual design of the educational books, we want to introduce a subtle, seamless Sambalpuri *Pasapalli* (Ikat / Bandha) stepped-diamond geometric vector pattern as a background accent while maintaining high typographic legibility and contrast.

## 2. Goals, Non-Goals, & Anti-Goals
* **Goals:**
  * Design a pure, crisp SVG vector tile capturing the traditional Sambalpuri *Pasapalli* stepped-diamond and check geometry.
  * Integrate the pattern into `.book-hero` in `shared/css/book.css` with subtle opacity (4–6%) layered over the existing warm ivory gradient.
  * Update `scripts/build.py` to copy shared assets (specifically `shared/assets/`) into `dist/<book>/html/assets/` during the build process.
  * Ensure the pattern is responsive, seamlessly repeating, and performs with zero render lag.
* **Non-Goals:**
  * Modifying the typography or chapter content of the books.
  * Implementing high-contrast or multicolored graphics that distract from reading.
  * Converting XeLaTeX PDF cover layout to use SVG (LaTeX uses native typography; this design specifically enhances HTML output).
* **Anti-Goals:**
  * Heavy raster/PNG assets that increase repository or bundle size.
  * Excessive pattern opacity or visual noise that interferes with title, author, or subtitle readability (WCAG contrast must remain intact).

## 3. Constraints
* The SVG must be resolution-independent and lightweight (< 4 KB).
* The build system is Python (`scripts/build.py`) orchestrating Pandoc.
* Any asset paths in CSS must resolve correctly whether viewing compiled files from `dist/<slug>/html/` or standalone test outputs.
* All existing tests in `tests/` must continue to pass.

## 4. Approaches Considered
1. **Approach 1 (*Pasapalli* Stepped-Diamond Lattice) — [Selected]**:
   * Repeating 2D geometric grid with stepped lozenges, concentric diamond outlines, and central dot/cross accents reminiscent of Sambalpuri *Bandha* dye-weaving.
   * *Trade-off*: Pure geometry without figurative elements, providing authentic cultural recognition while keeping text legibility 100% clean.
2. **Approach 2 (*Kumbha* / Temple Spire & Chevron Waves)**:
   * Alternating horizontal saw-tooth spires and ikat zigzag waves.
   * *Trade-off*: Directional/banded aesthetic rather than uniform backdrop; draws more eye movement away from text.
3. **Approach 3 (*Bandha Padma* 8-Point Star Rosette)**:
   * Repeating interlocking octagonal floral star tiles.
   * *Trade-off*: Denser visual density requiring extreme attenuation to avoid visual clutter.

## 5. Technical Implementation Details
* **Pattern Asset**:
  * Location: `shared/assets/patterns/sambalpuri-ikat.svg`.
  * Dimensions: 80x80 (or 60x60) viewBox seamlessly tileable in both X and Y directions.
  * Colors: Monochromatic terracotta (`#8b2500` / `#661800`) with precise stroke and opacity attributes so it works gracefully as a background image.
* **Stylesheet Integration**:
  * In `shared/css/book.css`, update `.book-hero`:
    * Multi-layer background: `linear-gradient(...)` combined with `url('assets/patterns/sambalpuri-ikat.svg') repeat`.
    * Ensure fallback support and print styles suppress decorative background when printing.
* **Build System Integration**:
  * In `scripts/build.py` inside `build_html()`:
    * Ensure `shared/assets` is copied to `out_dir / "assets"` alongside any book-specific assets in `book_dir / "assets"`.
* **Testing & Verification**:
  * Run `scripts/build.py` to compile HTML for `odia-words-and-sentences`.
  * Inspect generated HTML in `dist/odia-words-and-sentences/html/` to verify asset copy, CSS resolution, and visual output.
  * Run project test suite (`pytest`) to ensure no regressions.
