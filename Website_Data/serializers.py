from rest_framework import serializers
from .models import *

class HomePageTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePageText
        fields ='__all__'    