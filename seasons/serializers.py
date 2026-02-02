from .models import *
from rest_framework import serializers

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeasonModel
        fields ='__all__'    