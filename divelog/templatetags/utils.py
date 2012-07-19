from django import template
from django.core.serializers import serialize
from django.core.urlresolvers import reverse
from django.db.models.query import QuerySet
import json

register = template.Library()

@register.simple_tag
def active(request, view_name):
    view_url = reverse(view_name)
    return 'active' if request.path.startswith(view_url) else ''

@register.filter
def sec_to_min(seconds):
    "Returns number minutes in given number of seconds rounded to nearest int."
    return int(round(seconds / 60)) if seconds else ''

@register.filter
def jsonify(input):
    if isinstance(input, QuerySet):
        return serialize('json', input)
    return json.dumps(input)
