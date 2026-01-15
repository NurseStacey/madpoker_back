from rest_framework import serializers
from .models import *

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeasonsModel
        fields ='__all__'    

class GamesSerializer(serializers.ModelSerializer):
    Text = serializers.SerializerMethodField()

    class Meta:
        model = GamesModel
        fields ='__all__'    

    def get_Text(self,obj):
        return obj.GetText()
    
class GamesForPlayersSerializer(serializers.ModelSerializer):

    VenueName = serializers.SerializerMethodField()
    NextPlayerGameID = serializers.SerializerMethodField()

    class Meta:
        model = GamesModel
        fields =('id', 'VenueName', 'NextPlayerGameID','Description', 'Time', 'WeekDay') 

    def get_NextPlayerGameID(self, obj):
        return obj.GetNextGameID()

    def get_VenueName(self,obj):
        if obj.Venue==None:
            return ''
        else:
            return obj.Venue.VenueName 
    
class PlayedGamesSerializer(serializers.ModelSerializer):

    PlayersArray = serializers.SerializerMethodField()
    Text = serializers.SerializerMethodField()
    class Meta:
        model = PlayedGamesModel
        fields ='__all__'                

    def get_PlayersArray(self, obj):
        return obj.get_players()
    
    def get_Text(self, obj):

        return (obj.WhichGame.get_simple_text())