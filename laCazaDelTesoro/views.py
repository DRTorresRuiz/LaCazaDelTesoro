from django.shortcuts import render
from django.http import HttpResponse

# Import models needed
    # from .models import User

def index(request):
    ## Example of interaction with MongoDB
        # user = User.objects.createUser("JOSE")
        # name = User.objects.values_list("name", flat=True)
        # name = User.objects.filter(name__startswith='J').values("name").first()
        # name = User.objects.filter(name__startswith='J').values("name")[0]["name"] # https://stackoverflow.com/questions/32240718/dict-object-has-no-attribute-id
        # name = User.objects.filter(name__startswith='J').values("name").first()["name"]
        # return render(request, "index.html", {"name": name})
    
    ## Example of HttpResponse
        # return HttpResponse('Hello from Python!')

    return render(request, "index.html")