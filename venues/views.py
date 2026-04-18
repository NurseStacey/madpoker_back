from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.db.models import ProtectedError
from games.models import PlayedGameModel, GameModel
from datetime import date
from rest_framework.parsers import MultiPartParser, FormParser

class VenuesAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = VenuesSerializer
    def get(self, request, *args, **kwargs):

        try:
            TextItems = VenueModel.objects.all().order_by('venue_name')
            serializer = VenuesSerializer(TextItems, many=True)         
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request,*args, **kwargs):
        try:
            serializer=self.get_serializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            
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
            thisRecord = VenueModel.objects.get(id=id)
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
            thisRecord = VenueModel.objects.get(id=id)
            serializer = VenuesSerializer(thisRecord, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({}, status=status.HTTP_200_OK)   
    