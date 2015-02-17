from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('gamedata.urls')),
    url(r'^', include('authentication.urls')),
    url(r'^', include('player.urls')), 
    url(r'^developer/', include('developer.urls')),  
    url(r'^api/', include('restapi.urls')),      
)
urlpatterns += staticfiles_urlpatterns()    # adds static file url patterns to the coded ones
