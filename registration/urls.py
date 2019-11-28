from django.urls import path, include

#from django.contrib.auth import logout 
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('oauth/', include('social_django.urls', namespace='social')),
   #path('login/', auth.login, name='login'),
   path('logout/', views.logout, name='logout'),
]
