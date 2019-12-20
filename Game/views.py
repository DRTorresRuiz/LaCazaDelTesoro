from django.shortcuts import render

from .models import GameForm

def view(request):
    return render(request, 'view.html')

def create(request):
    form = GameForm()
    return render(request, 'create.html', {'form':form})

def treasure(request):
    form = GameForm()
    return render(request, 'treasure.html', {'form':form})