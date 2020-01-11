from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse

from .models import GameForm, Game
from .models import TreasureForm
from .models import Treasure
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect


def view(request):
    return render(request, 'view.html')


def create(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            obj = form.save(commit=False)
            obj.creator = request.user
            obj = form.save()

            return HttpResponseRedirect(reverse('treasure_create', kwargs={'id': obj.id}))
    else:
        form = GameForm()
    return render(request, 'create.html', {'form':form})


def treasure_create(request, id):
    form = TreasureForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            treasure = form.save(commit=False)
            try:
                treasure.game = Game.objects.get(id=id)
                treasure.save()
            except Game.DoesNotExist:
                pass
            # return HttpResponseRedirect(reverse('treasure_list'))
            treasures = treasure.game.game.all()
            return render(request, 'treasure/create.html',
                          {'form': form, 'treasure_list': treasures, 'game_id': treasure.game.id})
        else:
            game = Game.objects.get(id=id)
            return render(request, 'treasure/create.html', {'form': form, 'treasure_list': game.game.all(), 'game_id': id})
    else:
        game = get_object_or_404(Game, id=id)
        treasures = game.game.all()
        return render(request, 'treasure/create.html', {'form': form, 'treasure_list': treasures, 'game_id': id})


def treasure_list(request, game_id=0):
    if game_id != 0:
        treasure_list = Treasure.objects.filter(game=game_id).order_by('id')
    else:
        treasure_list = Treasure.objects.all().order_by('id')
    return render(request,'treasure/list.html', {'treasure_list':treasure_list})