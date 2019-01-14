from django import template




def list_fields(model):
	return [field.name for field in model._meta.get_fields() if not field.is_relation and field.name != 'id' ]

def get_value(model, value):

	return getattr(model, value)


def evento_fields(model):

	return [campo.name for campo in model._meta.get_fields() if not campo.is_relation and campo.name !='id']



def hola(username):
	return "hola" + username



register = template.Library()

register.filter('evento_fields', evento_fields)
register.filter('list_fields', list_fields) 
register.filter('hola',hola)

register.filter('get_value', get_value)