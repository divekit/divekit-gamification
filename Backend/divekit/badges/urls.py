from django.urls import path

from .views import BadgeView, UserBadgeListView,ModuleListView,UserBadgeDetailView,TestView

urlpatterns = [
    path('badges/', BadgeView.as_view()),
    # path("userBadges/",UserBadgeListView.as_view()),
    path("users/<int:user_id>/badges/",UserBadgeListView.as_view(),name="user_badges"),
    path("users/<int:user_id>/badges/<int:badge_id>/",UserBadgeDetailView.as_view(),name="user_badge"),
    path("modules/",ModuleListView.as_view()),
    path("test/",TestView.as_view())
]