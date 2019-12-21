from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .models import GameForm
from .models import TreasureForm
from .models import Treasure
from django.shortcuts import render_to_response, get_object_or_404, redirect

def view(request):
    return render(request, 'view.html')

def create(request):
    form = GameForm()
    return render(request, 'create.html', {'form':form})

def treasure_create(request):
    form = TreasureForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        #return HttpResponseRedirect('treasure/list.html')
        return redirect('treasure_list')
    return render(request, 'treasure/create.html', {'form':form})

def treasure_list(request):
    treasure_list = Treasure.objects.all().order_by('id')
    return render(request,'treasure/list.html', {'treasure_list':treasure_list})