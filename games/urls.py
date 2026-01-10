from django.urls import path,include
from .views import *


urlpatterns = [
    path('games/', GamesModelAPI.as_view(), name='games'),
    path('onegame/<int:id>/', OneGamesModelAPI.as_view(), name='one-game'),
    path('games_for_player/', GamesForPlayersAPI.as_view(), name='games-for-player'),    
]