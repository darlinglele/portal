from django import template

register = template.Library()

@register.filter(name='get')
def get(dic, key):
    if type(dic) == type({}):
    	return dic.get(key,None)
    else:
        return ''	
register.filter('get', get)   