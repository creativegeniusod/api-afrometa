import ast
from django import template

register = template.Library()

@register.filter
def get_type(value):
	return type(value)

@register.filter
def make_dict(val):
    return ast.literal_eval(val)