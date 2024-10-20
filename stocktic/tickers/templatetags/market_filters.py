"""This module defines custom template filters for market
capitalization formatting.

Filters:
    format_market_cap: Formats the market capitalization value.
"""

from custom_utils.utils import format_market_cap
from django import template

register = template.Library()


def format_market_cap_tag(value):
    """Formats the market capitalization value.

    Args:
        value (float): The market capitalization value to be formatted.

    Returns:
        str: The formatted market capitalization value.
    """
    return format_market_cap(value)


register.filter("format_market_cap", format_market_cap_tag)
