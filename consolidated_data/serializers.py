from rest_framework import serializers
from gameresults.models import GameResultModel

class PullDataForPointsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = GameResultModel
        fields ='__all__'        