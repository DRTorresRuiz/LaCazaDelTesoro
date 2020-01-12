from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.create, name="create"),
    url('^details/(?P<game_id>\d+)/$', views.details, name="details"),
    path('treasure/new/<int:id>/', views.treasure_create, name="treasure_create"),
    path('treasure/list', views.treasure_list, name="treasure_list"),
    url(r'treasure/list/(?P<game_id>[0-9]+)/$', views.treasure_list, name='treasure_list'),

]

