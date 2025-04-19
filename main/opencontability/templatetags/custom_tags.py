from django import template

register = template.Library()

@register.filter(name='get_attr')
def get_attr(obj, attr_name):
    return getattr(obj, attr_name, '')
