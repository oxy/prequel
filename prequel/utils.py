"""Provide utilities to process strings and Python types."""

import keyword
import re

__all__ = ["quote_ident", "clean_ident"]


CLEAN_IDENT_RE = re.compile(r"[\w]")
QUOTE_TABLE = str.maketrans({"\0": "\\0", '"': '""', "\\": "\\\\"})


def quote_ident(ident: str):
    """Escape an identifier.

    Escapes null bytes, the backslash, and double quotes,
    and returns a quoted SQL identifier.

    Args:
        ident: Identifier to process.

    Returns:
        Escaped and quoted identifier.
    """
    escaped_ident = ident.translate(QUOTE_TABLE)
    return f'"{escaped_ident}"'


def clean_ident(ident: str):
    """Clean an identifier.

    Cleans an identifier by removing all non-ASCII characters and numbers.

    Args:
        ident: Identifier to process.

    Returns:
        Escaped and quoted identifier.
    """
    clean = "".join([ch for ch in ident if CLEAN_IDENT_RE.match(ch)])
    if not clean.isidentifier() or keyword.iskeyword(clean):
        clean = "_" + clean
    return clean
