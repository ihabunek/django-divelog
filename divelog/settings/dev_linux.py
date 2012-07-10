from .dev import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/ihabunek/www/django_divelog/dev.db',
    }
}

WSGI_APPLICATION = 'divelog.wsgi.application'
