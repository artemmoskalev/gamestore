from django.conf.urls import patterns, url
from gamedata.views import request_index_page, request_common_page, request_category_page, request_game_page

urlpatterns = patterns('',    
    url(r'^$', request_index_page),
    url(r'^(games|about)/$', request_common_page),
    url(r'^games/(action|puzzle|adventure|sport|strategy|misc)/$', request_category_page),
    url(r'^games/(.*)/$', request_game_page),
)
