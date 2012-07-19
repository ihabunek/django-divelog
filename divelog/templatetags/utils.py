from django import template
from django.core.serializers import serialize
from django.core.urlresolvers import reverse
from django.db.models.query import QuerySet
import json

register = template.Library()

@register.simple_tag(takes_context=True)
def active(context, view_name):
    """
    Returns the string 'active' if the current request if for the given view. 
    Otherwise returns an empty string. Used to mark links as acitve in 
    navigation divs.
    """
    path = context['request'].path # request path
    view_url = reverse(view_name)  # view path
    return 'active' if path.startswith(view_url) else ''

@register.filter
def sec_to_min(seconds):
    "Returns number minutes in given number of seconds rounded to nearest int."
    return int(round(seconds / 60)) if seconds else ''

@register.filter
def jsonify(input):
    "Converts given input to a JSON string."
    if isinstance(input, QuerySet):
        return serialize('json', input)
    return json.dumps(input)
