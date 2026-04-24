from django.urls import path,include
from .views import *


urlpatterns = [
    path('players/', PlayersAPI.as_view(), name='players'),
    path('winners/', WinnersAPI.as_view(), name='winners'),
]