from rest_framework import serializers
from .models import *

class GamesSerializer(serializers.ModelSerializer):
    Text = serializers.SerializerMethodField()

    class Meta:
        model = GamesModel
        fields ='__all__'    

    def get_Text(self,obj):
        return obj.GetText()