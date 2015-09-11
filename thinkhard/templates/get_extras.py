from django import template

register = template.Library()

@register.filter(name='get')
def get(dic, key):
    return dic.get(key, None)

register.filter('get', get)   