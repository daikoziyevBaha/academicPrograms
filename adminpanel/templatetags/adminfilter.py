from asyncio.windows_events import NULL
from django import template
from django.template.defaultfilters import stringfilter
import json
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name = 'get_file_name')
def get_file_name(file):
    if len(file.url) > 1:
        return file.url.split('/')[3]
    else:
        return '---'