from django import template

register = template.Library()

@register.filter(name='split')
def split(value, key):
    """Разбивает строку по разделителю"""
    return value.split(key) if isinstance(value, str) else value
