from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User
from badges.models import UserBadge
from badges.serializers import BadgeSerializer,UserBadgeSerializer



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        # Add custom claims
        # token['app_lang'] = user.main_language
        token["username"] = user.username
        token["theme"] = user.get_theme_display()
        token["is_staff"] = user.is_staff
        if(user.img):
            token["img"] = user.img.url
        else:
            token["img"] = None

        return token








class UserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    email = serializers.EmailField(
        required=True
    )
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)
    # badges = UserBadgeSerializer(many=True)
    badges = serializers.SerializerMethodField()
    total_badges = serializers.SerializerMethodField()

    class Meta:
        model = User
        # fields = ('email', 'username', 'password')
        
        extra_kwargs = {
            'password': {'write_only': True},
            'discord_username': {'write_only': True},
            "email":{"write_only":True},
            'campus_id': {'write_only': True},
            'badges': {'read_only': True},
        }
        exclude = ('last_name',"first_name","groups","is_active","is_superuser","theme","user_permissions")

    def get_total_badges(self,instance):
        count = UserBadge.objects.filter(owner=instance).count()
        return count


    def get_badges(self,instance):
        user_badges = UserBadge.objects.filter(owner=instance).all()
        return UserBadgeSerializer(user_badges,many=True).data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserSerializerMinified(serializers.ModelSerializer):

    username = serializers.CharField()
    badges = serializers.SerializerMethodField()
    total_badges = serializers.SerializerMethodField()

    class Meta:
        model = User        
        extra_kwargs = {
            'password': {'write_only': True},
            'discord_username': {'write_only': True},
            "email":{"write_only":True},
            'campus_id': {'write_only': True},
            'badges': {'read_only': True},
        }
        exclude = ('last_name',"first_name","groups","is_active","is_superuser","theme","user_permissions")

    def get_total_badges(self,instance):
        count = UserBadge.objects.filter(owner=instance).count()
        return count


    def get_badges(self,instance):
        user_badges = UserBadge.objects.filter(owner=instance).all()[:10]
        return UserBadgeSerializer(user_badges,many=True).data



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, data):
        if data["new_password"] != data["new_password_confirm"]:
            raise ValidationError(
                {'new_password_confirm': "The two password fields didn't match."})
        return data