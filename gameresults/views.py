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


class UpdateRosterAPI(APIView):

    def post(self, request, *args, **kwargs):

        problemPlayers=[]
        for onePlayer in request.data['allUsers']:           
            try:

                thisRecord= GameResultModel.objects.get(id=onePlayer['id'])
                if str(onePlayer['position']).isdigit():
                    thisRecord.position=onePlayer['position']
                else:
                    thisRecord.position=-1
                thisRecord.save()
            except:
                problemPlayers.append(onePlayer['name'])

        if problemPlayers==[]:
            return Response({'result':'OK'}, status=status.HTTP_200_OK)  
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
