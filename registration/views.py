from django.shortcuts import render, redirect
from django.template import loader

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout

from django.http import HttpResponse

def index(request):
    return render(request, 'registration/index.html')
    
def logout(request):
    auth_logout(request)
    return render(request, 'registration/index.html')
