from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import  get_user_model, get_user
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers,exceptions
from .models import User
from badges.models import UserBadge
from badges.serializers import BadgeSerializer,UserBadgeSerializer,UserBadgeSerializerMinified
from drf_spectacular.utils import extend_schema,extend_schema_field
from drf_spectacular.types import OpenApiTypes

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self,data):
        validated_data = super().validate(data)
        if not self.user.is_verified:
            raise serializers.ValidationError({'detail': ['The user has not been verified.']})
        return validated_data
        

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


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, write_only=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        # fields = ('email', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'discord_username': {'write_only': True},
            "email":{"write_only":True},
            'campus_id': {'write_only': True},
        }
        fields = ("email","password","username","discord_username","campus_id")
    
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)
    badges = serializers.SerializerMethodField()
    total_badges = serializers.SerializerMethodField()


    class Meta:
        model = User
        # fields = ('email', 'username', 'password')
        
        extra_kwargs = {
            'password': {'write_only': True},
            # 'discord_username': {'write_only': True},
            # "email":{"read_only":True},
            'campus_id': {'read_only': True},
            'badges': {'read_only': True},
            "is_staff":{"read_only":True},
            # "last_login":{"read_only":True},
            "date_joined":{"read_only":True},
            "total_badges":{"read_only":True}
        }
        exclude = ('last_name',"first_name","groups","is_active","is_superuser","theme","user_permissions","last_login","campus_id","date_joined","is_verified")

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
    discord_username = serializers.SerializerMethodField()

    class Meta:
        model = User        
        extra_kwargs = {
            # 'password': {'write_only': True},
            'discord_username': {'write_only': True},
            # "email":{"write_only":True},
            # 'campus_id': {'write_only': True},
            'badges': {'read_only': True},
            # "is_staff":{"read_only":True},
            # "last_login":{"read_only":True},
            # "date_joined":{"read_only":True},
            "total_badges":{"read_only":True}
        }
        exclude = ("is_staff",'last_name',"first_name","groups","is_active","is_superuser","theme","user_permissions","notify_badge","password","is_verified","email","campus_id","visible_in_community","show_discord_username","date_joined","last_login")
    
    def get_discord_username(self,instance):
        print(instance)
        if not instance.show_discord_username:
            return None
        return instance.discord_username

    @extend_schema_field(OpenApiTypes.INT)
    def get_total_badges(self,instance):
        count = UserBadge.objects.filter(owner=instance).count()
        return count

    @extend_schema_field(UserBadgeSerializerMinified)
    def get_badges(self,instance):
        if self.context and self.context["request"]:
            modules = self.context['request'].query_params.getlist('modules[]',"")
            if modules:
                user_badges = UserBadge.objects.filter(owner=instance).filter(earned=True).filter(badge__module__in=[int(x) for x in modules]).all()[:10]
            else:
                user_badges = UserBadge.objects.filter(owner=instance).filter(earned=True).all()[:10]
        else:
            user_badges = UserBadge.objects.filter(owner=instance).filter(earned=True).all()[:10]
            
        return UserBadgeSerializerMinified(user_badges,many=True).data


class RefreshPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, data):
        if data["new_password"] != data["new_password_confirm"]:
            raise ValidationError(
                {'new_password_confirm': "The two password fields didn't match."})
        return data