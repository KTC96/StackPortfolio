from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def replace(value, arg):
    """
    Replacing filter
    Use `{{ "aaa"|replace:"a|b" }}`
    """
    if len(arg.split('|')) != 2:
        return value

    if value:
        what, to = arg.split('|')
        return value.replace(what, to)
