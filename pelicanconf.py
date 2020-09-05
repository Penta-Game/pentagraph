#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = "Cobalt"
SITENAME = "Pentagraph"
SITEURL = ""

PATH = "content"
OUTPUT_PATH = "docs"

TIMEZONE = "Europe/Paris"

DEFAULT_LANG = "en"
THEME = "theme"
PREFIX = "/pentagraph/"

# Navigation bar links

NAVLINKS = [
    ("Documentation", "/pages/docs-overview"),
    ("About", "/pages/about-us"),
    ("Getting Started", "/pages/getting-started"),
]


# Plugins
PLUGIN_PATHS = ["plugins"]
PLUGINS = ["uglify"]
UGLIFY_EXCLUDE = [".+fontawesome.*$"]

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

