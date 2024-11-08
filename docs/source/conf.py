# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'MELA'
copyright = '2024, Sergey Besedin, Andrey Goloborodko, Oleg Wizner'
author = 'Sergey Besedin, Andrey Goloborodko, Oleg Wizner'
release = '1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx_rtd_theme',
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# import ushahidi_sphinx_rtd_theme
import sphinx_rtd_theme
html_theme = 'sphinx_rtd_theme'
# html_theme = 'ushahidi_sphinx_rtd_theme'
html_static_path = ['_static']
