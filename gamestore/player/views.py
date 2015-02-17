from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required
from django.conf import settings
from hashlib import md5
from gamedata.models import Transaction, Game
from player.models import GameScore
from collections import OrderedDict
from django.http.response import Http404

@permission_required('gamedata.can_play', raise_exception=True)
def request_play_panel(request):
    bought_games = []
    for transaction in Transaction.objects.filter(payer=request.user):
        bought_games.append(transaction.game)
    game_data = {}
    for game in bought_games:
        game_data[game.name] = game.generate_game_cover_pic()
    return render_to_response("panel_parts/game_list.html", RequestContext(request, {"games": game_data}))

@permission_required('gamedata.can_play', raise_exception=True)
def request_score_panel(request):
    bought_games = []
    for transaction in Transaction.objects.filter(payer=request.user):
        bought_games.append(transaction.game)
    games_dict={}
    for bought_game in bought_games:
        score_dict = OrderedDict()
        scores = GameScore.objects.filter(player=request.user, game=bought_game).order_by("-score")
        for score in scores:
            score_dict[score.score] = score.time
        games_dict[bought_game.name] = score_dict      
      
    return render_to_response("panel_parts/score_list.html", RequestContext( request, {"games":games_dict} ))

@permission_required('gamedata.can_play', raise_exception=True)
def request_play(request, game_name):
    try:
        game = Game.objects.get(name=game_name)
    except:
        raise Http404
        
    return render_to_response("play.html", RequestContext(request, {"url":game.url}))

@permission_required('gamedata.can_play', raise_exception=True)
def request_payment(request, game_id):        
    game = Game.objects.get(pk=game_id)    
    pid = str(request.user.pk) + "g" + str(game.pk)
    
    purchase_details = {"name": game.name, "category": game.category, "buyer":request.user.username}
    payment_details = {"pid":pid, "sid":settings.SELLER_ID, "amount":game.price, "checksum":calculate_checksum(pid, game.price), 
                       "success_url": settings.SUCCESS_URL, "cancel_url": settings.CANCEL_URL, "error_url": settings.ERROR_URL}    
    params = {"purchase_details": purchase_details, "payment_details":payment_details}
       
    request_context = RequestContext(request, params)
    
    return render_to_response("payment.html", request_context)

@permission_required('gamedata.can_play', raise_exception=True)
def request_payment_result(request, status=None):    
    params = {}
    if status == "success":               
        if request.GET["checksum"] == calculate_response_checksum(request.GET["pid"], request.GET["ref"]):
            # get the pid and its info about the payment
            pid = request.GET["pid"].split("g")            
            game = Game.objects.get(pk=pid[1])           
           
            # save the information about transaction
            transaction = Transaction(payer=request.user, amount=game.price)
            transaction.game = game
            transaction.save()
            
            params['message'] = "Successful payment!" 
            params['game_name'] = game.name
            params['game_image'] = game.generate_game_cover_pic()
            
        else:
            params['message'] = "Untrusted connection error! Payment not performed"
            status = "error"
            
    elif status == "cancel":           
        pid = request.GET["pid"].split("g")            
        game = Game.objects.get(pk=pid[1])
        
        params['message'] = "Payment cancelled"
        params['game_id'] = game.pk
           
    else:                 
        params['message'] = "Payment error!" 
        
    params['status'] = status
    request_context = RequestContext(request, params)
    return render_to_response("payment_outcome.html", request_context)


""" utility methods used to turn payment and payment response parameters into md5 hash """
def calculate_checksum(payment_id, amount):
    checksum = "pid={}&sid={}&amount={}&token={}".format(payment_id, settings.SELLER_ID, amount, settings.SECRET_KEY)
    checksum_encoded = md5(checksum.encode("ascii"))
    return checksum_encoded.hexdigest()

def calculate_response_checksum(payment_id, reference):
    checksum = "pid={}&ref={}&token={}".format(payment_id, reference, settings.SECRET_KEY)
    checksum_encoded = md5(checksum.encode("ascii"))
    return checksum_encoded.hexdigest()