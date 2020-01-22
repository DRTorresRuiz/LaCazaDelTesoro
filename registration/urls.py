from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('logout/', views.logout, name='logout'),
]
