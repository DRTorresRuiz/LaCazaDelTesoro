from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse

from .models import GameForm
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

            obj = form.save()
            return HttpResponseRedirect(reverse('treasure_create', kwargs={'id': obj.id}))
    else :
        form = GameForm()
    return render(request, 'create.html', {'form':form})


def treasure_create(request, id):
    form = TreasureForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        #return HttpResponseRedirect('treasure/list.html')
        return redirect('treasure_list')
    return render(request, 'treasure/create.html', {'form':form})


def treasure_list(request):
    treasure_list = Treasure.objects.all().order_by('id')
    return render(request,'treasure/list.html', {'treasure_list':treasure_list})