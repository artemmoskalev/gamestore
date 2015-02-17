from django.conf.urls import patterns, url, include
from authentication.views import request_register_page, request_login_page, request_logout, request_register_validate

urlpatterns = patterns('',
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r"^register/?$",     request_register_page),
    url(r"^register/validate/$", request_register_validate),
    url(r"^login/$",     request_login_page),    
    url(r"^logout/$", request_logout)
)
