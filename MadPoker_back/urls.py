from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index),
    path('react_test/', react_test),
    path('login_api/', include('login_api.urls'))
]
