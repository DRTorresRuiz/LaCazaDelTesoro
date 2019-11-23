from django.shortcuts import render
from django.http import HttpResponse

from .models import User

def index(request):
    # return HttpResponse('Hello from Python!')
    
    # user = User.objects.createUser("JOSE")
    # name = User.objects.values_list("name", flat=True)
    # name = User.objects.filter(name__startswith='J').values("name").first()
    # name = User.objects.filter(name__startswith='J').values("name")[0]["name"]
    name = User.objects.filter(name__startswith='J').values("name").first()["name"]
    return render(request, "index.html", {"greetings": name})