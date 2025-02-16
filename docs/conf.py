"""Sphinx configuration file."""

project = "python-brreg"
author = "Cardboard AS"
copyright = f"2019 Otovo ASA, 2023-2025 {author}"  # noqa: A001

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx_rtd_theme",
]

html_theme = "sphinx_rtd_theme"

autodoc_member_order = "bysource"
