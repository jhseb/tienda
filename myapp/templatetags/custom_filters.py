from django import template

register = template.Library()

@register.filter
def range_filter(value):
    try:
        return range(1, int(value) + 1)
    except ValueError:
        return []