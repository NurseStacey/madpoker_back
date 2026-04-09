from rest_framework import serializers
from .models import *


class TournamentSerializer(serializers.ModelSerializer):

    class Meta:
        model = TournamentModel
        fields =['name','date', 'location','override_message','game_type','id']    