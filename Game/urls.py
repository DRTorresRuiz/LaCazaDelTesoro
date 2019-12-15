from django.contrib import admin
from django.urls import path

# Import your views
import Game.views as game

app_name = "game"

# Add patterns to access to your views
urlpatterns = [
    path('', game.index, name="index"),
    path('save', game.createGame, name="save")
    ]
