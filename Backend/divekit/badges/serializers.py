from rest_framework import serializers
from .models import Badge,UserBadge, Module
from django.core.exceptions import ValidationError


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = "__all__"
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['is_hidden']:
            del (representation["name"],representation["description"],representation["img"],representation["milestones"])

        return representation


class BadgeSerializerNoHidden(serializers.ModelSerializer):
    class Meta:
        model = Badge
        exclude = ("created_at",)
    



class BasicUserBadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBadge
        fields = "__all__"
    
    def validate_badge(self,value):
        if value.is_unique and self.context['request'].method == "POST":
            user_badge = UserBadge.objects.filter(owner=self.initial_data["owner"],badge=value).get()
            if user_badge:
                raise ValidationError('This Badge (%s-%s) is unique and therefore cannot be assigned twice to a user' % (value.id, value.name))
        
        
        return value

class UserBadgeSerializerMinified(serializers.ModelSerializer):
    badge = BadgeSerializerNoHidden()
    class Meta:
        model = UserBadge
        exclude = ("progress","earned_at","owner","last_progress_at")

class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializerNoHidden()
    class Meta:
        model = UserBadge
        fields = "__all__"



class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = "__all__"