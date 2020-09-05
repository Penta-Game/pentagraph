# -*- coding: utf-8 -*-

from pelican import signals
from subprocess import check_call
import logging
from re import match
import os

logger = logging.getLogger(__name__)

"""
Minify CSS and JS files in output path with uglifyjs and uglifycss.
Required: an existing installation of uglifyjs/ uglifycss Compressor.
"""


def minify(pelican):
    """
      Minify CSS and JS with uglifyjs/ uglifycss
      :param pelican: The Pelican instance
    """
    js = pelican.settings.get("UGLIFYJS_EXECUTABLE", "uglifyjs")
    css = pelican.settings.get("UGLIFYCSS_EXECUTABLE", "uglifycss")
    js_options = pelican.settings.get(
        "UGLIFYJS_OPTIONS", ["-c", "--source-map"])
    css_options = pelican.settings.get("UGLIFYCSS_OPTIONS", [])
    exclude = pelican.settings.get("UGLIFY_EXCLUDE", [])
    for dirpath, _, filenames in os.walk(pelican.settings["OUTPUT_PATH"]):
        for name in filenames:
            _name = os.path.splitext(name)
            filepath = os.path.join(dirpath, name)
            if None not in [match(regex, filepath) for regex in exclude]:
                continue
            elif _name[1] == ".css" and _name[0][-3:] != "min":
                logger.info(f"minify {filepath}")
                check_call([css, *css_options, filepath,
                            "--output", f"{filepath[:-4]}.min.css"])
            elif os.path.splitext(name)[1] == ".js" and _name[0][-3:] != "min":
                logger.info(f"minify {filepath}")
                check_call([js, filepath, *js_options,
                            "-o", f"{filepath[:-3]}.min.js"])


def register():
    signals.finalized.connect(minify)
