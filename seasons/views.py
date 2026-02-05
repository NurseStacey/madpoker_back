from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

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
    
    
