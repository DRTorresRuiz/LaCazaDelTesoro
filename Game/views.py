import math

from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.http import HttpResponse, Http404
from datetime import datetime

from .models import GameForm, Game, Status
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
            form = TreasureForm()
            center_game = getCenter(treasure.game.north_east_bound, treasure.game.south_west_bound)
            return render(request, 'treasure/create.html',
                          {'form': form, 'treasure_list': treasures, 'center_game': center_game,
                           'treasure_points': [[float(o.position.latitude), float(o.position.longitude), o.name] for o in treasures],
                           'game_id': treasure.game.id, 'coord_ne': treasure.game.north_east_bound,
                           'coord_sw': treasure.game.south_west_bound})
        else:
            game = Game.objects.get(id=id)
            center_game = getCenter(game.north_east_bound, game.south_west_bound)
            return render(request, 'treasure/create.html',
                          {'form': form, 'treasure_list': game.game.all(), 'center_game': center_game,
                           'treasure_points': [[float(o.position.latitude), float(o.position.longitude), o.name] for o in game.game.all()],
                           'game_id': id, 'coord_ne': game.north_east_bound, 'coord_sw': game.south_west_bound})
    else:
        game = get_object_or_404(Game, id=id)
        center_game = getCenter(game.north_east_bound, game.south_west_bound)
        treasures = game.game.all()
        return render(request, 'treasure/create.html',
                      {'form': form, 'treasure_list': treasures, 'center_game': center_game,
                       'treasure_points': [[float(o.position.latitude), float(o.position.longitude), o.name] for o in treasures],
                       'game_id': id, 'coord_ne': game.north_east_bound, 'coord_sw': game.south_west_bound})


def treasure_list(request, game_id=0):
    if game_id != 0:
        treasure_list = Treasure.objects.filter(game=game_id).order_by('id')
    else:
        treasure_list = Treasure.objects.all().order_by('id')
    return render(request,'treasure/list.html', {'treasure_list':treasure_list})


# distance between two coordinates (haversine) in km
def distanceBetweenPoints(lat_1, lng_1, lat_2, lng_2):
    # change to radians
    lng_1, lat_1, lng_2, lat_2 = map(math.radians, [lng_1, lat_1, lng_2, lat_2])

    d_lat = lat_2 - lat_1
    d_lng = lng_2 - lng_1

    temp = (
            math.sin(d_lat / 2) ** 2
            + math.cos(lat_1)
            * math.cos(lat_2)
            * math.sin(d_lng / 2) ** 2
    )

    return 6373.0 * (2 * math.atan2(math.sqrt(temp), math.sqrt(1 - temp)))


def getCenter(pointA, pointB):
    lat = (pointA.latitude + pointB.latitude) / 2
    lng = (pointA.longitude + pointB.longitude) / 2
    return [float(lat), float(lng)]


def control(request, game_id):
    gameObj = Game.objects.get(pk=game_id)
    if gameObj.creator is not request.user and not request.user.is_superuser:
        return redirect('homepage:index')
    room_name = game_id
    center_game = getCenter(gameObj.north_east_bound, gameObj.south_west_bound)
    context = {'game': gameObj,
               'treasure_points': [[float(o.position.latitude), float(o.position.longitude), o.name] for o in
                                    gameObj.game.all()],
               'treasure_list': gameObj.game.prefetch_related('treasure').all(),
               'coord_ne': gameObj.north_east_bound, 'coord_sw': gameObj.south_west_bound, 'center_game': center_game,
               'room_name': room_name}
    return render(request, 'control.html', context=context)


def play(request, game_id):
    gameObj = Game.objects.get(pk=game_id)
    room_name = game_id
    form = Player_Treasure_Found_Form(request.POST, request.FILES)
    location_error = None
    win_msg = None
    end_msg = None
    if request.method == 'POST':
        # check whether it's valid:
        if form.is_valid():
            try:
                if gameObj.status == Status.Finalized:
                    end_msg = 'Sorry the game are finish'
                else:
                    # check if coordinates are correct
                    treasure = Treasure.objects.get(id=request.POST.get('treasure_id'))
                    if distanceBetweenPoints(treasure.position.latitude, treasure.position.longitude,
                                              form.cleaned_data['position'][0], form.cleaned_data['position'][1]) < 0.5:
                        obj = form.save(commit=False)
                        obj.player = request.user
                        obj.game = Game.objects.get(id=game_id)
                        obj.treasure = treasure
                        obj = form.save()
                    else:
                        # error message not valid position
                        location_error = "Sorry, you were wrong"
            except Treasure.DoesNotExist:
                pass
    all_treasures_found = Player_Treasure_Found.objects.filter(game=gameObj, player=request.user)
    treasures_found = Player_Treasure_Found.objects.filter(game=gameObj, player=request.user)
    treasures_found_ids = [t.treasure.id for t in treasures_found]
    if treasures_found_ids is not None:
        all_treasures_available = Treasure.objects.filter(game=gameObj).exclude(pk__in=treasures_found_ids)

    if not gameObj.player.filter(pk=request.user.id).exists():
        end_msg = 'You aren`t join in this game'
    elif len(all_treasures_available) < 1 and gameObj.winner is None:
        # you win but you can be the first or not
        win_msg = 'You win the game!'
        gameObj.winner = request.user
        gameObj.status = Status.Finalized
        gameObj.save()

    context = {'game': gameObj, 'all_treasures_found': all_treasures_found,
               'treasure_points': [[float(o.position.latitude), float(o.position.longitude), o.treasure.name] for o in treasures_found],
               'all_treasures_available': all_treasures_available, 'room_name': room_name,
               'locationError': location_error, 'win_msg': win_msg, 'end_msg': end_msg}
    context.update({"form": form})
    return render(request, 'play.html', context=context)


def reset(request, game_id):
    gameObj = Game.objects.get(pk=game_id)
    if gameObj.creator == request.user:
        Player_Treasure_Found.objects.filter(game=gameObj).delete()
        gameObj.winner = None
        gameObj.status = Status.InProgress
        gameObj.save()
        return HttpResponse('ok')
    else:
        raise Http404
