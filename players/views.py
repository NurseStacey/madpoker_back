from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status
from django.db.utils import IntegrityError

class WinnersAPI(APIView):

    def get(self, request, *args, **kwargs):

        try:
            Winners = WinnersModel.objects.all()
            serializer = WinnerSerializer(Winners, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)    
        
    def post(self, request,*args, **kwargs):
        try:

            serializer = WinnerSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlayersAPI(APIView):

    def get(self, request, *args, **kwargs):

        try:
            Players = PlayerModel.objects.exclude(player='this is not a player')
            serializer = PlayersSerializer(Players, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)    
        
    def post(self, request,*args, **kwargs):
        try:

            serializer = PlayersSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
            else:
                if 'player' in serializer.errors:
                    for one_error in serializer.errors['player']:
                        if one_error.code=='unique':
                            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
                        
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except IntegrityError:
            #print('here')
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            print(serializer.errors)
            if 'player' in serializer.errors:
                if 'unique' in [x.code for x in serializer.errors['player']]:
                    return Response({'status':'duplicit username'}, status=status.HTTP_409_CONFLICT)
            print(e)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

