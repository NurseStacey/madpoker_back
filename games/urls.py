from django.urls import path,include
from .views import *


urlpatterns = [
    path('seasons/', SeasonModelAPI.as_view(), name='seasons'),
    path('oneseason/<int:id>/', SeasonModelAPI.as_view(), name='seasons'),
    path('games/', GameModelAPI.as_view(), name='games'),
    path('games_by_director/<int:id>/',GamesByDirectorAPI.as_view(), name='games_by_director'),
    path('onegame/<int:id>/', OneGameModelAPI.as_view(), name='one-game'),
    #path('games_for_player/', PlayedGamesAPI.as_view(), name='games-for-player'),    
    path('register_player_for_game/', GamesRegistrationsAPI.as_view(), name='games-for-player'),    
    path('register_new_player_for_game/', NewPlayerRegistrationAPI.as_view(), name='games-for-player'),    
    path('game_roster/<int:id>/', GameRostersAPI.as_view(), name='games-for-player'), 
    path('update_roster/',UpdateRosterAPI.as_view(), name='update_roster'),
    path('remove_layer_from_game/<int:id>/',GameResultsAPI.as_view(), name='remove_layer_from_game'),    
    path('events/',EventsAPI.as_view(), name='events'),        
    path('one_event/<int:id>/',EventsAPI.as_view(), name='one_event'),            
]