
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .permissions import IsStaffOrReadOnly, IsStaffOrSelf,IsStaff
from .models import Badge, UserBadge,Module
from .serializers import BadgeSerializer, UserBadgeSerializer,BasicUserBadgeSerializer,ModuleSerializer


class UserBadgeListView(APIView):
    permission_classes = (IsStaff,)
    def get(self,request,*args,**kwargs):
        user_badges = UserBadge.objects.all()
        
        serializer = UserBadgeSerializer(user_badges,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request, *args, **kwargs):
        data = request.data
        serializer = BasicUserBadgeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class BadgeView(APIView):
    permission_classes = (IsStaffOrReadOnly,)

    # @method_decorator(cache_page(60*15))
    def get(self, request, *args, **kwargs):
        badges = Badge.objects.all()
        
        # if not dictionaries:
        #     return Response({"msg": "test"}, status.HTTP_404_NOT_FOUND)
        serializer = BadgeSerializer(badges, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
    def get(self,request,*args,**kwargs):
        modules = Module.objects.all()
        serializer = ModuleSerializer(modules,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)