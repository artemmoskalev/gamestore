from django.shortcuts import render_to_response
from gamedata.models import Game, Transaction
from django.template import RequestContext
from player.models import GameScore
from collections import OrderedDict

def request_index_page(request):
    return render_to_response("common_pages/games.html", context_instance=RequestContext(request))

def request_common_page(request, page):    
    return render_to_response("common_pages/"+page+".html", context_instance=RequestContext(request))

def request_category_page(request, query_category):
    resultSet = Game.objects.filter(category=query_category) # query all games by respective category name
    games = []
    for game in resultSet:                                           # iterate the result set, and retrieve respective game images and titles
        games.append({
                "name" : game.name,
                "img_url" : game.generate_game_cover_pic()
            }) 
    return render_to_response("common_pages/game_category.html", context_instance=RequestContext(request, {"games": games}))

def request_game_page(request, game_name):    
    searched_game = Game.objects.get(name=game_name);      
    gamePic = searched_game.generate_game_cover_pic()    
    
    score_dict = OrderedDict()    
    if request.user.is_authenticated() and Transaction.objects.filter(payer=request.user, game=searched_game).exists():
        is_purchased = True        
        scores = GameScore.objects.filter(game=searched_game).order_by("-score")[:10]      
        for score in scores:
            if not score.player.username in score_dict:
                score_dict[score.player.username] = score.score
    else: 
        is_purchased = False    
    
    game_data = {"id":searched_game.pk, "is_purchased":is_purchased, "pic_url":gamePic, "title":searched_game.name, "description":searched_game.description, 
                 "category":searched_game.category, "publisher": searched_game.maker.username, "price":searched_game.price, "highscores":score_dict}   
    
    return render_to_response("common_pages/game.html", context_instance=RequestContext(request, {"game": game_data}))

