######################
# PROJECT VARIABLES  #
######################

NAME :=			nostr-nomad

PYTHON :=		python3
VENV :=			env
ACTIVATE :=		. $(VENV)/bin/activate

SRC :=			src
SRCS :=			$(wildcard $(SRC)/*.py)

# Folder to store exported substack data
EXPORT :=		export

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
all: run docs

# Create virtual environment
$(VENV)/bin/activate: requirements.txt
	@echo "$(BOLD)$(YELLOW)Setting up virtual environment...$(RESET)"
	@$(PYTHON) -m venv $(VENV) 
	@$(ACTIVATE) && pip install --upgrade pip 
	@$(ACTIVATE) && pip install -r requirements.txt
	@echo "$(BOLD)$(GREEN)Done.$(RESET)"

# Install dependencies
install: $(VENV)/bin/activate

# Run the main script
run: $(VENV)/bin/activate $(SRCS)
	@echo "$(BOLD)$(YELLOW)Running main script...$(RESET)"
	@$(ACTIVATE) && $(PYTHON) $(SRC)/main.py
	@echo "$(BOLD)$(GREEN)Done.$(RESET)"

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

# Generate Sphinx documentation (for Python code)
sphinx:
	@echo "$(BOLD)$(YELLOW)Generating Sphinx documentation...$(RESET)"
	@mkdir -p $(BUILD_DIR)/sphinx
	@$(ACTIVATE) && sphinx-build -b html $(DOCS)/sphinx/source $(BUILD_DIR)/sphinx
	@echo "$(BOLD)$(GREEN)Done.$(RESET)"

##################
# CLEAN TARGETS  #
##################

# Clean everything (environment, docs, cache)
clean: clean-env clean-docs clean-cache

# Remove virtual environment
clean-env:
	@echo "$(BOLD)$(YELLOW)Removing virtual environment...$(RESET)"
	@rm -rf $(VENV)
	@echo "$(BOLD)$(GREEN)Done.$(RESET)"

# Remove only generated documentation
clean-docs:
	@echo "$(BOLD)$(YELLOW)Cleaning up documentation...$(RESET)"
	@rm -rf $(BUILD_DIR)
	@rm -f $(README)
	@echo "$(BOLD)$(GREEN)Done.$(RESET)"

# Remove unzipped export data
clean-cache:
	@echo "$(BOLD)$(YELLOW)Cleaning up cache...$(RESET)"
	@rm -rf $(SRC)/__pycache__
	@rm -f $(DOCS)/doc.aux $(DOCS)/doc.toc $(DOCS)/doc.log
	@rm -rf $(EXPORT)/unzipped
	@echo "$(BOLD)$(GREEN)Done.$(RESET)"

.PHONY: all run install clean clean-env clean-docs clean-cache