from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index),
    path('react_test/', react_test),
    path('login_api/', include('login_api.urls')),
    path('website_data/', include('Website_Data.urls')),
    path('venues/', include('venues.urls')),
    path('games/', include('games.urls')),
    path('players/', include('players.urls')),
    path('seasons/', include('seasons.urls')),
    path('gameresults/', include('gameresults.urls')),    
    path('tournaments/', include('tournaments.urls')),    
   # path('consolidated_data/',include('consolidated_data.urls'))
]
