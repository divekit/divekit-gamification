from django.contrib import admin
from .models import Badge,UserBadge,Module, BadgeAdmin, UserBadgeAdmin,ModuleAdmin

admin.site.register(Badge,BadgeAdmin)
admin.site.register(UserBadge, UserBadgeAdmin)
admin.site.register(Module,ModuleAdmin)
# Register your models here.


