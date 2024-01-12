"""Sphinx configuration."""
project = "Torhen"
author = "Aina Yves"
copyright = "2024, Aina Yves"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
