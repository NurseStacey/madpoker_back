from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from games.models import PlayedGameModel
from seasons.models import SeasonModel
import itertools
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from players.models  import PlayerModel
from games.models import GameModel,PlayedGameModel
from seasons.models import SeasonModel
from venues.models import VenueModel
from gameresults.models import GameResultModel

class PullDataForPoints(APIView):
    def get(self, request, playerid, seasonid, venueid,*args, **kwargs):
        
        try:
            thisPlayerRec=PlayerModel.objects.get(id=playerid)
        except:
            return Response({'result':'Problem with getting player data.'}, status=status.HTTP_404_NOT_FOUND)

        these_games = GameModel.objects.all()
        thisSeasonRec=None
        if seasonid>0:
            try:
                thisSeasonRec=SeasonModel.objects.get(id=seasonid)
                these_games=these_games.filter(season_type=thisSeasonRec.season_type)
            except:
                pass
        
        if venueid>0:
            try:
                thisVenueRec=VenueModel.objects.get(id=venueid)
                these_games=these_games.filter(venue=thisVenueRec)
            except:
                pass
        
        try:
            these_played_games =PlayedGameModel.objects.filter(which_game__in=these_games)
            these_results = GameResultModel.objects.filter(player=thisPlayerRec).filter(game__in=these_played_games)
            if thisSeasonRec!=None:
                these_results=these_results.filter(date__gte=thisSeasonRec.start_date).filter(date__lt=thisSeasonRec.end_date)
            
            individual_game_results=[]
            for one_result in these_games.order_by('-date'):
                individual_game_results.append(one_result.this_result())

        except:
            return Response({
                'result':'OK',
                'individual_game_results':individual_game_results
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'result':'OK'}, status=status.HTTP_200_OK)
    
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

