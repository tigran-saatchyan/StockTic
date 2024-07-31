# stocks/templatetags/custom_tags.py
from django import template

register = template.Library()

@register.simple_tag
def active_url(request, url):
    if request.path.startswith(url):
        return 'active'
    return ''
