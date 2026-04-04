from django.urls import path,include
from .views import *
from .testing import *

urlpatterns = [
    path('basic_games/', GameModelAPI.as_view(), name='basic_games'),
    path('onegame/<int:id>/', OneGameModelAPI.as_view(), name='one-game'),
    path('info_for_locations_page/',InfoForLocations, name='info_for_locations_page'),
    path('get_game_types/',GameTypeView.as_view() , name='get_game_types'),
    path('one_game_type/<int:id>/',GameTypeView.as_view() , name='one_game_types'),
    path('games_for_roster/',GamesForRostersView.as_view() , name='games_for_roster'),
    path('played_games_events/<int:id>/', PlayedGamesEvents.as_view(), name='events-for-player'),
    path('gameinfo_for_review/', GameInfoForReview.as_view(), name='gameinfo-for-review'),
    path('played_game_list/<str:seasonidstr>/<str:venueidstr>/',PlayedGamesList.as_view(), name='played_game_list'), 
    path('canceled_game_list/',GetCanceledGames.as_view(), name='canceled_game_list'), 
    path('uncancel_game/<int:id>/',UnCancelGame.as_view(), name='uncancel_game'),     
    path('test/',CreateTestingData),
    path('print_test_file/', PrintTestFile)
]