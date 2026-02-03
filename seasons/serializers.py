from .models import *
from rest_framework import serializers

class SeasonTypesSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = SeasonTypeModel
        fields ='__all__'    

class SeasonSerializer(serializers.ModelSerializer):
    seasonTypeText = serializers.CharField(source='season_type.season_type', read_only=True)    
    class Meta:
        model = SeasonModel
        fields ='__all__'    