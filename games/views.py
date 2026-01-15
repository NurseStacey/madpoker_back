from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from login_api.models import UserModel
from .serializers import *
from rest_framework.permissions import AllowAny
from rest_framework import status
from players.serializers import PlayersSerializer

class GameRostersAPI(APIView):

    def get(self, request, id, *args, **kwargs):

        thisGame = PlayedGamesModel.objects.filter(WhichGame=GamesModel.objects.get(id=id)).latest('Date')
        serializer = PlayedGamesSerializer(thisGame, many=False)
        return Response(serializer.data)

class NewPlayerGameSignupPlayersAPI(APIView):

    def post(self, request,*args, **kwargs):

        try:
            newPlayerSerializer = PlayersSerializer(data=request.data['new_player'])
            if newPlayerSerializer.is_valid():
                newPlayerSerializer.save()    

            print(newPlayerSerializer.data['id'])        
            thisRecord = PlayedGamesModel.objects.get(id=request.data['WhichGame'])
            thisPlayer = PlayersModel.objects.get(id=newPlayerSerializer.data['id'])
            if thisPlayer not in thisRecord.Players.all():
                thisRecord.Players.add(thisPlayer)

                return Response({'status':'player added'}, status=status.HTTP_201_CREATED)
        except:
            
            return Response({'status':'problem'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'status':'player was already registered'}, status=status.HTTP_200_OK)
    
class GamesForPlayersAPI(APIView):

    def post(self, request,*args, **kwargs):

        try:
            thisRecord = PlayedGamesModel.objects.get(id=request.data['WhichGame'])
            thisPlayer = PlayersModel.objects.get(id=request.data['WhichPlayer'])
            if thisPlayer not in thisRecord.Players.all():
                thisRecord.Players.add(thisPlayer)

                return Response({'status':'player added'}, status=status.HTTP_201_CREATED)
        except:
            
            return Response({'status':'problem'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'status':'player was already registered'}, status=status.HTTP_200_OK)


class GamesByDirectorAPI(APIView):

    def get(self, request, id,  *args, **kwargs):
        Games = GamesModel.objects.filter(Director=UserModel.objects.get(id=id))
        serializer = GamesSerializer(Games, many=True)
        return Response(serializer.data)
        
class GamesModelAPI(APIView):
    
    def get(self, request, *args, **kwargs):

        Games = GamesModel.objects.all()
        serializer = GamesSerializer(Games, many=True)
        return Response(serializer.data)
    
    def post(self, request,*args, **kwargs):

        try:
            serializer = GamesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #
        #print(serializer.errors)
        return Response({'error':'invalid data'}, status=status.HTTP_400_BAD_REQUEST)

class SeasonsModelAPI(APIView):
    
    def get(self, request, *args, **kwargs):

        Seasons = SeasonsModel.objects.all()
        serializer = SeasonSerializer(Seasons, many=True)

        return Response(serializer.data)
    
    def post(self, request,*args, **kwargs):

        try:
            serializer = SeasonSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #
        #print(serializer.errors)
        return Response({'error':'invalid data'}, status=status.HTTP_400_BAD_REQUEST)
            
    def patch(self, request,id,*args, **kwargs):
        try:

            thisRecord = SeasonsModel.objects.get(id=id)
            serializer = SeasonSerializer(thisRecord, data=request.data, partial=True)
            if serializer.is_valid():

                serializer.save()

                
        except Exception as e:
            print(e)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        print('here')
        return Response({}, status=status.HTTP_200_OK)   
    
    

class OneGamesModelAPI(APIView):
    
    def get(self, request, id, *args, **kwargs):

        Games = GamesModel.objects.get(id=id)
        serializer = GamesSerializer(Games)
        return Response(serializer.data)
    
    def post(self, request,*args, **kwargs):

        try:
            serializer = GamesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #
        #print(serializer.errors)
        return Response({'error':'invalid data'}, status=status.HTTP_400_BAD_REQUEST)

        
    
    def delete(self, request,id,*args, **kwargs):

        try:
            thisRecord = GamesModel.objects.get(id=id)
            thisRecord.delete()
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({}, status=status.HTTP_200_OK)
    
    def patch(self, request,id,*args, **kwargs):
        try:
            thisRecord = GamesModel.objects.get(id=id)
            serializer = GamesSerializer(thisRecord, data=request.data, partial=True)
            print(request.data)
            if serializer.is_valid():
                serializer.save()
                
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({}, status=status.HTTP_200_OK)   

class PlayedGamesAPI(APIView):

    def get(self, request, *args, **kwargs):

        Games = GamesModel.objects.all()
        serializer = GamesForPlayersSerializer(Games, many=True)
        return Response(serializer.data)