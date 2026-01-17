from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny
from rest_framework import status


class PlayersAPI(APIView):

    def get(self, request, *args, **kwargs):

        Games = PlayerModel.objects.all()
        serializer = PlayersSerializer(Games, many=True)
        return Response(serializer.data)
    
    def post(self, request,*args, **kwargs):

        try:

            serializer = PlayersSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print(serializer.error_messages)
        except Exception as e:
            print(e)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error':'invalid data'}, status=status.HTTP_400_BAD_REQUEST)