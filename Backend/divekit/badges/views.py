
from rest_framework import status, permissions
from rest_framework.response import Response
from django.http import Http404 
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .permissions import IsStaffOrReadOnly, IsStaffOrSelf,IsStaff
from .models import Badge, UserBadge,Module
from .serializers import BadgeSerializer, UserBadgeSerializer,BasicUserBadgeSerializer,ModuleSerializer
from django.core.mail import send_mail
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from django.core.exceptions import ValidationError


class TestView(APIView):

    @extend_schema(
        tags=["users"],
        exclude=True
    )
    def get(self,request,*args,**kwargs):
        # print(self.request.query_params.get("foo"))
        print(request.query_params.getlist('foo[]')[0])
        return Response(status=status.HTTP_200_OK)

class UserBadgeListView(APIView):
    permission_classes = (IsStaffOrReadOnly,)
    
    @extend_schema(
        tags=["users"],
        responses={200: BasicUserBadgeSerializer},
    )
    def get(self,request,*args,**kwargs):
        user_id = kwargs.get("user_id")
        print(user_id)
        user_badges = UserBadge.objects.filter(owner=user_id).all()
        print(user_badges)
        serializer = UserBadgeSerializer(user_badges,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=BasicUserBadgeSerializer,
        responses={
            201: BasicUserBadgeSerializer,
        },
        parameters=[
          BasicUserBadgeSerializer,
        ],
        description="Give a user a new badge",
        tags=["users"]
    )
    def post(self,request, *args, **kwargs):
        data = request.data
        serializer = BasicUserBadgeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserBadgeDetailView(APIView):

    permission_classes = (IsStaffOrReadOnly,)
    
    @extend_schema(
        tags=["users"],
        request=BasicUserBadgeSerializer,
        examples=[
            OpenApiExample(
            'Example1',
            summary='Example Update Progress',
            value={
                'progress': 3,
            },
            request_only=True,
        ),
        OpenApiExample(
            'Example',
            summary='Example Update All Fields',
            value={
                "owner":"int",
                "badge":"int",
                "progress":"int",

            },
            request_only=True, 
        ),
        ],
        responses={202: BasicUserBadgeSerializer},
    )
    def put(self,request,*args,**kwargs):
        data = request.data
        data["owner"] = kwargs.get("user_id")
        data["badge"] = kwargs.get("badge_id")
        user_badge = UserBadge.objects.filter(owner=data["owner"]).filter(badge=data["badge"]).get()
        serializer = BasicUserBadgeSerializer(user_badge,data=data,partial=True,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=["users"]
    )
    def delete(self,request,*args,**kwargs):
        try:
            user_badge = UserBadge.objects.filter(owner=kwargs.get("user_id")).filter(badge=kwargs.get("badge_id")).get()
        except UserBadge.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

        if user_badge:
            user_badge.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
            
        



class BadgeView(APIView):
    permission_classes = (IsStaffOrReadOnly,)

    # @method_decorator(cache_page(60*15))
    @extend_schema(
        tags=["users"]
    )
    def get(self, request, *args, **kwargs):
        badges = Badge.objects.all()
        
        # if not dictionaries:
        #     return Response({"msg": "test"}, status.HTTP_404_NOT_FOUND)
        serializer = BadgeSerializer(badges, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["users"]
    )
    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = BadgeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ModuleListView(APIView):
    permission_classes = (IsStaffOrReadOnly,)


    # @method_decorator(cache_page(60*15))
    @extend_schema(
        tags=["users"]
    )
    def get(self,request,*args,**kwargs):
        modules = Module.objects.all()
        serializer = ModuleSerializer(modules,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)