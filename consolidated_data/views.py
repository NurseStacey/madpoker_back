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
from django.db.models import Sum

class PullDataForPoints(APIView):
    def get(self, request, playeridstr, seasonidstr, venueidstr,*args, **kwargs):
        playerid=int(playeridstr)
        seasonid=int(seasonidstr)
        venueid=int(venueidstr)
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
        
        thisVenueRec=None
        if venueid>0:
            try:
                thisVenueRec=VenueModel.objects.get(id=venueid)
                these_games=these_games.filter(venue=thisVenueRec)
            except:
                pass
        
        try:
            these_played_games=None
            if thisSeasonRec==None:
                these_played_games=PlayedGameModel.objects.filter(
                    finaliezed=True).filter(
                            which_game__in=these_games).order_by('-date')            
            else:

                these_played_games=PlayedGameModel.objects.filter(
                    finaliezed=True).filter(
                    date__gte=thisSeasonRec.start_date).filter(
                        date__lt=thisSeasonRec.end_date).filter(
                            which_game__in=these_games).order_by('-date')

            individual_game_results={}
            what_seasons = []
            season_summary={}
            for one_game in these_played_games:
                try:
                    one_result= GameResultModel.objects.filter(player=thisPlayerRec).get(game=one_game)
                    one_result_values=one_result.this_result()
                    if one_result_values['season']['season_name'] not in individual_game_results:
                        if not thisVenueRec==None:
                            one_result_values['season']['season_title'] = one_result_values['season']['season_title'] + ' - ' + thisVenueRec.venue_name
                        what_seasons.append(one_result_values['season'])
                        season_summary[one_result_values['season']['season_name']]={
                            'total_points':0,
                            'average_position':0,
                            'average_points':0,
                            'season_position':0
                        }
                        individual_game_results[one_result_values['season']['season_name']]=[]

                    individual_game_results[one_result_values['season']['season_name']].append({
                        'display_pieces':one_result_values['display_pieces'],
                        'display_str':one_result_values['display_str'],
                        'id':one_result_values['id']
                        })
                    season_summary[one_result_values['season']['season_name']]['total_points']+=one_result_values['points']
                    season_summary[one_result_values['season']['season_name']]['average_position']+=one_result_values['position']
                    season_summary[one_result_values['season']['season_name']]['average_points']+=one_result_values['points']

                except:
                    pass

        except:
            return Response({
                'result':'Problem',
                }, status=status.HTTP_400_BAD_REQUEST)
        
        for one_season in what_seasons:
            season_summary[one_season['season_name']]['average_position']/=len(individual_game_results[one_season['season_name']])
            season_summary[one_season['season_name']]['average_position']=round(season_summary[one_season['season_name']]['average_position'],1)
            season_summary[one_season['season_name']]['average_points']/=len(individual_game_results[one_season['season_name']])
            season_summary[one_season['season_name']]['average_points']=round(season_summary[one_season['season_name']]['average_points'],1)

            results_for_season = GetSeasonRankings(SeasonModel.objects.get(season=one_season['season_name']))

            season_summary[one_season['season_name']]['season_position'] = results_for_season.filter(total_points__gt=results_for_season.get(player=thisPlayerRec)['total_points']).count()+1

        return Response({
            'result':'OK',
            'individual_game_results':individual_game_results,
            'what_seasons':reversed(sorted(what_seasons, key=lambda x:x['season_start_index'])),
            'season_summaries':season_summary
            }, status=status.HTTP_200_OK)
    
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
