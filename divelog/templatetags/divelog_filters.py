'''
Created on 4. 7. 2012.

@author: ihabunek
'''

from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils import simplejson
from django import template

import math
import md5
import urllib
import logging
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def formatTime(time):
    '''
    Takes number of seconds as an integer, and returns the formatted duration.
    '''
    
    minutes = math.floor(time / 60)
    hours = math.floor(minutes / 60)
    minutes -= hours * 60;
    
    if hours > 0:
        return '%d h %02d min' % (hours, minutes)
    else:
        return '%02d min' % (minutes) 

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

