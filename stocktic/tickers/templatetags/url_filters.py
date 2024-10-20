"""This module defines custom template filters for URL encoding
and string replacement.

Filters:
    url_encode: Encodes a URL string.
    replace_with_hyphen: Replaces certain characters with hyphens.
"""

from urllib.parse import quote

from django import template

register = template.Library()


@register.filter
def url_encode(value):
    """Encodes a URL string.

    Args:
        value (str): The string to be URL encoded.

    Returns:
        str: The URL encoded string.
    """
    return quote(value, safe="")


@register.filter(name="replace_with_hyphen")
def replace_with_hyphen(value):
    """Replaces certain characters with hyphens.

    Args:
        value (str): The string in which characters will be replaced.

    Returns:
        str: The modified string with certain characters replaced by hyphens.
    """
    return value.replace("/", "-").replace("^", "-")
