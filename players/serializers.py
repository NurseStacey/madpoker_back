from rest_framework import serializers
from .models import *

class PlayersSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlayersModel
        fields ='__all__'    

