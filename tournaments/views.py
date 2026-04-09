from django.shortcuts import render
from django.db.utils import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.http import JsonResponse
from venues.models import VenueModel
from games.models import GameTypeModel 

class OneTournamentAPI(APIView):
    def get(self, request, id, *args, **kwargs):

        try:
            Tournaments = TournamentModel.objects.get(id=id)
            serializer = TournamentSerializer(Tournaments)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'status':'Problem'}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request,id,*args, **kwargs):

        try:
            thisRecord = TournamentModel.objects.get(id=id)
            if (thisRecord.finalized):
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
            
            thisRecord.delete()

        except Exception as e:

            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({}, status=status.HTTP_200_OK)
    
    def patch(self, request,id,*args, **kwargs):
        print("patch")
        try:
            thisRecord = TournamentModel.objects.get(id=id)
            serializer = TournamentSerializer(thisRecord, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
            else:
                print (serializer.errors)
        except:
            return Response({'status':'trouble with updating game'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status=status.HTTP_200_OK)


class TournamentAPI(APIView):

    def get(self, request, *args, **kwargs):

        Tournaments = TournamentModel.objects.filter(finalized=False)
        serializer = TournamentSerializer(Tournaments, many=True)
        return Response(serializer.data)
    
    def post(self, request,*args, **kwargs):
        try:

            serializer = TournamentSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()

            else:
                if 'name' in serializer.errors:
                    for one_error in serializer.errors['name']:
                        if one_error.code=='unique':
                            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
                        
                print (serializer.errors)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)


        except Exception as e:
            print (e)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

def InfoForTournaments(request, *args, **kwargs):
    return_values = {
        'venues':[],
        'game_types':[],
        'status':'OK'        
    }
    try:
        return_values['venues'] = list(VenueModel.objects.filter(active=True).values('id', 'venue_name'))
        return_values['game_types'] = list(GameTypeModel.objects.all().values('id', 'name'))

    except Exception as e:
        print(e)
        return JsonResponse({
            'venues':[],
            'game_types':[],
            'status':'Problem'})
    
    return JsonResponse(return_values)