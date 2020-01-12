from django.shortcuts import render

from Game.models import Game

# Create your views here.

#from catalog.models import Book, Author, BookInstance, Genre

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = 1
    num_instances = 2
    
    # Available books (status = 'a')
    num_instances_available = 3
    
    # The 'all()' is implied by default.    
    num_authors = 4

    games = Game.objects.all()
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
	'games': games
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index_homepage.html', context=context)
