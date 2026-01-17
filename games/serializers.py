from rest_framework import serializers
from .models import *

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeasonModel
        fields ='__all__'    

class GamesSerializer(serializers.ModelSerializer):
    Text = serializers.SerializerMethodField()
    venue_name = serializers.SerializerMethodField()
    NextPlayerGameID = serializers.SerializerMethodField()

    class Meta:
        model = GameModel
        fields ='__all__'    

    def get_Text(self,obj):
        return obj.GetText()
    
    def get_NextPlayerGameID(self, obj):
        return obj.GetNextGameID()

    def get_venue_name(self,obj):
        if obj.venue==None:
            return ''
        else:
            return obj.venue.venue_name     
    
class GamesForPlayersSerializer(serializers.ModelSerializer):

    venue_name = serializers.SerializerMethodField()
    NextPlayerGameID = serializers.SerializerMethodField()

    class Meta:
        model = GameModel
        fields =('id', 'venue_name', 'NextPlayerGameID','description', 'time', 'week_day') 

    def get_NextPlayerGameID(self, obj):
        return obj.GetNextGameID()

    def get_venue_name(self,obj):
        if obj.venue==None:
            return ''
        else:
            return obj.venue.venue_name 
    
class PlayedGamesSerializer(serializers.ModelSerializer):

    PlayersArray = serializers.SerializerMethodField()
    ##Text = serializers.SerializerMethodField()
    class Meta:
        model = PlayedGameModel
        fields =['PlayersArray' ]               

    def get_PlayersArray(self, obj):
        return obj.get_players()
    
    # def get_Text(self, obj):

    #     return (obj.which_game.get_simple_text())