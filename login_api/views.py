from django.shortcuts import render
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import *

class UserRegistrationView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        try:        
            serializer=self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user=serializer.save()
            token=RefreshToken.for_user(user)
            data = serializer.data
            data['tokens']={'refresh':str(token),
                            'access':str(token.access_token)}

            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
class AllUserAPIView(GenericAPIView):

    def get(self, request, *args, **kwargs):

        all_users = UserModel.objects.all()
        serializer = CustomUserSerializer(all_users, many=True)
        return Response(serializer.data)

    def patch(self, request,id,  *args, **kwargs):
        try:
            thisRecord = UserModel.objects.get(id=id)
            serializer =CustomUserSerializer(thisRecord,data=request.data)
            #print(request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({}, status=status.HTTP_200_OK)  
        except Exception as e:
            print(e)
        return Response({'status':'trouble with updating profile'}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request,id,  *args, **kwargs):

        try:
            this_users = UserModel.objects.get(id=id)
            this_users.delete()

            return Response({}, status=status.HTTP_200_OK)  
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)   
    
class UserLoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer


    
    def post(self, request, *args, **kwargs):
        try:
            serializer=self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user=serializer.validated_data
            serializer=CustomUserSerializer(user)
            token=RefreshToken.for_user(user)
            data = serializer.data
            data['tokens']={'refresh':str(token),
                            'access':str(token.access_token)}
        except Exception as e:
            print(e)
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(data, status=status.HTTP_200_OK)
    
class UserLogoutAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token=request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
class UserInfoAPIView(RetrieveAPIView):
    permission_classes  = (IsAuthenticated,)
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user