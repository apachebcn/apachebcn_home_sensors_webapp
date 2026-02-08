# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

from django import template
register = template.Library()

@register.filter
def get_item(value, arg):
    """Obtiene un campo del formulario dado el nombre del campo"""
    return value.get(arg)

@register.filter
def get_field_value(obj, field_name):
    """Obtiene el valor de un campo de un modelo basado en el nombre del campo."""
    return getattr(obj, field_name, None)
