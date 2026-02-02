from django.urls import path,include
from .views import *


urlpatterns = [ 
    path('game_roster/<int:id>/', GameRostersAPI.as_view(), name='games-for-player'),   
    path('update_roster/',UpdateRosterAPI.as_view(), name='update_roster'),
    path('remove_player_from_game/<int:id>/',GameResultsAPI.as_view(), name='remove_layer_from_game'),
    path('register_player_for_game/', GamesRegistrationsAPI.as_view(), name='games-for-player'),               
]

