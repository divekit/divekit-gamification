from django.urls import path

from .views import BadgeView, UserBadgeListView,ModuleListView

urlpatterns = [
    path('badges/', BadgeView.as_view()),
    path("userBadges/",UserBadgeListView.as_view()),
    path("modules/",ModuleListView.as_view())
]