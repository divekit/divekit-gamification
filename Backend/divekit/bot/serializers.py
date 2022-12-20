from rest_framework import serializers
from .models import Verification
from django.core.exceptions import ValidationError


class VerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verification
        fields = "__all__"
