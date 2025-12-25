from django.urls import path,include
from .views import *


urlpatterns = [
    path('homepagetext', HomePageTextAPI.as_view(), name='home-page-text')
]