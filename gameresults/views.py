from django.shortcuts import render
from rest_framework import status
from players.models import PlayerModel
from games.models import GameModel,PlayedGameModel
from venues.models import VenueModel
from seasons.models import SeasonModel
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum,F,Avg,Func
       
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
            if position>(number_of_players-10):
                return 2*(position+1)
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

class ThisGameResult(APIView):
    def get(self, request, id, *args, **kwargs):

        this_game_result=[]

        for one_result in GameResultModel.objects.filter(game=PlayedGameModel.objects.get(id=id)).order_by('position'):
            this_game_result.append(one_result.this_result_no_venue())
            
        return Response({
            'this_game_result':this_game_result
            }, status=status.HTTP_200_OK)
    
    
class Round(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 2)'

class PullDataForPoints(APIView):
    def get(self, request, playeridstr, seasonidstr, venueidstr,*args, **kwargs):
        playerid=int(playeridstr)
        seasonid=int(seasonidstr)
        venueid=int(venueidstr)

        try:
            thisPlayerRec=PlayerModel.objects.get(id=playerid)
        except:
            return Response({'result':'Problem with getting player data.'}, status=status.HTTP_404_NOT_FOUND)

        thisSeasonRec=None
        if seasonid>0:
            try:
                thisSeasonRec=SeasonModel.objects.get(id=seasonid)
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
        
        try:
            these_played_games=PlayedGameModel.objects.filter(
                    finalized=True)
            
            if not thisSeasonRec==None:
                these_played_games=these_played_games.filter(season=thisSeasonRec)
            if not these_games==None:
                these_played_games=these_played_games.filter(which_game__in=these_games)

            these_game_reults = GameResultModel.objects.filter(game__in=these_played_games)
            all_player_summary = these_game_reults.annotate(
                season_name=F('game__season__season')
                    ).annotate(season_start_date=F('game__season__start_date')
                        ).annotate(player_name=F('player__player')
                           ).values('season_name', 'player_name'                    
                                ).annotate(total_points=Sum('points')
                                    ).annotate(average_points=Round(Avg('points'))
                                        ).annotate(average_position=Round(Avg('position'))
                                          ).order_by('-season_start_date')
            
            season_stats = []
            for one_season in set([x['season_name'] for x in all_player_summary]):
                this_position_list = list(reversed(sorted([x['total_points'] for x in [y for y in all_player_summary if y['season_name']==one_season]])))
                try:
                    this_player_position = all_player_summary.filter(season_name=one_season).get(player=thisPlayerRec)
                    this_position = this_position_list.index(this_player_position['total_points'])+1
                    season_stats.append({
                        'season_name':one_season,
                        'position':this_position,
                        'average_position':this_player_position['average_position'],
                        'average_points':this_player_position['average_points'],
                        'total_points':this_player_position['total_points'],
                    })
                except:
                    pass
                
            game_results = these_game_reults.filter(player=thisPlayerRec
                ).annotate(date=F('game__date')
                    ).annotate(venue=F('game__which_game__venue__venue_name')
                        ).annotate(season_name=F('game__season__season')
                            ).annotate(game_type=F('game__which_game__game_type__name')                           
                                ).values('season_name','points','position','date', 'venue', 'season_name','game_type'
                                    ).order_by('-date')

            game_results_list=[]
            for one_game_result in game_results:
                this_result = one_game_result
                this_result['date']=this_result['date'].strftime('%m-%d-%Y')
                game_results_list.append(this_result)
            
        except Exception as e:
            print(e)
            return Response({
                'result':'Problem',
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'result':'OK',
            'individual_game_results':game_results_list,
            'season_stats':season_stats,
            }, status=status.HTTP_200_OK)
    