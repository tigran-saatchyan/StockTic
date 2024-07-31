from urllib.parse import quote

from django import template

register = template.Library()


@register.filter
def url_encode(value):
    return quote(value, safe='')


@register.filter(name='replace_with_hyphen')
def replace_with_hyphen(value):
    return value.replace('/', '-').replace('^', '-')
