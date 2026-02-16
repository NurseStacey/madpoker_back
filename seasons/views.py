from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from games.models import PlayedGameModel
import itertools

class SeasonsWithVenuesGamesAPI(APIView):
    def get(self,  request, *args,**kwargs):
        return_values=[]

        try:
            for oneSeason in SeasonModel.objects.all():
                theseGames = PlayedGameModel.objects.filter(
                    date__gte=oneSeason.start_date).filter(
                        date__lte=oneSeason.end_date).filter(
                            which_game__season_type=oneSeason.season_type)

                tempVenues = set([one_game.venue.venue_name for one_game in theseGames])
                tempGameTitles= set([one_game.which_game.get_text() for one_game in theseGames])
                return_values.append({
                    'season_name':oneSeason.season,
                    'venues':tempVenues,
                    'games':tempGameTitles
                })
        except Exception as e:
            print(e)
            return Response({'error':'error collected season data'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'all_data':return_values,
            'venues':set(itertools.chain.from_iterable([x['venues'] for x in return_values])),
            'games':set(itertools.chain.from_iterable([x['game_titles'] for x in return_values]))
            }, status=status.HTTP_200_OK)
                        
class SeasonTypeModelAPI(APIView):
    def get(self, request, *args, **kwargs):
        #For season types
        Seasons = SeasonTypeModel.objects.all()
        serializer = SeasonTypesSerializer(Seasons, many=True)

        return Response(serializer.data)
        
class SeasonModelAPI(APIView):
    #For seasons
    def get(self, request, *args, **kwargs):

        Seasons = SeasonModel.objects.all()
        serializer = SeasonSerializer(Seasons, many=True)

        return Response(serializer.data)
    
    def post(self, request,*args, **kwargs):
        
        if 'season_type_text' in request.data:
            obj, created = SeasonTypeModel.objects.get_or_create(
                season_type=request.data['season_type_text']
            )

            request.data['season_type']=obj.id
            del request.data['season_type_text']

            
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
            print(request.data)
            thisRecord = SeasonModel.objects.get(id=id)
            serializer = SeasonSerializer(thisRecord, data=request.data, partial=True)
            if serializer.is_valid():

                serializer.save()
                
        except Exception as e:
            print(e)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status=status.HTTP_200_OK)   
    
    def delete(self, request,id,*args, **kwargs):
        
        try:
            thisRecord = SeasonModel.objects.get(id=id)
            thisRecord.delete()
        except Exception as e:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({}, status=status.HTTP_200_OK)    
    
    
