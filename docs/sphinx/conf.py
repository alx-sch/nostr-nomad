# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0, os.path.abspath("../../src"))  # points to where modules live

# -- Project information -----------------------------------------------------
project = "nostr-nomad"
copyright = "2025 May, Natalie Holbrook, Alexander Schenk"
author = "Natalie Holbrook, Alexander Schenk"
release = "0.8.0"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",  # support for Google/NumPy-style docstrings
    "sphinx.ext.autosummary",  # autosummary tables if needed
]

autoclass_content = "both"
autosummary_generate = True
add_module_names = False  # optional: don't prefix classes/functions with module names

templates_path = ["_templates"]
exclude_patterns: list[str] = []

# -- Options for HTML output -------------------------------------------------
html_theme = "alabaster"
html_static_path = ["_static"]
