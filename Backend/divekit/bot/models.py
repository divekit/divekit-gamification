from django.db import models
import uuid, os
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class Verification(models.Model):
    owner = models.ForeignKey("authentication.User",on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return "%s - (%s)" % (self.owner.username,self.owner.discord_username)


class Notification(models.Model):
    owner = models.ForeignKey("authentication.User",on_delete=models.CASCADE)
    message = models.CharField(max_length=512)
    sent = models.BooleanField(default=False)
    
    def clean(self):
        
        if not self.owner.notify_badge:
            raise ValidationError('The user does not allow to send notifications.')