"""laCazaDelTesoro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

# mysite/urls.py
from django.conf.urls import include

# from django.conf.urls.static import static
# from django.conf import settings

admin.autodiscover()

# Add patterns to access to your views
urlpatterns = [
    # path('game/', include('Game.urls', namespace="game"), name="game"),
    # path('Game/', include('Game.urls', namespace="Game"), name="Game"),
    path('', include('homepage.urls')),
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
     url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    path('admin/', admin.site.urls),
    path('registration/', include('registration.urls')),
    # path('game/', include('game.urls')),
    path('Game/', include('Game.urls')),
    # for chat
    path('chat/', include('chat.urls')),
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

'''
#Add URL maps to redirect the base URL to our application
from django.views.generic import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='homepage/', permanent=True)),
]
'''

# Use static() to add url mapping to serve static files during development (only)
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
