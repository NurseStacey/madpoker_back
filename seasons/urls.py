from django.urls import path,include
from .views import *


urlpatterns = [
    path('seasons/', SeasonModelAPI.as_view(), name='seasons'),
    path('oneseason/<int:id>/', SeasonModelAPI.as_view(), name='seasons'),
]