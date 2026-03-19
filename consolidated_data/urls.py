from django.urls import path,include
from .views import *

urlpatterns = [
    path('info_for_search/', InfoForSearch.as_view(), name='info_for_search'),
    path('pull_data_for_points/<str:playeridstr>/<str:seasonidstr>/<str:venueidstr>/', PullDataForPoints.as_view(), name='info_for_search'),  
]