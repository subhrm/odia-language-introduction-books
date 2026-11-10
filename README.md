# ଓଡ଼ିଆ ଭାଷା ଶିକ୍ଷା ପୁସ୍ତକ ମାଳା
## Odia Language Introduction Books

An open-source repository of books for learning, reading, and speaking the **Odia (ଓଡ଼ିଆ)** language. Chapters are authored in Markdown and compiled into standalone, responsive **HTML** editions and print-ready **PDF** books using **Pandoc** and **XeLaTeX**.

---

## 📚 Available Books

| Folder Slug | Book Title (Odia) | Book Title (English) | Status | Formats |
| :--- | :--- | :--- | :--- | :--- |
| [`odia-words-and-sentences`](books/odia-words-and-sentences/) | **ଓଡ଼ିଆ ଶବ୍ଦ ଓ ବାକ୍ୟ** | *Odia Words and Sentences* | Complete Starter | HTML &bull; PDF |

---

## 📁 Repository Structure

The repository is organized to support multiple books in parallel with shared build tooling:

```text
odia-language-introduction-books/
├── books/                               # Books collection
│   └── odia-words-and-sentences/        # First book: "ଓଡିଆ ଶବ୍ଦ ଓ ବାକ୍ଯ"
│       ├── book.yaml                    # Book metadata & chapter sequence
│       ├── chapters/                    # Markdown chapters
│       │   ├── 00-preface.md
│       │   ├── 01-varnamala-and-pronunciation.md
│       │   ├── 02-essential-words.md
│       │   ├── 03-grammar-and-sentence-patterns.md
│       │   ├── 04-daily-conversations.md
│       │   └── 05-practice-and-exercises.md
│       └── assets/                      # Book-specific diagrams / images
├── shared/                              # Shared templates and styling
│   ├── css/
│   │   └── book.css                     # Modern reader styling with Odia Google Fonts
│   └── templates/
│       ├── html/
│       │   └── template.html            # Standalone HTML5 template with TOC & sidebar
│       └── latex/
│           └── preamble.tex             # XeLaTeX preamble for Odia OpenType ligatures
├── scripts/
│   └── build.py                         # Build runner for discovering & compiling books
├── tests/
│   └── test_build.py                    # Automated test suite (schemas, HTML, PDF)
├── dist/                                # Compiled outputs (git-ignored)
│   └── <book-slug>/
│       ├── html/                        # Standalone web book + CSS
│       └── pdf/                         # XeLaTeX compiled PDF
├── Makefile                             # Convenient build commands
├── pyproject.toml                       # Python 3.14 project & uv configuration
└── .github/workflows/build.yml          # GitHub Actions CI pipeline
```

---

## 🛠️ Prerequisites

To build both HTML and PDF formats locally:

1. **Pandoc** (>= 3.0):
   ```bash
   # macOS (Homebrew)
   brew install pandoc
   ```
2. **XeLaTeX** (for PDF generation with Indic OpenType font rendering):
   ```bash
   # macOS
   brew install --cask mactex-no-gui
   # Linux (Ubuntu/Debian)
   sudo apt-get install texlive-xetex fonts-noto-extra
   ```
3. **Python 3.14 & uv**:
   ```bash
   # macOS (Homebrew)
   brew install uv
   uv python install 3.14
   uv sync --extra dev
   ```
4. **Odia Font**:
   The PDF build uses **Baloo Bhaina 2** (installed natively on macOS and available on Google Fonts), which supports both Odia script and Latin alphabet seamlessly.

---

## 🚀 Building the Books

### Using Make

```bash
# Check prerequisites
make check

# Build all books in both HTML and PDF formats
make all

# Build only HTML (fast)
make html

# Build only a specific book
make html BOOK=odia-words-and-sentences
make pdf BOOK=odia-words-and-sentences

# Run automated tests
make test

# Clean build artifacts
make clean
```

### Using uv directly

```bash
# Verify environment
uv run python scripts/build.py --check

# Build all books
uv run python scripts/build.py

# Build specific book to HTML
uv run python scripts/build.py --book odia-words-and-sentences --format html

# Build specific book to PDF
uv run python scripts/build.py --book odia-words-and-sentences --format pdf
```

Compiled books will be generated inside:
- `dist/<book-slug>/html/<book-slug>.html`
- `dist/<book-slug>/pdf/<book-slug>.pdf`

---

## ✍️ How to Add a New Book

To add a new book to the library:

1. Create a new folder under `books/<your-book-slug>/`:
   ```bash
   mkdir -p books/my-new-book/chapters
   ```
2. Create a `book.yaml` file inside the book folder:
   ```yaml
   slug: my-new-book
   title_or: "ପୁସ୍ତକର ନାମ"
   title_en: "English Title"
   subtitle: "Subtitle / Tagline"
   author: "Author Name"
   language: "or"
   version: "1.0.0"
   chapters:
     - "01-introduction.md"
     - "02-first-chapter.md"
   ```
3. Add your Markdown chapter files in `books/<your-book-slug>/chapters/`.
4. Run `make all` to compile your new book to HTML and PDF automatically!

---

## 📄 License

This project is licensed under the MIT License. Book content is released for free educational use.
