from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from login_api.models import UserModel
from .serializers import *
from rest_framework import status
from players.serializers import PlayersSerializer
from gameresults.models import GameResultModel
from players.models import PlayerModel
from django.db.models import ProtectedError
from django.http import JsonResponse
from django.db.models import F
from datetime import date, timedelta
import calendar

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
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
    
    def delete(self, request,id,*args, **kwargs):

        try:
            thisRecord = GameModel.objects.get(id=id)
            thisRecord.delete()
        except ProtectedError:
            pass
            if PlayedGameModel.objects.filter(which_game=thisRecord).filter(finalized=True).count()>0:
                return Response({}, status=status.HTTP_403_FORBIDDEN)
            else:
                PlayedGameModel.objects.filter(which_game=thisRecord).delete()
                thisRecord.delete()

        except Exception as e:

            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({}, status=status.HTTP_200_OK)
    
    def patch(self, request,id,*args, **kwargs):
        print("patch")
        try:
            thisRecord = GameModel.objects.get(id=id)
            serializer = GamesSerializer(thisRecord, data=request.data, partial=True)
            #print(request.data)
            if serializer.is_valid():
                serializer.save()
        except:
            return Response({'status':'trouble with updating game'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status=status.HTTP_200_OK)   


def InfoForLocations(request, *args, **kwargs):

    return_values = {
        "Sunday":[],
        "Monday":[],
        "Tuesday":[],
        "Wednesday":[],
        "Thursday":[],
        "Friday":[],
        "Saturday":[],
    }

    CanceledDates={
        "Sunday":[],
        "Monday":[],
        "Tuesday":[],
        "Wednesday":[],
        "Thursday":[],
        "Friday":[],
        "Saturday":[],
    }    
    this_day = date.today()
    for one_day in range(7):
        CanceledDates[calendar.day_name[this_day.weekday()]]=this_day
        this_day += timedelta(1)


    try:
        for one_game in GameModel.objects.filter(active=True).order_by('venue__venue_name','time'):

            this_dictionary=one_game.GetNextPlayedGameInfo(CanceledDates)
            return_values[one_game.week_day].append(this_dictionary)

    except Exception as e:
        print(e)
        return JsonResponse({
            'data':[],
            'status':'Problem'})
    
    return JsonResponse({
        'data':return_values,
        'status':'No Problem'})

class GameTypeView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            GameTypes = GameTypeModel.objects.all()
            serializer = GamesTypesSerializer(GameTypes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request,*args, **kwargs):
        try:
            serializer = GamesTypesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self, request,id,*args, **kwargs):

        def override_protction():            
            thesePlayedGames.delete()
            theseGames.delete()
            try:
                thisRecord.delete()
                return Response({}, status=status.HTTP_200_OK)
            except:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
                    
        try:
            thisRecord = GameTypeModel.objects.get(id=id)
            thisRecord.delete()

        except ProtectedError:
            theseGames=GameModel.objects.filter(venue=thisRecord)
            thesePlayedGames = PlayedGameModel.objects.filter(which_game__in=theseGames).filter(date__lt=date.today())
            if thesePlayedGames.count()==0:
                thesePlayedGames = PlayedGameModel.objects.filter(which_game__in=theseGames)
                override_protction()
            else:
                thesePlayedGames = PlayedGameModel.objects.filter(which_game__in=theseGames)
                players = [x  for thisGame in thesePlayedGames for x in thisGame.player_results.all()]
                if len(players)==0:
                    override_protction()

            return Response({}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({}, status=status.HTTP_200_OK)
    
    def patch(self, request,id,*args, **kwargs):
        try:
            thisRecord = GameTypeModel.objects.get(id=id)
            serializer = GamesTypesSerializer(thisRecord, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({}, status=status.HTTP_200_OK)   
    
class GamesForRostersView(APIView):
    def get(self, request,*args, **kwargs):
        all_game_data=[]

        for oneGame in GameModel.objects.exclude(description='default game'):
            all_game_data.append(oneGame.RosterDictionary())
        
        #all_venues = list(set([x['venue'] for x in all_game_data]))
        pass

        return Response({
            'all_game_data':all_game_data,
            'directors':set([x['director'] for x in all_game_data]),
            'venues':set([x['venue'] for x in all_game_data]),
            'all_dates':[x for y in all_game_data for x in y['dates']]
        }, status=status.HTTP_200_OK)   

class GameInfoForReview(APIView):
    def get(self, request, *args, **kwargs):
        return_value=[]

        try:
            for oneGame in GameModel.objects.all():
                return_value.append({
                    'title':oneGame.GetText(),
                    'dates':[x.get_date_with_ID() for x in self.played_games.all()]
                })
        except Exception as e:
            print(e)
            return Response({'status':'problem getting game info'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'all_data':return_value
        })
    
class PlayedGamesEvents(APIView):
    def get(self, request,  id, *args, **kwargs):

        try:
            thisGame = PlayedGameModel.objects.get(id=id)
            #serializer= PlayedGamesSerializer(thisGame, many=True)
            #print(serializer.data)
            return Response({'data':thisGame.get_players()},status=status.HTTP_200_OK)
        except Exception as e:

            print(e)
            return Response({'status':'problem'}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,id,*args,**kwargs):
        try:
            thisGame = PlayedGameModel.objects.get(id=id)
            thisGame.finalized=request.data['finalized']
            thisGame.save()
            
            return Response({'status':'finalized'},status=status.HTTP_200_OK)
        except:
            return Response({'status':'problem'}, status=status.HTTP_400_BAD_REQUEST)

class PlayedGamesList(APIView):
    def get(self,request,venueidstr,seasonidstr, *args, **kwargs):

        #seasonidstr and venueidstr are always -1 =>filtering in the front end
        seasonid=int(seasonidstr)
        venueid=int(venueidstr)       

        thisSeasonRec=None
        if seasonid>0:
            try:
               thisSeasonRec=SeasonModel.objects.get(id=seasonid)
        #         these_games=these_games.filter(season_type=thisSeasonRec.season_type)
            except:
                pass
        
        these_games=None
        thisVenueRec=None
        if venueid>0:
            try:
                thisVenueRec=VenueModel.objects.get(id=venueid)
                these_games= GameModel.objects.filter(venue=thisVenueRec)
            except:
                pass
        these_played_games = PlayedGameModel.objects.filter(finalized=True).exclude(season=None)
        if not thisSeasonRec==None:
            these_played_games=these_played_games.objects.filter(season=thisSeasonRec)
        if not these_games==None:
            these_played_games=these_played_games.objects.filter(which_game__in=these_games)
            
        serializer = PlayedGamesListSerializer(these_played_games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetCanceledGames(APIView):
    def get(self,  *args, **kwargs):

        try:
            CanceledGames = CanceledGamesModel.objects.filter(date__gte=datetime.today())
            serializer = CanceledGamesSerializer(CanceledGames, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request,*args, **kwargs):
        try:
            serializer = CanceledGamesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

        except Exception as e:
            print(e)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({}, status=status.HTTP_200_OK)        

class UnCancelGame(APIView):
    def delete(self, request,id,*args, **kwargs):

        try:
            thisRecord = CanceledGamesModel.objects.get(id=id)
            thisRecord.delete()

        except Exception as e:
            print(e)
            return Response({'error':'Not able to delete cancelation'}, status=status.HTTP_400_BAD_REQUEST)  

        return Response({}, status=status.HTTP_200_OK)             