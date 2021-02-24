from django import template
import datetime

register = template.Library()

@register.filter(name='add_minutes')
def add_minutes(base, value):
    return base + datetime.timedelta(minutes=value)

@register.filter(name='at_least')
def at_least(limit, value):
    return max(limit, value)
