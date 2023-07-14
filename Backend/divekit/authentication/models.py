from django.db import models
from django.contrib.auth.models import AbstractUser
import os,uuid



def update_filename(instance, filename,prefix=None):
    path = "users/"
    extension = filename.split('.')[-1]
    if prefix:
        filename = "%s_%s.%s" % (prefix,uuid.uuid4(), extension)
    else:
        filename = "%s.%s" % (uuid.uuid4(), extension)
    return os.path.join(path, filename)


THEMES = [
    (1,"light"),
    (2,"dark")
]

class User(AbstractUser):
    email                   = models.EmailField(blank=False)
    campus_id               = models.CharField(max_length=15)
    discord_username        = models.CharField(max_length=255, blank=True)
    img                     = models.ImageField(upload_to=update_filename,blank=True,default="users/default_orange.jpg")
    theme                   = models.IntegerField(choices=THEMES, default=1)
    is_verified             = models.BooleanField(default=False)
    visible_in_community    = models.BooleanField(default=True)
    show_discord_username   = models.BooleanField(default=False)
    notify_badge            = models.BooleanField(default=False,blank=True)


    def __repr__(self) -> str:
        return "{}".format(self.campus_id)

