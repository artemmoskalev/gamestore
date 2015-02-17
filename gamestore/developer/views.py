from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required
from django.core.context_processors import csrf
from developer.forms import DeveloperGameForm
from django.http import HttpResponseRedirect

#For datetime to month conversion
from django.db import connection

#For calculating stats
from django.db.models import Sum, Count
import datetime

#Needed gamedata models
from gamedata.models import Game, Transaction

#For ApiKey
from restapi.viewsHelpers import make_and_get_key

#permission_required is needed to check permissions - add to all view methods (raise exception is to redirect to 403.html - same as Http404 exception)
@permission_required('gamedata.can_publish', raise_exception=True)
def request_developer_base(request):

    stats_by_game = get_transactions_by_game(request.user)

    context = {}

    context["five_most_revenue"] = stats_by_game[:5]

    revenue = 0.0

    total_revenue = Transaction.objects.filter( game__maker = request.user ).aggregate( Sum('amount') )["amount__sum"] 

    if( total_revenue is not None ):
        revenue = total_revenue

    context["total_revenue"] = revenue
    context["api_key"] = make_and_get_key(request.user)

    return render_to_response("developer/dev_overview.html", context, context_instance=RequestContext(request))




#permission_required is needed to check permissions - add to all view methods (raise exception is to redirect to 403.html - same as Http404 exception)
@permission_required('gamedata.can_publish', raise_exception=True)
def request_developer_inventory(request):
    context = {}
    context["games"] = request.user.madeGames.all()

    return render_to_response("developer/dev_inventory.html", context, context_instance=RequestContext(request))


#permission_required is needed to check permissions - add to all view methods (raise exception is to redirect to 403.html - same as Http404 exception)
@permission_required('gamedata.can_publish', raise_exception=True)
def request_developer_edit_game(request, pk):
    if(pk):
        game = get_object_or_404(Game, pk=pk)
        if(game.maker == request.user):

            context = {}
            context.update( csrf(request) )
            #We found the game and request.user is actually maker of the game
            if( request.method == "POST" ):
                form = DeveloperGameForm( request.POST, instance=game )
                if( form.is_valid() ):
                    form.save()
                    return HttpResponseRedirect("/developer/inventory/")
                
                else: #Form is not valid
                    context["error"] = "Form has failed validation! " + form.errors
                    context["form"] = form
                    return render_to_response( 'developer/dev_edit_game.html' , context_instance=RequestContext(request, context))
 
            context["form"] = DeveloperGameForm(instance=game)
            return render_to_response( 'developer/dev_edit_game.html' , context_instance=RequestContext(request, context))

        return render_to_response( '403.html' , context_instance=RequestContext(request))

    return render_to_response( '404.html' , context_instance=RequestContext(request))


#permission_required is needed to check permissions - add to all view methods (raise exception is to redirect to 403.html - same as Http404 exception)
@permission_required('gamedata.can_publish', raise_exception=True)
def request_developer_add_game(request):

    context = {}
    #If form request method is post, we should get the data from form, validate and save it
    if (request.method == "POST"):
        form = DeveloperGameForm( request.POST )
        if( form.is_valid() ):
            game = form.save(commit=False)
            game.maker = request.user
            form.save()
            return HttpResponseRedirect("/developer/inventory/")

        else: #Form is not valid!
            context["error"] = "Form has failed validation! " + str(form.errors)
            context["form"] = form
            return render_to_response( 'developer/dev_add_game.html' ,context , context_instance=RequestContext(request))


    #If not post from form, we just give the as response 
    context.update( csrf(request) )
        
    context["form"] = DeveloperGameForm()

    return render_to_response( "developer/dev_add_game.html", context, context_instance=RequestContext(request) )

def request_developer_delete_game(request, pk):

    errors = []
    game = get_object_or_404(Game, pk=pk)

    if (game.maker == request.user):
        if request.method == "POST":

            if 'delete_game' in request.POST:
                game.delete()
                return HttpResponseRedirect("/developer/inventory/")
            else:
                errors.append("You must check the checkbox")  
                

            
        context = {}
        context.update(csrf(request))   
        context["errors"] = errors
        context["game"] = game
        return render_to_response("developer/dev_delete_game.html", context, context_instance=RequestContext(request))

    else: #Someoni is trying to acces elses game
        return render_to_response("403.html", context_instance=RequestContext(request))


#permission_required is needed to check permissions - add to all view methods (raise exception is to redirect to 403.html - same as Http404 exception)
@permission_required('gamedata.can_publish', raise_exception=True)
def request_developer_statistics(request):

    year = request.GET.get('year')

    if year is None:
        year = str(datetime.datetime.now().year)

    stats_by_game = get_transactions_by_game(request.user, year = year)
    stats_by_month = get_transaction_by_month(request.user, year=year)

    context = {}

    context["stats_by_game"] = stats_by_game  
    context["stats_by_month"] = stats_by_month
    context["year"] = year 
    context["last_year"] = int(year) - 1
    context["next_year"] = int(year) + 1

    return render_to_response("developer/dev_stats.html", context, context_instance=RequestContext(request))

#This is helper method to get developers stats by game
def get_transactions_by_game(user, year=None, reverse=True):
    games = user.madeGames.all()

    bought_counts = []

    for game in games:

        transactions = game.transactions

        if year:
            transactions = transactions.filter( time__year = year)

        number_of_transactions = transactions.count()

        revenue = transactions.aggregate( Sum('amount') )["amount__sum"] 

        if revenue is None:
            revenue = 0.0

        games_stats = { "game": game, "copies_sold": number_of_transactions, "revenue" : revenue }

        bought_counts.append( games_stats )

    return sorted(bought_counts, key=lambda k: k['revenue'], reverse=reverse) 

#This is helper method to get developers stats by month
def get_transaction_by_month(user, year=None):
    transactions = Transaction.objects.filter( game__maker = user )
    if year:
        transactions = transactions.filter( time__year = year )

    truncate_date = connection.ops.date_trunc_sql('month', 'time')
    qs = transactions.extra({'month':truncate_date})
    report = qs.values('month').annotate( revenue = Sum('amount'), copies_sold = Count('pk')).order_by('month')

    return report

"""
def get_bought_of_transactions(transactions):
    queryset = Model1.objects.annotate(model2_price=Sum('model2_set__price'))
"""   





