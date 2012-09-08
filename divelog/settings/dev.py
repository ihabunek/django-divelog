from .base import *

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# set up Django Debug Toolbar if installed
try:
    import debug_toolbar
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TOOLBAR_CALLBACK': lambda *args, **kwargs: True
    }
except ImportError:
    pass

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'divelog',
        'USER': 'root',
        'PASSWORD': 'starseed',
        'HOST': '',
        'PORT': '',
        'OPTIONS': { 
            'init_command': 'SET storage_engine=INNODB;' 
        }
    }
}

