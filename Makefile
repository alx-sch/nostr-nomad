######################
# PROJECT VARIABLES  #
######################

NAME :=			nostr-nomad

PYTHON :=		python3
VENV :=			env

SRC :=			src
SRCS :=			$(wildcard $(SRC)/*.py)

# Hidden folder to store caches
CACHES :=	.caches

# User input folder, export folder (put substack export here)
EXPORT_DIR := user_entries/export

# Documentation
DOCS := docs
TEXINFO := $(DOCS)/doc.texi
BUILD_DIR := build_docs
README := README.md

######################
# FORMATTING STRINGS #
######################

RESET :=		\033[0m
BOLD :=			\033[1m
RED :=			\033[91m
GREEN :=		\033[32m
YELLOW :=		\033[33m

###############
# MAIN TARGET #
###############

# Default target
# all: run docs
all: run

# Create virtual environment
$(VENV)/bin/activate: 
	@echo "$(BOLD)$(YELLOW)Setting up virtual environment...$(RESET)"
	@$(PYTHON) -m venv $(VENV) 
	@$(VENV)/bin/pip install --upgrade pip
	@$(VENV)/bin/pip install -r requirements.txt
	@echo "$(BOLD)$(GREEN)Done.$(RESET)"

# Install dependencies
install: $(VENV)/bin/activate

# Run the main script
run: $(VENV)/bin/activate $(SRCS)
	@echo "$(BOLD)$(YELLOW)Running $(NAME)...$(RESET)"
	@rm -f $(EXPORT_DIR)/.gitkeep
	@$(VENV)/bin/python $(SRC)/main.py
	@echo "$(BOLD)$(GREEN)Done.$(RESET)"
	@touch $(EXPORT_DIR)/.gitkeep

#################
# DOCUMENTATION #
#################

# Generate documentation
docs: $(README) texinfo sphinx

# Generate README.md from Texinfo
$(README): $(TEXINFO)
	@echo "$(BOLD)$(YELLOW)Generating README.md...$(RESET)"
	@makeinfo --plaintext --output=$(README) $(TEXINFO)
	@echo "$(BOLD)$(GREEN)Done.$(RESET)"

# Generate Texinfo documentation
texinfo: $(TEXINFO)
	@echo "$(BOLD)$(YELLOW)Generating Texinfo documentation...$(RESET)"
	@mkdir -p $(BUILD_DIR)
	@makeinfo --output=$(BUILD_DIR)/doc.info $(TEXINFO)
	@makeinfo --html --output=$(BUILD_DIR)/html $(TEXINFO)
	@texi2pdf -o $(BUILD_DIR)/doc.pdf $(TEXINFO)
	@mv doc.aux $(DOCS)/doc.aux
	@mv doc.toc $(DOCS)/doc.toc
	@mv doc.log $(DOCS)/doc.log
	@echo "$(BOLD)$(GREEN)Done.$(RESET)"

# Check if sphinx-build exists in the virtual environment, if not create the venv and install sphinx
sphinx_check:
	@if [ ! -f "$(VENV)/bin/sphinx-build" ]; then \
		echo "$(BOLD)$(YELLOW)Installing Sphinx in the virtual environment...$(RESET)"; \
		$(PYTHON) -m venv $(VENV);  \
		$(VENV)/bin/pip install --upgrade pip; \
		$(VENV)/bin/pip install sphinx==8.2.3; \
		echo "$(BOLD)$(GREEN)Sphinx installed successfully.$(RESET)"; \
	fi

# Generate Sphinx documentation (for Python code)
sphinx: sphinx_check
	@echo "$(BOLD)$(YELLOW)Generating Sphinx documentation...$(RESET)"
	@mkdir -p $(BUILD_DIR)/sphinx
	@$(VENV)/bin/sphinx-build -b html $(DOCS)/sphinx/source $(BUILD_DIR)/sphinx
	@echo "$(BOLD)$(GREEN)Done.$(RESET)"

##################
# CLEAN TARGETS  #
##################

# Clean up everything, including the cache keeping track of publishing history
clean-all: clean clean-cache

# Clean everything (environment, docs, cache)
clean: clean-env clean-docs clean-temp

# Remove virtual environment
clean-env:
	@echo "$(BOLD)$(YELLOW)Removing virtual environment...$(RESET)"
	@rm -rf $(VENV)
	@echo "$(BOLD)$(GREEN)Done.$(RESET)"

# Remove only generated documentation
clean-docs:
	@echo "$(BOLD)$(YELLOW)Cleaning up documentation...$(RESET)"
	@rm -rf $(BUILD_DIR)
#	@rm -f $(README)
	@echo "$(BOLD)$(GREEN)Done.$(RESET)"

# Remove unzipped export data
clean-temp:
	@echo "$(BOLD)$(YELLOW)Cleaning up temporay files...$(RESET)"
	@rm -rf $(SRC)/__pycache__
	@rm -f $(DOCS)/doc.aux $(DOCS)/doc.toc $(DOCS)/doc.log
	@echo "$(BOLD)$(GREEN)Done.$(RESET)"

# Remove the cache keeping track of publishing history
clean-cache:
	@echo "$(BOLD)$(YELLOW)Cleaning up publishing cache...$(RESET)"
	@rm -f $(CACHES)/assets/*
	@rm -f $(CACHES)/posts/caches.json
	@echo "$(BOLD)$(GREEN)Done.$(RESET)"

.PHONY: all run install clean clean-env clean-docs clean-temp