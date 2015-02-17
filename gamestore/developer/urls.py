from django.conf.urls import patterns, url
from developer.views import request_developer_base, request_developer_inventory, request_developer_add_game, request_developer_edit_game, request_developer_statistics, request_developer_delete_game

urlpatterns = patterns('',
    url(r"^$",     request_developer_base),
    url(r"^inventory/$",     request_developer_inventory),
    url(r"^inventory/add/$",     request_developer_add_game),
    url(r"^inventory/edit/(.*)/$",     request_developer_edit_game),
    url(r"^inventory/delete/(.*)/$",     request_developer_delete_game),
    url(r"^stats/$",     request_developer_statistics),
)
