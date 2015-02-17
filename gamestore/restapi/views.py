from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

#For json api
import json
from django.http import Http404
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from gamedata.models import Game

from django.contrib.auth.models import User

from restapi.models import ApiKey

from developer.views import get_transactions_by_game

from restapi.viewsHelpers import make_and_get_key, make_key_for


""" REST API for the Gamestores games"""
def request_game_data(request):

    try:
        games = Game.objects.all()

        name = request.GET.get('name')
        if name:
            games = games.filter(name__contains=name)

        exaname = request.GET.get('exactname')
        if exaname:
            games = games.filter(name__exact=exaname)

        category = request.GET.get('category')
        if category:
            games = games.filter(category__iexact=category)

        maker = request.GET.get('publisher')
        if maker:
            games = games.filter(maker__username__iexact=maker)
        
        orderby = request.GET.get('orderby')
        if orderby:
            orderby = str(orderby)
            print("Order by: " + orderby)
            if(orderby == "name"):
                games = games.order_by("name")
            if(orderby == "category"):
                games = games.order_by("category")
            if(orderby == "price"):
                games = games.order_by("price")
                
        order = request.GET.get('order')
        if order:
            order = str(order)
            if(order == "reverse"):
                games = games.reverse()

        showmaxamount = request.GET.get('showmaxamount')
        if showmaxamount:
            games = games[:int(showmaxamount)]
        
        jsonData = []

        for game in games:
                jsonData.append({
                    "name":game.name,
                    "category":game.category,
                    "description":game.description,
                    "price":game.price,
                    "publisher":game.maker.username,
                })

        #print(jsonData)

        return makeJsonResponse(request, jsonData)
    
    except:    
        raise Http404("Sorry, api failed")


def request_developer_data(request):

    username = request.GET.get('user')
    key = request.GET.get('key')

    if(key is None or username is None):
        raise Http404("Request needs to have username and key defined")

    user = get_object_or_404(User, username=username)

    if(user is None):
        raise Http404("Requested user not found")

    if(user.key.key == key):

        try:

            year = request.GET.get('year')
            if( year ):
                year = int(year)

            reverse = False
            order = request.GET.get('order')
            if order:
                order = str(order)
                if(order == "reverse"):
                    reverse = True

            gameRevenues = get_transactions_by_game(user, year=year, reverse=reverse)


            showmaxamount = request.GET.get('showmaxamount')
            if showmaxamount:
                gameRevenues = gameRevenues[:int(showmaxamount)]

            jsonData = []

            for gamerevenue in gameRevenues:
                jsonData.append({
                    "name":gamerevenue["game"].name,
                    "category":gamerevenue["game"].category,
                    "price":gamerevenue["game"].price,
                    "copies_sold":gamerevenue["copies_sold"],
                    "revenue":gamerevenue["revenue"]
                })

            #print(jsonData)

            return makeJsonResponse(request, jsonData)
        
        except:    
            raise Http404("Sorry, api failed")

    raise Http404("Frong key for user")

#Helper method for sending the json data (With callback)
def makeJsonResponse(request, jsonData):
    #data = json.dumps(jsonData) 
    #data = renderers.JSONRenderer().render(jsonData, 'application/json')
    data = json.dumps(jsonData, cls=DjangoJSONEncoder)

    #If there is callback we should wrap it in function (function name=calback name)
    callback = request.GET.get('callback')
    if callback:
        data = '%s(%s)' % (callback, data)    

    return HttpResponse(data, content_type='application/json')