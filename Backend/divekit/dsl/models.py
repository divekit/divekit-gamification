import os
import uuid
from django.db import models


def dkb_file_path(instance, filename, prefix=None):
    path = "dkbFiles/"
    extension = filename.split('.')[-1]
    if prefix:
        filename = "%s_%s.%s" % (prefix, uuid.uuid4(), extension)
    else:
        filename = "%s.%s" % (uuid.uuid4(), extension)
    return os.path.join(path, filename)


class DKBFile(models.Model):
    file = models.FileField(upload_to=dkb_file_path)
    title = models.CharField(max_length=255,null=True,blank=True)
    # text = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "authentication.User", on_delete=models.CASCADE)
    
    def __str__(self):
        return "{}-{}".format(self.pk,self.title)
