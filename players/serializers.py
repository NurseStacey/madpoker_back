from rest_framework import serializers
from .models import *

class PlayersSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlayerModel
        fields ='__all__'    

class WinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WinnersModel
        fields='__all__'