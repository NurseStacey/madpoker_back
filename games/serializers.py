from rest_framework import serializers
from .models import *

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeasonModel
        fields ='__all__'    

# class CustomForiegnField(serializers.):
#     def to_representation(self, value):
        
#         if value is None:
#             return -1  # Change null output to 0
#         return super().to_representation(value)
    
class GamesSerializer(serializers.ModelSerializer):
    Text = serializers.SerializerMethodField()
    #director=CustomForiegnField(allow_null=True)
    #venue_name = serializers.SerializerMethodField()
    #NextPlayerGameID = serializers.SerializerMethodField()
    #Dates = serializers.SerializerMethodField()

    class Meta:
        model = GameModel
        fields ='__all__'    


    # def get_Dates(self, obj):
    #     return obj.get_dates()
    
    def get_Text(self,obj):
        return obj.GetText()
    
    # def get_NextPlayerGameID(self, obj):
    #     return obj.GetNextGameID()

    # def get_venue_name(self,obj):
    #     if obj.venue==None:
    #         return ''
    #     else:
    #         return obj.venue.venue_name     
    
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
    
class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model=SectionModel
        fields='__all__'

class SectionThroughSerializerSimple(serializers.ModelSerializer):

    class Meta:
        model=SectionThrough
        fields='__all__'

class SectionThroughSerializer(serializers.ModelSerializer):
    section_name = serializers.CharField(source='section.name', read_only=True)
    director_name = serializers.CharField(default='', source='director.username', read_only=True)
    #director_name = serializers.SerializerMethodField()
    game_text=serializers.SerializerMethodField()

    class Meta:
        model = SectionThrough
        fields = ['section_name','game_text', 'director_name', 'active','id']        

    def get_game_text(self, obj):
        return obj.game.GetText()
    
    def get_director_name(self, obj):
        try:
            return obj.director.username
        except:
            return ''
# class GameSerializerNew(serializers.ModelSerializer):

#     venue_name = serializers.CharField(source='venue.venue_name', read_only=True)
#     events = EventThroughSerializer(source='EventThrough', many=True, read_only=True)

#     class Meta:
#         model = GameModel
#         fields = ['week_day', 'time','venue_name','description','events'],