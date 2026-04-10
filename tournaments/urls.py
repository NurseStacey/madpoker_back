from django.urls import path,include
from .views import *

urlpatterns = [
    path('tournament/', TournamentAPI.as_view(), name='tournament'),    
    path('onetournament/<int:id>/', OneTournamentAPI.as_view(), name='onetournament'),    
    path('info_for_tournament/',InfoForTournaments, name='info_for_tournament'),   
    path('info_for_tournament_player_page/',TournamentInfoForPlayerPage.as_view(), name='info_for_tournament_player_page'),  
]