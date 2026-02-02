from django.urls import path,include
from .views import *


urlpatterns = [
    path('games/', GameModelAPI.as_view(), name='games'),
    path('games_by_director/<int:id>/',GamesByDirectorAPI.as_view(), name='games_by_director'),
    path('onegame/<int:id>/', OneGameModelAPI.as_view(), name='one-game'),
    path('played_games_events/<int:id>/', PlayedGamesEvents.as_view(), name='events-for-player'),
    path('sections/',SectionsAPI.as_view(), name='sections'), 
    path('get_all_sections/', AllSectionsAPI.as_view(), name='sections'),
    path('one_section/<int:id>/',SectionsAPI.as_view(), name='one_event'),
    path('sectionthrough/',SectionsThroughAPI.as_view(), name='section_through'),
    path('one_sectionthrough/<int:id>/',SectionsThroughAPI.as_view(), name='one_section_through'),
    path('info_for_locations_page/',InfoForLocations, name='info_for_locations_page')
]