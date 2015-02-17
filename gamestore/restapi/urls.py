from django.conf.urls import patterns, url
from restapi.views import request_game_data, request_developer_data

urlpatterns = patterns('',    
    url(r'^games.json', request_game_data),
    url(r'^developer.json', request_developer_data),
)
