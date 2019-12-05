from django.shortcuts import render

from .models import GameForm

def view(request):
    return render(request, 'view.html')

def create(request):
    form = GameForm()
    return render(request, 'create.html', {'form':form})
