from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from login_api.models import UserModel
from .serializers import *
from rest_framework.permissions import AllowAny
from rest_framework import status
from players.serializers import PlayersSerializer
from django.db.models import ProtectedError

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

        print(id)
        thisGame = PlayedGameModel.objects.get(id=id)
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

        except Exception as e:
            if 'player' in newPlayerSerializer.errors:
                if 'unique' in [x.code for x in newPlayerSerializer.errors['player']]:
                    return Response({'status':'duplicit username'}, status=status.HTTP_409_CONFLICT)

            return Response({'status':'problem'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
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

class GamesByDirectorAPI(APIView):
    #used if we need the games assigned to one director
    def get(self, request, id,  *args, **kwargs):

    
        if id<0:
            return Response({'status':'error'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            Games = GameModel.objects.filter(director=UserModel.objects.get(id=id))
          
            serializer = GamesSerializer(Games, many=True)
           
        except Exception as e:
            print(e)
            return Response({'status':'error'}, status=status.HTTP_400_BAD_REQUEST)
        

        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
class GameModelAPI(APIView):
    #used for getting all games and creating/altering a game
    def get(self, request, *args, **kwargs):

        try:
            Games = GameModel.objects.all()
            serializer = GamesSerializer(Games, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request,*args, **kwargs):

        try:
            serializer = GamesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                temp=GameModel.objects.get(id=serializer.data['id'])

        except:
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        thisRecord=SectionThrough(
            section=SectionModel.objects.get(name='Texas Holdem'),
            game=GameModel.objects.get(id=serializer.data['id'])
        )
        thisRecord.save()
        try:
            thisDirector = UserModel.objects.get(id=request.data['director'])
            thisRecord.director=thisDirector
            thisRecord.save()
        except:
            pass
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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

        return Response({}, status=status.HTTP_200_OK)   
    
    

class OneGameModelAPI(APIView):
    #used when we need to get one game or alter a game.
    def get(self, request, id, *args, **kwargs):

        try:
            Games = GameModel.objects.get(id=id)
            serializer = GamesSerializer(Games)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'status':'Problem'}, status=status.HTTP_400_BAD_REQUEST)
    
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
        except ProtectedError:
            print('protected error')
            for oneSection in SectionThrough.objects.filter(game=thisRecord):
                if oneSection.need_to_protect():
                    return Response({'status':'protected'}, status=status.HTTP_403_FORBIDDEN)  
            
            try:
                for oneSection in SectionThrough.objects.filter(game=thisRecord):
                    for oneplayedgame in PlayedGameModel.objects.filter(which_game=oneSection):
                        oneplayedgame.delete()
                    oneSection.delete()
            
                thisRecord.delete() 
            except Exception as e:
                print('other protected error')
                print(e)
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:

            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({}, status=status.HTTP_200_OK)
    
    def patch(self, request,id,*args, **kwargs):
        print(request.data)
        try:
            thisRecord = GameModel.objects.get(id=id)
            serializer = GamesSerializer(thisRecord, data=request.data, partial=True)
            print(request.data)
            if serializer.is_valid():
                serializer.save()
                
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({}, status=status.HTTP_200_OK)   

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
        

class SectionsAPI(APIView):
    
    def get(self, request, *args, **kwargs):

        TextItems = SectionModel.objects.all().order_by('name')
        serializer = SectionSerializer(TextItems, many=True)
        return Response(serializer.data)
    
    def post(self, request,*args, **kwargs):
        #print(request.data)
        try:
            serializer = SectionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            try:
                if 'unique' in [x.code for x in SectionSerializer.errors['name']]:
                    return Response({'status':'duplicit event name'}, status=status.HTTP_409_CONFLICT)
            except:
                pass
        
            return Response({'status':'problem'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request,id,*args, **kwargs):
        
        try:
            thisRecord = SectionModel.objects.get(id=id)
            thisRecord.delete()
        except ProtectedError:
            return Response({}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({}, status=status.HTTP_200_OK)
    
    def patch(self, request,id,*args, **kwargs):

        try:
            thisRecord = SectionModel.objects.get(id=id)
            serializer = SectionSerializer(thisRecord, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({}, status=status.HTTP_200_OK)   
            

class SectionsThroughAPI(APIView):
    
    def get(self, request, *args, **kwargs):

        try:
            AllItems = SectionThrough.objects.all()
            #serializer = SectionThroughSerializer(AllItems, many=True)
            serializer = SectionThroughSerializerSimple(AllItems, many=True)
            #print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'status':'error'}, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request, *args, **kwargs):

        print(request.data)
        try:
            serializer = SectionThroughSerializerSimple(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)            
        except Exception as e:
            print(e)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request,id,*args, **kwargs):
        print('here')
        try:
            thisRecord = SectionThrough.objects.get(id=id)
            serializer = SectionThroughSerializerSimple(thisRecord, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({}, status=status.HTTP_200_OK)      
        