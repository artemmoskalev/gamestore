from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import permission_required
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
from player.models import GameState, GameScore
from gamedata.models import Game

@permission_required('gamedata.can_play', raise_exception=True)
@csrf_exempt
def save_player_score(request, game_title):
    new_score = float(request.POST["score"])    
    played_game = Game.objects.get(name=game_title)
    playing_user = request.user
    
    # get the highest score in the game for this player
    maxscore = GameScore.objects.filter(player=playing_user, game=played_game).aggregate(Max("score"))['score__max']
    
    game_score = GameScore(score=new_score, player=playing_user, game=played_game)
    game_score.save()   
   
    # check if the new score is maximum or if there are any other scores saved
    if maxscore == None:
        status = "record"
    elif maxscore < new_score:
        status = "record"
    else: 
        status = "saved"    
       
    return HttpResponse(json.dumps({"status": status}), content_type="application/json")

@permission_required('gamedata.can_play', raise_exception=True)
@csrf_exempt
def save_game_state(request, game_title):
    new_state = request.POST["state"]
    played_game = Game.objects.get(name=game_title)
    playing_user = request.user
    
    game_state = GameState.objects.get_or_create(player=playing_user, game=played_game)
    game_state[0].state = new_state    
    game_state[0].save()
    
    return HttpResponse("Your game state has been successfully saved!", content_type="text/plain")


@permission_required('gamedata.can_play', raise_exception=True)
@csrf_exempt
def load_game_state(request, game_title):
    played_game = Game.objects.get(name=game_title)
    playing_user = request.user
    
    try: 
        game_state = GameState.objects.get(player=playing_user, game=played_game)
        message = game_state.state
    except:
        message = "None"
    
    return HttpResponse(message, content_type="text/plain")

