from django import template
from django.core.serializers import serialize
from django.core.urlresolvers import reverse
from django.db.models.query import QuerySet
from django.utils import simplejson

register = template.Library()

@register.simple_tag
def active(request, view):
    url = reverse(view)
    return 'active' if request.path.startswith(url) else ''

@register.filter
def sec_to_min(seconds):
    "Returns number minutes in given number of seconds rounded to nearest int."
    return int(round(seconds / 60)) if seconds else ''

@register.filter
def jsonify(input):
    if isinstance(input, QuerySet):
        return serialize('json', input)
    return simplejson.dumps(input)
