# AGENTS.md — Agent & Contributor Guide

Welcome to the **Odia Language Introduction Books** repository. This document outlines project architecture, technical setup, coding and authoring standards, build commands, and testing expectations for AI agents and human contributors working on this codebase.

---

## 1. Project Overview

The mission of this repository is to create high-quality, open-source educational books for learning the **Odia (ଓଡ଼ିଆ)** language. 
- Source files are written in standard **Markdown** (`.md`).
- Outputs are compiled into modern **HTML** (with responsive reading layouts and Google Fonts) and print-ready **PDF** (via **Pandoc** and **XeLaTeX** with native Odia script support).
- The repository is organized to support **multiple books** side-by-side with shared tooling.

---

## 2. Directory Structure

```text
odia-language-introduction-books/
├── books/                               # Multi-book collection
│   └── <book-slug>/                     # e.g., odia-words-and-sentences/
│       ├── book.yaml                    # Metadata & chapter sequence
│       ├── chapters/                    # Markdown chapter files
│       │   ├── 00-preface.md
│       │   ├── 01-chapter-one.md
│       │   └── ...
│       └── assets/                      # Book-specific images & diagrams
├── shared/                              # Shared templates & styles
│   ├── css/
│   │   └── book.css                     # Modern reader styles & Google Fonts
│   └── templates/
│       ├── html/
│       │   └── template.html            # Standalone HTML5 template (TOC, sidebar)
│       └── latex/
│           └── preamble.tex             # XeLaTeX preamble (Noto Sans Oriya, spacing)
├── scripts/
│   └── build.py                         # Universal Python build engine
├── tests/
│   └── test_build.py                    # Pytest test suite for build & schemas
├── dist/                                # Build outputs (git-ignored)
│   └── <book-slug>/
│       ├── html/<book-slug>.html
│       └── pdf/<book-slug>.pdf
├── Makefile                             # Convenient make targets
├── pyproject.toml                       # Python 3.14 project & uv configuration
└── .github/workflows/build.yml          # GitHub Actions CI workflow
```

---

## 3. Environment & Prerequisites

- **Python**: `>= 3.14` managed via **`uv`**.
  - Install dependencies: `uv sync --extra dev`
  - Run commands in virtual environment: `uv run <command>`
- **Pandoc**: `>= 3.0` (required for markdown parsing and conversion).
- **XeLaTeX**: (MacTeX / TeX Live) required for PDF rendering of Indic scripts.
- **Font**: `Noto Sans Oriya` is the primary font for XeLaTeX PDF generation.

---

## 4. Key Commands

Always run commands via `make` or `uv run`:

| Action | Command | Notes |
| :--- | :--- | :--- |
| **Check Environment** | `make check` | Verifies Pandoc, XeLaTeX, Python, and uv |
| **Build All Books** | `make all` | Compiles HTML and PDF for all books |
| **Build HTML Only** | `make html` | Fast compilation of all books |
| **Build Specific Book** | `make html BOOK=<slug>` | Targets a single book (e.g. `odia-words-and-sentences`) |
| **Build PDF Only** | `make pdf BOOK=<slug>` | Compiles PDF using XeLaTeX |
| **Run Tests** | `make test` | Runs `uv run pytest -v` |
| **Clean Output** | `make clean` | Removes the `dist/` directory |

Direct Python script usage:
```bash
uv run python scripts/build.py --book odia-words-and-sentences --format all
uv run python scripts/build.py --clean
uv run python scripts/build.py --check
```

---

## 5. Book Authoring Standards

When adding or modifying book content, agents must adhere to the following conventions:

### A. Folder & File Naming
- Book slugs must be lowercase, hyphen-separated (kebab-case): `books/<slug>/`.
- Chapter files must be prefixed with a 2-digit zero-padded index: `00-preface.md`, `01-introduction.md`, etc.
- All files must be saved with **UTF-8** encoding.

### B. `book.yaml` Schema
Every book directory must contain a `book.yaml` file with the following keys:

```yaml
slug: "book-slug"                          # Must match directory name
title_or: "ଓଡ଼ିଆରେ ପୁସ୍ତକ ଶୀର୍ଷକ"           # Title in Odia script
title_en: "English Title of Book"          # Title in English
subtitle: "A subtitle describing the book" # Optional subtitle
author: "Author Name or Contributor Group" # Author attribution
language: "or"                             # Language code (ISO 639-1)
version: "1.0.0"                           # Semantic version
date: "2026"                               # Publication year/date
chapters:                                  # Exact ordered list of chapter files
  - "00-preface.md"
  - "01-alphabet.md"
  - "02-vocabulary.md"
```

### C. Odia Content Conventions
Because these books are instructional:
- **Odia only**: 
- **Vocabulary Tables**: Use GitHub Flavored Markdown tables
- **Grammar & Sentence Patterns**: Clearly identify sentence components when introducing Odia's **SOV** (Subject + Object + Verb) order.
- **Accurate Odia Unicode**: Use standard Unicode characters for Odia (range `U+0B00` to `U+0B7F`). Ensure proper use of halant (`୍`) for conjuncts (`କ୍ଷ`, `ଜ୍ଞ`, `ସ୍ତ`, `ପ୍ର`, etc.) and nukta (`଼`) where applicable (`ଡ଼`, `ଢ଼`).

---

## 6. How to Add a New Book

1. **Create directory structure**:
   ```bash
   mkdir -p books/<new-book-slug>/chapters
   mkdir -p books/<new-book-slug>/assets
   ```
2. **Create `book.yaml`** inside `books/<new-book-slug>/book.yaml`.
3. **Write Markdown chapters** in `books/<new-book-slug>/chapters/`.
4. **Verify**:
   - Run `make test` to verify configuration schema and chapter paths.
   - Run `make html BOOK=<new-book-slug>` to inspect HTML output in `dist/`.
   - Run `make pdf BOOK=<new-book-slug>` to inspect PDF compilation.

---

## 7. Testing & Quality Requirements

Before submitting changes or completing tasks:
1. Ensure all chapters listed in `book.yaml` exist on disk.
2. Run `make test` and confirm all tests pass (`pytest`).
3. Run `make all` to ensure both HTML and PDF compile without warnings or fatal errors.
4. If modifying LaTeX or CSS templates, verify that:
   - HTML remains responsive and correctly imports Google Fonts (`Noto Sans Oriya`).
   - PDF renders complex Indic ligatures and Latin text without missing glyph warnings.
