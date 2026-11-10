# ==============================================================================
# Odia Language Introduction Books - Build Makefile
# ==============================================================================

UV := uv
PYTHON := $(UV) run python
BUILD_SCRIPT := scripts/build.py

.PHONY: all html pdf clean check test help

all: ## Build all books in all formats (HTML and PDF)
	@$(PYTHON) $(BUILD_SCRIPT) --format all

html: ## Build HTML edition (optional: BOOK=<slug>)
ifdef BOOK
	@$(PYTHON) $(BUILD_SCRIPT) --book $(BOOK) --format html
else
	@$(PYTHON) $(BUILD_SCRIPT) --format html
endif

pdf: ## Build PDF edition with XeLaTeX (optional: BOOK=<slug>)
ifdef BOOK
	@$(PYTHON) $(BUILD_SCRIPT) --book $(BOOK) --format pdf
else
	@$(PYTHON) $(BUILD_SCRIPT) --format pdf
endif

clean: ## Remove compiled books in dist/
	@$(PYTHON) $(BUILD_SCRIPT) --clean

check: ## Verify system prerequisites (pandoc, xelatex, python, uv)
	@$(PYTHON) $(BUILD_SCRIPT) --check

test: ## Run automated pytest test suite
	@$(UV) run pytest -v

help: ## Show this help message
	@echo "Usage: make [target] [BOOK=book-slug]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-10s %s\n", $$1, $$2}'
