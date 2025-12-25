from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny
from rest_framework import status


# Create your views here.
class HomePageTextAPI(APIView):
    
    def get(self, request, *args, **kwargs):
        TextItems = HomePageText.objects.all()
        serializer = HomePageTextSerializer(TextItems, many=True)
        return Response(serializer.data)
    
    def post(self, request,*args, **kwargs):
        serializer = HomePageTextSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)