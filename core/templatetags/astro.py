import subprocess
import datetime
import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='add_minutes')
def add_minutes(base, value):
    return base + datetime.timedelta(minutes=value)


@register.filter(name='at_least')
def at_least(limit, value):
    return max(limit, value)


@register.filter(name='replace')
def replace(string, args):
    find = args.split(args[0])[1]
    repl = args.split(args[0])[2]

    return mark_safe(re.sub(find, repl, string))


@register.filter
def pandoc(text: str) -> str:
    text = text.encode('utf-8')
    completed = subprocess.run(["pandoc", '--to', 'html'], input=text, capture_output=True)
    return completed.stdout.decode('utf-8')


