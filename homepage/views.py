from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Game.models import Game
from Game.models import Player_Treasure_Found
from Game.models import Treasure
# Create your views here.

@login_required(login_url='/registration/')
def index(request):

    games = Game.objects.all()
    num_games_finished = len(Game.objects.filter(status = 1))
    num_games_active = len(Game.objects.filter(status = 2))
    num_winners = len(set(filter(None.__ne__, Game.objects.all().values_list('winner', flat=True))))
    games_joined = Game.objects.filter(player=request.user)
    games_created = Game.objects.filter(creator=request.user)

    context = {
        'num_games_finished': num_games_finished,
        'num_games_active': num_games_active,
        'num_winners': num_winners,
	    'games': games,
        'games_joined':games_joined,
        'games_created':games_created
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index_homepage.html', context=context)
