from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def replace(value, arg):
    """
    Replacing filter.
    Use `{{ "aaa"|replace:"a|b" }}`.
    """
    if '|' not in arg:
        return value

    what, to = arg.split('|', 1)
    if to not in value:
        return value.replace(what, to)
    return value
