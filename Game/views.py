from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.http import HttpResponse
from datetime import datetime

from .models import GameForm, Game
from .models import TreasureForm
from .models import Treasure
from .models import Player_Treasure_Found, Player_Treasure_Found_Form
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect

def details(request, game_id):
    gameObj = Game.objects.get(pk = game_id)
    room_name = game_id
    all_treasures = Treasure.objects.filter(game = gameObj)
    found_treasures_obj = Player_Treasure_Found.objects.filter(game_id = gameObj)
    found_treasures = found_treasures_obj.values_list('treasure_id', flat=True)
    context = {'game': gameObj, 'all_treasures': all_treasures, 'found_treasures_obj': found_treasures_obj, 'found_treasures': found_treasures, 'room_name': room_name, }
    return render(request, 'details.html', context=context)

def join(request, game_id):
    game = Game.objects.get(pk = game_id)
    game.player.add(request.user)
    game.save()
    return redirect('homepage:index')

def leave(request, game_id):
    game = Game.objects.get(pk = game_id)
    game.player.remove(request.user)
    game.save()
    return redirect('homepage:index')

def found(request, treasure_id):
    treasure = Treasure.objects.get(pk = treasure_id)
    if request.method == 'POST':
        form = Player_Treasure_Found_Form(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.treasure_id = treasure
            obj.player = request.user
            obj.prove_date = datetime.now()
            obj.game_id = treasure.game
            obj = form.save()
            return redirect('homepage:index')
    else:
        form = Player_Treasure_Found_Form()
    context = { 'form': form, 'treasure': treasure,  }
    return render(request, 'treasure/found.html', context = context)

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

def play(request, game_id):
    gameObj = Game.objects.get(pk = game_id)
    room_name = game_id
    form = Player_Treasure_Found_Form(request.POST, request.FILES)
    #treasures = Treasure.objects.filter(game = gameObj)
    # ** treasures_found = Player_Treasure_Found.objects.filter(game=gameObj, player=request.user).values('treasure__id')
    # ** all_treasures_found = Treasure.objects.filter(pk__in=treasures_found)
    #found_treasures_obj = Player_Treasure_Found.objects.filter(game_id = gameObj)
    #found_treasures = found_treasures_obj.values_list('treasure_id', flat=True)
    #context = {'game': gameObj, 'all_treasures': all_treasures, 'found_treasures_obj': found_treasures_obj, 'found_treasures': found_treasures, 'room_name': room_name, }
    if request.method == 'POST':
        # check whether it's valid:
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.player = request.user
                obj.game = Game.objects.get(id=game_id)
                obj.treasure = Treasure.objects.get(id=request.POST.get('treasure_id'))
                obj = form.save()
            except Treasure.DoesNotExist:
                pass
            #return HttpResponseRedirect(reverse('play', kwargs={'id': obj.id}))
            #else:
            #    form = GameForm()
            #return render(request, 'play.html', {'form':form})
    all_treasures_found = Player_Treasure_Found.objects.filter(game=gameObj, player=request.user)
    treasures_found = Player_Treasure_Found.objects.filter(game=gameObj, player=request.user).values()
    treasures_found_ids = [t['treasure_id'] for t in treasures_found]
    if treasures_found_ids is not None:
        all_treasures_available = Treasure.objects.filter(game=gameObj).exclude(pk__in=treasures_found_ids)
    context = {'game': gameObj, 'all_treasures_found': all_treasures_found,'all_treasures_available': all_treasures_available, 'room_name': room_name, }
    context.update({"form": form})
    return render(request, 'play.html', context=context)
