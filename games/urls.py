from django.urls import path,include
from .views import *


urlpatterns = [
    path('games/', GamesModelAPI.as_view(), name='games'),
    path('seasons/', SeasonsModelAPI.as_view(), name='seasons'),
    path('oneseason/<int:id>/', SeasonsModelAPI.as_view(), name='seasons'),
    path('onegame/<int:id>/', OneGamesModelAPI.as_view(), name='one-game'),
    path('games_for_player/', PlayedGamesAPI.as_view(), name='games-for-player'),    
    path('register_player_for_game/', GamesForPlayersAPI.as_view(), name='games-for-player'),    
]