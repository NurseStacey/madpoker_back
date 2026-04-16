from rest_framework import serializers
from .models import *
from datetime import date

class TournamentRosterSerializer(serializers.ModelSerializer):
    player_name=serializers.SerializerMethodField()

    class Meta:
        model = TournamentPlayersModel
        fields =['player_name','position','id']
        
    def get_player_name(self, obj):
        return obj.player.player

class TournamentSerializer(serializers.ModelSerializer):

    class Meta:
        model = TournamentModel
        fields =['name','date', 'location','override_message','game_type','id','time']    

class TournamentSerializerForPlayerPage(serializers.ModelSerializer):

    display_text = serializers.SerializerMethodField()
    action = serializers.SerializerMethodField()

    class Meta:
        model = TournamentModel
        fields =['id','name', 'display_text','action']

    def get_action(self, obj):
        if obj.date>=date.today():
            return 'signup'
        if obj.finalized:
            return 'results'
        else:
            return 'noresults'

    def get_display_text(self, obj):

        if obj.date>=date.today():
            return obj.name + ' is to be held at ' + obj.location.venue_name + ' on ' + obj.date.strftime('%m/%d/%Y') + ' at ' + obj.time.strftime('%#I:%M')
        else:
            return obj.name + ' was held at ' + obj.location.venue_name + ' on ' + obj.date.strftime('%m/%d/%Y') 
