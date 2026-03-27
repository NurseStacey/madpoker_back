from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from games.models import PlayedGameModel
from seasons.models import SeasonModel
import itertools
#from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from players.models  import PlayerModel
from games.models import GameModel,PlayedGameModel
from seasons.models import SeasonModel
from venues.models import VenueModel
from gameresults.models import GameResultModel
from django.db.models import Sum,F,Avg,Func
from .serializers import *

# class Round(Func):
#     function = 'ROUND'
#     template='%(function)s(%(expressions)s, 2)'

# class PullDataForPoints(APIView):
#     def get(self, request, playeridstr, seasonidstr, venueidstr,*args, **kwargs):
#         playerid=int(playeridstr)
#         seasonid=int(seasonidstr)
#         venueid=int(venueidstr)

#         try:
#             thisPlayerRec=PlayerModel.objects.get(id=playerid)
#         except:
#             return Response({'result':'Problem with getting player data.'}, status=status.HTTP_404_NOT_FOUND)

#         thisSeasonRec=None
#         if seasonid>0:
#             try:
#                 thisSeasonRec=SeasonModel.objects.get(id=seasonid)
#             except:
#                 pass
        
#         these_games=None
#         thisVenueRec=None
#         if venueid>0:
#             try:
#                 thisVenueRec=VenueModel.objects.get(id=venueid)
#                 these_games= GameModel.objects.filter(venue=thisVenueRec)
#             except:
#                 pass
        
#         try:
#             these_played_games=PlayedGameModel.objects.filter(
#                     finalized=True)
            
#             if not thisSeasonRec==None:
#                 these_played_games=these_played_games.objects.filter(season=thisSeasonRec)
#             if not these_games==None:
#                 these_played_games=these_played_games.objects.filter(which_game__in=these_games)

#             these_game_reults = GameResultModel.objects.filter(game__in=these_played_games)
#             all_player_summary = these_game_reults.annotate(
#                 season_name=F('game__season__season')
#                     ).annotate(season_start_date=F('game__season__start_date')
#                         ).annotate(player_name=F('player__player')
#                            ).values('season_name', 'player_name'                    
#                                 ).annotate(total_points=Sum('points')
#                                     ).annotate(average_points=Round(Avg('points'))
#                                         ).annotate(average_position=Round(Avg('position'))
#                                           ).order_by('-season_start_date')
            
#             season_stats = []
#             for one_season in set([x['season_name'] for x in all_player_summary]):
#                 this_position_list = list(reversed(sorted([x['total_points'] for x in [y for y in all_player_summary if y['season_name']==one_season]])))
#                 this_player_position = all_player_summary.filter(season_name=one_season).get(player=thisPlayerRec)
#                 this_position = this_position_list.index(this_player_position['total_points'])+1
#                 season_stats.append({
#                     'season_name':one_season,
#                     'position':this_position,
#                     'average_position':this_player_position['average_position'],
#                     'average_points':this_player_position['average_points'],
#                     'total_points':this_player_position['total_points'],
#                 })

#             game_results = these_game_reults.filter(player=thisPlayerRec
#                 ).annotate(date=F('game__date')
#                     ).annotate(venue=F('game__which_game__venue__venue_name')
#                         ).annotate(season_name=F('game__season__season')
#                             ).annotate(game_type=F('game__which_game__game_type__name')                           
#                                 ).values('season_name','points','position','date', 'venue', 'season_name','game_type'
#                                     ).order_by('-date')

#             game_results_list=[]
#             for one_game_result in game_results:
#                 this_result = one_game_result
#                 this_result['date']=this_result['date'].strftime('%m-%d-%Y')
#                 game_results_list.append(this_result)
            
#         except Exception as e:
#             print(e)
#             return Response({
#                 'result':'Problem',
#                 }, status=status.HTTP_400_BAD_REQUEST)
        
#         return Response({
#             'result':'OK',
#             'individual_game_results':game_results_list,
#             'season_stats':season_stats,
#             }, status=status.HTTP_200_OK)
    
    
class InfoForSearch(APIView):
    def get(self,  request, *args,**kwargs):
        return_values=[]

        try:
            for oneSeason in SeasonModel.objects.all():
                theseGames = PlayedGameModel.objects.filter(
                    date__gte=oneSeason.start_date).filter(
                        date__lte=oneSeason.end_date).filter(
                            which_game__season_type=oneSeason.season_type)

                tempVenues = set([one_game.which_game.venue.venue_name for one_game in theseGames])
                tempGameTitles= set([one_game.which_game.GetText() for one_game in theseGames])
                return_values.append({
                    'season_name':oneSeason.season,
                    'venues':tempVenues,
                    'game_titles':tempGameTitles
                })
        except Exception as e:
            print(e)
            return Response({'error':'error collected season data'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'all_data':return_values,
            'venues':set(itertools.chain.from_iterable([x['venues'] for x in return_values])),
            'game_titles':set(itertools.chain.from_iterable([x['game_titles'] for x in return_values]))
            }, status=status.HTTP_200_OK)

def GetSeasonRankings(this_season):


    which_games = GameModel.objects.filter(season_type=this_season.season_type)
    these_played_games=PlayedGameModel.objects.filter(
        date__gte=this_season.start_date).filter(
            date__lt=this_season.end_date).filter(
                which_game__in=which_games)
    
    return GameResultModel.objects.filter(game__in=these_played_games).values('player__player').annotate(total_points=Sum('points'))
