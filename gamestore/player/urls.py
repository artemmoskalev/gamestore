from django.conf.urls import patterns, url
from player.views import request_play_panel, request_score_panel, request_play, request_payment, request_payment_result
from player.views_ajax import save_player_score, save_game_state, load_game_state

urlpatterns = patterns('',
    url(r'^playerpanel/$',     request_play_panel),  
    url(r'^scorepanel/$',     request_score_panel),    
    url(r'^play/([^/]+)/$',     request_play),  
    url(r'^play/(.+)/submitscore/$',     save_player_score),  
    url(r'^play/(.+)/savestate/$',     save_game_state),
    url(r'^play/(.+)/loadstate/$',     load_game_state),
    url(r'^payment/(\d+)/$',     request_payment),
    url(r'^payment/success$',    request_payment_result,  {"status": "success"}),
    url(r'^payment/cancel$',     request_payment_result,  {"status": "cancel"}),       
    url(r'^payment/error$',      request_payment_result,  {"status": "error"}),    
)
