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

# Navigation bar links
NAVLINKS = [
    ("Documentation", "/overview/"),
    ("About", "/pages/about-us"),
    ("Getting Started", "/pages/getting-started"),
]

# Resource prefix
PREFIX = ""

# Prefixes for robots.txt
PREFIXES = ["pages"]

# Direct templates
TEMPLATE_PAGES = {
    "overview.html": "overview/index.html",
    "robots.txt": "robots.txt",
}

# Article settings
ARTICLE_PATHS = ["articles"]
ARTICLE_URL = "blog/{slug}/"
ARTICLE_SAVE_AS = "blog/{slug}/index.html"
DRAFT_URL = "drafts/{slug}/index.html"
DRAFT_SAVE_AS = "drafts/{slug}/index.html"
DEFAULT_METADATA = {"status": "published"}

# Plugins
PLUGIN_PATHS = ["plugins"]
PLUGINS = ["uglify", "filters"]
UGLIFY_EXCLUDE = [".+fontawesome.*$"]

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

