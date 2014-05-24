from django import template

register = template.Library()

from ..models import Config

def get_opt(key,fallback=None):
    return Config.get(key,fallback)

register.simple_tag(get_opt)
register.simple_tag(get_opt,name="option")
