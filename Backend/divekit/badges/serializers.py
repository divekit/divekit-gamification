from rest_framework import serializers
from .models import Badge,UserBadge
from authentication.models import User
from django.core.exceptions import ValidationError
class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = "__all__"



class BasicUserBadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBadge
        fields = "__all__"
    
    def validate_badge(self,value):
        if value.is_unique:
            if UserBadge.objects.filter(owner=self.initial_data["owner"],badge=value):
                raise ValidationError('This Badge (%s-%s) is unique and therefore cannot be assigned twice to a user' % (value.id, value.name))
        
        
        return value

class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer()
    class Meta:
        model = UserBadge
        fields = "__all__"