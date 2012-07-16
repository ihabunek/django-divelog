from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from divelog.views import ImportWizard
from divelog.forms import ImportForm1, ImportForm2

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^/?$', 'divelog.views.index'),
    url(r'^gallery/$', 'divelog.views.gallery'),
    
    url(r'^settings/$', 'divelog.views.settings'),
    url(r'^settings/account/$', 'divelog.views.settings_account'),
    url(r'^settings/password/$', 'divelog.views.settings_password'),
    
    url(r'^dives/?$', 'divelog.views.dive_list'),
    url(r'^dives/new/?$', 'divelog.views.dive_add'),
    
    url(r'^dive/(?P<dive_id>\d+)/$', 'divelog.views.dive_view'),
    url(r'^dive/(?P<dive_id>\d+)/edit/$', 'divelog.views.dive_edit'),
    url(r'^dive/(?P<dive_id>\d+)/trash/$', 'divelog.views.dive_trash'),
    url(r'^dive/(?P<dive_id>\d+)/restore/$', 'divelog.views.dive_restore'),
    url(r'^dive/(?P<dive_id>\d+)/samples.json$', 'divelog.views.dive_samples_json'),
    url(r'^dive/(?P<dive_id>\d+)/events.json$', 'divelog.views.dive_events_json'),

    url(r'^uploads/$', 'divelog.views.upload_list'),
    url(r'^upload/new/$', 'divelog.views.upload_add'),
    url(r'^upload/import/$', 'divelog.views.upload_import'),
    url(r'^upload/(?P<upload_id>\d+)/$', 'divelog.views.upload_view'),
    
    
    url(r'^accounts/login/?$', 'django.contrib.auth.views.login', { 'template_name': 'accounts/login.html'}),
    url(r'^accounts/logout/?$', 'django.contrib.auth.views.logout', { 'next_page': '/'}),
    url(r'^accounts/profile/?$', 'divelog.views.profile'),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    url(r'^wizard/$', ImportWizard.as_view([
        ImportForm1,
        ImportForm2,
    ])),
)

# for development, see:
# https://docs.djangoproject.com/en/dev/howto/static-files/#staticfiles-development
urlpatterns += staticfiles_urlpatterns()
