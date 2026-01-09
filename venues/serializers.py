from rest_framework import serializers
from .models import *

class VenuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VenuesModel
        fields ='__all__'    