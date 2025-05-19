# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))  # points to where modules live

# -- Project information -----------------------------------------------------
project = 'nostr-nomad'
copyright = '2025 May, Natalie Holbrook, Alex Schenk'
author = 'Natalie Holbrook, Alex Schenk'
release = '0.8.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',     # support for Google/NumPy-style docstrings
    'sphinx.ext.autosummary',  # autosummary tables if needed
]

autoclass_content = "both"
autosummary_generate = True
add_module_names = False  # optional: don't prefix classes/functions with module names

templates_path = ['_templates']
exclude_patterns: list[str] = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['_static']

html_theme_options = {
    'description': 'Migration tool to convert and publish Substack posts to Nostr',
    'github_user': 'alx-sch',
    'github_repo': 'nostr-nomad',
    'github_banner': True,
    'github_type': 'star',
    'fixed_sidebar': True,
}

html_context = {
    'display_github': True,
    'github_user': 'alx-sch',
    'github_repo': 'nostr-nomad',
    'github_version': 'main',
    'conf_py_path': '/docs/source/',
}
