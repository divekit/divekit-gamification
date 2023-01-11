from django.urls import path

from .views import VerificationsListView,NotificationListView

urlpatterns = [
    path('bot/verifications/', VerificationsListView.as_view()),
    path('bot/notifications/', NotificationListView.as_view()),
]