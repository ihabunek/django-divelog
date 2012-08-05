from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('divelog.views',
    url(r'^/?$',       'main.index',   name='divelog_index'),
    url(r'^gallery/$', 'main.gallery', name='divelog_gallery'),
    
    url(r'^settings/$',          'main.settings'),
    url(r'^settings/account/$',  'main.settings_account',  name='divelog_settings_account'),
    url(r'^settings/password/$', 'main.settings_password', name='divelog_settings_password'),
    
    url(r'^dives/$',                             'dives.dive_list',         name='divelog_dive_list'),
    url(r'^dives/new/$',                         'dives.dive_add',          name='divelog_dive_add'),
    url(r'^dive/(?P<dive_id>\d+)/$',             'dives.dive_view',         name='divelog_dive_view'),
    url(r'^dive/(?P<dive_id>\d+)/edit/$',        'dives.dive_edit',         name='divelog_dive_edit'),
    url(r'^dive/(?P<dive_id>\d+)/trash/$',       'dives.dive_trash',        name='divelog_dive_trash'),
    url(r'^dive/(?P<dive_id>\d+)/restore/$',     'dives.dive_restore',      name='divelog_dive_restore'),
    url(r'^dive/(?P<dive_id>\d+)/samples.json$', 'dives.dive_samples_json', name='divelog_dive_samples_json'),
    url(r'^dive/(?P<dive_id>\d+)/events.json$',  'dives.dive_events_json',  name='divelog_dive_events_json'),
    url(r'^dive/(?P<dive_id>\d+)/stats.json$',   'dives.dive_stats_json',   name='divelog_dive_stats_json'),
    
    url(r'^locations/$',                           'locations.location_list',  name='divelog_location_list'),
    url(r'^location/(?P<location_id>\d+)/$',       'locations.location_view',  name='divelog_location_view'),
    url(r'^location/(?P<location_id>\d+)/edit/$',  'locations.location_edit',  name='divelog_location_edit'),
    url(r'^location/(?P<location_id>\d+)/dives/$', 'locations.location_dives', name='divelog_location_dives'),

    url(r'^uploads/$',                   'uploads.upload_list',   name='divelog_upload_list'),
    url(r'^upload/new/$',                'uploads.upload_add',    name='divelog_upload_add'),
    url(r'^upload/import/$',             'uploads.upload_import', name='divelog_upload_import'),
    url(r'^upload/(?P<upload_id>\d+)/$', 'uploads.upload_view',   name='divelog_upload_view'),
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
