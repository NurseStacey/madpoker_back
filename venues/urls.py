from django.urls import path
from .views import *

urlpatterns = [
    path('venues/', VenuesAPI.as_view(), name='venues'),
    path('onevenue/<int:id>/', VenuesAPI.as_view(), name='one_venue'),    
]