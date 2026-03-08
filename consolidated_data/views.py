from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from games.models import PlayedGameModel
from seasons.models import SeasonModel
import itertools
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class PullDataForPoints(APIView):
    def get(self, request, *args, **kwargs):

        return Response({}, status=status.HTTP_200_OK)
    
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

