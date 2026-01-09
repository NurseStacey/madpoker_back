from django.urls import path,include
from .views import *


urlpatterns = [
    path('games/', GamesModelAPI.as_view(), name='games'),
    path('onegame/<int:id>/', GamesModelAPI.as_view(), name='one-game'),
]