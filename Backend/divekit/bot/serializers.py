from rest_framework import serializers
from .models import Verification,Notification
from django.core.exceptions import ValidationError


class VerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verification
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    class Meta:
        model = Notification
        fields = "__all__"
        

    def get_owner(self,instance):
        print(instance)
        if not instance.owner.discord_username:
            return None
        return instance.owner.discord_username

    def validate(self,data):
        validated_data = super().validate(data)

        if not validated_data["owner"].notify_badge:
            raise serializers.ValidationError({'detail': ['The user does not allow to send notifications.']})

        return validated_data