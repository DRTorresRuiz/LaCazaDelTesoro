from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.create, name="create"),
    path('view/', views.view, name="view"),
    path('treasure/', views.treasure_list, name="treasure_list"),
    path('treasure/new/<int:id>/', views.treasure_create, name="treasure_create"),
]

