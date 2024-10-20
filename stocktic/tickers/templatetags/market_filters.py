from django import template

from custom_utils.utils import format_market_cap

register = template.Library()


def format_market_cap_tag(value):
    format_market_cap(value)


register.filter("format_market_cap", format_market_cap)
