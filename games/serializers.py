from rest_framework import serializers
from .models import *

class GamesSerializer(serializers.ModelSerializer):
    Text = serializers.SerializerMethodField()

    class Meta:
        model = GamesModel
        fields ='__all__'    

    def get_Text(self,obj):
        return obj.GetText()
    
class GamesFOrPlayersSerializer(serializers.ModelSerializer):

    VenueName = serializers.SerializerMethodField()

    class Meta:
        model = GamesModel
        fields =('id', 'VenueName', 'Description', 'Time', 'WeekDay') 

    def get_VenueName(self,obj):
        if obj.Venue==None:
            return ''
        else:
            return obj.Venue.VenueName 
    
class PlayedGamessSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlayedGamesModel
        fields ='__all__'                