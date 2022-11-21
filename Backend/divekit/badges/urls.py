from django.urls import path

from .views import BadgeView, UserBadgeListView

urlpatterns = [
    path('badges/', BadgeView.as_view()),
    path("userBadges/",UserBadgeListView.as_view())
    # path('dictionaries/', DictionaryView.as_view(), name='dictionaries'),
    # path('dictionaries/<int:pk>/',
    #      DictionaryDetailView.as_view(), name="dictionary"),
]