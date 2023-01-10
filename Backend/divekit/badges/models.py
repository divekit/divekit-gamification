from django.db import models
import uuid, os
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import resolve
from django.db.models.fields.files import FieldFile
from django.db.models.fields.files import ImageFieldFile


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
    active = models.BooleanField(default=True,blank=True)

    def __str__(self):
        return "%s - (%s)" % (self.acronym,self.name)

@admin.action(description='Mark as active')
def make_active(modeladmin, request, queryset):
    queryset.update(active=True)

@admin.action(description='Mark as deactive')
def make_deactive(modeladmin, request, queryset):
    queryset.update(active=False)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['pk', "link_to_name", 'acronym',"active"]
    search_fields = ['pk',"name__icontains","acronym__icontains"]
    actions = [make_active,make_deactive]
    def link_to_name(self, obj):
        link = reverse("admin:badges_module_change", args=[obj.pk])
        return format_html('<a href="{}">{}</a>', link, obj.name)
    link_to_name.admin_order_field = 'name'
    link_to_name.short_description = 'Name'  


class Badge(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    img = models.ImageField(upload_to=update_filename, blank=True)
    milestones = models.IntegerField(default=1,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_unique = models.BooleanField(default=True, null=False)
    is_hidden = models.BooleanField(default=False, null=False)
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True, default=None)

    # def save(self):
    #     if self.badge.is_unique:
    #         if UserBadge.objects.exclude(pk=self.pk).filter(owner=self.owner,badge=self.badge):
    #             raise ValidationError('This Badge (%s-%s) is unique and therefore cannot be assigned twice to a user' % (self.badge.id, self.badge.name))
    #     return super(UserBadge,self).validate_unique(exclude=exclude)

    def __str__(self):
        return "%s - %s (%sM)" % (self.pk,self.name,str(self.milestones))



class BadgeAdmin(admin.ModelAdmin):
    list_display = ['link_to_pk', "link_to_name", 'description',"link_to_module"]
    search_fields = ['pk',"name__icontains","description__icontains"]
    save_as = True

    def link_to_pk(self, obj):
        link = reverse("admin:badges_badge_change", args=[obj.pk])
        return format_html('<a href="{}">{}</a>', link, obj.pk)
    link_to_pk.admin_order_field = 'pk'
    link_to_pk.short_description = 'ID'  

    def link_to_name(self, obj):
        link = reverse("admin:badges_badge_change", args=[obj.pk])
        return format_html('<a href="{}">{}</a>', link, obj.name)
    link_to_name.admin_order_field = 'name'
    link_to_name.short_description = 'Name'  

    def link_to_module(self, obj):
        link = reverse("admin:badges_module_change", args=[obj.module.id])
        return format_html('<a href="{}">{}</a>', link, obj.module.name)
    link_to_module.admin_order_field = 'module'
    link_to_module.short_description = 'Module'

    def save_model(self, request, obj, form, change):
    # Django always sends this when "Save as new is clicked"
        if '_saveasnew' in request.POST:
            # Get the ID from the admin URL
            original_pk = request.resolver_match.kwargs['object_id']
            print(original_pk)

            # Get the original object
            original_obj = obj._meta.concrete_model.objects.get(id=original_pk)

            # Iterate through all it's properties
            for prop, value in vars(original_obj).items():
                # if the property is an Image (don't forget to import ImageFieldFile!)
                if isinstance(getattr(original_obj, prop), ImageFieldFile):
                    setattr(obj, prop, getattr(original_obj, prop))  # Copy it!
        obj.save()

@receiver(post_save,sender = Badge, dispatch_uid="update_user_progress")
def update_user_progress(sender,**kwargs):
    updated_badge = kwargs["instance"]
    user_badges = UserBadge.objects.filter(badge__pk=updated_badge.pk,progress__gt=updated_badge.milestones).all()
    if user_badges:
        for user_badge in user_badges:
            print(user_badge.progress)
            user_badge.progress = updated_badge.milestones
            user_badge.save()


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