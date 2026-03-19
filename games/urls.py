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
    path('test/',CreateTestingData)
    # path('games_by_director/<int:id>/',GamesByDirectorAPI.as_view(), name='games_by_director'),
    # 
    # 
    # path('sections/',SectionsAPI.as_view(), name='sections'), 
    # path('get_all_sections/', AllSectionsAPI.as_view(), name='sections'),
    # path('one_section/<int:id>/',SectionsAPI.as_view(), name='one_event'),
    # path('sectionthrough/',SectionsThroughAPI.as_view(), name='section_through'),
    # path('one_sectionthrough/<int:id>/',SectionsThroughAPI.as_view(), name='one_section_through'),
    # path('info_for_locations_page/',InfoForLocations, name='info_for_locations_page'),
    # path('get_all_info_for_game_view/',GetAllGamesInfoGameView.as_view(), name='get_all_info_for_game_view'),
    # path('get_this_player_results/<int:id>/',GetThisPlayerResults.as_view(), name='get_this_player_results'),    
]