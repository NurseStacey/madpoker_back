from rest_framework import serializers
from gameresults.models import *
from .models import *
from zoneinfo import ZoneInfo
    
class GamesSerializer(serializers.ModelSerializer):
    game_text = serializers.SerializerMethodField()

    class Meta:
        model = GameModel
        fields ='__all__'

    def get_game_text(self,obj):
        return obj.GetText()

class GamesTypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameTypeModel
        fields ='__all__'

class PlayedGamesListSerializer(serializers.ModelSerializer):
    venue=serializers.CharField(source='which_game.venue.venue_name')
    season_name=serializers.CharField(source='season.season')
    game_type=serializers.CharField(source='which_game.game_type.name')
    week_day=serializers.CharField(source='which_game.week_day')

    class Meta:
        model=PlayedGameModel
        fields=['id', 'season_name', 'venue', 'date',  'game_type', 'week_day']

class PlayedGamesSerializer(serializers.ModelSerializer):

    PlayersArray = serializers.SerializerMethodField()
    OtherEvents = serializers.SerializerMethodField()
    
    class Meta:
        model = PlayedGameModel
        fields =['PlayersArray','OtherEvents' ]               

    def get_PlayersArray(self, obj):
        return obj.get_players()
    
    def get_OtherEvents(self,obj):
        return obj.get_other_events()
    
class CanceledGamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = CanceledGamesModel
        fields ='__all__'
    
# class SectionSerializer(serializers.ModelSerializer):

#     class Meta:
#         model=SectionModel
#         fields='__all__'

# class SectionThroughSerializerSimple(serializers.ModelSerializer):

#     class Meta:
#         model=SectionThrough
#         fields='__all__'

# class SectionThroughSerializer(serializers.ModelSerializer):
#     section_name = serializers.CharField(source='section.name', read_only=True)
#     director_name = serializers.CharField(default='', source='director.username', read_only=True)
#     venue_name = serializers.CharField(default='', source='game.venue.venue_name', read_only=True)
#     week_day = serializers.CharField(default='', source='game.week_day', read_only=True)
#     time = serializers.CharField(default='', source='game.time      ', read_only=True)
#     game_text=serializers.SerializerMethodField()
#     all_dates=serializers.SerializerMethodField()

#     class Meta:
#         model = SectionThrough
#         fields = ['game_text','time','section_name','week_day', 'director_name', 'active','id','venue_name', 'all_dates']        

#     def get_all_dates(self, obj):
#         return list({
#             'id':y.id,
#             'date':y.date.strftime('%m-%d-%Y'),
#             'canUpdate':not (y.finalized)
#             } for y in obj.played_games.all())
    
#     def get_game_text(self, obj):
#         venue_name = obj.game.venue.venue_name
#         week_day=obj.game.week_day
#         time=obj.game.time
#         event=obj.section.name

#         return venue_name + ' - ' + time + ' - ' + week_day + ' - ' + event
    
#     def get_director_name(self, obj):
#         try:
#             return obj.director.username
#         except:
#             return ''

# class SectionThroughForLocations(serializers.ModelSerializer):
#     venue = serializers.CharField(source='game.venue.venue_name', read_only=True)
    
#     class Meta:
#         model = SectionThrough
#         fields='__all__'
