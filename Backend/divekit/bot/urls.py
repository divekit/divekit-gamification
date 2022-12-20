from django.urls import path

from .views import VerificationsListView

urlpatterns = [
    path('bot/verifications/', VerificationsListView.as_view()),
]