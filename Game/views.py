from django.shortcuts import render


# Create your views here.
from Game.models import Game


def index(request):
    return render(request, "view.html")


def createGame(request):
    # prueba guardado coordenadas
    lat = request.POST['lat']
    lon = request.POST['lon']
    newGame = Game()
    newGame.name = 'prueba'
    newGame.geolocation_center = lat, lon
    newGame.save()
    return render(request, "view.html")
