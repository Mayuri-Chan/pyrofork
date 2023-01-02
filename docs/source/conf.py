#  PyroFork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2022-present wulan17 <https://github.com/wulan17>
#
#  This file is part of PyroFork.
#
#  PyroFork is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PyroFork is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with PyroFork.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

from pyrogram import __version__

from pygments.styles.friendly import FriendlyStyle

FriendlyStyle.background_color = "#f3f2f1"

project = "PyroFork"
copyright = f"2022-present, wulan17"
author = "wulan17"

version = ".".join(__version__.split(".")[:-1])

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_rtd_dark_mode"
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None)
}

master_doc = "index"
source_suffix = ".rst"
autodoc_member_order = "bysource"

templates_path = ["../resources/templates"]
html_copy_source = False

napoleon_use_rtype = False
napoleon_use_param = False

pygments_style = "friendly"

copybutton_prompt_text = "$ "

suppress_warnings = ["image.not_readable"]

html_title = "PyroFork Documentation"
html_theme = "sphinx_rtd_theme"
html_static_path = ["../resources/static","_static"]
html_show_sourcelink = True
html_show_copyright = False
html_theme_options = {
    "canonical_url": "https://docs.pyrogram.org/",
    "collapse_navigation": True,
    "sticky_navigation": False,
    "logo_only": True,
    "display_version": False,
    "style_external_links": True
}

html_logo = "../resources/static/img/pyrogram.png"
html_favicon = "../resources/static/img/favicon.ico"

latex_engine = "xelatex"
latex_logo = "../resources/static/img/pyrogram.png"

latex_elements = {
    "pointsize": "12pt",
    "fontpkg": r"""
        \setmainfont{Open Sans}
        \setsansfont{Bitter}
        \setmonofont{Ubuntu Mono}
        """
}

html_css_files = [
    "css/my.css",
    "https://docs.pyrogram.org/_static/css/custom.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.2/css/all.min.css",
]