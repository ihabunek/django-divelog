from .dev import *

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': 'd:/Projects/git/django_divelog/dev.db',
#    }
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'divelog',
        'USER': 'root',
        'PASSWORD': 'starseed',
        'HOST': '',
        'PORT': '',
    }
}