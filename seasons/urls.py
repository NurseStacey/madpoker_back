from django.urls import path,include
from .views import *


urlpatterns = [
    path('seasons/', SeasonModelAPI.as_view(), name='seasontypes'),
    path('oneseason/<int:id>/', SeasonModelAPI.as_view(), name='oneseasons'),
    path('seasontypes/', SeasonTypeModelAPI.as_view(), name='seasons'),
]