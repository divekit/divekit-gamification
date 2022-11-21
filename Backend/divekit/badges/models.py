from django.db import models
import uuid, os
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


def update_filename(instance, filename,prefix=None):
    path = "badges/"
    extension = filename.split('.')[-1]
    if prefix:
        filename = "%s_%s.%s" % (prefix,uuid.uuid4(), extension)
    else:
        filename = "%s.%s" % (uuid.uuid4(), extension)
    return os.path.join(path, filename)



class Module(models.Model):
    name = models.CharField(max_length=255)
    acronym = models.CharField(max_length=15)
    old = models.BooleanField(default=False,blank=True)

    def __str__(self):
        return "%s - (%s)" % (self.acronym,self.name)

class Badge(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    img = models.ImageField(upload_to=update_filename)
    milestones = models.IntegerField(default=1,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_unique = models.BooleanField(default=True, null=False)
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True, default=None)

    # def save(self):
    #     if self.badge.is_unique:
    #         if UserBadge.objects.exclude(pk=self.pk).filter(owner=self.owner,badge=self.badge):
    #             raise ValidationError('This Badge (%s-%s) is unique and therefore cannot be assigned twice to a user' % (self.badge.id, self.badge.name))
    #     return super(UserBadge,self).validate_unique(exclude=exclude)

    def __str__(self):
        return "%s - %s (%sM)" % (self.pk,self.name,str(self.milestones))

class BadgeAdmin(admin.ModelAdmin):
    list_display = ['pk', "name", 'description']

@receiver(post_save,sender = Badge, dispatch_uid="update_user_progress")
def update_user_progress(sender,**kwargs):
    updated_badge = kwargs["instance"]
    user_badges = UserBadge.objects.filter(badge__pk=updated_badge.pk,progress__gt=updated_badge.milestones).all()
    if user_badges:
        for user_badge in user_badges:
            print(user_badge.progress)
            user_badge.progress = updated_badge.milestones
            user_badge.save()
    # print(kwargs)
    
    # print(updated_badge)


class UserBadge(models.Model):
    owner = models.ForeignKey("authentication.User",on_delete=models.CASCADE,related_name="badges")
    badge = models.ForeignKey(Badge,on_delete=models.CASCADE)
    progress = models.IntegerField(default=1)
    earned = models.BooleanField(default=False, editable=False)
    earned_at = models.DateTimeField(null=True, blank=True, editable=False)
    last_progress_at = models.DateTimeField(auto_now=True)
    
    def clean(self):
        super(UserBadge,self).clean()
        if self.progress > self.badge.milestones:
            raise ValidationError("Progress cannot be bigger than milestone count!")

    def save(self,*args,**kwargs):
        self.clean()
        if( self.progress == self.badge.milestones):
            self.earned = True
            self.earned_at = timezone.now()
        else:
            self.earned = False
            self.earned_at = None
        super().save(*args,**kwargs)

    def __str__(self):
        return "%s - %s (%s/%s)" % (self.owner.username, self.badge.name, self.progress, self.badge.milestones)

    def validate_unique(self, exclude=None):
        if self.badge.is_unique:
            if UserBadge.objects.exclude(pk=self.pk).filter(owner=self.owner,badge=self.badge):
                raise ValidationError('This Badge (%s-%s) is unique and therefore cannot be assigned twice to a user' % (self.badge.id, self.badge.name))
        return super(UserBadge,self).validate_unique(exclude=exclude)

    

class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ["link_to_pk", "link_to_user", 'link_to_badge',"get_progress","get_last_progress_at","earned","earned_at"]

    search_fields = ['pk',"badge__name__icontains","last_progress_at__icontains","progress","badge__milestones","owner__username__icontains"]

    # pk.admin_order_field = 'last_progress_at'
    def link_to_pk(self, obj):
        link = reverse("admin:badges_userbadge_change", args=[obj.pk])
        return format_html('<a href="{}">{}</a>', link, obj.pk)
    link_to_pk.admin_order_field = 'pk'
    link_to_pk.short_description = 'ID'  

    def get_last_progress_at(self,obj):
        return obj.last_progress_at.strftime("%d.%m.%Y %H:%M:%S")
    get_last_progress_at.admin_order_field = 'last_progress_at'
    get_last_progress_at.short_description = 'Last Progress At'  

    def get_progress(self,obj):
        return "%s/%s" % (obj.progress, obj.badge.milestones)
    get_progress.short_description = 'Progress'

    def link_to_user(self, obj):
        link = reverse("admin:authentication_user_change", args=[obj.owner.id])
        return format_html('<a href="{}">{}</a>', link, obj.owner.username)
    link_to_user.short_description = 'User'

    def link_to_badge(self,obj):
        link = reverse("admin:badges_badge_change", args=[obj.badge.id])
        return format_html('<a href="{}">{}</a>', link, obj.badge.name)
    link_to_badge.short_description = 'Badge'


    # list_display_links = ['owner', 'badge']