from rest_framework import serializers
from .models import *

class VenuesSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    
    class Meta:
        model = VenueModel
        fields =('venue_name','image', 'active')