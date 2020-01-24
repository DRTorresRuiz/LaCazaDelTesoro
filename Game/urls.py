from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.create, name="create"),
    url('^details/(?P<game_id>\d+)/$', views.details, name="details"),
    url('^join/(?P<game_id>\d+)/$', views.join, name="join"),
    url('^leave/(?P<game_id>\d+)/$', views.leave, name='leave'),
    url('^play/(?P<game_id>\d+)/$', views.play, name="play"),
    path('treasure/new/<int:id>/', views.treasure_create, name="treasure_create"),
    path('treasure/list', views.treasure_list, name="treasure_list"),
    url(r'treasure/list/(?P<game_id>[0-9]+)/$', views.treasure_list, name='treasure_list'),
    url('^found/(?P<treasure_id>\d+)/$', views.found, name="found"),
]

