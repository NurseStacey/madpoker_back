from django.urls import path,include
from .views import *

urlpatterns = [
    path('tournament/', TournamentAPI.as_view(), name='tournament'),    
    path('onetournament/<int:id>/', OneTournamentAPI.as_view(), name='onetournament'),    
    path('info_for_tournament/',InfoForTournaments, name='info_for_tournament'),   
    path('info_for_tournament_player_page/',TournamentInfoForPlayerPage.as_view(), name='info_for_tournament_player_page'),  
    path('register_player_for_tournament/',RegisterForTournament.as_view(), name='register_player_for_tournament'),  
    path('this_roster/<int:id>/',TournamentRoster.as_view(), name='this_roster'),      
    path('remove_player_from_tournament/<int:id>/',TournamentRosterRemovePlayer.as_view(), name='remove_player_from_tournament'),      
    path('update_roster/',TournamentRosterUpdate.as_view(), name='update_roster'),          
    path('finalize_roster/<int:id>/',TournamentRosterFinalize.as_view(), name='finalize_roster'),        
]