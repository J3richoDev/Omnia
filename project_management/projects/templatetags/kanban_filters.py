from django import template

register = template.Library()

@register.filter
def replace_underscore(value):
    """Replaces underscores with spaces in the given string."""
    return value.replace('_', ' ')
