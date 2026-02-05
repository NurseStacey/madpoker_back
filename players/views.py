from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.db.utils import IntegrityError

class PlayersAPI(APIView):

    def get(self, request, *args, **kwargs):

        Games = PlayerModel.objects.exclude(player='this is not a player')
        serializer = PlayersSerializer(Games, many=True)
        return Response(serializer.data)
    
    def post(self, request,*args, **kwargs):
        try:

            serializer = PlayersSerializer(data=request.data)

            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except IntegrityError:
            print('here')
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            print(serializer.errors)
            if 'player' in serializer.errors:
                if 'unique' in [x.code for x in serializer.errors['player']]:
                    return Response({'status':'duplicit username'}, status=status.HTTP_409_CONFLICT)
            print(e)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error':'invalid data'}, status=status.HTTP_400_BAD_REQUEST)