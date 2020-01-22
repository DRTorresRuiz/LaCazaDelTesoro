from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from Game.models import Game

# Create your views here.

@login_required(login_url='/registration/')
def index(request):

    games = Game.objects.all()
    num_games_finished = len(Game.objects.filter(status = 1))
    num_games_active = len(Game.objects.filter(status = 2))
    num_winners = len(set(filter(None.__ne__, Game.objects.all().values_list('winner', flat=True))))

    context = {
        'num_games_finished': num_games_finished,
        'num_games_active': num_games_active,
        'num_winners': num_winners,
	'games': games
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index_homepage.html', context=context)
