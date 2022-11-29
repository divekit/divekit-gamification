from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .permissions import IsStaffOrReadOnly,IsStaffOrSelf,IsStaff
from .models import User
from .serializers import ChangePasswordSerializer, MyTokenObtainPairSerializer, UserSerializer,UserSerializerMinified
from rest_framework import serializers

from badges.models import UserBadge
from badges.serializers import BasicUserBadgeSerializer,UserBadgeSerializer

class ObtainTokenPairWithColorView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserListView(APIView):
    def get(self,request,*args,**kwargs):
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class UserListViewMinified(APIView):

    @method_decorator(cache_page(60*15))
    def get(self,request,*args,**kwargs):
        users = User.objects.all()
        serializer = UserSerializerMinified(users,many=True)
        return Response(serializer.data,status.HTTP_200_OK)

class UserCreate(APIView):
    permission_classes = (permissions.AllowAny,)    

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():

            email_exists = User.objects.filter(
                email=serializer.validated_data["email"]).exists()
            username_exists = User.objects.filter(
                username=serializer.validated_data["username"]).exists()
            if email_exists and username_exists:
                return Response({"email": "Email already exists", "username": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
            if email_exists:
                return Response({"email": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            if username_exists:
                return Response({"username": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):

    permission_classes = (IsStaffOrSelf,)

    # @method_decorator(cache_page(60*15))
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs["user_id"])
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


    def put(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs["user_id"])
        self.check_object_permissions(self.request, user)

        serializer = UserSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

        if serializer.is_valid():
            return Response(serializer.data, status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserBadgeListView(APIView):
    permission_classes = (IsStaffOrReadOnly,)

    def get(self,request,*args,**kwargs):

        badges = UserBadge.objects.filter(owner=kwargs["user_id"]).all()
        serializer = UserBadgeSerializer(badges,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        serializer = BasicUserBadgeSerializer(data=request.data)
        if serializer.is_valid():
            print("VALID")
            user_badge = serializer.save()
            if user_badge:
                return Response(serializer.data,status=status.HTTP_201_CREATED)


        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)