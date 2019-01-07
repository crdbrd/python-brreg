import os
import sys

import sphinx_rtd_theme

sys.path.insert(0, os.path.abspath('..'))

import brreg  # noqa


# -- General configuration ------------------------------------------------

# needs_sphinx = '1.0'

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.viewcode']

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = 'brreg'
copyright = '2019, Otovo AS'
author = 'Otovo AS'

release = brreg.__version__
version = '.'.join(release.split('.')[:2])

language = None
exclude_patterns = ['_build']

pygments_style = 'sphinx'

todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_theme_options = {}
html_theme_options['canonical_url'] = 'https://brreg.readthedocs.io/en/latest/'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = ['_static']


# -- Options for HTMLHelp output ------------------------------------------

htmlhelp_basename = 'brreg'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    'papersize': 'a4paper',
    # 'pointsize': '10pt',
    # 'preamble': '',
    # 'figure_align': 'htbp',
}

latex_documents = [
    (master_doc, 'brreg.tex', 'brreg documentation', 'Otovo AS', 'manual')
]


# -- Options for doctest extension ----------------------------------------

autodoc_member_order = 'groupwise'


# -- Options for doctest builder ------------------------------------------

doctest_path = [os.path.abspath('..')]

doctest_global_setup = """
from pprint import pprint
"""

doctest_test_doctest_blocks = 'default'
