from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('divelog.views',
    url(r'^/?$', 'index'),
    url(r'^gallery/$', 'gallery'),
    
    url(r'^settings/$', 'settings'),
    url(r'^settings/account/$', 'settings_account'),
    url(r'^settings/password/$', 'settings_password'),
    
    url(r'^dives/?$', 'dive_list'),
    url(r'^dives/new/?$', 'dive_add'),
    
    url(r'^dive/(?P<dive_id>\d+)/$', 'dive_view'),
    url(r'^dive/(?P<dive_id>\d+)/edit/$', 'dive_edit'),
    url(r'^dive/(?P<dive_id>\d+)/trash/$', 'dive_trash'),
    url(r'^dive/(?P<dive_id>\d+)/restore/$', 'dive_restore'),
    url(r'^dive/(?P<dive_id>\d+)/samples.json$', 'dive_samples_json'),
    url(r'^dive/(?P<dive_id>\d+)/events.json$', 'dive_events_json'),

    url(r'^locations/$', 'location_list'),
    url(r'^location/(?P<location_id>\d+)/$', 'location_view'),
    url(r'^location/(?P<location_id>\d+)/edit/$', 'location_edit'),

    url(r'^uploads/$', 'upload_list'),
    url(r'^upload/new/$', 'upload_add'),
    url(r'^upload/import/$', 'upload_import'),
    url(r'^upload/(?P<upload_id>\d+)/$', 'upload_view'),
)

urlpatterns += patterns('',
    url(r'^accounts/login/?$', 'django.contrib.auth.views.login', { 'template_name': 'accounts/login.html'}),
    url(r'^accounts/logout/?$', 'django.contrib.auth.views.logout', { 'next_page': '/'}),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

# for development, see:
# https://docs.djangoproject.com/en/dev/howto/static-files/#staticfiles-development
urlpatterns += staticfiles_urlpatterns()
