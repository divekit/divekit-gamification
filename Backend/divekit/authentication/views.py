from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from .permissions import IsStaffOrReadOnly,IsStaffOrSelf,IsStaff
from .models import User
from .serializers import (ChangePasswordSerializer, 
                            MyTokenObtainPairSerializer, 
                            UserSerializer,
                            UserSerializerMinified,
                            UserCreateSerializer,
                            RefreshPasswordSerializer)
from rest_framework import serializers

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from badges.models import UserBadge
from badges.serializers import BasicUserBadgeSerializer,UserBadgeSerializer


class CustomTokenRefreshView(TokenRefreshView):
    
    @extend_schema(
        tags=["auth"]
    )
    def post(self,request,*args,**kwargs):
        response = super().post(request,*args,**kwargs)
        return response

class ObtainTokenPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    @extend_schema(
        tags=["auth"]
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request,*args,**kwargs)
        return response


class UserListView(APIView):
    permission_classes = (IsStaff,)
    
    @extend_schema(
        tags=["auth"],
        exclude=True
        
    )
    def get(self,request,*args,**kwargs):
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data, status.HTTP_200_OK)

class UserListViewMinified(APIView):

    @extend_schema(
        tags=["auth"],
        operation_id="asdasd",
        responses={200:UserSerializerMinified}
    )
    def get(self,request,*args,**kwargs):
        
        users = User.objects.filter(visible_in_community=True).all()
        serializer = UserSerializerMinified(users,many=True,context = {'request':request})
        return Response(serializer.data,status.HTTP_200_OK)

class UserCreate(APIView):
    permission_classes = (permissions.AllowAny,)    

    @extend_schema(
        tags=["auth"],
        request=UserCreateSerializer
    )
    def post(self, request, format='json'):
        serializer = UserCreateSerializer(data=request.data)
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
                confirmation_token = default_token_generator.make_token(user)
                actiavation_link = f'http://{request.get_host()}/api/v1/users/confirmation?user_id={user.id}&confirmation_token={confirmation_token}'
                send_mail(
                    'Konto Bestätigen',
                    f'Bitte bestätigen Sie Ihr Konto indem Sie auf den folgenden Link drücken. \n {actiavation_link}',
                    None,
                    [serializer.validated_data["email"],],
                    fail_silently=True,
                )
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserActivationView(APIView):
    permission_classes = (permissions.AllowAny,)

    @extend_schema(
        tags=["auth"],
        exclude=True
    )
    def get(self,request,*args,**kwargs):
        
        user_id = request.query_params.get('user_id', '')
        confirmation_token = request.query_params.get('confirmation_token', '')
        try:
            user = User.objects.get(pk=user_id)
        except Exception as e:
            user = None
        
        if user is None:
            return Response({
                "errors":[
                    {
                        "message":"User not found."
                    }
                ]
            },status=status.HTTP_404_NOT_FOUND)
        
        if not default_token_generator.check_token(user,confirmation_token):
            return Response({
                "errors":[
                    {
                        "message":"Token is not valid."
                    }
                ]
            },status=status.HTTP_400_BAD_REQUEST)
        default_token_generator
        user.is_verified = True
        user.save()
        # return Response({"success":True,"message":"Email successfully confirmed"},status=status.HTTP_200_OK)
        return HttpResponseRedirect(redirect_to='http://localhost:3000/login')

class UserDetailView(APIView):

    permission_classes = (IsStaffOrSelf,)

    # @method_decorator(cache_page(60*15))
    @extend_schema(
        tags=["auth"]
    )
    def get(self, request, *args, **kwargs):
        print(request.user.id)
        user = User.objects.get(id=kwargs["user_id"])

        if request.user.id == kwargs["user_id"]:
            serializer = UserSerializer(user)
        else:
            serializer = UserSerializerMinified(user)
        
        return Response(serializer.data, status.HTTP_200_OK)


    @extend_schema(
        tags=["auth"],
        request=UserSerializer
    )
    def put(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs["user_id"])
        self.check_object_permissions(self.request, user)

        serializer = UserSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

        if serializer.is_valid():
            return Response(serializer.data, status.HTTP_200_OK)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=["auth"]
    )
    def delete(self,request,*args,**kwargs):
        user = User.objects.get(id=kwargs["user_id"])
        self.check_object_permissions(self.request, user)
        if user:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class UserBadgeListView(APIView):
    permission_classes = (IsStaffOrReadOnly,)

    @extend_schema(
        tags=["auth"]
    )
    def get(self,request,*args,**kwargs):

        badges = UserBadge.objects.filter(owner=kwargs["user_id"]).all()
        serializer = UserBadgeSerializer(badges,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    @extend_schema(
        tags=["auth"]
    )
    def post(self,request,*args,**kwargs):
        serializer = BasicUserBadgeSerializer(data=request.data)
        if serializer.is_valid():
            print("VALID")
            user_badge = serializer.save()
            if user_badge:
                return Response(serializer.data,status=status.HTTP_201_CREATED)


        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class UserRefreshPasswordView(APIView):

    permission_classes = (permissions.AllowAny,)

    @extend_schema(
        tags=["auth"],
        # request=UserSerializer
        request=RefreshPasswordSerializer
    )
    def put(self,request,*args,**kwargs):
        # user = 
        serializer = RefreshPasswordSerializer(request.data)
        if serializer.is_valid:
            print("VALID")
            # print()
            user = User.objects.filter(email=serializer.data["email"]).first()
            # print(user)
            if user:
                password = User.objects.make_random_password()
                # print(user)
                user.set_password(password)
                
                user.save()
                send_mail(  "DivekitBadge Passwort wurde geändert",
                            f"Hier ist das neue Passwort: {password}",
                            None,
                            recipient_list=[user.email],
                            fail_silently=True,
                        )
                
            else:
                print("USER NOT FOUND")
                return Response({"detail":"Fehler aufgetreten!"},status=status.HTTP_400_BAD_REQUEST)


        # print(user)
        return Response(status=status.HTTP_200_OK)