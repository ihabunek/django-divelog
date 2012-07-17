'''
Created on 4. 7. 2012.

@author: ihabunek
'''

from django import template
from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils import simplejson
import math
import md5
import urllib

register = template.Library()

@register.filter
def sec_to_min(seconds):
    "Returns number minutes in given number of seconds rounded to nearest int."
    return int(round(seconds / 60))

@register.filter
def jsonify(input):
    if isinstance(input, QuerySet):
        return serialize('json', input)
    return simplejson.dumps(input)

@register.simple_tag
def gravatar_image(user, size=80):
    email = user.email.strip().lower()
    hash = md5.new(email).hexdigest()
    url = "http://www.gravatar.com/avatar/%s?" % hash
    url += urllib.urlencode({'s': size})
    return url

@register.simple_tag
def gravatar_profile(user, callback) :
    email = user.email.strip().lower()
    hash = md5.new(email).hexdigest()
    url = "http://www.gravatar.com/%s.json?" % hash
    url += urllib.urlencode({'callback': callback })
    return url

