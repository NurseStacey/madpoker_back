from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny
from rest_framework import status


class PlayersAPI(APIView):

    def get(self, request, *args, **kwargs):

        Games = PlayersModel.objects.all()
        serializer = PlayersSerializer(Games, many=True)
        return Response(serializer.data)