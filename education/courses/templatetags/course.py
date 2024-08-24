from django import template

register = template.Library()


@register.filter
def model_name(obj):
    """
    Return model_name of obj
    """
    try:
        return obj._meta.model_name
    except AttributeError:
        return None
