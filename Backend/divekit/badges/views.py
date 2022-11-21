
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Badge, UserBadge
from .serializers import BadgeSerializer, UserBadgeSerializer,BasicUserBadgeSerializer


class UserBadgeListView(APIView):
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
