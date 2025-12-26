from django.urls import path,include
from .views import *


urlpatterns = [
    path('homepagetext/', HomePageTextAPI.as_view(), name='home-page-text'),
    path('homepagetext/<int:id>/', HomePageTextAPI.as_view(), name='home-page-text-record'),
    path('specialmessages/', SpecialMessageAPI.as_view(), name='special-messages-text'),
    path('specialmessages/<int:id>/', SpecialMessageAPI.as_view(), name='special-messages-text-record')
]