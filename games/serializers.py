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
    Dates = serializers.SerializerMethodField()

    class Meta:
        model = GameModel
        fields ='__all__'    

    def get_Dates(self, obj):
        return obj.get_dates()
    
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
    
# class SectionSerializer(serializers.ModelSerializer):

#     class Meta:
#         model=SeasonModel
#         fields='__all__'

# class EventThroughSerializer(serializers.ModelSerializer):
#     event_name = serializers.CharField(source='event.name', read_only=True)

#     class Meta:
#         model = EventThrough
#         fields = ['event_name', 'director', 'active']        

# class GameSerializerNew(serializers.ModelSerializer):

#     venue_name = serializers.CharField(source='venue.venue_name', read_only=True)
#     events = EventThroughSerializer(source='EventThrough', many=True, read_only=True)

#     class Meta:
#         model = GameModel
#         fields = ['week_day', 'time','venue_name','description','events'],