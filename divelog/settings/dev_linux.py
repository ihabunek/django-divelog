from .dev import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/ihabunek/divelog.db',
    }
}

WSGI_APPLICATION = 'divelog.wsgi.application'
