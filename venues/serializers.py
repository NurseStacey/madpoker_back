from rest_framework import serializers
from .models import *

class VenuesSerializer(serializers.ModelSerializer):    
    class Meta:
        model = VenueModel
        fields ='__all__'    