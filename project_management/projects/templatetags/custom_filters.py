from django import template

register = template.Library()

@register.filter
def replace_underscore(value):
    """Replaces underscores with spaces in the given string."""
    return value.replace('_', ' ')

@register.filter
def get_item(value, key):
    """Retrieve an item from a list by key."""
    for item in value:
        if item.id == int(key):
            return item
    return None
