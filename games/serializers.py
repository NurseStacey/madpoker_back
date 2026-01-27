from rest_framework import serializers
from .models import *
from zoneinfo import ZoneInfo

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
    
# class GamesForPlayersSerializer(serializers.ModelSerializer):

#     venue_name = serializers.SerializerMethodField()
#     NextPlayerGameID = serializers.SerializerMethodField()

#     class Meta:
#         model = GameModel
#         fields =('id', 'venue_name', 'NextPlayerGameID','description', 'time', 'week_day') 

#     def get_NextPlayerGameID(self, obj):
#         return obj.GetNextGameID()

#     def get_venue_name(self,obj):
#         if obj.venue==None:
#             return ''
#         else:
#             return obj.venue.venue_name 
    
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
    venue_name = serializers.CharField(default='', source='game.venue.venue_name', read_only=True)
    week_day = serializers.CharField(default='', source='game.week_day', read_only=True)
    time = serializers.CharField(default='', source='game.time      ', read_only=True)
    game_text=serializers.SerializerMethodField()
    all_dates=serializers.SerializerMethodField()

    class Meta:
        model = SectionThrough
        fields = ['game_text','time','section_name','week_day', 'director_name', 'active','id','venue_name', 'all_dates']        

    def get_all_dates(self, obj):
        return list({'id':y.id,'date':y.date.strftime('%m-%d-%Y')} for y in obj.played_games.all())
    
    def get_game_text(self, obj):
        venue_name = obj.game.venue.venue_name
        week_day=obj.game.week_day
        time=obj.game.time
        event=obj.section.name

        return venue_name + ' - ' + time + ' - ' + week_day + ' - ' + event
    
    def get_director_name(self, obj):
        try:
            return obj.director.username
        except:
            return ''

class SectionThroughForLocations(serializers.ModelSerializer):
    venue = serializers.CharField(source='game.venue.venue_name', read_only=True)
    
    class Meta:
        model = SectionThrough
        fields='__all__'

class GameResultsSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source='player.player', read_only=True)
    registration_date_time_str = serializers.SerializerMethodField()

    class Meta:
        model=GameResultModel
        fields='__all__'
    
    def get_registration_date_time_str(self, obj):
        pacific_timezone = ZoneInfo('America/Los_Angeles')
        thisDate=obj.registration_date_time.astimezone(pacific_timezone)
        return thisDate.strftime('%m-%d-%Y  %H:%M')