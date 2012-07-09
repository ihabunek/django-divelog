from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^/?$', 'divelog.views.index'),
    url(r'^dives/?$', 'divelog.views.dives'),
    url(r'^import/?$', 'divelog.views.upload'),
    url(r'^dive/(?P<dive_id>\d+)/$', 'divelog.views.dive'),
    url(r'^dive/(?P<dive_id>\d+)/edit/$', 'divelog.views.dive_edit'),
    
    url(r'^accounts/login/?$', 'django.contrib.auth.views.login', { 'template_name': 'accounts/login.html'}),
    url(r'^accounts/logout/?$', 'django.contrib.auth.views.logout', { 'next_page': '/'}),
    url(r'^accounts/profile/?$', 'divelog.views.profile'),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

# for development, see:
# https://docs.djangoproject.com/en/dev/howto/static-files/#staticfiles-development
urlpatterns += staticfiles_urlpatterns()
