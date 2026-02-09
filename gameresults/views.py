from django.shortcuts import render
from rest_framework import status
from players.models import PlayerModel
from games.models import PlayedGameModel
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
       
class GameResultsAPI(APIView):
    #only used for removing a player from the roster
    def delete(self, request, id, *args, **kwargs):

        try:
            thisRecord = GameResultModel.objects.get(id=id)
            thisRecord.delete()
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({}, status=status.HTTP_200_OK)
       
class GameRostersAPI(APIView):
#used to get roster for  director
    def get(self, request, id, *args, **kwargs):


        try:
            thisGame = PlayedGameModel.objects.get(id=id)
            serializer = GameResultsSerializer(GameResultModel.objects.filter(game=thisGame), many=True)

            return Response(serializer.data,)
        
        except Exception as e:
            print(e)
            return Response({'status':'problem'}, status=status.HTTP_400_BAD_REQUEST)

class UpdateRosterOnlyPositionAPI(APIView):

    def post(self, request, *args, **kwargs):

        def calculate_points(position):
            if position<10:
                return 2*(number_of_players-position+1)
            else:
                return number_of_players-position+1            
            
        problemPlayers=[]
        number_of_players = len(request.data['allUsers'])
        which_game=-1
        for onePlayer in request.data['allUsers']:           
            try:

                thisRecord= GameResultModel.objects.get(id=onePlayer['id'])
                if str(onePlayer['position']).isdigit():
                    which_game=thisRecord.game.id
                    thisPosition=int(onePlayer['position'])

                    if thisPosition>0 and not thisPosition==thisRecord.position:
                        thisRecord.position=thisPosition
                        thisRecord.points=calculate_points(thisPosition)
                        thisRecord.save()            
            except:
                problemPlayers.append(onePlayer['name'])

        if problemPlayers==[] and not which_game==-1:
            thisGame = PlayedGameModel.objects.get(id=which_game)
            serializer = GameResultsSerializer(GameResultModel.objects.filter(game=thisGame), many=True)            
            return Response(serializer.data, status=status.HTTP_200_OK)  
        else: 
            return Response({
                'result':'problem',
                'problem_players':problemPlayers
                }, status=status.HTTP_400_BAD_REQUEST)
        
class UpdateRosterAPI(APIView):

    def post(self, request, *args, **kwargs):

        def calculate_points(position):
            if position<10:
                return 2*(number_of_players-position+1)
            else:
                return number_of_players-position+1            
            
        problemPlayers=[]
        number_of_players = len(request.data['allUsers'])
        which_game=-1
        for onePlayer in request.data['allUsers']:           
            try:

                thisRecord= GameResultModel.objects.get(id=onePlayer['id'])
                if str(onePlayer['position']).isdigit():
                    which_game=thisRecord.game.id
                    thisPosition=int(onePlayer['position'])

                    if thisPosition>0 and not thisPosition==thisRecord.position:
                        thisRecord.position=thisPosition
                        thisPoints=0
                        if str(onePlayer['points']).isdigit():
                            thisPoints = int(onePlayer['points'])
                            if thisPoints<1:
                                thisPoints=calculate_points(thisPosition)
                        else:
                            thisPoints=calculate_points(thisPosition)
                            
                        thisRecord.points=thisPoints
                        thisRecord.save()
                elif str(onePlayer['points']).isdigit():
                    thisPoints = int(onePlayer['points'])
                    if thisPoints>0 and not thisPoints==thisRecord.points:
                        thisRecord.points=thisPoints
                        thisRecord.save()
                
            except:
                problemPlayers.append(onePlayer['name'])

        if problemPlayers==[] and not which_game==-1:
            thisGame = PlayedGameModel.objects.get(id=which_game)
            serializer = GameResultsSerializer(GameResultModel.objects.filter(game=thisGame), many=True)            
            return Response(serializer.data, status=status.HTTP_200_OK)  
        else: 
            return Response({
                'result':'problem',
                'problem_players':problemPlayers
                }, status=status.HTTP_400_BAD_REQUEST)
        
  
# def RegisterForGame(PlayerID, GameID):
#     try:

#         thisRecord = PlayedGameModel.objects.get(id=GameID)
#         thisPlayer = PlayerModel.objects.get(id=PlayerID)
#         try:
#             thisRecord.player_results.get(player=thisPlayer)
#             return Response({'status':'player already registered'}, status=status.HTTP_201_CREATED)
#         except Exception as e:

#             new_player_result = GameResultModel(player=thisPlayer)
#             new_player_result.save()
#             thisRecord.player_results.add(new_player_result)

#             return Response({'status':'player added'}, status=status.HTTP_201_CREATED)
#     except Exception as e:
#         print(e)
        
#         return Response({'status':'problem'}, status=status.HTTP_400_BAD_REQUEST) 
    
    
class GamesRegistrationsAPI(APIView):
#used for registering for a game
    def post(self, request,*args, **kwargs):

        try:
            if PlayedGameModel.objects.get(id=request.data['which_game']).finalized:
                return Response({'status':'duplicate'}, status=status.HTTP_423_LOCKED) 
            
            GameResultModel.objects.create(
                player=PlayerModel.objects.get(id=request.data['which_player']),
                game=PlayedGameModel.objects.get(id=request.data['which_game'])
            )
           
        except Exception as e:
            if 'UNIQUE' in e.args[0]:
                return Response({'status':'duplicate'}, status=status.HTTP_409_CONFLICT)    
            print(e)
            return Response({'status':'problem'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status':'player added'}, status=status.HTTP_201_CREATED)
