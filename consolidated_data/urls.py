from django.urls import path,include
from .views import *

urlpatterns = [
    path('info_for_search/', InfoForSearch.as_view(), name='info_for_search'),   
]