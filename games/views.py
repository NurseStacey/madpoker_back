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
#used to get roster for  director
    def get(self, request, id, *args, **kwargs):

        thisGame = PlayedGameModel.objects.filter(which_game=GameModel.objects.get(id=id)).latest('date')
        serializer = PlayedGamesSerializer(thisGame, many=False)
        return Response(serializer.data)

class NewPlayerRegistrationAPI(APIView):
#used for registering a new player and signing up for game
    def post(self, request,*args, **kwargs):
        
        try:
            newPlayerSerializer = PlayersSerializer(data=request.data['new_player'])
            if newPlayerSerializer.is_valid():
                newPlayerSerializer.save()    
            
            return RegisterForGame(newPlayerSerializer.data['id'],request.data['which_game'])
            # thisRecord = PlayedGameModel.objects.get(id=request.data['which_game'])

            # thisPlayer = PlayerModel.objects.get(id=newPlayerSerializer.data['id'])

            # if thisPlayer not in thisRecord.players.all():
            #     thisRecord.players.add(thisPlayer)

            #     return Response({'status':'player added'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            
            return Response({'status':'problem'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'status':'player was already registered'}, status=status.HTTP_200_OK)

def RegisterForGame(PlayerID, GameID):
    try:

        thisRecord = PlayedGameModel.objects.get(id=GameID)
        thisPlayer = PlayerModel.objects.get(id=PlayerID)
        try:
            thisRecord.player_results.get(player=thisPlayer)
            return Response({'status':'player already registered'}, status=status.HTTP_201_CREATED)
        except Exception as e:

            new_player_result = GameResultModel(player=thisPlayer)
            new_player_result.save()
            thisRecord.player_results.add(new_player_result)

            return Response({'status':'player added'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        
        return Response({'status':'problem'}, status=status.HTTP_400_BAD_REQUEST)
        
class GamesRegistrationsAPI(APIView):
#used for registering for a game
    def post(self, request,*args, **kwargs):
        return RegisterForGame(request.data['WhichPlayer'],request.data['which_game'])

        # try:
        #     thisRecord = PlayedGameModel.objects.get(id=request.data['which_game'])
        #     thisPlayer = PlayerModel.objects.get(id=request.data['WhichPlayer'])
        #     if thisPlayer not in thisRecord.players.all():
        #         thisRecord.players.add(thisPlayer)

        #         return Response({'status':'player added'}, status=status.HTTP_201_CREATED)
        # except:
            
        #     return Response({'status':'problem'}, status=status.HTTP_400_BAD_REQUEST)
        
        # return Response({'status':'player was already registered'}, status=status.HTTP_200_OK)


class GamesByDirectorAPI(APIView):
    #used if we need the games assigned to one director
    def get(self, request, id,  *args, **kwargs):
        Games = GameModel.objects.filter(director=UserModel.objects.get(id=id))
        serializer = GamesSerializer(Games, many=True)
        return Response(serializer.data)
        
class GameModelAPI(APIView):
    #used for getting all games and creating/altering a game
    def get(self, request, *args, **kwargs):

        Games = GameModel.objects.all()
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

        return Response({'error':'invalid data'}, status=status.HTTP_400_BAD_REQUEST)

class SeasonModelAPI(APIView):
    #For seasons
    def get(self, request, *args, **kwargs):

        Seasons = SeasonModel.objects.all()
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

            thisRecord = SeasonModel.objects.get(id=id)
            serializer = SeasonSerializer(thisRecord, data=request.data, partial=True)
            if serializer.is_valid():

                serializer.save()

                
        except Exception as e:
            print(e)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        print('here')
        return Response({}, status=status.HTTP_200_OK)   
    
    

class OneGameModelAPI(APIView):
    #used when we need to get one game or alter a game.
    def get(self, request, id, *args, **kwargs):

        Games = GameModel.objects.get(id=id)
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
            thisRecord = GameModel.objects.get(id=id)
            thisRecord.delete()
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({}, status=status.HTTP_200_OK)
    
    def patch(self, request,id,*args, **kwargs):
        try:
            thisRecord = GameModel.objects.get(id=id)
            serializer = GamesSerializer(thisRecord, data=request.data, partial=True)
            print(request.data)
            if serializer.is_valid():
                serializer.save()
                
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({}, status=status.HTTP_200_OK)   

# class PlayedGamesAPI(APIView):

#     def get(self, request, *args, **kwargs):

#         Games = GameModel.objects.all()
#         serializer = GamesForPlayersSerializer(Games, many=True)
#         return Response(serializer.data)