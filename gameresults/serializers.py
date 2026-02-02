from rest_framework import serializers
from .models import *
from zoneinfo import ZoneInfo



class GameResultsSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source='player.player', read_only=True)
    registration_date_time_str = serializers.SerializerMethodField()
    other_evenets = serializers.SerializerMethodField()

    class Meta:
        model=GameResultModel
        fields='__all__'
    
    def get_other_evenets(self,obj):
        thisGame = obj.game.which_game.game
        theseEvents = [x.name for x in thisGame.all_sections.all()]
        return theseEvents
     
    def get_registration_date_time_str(self, obj):
        pacific_timezone = ZoneInfo('America/Los_Angeles')
        thisDate=obj.registration_date_time.astimezone(pacific_timezone)
        return thisDate.strftime('%m-%d-%Y  %H:%M')