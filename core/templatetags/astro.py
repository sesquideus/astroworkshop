from django import template
import datetime

register = template.Library()

@register.filter(name='add_minutes')
def add_minutes(base, value):
    return base + datetime.timedelta(minutes=value)
