from django.contrib import admin

# Register your models here.
from Game.models import Game, Treasure

admin.site.register(Game)
admin.site.register(Treasure)
