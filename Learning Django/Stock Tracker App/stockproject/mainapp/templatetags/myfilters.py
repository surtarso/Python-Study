from django import template


register = template.Library()

@register.filter

## mapping is the dictionary
def get(mapping, key):
    return mapping.get(key, '')