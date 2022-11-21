from rest_framework import serializers
from .models import Badge,UserBadge

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = "__all__"



class BasicUserBadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBadge
        fields = "__all__"

class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer()
    class Meta:
        model = UserBadge
        fields = "__all__"