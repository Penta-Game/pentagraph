from pelican import signals
from re import sub


def _html_cleaner(text: str) -> str:
    if isinstance(text, str):
        return sub("\<.+?\>", "", text)
    else:
        return ""


def add_filter(pelican):
    """Add filters to Pelican."""
    pelican.env.filters.update({"clean": _html_cleaner})


# Module entry point
def register():
    signals.generator_init.connect(add_filter)
