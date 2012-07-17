'''
Created on 4. 7. 2012.

@author: ihabunek
'''

from django import template
import md5
import urllib

register = template.Library()

@register.simple_tag
def gravatar_image_url(user, size=80):
    email = user.email.strip().lower()
    digest = md5.new(email).hexdigest()
    url = "http://www.gravatar.com/avatar/%s?" % digest
    url += urllib.urlencode({'s': size})
    return url

@register.simple_tag
def gravatar_image(user, size=80):
    url = gravatar_image_url(user, size)
    return '<img src="%s" alt="User avatar" style="width: %dpx" />' % (url, size);

@register.simple_tag
def gravatar_profile(user, callback) :
    email = user.email.strip().lower()
    digest = md5.new(email).hexdigest()
    url = "http://www.gravatar.com/%s.json?" % digest
    url += urllib.urlencode({'callback': callback })
    return url
